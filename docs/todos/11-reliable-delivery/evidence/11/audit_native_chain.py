#!/usr/bin/env python3
"""Read-only task 06 evidence probe. Findings are not independent approval."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
COORD = 'fdcc4cce88635ee81573be5991de11de650659d8'
OWNER = 'iter11-controller-linux-20261115'

class Finding(Exception):
    def __init__(self, result, detail): self.result, self.detail = result, detail

def require(ok, message, result='FAIL'):
    if not ok: raise Finding(result, message)

def read(path):
    p = Path(path)
    if not p.is_absolute(): p = ROOT / p
    try: return p.read_bytes()
    except OSError as e: raise Finding('BLOCKED', f'{path}: {e}; Controller must supply original')

def obj(path):
    try: return json.loads(read(path))
    except (ValueError, UnicodeError) as e: raise Finding('FAIL', f'{path}: malformed JSON: {e}')

def git(*args):
    p = subprocess.run(['git', '-C', str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode: raise Finding('BLOCKED', f'git {args}: {p.stderr.decode(errors="replace")}; Controller must restore Git evidence')
    return p.stdout

def ancestor(a,b): git('merge-base','--is-ancestor',a,b)

def validate_source_index(source):
    """Reject malformed controller input before building case evidence."""
    def mapping(value, where):
        require(isinstance(value, dict), f'{where} must be an object')
        return value
    def field(parent, key, where):
        require(key in parent, f'{where}.{key} missing', 'UNKNOWN')
        return parent[key]
    def string(value, where):
        require(isinstance(value, str) and bool(value.strip()), f'{where} must be a nonempty string')
        return value
    def strings(value, where, minimum=1):
        require(isinstance(value, list) and len(value) >= minimum, f'{where} must be a list with at least {minimum} entries')
        for i, item in enumerate(value): string(item, f'{where}[{i}]')
    top=mapping(source, 'source-index')
    require(type(field(top, 'version', 'source-index')) is int and top['version']==1, 'source-index.version must be 1')
    string(field(top, 'observed_head', 'source-index'), 'source-index.observed_head')
    sources=field(top, 'sources', 'source-index')
    require(isinstance(sources,list) and len(sources)==1, 'source-index.sources must contain one selected source')
    selected=mapping(sources[0], 'sources[0]')
    for key in ('task_id','task_path','selection','inventory','inheritance','checkpoint','envelope','review_report','review_receipt','local_strict','local_strict_call'):
        string(field(selected,key,'sources[0]'),f'sources[0].{key}')
    require(selected['task_id']=='06','selected source must be task 06')
    for key,minimum in (('retained_rejections',3),('extra_sources',5)):
        strings(field(selected,key,'sources[0]'),f'sources[0].{key}',minimum)
    commits=mapping(field(selected,'commits','sources[0]'),'sources[0].commits')
    for key in ('base','checkpoint','candidate','D'):
        string(field(commits,key,'commits'),f'commits.{key}')
    strings(field(commits,'registration','commits'),'commits.registration',2)
    require(len(commits['registration'])==2,'commits.registration must contain two commits')
    stages=field(selected,'stages','sources[0]')
    require(isinstance(stages,list) and len(stages)==6,'stages must contain six entries')
    for i,stage in enumerate(stages):
        where=f'stages[{i}]'; stage=mapping(stage,where)
        for key in ('session_id','candidate','phase','context','guard','native','terminal'):
            string(field(stage,key,where),f'{where}.{key}')
        sid=field(stage,'tool_session_id',where)
        require(type(sid) is int and sid>0,f'{where}.tool_session_id must be a positive integer')
        for key,minimum in (('claims',1),('attempts',2),('releases',1),('runner_receipts',0)):
            strings(field(stage,key,where),f'{where}.{key}',minimum)
        check=mapping(field(stage,'check',where),f'{where}.check')
        for key in ('cwd','request_id'): string(field(check,key,f'{where}.check'),f'{where}.check.{key}')
        strings(field(check,'argv',f'{where}.check'),f'{where}.check.argv')
        terminal=mapping(field(check,'terminal_evidence',f'{where}.check'),f'{where}.check.terminal_evidence')
        for key in ('source','id'): string(field(terminal,key,'terminal_evidence'),f'terminal_evidence.{key}')
        events=field(check,'utc_events',f'{where}.check')
        require(isinstance(events,list) and len(events)==3,f'{where}.check.utc_events must contain three entries')
        for j,event in enumerate(events):
            ew=f'{where}.check.utc_events[{j}]'; event=mapping(event,ew)
            for key in ('kind','utc'): string(field(event,key,ew),f'{ew}.{key}')
            ordinal=field(event,'ordinal',ew); require(type(ordinal) is int and ordinal>=0,f'{ew}.ordinal must be a nonnegative integer')
            try: parsed=datetime.fromisoformat(event['utc'])
            except ValueError: raise Finding('FAIL',f'{ew}.utc must be an ISO timestamp')
            require(parsed.tzinfo is not None and parsed.utcoffset() is not None,f'{ew}.utc must include a timezone')
    observations=field(top,'related_observations','source-index')
    require(isinstance(observations,list) and len(observations)>=3,'related_observations must be a list with all retained cases')
    ids=[]
    for i,observation in enumerate(observations):
        where=f'related_observations[{i}]'; observation=mapping(observation,where)
        ids.append(string(field(observation,'id',where),f'{where}.id'))
        string(field(observation,'path',where),f'{where}.path')
    require(len(ids)==len(set(ids)) and {'codeg-worker-environment','codeg-assessment','root04-order-incident'}<=set(ids),'related observations missing or duplicate')
    entries=field(top,'source_files','source-index')
    require(isinstance(entries,list) and bool(entries),'source_files must be a nonempty list')
    for i,entry in enumerate(entries):
        where=f'source_files[{i}]'; entry=mapping(entry,where)
        string(field(entry,'path',where),f'{where}.path')
        digest=string(field(entry,'sha256',where),f'{where}.sha256')
        require(len(digest)==64 and all(c in '0123456789abcdef' for c in digest),f'{where}.sha256 must be lowercase SHA256')
    return selected,stages

def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument('--sources',required=True); parser.add_argument('--output',required=True); args=parser.parse_args(argv)
    cases=[]; fatal=False; source=None
    native_layer='native-self-use' if args.sources=='docs/todos/11-reliable-delivery/evidence/planning/native-source-index.json' else 'synthetic'
    def case(id, layer, expected, evidence, fn):
        nonlocal fatal
        try: observed=fn(); result='PASS'
        except Finding as e: observed=e.detail+'; Controller must inspect or supply the original before redispatch'; result=e.result; fatal=True
        except (KeyError, TypeError, ValueError, IndexError, OSError, AttributeError, StopIteration, OverflowError) as e: observed=f'malformed or incomplete record: {e}; Controller must supply valid original'; result='UNKNOWN'; fatal=True
        cases.append(dict(id=id,layer=layer,expected=expected,observed=observed,result=result,evidence=evidence))
    try:
        source=obj(args.sources); s,stages=validate_source_index(source)
        candidate=git('rev-parse','HEAD').decode().strip()
    except (Finding,KeyError,TypeError,ValueError,IndexError,AttributeError) as e:
        result=e.result if isinstance(e,Finding) else 'UNKNOWN'; detail=e.detail if isinstance(e,Finding) else str(e)
        cases.append(dict(id='source-index',layer='static',expected='version 1 selected task 06',observed=detail+'; Controller must supply a complete valid source index',result=result,evidence=[args.sources])); fatal=True; candidate=None; s={}; stages=[]; source=None
    def hashes():
        entries=source['source_files']; require(bool(entries),'empty source inventory'); paths=[e['path'] for e in entries]; require(len(paths)==len(set(paths)),'duplicate source hash entries'); required=[s[k] for k in ('selection','inventory','inheritance','checkpoint','envelope','review_report','review_receipt','local_strict','local_strict_call')]+s['retained_rejections']+s['extra_sources'];
        for st in stages:
            required.extend(st[k] for k in ('context','guard','native','terminal'));
            for k in ('claims','attempts','releases','runner_receipts'): required.extend(st[k])
        for ent in entries:
            actual=hashlib.sha256(read(ent['path'])).hexdigest(); require(actual==ent['sha256'],f'hash mismatch: {ent["path"]}; Controller must restore original')
        require(set(required)<=set(paths),'selected original lacks independent source hash')
        return f'{len(entries)} original byte hashes matched independently'
    if source and stages:
        case('source-hashes','static','all selected original SHA256 values match',[args.sources],hashes)
        def ownership():
            p='docs/todos/11-reliable-delivery/evidence/11/controller-artifact-ownership.json'; d=obj(p); require(len(d['files'])==28,'ownership expected 28 files')
            for e in d['files']: require(hashlib.sha256(read(e['path'])).hexdigest()==e['sha256'],f'ownership hash mismatch {e["path"]}')
            return '28 Controller-only input hashes match; 27 startup/migration originals plus index; no replan or budget reset'
        def frozen():
            cm=obj('docs/todos/11-reliable-delivery/evidence/planning/coordinator-manifest.json'); require(cm['source_commit']==COORD, 'coordinator manifest commit mismatch');
            for name in ('scripts/iter_sync.py','scripts/iter_contracts.py','references/task_card_schema.md'):
                entry=next(e for e in cm['files'] if e['path']==name); data=read(str(Path(cm['root'])/name)); require(hashlib.sha256(data).hexdigest()==entry['sha256']==hashlib.sha256(git('show',COORD+':'+name)).hexdigest(),f'frozen coordinator byte mismatch {name}')
            rm=obj('/data/workspace/iteration-manager/build/frozen-runners/iter11-platform-v1/manifest.json'); require(rm['coordinator_commit']==COORD,'runner coordinator mismatch');
            for e in rm['files']:
                data=read('/data/workspace/iteration-manager/build/frozen-runners/iter11-platform-v1/'+e['path']); require(hashlib.sha256(data).hexdigest()==e['sha256']==hashlib.sha256(git('show',rm['source_commit']+':'+e['path'])).hexdigest(),f'frozen runner mismatch {e["path"]}')
            return 'coordinator entry/contracts and all approved platform runner snapshot bytes match their source commits and manifests'
        case('frozen-tool-identity','static','frozen coordinator and platform runner match Git bytes and manifests',['docs/todos/11-reliable-delivery/evidence/planning/coordinator-manifest.json','/data/workspace/iteration-manager/build/frozen-runners/iter11-platform-v1/manifest.json'],frozen)
        case('ownership','static','28 exact Controller input hashes', ['docs/todos/11-reliable-delivery/evidence/11/controller-artifact-ownership.json'],ownership)
        def stage_check(st):
            g=obj(st['guard']); req=g['request']; c=st['check']; ev=g['events']; rc=g['result']['check']; native_check=g['native_check']; nc=json.loads(native_check['output']) if 'output' in native_check else native_check; response=json.loads(nc['stdout'])
            for key,value in [('task_id','06'),('owner',OWNER),('candidate',st['candidate']),('phase',st['phase']),('context',st['context']),('request_id',c['request_id'])]: require(req[key]==value,f'guard {key} mismatch: {st["guard"]}')
            ctx=obj(st['context'])['tasks']['06']; require(ctx['candidate']==st['candidate'] and ctx['phase']==st['phase'] and ctx['tool_entry']==req['tool_entry'], 'context identity mismatch')
            require(req['project_root']==c['cwd'] and req['task_path']==c['argv'][c['argv'].index('--dispatch-check')+1] and c['argv'][c['argv'].index('--context')+1]==st['context'] and c['argv'][c['argv'].index('--phase')+1]==st['phase'] and c['argv'][c['argv'].index('--owner')+1]==OWNER, 'guard argv context/cwd/task mismatch')
            require([e['kind'] for e in ev]==['check-start','check-terminal-consumed','dispatch-call'],'guard event order inversion')
            require(all(ev[i]['at']<=ev[i+1]['at'] for i in (0,1)), 'guard timestamps inverted')
            u=c['utc_events']; require([x['kind'] for x in u]==[x['kind'] for x in ev] and [x['ordinal'] for x in u]==[0,1,2], 'index event order inversion')
            require(all(datetime.fromisoformat(u[i]['utc']).timestamp()*1000 == ev[i]['at'] for i in range(3)), 'index/guard times mismatch')
            require(c['argv']==rc['argv']==nc['argv'] and c['cwd']==rc['cwd'] and ev[0].get('argv',c['argv'])==c['argv'] and ev[0].get('cwd',c['cwd'])==c['cwd'] and nc.get('cwd',c['cwd'])==c['cwd'],'check argv/cwd mismatch')
            require(ev[1]['exit_code']==0 and ev[1]['readiness']=='READY' and rc['state']=='completed' and rc['exit_code']==0 and rc['request_id']==ev[2].get('request_id',c['request_id'])==c['request_id'] and rc['terminal_evidence']==c['terminal_evidence'] and response['candidate']==st['candidate'] and response['phase']==st['phase'] and response['task_id']=='06' and response['readiness']=='READY','completed check identity/readiness mismatch')
            require((native_check.get('chunk_id')==c['terminal_evidence']['id'] if 'output' in native_check else obj(c['terminal_evidence']['source'])==native_check and native_check['ended_at']==c['terminal_evidence']['id']) and g['result']['dispatched'] is True,'dispatch or terminal evidence mismatch')
            t=obj(st['terminal']); monitor=t['monitor']; require(monitor['terminalConfirmed'] is True and monitor['final']['status']=='completed' and monitor['final']['raw']['exit_code']==0,'wrapper terminal unknown','UNKNOWN')
            require(t['launch']['launch']['session_id']==st['tool_session_id'] and t==g['result']['delegation'], 'dispatch wrapper identity mismatch')
            try: lines=[json.loads(line) for line in read(st['native']).splitlines()]
            except ValueError as e: raise Finding('FAIL',f'malformed JSONL: {e}')
            require([x['thread_id'] for x in lines if x.get('type')=='thread.started']==[st['session_id']], 'native thread identity mismatch')
            terminal=[x['type'] for x in lines if x.get('type') in ('turn.completed','turn.failed')]; require(terminal==['turn.completed'],'native turn terminal unknown','UNKNOWN')
            a=obj(st['attempts'][0]); require(a['executor_id']==st['session_id'] and a['candidate']==st['candidate'] and a['phase']==st['phase'] and a['terminal_evidence']==st['terminal'],'attempt mismatch')
            for k in ('claims','attempts','releases'):
                for p in st[k]:
                    o=obj(p)
                    if 'argv' in o:
                        require(o['exit_code']==0 and '--owner' in o['argv'] and o['argv'][o['argv'].index('--owner')+1]==OWNER, f'event call invalid {p}')
            claim=obj(st['claims'][0]); attempt_call=obj(st['attempts'][1]); release=obj(st['releases'][0]); require(claim['ended_at']<=attempt_call['started_at']<=attempt_call['ended_at']<=release['started_at'], 'claim/attempt/release time inversion'); require(attempt_call['argv'][attempt_call['argv'].index('--evidence')+1]==st['attempts'][0] and release['argv'][release['argv'].index('--evidence')+1]==st['terminal'], 'event evidence mismatch')
            for p in st['runner_receipts']:
                r=obj(p); require(r['status']=='COMPLETED' and r['tree_terminal'] is True and r['command']['status']=='COMPLETED' and r['command']['tree_terminal'] is True and r['command']['raw_exit_code']==r['raw_exit_code'],f'runner terminal unknown {p}','UNKNOWN'); require(bool(read(r['output'])),f'empty raw output {p}','UNKNOWN')
            return f'{st["session_id"]:s}; {st["phase"]}; completed check, dispatch, native and wrapper terminals, events and {len(st["runner_receipts"])} runner receipts bound'
        for i,st in enumerate(stages): case(f'stage-{i+1}', native_layer,'bound owner/candidate/check/dispatch/session/terminal/events', [st['guard'],st['native'],st['terminal'],*st['attempts'],*st['releases'],*st['runner_receipts']],lambda st=st:stage_check(st))
        def continuation():
            cp=obj(s['checkpoint']); inh=obj(s['inheritance']); red=obj(cp['raw_receipt']); env=obj(s['envelope']); raw=read(cp['raw_output']).decode(errors='replace'); commits=s['commits']; p=commits['checkpoint']
            require(cp['native_session_uuid']==stages[0]['session_id']==stages[2]['session_id'] and inh['consumer_session_id']==stages[1]['session_id']!=stages[0]['session_id'] and inh['original_implementer_session_id']==stages[0]['session_id'],'implementer/consumer mismatch')
            require(inh['head']==p==stages[1]['candidate']==stages[2]['candidate'] and cp['base_sha']==commits['base']==inh['original_red_candidate'],'checkpoint candidate mismatch')
            ancestor(commits['base'],p); require(hashlib.sha256(git('show',p+':'+cp['test_source'])).hexdigest()==cp['sha256'][cp['test_source']]==inh['verified_sha256'][cp['test_source']], 'checkpoint test blob hash mismatch')
            for path,h in cp['sha256'].items():
                if path!=cp['test_source']: require(hashlib.sha256(read(path)).hexdigest()==h==inh['verified_sha256'][path],f'original RED hash mismatch {path}')
            require(red['raw_exit_code']==1 and red['status']=='COMPLETED' and red['tree_terminal'] is True and '22 failed' in raw and '11 passed' in raw and 'AssertionError' in raw,'RED assertion evidence mismatch')
            require(inh['original_red_started_at']==red['started_at'] and inh['original_red_ended_at']==red['ended_at'],'inherited RED timestamps mismatch')
            envelope=json.loads(env['stdout'])['TASK_HANDOFF']; last=envelope['execution']['last_attempt']; require(last['executor_id']==stages[0]['session_id'] and last['commands'][0]['receipt']==cp['raw_receipt'] and last['commands'][0]['started_at']==red['started_at'] and last['commands'][0]['ended_at']==red['ended_at'],'envelope did not inherit original RED')
            require(inh['event_observation']['budget_reset_observed'] is False and all(envelope[k]==0 for k in ('fix_rounds','fix_total','consilium_count','replan_count')) and not stages[1]['runner_receipts'],'consumer rerun or budget evidence mismatch')
            require(git('show',commits['candidate']+':'+cp['test_source']).startswith(git('show',p+':'+cp['test_source'])), 'RED test is not prefix of final test'); green=obj(stages[2]['runner_receipts'][-1]); require(green['raw_exit_code']==0 and '39 passed' in read(green['output']).decode(), 'final GREEN raw evidence mismatch'); require('resume '+stages[0]['session_id'] in obj(stages[2]['terminal'])['launch']['cmd'],'same implementer resume missing')
            return 'P='+p+'; distinct consumer inherited original RED hashes/times; same thread resumed GREEN; runtime identity beyond observed versions remains unknown'
        case('checkpoint-continuation',native_layer,'original RED at P inherited without rerun/reset and same implementer GREEN',[s['checkpoint'],s['inheritance'],s['envelope'],stages[2]['terminal']],continuation)
        def reviews():
            c=s['commits']; c1=stages[3]['candidate']; c2=c['candidate']; d1,d2=c['registration']; ancestor(c['checkpoint'],c1); ancestor(c1,c2); ancestor(c2,d1); ancestor(d1,d2); ancestor(d2,candidate)
            pre=obj(s['retained_rejections'][0]); report=obj(s['review_report'])['independent_review']; receipt=obj(s['review_receipt']); require(pre['candidate']==c1 and pre['verdicts']['overall']=='NEEDS_FIX' and any(x['id']=='F1' for x in pre['findings']),'C1 rejection missing')
            require(report['candidate']==c2 and report['verdicts']['overall']=='APPROVED' and any(x['id']=='F1' and x['status']=='ADDRESSED' for x in report['prior_findings']),'C2 independent review mismatch')
            require(receipt['head_sha']==c2 and receipt['base_sha']==c['base'] and receipt['contract_sha']==c['base'] and receipt['implementer']==stages[0]['session_id'] and receipt['reviewer']==stages[5]['session_id']!=receipt['implementer'],'receipt candidate/contract/identity mismatch'); ancestor(receipt['contract_sha'],c2)
            require(json.loads(git('show',d2+':'+s['review_receipt']))==receipt,'D2 receipt differs from current receipt'); d1receipt=json.loads(git('show',d1+':'+s['review_receipt'])); require(any(x['name']=='actual-payload-smoke' and x['kind']=='observation' for x in d1receipt['checks']) and any(x['name']=='actual-payload-smoke' and x['kind']=='command' for x in receipt['checks']), 'D1/D2 kind correction missing')
            smoke=obj(stages[4]['runner_receipts'][0]); raw=read(smoke['output']).decode(); require(smoke['raw_exit_code']==0 and c1 in raw and 'check-clean' in raw and 'check-drift' in raw,'F1 actual payload raw incomplete')
            inventory=obj(s['extra_sources'][3]); manifest=obj(s['extra_sources'][4]); require(inventory['source_commit']==manifest['source_commit']==c1 and inventory['manifest_file_count']==inventory['git_tree_file_count']==len(inventory['files'])==len(manifest['files'])==111, 'actual payload inventory mismatch'); require(inventory['manifest_sha256']==hashlib.sha256(read(s['extra_sources'][4])).hexdigest(), 'actual payload manifest hash mismatch'); im={x['path']:x['sha256'] for x in inventory['files']}; mm={x['path']:x['sha256'] for x in manifest['files']}; require(im==mm, 'inventory and manifest differ'); tree=git('ls-tree','-r','--name-only',c1,'--','SKILL.md','scripts','references','templates','tests','.agents/notes').decode().splitlines(); require(set(tree)==set(im), 'actual whitelist differs from C1 tree');
            for path,h in im.items(): require(hashlib.sha256(git('show',c1+':'+path)).hexdigest()==h and git('rev-parse',c1+':'+path)==git('rev-parse',c2+':'+path),f'payload Git blob mismatch {path}');
            for mp in s['extra_sources'][:3]:
                for path,h in obj(mp)['sha256'].items(): require(hashlib.sha256(git('show',c2+':'+path)).hexdigest()==h,f'source manifest mismatch {path}')
            old=obj(s['retained_rejections'][1]); strict=obj(s['local_strict']); require(old['raw_exit_code']==2 and 'Invalid check kind: actual-payload-smoke' in read(old['output']).decode(),'D1 invalid kind rejection missing'); require(strict['raw_exit_code']==0 and strict['status']=='COMPLETED' and strict['tree_terminal'] is True and COORD[:12] in strict['argv'][2] and '--strict' in strict['argv'] and obj(s['local_strict_call'])['exit_code']==0,'D2 frozen strict missing')
            return f'C1={c1} NEEDS_FIX; C2={c2} independent review; D1={d1} rejected invalid kind; D2={d2} corrected and frozen local strict exit 0'
        case('review-registration',native_layer,'C1/F1/C2 independent review and D1 rejection/D2 corrected frozen strict', [s['review_report'],s['review_receipt'],s['local_strict'],*s['retained_rejections']],reviews)
        for observation in source['related_observations']:
            try:
                data=obj(observation['path']); ident=observation['id']
                if ident=='codeg-worker-environment':
                    require('bwrap' in json.dumps(data).lower(),'missing raw bwrap record'); result='BLOCKED'; detail='Codeg worker bwrap failed to mount proc; worker execution not established; host owner must repair environment.'
                elif ident=='codeg-assessment':
                    require('BLOCKED' in data['native_worker'],'Codeg assessment missing BLOCKED'); result='BLOCKED'; detail=data['native_worker']
                elif ident=='root04-order-incident':
                    require(data['result']=='FAIL','root04 original failure missing'); result='FAIL'; detail=data['cause']+'; Controller owns correction; historical failure retained.'
                else: raise Finding('UNKNOWN','unrecognized observation; Controller must classify')
            except Finding as e: result=e.result; detail=e.detail; fatal=True
            except (KeyError, TypeError, ValueError, IndexError, AttributeError) as e: result='UNKNOWN'; detail=f'malformed observation: {e}; Controller must supply valid original'; fatal=True
            cases.append(dict(id=observation['id'],layer=native_layer,expected='retain actual historical observation and boundary',observed=detail,result=result,evidence=[observation['path']]))
    unverified=['Independent nonparticipant semantic review of this probe and original records is required.', 'Codeg worker execution, complete original environment identity, installation/deployment, current Windows and external FS lifecycle are UNKNOWN/BLOCKED.', 'Controller must complete all 13 cards including 12 before integration, full suite, independent total review and final branch strict.', 'Frozen coordinator FROZEN-KNOWN-01/02 cannot self-approve candidate.', 'Task 10 isolated static/synthetic results are linked at docs/todos/11-reliable-delivery/evidence/10/integration-report.json; no suite rerun here.']
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(dict(version=1,candidate=candidate,coordinator_commit=COORD,cases=cases,unverified=unverified),ensure_ascii=False,indent=2)+'\n')
    (out.parent/'native-chain-index.json').write_text(json.dumps(dict(version=1,sources=args.sources,selected_task='06',source_index_observed_head=source.get('observed_head') if source else None,case_evidence={c['id']:c['evidence'] for c in cases}),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'selected_chain_valid':not fatal,'case_counts':{r:sum(c['result']==r for c in cases) for r in ('PASS','FAIL','UNKNOWN','BLOCKED')},'output':str(out)}))
    return 2 if fatal else 0
if __name__=='__main__': raise SystemExit(main())
