"""Check the matrix interface and repository links, not historical truth."""
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / 'references/support_matrix.md'
FIELDS = ('capability', 'platform', 'host', 'status', 'observed_at',
          'source_candidate', 'evidence', 'limitation')


def test_rows_have_complete_dated_evidence_and_responsibility():
    text = MATRIX.read_text(encoding='utf-8')
    assert '| ' + ' | '.join(FIELDS) + ' |' in text
    rows = [line for line in text.splitlines() if line.startswith('| ')][2:]
    assert len(rows) >= 11
    for row in rows:
        cells = [cell.strip() for cell in row.strip('|').split('|')]
        assert len(cells) == len(FIELDS) and all(cells)
        assert datetime.fromisoformat(cells[4]).date()
        assert re.search(r'\[[^]]+\]\([^)]+\)', cells[6])
        assert any(owner in cells[7] for owner in ('owner', '控制者', '消费者'))
    for term in ('513 passed', '2 Windows skip', '493 passed', 'BLOCKED worker',
                 'FS时间中断grant', 'Gemini CLI自动发现', '安装白名单'):
        assert term in text


def test_matrix_links_resolve_from_matrix_in_maintenance_root():
    text = MATRIX.read_text(encoding='utf-8')
    for link in re.findall(r'\[[^]]+\]\(([^)]+)\)', text):
        target = (MATRIX.parent / link.split('#')[0]).resolve()
        assert target.is_relative_to(ROOT), link
        assert target.is_file(), link
    assert '[支持矩阵](support_matrix.md)' in (ROOT / 'references/release_status.md').read_text(encoding='utf-8')
