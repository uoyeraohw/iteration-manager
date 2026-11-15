"""Exercise the actual executor source with controlled asynchronous callbacks."""
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / 'scripts/dispatch_guard.js'


def run_js(body):
    # RED fallback deliberately does nothing; missing module is not an import error.
    source = GUARD.read_text(encoding='utf-8') if GUARD.exists() else (
        'async function dispatchAfterReady() { return {dispatched:false, reason:"missing"}; }')
    setup = r'''
const request={request_id:'r1',project_root:'/project',tool_entry:'/tools/iter_sync.py',
 task_path:'/project/card.md',task_id:'03',owner:'owner',phase:'implementation',
 candidate:'abc',context:'/project/context.json'};
const ready={task_path:request.task_path,task_id:request.task_id,phase:request.phase,
 candidate:request.candidate,readiness:'READY'};
const result={state:'completed',exit_code:0,cwd:request.project_root,request_id:request.request_id,
 argv:['python3','-B',request.tool_entry,'--dispatch-check',request.task_path,'--context',request.context,
 '--phase',request.phase,'--owner',request.owner],terminal_evidence:{source:'native-command',id:'cmd-1'},
 stdout:JSON.stringify(ready),stderr:''};
let calls=0; const dispatch=async()=>{calls++;return {status:'unknown',id:'d1'};};
'''
    proc = subprocess.run(['node', '-e', source + '\n(async()=>{\n' + setup + body +
                           '\n})().catch(e=>{console.error(e);process.exitCode=1;});'],
                          cwd=ROOT, capture_output=True, text=True, timeout=10)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_pending_check_then_ready_calls_once_and_preserves_native_result():
    actual = run_js('''
let resolve; const pending=new Promise(r=>resolve=r);
const work=dispatchAfterReady({request,check:()=>pending,dispatch});
await Promise.resolve(); const before=calls; resolve(result); const answer=await work;
console.log(JSON.stringify({before,calls,answer}));''')
    assert actual['before'] == 0
    assert actual['calls'] == 1
    assert actual['answer']['dispatched'] is True
    assert actual['answer']['delegation'] == {'status': 'unknown', 'id': 'd1'}


def test_overlapping_requests_dispatch_in_reverse_completion_order_with_own_identity():
    actual = run_js('''
const second={...request,request_id:'r2',task_path:'/project/second.md',task_id:'04',
 owner:'other-owner',phase:'review',candidate:'def',context:'/project/second.json'};
function observation(req, id) {
 return {...result,request_id:req.request_id,terminal_evidence:{source:'native-command',id},
  argv:['python3','-B',req.tool_entry,'--dispatch-check',req.task_path,'--context',req.context,
   '--phase',req.phase,'--owner',req.owner],
  stdout:JSON.stringify({readiness:'READY',task_path:req.task_path,task_id:req.task_id,
   phase:req.phase,candidate:req.candidate})};
}
let resolveFirst, resolveSecond;
const firstCheck=new Promise(resolve=>{resolveFirst=resolve});
const secondCheck=new Promise(resolve=>{resolveSecond=resolve});
const events=[];
const delegate=async(req, observed)=>{events.push({request:req,ready:observed});
 return {id:req.request_id};};
const firstWork=dispatchAfterReady({request,check:()=>firstCheck,dispatch:delegate});
const secondWork=dispatchAfterReady({request:second,check:()=>secondCheck,dispatch:delegate});
await Promise.resolve(); const before=events.length;
resolveSecond(observation(second,'cmd-2'));
const secondResult=await secondWork; const afterSecond=events.length;
resolveFirst(observation(request,'cmd-1'));
const firstResult=await firstWork;
console.log(JSON.stringify({before,afterSecond,events,firstResult,secondResult}));''')
    assert actual['before'] == 0
    assert actual['afterSecond'] == 1
    assert [event['request']['request_id'] for event in actual['events']] == ['r2', 'r1']
    for event, identity in zip(actual['events'], [
        ('r2', '/project/second.md', '04', 'other-owner', 'review', 'def', '/project/second.json'),
        ('r1', '/project/card.md', '03', 'owner', 'implementation', 'abc', '/project/context.json'),
    ]):
        req, ready = event['request'], event['ready']
        assert tuple(req[key] for key in ('request_id', 'task_path', 'task_id', 'owner',
                                          'phase', 'candidate', 'context')) == identity
        assert tuple(ready[key] for key in ('task_path', 'task_id', 'phase', 'candidate')) == (
            identity[1], identity[2], identity[4], identity[5])
    assert actual['firstResult']['delegation'] == {'id': 'r1'}
    assert actual['secondResult']['delegation'] == {'id': 'r2'}
    assert actual['firstResult']['check']['terminal_evidence']['id'] == 'cmd-1'
    assert actual['secondResult']['check']['terminal_evidence']['id'] == 'cmd-2'


@pytest.mark.parametrize('mutation', [
    "result.state='running'", "result.state='failed'", "result.state='unknown'",
    "result.exit_code=1", "result.exit_code='0'", "result.stdout='{'",
    "result.stdout=JSON.stringify(ready)+'\\n'+JSON.stringify(ready)",
    "result.stdout=JSON.stringify({...ready,readiness:'BLOCKED'})",
    "result.stdout=JSON.stringify({...ready,task_path:'/other'})",
    "result.stdout=JSON.stringify({...ready,task_id:'04'})",
    "result.stdout=JSON.stringify({...ready,phase:'review'})",
    "result.stdout=JSON.stringify({...ready,candidate:'old'})",
    "result.request_id='old'", "result.cwd='/other'",
    "result.argv[2]='/old/iter_sync.py'", "result.argv[4]='/old/card.md'",
    "result.argv[6]='/old/context.json'", "result.argv[8]='review'",
    "result.argv[10]='other'", "result.argv.push('--owner','other')",
    "result.terminal_evidence=null", "result.terminal_evidence={source:'',id:'x'}",
    "result.stderr=null", "result.argv=null",
])
def test_untrusted_check_never_dispatches(mutation):
    actual = run_js(mutation + ''';
const answer=await dispatchAfterReady({request,check:async()=>result,dispatch});
console.log(JSON.stringify({calls,answer}));''')
    assert actual['calls'] == 0
    assert actual['answer']['dispatched'] is False


def test_check_rejection_and_bad_request_do_not_dispatch():
    actual = run_js('''
const a=await dispatchAfterReady({request,check:async()=>{throw Error('lost')},dispatch});
const b=await dispatchAfterReady({request:{...request,owner:''},check:async()=>result,dispatch});
console.log(JSON.stringify({calls,a,b}));''')
    assert actual['calls'] == 0
    assert actual['a']['dispatched'] is False
    assert actual['b']['dispatched'] is False


def test_dispatch_throw_is_attempted_once_and_not_retried():
    actual = run_js('''
const answer=await dispatchAfterReady({request,check:async()=>result,
 dispatch:async()=>{calls++;throw Error('transport lost')}});
console.log(JSON.stringify({calls,answer}));''')
    assert actual['calls'] == 1
    assert actual['answer']['dispatched'] is True
    assert actual['answer']['reason'] == 'dispatch-error'
