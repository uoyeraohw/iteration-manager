"""Task inventory regression; synthetic fixtures are not product receipts."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import iter_sync


def test_board_excludes_supporting_documents_but_keeps_broken_cards(tmp_path):
    for name, text in {
        'README.md': '# Index',
        '验收大盘.md': '# Local delivery',
        'guide.md': '# Example\n---\ntask_id: example\n---\n',
        '01-done.md': '---\ntask_id: 01\nstatus: DONE\n---\n',
        '02-broken.md': 'broken card',
        'custom.md': '\ufeff---\ntask_id:\n---\n',
    }.items():
        (tmp_path / name).write_text(text, encoding='utf-8')
    data = iter_sync.generate_board_data(tmp_path)
    assert data['total'] == 3
    cards = {c['filename']: c for c in data['cards']}
    assert cards['02-broken.md']['status'] == 'UNKNOWN'
    assert cards['01-done.md']['acceptance_verdict'] != 'PASS'
    assert cards['custom.md']['status'] == 'UNKNOWN'


def test_no_cards_in_support_only_directory(tmp_path):
    (tmp_path / 'README.md').write_text('# index', encoding='utf-8')
    (tmp_path / 'notes.md').write_text('# notes', encoding='utf-8')
    assert iter_sync.generate_board_data(tmp_path)['total'] == 0


def test_unnumbered_status_only_legacy_card_is_not_hidden(tmp_path):
    (tmp_path / 'legacy.md').write_text('---\nstatus: DONE\n---\n', encoding='utf-8')
    data = iter_sync.generate_board_data(tmp_path)
    assert data['total'] == 1
    assert data['cards'][0]['acceptance_verdict'] == 'UNKNOWN'


def test_unreadable_document_is_not_silently_ignored(tmp_path, monkeypatch):
    path = tmp_path / 'unreadable.md'
    path.write_text('bytes', encoding='utf-8')
    original = Path.read_text

    def read(self, *args, **kwargs):
        if self == path:
            raise UnicodeError('synthetic unreadable file')
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, 'read_text', read)
    cards = iter_sync.generate_board_data(tmp_path)['cards']
    assert len(cards) == 1
    assert cards[0]['acceptance_verdict'] == 'FAIL'


def test_takeover_uses_same_inventory(tmp_path):
    (tmp_path / '01-broken.md').write_text('broken', encoding='utf-8')
    (tmp_path / 'custom.md').write_text('---\ntask_id: custom\nstatus: TODO\n---\n', encoding='utf-8')
    (tmp_path / '验收大盘.md').write_text('# supporting report', encoding='utf-8')
    command = [sys.executable, '-B', str(Path(iter_sync.__file__)), '--takeover-report', str(tmp_path)]
    result = subprocess.run(command, capture_output=True, encoding='utf-8', check=False)
    assert result.returncode == 0, result.stderr
    actual = {Path(c['path']).name for c in json.loads(result.stdout)['tasks']}
    expected = {c['filename'] for c in iter_sync.generate_board_data(tmp_path)['cards']}
    assert actual == expected == {'01-broken.md', 'custom.md'}
