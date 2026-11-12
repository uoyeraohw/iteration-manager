from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def test_authoritative_assistant_sources_and_consistent_protocol():
    names = ('iteration_controller','task_tech_lead','iteration_planner')
    for name in names:
        p = ROOT/'templates/assistants'/f'{name}.md'
        assert p.is_file(), name
        text = p.read_text(encoding='utf-8')
        assert 'agent_protocol.md' in text
    skill = (ROOT/'SKILL.md').read_text(encoding='utf-8')
    assert 'invoke_subagent' not in skill
    assert '禁止在主窗口直接编写业务实现代码或直接在大段上下文中肉眼审查' not in skill


def test_no_default_score_or_unbounded_reset():
    task = (ROOT/'templates/task_detail.md').read_text(encoding='utf-8')
    assert 'typesafe_score: 85' not in task
    assert '`85/100`' not in task
    rca = (ROOT/'templates/consilium_rca_prompt.md').read_text(encoding='utf-8')
    assert '重置 `fix_rounds: 0`' not in rca
    assert 'agent_protocol.md' in rca
    guide = (ROOT/'references/typesafe_eval_guide.md').read_text(encoding='utf-8')
    assert '"state"' in guide and '"questions"' in guide
    assert '或运行内置评估逻辑' not in guide
    assert '30/30/20/20' in guide
