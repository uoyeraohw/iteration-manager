import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback

HERE = Path.cwd()
ROOT = Path('C:/Users/qingyu/.codex/skills/iteration-manager')
PREVIOUS = HERE.parent
TARGET = 'C:/Users/qingyu/.codeg/skills/iteration-manager/docs/todos/10-self-hosting-hardening'
old = json.loads((PREVIOUS / 'probe-results.json').read_text(encoding='utf-8'))
commands = old['commands']
checks = []


def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def persist():
    write_json('probe-results.json', {'reused_raw_evidence': '../probe-results.json',
        'commands': commands, 'checks': checks})


def check(name, condition):
    checks.append({'name': name, 'satisfied': bool(condition)})
    persist()
    assert condition, name


def run(label, script, args):
    argv = [sys.executable, '-B', str(ROOT / 'scripts' / script), *args]
    start = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    commands.append({'label': label, 'argv': argv, 'cwd': str(HERE),
        'started_at': start, 'ended_at': datetime.now(timezone.utc).isoformat(),
        'returncode': p.returncode, 'stdout': p.stdout.decode('utf-8', errors='replace'),
        'stderr': p.stderr.decode('utf-8', errors='replace'),
        'stdout_base64': base64.b64encode(p.stdout).decode('ascii'),
        'stderr_base64': base64.b64encode(p.stderr).decode('ascii')})
    persist()
    return p


report = json.loads((PREVIOUS / 'consumption-report.json').read_text(encoding='utf-8'))
report.pop('error', None)
report['initial_probe_correction'] = {'evidence': '../probe-run.json',
    'raw_exit_code': 1, 'reason': 'Probe expected acceptance_verdict in generated frontmatter; observed initial field is review_status: PENDING. Product output was valid.',
    'unchanged_valid_evidence_reused': ['../spec.json', '../card.md', '../probe-results.json']}
report['evidence'] = {'commands': 'probe-results.json', 'spec': 'spec.json', 'card': 'card.md',
    'takeover': 'takeover.json', 'runner': 'probe-run.json', 'initial_runner': '../probe-run.json'}
report['session']['continuation_probe_pid'] = os.getpid()
report['session']['continuation_probe_parent_pid'] = os.getppid()
report['session']['continuation_cwd'] = str(HERE)
report['result'] = 'INCOMPLETE'
report['remaining_work'] = []
try:
    # Preserve the original bytes; do not rerun successful render/check commands.
    for name in ['spec.json', 'card.md']:
        (HERE / name).open('xb').write((PREVIOUS / name).read_bytes())
    spec = json.loads((HERE / 'spec.json').read_bytes())
    card = (HERE / 'card.md').read_text(encoding='utf-8')
    check('render zero; exact output preserved', commands[0]['returncode'] == 0 and
        base64.b64decode(commands[0]['stdout_base64']) == (HERE / 'card.md').read_bytes())
    check('filesystem check zero and valid true', commands[1]['returncode'] == 0 and
        json.loads(commands[1]['stdout'])['valid'] is True)
    check('complete UI filesystem spec', spec['version'] == 1 and spec['type'] == 'UI-Component' and
        spec['delivery_mode'] == 'filesystem' and set(spec['verification']) == {'interaction', 'states', 'visual', 'regression'})
    check('marker and isolated candidate retained', 'ITER10-CODEX-20261114' in card and spec['candidate_id'] in card)
    check('four UI verification categories retained', all('**' + k + '**' in card and v in card for k, v in spec['verification'].items()))
    for key, value in [('status', 'TODO'), ('review_status', 'PENDING'), ('tdd_verified', 'false'), ('typesafe_score', 'UNASSESSED')]:
        check('initial ' + key + '=' + value, re.search(r'^' + key + r':\s*"?' + value + r'\b', card, re.M) is not None)
    check('no approval/SHA/RED/GREEN fabrication',
        all(re.search(r'^' + key + r':\s*""\s*$', card, re.M) for key in ['base_sha', 'head_sha', 'review_receipt']) and
        not re.search(r'(red_verified|green_verified|tdd_verified):\s*true', card))
    write_json('invalid-spec.json', dict(spec, scope=['../escape']))
    workspace = PREVIOUS.parent
    before = sorted(str(x.relative_to(workspace)) for x in workspace.rglob('*') if x.is_file())
    bad = run('reject traversal', 'iter_templates.py', ['--render', 'invalid-spec.json'])
    after = sorted(str(x.relative_to(workspace)) for x in workspace.rglob('*') if x.is_file())
    write_json('traversal-observation.json', {'before': before, 'after': after,
        'new_files': sorted(set(after) - set(before)), 'target': str(PREVIOUS / 'escape'),
        'target_exists': (PREVIOUS / 'escape').exists(), 'external_paths_not_read': True})
    check('traversal exit two and parseable error', bad.returncode == 2 and
        isinstance(json.loads(bad.stdout if bad.stdout.strip() else bad.stderr), dict))
    check('no out-of-sandbox file created', before == after and not (PREVIOUS / 'escape').exists())
    takeover = run('readonly takeover', 'iter_sync.py', ['--takeover-report', TARGET])
    (HERE / 'takeover.json').open('xb').write(takeover.stdout)
    check('takeover exit zero', takeover.returncode == 0)
    data = json.loads(takeover.stdout)
    check('takeover read_only true', data.get('read_only') is True)
    tasks = data.get('tasks')
    check('exactly six takeover tasks', isinstance(tasks, list) and len(tasks) == 6)
    for i, task in enumerate(tasks):
        check('task %d declares DONE' % (i + 1), task.get('declared_status', task.get('status')) == 'DONE')
        check('task %d acceptance PASS' % (i + 1), task.get('acceptance_verdict') == 'PASS')
    report['result'] = 'ALL_REQUESTED_PROBE_ASSERTIONS_SATISFIED'
except BaseException as exc:
    report['error'] = {'type': type(exc).__name__, 'message': str(exc), 'traceback': traceback.format_exc()}
    report['remaining_work'] = ['Resolve the failed assertion against preserved raw output.']
    raise
finally:
    report['checks'] = checks
    report['command_returncodes'] = [{'label': c['label'], 'returncode': c['returncode']} for c in commands]
    report['ended_at'] = datetime.now(timezone.utc).isoformat()
    report['runner_observation'] = 'Controller must inspect this continuation runner receipt after probe termination.'
    write_json('consumption-report.json', report)
    print(json.dumps({'result': report['result'], 'checks': checks}, ensure_ascii=False))
