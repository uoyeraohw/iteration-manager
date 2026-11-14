"""Compare the extracted dispatcher and existing API against the C baseline."""
import ast
import json
import subprocess
from pathlib import Path

root = Path.cwd()
old = subprocess.run(['git', 'show', '268f221742f2b22ff8faa88a53ac50b18947f57f:scripts/iter_sync.py'],
                     capture_output=True, text=True, check=True, encoding='utf-8').stdout
new = (root / 'scripts/iter_sync.py').read_text(encoding='utf-8')
cli = (root / 'scripts/iter_cli.py').read_text(encoding='utf-8')
assert old.split('def main():\n')[0] == new.split('def main():\n')[0]
old_main = next(n for n in ast.parse(old).body if isinstance(n, ast.FunctionDef) and n.name == 'main')
new_main = next(n for n in ast.parse(cli).body if isinstance(n, ast.FunctionDef) and n.name == '_dispatch')
# Parameter acquisition and the expanded help text are the only body changes.
new_main.body[1] = old_main.body[1]
old_help = next(n for n in ast.walk(old_main) if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.startswith('Iteration Manager:'))
new_help = next(n for n in ast.walk(new_main) if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.startswith('Timing:'))
new_help.value = old_help.value
assert [ast.dump(n) for n in old_main.body] == [ast.dump(n) for n in new_main.body]

evidence = root / 'docs/todos/10-self-hosting-hardening/evidence/03'
series = {}
signatures = {}
for label, filename in [('before', 'slice-a-before-1732.json.output.txt'), ('after', 'slice-c-after-1751.json.output.txt')]:
    rows = [json.loads(line) for line in (evidence / filename).read_text(encoding='utf-8').splitlines() if line.startswith('{')]
    signatures[label] = rows[0]['signatures']
    series[label] = [{key: row[key] for key in ('size', 'repeat', 'seconds', 'git_call_count')} for row in rows[1:]]
signature_changes = {name: {'before': value, 'after': signatures['after'].get(name)}
                     for name, value in signatures['before'].items() if signatures['after'].get(name) != value}
print(json.dumps(dict(signature_changes=signature_changes,
                     added_exports=sorted(set(signatures['after']) - set(signatures['before'])))))
assert not signature_changes
assert [(r['size'], r['repeat']) for r in series['before']] == [(r['size'], r['repeat']) for r in series['after']]
print(json.dumps(dict(api_signatures_unchanged=True, legacy_prefix_unchanged=True,
                     dispatcher_body_unchanged_except_argv_and_help=True,
                     benchmark=series, performance_claim=None), indent=2))
