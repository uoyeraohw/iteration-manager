"""Read only the explicit historical delivery manifest and named entry points."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
MAIN = Path('C:/Users/qingyu/.codeg/skills/iteration-manager')
OUT = ROOT / 'docs/todos/10-self-hosting-hardening/evidence/05'

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args]).decode().strip()

def save(name, value):
    path = OUT / name
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')

now = datetime.now(timezone.utc).isoformat()
history = MAIN / 'build/git-init-sync-20261112-120855'
plan = json.loads((history / 'deployment-plan.json').read_text(encoding='utf-8'))
paths = sorted({item['relative'] for item in plan['items']})
assert len(paths) == plan['files_per_target'] == 58
captures = []
for label, source in [
    ('git-final', history / 'final-receipt.json'),
    ('manifest', history / 'deployment-plan.json'),
    ('deployment', history / 'deployment.json'),
    ('r7-acceptance', MAIN / 'build/stage10-checkpoint-resume-20261111/fs-r7-migration-independent/ACCEPTANCE.md'),
    ('p1-readme', MAIN / 'build/p1-inventory-20261113/README.md'),
]:
    suffix = source.suffix
    target = OUT / ('slice-a-original-' + label + suffix)
    with target.open('xb') as stream:
        stream.write(source.read_bytes())
    captures.append({'original_absolute_path': source.as_posix(), 'capture': target.relative_to(ROOT).as_posix(), 'captured_at': now, 'scope': 'complete original bytes, not a retelling'})
targets = [MAIN, Path('C:/Users/qingyu/.codex/skills/iteration-manager'), Path('C:/Users/qingyu/.gemini/config/skills/iteration-manager')]
observations = []
for target in targets:
    files = []
    for relative in paths:
        file = target / relative
        item = {'path': relative, 'exists': file.is_file()}
        if file.is_file():
            data = file.read_bytes()
            item['equals_main'] = data == (MAIN / relative).read_bytes()
            item['equals_iter10_base'] = data == (ROOT / relative).read_bytes()
            item['equals_historical_capture'] = data == (history / 'source' / relative).read_bytes()
        files.append(item)
    entries = {}
    for relative in ['SKILL.md', 'scripts/iter_sync.py', 'scripts/iter_templates.py', 'scripts/iter_query.py', 'references/template_generation.md']:
        file = target / relative
        entries[relative] = {'exists': file.is_file(), 'equals_iter10_base': file.is_file() and file.read_bytes() == (ROOT / relative).read_bytes()}
    observations.append({'target': target.as_posix(), 'observed_version': 'UNKNOWN', 'files': files, 'entries': entries})
reviews = []
for task in ['01', '02', '03', '04']:
    path = ROOT / f'docs/todos/10-self-hosting-hardening/evidence/{task}/review.json'
    receipt = json.loads(path.read_text(encoding='utf-8'))
    assert receipt['verdict'] == 'APPROVED'
    pointers = [receipt['review_report']] + [c['output'] for c in receipt['checks']]
    assert all((ROOT / p).is_file() for p in pointers)
    reviews.append({'task': task, 'reviewed_candidate': receipt['head_sha'], 'verdict': receipt['verdict'], 'receipt': path.relative_to(ROOT).as_posix(), 'pointers': pointers})
result = {'checked_at': now, 'source_commit': git(ROOT, 'rev-parse', 'HEAD'), 'main_commit': git(MAIN, 'rev-parse', 'HEAD'), 'main_branch': git(MAIN, 'branch', '--show-current'), 'manifest_scope': '58 explicit historical delivery paths plus five named entry points; no recursive installation scan', 'captures': captures, 'p1_deployment_json_exists': (MAIN / 'build/p1-inventory-20261113/deployment.json').is_file(), 'observations': observations, 'reviews': reviews}
save('slice-a-observation.json', result)
print(json.dumps(result, ensure_ascii=False, indent=2))
