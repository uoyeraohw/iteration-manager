import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
old = Path('docs/todos/10-self-hosting-hardening/evidence/04/browser_harness.py')
new = Path('tests/support/browser_harness.py')
original = old.read_bytes()
extracted = new.read_bytes()
assert original.replace(b'parents[5]', b'parents[2]', 1) == extracted
status = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all', '--',
                         'docs/todos/10-self-hosting-hardening/evidence/04'], capture_output=True, text=True, check=True)
assert not status.stdout, status.stdout
blob = subprocess.run(['git', 'show', '3158e75869d5c4346c51256de878f14ea190f305:' + str(old)],
                      capture_output=True, check=True).stdout
assert blob == original
payload = Path('/tmp/iter11-task07-regression-v2/test_payload_copy_runs_handoff0/payload')
receipt = json.loads((payload / 'installed-copy-receipt.json').read_text())
assert receipt['status'] == 'COMPLETED' and receipt['raw_exit_code'] == 0 and receipt['tree_terminal']
assert not (payload / 'docs/todos').exists()
print(json.dumps({'original_sha256': hashlib.sha256(original).hexdigest(),
                  'support_sha256': hashlib.sha256(extracted).hexdigest(),
                  'comparison': 'only parents[5] to parents[2]',
                  'history_git_status': status.stdout or 'clean',
                  'payload_path': str(payload), 'payload_history_exists': False,
                  'payload_receipt': receipt,
                  'payload_output': (payload / receipt['output']).read_text(),
                  'regression_coverage': 'fixture isolation and real path, ready/stop, HTTP normal/loading/evidence/error, argument rejection',
                  'native_browser': 'not run; no UI behavior change'}, indent=2))
