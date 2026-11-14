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


def test_worktree_text_and_diagram_do_not_restore_automatic_git_actions():
    text = (ROOT/'references/worktree_git_contract.md').read_text(encoding='utf-8')
    for obsolete in (
        'git add .gitignore docs/todos/',
        '/iter init` 收尾强制提交',
        '在生成新窗口 Prompt 及执行',
        '立即补充 Commit',
        '立即将该迭代分支',
        '并销毁该 Worktree',
    ):
        assert obsolete not in text, obsolete
    diagram = text.split('```mermaid\n', 1)[1].split('```', 1)[0]
    for boundary in ('仅Prompt或只读', '--verify-committed', '未授权', '保留分支与Worktree', '另有清理授权'):
        assert boundary in diagram, boundary


def test_adjacent_sources_keep_authority_above_goal_and_ruling():
    handbook = (ROOT/'references/superpowers_handbook.md').read_text(encoding='utf-8')
    assert '以迭代总目标为最高权威' not in handbook
    assert '目标和Ruling不创造写入、提交、合流或清理权限' in handbook
    assert '单轮5、累计10、自动会诊1、自动重规划2' in handbook
    root = (ROOT/'templates/root_readme.md').read_text(encoding='utf-8')
    assert 'Git提交、推送和清理分别按各自授权' in root
    assert '仅生成Prompt' in root and '--verify-committed' in root
