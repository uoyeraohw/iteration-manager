"""Repeatable synthetic projection benchmark; run through the frozen runner."""
import argparse
import inspect
import json
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import iter_sync

SIZES = (10, 100)
REPEATS = 3
STATUSES = ('TODO', 'IN_PROGRESS', 'TESTING', 'DONE', 'FUSED')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    print(json.dumps(dict(label=args.label, python=sys.version, platform=platform.platform(),
                         sizes=SIZES, repeats=REPEATS, statuses=STATUSES,
                         workload='one board plus all task envelopes; fixture setup excluded',
                         limitation='synthetic cards; DONE missing receipt; no approved-binding workload',
                         signatures={name: str(inspect.signature(value)) for name, value in vars(iter_sync).items()
                                     if inspect.isfunction(value)},
                         candidate=subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                                  capture_output=True, text=True, check=True).stdout.strip())))
    real_run = subprocess.run
    with tempfile.TemporaryDirectory(prefix='iter10-query-benchmark-') as temp:
        for size in SIZES:
            directory = Path(temp) / 'docs/todos' / f'{size}-fixed'
            directory.mkdir(parents=True)
            (directory / 'README.md').write_text('# Benchmark\n', encoding='utf-8')
            for index in range(size):
                (directory / f'{index + 1:03}-task.md').write_text(
                    f'---\nschema_version: 1\ntask_id: "{index + 1:03}"\n'
                    f'status: {STATUSES[index % len(STATUSES)]}\ntype: Strict-TDD\n---\n'
                    '<!-- iter:stages -->\n- [ ] fixed stage\n<!-- /iter:stages -->\n', encoding='utf-8')
            files = sorted(directory.glob('*-task.md'))
            for repeat in range(1, REPEATS + 1):
                git_calls = []

                def observed_run(argv, *positional, **kwargs):
                    if isinstance(argv, (tuple, list)) and Path(str(argv[0])).stem.lower() == 'git':
                        git_calls.append(list(argv))
                    return real_run(argv, *positional, **kwargs)

                with patch.object(subprocess, 'run', observed_run):
                    started = time.perf_counter()
                    board = iter_sync.generate_board_data(directory)
                    envelopes = [iter_sync.render_task_envelope(path, Path(temp)) for path in files]
                    elapsed = time.perf_counter() - started
                assert board['total'] == size
                assert all('TASK_HANDOFF' in item for item in envelopes)
                print(json.dumps(dict(label=args.label, size=size, repeat=repeat,
                                     seconds=elapsed, git_call_count=len(git_calls), git_calls=git_calls,
                                     board_keys=sorted(board), card_keys=sorted(board['cards'][0]))), flush=True)


if __name__ == '__main__':
    main()
