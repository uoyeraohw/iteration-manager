"""Synthetic approved-chain benchmark, never evidence of human or business approval."""
import argparse
import hashlib
import http.client
import http.server
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'scripts'))
from iter_queries import audit_task_file, render_task_envelope
from iter_sync import generate_board_data, LiveBoardHandler
from iter_inventory import inventory


def run_git(root, *args):
    return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def dump(path, obj):
    write(path, json.dumps(obj, indent=2) + '\n')


def make_workload(root, mode, size):
    """Adapt mature completion-gate and filesystem-delivery synthetic fixtures."""
    root.mkdir(parents=True)
    directory = root / 'docs/todos/01-synthetic'
    directory.mkdir(parents=True)
    readme = directory / 'README.md'
    write(readme, '# Synthetic workload\n<!-- iter:goal -->\nSynthetic frozen goal\n<!-- /iter:goal -->\n')
    if mode == 'git':
        run_git(root, 'init', '-b', 'main')
        run_git(root, 'config', 'user.name', 'Synthetic benchmark')
        run_git(root, 'config', 'user.email', 'synthetic@example.invalid')
        run_git(root, 'add', '.')
        run_git(root, 'commit', '-m', 'Synthetic base')
    elif mode == 'filesystem':
        dump(directory / 'iteration-delivery.json', {'schema_version': 1, 'mode': 'filesystem'})
    else:
        raise ValueError(mode)
    cards, receipts = [], []
    for i in range(1, size + 1):
        ident = f'{i:03d}'
        if mode == 'git':
            base = run_git(root, 'rev-parse', 'HEAD')
        card = directory / f'{ident}-task.md'
        evidence = f'docs/todos/01-synthetic/evidence/{ident}'
        source = f'src/{ident}.py'
        write(root / source, f'# synthetic workload {ident}\nvalue = 1\n')
        checks = []
        for name in ('experiment', 'decision', 'interfaces'):
            out = f'{evidence}/{name}.txt'
            write(root / out, f'Synthetic workload fixture: {name}; not a real execution or approval.\n')
            check = dict(name=name, kind='command' if name == 'experiment' else 'observation', summary='Synthetic workload fixture', output=out)
            if name == 'experiment':
                check.update(command='synthetic workload command (not executed)', cwd='.', exit_code=0)
            checks.append(check)
        report = f'{evidence}/review.txt'
        write(root / report, 'Synthetic review fixture; not a human review or business approval.\n')
        receipt_path = f'{evidence}/review.json'
        mode_meta = (f'delivery_mode: filesystem\ncandidate_id: synthetic-{ident}\n' if mode == 'filesystem' else f'base_sha: {base}\nhead_sha: ""\n')
        content = (f'---\nschema_version: 1\ntask_id: "{ident}"\ntype: Spike-Discovery\nstatus: TESTING\n'
                   + mode_meta + f'review_status: PENDING\ntdd_verified: false\nreview_receipt: {receipt_path}\n---\n'
                   + f'## Objective\nSynthetic workload {ident}\n<!-- iter:scope -->\n| File path | Role |\n| --- | --- |\n| `{source}` | source |\n| `{evidence}/` | evidence |\n<!-- /iter:scope -->\n'
                   + '<!-- iter:acceptance -->\n- [x] Synthetic acceptance\n<!-- /iter:acceptance -->\n<!-- iter:ledger -->\nSynthetic fixture only\n<!-- /iter:ledger -->\n')
        write(card, content)
        receipt = dict(schema_version=1, task_id=ident, type='Spike-Discovery', task_path=card.relative_to(root).as_posix(), implementer='synthetic-implementer', reviewer='synthetic-reviewer', verdict='APPROVED', review_report=report, checks=checks)
        if mode == 'git':
            run_git(root, 'add', '.')
            run_git(root, 'commit', '-m', f'Synthetic candidate {ident}')
            head = run_git(root, 'rev-parse', 'HEAD')
        text = card.read_text(encoding='utf-8').replace('status: TESTING', 'status: DONE').replace('review_status: PENDING', 'review_status: APPROVED')
        if mode == 'git':
            receipt.update(base_sha=base, head_sha=head, contract_sha=head)
            text = text.replace('head_sha: ""', f'head_sha: {head}')
        else:
            frozen = f'frozen/{ident}'
            files = []
            for n, source in enumerate([f'src/{ident}.py'] + [c['output'] for c in receipt['checks']]):
                snap = f'{frozen}/file-{n}'
                write(root / snap, (root / source).read_text(encoding='utf-8'))
                files.append(dict(path=source, snapshot=snap))
            dump(root / f'{frozen}/manifest.json', dict(candidate_id=f'synthetic-{ident}', files=files))
            write(root / f'{frozen}/contract.md', text)
            write(root / f'{frozen}/goal.md', readme.read_text(encoding='utf-8'))
            receipt.update(receipt_kind='current-filesystem-review-v1', delivery_mode='filesystem', candidate_id=f'synthetic-{ident}', recorded_at='2026-11-15T00:00:00+00:00', candidate_manifest=f'{frozen}/manifest.json', contract_snapshot=f'{frozen}/contract.md', goal_snapshot=f'{frozen}/goal.md')
        write(card, text)
        dump(root / receipt_path, receipt)
        if mode == 'git':
            run_git(root, 'add', '.')
            run_git(root, 'commit', '-m', f'Synthetic registration {ident}')
        cards.append(card)
        receipts.append((receipt_path, receipt))
    if mode == 'git':
        current = run_git(root, 'rev-parse', 'HEAD')
    context = {'version': 1, 'tasks': {}}
    for card, (_, receipt) in zip(cards, receipts):
        ident = receipt['task_id']
        context['tasks'][ident] = dict(phase='implementation', candidate=current if mode == 'git' else f'synthetic-{ident}', inputs=[card.relative_to(root).as_posix()], capabilities=['synthetic-benchmark'], dependencies=[], tool_entry=str(PROJECT / 'scripts/iter_sync.py'), checkpoint='Synthetic approved workload', remaining_work=['No actual dispatch'], observations={k: dict(status='READY', evidence=receipt['checks'][0]['output'], summary='Synthetic workload observation, not actual authority') for k in ('authority','execution','verification')})
    return directory, cards, context


