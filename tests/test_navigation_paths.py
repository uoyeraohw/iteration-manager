from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_skill_routes_to_authoritative_sources_and_current_task():
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    for path in ('references/agent_protocol.md', 'references/task_card_schema.md',
                 'references/worktree_git_contract.md', 'scripts/iter_sync.py',
                 'templates/contracts/strict_tdd_contract.md',
                 'templates/contracts/ui_component_contract.md',
                 'templates/contracts/refactor_benchmark_contract.md',
                 'templates/contracts/spike_discovery_contract.md'):
        assert path in skill and (ROOT / path).is_file()
    for term in ('iter:goal', '--render-envelope', 'UNKNOWN', 'DONE', 'PASS', 'filesystem'):
        assert term in skill
    assert '历史全文' in skill
    assert not re.search(r'^\d+\. ', skill, re.M)


def test_template_handoff_is_a_navigation_slot_not_embedded_evidence():
    template = (ROOT / 'templates/iteration_readme.md').read_text(encoding='utf-8')
    for term in ('当前交接摘要', '任务卡及 envelope', '证据原件路径', '项目内', '缺失'):
        assert term in template
    assert '不嵌入原始日志' in template
    assert template.index('<!-- /iter:goal -->') < template.index('当前交接摘要')
