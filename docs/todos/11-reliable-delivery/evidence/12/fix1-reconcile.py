#!/usr/bin/env python3
"""Reconcile preserved native events; never mutate historic evidence or task state."""
import hashlib
import json
import subprocess
from pathlib import Path

D = Path('docs/todos/11-reliable-delivery/evidence/12')
BASE = '305f1d49d499ae3a5112358d57c2fefa48349261'
EXPECTED = {
    'codeg-probe-v2-native-excerpt.jsonl': '794da4df789e5eb6e9106f683fdebfd17049b0eba2b119597d8227eeaeb1174c',
    'codeg-interruption-decision.json': '5f875aead0b6230493a0c518e85acd07c92508931b22a4a0c1343e7082847ee1',
    'codeg-interruption-terminal.json': 'fab5085b8bb65dfa4a12de2e15e676e76ec1de6caec64cde3a4467b1947ace27',
    'review-round1-input.json': '83793a2e524093f8a65158e6f2f7a451ccc3bdc49ddd347e2c1875d2e11d2fc2',
}
EXPECTED_IDS = [
    'exec-8ab4cc65-d73a-4fa2-8531-383d929dd495', 'exec-3ebd2bdb-d82c-479e-aaa9-83af29674778',
    'exec-8636abde-9545-4dd3-abc4-0adc0b1ab756', 'exec-e12979c7-3100-4dff-81e9-df87ff4e4edf',
    'exec-d839a07c-acc8-43f6-a37c-79ed011cf48e', 'exec-a2649b2d-f462-4c2f-a0b6-3b548b4a46e8',
    'exec-51d7fb94-01eb-4847-8c97-11fd7e3d053e', 'exec-08529fd8-6fe9-443f-b0d3-3f22a344b057',
    'exec-9dfa64ad-ce76-47c1-b701-54a23b5bd204', 'exec-05d129b8-05e1-490e-a90a-435bde2a59bc',
]
sha = lambda b: hashlib.sha256(b).hexdigest()
def source_hashes():
    return {name: sha((D/name).read_bytes()) for name in EXPECTED}
assert source_hashes() == EXPECTED, 'original source hash mismatch'
for name in list(EXPECTED)[:3]:
    committed = subprocess.run(['git', 'show', f'{BASE}:{D/name}'], check=True, capture_output=True).stdout
    assert sha(committed) == EXPECTED[name], f'original differs from committed {name}'
raw = (D/'codeg-probe-v2-native-excerpt.jsonl').read_bytes()
lines = raw.splitlines(keepends=True)
events = [json.loads(line) for line in lines]
def ref(index):
    return {'path': str(D/'codeg-probe-v2-native-excerpt.jsonl'), 'line': index+1,
            'line_sha256_including_newline': sha(lines[index]), 'timestamp': events[index]['timestamp'],
            'ordinal': events[index].get('ordinal')}
assert len(events) == 59
starts = [i for i,e in enumerate(events) if e['type']=='response_item' and e['payload']['type']=='custom_tool_call']
outputs = [i for i,e in enumerate(events) if e['type']=='response_item' and e['payload']['type']=='custom_tool_call_output']
terms = [i for i,e in enumerate(events) if e['type']=='event_msg' and e['payload'].get('type')=='item_completed' and e['payload'].get('item',{}).get('type')=='CommandExecution']
actual_starts = [i for i,e in enumerate(events) if e['type']=='event_msg' and e['payload'].get('type')=='item_started' and e['payload'].get('item',{}).get('type')=='CommandExecution']
assert [i+1 for i in starts] == [13,20,28,34,47,53]
assert [i+1 for i in outputs] == [14,22,30,41,49,55]
assert [i+1 for i in terms] == [21,29,35,36,37,38,39,40,48,54]
assert not actual_starts, 'unexpected native CommandExecution start events'
assert [events[i]['payload']['item']['id'] for i in terms] == EXPECTED_IDS
assert len(set(EXPECTED_IDS)) == 10
calls=[]; commands=[]
for begin,end in zip(starts,outputs):
    call=events[begin]['payload']; out=events[end]['payload']
    assert call['call_id']==out['call_id'] and begin<end
    group=[i for i in terms if begin<i<end]
    text=''.join(x.get('text','') for x in out['output'])
    c={'call_id':call['call_id'], 'call_source':ref(begin), 'output_source':ref(end),
       'call_input':call['input'], 'call_input_sha256_utf8':sha(call['input'].encode()),
       'tool_output_sha256_utf8':sha(text.encode()), 'command_ids':[events[i]['payload']['item']['id'] for i in group]}
    calls.append(c)
    for i in group:
        item=events[i]['payload']['item']
        assert item['status']=='completed' and type(item['exit_code']) is int and item['exit_code']==0
        assert item['command'] and item['cwd'] and item['aggregated_output'] is not None
        commands.append({'id':item['id'],'process_id':item.get('process_id'),'cwd':item['cwd'],
            'argv':item['command'],'status':item['status'],'exit_code':item['exit_code'],
            'event_source':ref(i),'native_thread_id':events[i]['payload']['thread_id'],
            'native_turn_id':events[i]['payload']['turn_id'],'native_source':item.get('source'),
            'aggregated_output_sha256_utf8':sha(item['aggregated_output'].encode()),
            'call_id':call['call_id'],'call_source':ref(begin),'tool_output_source':ref(end),
            'native_command_started_at':None,'start_note':'No CommandExecution item_started event in this excerpt; call timestamp is not process start.',
            'runner_tree_terminal':'UNKNOWN; native exit is not runner process-tree proof'})
