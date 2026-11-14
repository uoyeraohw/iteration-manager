"""Structural checks only: primary observations and independent review own truth."""
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'references/release_status.md'
FIELDS = ('source_commit', 'reviewed_candidate', 'install_target', 'observed_version',
          'consumer_evidence', 'checked_at', 'evidence_scope', 'result', 'source_pointer')


def test_four_layers_have_complete_rows_and_dated_pointers():
    text = INDEX.read_text(encoding='utf-8')
    for heading in ('一、源码', '二、已审候选', '三、安装', '四、实际消费'):
        assert heading in text
    tables = text.count('| ' + ' | '.join(FIELDS) + ' |')
    assert tables == 4
    rows = [line for line in text.splitlines() if line.startswith('| ')][2:]
    facts = 0
    for line in rows:
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if cells[0] in ('source_commit', '---'):
            continue
        assert len(cells) == len(FIELDS)
        assert all(cells)
        assert datetime.fromisoformat(cells[5].replace('Z', '+00:00')).tzinfo
        assert re.search(r'\[[^]]+\]\([^)]+\)', cells[-1])
        facts += 1
    assert facts >= 12


def test_index_and_entry_links_resolve_without_external_history_dependency():
    for source in (INDEX, ROOT / 'SKILL.md'):
        text = source.read_text(encoding='utf-8')
        for link in re.findall(r'\[[^]]+\]\(([^)]+)\)', text):
            if '://' in link or link.startswith('#'):
                continue
            target = (source.parent / link.split('#')[0]).resolve()
            assert target.is_relative_to(ROOT), link
            assert target.is_file(), link
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    assert 'references/release_status.md' in skill
    assert 'references/template_generation.md' in skill


def test_unknown_ownership_and_evidence_boundaries_are_explicit():
    text = INDEX.read_text(encoding='utf-8')
    for required in ('UNKNOWN由谁补齐', '部署owner', '历史证据owner', '主控',
                     '合成', '非安装消费', '不预写本轮PASS', '不维护任务状态'):
        assert required in text
