"""Build committed installation manifests and check copies without modifying them."""
import argparse
import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath

_ROOTS = ('scripts', 'references', 'templates', 'tests', '.agents/notes')
_SHA = re.compile(r'^[0-9a-f]{64}$')
_COMMIT = re.compile(r'^(?:[0-9a-f]{40}|[0-9a-f]{64})$')


def _path(value):
    if not isinstance(value, str) or not value or '\\' in value or '\0' in value:
        raise ValueError('invalid manifest path')
    parts = value.split('/')
    if any(part in ('', '.', '..') for part in parts) or PurePosixPath(value).is_absolute():
        raise ValueError('path must be canonical and relative')
    if value != 'SKILL.md' and not any(value.startswith(root + '/') for root in _ROOTS):
        raise ValueError('path outside delivery whitelist')
    return value


def _read(root, name):
    """Reject links in every component before reading; never follow a link outside root."""
    current = root
    parts = _path(name).split('/')
    for part in parts:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('symbolic links are not supported')
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('expected regular file')
    return current.read_bytes()


def _git(root, *args):
    result = subprocess.run(['git', '--no-optional-locks', '-C', str(root), *args],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise ValueError('git source verification failed')
    return result.stdout


def _inventory(root):
    result = set()
    for entry in ('SKILL.md', *_ROOTS):
        path = root / entry
        # Check ancestor components too, including .agents for the notes root.
        current = root
        for part in entry.split('/'):
            current = current / part
            if current.is_symlink():
                raise ValueError('symbolic link in delivery path')
        if not path.exists():
            continue
        if path.is_file():
            result.add(_path(entry))
            continue
        if not path.is_dir():
            raise ValueError('invalid delivery path')
        def fail_walk(error):
            raise error
        for directory, dirs, files in os.walk(path, followlinks=False, onerror=fail_walk):
            for name in dirs + files:
                child = Path(directory) / name
                if child.is_symlink():
                    raise ValueError('symbolic link in delivery tree')
            for name in files:
                result.add(_path((Path(directory) / name).relative_to(root).as_posix()))
    return result


def build_install_manifest(source_root: Path, source_commit: str) -> dict:
    root = Path(source_root).resolve(strict=True)
    if not root.is_dir() or not isinstance(source_commit, str) or not _COMMIT.fullmatch(source_commit):
        raise ValueError('full source commit required')
    top = Path(os.fsdecode(_git(root, 'rev-parse', '--show-toplevel').strip())).resolve()
    if top != root:
        raise ValueError('source root must be repository root')
    resolved = _git(root, 'rev-parse', '--verify', source_commit + '^{commit}').decode('ascii').strip()
    if resolved != source_commit:
        raise ValueError('commit must be a full commit object id')
    # The worktree may match while the index contains different staged bytes.
    _git(root, 'diff', '--cached', '--quiet', source_commit, '--', 'SKILL.md', *_ROOTS)
    output = _git(root, 'ls-tree', '-rz', '--full-tree', source_commit, '--', 'SKILL.md', *_ROOTS)
    entries = {}
    for row in output.split(b'\0'):
        if not row:
            continue
        meta, raw_name = row.split(b'\t', 1)
        mode, kind, blob = meta.decode('ascii').split(' ')
        name = _path(os.fsdecode(raw_name))
        if mode not in ('100644', '100755') or kind != 'blob' or name in entries:
            raise ValueError('unsupported committed delivery entry')
        entries[name] = blob
    if not entries or 'SKILL.md' not in entries or _inventory(root) != set(entries):
        raise ValueError('source inventory differs from commit')
    files = []
    for name, blob in sorted(entries.items()):
        committed = _git(root, 'cat-file', 'blob', blob)
        if _read(root, name) != committed:
            raise ValueError('source bytes differ from commit: ' + name)
        files.append({'path': name, 'sha256': hashlib.sha256(committed).hexdigest()})
    return {'version': 1, 'source_commit': source_commit, 'files': files}


def _manifest(manifest):
    if not isinstance(manifest, dict) or set(manifest) != {'version', 'source_commit', 'files'}:
        raise ValueError('invalid manifest fields')
    if type(manifest['version']) is not int or manifest['version'] != 1:
        raise ValueError('unsupported manifest version')
    commit = manifest['source_commit']
    if not isinstance(commit, str) or not _COMMIT.fullmatch(commit):
        raise ValueError('invalid source commit')
    if not isinstance(manifest['files'], list) or not manifest['files']:
        raise ValueError('empty file list')
    entries = {}
    for item in manifest['files']:
        if not isinstance(item, dict) or set(item) != {'path', 'sha256'}:
            raise ValueError('invalid file entry')
        name = _path(item['path'])
        digest = item['sha256']
        if name in entries or not isinstance(digest, str) or not _SHA.fullmatch(digest):
            raise ValueError('duplicate path or invalid digest')
        entries[name] = digest
    if 'SKILL.md' not in entries:
        raise ValueError('missing skill entry')
    return entries


def check_installation(installation_root: Path, manifest: dict) -> dict:
    entries = _manifest(manifest)  # Validate every path before opening any installation file.
    root = Path(installation_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('installation root must be a directory')
    if _inventory(root) != set(entries):
        raise ValueError('installation inventory differs from manifest')
    for name, digest in entries.items():
        if hashlib.sha256(_read(root, name)).hexdigest() != digest:
            raise ValueError('installation bytes differ: ' + name)
    query_present = 'scripts/iter_queries.py' in entries
    runner = 'scripts/iter_run.py' in entries
    backend = ('scripts/iter_linux_job.py' if sys.platform == 'linux' else
               'scripts/iter_win_job.py' if sys.platform == 'win32' else None)
    backend_present = backend in entries if backend else False
    if sys.platform == 'linux':
        prerequisites = {
            'pidfd_open_api': callable(getattr(os, 'pidfd_open', None)),
            'pidfd_send_signal_api': callable(getattr(signal, 'pidfd_send_signal', None)),
            'proc_children_accessible': os.access('/proc/self/task/%s/children' % os.getpid(), os.R_OK),
        }
    elif sys.platform == 'win32':
        # Job Object behavior is not verified by merely observing the platform.
        prerequisites = {'job_object_execution': None}
    else:
        prerequisites = {'supported_platform': False}
    prerequisites_missing = any(value is False for value in prerequisites.values())
    return {
        'source': {'source_commit': manifest['source_commit'], 'files_match': True,
                   'trust': 'manifest supplied by caller; Git origin not reverified in copy'},
        'runtime_capabilities': {
            'query': {'status': 'PRESENT' if query_present else 'UNAVAILABLE',
                      'meaning': 'file presence only; execution not tested'},
            'runner': {'status': 'UNKNOWN' if runner and backend_present and not prerequisites_missing else 'UNAVAILABLE',
                       'platform': sys.platform, 'entry_present': runner,
                       'backend_present': backend_present, 'prerequisites': prerequisites,
                       'meaning': 'not executed; OS prerequisites and complete chain unverified'},
            'complete_chain': {'status': 'UNKNOWN', 'meaning': 'not tested'},
        },
    }


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--make-manifest', action='store_true')
    group.add_argument('--check', action='store_true')
    parser.add_argument('--root', required=True)
    parser.add_argument('--source-commit')
    parser.add_argument('--manifest')
    try:
        args = parser.parse_args(argv)
        if args.make_manifest:
            if not args.source_commit or args.manifest:
                raise ValueError('--make-manifest needs --source-commit only')
            result = build_install_manifest(Path(args.root), args.source_commit)
        else:
            if not args.manifest or args.source_commit:
                raise ValueError('--check needs --manifest only')
            with Path(args.manifest).open(encoding='utf-8') as stream:
                manifest = json.load(stream, object_pairs_hook=_unique_pairs)
            result = check_installation(Path(args.root), manifest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, UnicodeError, subprocess.SubprocessError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