assert [c['id'] for c in commands]==EXPECTED_IDS
assert not calls[0]['command_ids'] and 'bwrap: Can\'t mount proc on /proc' in ''.join(x.get('text','') for x in events[outputs[0]]['payload']['output'])
assert events[-1]['payload']['type']=='turn_aborted'
old=json.loads((D/'codeg-interruption-terminal.json').read_text())
assert len(old['commands'])==2 and not set(EXPECTED_IDS)&{x['id'] for x in old['commands']}
assert source_hashes()==EXPECTED
inventory={'version':1,'source':{'path':str(D/'codeg-probe-v2-native-excerpt.jsonl'),'sha256':EXPECTED['codeg-probe-v2-native-excerpt.jsonl'],'committed_base':BASE},
  'session_task_id':'083b45e8-276c-4509-8720-0c2c9c8ff6a4','calls':calls,'commands':commands,
  'not_started':{'call_id':calls[0]['call_id'],'call_source':calls[0]['call_source'],'output_source':calls[0]['output_source'],
    'reason':'bwrap failed to mount /proc before command launch','command_exit_code':None,'command_id':None},
  'limitations':['Invocation timestamps are tool-call timestamps; individual process start times are unknown.',
    'Tool-call group association follows event ordering inside each call/output interval; no per-item call ID is present.',
    'Raw native exit/status are not independently proven runner tree termination.',
    'Excerpt covers observed session events; process-tree state beyond native observations remains UNKNOWN.']}
terminal={'version':1,'kind':'retrospective reconciliation, not replacement for original grant terminal',
  'original_terminal':{'path':str(D/'codeg-interruption-terminal.json'),'sha256':EXPECTED['codeg-interruption-terminal.json'], 'commands':old['commands']},
  'original_decision':{'path':str(D/'codeg-interruption-decision.json'),'sha256':EXPECTED['codeg-interruption-decision.json'],
    'correction':'The original claim that source-reading calls exposed no inner exit metadata is contradicted by ten native terminal events.'},
  'session':{'task_id':inventory['session_task_id'],'status':'canceled','status_source':str(D/'codeg-probe-v2-chain.json'),'turn_aborted_event':ref(58)},
  'native_inventory':str(D/'fix1-native-command-inventory.json'),'native_completed_count':10,
  'native_command_ids':EXPECTED_IDS,'not_started_call_id':calls[0]['call_id'],
  'omission':'Original grant terminal omitted all ten source-reading CommandExecution items; its two entries are other commands.',
  'unknown':'No CommandExecution item_started timestamps or independent runner process-tree terminal receipts for those ten commands. This record is not retroactively bound to the consumed grant.'}
disposition={'version':1,'type':'draft; not authorization or execution', 'finding_F2':'Original inventory incomplete; retrospective reconciliation produced, subject to independent review.',
 'finding_F1':'BLOCKED: original explicit checkpoint-resume authority is absent from cited records; prior general-authorization interpretation remains historical FAIL. No inference that authorization never existed.',
 'historic_grant':'Issued/consumed as recorded, but authority unestablished; this draft cannot retroactively validate it or bind a new inventory to it.',
 'required_next':'Controller obtain explicit authority/recovery disposition, reassess affected candidate and obtain new compliant consumption and independent review under the recovery contract; no grant or resume is authorized by this draft.',
 'sources':[str(D/'fix1-native-command-inventory.json'),str(D/'fix1-reconciled-terminal.json'),str(D/'review-round1-input.json')],
 'scope':'Evidence reconciliation only; no product/iteration approval, new grant, card mutation or delegation.'}
for name,obj in [('fix1-native-command-inventory.json',inventory),('fix1-reconciled-terminal.json',terminal),('fix1-recovery-disposition-draft.json',disposition)]:
    p=D/name
    with p.open('x',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n')
assert source_hashes()==EXPECTED
print('PASS: 6 tool calls and outputs; 10 unique completed native commands matched exact lines/IDs/exit metadata; bwrap not started; original 3 committed sources and review input unchanged.')
print('Native command process starts and independent tree terminals UNKNOWN; F1 BLOCKED; no recovery authorization or approval inferred.')