class Counters:
    """Count launched git processes and bytes returned by Path read methods only."""
    def __enter__(self):
        self.git_calls = self.bytes = self.read_calls = 0
        self.popen, self.read_bytes, self.read_text = subprocess.Popen, Path.read_bytes, Path.read_text
        owner = self
        def popen(args, *a, **kw):
            if isinstance(args, (tuple, list)) and args and Path(str(args[0])).name == 'git': owner.git_calls += 1
            return owner.popen(args, *a, **kw)
        def read_bytes(path):
            result = owner.read_bytes(path); owner.read_calls += 1; owner.bytes += len(result); return result
        def read_text(path, *a, **kw):
            result = owner.read_text(path, *a, **kw); owner.read_calls += 1; owner.bytes += len(result.encode(kw.get('encoding') or 'utf-8')); return result
        subprocess.Popen, Path.read_bytes, Path.read_text = popen, read_bytes, read_text
        return self
    def __exit__(self, *args):
        subprocess.Popen, Path.read_bytes, Path.read_text = self.popen, self.read_bytes, self.read_text


def benchmark(root, directory, cards, context, repeats, save):
    # The full gate precedes all trials; no patched audit or successful result.
    audits = [audit_task_file(card) for card in cards]
    assert all(a['verdict'] == 'PASS' for a in audits), audits
    assert generate_board_data(directory)['accepted'] == len(cards)
    handler = type('SyntheticHandler', (LiveBoardHandler,), {'iter_dir': directory, 'log_message': lambda *a: None})
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    def http_read():
        connection = http.client.HTTPConnection('127.0.0.1', server.server_address[1])
        try:
            connection.request('GET', f'/api/evidence?task={cards[0].name}&source=1')
            response = connection.getresponse(); body = response.read()
            assert response.status == 200 and b'Synthetic review fixture' in body
        finally: connection.close()
    def board():
        result = generate_board_data(directory)
        assert result['accepted'] == len(cards), result
    def envelopes():
        for card in cards:
            result = render_task_envelope(card, root)
            assert result['TASK_HANDOFF']['acceptance_verdict'] == 'PASS', result
    def inv():
        result = inventory(directory, root, 'continue', context=context)
        assert len(result['tasks']) == len(cards) and all(t['acceptance_verdict'] == 'PASS' for t in result['tasks']), result
        return result['readiness']
    results = {}
    try:
        for name, operation in [('board', board), ('all_envelopes', envelopes), ('inventory', inv), ('http_evidence', http_read)]:
            trials = []
            for _ in range(repeats):
                with Counters() as count:
                    start = time.perf_counter(); detail = operation(); seconds = time.perf_counter() - start
                trials.append(dict(seconds=seconds, git_calls=count.git_calls, path_read_calls=count.read_calls, path_read_bytes=count.bytes, detail=detail))
                results[name] = dict(trials=trials)
                save(results)
                print(f'{directory.parent.parent.parent.name} {len(cards)} {name} trial {len(trials)}: {seconds:.6f}s, git={count.git_calls}, path_read_bytes={count.bytes}', flush=True)
            values = [t['seconds'] for t in trials]
            results[name].update(mean_seconds=statistics.mean(values), range_seconds=[min(values), max(values)])
            save(results)
    finally:
        server.shutdown(); server.server_close(); thread.join()
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sizes', nargs='+', type=int, required=True)
    parser.add_argument('--repeats', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.repeats < 1 or any(n < 1 for n in args.sizes): parser.error('positive sizes and repeats required')
    out = args.output.resolve()
    source_files = sorted((PROJECT / 'scripts').glob('*.py')) + [Path(__file__).resolve(), PROJECT / 'tests/test_approval_benchmark_fixture.py']
    manifest = {p.relative_to(PROJECT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files if p.exists()}
    result = dict(label='Synthetic workload receipts and reviews; not human or business approval', base=run_git(PROJECT, 'rev-parse', 'HEAD'), source_sha256=manifest, environment=dict(python=sys.version, platform=platform.platform(), cpu=platform.processor(), cpu_count=os.cpu_count(), cpu_model=next((line.split(':', 1)[1].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')), 'unknown'), memory_kib=next((line.split(':', 1)[1].strip() for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemTotal')), 'unknown'), git=run_git(PROJECT, '--version')), definitions={'git_calls':'actual git subprocess launches during operation', 'path_read_bytes':'bytes returned by Path.read_bytes and encoded Path.read_text; excludes git subprocess, open(), HTTP socket and OS reads', 'timing':'includes query and assertions/client HTTP read; excludes fixture construction, preflight audit, server startup and shutdown', 'limits':'synthetic Spike fixtures; Python stdlib HTTP is not browser evidence; 3 trials do not establish tail latency'}, workloads=[])
    dump(out, result)
    for mode in ('git', 'filesystem'):
        for size in args.sizes:
            root = Path(tempfile.mkdtemp(prefix=f'iter11-task08-{mode}-{size}-', dir='/tmp')) / 'project'
            print(f'Building synthetic {mode} workload size={size}: {root}', flush=True)
            directory, cards, context = make_workload(root, mode, size)
            row = dict(mode=mode, size=size, root=str(root), approved_count=0, operations={})
            result['workloads'].append(row); dump(out, result)
            def save(ops):
                row['approved_count'] = size; row['operations'] = ops; dump(out, result)
            benchmark(root, directory, cards, context, args.repeats, save)
    return 0

if __name__ == '__main__':
    sys.exit(main())
