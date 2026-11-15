"""Task00-only bounded bootstrap observation; never a formal runner receipt."""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deadline', required=True)
    parser.add_argument('--evidence', required=True)
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv[:1] == ['--'] else args.argv
    root = Path.cwd().resolve()
    receipt = (root / args.evidence).resolve()
    if not receipt.is_relative_to(root) or not argv:
        raise ValueError('Nonempty argv and project-relative evidence required')
    receipt.parent.mkdir(parents=True, exist_ok=True)
    end = datetime.fromisoformat(args.deadline.replace('Z', '+00:00'))
    if end.tzinfo is None:
        raise ValueError('Absolute timezone-aware deadline required')
    start = datetime.now(timezone.utc)
    seconds = min(180, (end - start).total_seconds() - 5)
    record = dict(kind='task00-bootstrap-observation', argv=argv, cwd=str(root),
                  deadline=end.isoformat(), checked_at=start.isoformat(),
                  formal_runner_receipt=False, status='NOT_STARTED', exit_code=None)
    output = receipt.with_name(receipt.name + '.output.txt')
    with receipt.open('x', encoding='utf-8') as stream:
        def save():
            stream.seek(0)
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.truncate()
            stream.flush()
        save()
        with output.open('x', encoding='utf-8') as log:
            if seconds <= 0:
                code = 124
            else:
                record.update(status='RUNNING', started_at=datetime.now(timezone.utc).isoformat())
                save()
                bounded = ['timeout', '--signal=TERM', '--kill-after=5s', f'{seconds:.3f}s', *argv]
                record['bootstrap_argv'] = bounded
                code = subprocess.run(bounded, cwd=root, stdout=log, stderr=subprocess.STDOUT).returncode
                record['status'] = 'TIMED_OUT_OR_KILLED' if code in (124, 137) else 'COMPLETED'
            record.update(exit_code=code, ended_at=datetime.now(timezone.utc).isoformat(),
                          output=output.relative_to(root).as_posix())
            save()
    print(json.dumps(record, ensure_ascii=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
