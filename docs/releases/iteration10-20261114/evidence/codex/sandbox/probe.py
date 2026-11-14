import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
from datetime import datetime, timezone

ROOT = Path('C:/Users/qingyu/.codex/skills/iteration-manager')
HERE = Path.cwd()
MARKER = 'ITER10-CODEX-20261114'
CANDIDATE = 'iter10-codex-installed-consumption-isolated-sample'
TARGET = 'C:/Users/qingyu/.codeg/skills/iteration-manager/docs/todos/10-self-hosting-hardening'
commands = []
checks = []


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def persist_results():
    # This file is owned exclusively by this probe and updated after each command.
    (HERE / 'probe-results.json').write_text(
        json.dumps({'commands': commands, 'checks': checks}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')


def run(label, script, args):
    argv = [sys.executable, '-B', str(ROOT / 'scripts' / script), *args]
    started = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    record = {'label': label, 'argv': argv, 'cwd': str(HERE),
              'started_at': started, 'ended_at': datetime.now(timezone.utc).isoformat(),
              'returncode': p.returncode,
              'stdout': p.stdout.decode('utf-8', errors='replace'),
              'stderr': p.stderr.decode('utf-8', errors='replace'),
              'stdout_base64': base64.b64encode(p.stdout).decode('ascii'),
              'stderr_base64': base64.b64encode(p.stderr).decode('ascii')}
    commands.append(record)
    persist_results()
    return p


def check(name, condition):
    checks.append({'name': name, 'satisfied': bool(condition)})
    persist_results()
    assert condition, name


report = {
    'version': 1,
    'marker': MARKER,
    'installed_root': str(ROOT),
    'documents_read_by_controller': [str(ROOT / 'SKILL.md'),
        str(ROOT / 'references/template_generation.md'),
        str(ROOT / 'references/execution_readiness.md')],
    'session': {'kind': 'independent new Codex installation-consumption session',
        'agent': '/root', 'codex_thread_id': os.environ.get('CODEX_THREAD_ID'),
        'codex_session_id': os.environ.get('CODEX_SESSION_ID'),
        'probe_pid': os.getpid(), 'probe_parent_pid': os.getppid(), 'cwd': str(HERE)},
    'evidence': {'commands': 'probe-results.json', 'spec': 'spec.json', 'card': 'card.md',
        'takeover': 'takeover.json', 'runner': 'probe-run.json'},
    'limitations': [
        'Explicit loading of installed documents/scripts does not establish native automatic discovery.',
        'No real filesystem business delivery lifecycle is tested.',
        'Takeover observes existing declarations and acceptance audit; it does not implement or re-approve the six cards.',
        'No budget registration, Git writes, product edits, network, installation, credentials, assistant configuration, deployment, cleanup, or delegation.'],
    'started_at': datetime.now(timezone.utc).isoformat(),
    'result': 'INCOMPLETE', 'remaining_work': []}

try:
    check('exclusive sandbox cwd', HERE.name == 'sandbox' and HERE.parent.name == 'codex-consumption')
    spec = {
        'version': 1, 'task_id': '01', 'iteration': '10-codex-install-consumption',
        'task_name': MARKER + ' isolated UI card', 'type': 'UI-Component',
        'delivery_mode': 'filesystem', 'candidate_id': CANDIDATE,
        'objective': MARKER + ': render an isolated unapproved UI consumption sample',
        'consumes': 'Local isolated UI fixture only',
        'produces': 'An unapproved filesystem UI task card',
        'scope': ['ui/sample.py', 'tests/'],
        'stages': ['Describe an isolated UI sample without implementation'],
        'acceptance': ['All four UI verification categories are present; no approval facts are generated'],
        'verification': {
            'interaction': 'Observe sample button interaction in an isolated UI fixture; not executed by generation',
            'states': 'Observe loading, empty, success and error states; not executed by generation',
            'visual': 'Inspect sample layout at its actual viewport; not executed by generation',
            'regression': 'Run affected sample UI regression checks after authorized implementation; not executed here'}}
    save('spec.json', spec)
    p = run('render', 'iter_templates.py', ['--render', 'spec.json'])
    (HERE / 'card.md').open('xb').write(p.stdout)
    check('render exits zero', p.returncode == 0)
    pcheck = run('check', 'iter_templates.py', ['--check', 'card.md', '--delivery-mode', 'filesystem'])
    check('check exits zero and valid true', pcheck.returncode == 0 and json.loads(pcheck.stdout)['valid'] is True)
    card = p.stdout.decode('utf-8')
    check('marker and candidate retained', MARKER in card and CANDIDATE in card)
    check('four UI categories retained', all(v in card for v in spec['verification'].values()))
    for key, value in [('status', 'TODO'), ('acceptance_verdict', 'PENDING'), ('tdd_verified', 'false')]:
        check('initial ' + key + '=' + value,
              re.search(r'[\"\x27]?' + key + r'[\"\x27]?\s*:\s*[\"\x27]?' + value + r'\b', card) is not None)
    check('no fabricated RED/GREEN verification', not re.search(r'(red_verified|green_verified|tdd_verified)[\"\x27]?\s*:\s*true', card))
    bad = dict(spec, scope=['../escape'])
    save('invalid-spec.json', bad)
    # No scope path is passed as an output destination. Observe the complete authorized
    # workspace file inventory before/after to detect any unexpected file creation.
    workspace = HERE.parent
    before = sorted(str(x.relative_to(workspace)) for x in workspace.rglob('*') if x.is_file())
    badp = run('reject traversal', 'iter_templates.py', ['--render', 'invalid-spec.json'])
    after = sorted(str(x.relative_to(workspace)) for x in workspace.rglob('*') if x.is_file())
    save('traversal-observation.json', {'scope': bad['scope'], 'before': before, 'after': after,
        'new_files': sorted(set(after) - set(before)),
        'escape_in_authorized_workspace': (workspace / 'escape').exists(),
        'external_paths_not_read': True})
    check('traversal rejected with exit two', badp.returncode == 2)
    error = json.loads(badp.stdout if badp.stdout.strip() else badp.stderr)
    check('traversal error parseable', isinstance(error, dict) and bool(error))
    check('no traversal file produced', before == after and not (workspace / 'escape').exists())
    takeover = run('readonly takeover', 'iter_sync.py', ['--takeover-report', TARGET])
    (HERE / 'takeover.json').open('xb').write(takeover.stdout)
    check('takeover exits zero', takeover.returncode == 0)
    data = json.loads(takeover.stdout)
    check('takeover read_only true', data.get('read_only') is True)
    tasks = data.get('tasks')
    check('takeover has exactly six tasks', isinstance(tasks, list) and len(tasks) == 6)
    for i, task in enumerate(tasks):
        check('task %d declares DONE' % (i + 1),
              task.get('declared_status', task.get('status')) == 'DONE')
        check('task %d acceptance PASS' % (i + 1), task.get('acceptance_verdict') == 'PASS')
    report['result'] = 'ALL_REQUESTED_PROBE_ASSERTIONS_SATISFIED'
except BaseException as exc:
    report['error'] = {'type': type(exc).__name__, 'message': str(exc), 'traceback': traceback.format_exc()}
    report['remaining_work'] = ['Resolve the failed probe assertion using preserved raw evidence.']
    raise
finally:
    report['checks'] = checks
    report['command_returncodes'] = [{'label': c['label'], 'returncode': c['returncode']} for c in commands]
    report['ended_at'] = datetime.now(timezone.utc).isoformat()
    report['runner_observation'] = 'Runner receipt must be inspected by the controller after this probe exits.'
    save('consumption-report.json', report)
    print(json.dumps({'result': report['result'], 'report': 'consumption-report.json',
        'checks': checks}, ensure_ascii=False))
