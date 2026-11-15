"""One-shot task 06 experiment; retain clean C1 source and temporary copy."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COMMIT = '6ee7605de94fde0dfb4454f512b9913fd7aa01ae'
REPOSITORY = Path.cwd()
EVIDENCE = REPOSITORY / 'docs/todos/11-reliable-delivery/evidence/06'
ROOTS = ('SKILL.md', 'scripts', 'references', 'templates', 'tests', '.agents/notes')
experiment = Path(tempfile.mkdtemp(prefix='iter11-task06-real-payload-', dir='/tmp'))
source = experiment / 'source'
copy = experiment / 'installation'
copy.mkdir()
print('experiment:', experiment, flush=True)


def run(name, argv, expected=0):
    result = subprocess.run([str(a) for a in argv], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for suffix, data in (('stdout', result.stdout), ('stderr', result.stderr)):
        with (EVIDENCE / ('fix1-' + name + '.' + suffix + '.bin')).open('xb') as output:
            output.write(data)
    print(json.dumps({'step': name, 'argv': [str(a) for a in argv],
                      'exit_code': result.returncode, 'expected': expected}), flush=True)
    if result.returncode != expected:
        raise RuntimeError(name + ' unexpected exit')
    return result.stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


run('clone', ['git', 'clone', '--no-local', '--no-checkout', str(REPOSITORY), str(source)])
run('checkout', ['git', '-C', source, 'checkout', '--detach', COMMIT])
head = run('head', ['git', '-C', source, 'rev-parse', 'HEAD']).decode().strip()
if head != COMMIT:
    raise RuntimeError('incorrect checked out commit')
status = run('status', ['git', '-C', source, 'status', '--porcelain', '--untracked-files=all'])
if status:
    raise RuntimeError('source checkout is dirty')
entry = source / 'scripts/iter_install.py'
manifest_bytes = run('manifest', [sys.executable, '-B', entry, '--make-manifest', '--root', source,
                                   '--source-commit', COMMIT])
manifest = json.loads(manifest_bytes)
if manifest['source_commit'] != COMMIT:
    raise RuntimeError('wrong manifest source')
manifest_path = experiment / 'manifest.json'
manifest_path.write_bytes(manifest_bytes)
tree = run('tree', ['git', '-C', source, 'ls-tree', '-rz', '--full-tree', COMMIT, '--', *ROOTS])
entries = {}
for line in tree.split(b'\0'):
    if not line:
        continue
    meta, path = line.split(b'\t', 1)
    mode, kind, oid = meta.decode('ascii').split()
    if mode not in ('100644', '100755') or kind != 'blob':
        raise RuntimeError('unexpected tree mode')
    entries[os.fsdecode(path)] = oid
listed = {item['path']: item['sha256'] for item in manifest['files']}
if len(listed) != len(manifest['files']) or set(entries) != set(listed):
    raise RuntimeError('manifest paths differ from actual committed whitelist')
for name, expected in listed.items():
    data = (source / name).read_bytes()
    if digest(data) != expected:
        raise RuntimeError('source digest differs: ' + name)
    destination = copy / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    if digest(destination.read_bytes()) != expected:
        raise RuntimeError('copy digest differs: ' + name)
manifest_copy = EVIDENCE / 'fix1-real-payload-manifest.json'
with manifest_copy.open('xb') as output:
    output.write(manifest_bytes)
check = run('check-clean', [sys.executable, '-B', copy / 'scripts/iter_install.py', '--check',
                             '--root', copy, '--manifest', manifest_path])
report = json.loads(check)
if not report['source']['files_match'] or report['source']['source_commit'] != COMMIT:
    raise RuntimeError('incorrect clean check result')
mutated = copy / 'SKILL.md'
with mutated.open('ab') as output:
    output.write(b'\nsmoke drift\n')
if digest(mutated.read_bytes()) == listed['SKILL.md']:
    raise RuntimeError('drift not created')
run('check-drift', [sys.executable, '-B', copy / 'scripts/iter_install.py', '--check',
                     '--root', copy, '--manifest', manifest_path], expected=2)
summary = {'version': 1, 'source_commit': COMMIT, 'temporary_root': str(experiment),
           'source_root': str(source), 'installation_root': str(copy),
           'manifest_file_count': len(listed), 'git_tree_file_count': len(entries),
           'manifest_sha256': digest(manifest_bytes),
           'files': [{'path': name, 'sha256': listed[name], 'git_blob': entries[name]}
                     for name in sorted(listed)],
           'clean_exit': 0, 'drift_exit': 2, 'drift_path': 'SKILL.md',
           'drift_sha256': digest(mutated.read_bytes()),
           'runtime_capabilities': report['runtime_capabilities'],
           'limitations': ['copy is intentionally left drifted', 'no deployment or host adoption',
                           'runner and complete chain not exercised by installation check']}
with (EVIDENCE / 'fix1-real-payload-inventory.json').open('x', encoding='utf-8') as output:
    json.dump(summary, output, ensure_ascii=False, indent=2)
    output.write('\n')
print('file_count:', len(listed), 'clean: 0 drift: 2', flush=True)
print('capabilities:', json.dumps(report['runtime_capabilities'], ensure_ascii=False), flush=True)
