"""Execute the actual tool-executor function with controlled clocks and callbacks."""
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_js(body):
    source = (ROOT / 'scripts/deadline_watch.js').read_text(encoding='utf-8')
    result = subprocess.run(
        ['node', '-e', source + '\n(async () => {\n' + body +
         '\n})().catch(e => { console.error(e); process.exitCode = 1; });'],
        cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=10)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_watch_keeps_cancel_inside_executor_without_model_gap():
    result = run_js('''
let clock=0, stopped=false; const waits=[];
const result=await watchDeadline({deadlineMs:125000, checkpoints:[60000],
 now:()=>clock, pause:async ms=>{clock+=ms;},
 query:async ms=>{if(ms===undefined)return {status:'canceled'};
   waits.push(ms);clock+=ms;return {status:'running'};},
 cancel:async()=>{stopped=true;clock+=13;return {status:'canceled'};}});
console.log(JSON.stringify({result,waits,stopped}));
''')
    assert result['stopped'] is True
    assert result['waits'] == [60000, 55000]
    assert result['result']['requestedAt'] == 115000
    assert result['result']['confirmedAt'] == 115013
    assert result['result']['lateByMs'] == 0
    assert result['result']['terminalConfirmed'] is True
    assert any(x['kind'] == 'checkpoint' for x in result['result']['events'])


def test_early_terminal_is_returned_without_cancellation():
    result = run_js('''
let calls=0;
const result=await watchDeadline({deadlineMs:20000,now:()=>0,
 query:async()=>({status:'completed',text:'raw result'}),
 cancel:async()=>{calls++;}});
console.log(JSON.stringify({result,calls}));
''')
    assert result['calls'] == 0
    assert result['result']['final']['text'] == 'raw result'


def test_already_expired_cancels_without_another_wait_or_deadline_shift():
    result = run_js('''
let clock=30000;const waits=[];
const result=await watchDeadline({deadlineMs:25000,now:()=>clock,
 query:async ms=>{waits.push(ms??null);return {status:'unknown'};},
 cancel:async()=>{clock+=100;return {status:'canceled'};}});
console.log(JSON.stringify({result,waits}));
''')
    assert result['waits'] == [None]
    assert result['result']['deadlineMs'] == 25000
    assert result['result']['lateByMs'] == 5100
    assert result['result']['terminalConfirmed'] is False


def test_monitor_error_and_cancel_failure_preserve_unknown():
    result = run_js('''
let calls=0;
const result=await watchDeadline({deadlineMs:50000,now:()=>0,
 query:async ms=>{calls++;throw new Error('transport lost');},
 cancel:async()=>{throw new Error('cancel lost');}});
console.log(JSON.stringify({result,calls}));
''')
    assert result['calls'] == 2
    assert result['result']['reason'] == 'monitor-error'
    assert result['result']['final']['status'] == 'unknown'
    assert result['result']['terminalConfirmed'] is False


def test_fast_blocked_notifications_do_not_disable_guard_or_spin():
    result = run_js('''
let clock=0, pauses=0, canceled=false;
const result=await watchDeadline({deadlineMs:12000,now:()=>clock,
 pause:async ms=>{pauses++;clock+=ms;},
 query:async ms=>ms===undefined ? {status:'canceled'} :
   {status:'running',blocked_on:'approval'},
 cancel:async()=>{canceled=true;return {status:'canceled'};}});
console.log(JSON.stringify({result,pauses,canceled}));
''')
    assert result['pauses'] == 2
    assert result['canceled'] is True
    assert result['result']['requestedAt'] == 2000


def test_tool_latency_overrun_is_reported_not_hidden():
    result = run_js('''
let clock=0;
const result=await watchDeadline({deadlineMs:20000,now:()=>clock,
 query:async ms=>{if(ms!==undefined)clock+=ms+3000;
   return {status:ms===undefined?'canceled':'running'};},
 cancel:async()=>{clock+=12000;return {status:'canceled'};}});
console.log(JSON.stringify(result));
''')
    assert result['requestedAt'] == 13000
    assert result['confirmedAt'] == 25000
    assert result['lateByMs'] == 5000
