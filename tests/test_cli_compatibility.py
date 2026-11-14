"""Callable CLI contract; legacy command routing remains unchanged."""
import sys
import subprocess
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import iter_cli as cli


def test_callable_help_returns_zero_and_covers_timing(capsys):
    args = ['--help']
    assert cli.main(args) == 0
    assert args == ['--help']
    help_text = capsys.readouterr().out
    for flag in ('--timing-init', '--timing-import', '--timing-import-receipt', '--timing-report', '--timing-trace'):
        assert flag in help_text


def test_unknown_option_has_no_writes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    marker = tmp_path / 'README.md'
    marker.write_text('unchanged', encoding='utf-8')
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    assert cli.main(['--local', '--not-a-command']) == 1
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


@pytest.mark.parametrize('command', ['--inventory', '--preflight', '--dispatch-check'])
def test_default_phase_and_readiness_exits(command, tmp_path, monkeypatch):
    import iter_inventory
    import iter_preflight
    seen = []
    outcome = ['READY']
    def check(*args):
        seen.append(args)
        return {'readiness': outcome[0]}
    monkeypatch.setattr(iter_inventory, 'inventory', check)
    monkeypatch.setattr(iter_preflight, 'preflight', check)
    monkeypatch.setattr(iter_preflight, 'dispatch_check', check)
    flags = ['--mode', 'continue'] if command == '--inventory' else []
    for status, expected in [('READY', 0), ('NEEDS_INPUT', 2), ('BLOCKED', 3)]:
        outcome[0] = status
        assert cli.main([command, str(tmp_path), *flags]) == expected
        assert seen[-1][4 if command == '--inventory' else 3] == 'implementation'


@pytest.mark.parametrize('flag,name,positionals,expected', [
    ('--render-envelope', 'render_task_envelope', ['card.md', 'repo'], (Path('card.md'), Path('repo'))),
    ('--review-pkg', 'generate_review_package', ['BASE', 'HEAD', '03', 'repo'], ('BASE', 'HEAD', '03', Path('repo'))),
    ('--verify-committed', 'verify_todos_committed', ['repo'], (Path('repo'),)),
    ('--check-scope', 'audit_scope_firewall', ['BASE', 'HEAD', 'card.md', 'repo'], (Path('repo'), 'BASE', 'HEAD', Path('card.md'), False, None)),
])
def test_legacy_positionals(flag, name, positionals, expected, monkeypatch):
    seen = []
    def operation(*args, **kwargs):
        seen.append(args)
        if name == 'generate_review_package':
            return Path('package.md')
        return {'committed': True, 'passed': True, 'changed_files': []}
    monkeypatch.setattr(cli, name, operation)
    args = [flag, *positionals]
    original = list(args)
    assert cli.main(args) == 0
    assert seen == [expected]
    assert args == original


def test_cli_errors_return_integer_without_exiting():
    assert cli.main(['--check-scope']) == 1
    assert cli.main(['--inventory']) == 2


def test_legacy_import_is_lazy_and_main_signature_preserved():
    scripts = Path(__file__).resolve().parents[1] / 'scripts'
    code = (f'import sys, inspect; sys.path.insert(0, {str(scripts)!r}); '
            'import iter_sync; assert "iter_cli" not in sys.modules; '
            'assert str(inspect.signature(iter_sync.main)) == "()"; '
            'sys.argv = ["iter_sync.py", "--help"]; '
            'assert iter_sync.main() is None; assert "iter_cli" in sys.modules; '
            'sys.argv = ["iter_sync.py", "--check-scope"]; '
            '\ntry: iter_sync.main()\nexcept SystemExit as error: assert error.code == 1\nelse: raise AssertionError("legacy exit lost")')
    result = subprocess.run([sys.executable, '-B', '-c', code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
