"""Read original self-use records; emit bounded task06 evidence, not approval."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'scripts'))
from iter_contracts import parse_card
from iter_autonomy import load_state

IT = Path('docs/todos/10-self-hosting-hardening')
OUT = IT / 'evidence/06'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def write(name, value):
    path = ROOT / OUT / name
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


cards = []
for number in range(1, 6):
    card = next((ROOT / IT).glob(f'{number:02}-*.md'))
    meta, _, errors = parse_card(card.read_text(encoding='utf-8-sig'))
    receipt = read(meta['review_receipt'])
    events = load_state(meta)['events']
    cards.append(dict(task=f'{number:02}', card=card.relative_to(ROOT).as_posix(),
        declared_status=meta['status'], base=meta['base_sha'], candidate=meta['head_sha'],
        review_receipt=meta['review_receipt'], review_report=receipt['review_report'],
        verdict=receipt['verdict'], reviewer=receipt['reviewer'], implementer=receipt['implementer'],
        checks=receipt['checks'], parse_errors=errors,
        events=[dict(id=eid, action=e['input']['action'], owner=e['input']['owner'],
                     at=e.get('at'), evidence=e['input'].get('evidence')) for eid, e in events.items()]))

chain = []
for label in 'abc':
    directory = IT / 'evidence/03'
    native_path = directory / f'native-terminal-{label}.json'
    native = read(native_path)
    attempt_path = directory / f'attempt-{label}.json'
    attempt = read(attempt_path)
    context_path = directory / f'context-implementation-{label}.json'
    context = read(context_path)['tasks']['03']
    handoff_path = directory / f'handoff-{label}.json'
    handoff = read(handoff_path)['TASK_HANDOFF']
    dispatch_path = directory / f'dispatch-{label}.json'
    dispatch = read(dispatch_path)
    commands = []
    for path in attempt['commands']:
        command = read(path)
        commands.append(dict(receipt=path, candidate_at_attempt=attempt['candidate'],
            status=command['status'], raw_exit_code=command['raw_exit_code'],
            tree_terminal=command['tree_terminal'], output=command['output']))
    chain.append(dict(slice=label, context=str(context_path).replace('\\','/'), context_candidate=context['candidate'],
        context_inputs=context['inputs'], native=str(native_path).replace('\\','/'),
        task_id=native['dispatch']['structuredContent']['task_id'],
        session=native['dispatch']['structuredContent']['child_conversation_id'],
        terminal=native['guard']['final']['status'], terminal_confirmed=native['guard']['terminalConfirmed'],
        dispatch=str(dispatch_path).replace('\\','/'), readiness=dispatch['readiness'],
        attempt=str(attempt_path).replace('\\','/'), candidate=attempt['candidate'], commands=commands,
        handoff=str(handoff_path).replace('\\','/'), released_writer=handoff['writer'],
        checkpoint=handoff['execution']['checkpoint'], remaining_work=handoff['execution']['remaining_work']))

targeted = read(OUT / 'slice-a-targeted-2.json')
strict = read(OUT / 'slice-a-frozen-strict-dry-run.json')
assert targeted['status'] == 'COMPLETED' and targeted['raw_exit_code'] == 0 and targeted['tree_terminal']
assert len({s['task_id'] for s in chain}) == 3
assert all(s['terminal'] == 'completed' and s['terminal_confirmed'] and not s['released_writer'] for s in chain)
assert all(c['tree_terminal'] for s in chain for c in s['commands'])
assert strict['status'] == 'COMPLETED' and strict['tree_terminal']
strict_output = (ROOT / strict['output']).read_text(encoding='utf-8-sig')
assert '验收PASS: 5/6' in strict_output and 'Uncommitted candidate changes' in strict_output
inventory = dict(version=1, observed_candidate='7107ddb2f2256ceaea40e6ea0aeddd045220b99b',
    cards=cards, complete_chain=dict(task='03', inventory=str(IT/'evidence/03/inventory-a.json').replace('\\','/'),
    inventory_target_readiness=read(IT/'evidence/03/inventory-a.json')['tasks'][2]['readiness'],
    claim=str(IT/'evidence/03/claim-a.json').replace('\\','/'), slices=chain,
    implementation_C=cards[2]['candidate'], registration_D='2ce0705ebeeaee73f75a1dcd2882836dbc6b9d29',
    strict_receipt=str(OUT/'slice-a-frozen-strict-dry-run.json').replace('\\','/'),
    strict_meaning='Current frozen dry-run: prior five task verdicts PASS; whole command exit2 because current06 candidate is uncommitted. Historical strict source remains controller/card record; no exit0 claim'),
    reuse=dict(browser='04 review.json checks retain native interaction, states, visual and 67-pass output; product unchanged by06',
              continuation='03 B context consumes A checkpoint; C context consumes A+B and rulings; before/RED preserved',
              task01='01 card events and implementation-checkpoint-a/b plus native-terminal-implementation-a/b retain additional continuation',
              task05='05 review.json/review-report.json retained; review-final.json/review-report-final.json bind dc5d868 after correct strict body-drift refusal'))
write('native-chain-inventory.json', inventory)
cases = []
def case(id, layer, expected, observed, result, evidence):
    cases.append(dict(id=id, layer=layer, expected=expected, observed=observed, result=result, evidence=evidence))

for id in ('authority/context/writer/candidate/phase/dependency', 'two-empty-attempts', 'idempotency/payload/release/reclaim',
           'bad-number/unknown-DONE', 'FS-source/evidence/body-drift', 'feature-root-index'):
    case(id, 'synthetic', 'Cross-module refusal/persistence contract in isolated fixtures',
         '14 tests passed in 16.36s; first run API signature misuse corrected; original failure retained', 'PASS',
         ['tests/test_self_hosting.py', str(OUT/'slice-a-targeted-2.json').replace('\\','/'), targeted['output']])
case('native-complete-chain-03', 'native-self-use', 'inventory through independent C/D and frozen strict',
     '03 target inventory READY, same controller claim/dispatch; distinct A/B/C completed; receipts/events/review bind actual candidates; current frozen dry-run shows03 PASS but overall exit2 due06 dirty; historical strict retained in controller/card record',
     'PASS', [str(OUT/'native-chain-inventory.json').replace('\\','/'), cards[2]['card'], cards[2]['review_receipt'], str(OUT/'slice-a-frozen-strict-dry-run.json').replace('\\','/')])
case('normal-cross-session-continuation', 'native-self-use', 'New sessions consume valid checkpoints without inventing fresh RED',
     '1714/A ->1715/B ->1716/C, context inputs explicitly include A/B; original before and RED retained; after slower, no speedup claim',
     'PASS', [str(IT/'evidence/03/context-implementation-b.json').replace('\\','/'), str(IT/'evidence/03/context-implementation-c.json').replace('\\','/'), str(OUT/'native-chain-inventory.json').replace('\\','/')])
case('04-browser-reuse', 'native-self-use', 'Reuse unaffected native UI evidence',
     '04 receipt lists real browser, screenshots, four states and 67-pass regression;06 changes no UI product', 'PASS', [cards[3]['review_receipt'], cards[3]['review_report']])
case('05-strict-body-drift', 'native-self-use', 'Reject registration prose drift and require affected review/new binding',
     'Old/new reports retained; final receipt binds dc5d868; frozen dry-run reports prior five task verdicts PASS; overall command exit2 due06 dirty, not a new strict approval', 'PASS',
     [cards[4]['card'], str(IT/'evidence/05/review-report.json').replace('\\','/'), cards[4]['review_receipt'], cards[4]['review_report']])
case('runner/unknown/budgets/resume/FS-grant-existing-definitions', 'static', 'Reuse mature test definitions; final execution by controller',
     'Existing test_iter_run/test_deadline_watch/test_autonomy/test_checkpoint_resume definitions retained; no full run this leaf', 'PASS',
     ['tests/test_iter_run.py', 'tests/test_deadline_watch.py', 'tests/test_autonomy.py', 'tests/test_checkpoint_resume.py'])
case('final-full-regression', 'synthetic', 'Final candidate full tests pass', 'Not run in this leaf; controller owns full run', 'UNKNOWN', [])
case('final-cross-check-and-independent-review', 'native-self-use', 'Frozen/candidate comparison and nonparticipant task06 review', 'Pending controller checkpoint; no self-approval', 'UNKNOWN', [])
write('robustness-report.json', dict(version=1, candidate=inventory['observed_candidate'],
    coordinator_commit='46ded3a4696e3bdb531d06951fce7982fa9db1cd', cases=cases,
    unverified=[dict(item='final full regression plus existing runner/guard/budget/resume/FS-grant behavior', owner='controller'),
        dict(item='final candidate cross-check, scope, independent06 review, C/D and strict', owner='controller'),
        dict(item='deployment/full installed version/new installed session/external user business', owner='separately authorized deployment or business owner')]))
print(json.dumps(dict(cards=len(cards), native_slices=len(chain), report_cases=len(cases), status='TESTING'), ensure_ascii=False))
