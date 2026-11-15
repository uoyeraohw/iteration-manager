"""Installation provenance is derived from committed bytes and checked read-only."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'iter_install.py'
if SCRIPT.exists():
    spec = importlib.util.spec_from_file_location('iter_install', SCRIPT)
    install = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(install)
else:
    # Inert RED adapter: missing behavior returns no result, never claims success.
    class MissingInstallationBehavior:
        def build_install_manifest(self, source_root, source_commit):
            return None

        def check_installation(self, installation_root, manifest):
            return None

        def main(self, argv=None):
            return 1

    install = MissingInstallationBehavior()


FILES = {
    'SKILL.md': b'skill\n',
    'scripts/query.py': b'query\n',
    'references/guide.md': b'guide\n',
    'templates/card.md': b'card\n',
    'tests/test_example.py': b'test\n',
    '.agents/notes/decision.md': b'decision\n',
}


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()


@pytest.fixture
def source(tmp_path):
    root = tmp_path / 'source'
    root.mkdir()
    git(root, 'init', '-q')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    git(root, 'config', 'user.name', 'Fixture')
    for name, content in FILES.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (root / 'private.txt').write_bytes(b'outside whitelist')
    git(root, 'add', '.')
    git(root, 'commit', '-qm', 'fixture')
    return root, git(root, 'rev-parse', 'HEAD')


@pytest.fixture
def installation(tmp_path, source):
    root = tmp_path / 'installed'
    root.mkdir()
    for name, content in FILES.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    manifest = {'version': 1, 'source_commit': source[1], 'files': [
        {'path': name, 'sha256': hashlib.sha256(content).hexdigest()}
        for name, content in FILES.items()
    ]}
    return root, manifest


def check_cli(tmp_path, root, manifest):
    path = tmp_path / 'manifest.json'
    path.write_text(json.dumps(manifest), encoding='utf-8')
    return install.main(['--check', '--root', str(root), '--manifest', str(path)])


def test_build_manifest_is_exact_committed_whitelist_and_byte_hashes(source):
    root, commit = source
    manifest = install.build_install_manifest(root, commit)
    assert isinstance(manifest, dict), 'build_install_manifest must return a provenance manifest'
    assert manifest['version'] == 1
    assert manifest['source_commit'] == commit
    assert {entry['path']: entry['sha256'] for entry in manifest['files']} == {
        name: hashlib.sha256(content).hexdigest() for name, content in FILES.items()
    }


def test_make_manifest_cli_prints_json_without_writing_source(source, capsys):
    root, commit = source
    before = git(root, 'status', '--porcelain', '--untracked-files=all')
    assert install.main(['--make-manifest', '--root', str(root), '--source-commit', commit]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output['source_commit'] == commit
    assert git(root, 'status', '--porcelain', '--untracked-files=all') == before


@pytest.mark.parametrize('change', ['tracked_bytes', 'untracked_whitelist', 'old_commit', 'unknown_commit', 'abbreviated_commit'])
def test_make_manifest_rejects_unverified_source(source, change):
    root, commit = source
    if change == 'tracked_bytes':
        (root / 'SKILL.md').write_bytes(b'changed')
    elif change == 'untracked_whitelist':
        (root / 'scripts/new.py').write_bytes(b'uncommitted')
    elif change == 'old_commit':
        (root / 'SKILL.md').write_bytes(b'new committed bytes')
        git(root, 'add', 'SKILL.md')
        git(root, 'commit', '-qm', 'different source')
    elif change == 'unknown_commit':
        commit = 'f' * 40
    else:
        commit = commit[:7]
    assert install.main(['--make-manifest', '--root', str(root), '--source-commit', commit]) == 2


def test_clean_install_checks_without_modification(tmp_path, installation):
    root, manifest = installation
    before = {name: (root / name).read_bytes() for name in FILES}
    assert check_cli(tmp_path, root, manifest) == 0
    assert {name: (root / name).read_bytes() for name in FILES} == before
    report = install.check_installation(root, manifest)
    assert isinstance(report, dict), 'check_installation must return a report'
    # File provenance and runtime capability are distinct, independently reported facts.
    keys = {str(k).lower() for k in report}
    assert any('capabilit' in k or 'runtime' in k for k in keys)
    assert any('source' in k or 'provenance' in k or 'file' in k for k in keys)


@pytest.mark.parametrize('damage', ['drift', 'missing', 'outside_link'])
def test_install_check_rejects_damage_without_repair(tmp_path, installation, damage):
    root, manifest = installation
    target = root / 'scripts/query.py'
    if damage == 'drift':
        target.write_bytes(b'drift')
    else:
        target.unlink()
        if damage == 'outside_link':
            secret = tmp_path / 'secret'
            secret.write_bytes(FILES['scripts/query.py'])
            target.symlink_to(secret)
    assert check_cli(tmp_path, root, manifest) == 2
    if damage == 'drift':
        assert target.read_bytes() == b'drift'
    elif damage == 'missing':
        assert not target.exists()
    else:
        assert target.is_symlink()


@pytest.mark.parametrize('mutation', ['unknown_key', 'file_unknown_key', 'duplicate', 'traversal', 'absolute', 'outside_whitelist', 'bad_digest', 'bad_commit', 'bad_version', 'empty_files'])
def test_check_rejects_bad_manifest_before_reading_external_data(tmp_path, installation, monkeypatch, mutation):
    root, original = installation
    manifest = copy.deepcopy(original)
    secret = tmp_path / 'secret'
    secret.write_bytes(b'do not read')
    if mutation == 'unknown_key': manifest['surprise'] = True
    elif mutation == 'file_unknown_key': manifest['files'][0]['surprise'] = True
    elif mutation == 'duplicate': manifest['files'].append(copy.deepcopy(manifest['files'][0]))
    elif mutation == 'traversal': manifest['files'][0]['path'] = '../secret'
    elif mutation == 'absolute': manifest['files'][0]['path'] = str(secret)
    elif mutation == 'outside_whitelist':
        (root / 'private.txt').write_bytes(b'outside')
        manifest['files'][0]['path'] = 'private.txt'
    elif mutation == 'bad_digest': manifest['files'][0]['sha256'] = 'not-a-sha256'
    elif mutation == 'bad_commit': manifest['source_commit'] = 'unknown'
    elif mutation == 'bad_version': manifest['version'] = 2
    else: manifest['files'] = []
    original_open = Path.open
    def guarded_open(path, *args, **kwargs):
        assert path.resolve() != secret.resolve(), 'attempted to read outside installation'
        assert path != root / 'private.txt', 'attempted to read outside delivery whitelist'
        return original_open(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'open', guarded_open)
    assert check_cli(tmp_path, root, manifest) == 2


def test_check_cli_rejects_malformed_json(tmp_path, installation):
    root, _ = installation
    path = tmp_path / 'broken.json'
    path.write_text('{', encoding='utf-8')
    assert install.main(['--check', '--root', str(root), '--manifest', str(path)]) == 2
