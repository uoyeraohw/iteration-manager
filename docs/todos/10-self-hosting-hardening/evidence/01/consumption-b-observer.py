"""Read-only workspace/Git observation and direct-byte snapshot comparison."""
import base64
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path.cwd()
OUT = ROOT / 'docs/todos/10-self-hosting-hardening/evidence/01/consumption-b'

def git(*args):
    p = subprocess.run(['git', *args], capture_output=True)
    return {'argv': ['git', *args], 'exit_code': p.returncode,
            'stdout': p.stdout.decode('utf-8', 'replace'),
            'stderr': p.stderr.decode('utf-8', 'replace')}

def snapshot():
    files = git('ls-files', '-c', '-o', '--exclude-standard', '-z')['stdout'].split('\0')
    contents = {}
    for name in sorted(set(files)):
        if not name or name.startswith('docs/todos/10-self-hosting-hardening/evidence/01/consumption-b/'):
            continue
        p = ROOT / name
        if p.is_file():
            contents[name] = base64.b64encode(p.read_bytes()).decode('ascii')
    inventory = {}
    for p in ROOT.rglob('*'):
        if p.is_file() and '.git' not in p.relative_to(ROOT).parts and OUT not in p.parents:
            s = p.stat()
            inventory[p.relative_to(ROOT).as_posix()] = [s.st_size, s.st_mtime_ns]
    return {'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'cwd': str(ROOT), 'files_base64': contents, 'disk_inventory': inventory,
            'git': {key: git(*args) for key, args in {
                'head': ['rev-parse', 'HEAD'], 'branch': ['branch', '--show-current'],
                'status': ['status', '--porcelain=v1', '--untracked-files=all'],
                'cached': ['diff', '--cached', '--binary'], 'diff': ['diff', '--binary'],
                'refs': ['show-ref'], 'worktrees': ['worktree', 'list', '--porcelain'],
                'reflog': ['reflog', '-10', '--format=%H %gs']}.items()}}

def compare(a, b):
    left, right = a['files_base64'], b['files_base64']
    changed = [p for p in sorted(set(left) | set(right)) if left.get(p) != right.get(p)]
    disk = [p for p in sorted(set(a['disk_inventory']) | set(b['disk_inventory']))
            if a['disk_inventory'].get(p) != b['disk_inventory'].get(p)]
    git_changes = [k for k in a['git'] if a['git'][k] != b['git'][k]]
    return {'byte_changed_paths': changed, 'disk_metadata_changed_paths': disk,
            'git_changed_fields': git_changes, 'byte_compared_file_count': len(left),
            'unchanged': not changed and not disk and not git_changes,
            'exclusion': 'Only parent-owned consumption-b evidence directory excluded; ignored files covered by disk size/mtime inventory, not byte comparison.'}

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    if sys.argv[1] == 'snapshot':
        path = OUT / (sys.argv[2] + '.json')
        with path.open('x', encoding='utf-8') as f:
            json.dump(snapshot(), f, ensure_ascii=False, indent=2)
        print(path)
    elif sys.argv[1] == 'compare':
        a, b = [json.loads((OUT / (x + '.json')).read_text(encoding='utf-8')) for x in sys.argv[2:4]]
        result = compare(a, b)
        with (OUT / (sys.argv[4] + '.json')).open('x', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result['unchanged'] else 1)
