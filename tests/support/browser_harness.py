"""Real HTTP boundaries for root's native browser checks; fixtures are synthetic."""
import argparse
import http.server
import json
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from iter_autonomy import load_state
from iter_sync import LiveBoardHandler, generate_board_data


def filesystem_fixture(root):
    directory = root / 'docs/todos/01-synthetic-fs'
    directory.mkdir(parents=True)
    (directory / 'iteration-delivery.json').write_text(
        json.dumps({'schema_version': 1, 'mode': 'filesystem'}), encoding='utf-8')
    (directory / 'README.md').write_text('# SYNTHETIC FS\n', encoding='utf-8')
    evidence = root / 'evidence'
    evidence.mkdir()
    (evidence / 'progress.txt').write_text('SYNTHETIC: template/HTTP fixture, not native acceptance.', encoding='utf-8')
    (evidence / 'report.txt').write_text('SYNTHETIC provenance; no independent approval.', encoding='utf-8')
    (evidence / 'attempt.json').write_text('{"synthetic":true}', encoding='utf-8')
    (evidence / 'sources.json').write_text(json.dumps({
        'review_report': 'evidence/report.txt',
        'checks': [{'name': 'synthetic progress', 'output': 'evidence/progress.txt'}]}), encoding='utf-8')
    meta = {'schema_version': '1', 'task_id': '01', 'type': 'UI-Component',
        'status': 'IN_PROGRESS', 'task_name': 'SYNTHETIC · FS交接样例',
        'delivery_mode': 'filesystem', 'candidate_id': 'synthetic-fs-current-a',
        'review_receipt': 'evidence/sources.json'}
    state = load_state(meta)
    state['events']['synthetic-attempt'] = {'input': {'action': 'attempt', 'attempt': {
        'candidate': 'synthetic-fs-original-a', 'phase': 'implementation',
        'checkpoint': 'SYNTHETIC · 已保存模板检查点', 'source': 'evidence/attempt.json',
        'progress': [{'kind': 'implementation', 'evidence': 'evidence/progress.txt',
                      'summary': 'SYNTHETIC · 可读列明证据'}],
        'remaining_work': ['由根执行真实浏览器交互与四态观测', '非参与者独立审查']}}}
    meta['autonomy_state'] = json.dumps(state)
    (directory / '01-task.md').write_text('---\n' + ''.join(
        f'{key}: {json.dumps(value, ensure_ascii=False)}\n' for key, value in meta.items()) +
        '---\n<!-- iter:stages -->\n- [x] SYNTHETIC checkpoint\n- [ ] Native browser pending\n<!-- /iter:stages -->\n', encoding='utf-8')
    return directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stop-file', type=Path, required=True)
    parser.add_argument('--ready-file', type=Path, required=True)
    parser.add_argument('--duration', type=float, default=120)
    parser.add_argument('--delay', type=float, default=6)
    parser.add_argument('--isolated-fixtures', action='store_true',
                        help='Use only temporary synthetic inventory; not native self-use evidence')
    args = parser.parse_args()
    if args.duration <= 0 or args.delay < 0:
        parser.error('duration must be positive; delay must be nonnegative')
    if args.stop_file.exists() or args.ready_file.exists():
        parser.error('Use fresh stop/ready paths; existing files are not overwritten')
    services = []
    with tempfile.TemporaryDirectory(prefix='iter04-synthetic-') as temp:
        fixture_root = Path(temp)
        fs = filesystem_fixture(fixture_root)
        empty = fixture_root / 'empty-synthetic'
        empty.mkdir()
        git_name, git_directory = 'real_git', ROOT / 'docs/todos/10-self-hosting-hardening'
        if args.isolated_fixtures:
            git_name, git_directory = 'synthetic_git', fixture_root / 'docs/todos/02-synthetic-git'
            git_directory.mkdir(parents=True)
            (git_directory / '01-task.md').write_text(
                '---\nstatus: IN_PROGRESS\ntask_name: SYNTHETIC Git inventory\n'
                'delivery_mode: git\nbase_sha: synthetic-base\nhead_sha: synthetic-head\n---\n',
                encoding='utf-8')
        try:
            for name, directory, delay in (
                (git_name, git_directory, 0),
                ('synthetic_fs', fs, 0), ('synthetic_empty', empty, 0),
                ('synthetic_loading', fs, args.delay)):
                stopping = threading.Event()
                def do_get(self):
                    if urlsplit(self.path).path == '/api/board':
                        self.stopping.wait(self.delay)
                    return LiveBoardHandler.do_GET(self)
                handler = type('HarnessHandler', (LiveBoardHandler,), {
                    'iter_dir': directory, 'delay': delay, 'stopping': stopping, 'do_GET': do_get})
                server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
                thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': .1})
                thread.start()
                stop = Path(str(args.stop_file) + '.' + name)
                services.append((name, server, thread, stopping, stop, directory))
            ready = {'ready': True, 'root': str(ROOT), 'synthetic_root': str(fixture_root),
                'stop_file': str(args.stop_file), 'duration_seconds': args.duration,
                'services': {name: {'url': f'http://127.0.0.1:{server.server_port}/',
                    'port': server.server_port, 'stop_file': str(stop), 'iter_dir': str(directory),
                    'synthetic': name != 'real_git',
                    'total': generate_board_data(directory)['total']}
                    for name, server, _, _, stop, directory in services}}
            args.ready_file.write_text(json.dumps(ready, ensure_ascii=False, indent=2), encoding='utf-8')
            print(json.dumps(ready, ensure_ascii=False), flush=True)
            end = time.monotonic() + args.duration
            while time.monotonic() < end and not args.stop_file.exists():
                for _, server, thread, stopping, stop, _ in services:
                    if stop.exists() and thread.is_alive():
                        stopping.set(); server.shutdown(); thread.join(); server.server_close()
                time.sleep(.1)
        finally:
            for _, server, thread, stopping, _, _ in services:
                stopping.set()
                if thread.is_alive():
                    server.shutdown(); thread.join()
                server.server_close()
    print(json.dumps({'stopped': True, 'active_commands': []}), flush=True)


if __name__ == '__main__':
    main()
