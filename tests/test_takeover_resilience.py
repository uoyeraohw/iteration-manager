"""Legacy takeover reports isolate per-card read failures; fixtures are synthetic."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import iter_cli
import iter_sync

HEALTHY = '---\ntask_id: 01\nstatus: TODO\ntype: Strict-TDD\nschema_version: 1\n---\n'


def snapshot(directory):
    return {p.name: p.read_bytes() for p in directory.iterdir() if p.is_file()}


def assert_report(output, directory, damaged):
    report = json.loads(output)
    assert set(report) == {'read_only', 'tasks', 'next'}
    assert report['read_only'] is True
    assert report['next'] == 'Request migration/reverification authorization; preserve history'
    rows = {Path(row['path']).name: row for row in report['tasks']}
    assert set(rows) == {'01-healthy.md', *damaged}
    assert rows['01-healthy.md'] == {
        'path': str(directory / '01-healthy.md'), 'declared_status': 'TODO',
        'acceptance_verdict': 'UNKNOWN', 'missing': ['review_receipt'], 'findings': []}
    for name, reason in damaged.items():
        row = rows[name]
        assert set(row) == {'path', 'declared_status', 'acceptance_verdict', 'missing', 'findings'}
        assert row['declared_status'] == 'UNKNOWN'
        assert row['acceptance_verdict'] in ('UNKNOWN', 'FAIL')
        assert row['missing'] is None
        assert any(reason in finding for finding in row['findings'])


def test_legacy_subprocess_real_bad_utf8(tmp_path):
    (tmp_path / '01-healthy.md').write_text(HEALTHY, encoding='utf-8')
    (tmp_path / '02-bad.md').write_bytes(b'\xffinvalid')
    before = snapshot(tmp_path)
    result = subprocess.run([sys.executable, '-B', iter_sync.__file__, '--takeover-report', str(tmp_path)],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert_report(result.stdout, tmp_path, {'02-bad.md': 'utf-8'})
    assert snapshot(tmp_path) == before


def test_callable_mixed_encoding_and_oserror(tmp_path, monkeypatch, capsys):
    (tmp_path / '01-healthy.md').write_text(HEALTHY, encoding='utf-8')
    (tmp_path / '02-bad.md').write_bytes(b'\xffinvalid')
    bad = tmp_path / '03-oserror.md'
    bad.write_text(HEALTHY, encoding='utf-8')
    before = snapshot(tmp_path)
    original = Path.read_text
    def read(path, *args, **kwargs):
        if path == bad:
            raise OSError('synthetic read failure')
        return original(path, *args, **kwargs)
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'read_text', read)
        assert iter_cli.main(['--takeover-report', str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert_report(captured.out, tmp_path, {'02-bad.md': 'utf-8', '03-oserror.md': 'synthetic read failure'})
    assert captured.err == ''
    assert snapshot(tmp_path) == before


def test_discovered_card_deleted_before_read(tmp_path, monkeypatch, capsys):
    (tmp_path / '01-healthy.md').write_text(HEALTHY, encoding='utf-8')
    deleted = tmp_path / '02-deleted.md'
    deleted.write_text(HEALTHY, encoding='utf-8')
    before = snapshot(tmp_path)
    discover = iter_cli.discover_task_files
    def remove_after_discovery(directory):
        paths = discover(directory)
        deleted.unlink()  # Explicit fixture action, not a write by the report.
        return paths
    monkeypatch.setattr(iter_cli, 'discover_task_files', remove_after_discovery)
    assert iter_cli.main(['--takeover-report', str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert_report(captured.out, tmp_path, {'02-deleted.md': 'No such file'})
    assert captured.err == ''
    assert snapshot(tmp_path) == {k: v for k, v in before.items() if k != deleted.name}


@pytest.mark.parametrize('args', [['--takeover-report'], ['--takeover-report', 'missing'],
                                  ['--takeover-report', 'a', 'b']])
def test_invalid_arguments_remain_global_errors(args, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert iter_cli.main(args) == 1
    captured = capsys.readouterr()
    assert captured.out == ''
    assert '[IterSync:Error]' in captured.err
    monkeypatch.setattr(sys, 'argv', ['iter_sync.py', *args])
    with pytest.raises(ValueError):
        iter_sync.main()
    result = subprocess.run([sys.executable, '-B', iter_sync.__file__, *args], cwd=tmp_path,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert result.stdout == ''
    assert '[IterSync:Error]' in result.stderr


def test_callable_oserror_isolated(tmp_path, monkeypatch, capsys):
    (tmp_path / '01-healthy.md').write_text(HEALTHY, encoding='utf-8')
    bad = tmp_path / '03-oserror.md'
    bad.write_text(HEALTHY, encoding='utf-8')
    before = snapshot(tmp_path)
    original = Path.read_text
    def read(path, *args, **kwargs):
        if path == bad:
            raise OSError('synthetic read failure')
        return original(path, *args, **kwargs)
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'read_text', read)
        assert iter_cli.main(['--takeover-report', str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert_report(captured.out, tmp_path, {'03-oserror.md': 'synthetic read failure'})
    assert captured.err == ''
    assert snapshot(tmp_path) == before


def test_deleted_between_parse_and_audit_and_malformed_card(tmp_path, monkeypatch, capsys):
    (tmp_path / '01-healthy.md').write_text(HEALTHY, encoding='utf-8')
    vanished = tmp_path / '02-vanished.md'
    vanished.write_text(HEALTHY, encoding='utf-8')
    (tmp_path / '03-malformed.md').write_bytes(b'not a task card')
    before = snapshot(tmp_path)
    original = Path.read_text
    def read(path, *args, **kwargs):
        content = original(path, *args, **kwargs)
        if path == vanished:
            vanished.unlink()  # Explicit fixture deletion after parsing, before audit.
        return content
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'read_text', read)
        assert iter_cli.main(['--takeover-report', str(tmp_path)]) == 0
    captured = capsys.readouterr()
    report = json.loads(captured.out)
    rows = {Path(row['path']).name: row for row in report['tasks']}
    assert set(rows) == {'01-healthy.md', '02-vanished.md', '03-malformed.md'}
    assert rows['01-healthy.md']['declared_status'] == 'TODO'
    assert rows['02-vanished.md']['declared_status'] == 'UNKNOWN'
    assert rows['02-vanished.md']['acceptance_verdict'] == 'FAIL'
    assert rows['02-vanished.md']['missing'] == ['review_receipt']
    assert any('No such file' in finding for finding in rows['02-vanished.md']['findings'])
    assert rows['03-malformed.md']['declared_status'] == 'UNKNOWN'
    assert rows['03-malformed.md']['acceptance_verdict'] != 'PASS'
    assert rows['03-malformed.md']['findings']
    assert captured.err == ''
    assert snapshot(tmp_path) == {k: v for k, v in before.items() if k != vanished.name}
