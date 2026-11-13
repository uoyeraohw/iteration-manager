import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from iter_autonomy import record_event, load_state, update_meta
from iter_contracts import parse_card


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


@pytest.fixture
def checkpoint(tmp_path, monkeypatch, request):
    root = tmp_path / 'repo'
    root.mkdir()
    monkeypatch.chdir(root)
    git(root, 'init')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    git(root, 'config', 'user.name', 'Fixture')
    card = root / 'task.md'
    card.write_text('---\nschema_version: 1\nstatus: IN_PROGRESS\nreplan_count: 2\n---\n# Task\n', encoding='utf-8')
    terminal = dict(version=1, sessions=[dict(id='native-session', status='canceled', source='native:1')],
                    commands=[dict(id='native-command', status='completed', exit_code=1, source='native:20')])
    (root / 'terminal.json').write_text(json.dumps(terminal), encoding='utf-8')
    result = record_event(card, 'closeout', 'stop', 'old', getattr(request, 'param', 'execution deadline; reviewed RED'), 'terminal.json', 'canceled')
    assert result['status'] == 'FUSED'
    git(root, 'add', '.')
    git(root, 'commit', '-m', 'frozen checkpoint')
    head = git(root, 'rev-parse', 'HEAD')
    grant = dict(version=1, grant_id='grant-1', workspace=str(root.resolve()), card='task.md', head=head,
                 checkpoint_sha=head, closeout_event_id='stop', terminal_evidence='terminal.json',
                 expires_at=(datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat())
    path = tmp_path / 'grant.json'
    path.write_text(json.dumps(grant), encoding='utf-8')
    return root, card, path, grant


def resume(card, grant, event='resume'):
    return record_event(card, 'resume-checkpoint', event, 'new', resume_grant=str(grant))


def test_resume_preserves_four_counters_at_replan_limit(checkpoint):
    root, card, path, grant = checkpoint
    result = resume(card, path)
    assert result['status'] == 'IN_PROGRESS', result
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    assert [state[k] for k in ('round', 'total', 'consilium', 'replan')] == [0, 0, 0, 2]
    assert state['writer'] == 'new' and not state['blocked_reason']
    saved = card.read_bytes()
    assert resume(card, path)['replayed']
    assert saved == card.read_bytes()
    assert resume(card, path, 'different').get('error')
    assert saved == card.read_bytes()


@pytest.mark.parametrize('change', ['head', 'workspace', 'card', 'closeout_event_id', 'expires_at', 'checkpoint_sha', 'terminal_evidence'])
def test_bad_binding_rejects_without_writing(checkpoint, change):
    root, card, path, grant = checkpoint
    grant[change] = {'head':'0'*40, 'workspace':str(root.parent), 'card':'../task.md',
                     'closeout_event_id':'old-closeout', 'expires_at':'2000-01-01T00:00:00Z',
                     'checkpoint_sha':'0'*40, 'terminal_evidence':'missing.json'}[change]
    path.write_text(json.dumps(grant), encoding='utf-8')
    saved = card.read_bytes()
    assert resume(card, path).get('error')
    assert saved == card.read_bytes()


@pytest.mark.parametrize('case', ['dirty', 'writer', 'budget', 'unknown_command', 'running_session', 'inside_grant', 'wrong_cwd'])
def test_unsafe_state_rejects_without_writing(checkpoint, case, monkeypatch):
    root, card, path, grant = checkpoint
    if case == 'dirty':
        (root/'unowned.txt').write_text('preserve', encoding='utf-8')
    elif case in ('writer', 'budget'):
        state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
        state['writer' if case == 'writer' else 'blocked_reason'] = 'active' if case == 'writer' else 'consilium budget exhausted'
        card.write_text(update_meta(card.read_text(encoding='utf-8'), {'autonomy_state':json.dumps(state)}), encoding='utf-8')
        git(root, 'add', '.'); git(root, 'commit', '-m', case)
        grant['head'] = git(root, 'rev-parse', 'HEAD')
    elif case in ('unknown_command', 'running_session'):
        terminal = json.loads((root/'terminal.json').read_text())
        terminal['commands' if case == 'unknown_command' else 'sessions'][0]['status'] = 'unknown' if case == 'unknown_command' else 'running'
        (root/'terminal.json').write_text(json.dumps(terminal), encoding='utf-8')
        git(root, 'add', '.'); git(root, 'commit', '-m', case)
        grant['head'] = git(root, 'rev-parse', 'HEAD')
    elif case == 'inside_grant':
        path = root/'grant.json'
    elif case == 'wrong_cwd':
        monkeypatch.chdir(root.parent)
    path.write_text(json.dumps(grant), encoding='utf-8')
    saved = card.read_bytes()
    assert resume(card, path).get('error')
    assert saved == card.read_bytes()


def test_three_resume_limit_and_no_reuse(checkpoint):
    root, card, path, grant = checkpoint
    for i in range(4):
        if i:
            record_event(card, 'closeout', f'stop-{i}', 'new', 'execution deadline', 'terminal.json', 'canceled')
            git(root, 'add', '.'); git(root, 'commit', '-m', f'closeout {i}')
            grant.update(grant_id=f'grant-{i+1}', head=git(root, 'rev-parse', 'HEAD'), closeout_event_id=f'stop-{i}')
            path.write_text(json.dumps(grant), encoding='utf-8')
        before = card.read_bytes()
        result = resume(card, path, f'resume-{i}')
        if i < 3:
            assert result['status'] == 'IN_PROGRESS', result
        else:
            assert result.get('error') and before == card.read_bytes()


def test_resume_cli_real_consumption(checkpoint):
    root, card, path, grant = checkpoint
    script = Path(__file__).resolve().parents[1]/'scripts/iter_sync.py'
    proc = subprocess.run([sys.executable, '-B', str(script), '--autonomy', 'resume-checkpoint', str(card),
                           '--event-id', 'cli', '--owner', 'new', '--resume-grant', str(path)], cwd=root, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert json.loads(proc.stdout)['status'] == 'IN_PROGRESS'


@pytest.mark.parametrize('mode', ['card', 'profile', 'invalid-profile', 'unknown-card'])
def test_resume_rejects_non_git_delivery_even_inside_git(checkpoint, mode):
    root, card, path, grant = checkpoint
    if mode in ('card', 'unknown-card'):
        content = update_meta(card.read_text(encoding='utf-8'),
                              {'delivery_mode': 'filesystem' if mode == 'card' else 'unknown'})
        card.write_text(content, encoding='utf-8')
    else:
        directory = root/'docs/todos/01-demo'
        directory.mkdir(parents=True)
        card.rename(directory/'01-task.md')
        card = directory/'01-task.md'
        (directory/'iteration-delivery.json').write_text(
            '{"schema_version":1,"mode":"filesystem"}' if mode == 'profile' else '{bad', encoding='utf-8')
        grant['card'] = card.relative_to(root).as_posix()
    git(root, 'add', '.'); git(root, 'commit', '-m', 'delivery mode')
    grant['head'] = git(root, 'rev-parse', 'HEAD')
    path.write_text(json.dumps(grant), encoding='utf-8')
    saved = card.read_bytes()
    result = resume(card, path)
    assert result.get('error'), result
    assert card.read_bytes() == saved


@pytest.mark.parametrize('counter,value', [('round', 5), ('total', 10), ('consilium', 2), ('replan', 3)])
def test_numeric_budget_exhaustion_cannot_be_hidden_by_deadline(checkpoint, counter, value):
    root, card, path, grant = checkpoint
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    state[counter] = value
    state['total'] = max(state['total'], state['round'])
    card.write_text(update_meta(card.read_text(encoding='utf-8'), {'autonomy_state':json.dumps(state)}), encoding='utf-8')
    git(root, 'add', '.'); git(root, 'commit', '-m', counter)
    grant['head'] = git(root, 'rev-parse', 'HEAD')
    path.write_text(json.dumps(grant), encoding='utf-8')
    saved = card.read_bytes()
    assert resume(card, path).get('error')
    assert saved == card.read_bytes()


def test_same_event_changed_grant_rejected(checkpoint):
    root, card, path, grant = checkpoint
    assert resume(card, path)['status'] == 'IN_PROGRESS'
    saved = card.read_bytes()
    grant['grant_id'] = 'changed'
    path.write_text(json.dumps(grant), encoding='utf-8')
    assert resume(card, path).get('error')
    assert saved == card.read_bytes()


@pytest.mark.parametrize('checkpoint', ['interrupted supervisor closeout after RED checkpoint; no implementation; replan2 retained; requires explicitly authorized recovery plan/budget or reviewed checkpoint-resume capability'], indirect=True)
def test_legacy_interruption_needs_bound_independent_review(checkpoint):
    root, card, path, grant = checkpoint
    before = card.read_bytes()
    assert resume(card, path).get('error')  # Do not infer time interruption from arbitrary text.
    assert card.read_bytes() == before
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    review = dict(version=1, kind='execution-deadline', verdict='APPROVED', closeout_event_id='stop',
                  blocked_reason=state['blocked_reason'], reviewer_session='independent-session', source='native:deadline-watch+independent-report')
    (root/'interruption-review.json').write_text(json.dumps(review), encoding='utf-8')
    git(root, 'add', '.'); git(root, 'commit', '-m', 'review legacy interruption')
    grant.update(head=git(root, 'rev-parse', 'HEAD'), interruption_review='interruption-review.json')
    path.write_text(json.dumps(grant), encoding='utf-8')
    result = resume(card, path)
    assert result['status'] == 'IN_PROGRESS', result
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    assert [state[k] for k in ('round','total','consilium','replan')] == [0,0,0,2]


@pytest.mark.parametrize('tamper', ['reason', 'closeout', 'verdict', 'kind', 'reviewer', 'uncommitted', 'budget'])
def test_typed_review_cannot_bypass_binding_or_budget(checkpoint, tamper):
    root, card, path, grant = checkpoint
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    review = dict(version=1, kind='execution-deadline', verdict='APPROVED', closeout_event_id='stop',
                  blocked_reason=state['blocked_reason'], reviewer_session='independent', source='native source')
    field = {'reason':'blocked_reason','closeout':'closeout_event_id','verdict':'verdict','kind':'kind','reviewer':'reviewer_session'}.get(tamper)
    if field:
        review[field] = '' if tamper == 'reviewer' else 'mismatch'
    if tamper == 'budget':
        state['blocked_reason'] = 'replan budget exhausted'
        review['blocked_reason'] = state['blocked_reason']
        card.write_text(update_meta(card.read_text(encoding='utf-8'), {'autonomy_state':json.dumps(state)}), encoding='utf-8')
    (root/'interruption-review.json').write_text(json.dumps(review), encoding='utf-8')
    if tamper == 'uncommitted':
        (root/'.gitignore').write_text('interruption-review.json\n', encoding='utf-8')
    git(root, 'add', '.'); git(root, 'commit', '-m', tamper)
    grant.update(head=git(root, 'rev-parse', 'HEAD'), interruption_review='interruption-review.json')
    path.write_text(json.dumps(grant), encoding='utf-8')
    before = card.read_bytes()
    assert resume(card, path).get('error')
    assert card.read_bytes() == before
