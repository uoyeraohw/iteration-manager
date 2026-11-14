"""Correct the singular query-entry spelling without rewriting first evidence."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
main = Path('C:/Users/qingyu/.codeg/skills/iteration-manager')
result = {'checked_at': datetime.now(timezone.utc).isoformat(),
          'correction': 'First experiment named scripts/iter_query.py; actual source is scripts/iter_queries.py. Original evidence remains unchanged.',
          'tags': [], 'entries': [], 'native': []}
for source in (root, main):
    p = subprocess.run(['git', '-C', str(source), 'describe', '--tags', '--exact-match', 'HEAD'], capture_output=True, text=True)
    result['tags'].append({'root': source.as_posix(), 'argv': ['git', 'describe', '--tags', '--exact-match', 'HEAD'], 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr, 'observed_version': p.stdout.strip() if p.returncode == 0 else 'UNKNOWN'})
for target in (main, Path('C:/Users/qingyu/.codex/skills/iteration-manager'), Path('C:/Users/qingyu/.gemini/config/skills/iteration-manager')):
    entries = []
    for relative in ('scripts/iter_queries.py', 'scripts/iter_cli.py'):
        file = target / relative
        entries.append({'path': relative, 'exists': file.is_file(), 'equals_iter10_base': file.is_file() and file.read_bytes() == (root / relative).read_bytes()})
    result['entries'].append({'target': target.as_posix(), 'entries': entries})
for task, name in [('01', 'native-terminal-implementation-b.json'), ('02', 'native-terminal-c.json'), ('03', 'native-terminal-c.json'), ('04', 'native-terminal-a.json')]:
    path = f'docs/todos/10-self-hosting-hardening/evidence/{task}/{name}'
    record = json.loads((root / path).read_text(encoding='utf-8'))
    result['native'].append({'source_pointer': path, 'guard_reason': record['guard']['reason'], 'status': record['guard']['final']['status'], 'scope': 'slice native terminal, not final candidate approval or installed consumption'})
out = root / 'docs/todos/10-self-hosting-hardening/evidence/05/slice-a-entry-observation.json'
with out.open('x', encoding='utf-8') as stream:
    json.dump(result, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
