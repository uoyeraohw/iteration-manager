"""Structural routing checks; real host consumption requires native evidence."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_a_default_codeg_guard_routes_real_check_and_dispatch():
    protocol = read('references/agent_protocol.md')
    section = protocol.split('### 新流程的默认派发', 1)[1].split('### 正常检查点', 1)[0]
    for required in ('dispatchAfterReady({request, check, dispatch})', '--dispatch-check',
                     'tools.exec_command', 'tools.mcp__codeg_mcp__delegate_to_agent',
                     "state:'unknown'", 'owner', 'candidate', 'phase', 'context',
                     'request_id', 'running', '非 READY', 'BLOCKED', 'bwrap'):
        assert required in section
    assert section.index('const check =') < section.index('const dispatch =') < section.index('await dispatchAfterReady(')
    for path in ('references/execution_readiness.md', 'templates/assistants/iteration_controller.md',
                 'templates/assistants/task_tech_lead.md'):
        assert '共同协议' in read(path)


def test_b_early_precheck_is_not_per_card_or_final_acceptance():
    diagram = read('references/worktree_git_contract.md').split('```mermaid\n', 1)[1].split('```', 1)[0]
    for edge in ('T1[', ' --> T2[', 'T2 --> T3[', 'T3 --> T4[',
                 'T4 -.-> E', 'T4 --> F0', '不是最终验收'):
        assert edge in diagram
    assert 'E -.-> F0' not in diagram
    assert '--local --strict' in diagram


def test_c_all_cards_precede_integration_review_and_final_strict():
    protocol = read('references/agent_protocol.md').split('### Git 整轮收口的权威顺序', 1)[1].split('## 分层验证', 1)[0]
    for text in ('全部卡（包括最后一张）', '集成路径与全量回归 → 独立整轮总审 →',
                 '最终登记候选', '最后一张卡不依赖', '重新独审',
                 'build/iter11-closeout/', '不写回已批准任务 scope'):
        assert text in protocol
    diagram = read('references/worktree_git_contract.md').split('```mermaid\n', 1)[1].split('```', 1)[0]
    for edge in ('F0[', ' --> F1[', 'F1 --> F2[', 'F2 --> F3[', 'F3 --> F4['):
        assert edge in diagram
    controller = read('templates/assistants/iteration_controller.md')
    assert '共同协议' in controller and '最终登记候选' in controller


def test_a_adapter_executes_guard_with_pending_and_ready(tmp_path):
    """Synthetic host callbacks exercise the documented code, including shell quoting."""
    import json
    import subprocess
    import sys

    root = tmp_path / "project's root"
    root.mkdir()
    check = root / "check's cli.py"
    check.write_text("import json,sys\nprint(json.dumps(dict(readiness='READY',task_path=sys.argv[2],task_id='12',phase='implementation',candidate='candidate')))\n", encoding='utf-8')
    request = dict(request_id='request-1', project_root=str(root), tool_entry=str(check),
                   task_path=str(root / "task's card.md"), task_id='12', owner='owner',
                   phase='implementation', candidate='candidate', context="context's path")
    section = read('references/agent_protocol.md').split('### 新流程的默认派发', 1)[1]
    snippet = section.split('```javascript\n', 1)[1].split('\n```', 1)[0]
    guard = read('scripts/dispatch_guard.js')
    js = f'''
const {{spawnSync}} = require('child_process');
const python = {json.dumps(sys.executable)};
const request = {json.dumps(request)};
const delegateArgs = {{task:'brief'}};
let calls = 0, pending = false, nonready = false;
const tools = {{
  exec_command: async (args) => {{
    if (pending) return {{session_id:123}};
    const p = spawnSync('bash', ['-lc', args.cmd], {{cwd:args.workdir, encoding:'utf8'}});
    let output = p.stdout;
    if (nonready) {{ const o = JSON.parse(output); const body = JSON.parse(o.stdout); body.readiness = 'BLOCKED'; o.stdout = JSON.stringify(body); output = JSON.stringify(o); }}
    return {{exit_code:p.status, output, chunk_id:'original-terminal'}};
  }},
  mcp__codeg_mcp__delegate_to_agent: async () => {{calls++; return {{status:'running'}};}}
}};
{guard}
(async () => {{
{snippet}
const first = result;
pending = true;
const second = await dispatchAfterReady({{request, check, dispatch}});
pending = false; nonready = true;
const third = await dispatchAfterReady({{request, check, dispatch}});
console.log(JSON.stringify({{first, second, third, calls}}));
}})().catch(e => {{console.error(e); process.exit(1);}});
'''
    result = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True)
    observed = json.loads(result.stdout)
    assert observed['first']['dispatched'] is True
    assert observed['first']['check']['raw']['chunk_id'] == 'original-terminal'
    assert observed['second']['dispatched'] is False
    assert observed['third']['dispatched'] is False
    assert observed['third']['reason'] == 'not-ready'
    assert observed['calls'] == 1
