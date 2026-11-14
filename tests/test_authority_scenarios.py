"""Actual prompt-source regressions, not native agent-session acceptance."""

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(('scenario', 'path', 'required'), [
    ('prompt_only', 'references/worktree_git_contract.md', (
        '仅生成Prompt、评估或只读接管不授权写文件、实现、提交或创建Worktree',
        '只交付标明执行前门禁的预览',
        '仅生成Prompt不触发该提交流程',
    )),
    ('no_git_permission', 'references/worktree_git_contract.md', (
        '实际创建Worktree或执行任务前必须运行', '--verify-committed',
        '没有Git提交权限时交付未提交计划和执行依赖，不自动补Commit，不启动受阻执行',
    )),
    ('preexisting_dirty', 'references/worktree_git_contract.md', (
        '逐个精准暂存本次归属文件，检查cached diff后提交',
        '不夹带他人dirty', '不自动checkout/reset/clean',
        '目录边界不是整目录写权',
    )),
    ('no_merge_permission', 'references/worktree_git_contract.md', (
        '未授权合流时保留Worktree与分支，不合入main、不推送、不清理',
        '合流授权不包含推送或删除授权',
    )),
])
def test_scenario_expectation_is_in_actual_source(scenario, path, required):
    text = (ROOT/path).read_text(encoding='utf-8')
    for expected in required:
        assert expected in text, (scenario, path, expected)


def test_cross_entry_sources_preserve_readonly_and_independent_review():
    for name, marker in (
        ('iteration_planner', '仅Prompt/分析只在会话交付'),
        ('iteration_controller', '只生成Prompt时止于预览'),
        ('task_tech_lead', '只读模式不变更文件或Git'),
    ):
        text = (ROOT/f'templates/assistants/{name}.md').read_text(encoding='utf-8')
        assert marker in text, name
        assert 'agent_protocol.md' in text, name
    contract = (ROOT/'references/worktree_git_contract.md').read_text(encoding='utf-8')
    assert '不同type使用各自证据，不为非TDD任务补造RED' in contract
    assert '实现C → 非参与者独审 → 主管登记D → `--local --strict`' in contract
