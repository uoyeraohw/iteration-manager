import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('phase', choices=['before', 'after'])
a = p.parse_args()
root = Path.cwd()
out = root / 'docs/todos/11-reliable-delivery/evidence/07'
consumer = root / 'tests/test_board_handoff.py'
historical = 'docs/todos/10-self-hosting-hardening/evidence/04/browser_harness.py'
count = consumer.read_text(encoding='utf-8').count(historical)
print(json.dumps({'phase': a.phase, 'historical_path_consumers': count, 'python': sys.executable,
                  'platform': sys.platform, 'sample': 'test_board_handoff browser_harness checks'}), flush=True)
failed = False
for n in range(1, 4):
    argv = [sys.executable, '-B', '-m', 'pytest', '-p', 'no:cacheprovider',
            'tests/test_board_handoff.py', '-q', '-k', 'browser_harness or browser_http_harness',
            '--basetemp', f'/tmp/iter11-task07-measure-{a.phase}-{n}']
    start = time.monotonic()
    result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration = time.monotonic() - start
    path = out / f'measure-{a.phase}-{n}.txt'
    path.write_bytes(result.stdout)
    print(json.dumps({'run': n, 'argv': argv, 'duration_seconds': duration,
                      'exit_code': result.returncode, 'output': str(path.relative_to(root))}), flush=True)
    failed |= result.returncode != 0
sys.exit(1 if failed else 0)
