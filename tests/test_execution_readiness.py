import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import iter_sync as engine
from iter_autonomy import record_event, update_meta, load_state
from iter_contracts import parse_card


def fixture(root):
    directory = root / 'docs/todos/01-demo'
    directory.mkdir(parents=True)
    (directory / 'iteration-delivery.json').write_text('{"schema_version":1,"mode":"filesystem"}', encoding='utf-8')
    (directory / 'README.md').write_text('<!-- iter:goal -->\nGoal\n<!-- /iter:goal -->', encoding='utf-8')
    card = directory / '01-task.md'
    card.write_text('---\nschema_version: 1\ntask_id: "01"\ntype: Strict-TDD\nstatus: IN_PROGRESS\ndelivery_mode: filesystem\ncandidate_id: candidate-1\n---\n'
                    '<!-- iter:scope -->\n| File | Change | Why |\n| --- | --- | --- |\n| `src.py` | MODIFIED | behavior |\n<!-- /iter:scope -->\n'
                    '<!-- iter:acceptance -->\n- [ ] behavior\n<!-- /iter:acceptance -->\n<!-- iter:ledger -->\n<!-- /iter:ledger -->', encoding='utf-8')
    (root / 'src.py').write_text('pass\n', encoding='utf-8')
    (root / 'observation.txt').write_text('Raw authority, executor/access and verification observations', encoding='utf-8')
    context = dict(version=1, tasks={'01': dict(
        phase='implementation', candidate='candidate-1', inputs=['src.py'], capabilities=['executor/native-ui'],
        dependencies=[], tool_entry=str(Path(engine.__file__).resolve()), checkpoint='core GREEN', remaining_work=['independent review'],
        observations={name: dict(status='READY', evidence='observation.txt', summary='observed '+name)
                      for name in ('authority', 'execution', 'verification')})})
    ctx = root / 'context.json'; ctx.write_text(json.dumps(context), encoding='utf-8')
    return card, ctx, context


def cli(root, *args):
    return subprocess.run([sys.executable, '-B', engine.__file__, *map(str, args)], cwd=root, capture_output=True, encoding='utf-8')


def inventory(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}


def test_preflight_ready_is_read_only_not_acceptance(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = json.loads(proc.stdout)
    assert report['readiness'] == 'READY' and report['read_only'] is True
    assert report['tasks'][0]['acceptance_verdict'] == 'UNKNOWN'
    assert before == inventory(tmp_path)


def test_continue_inventory_combines_readiness_with_true_acceptance_without_writing(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', '--context', ctx.name)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = json.loads(proc.stdout)
    assert data['read_only'] and data['mode'] == 'continue' and data['readiness'] == 'READY'
    task = data['tasks'][0]
    assert (task['task_id'], task['readiness'], task['phase']) == ('01', 'READY', 'implementation')
    assert task['status'] == 'IN_PROGRESS' and task['acceptance_verdict'] == 'UNKNOWN'
    assert task['execution']['checkpoint'] is None and task['execution']['no_progress_streak'] == 0
    assert before == inventory(tmp_path)


def test_takeover_exposes_existing_missing_evidence_without_changing_continue(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    before = inventory(tmp_path)
    base = ['--inventory', card.parent, '--context', ctx.name]
    cont = cli(tmp_path, *base, '--mode', 'continue')
    takeover = cli(tmp_path, *base, '--mode', 'takeover')
    old = cli(tmp_path, '--takeover-report', card.parent)
    assert cont.returncode == takeover.returncode == old.returncode == 0
    c, t, previous = json.loads(cont.stdout), json.loads(takeover.stdout), json.loads(old.stdout)
    assert 'missing' not in c['tasks'][0] and 'next' not in c
    assert t['tasks'][0]['missing'] == previous['tasks'][0]['missing'] == ['review_receipt']
    assert t['tasks'][0]['acceptance_verdict'] == previous['tasks'][0]['acceptance_verdict'] == 'UNKNOWN'
    assert 'authorization' in t['next']
    assert before == inventory(tmp_path)


def test_inventory_details_reuses_same_handoff_and_compact_keeps_sources(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    before = inventory(tmp_path)
    args = ['--inventory', card.parent, '--mode', 'continue', '--context', ctx.name]
    compact = json.loads(cli(tmp_path, *args).stdout)['tasks'][0]
    detail = json.loads(cli(tmp_path, *args, '--details').stdout)['tasks'][0]
    original = engine.render_task_envelope(card, tmp_path)['TASK_HANDOFF']
    assert 'details' not in compact
    assert detail['details']['handoff'] == original
    assert detail['details']['preflight']['readiness'] == compact['readiness']
    assert compact['candidate'] == compact['candidate_id'] == 'candidate-1'
    assert compact['receipt'] == original['evidence']['receipt']
    assert before == inventory(tmp_path)


def test_inventory_uses_actual_done_audit_not_preflight_unknown(tmp_path):
    from test_filesystem_delivery_controller import fixture as done_fixture
    card, _, _ = done_fixture(tmp_path)
    before = inventory(tmp_path)
    assert engine.audit_task_file(card)['verdict'] == 'PASS'
    proc = cli(tmp_path, '--inventory', card.parent, '--mode', 'takeover')
    assert proc.returncode == 3, proc.stdout + proc.stderr  # DONE is not dispatchable.
    task = json.loads(proc.stdout)['tasks'][0]
    assert task['status'] == 'DONE' and task['readiness'] == 'BLOCKED'
    assert task['acceptance_verdict'] == 'PASS' and task['receipt'] == 'evidence/review.json'
    assert task['missing'] == []
    assert before == inventory(tmp_path)


def test_inventory_legacy_done_without_receipt_is_unknown(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    card.write_text(card.read_text(encoding='utf-8').replace('status: IN_PROGRESS','status: DONE'),encoding='utf-8')
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--inventory', card.parent, '--mode', 'takeover', '--context', ctx.name)
    assert proc.returncode == 3
    task = json.loads(proc.stdout)['tasks'][0]
    assert task['acceptance_verdict'] == 'UNKNOWN' and 'review_receipt' in task['missing']
    assert before == inventory(tmp_path)


def test_inventory_mixed_phases_keeps_independent_ready_task(tmp_path):
    card, ctx, data = fixture(tmp_path)
    second = card.with_name('02-task.md')
    second.write_text(card.read_text(encoding='utf-8').replace('task_id: "01"','task_id: "02"'),encoding='utf-8')
    data['tasks']['01']['phase'] = 'implementation'
    data['tasks']['02'] = json.loads(json.dumps(data['tasks']['01']))
    data['tasks']['02'].update(phase='review', candidate='wrong')
    save(ctx, data)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', '--context', ctx.name, '--phase-from-context')
    assert proc.returncode == 3
    first, second = json.loads(proc.stdout)['tasks']
    assert (first['phase'], first['readiness']) == ('implementation', 'READY')
    assert (second['phase'], second['readiness']) == ('review', 'BLOCKED')
    assert any('candidate mismatch' in s for s in second['findings'])
    assert before == inventory(tmp_path)


def test_inventory_missing_or_bad_card_does_not_erase_other_cards(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    (card.parent/'02-bad.md').write_text('---\nstatus: TODO\nautonomy_state: "{bad"\n---\n',encoding='utf-8')
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--inventory', card.parent, '--mode', 'takeover', '--context', ctx.name)
    assert proc.returncode == 3
    first, bad = json.loads(proc.stdout)['tasks']
    assert first['readiness'] == 'READY' and bad['readiness'] == 'BLOCKED' and bad['findings']
    assert bad['acceptance_verdict'] == 'UNKNOWN'
    assert before == inventory(tmp_path)


@pytest.mark.parametrize('name', ['02-outside.md', 'outside.md'])
def test_inventory_does_not_read_outside_symlink_or_hide_safe_card(tmp_path, name):
    project = tmp_path/'project'; card, ctx, _ = fixture(project)
    outside = tmp_path/'secret.md'; outside.write_text('---\ntask_id: PRIVATE-MARKER\nstatus: TODO\n---\n',encoding='utf-8')
    (card.parent/name).symlink_to(outside)
    before = inventory(project)
    proc = cli(project, '--inventory', card.parent, '--mode', 'continue', '--context', ctx.name)
    assert proc.returncode == 3
    result = json.loads(proc.stdout)
    assert len(result['tasks']) == 2 and any(t['readiness']=='READY' for t in result['tasks'])
    assert any('leaves project root' in ' '.join(t['findings']) for t in result['tasks'])
    assert 'PRIVATE-MARKER' not in proc.stdout
    assert before == inventory(project)


def test_inventory_audits_each_card_at_most_once_even_for_dependency(tmp_path, monkeypatch):
    from iter_inventory import inventory as combined
    card, ctx, data = fixture(tmp_path)
    second = card.with_name('02-task.md')
    second.write_text(card.read_text(encoding='utf-8').replace('task_id: "01"','task_id: "02"'),encoding='utf-8')
    data['tasks']['02'] = json.loads(json.dumps(data['tasks']['01']))
    data['tasks']['02']['dependencies'] = [card.relative_to(tmp_path).as_posix()]
    save(ctx, data)
    calls = []; original = engine.audit_task_file
    def observed(path):
        calls.append(path.name)
        return original(path)
    monkeypatch.setattr(engine, 'audit_task_file', observed)
    result = combined(card.parent, tmp_path, 'continue', ctx.name)
    assert result['readiness'] == 'BLOCKED' and sorted(calls) == ['01-task.md','02-task.md']


def test_inventory_preserves_no_progress_and_legacy_preflight_result(tmp_path):
    card, ctx, data = fixture(tmp_path)
    data['tasks']['01']['phase'] = 'review'; save(ctx, data)
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    conditions = dict(inputs=['src.py'], capabilities=['executor/native-ui'], scope=['src.py'])
    for i in range(2):
        state['events'][str(i)] = dict(input=dict(action='attempt', attempt=dict(
            phase='implementation', conditions=conditions, progress=[], checkpoint='planned', remaining_work=[],
            session_seconds=None, command_seconds=None)))
    card.write_text(update_meta(card.read_text(encoding='utf-8'), {'autonomy_state':json.dumps(state)}),encoding='utf-8')
    before = inventory(tmp_path)
    old = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--phase-from-context')
    new = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', '--context', ctx.name, '--phase-from-context')
    assert old.returncode == new.returncode == 3
    original = json.loads(old.stdout)['tasks'][0]; combined = json.loads(new.stdout)['tasks'][0]
    assert combined['findings'] == original['findings']
    assert combined['execution']['no_progress_streak'] == 2 and combined['phase'] == 'review'
    assert before == inventory(tmp_path)


def test_inventory_requires_explicit_mode_and_conflicting_phase_options_are_rejected(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    before = inventory(tmp_path)
    assert cli(tmp_path, '--inventory', card.parent, '--context', ctx.name).returncode == 2
    assert cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', '--context', ctx.name,
               '--phase', 'review', '--phase-from-context').returncode == 2
    missing = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue')
    assert missing.returncode == 2 and json.loads(missing.stdout)['readiness'] == 'NEEDS_INPUT'
    assert before == inventory(tmp_path)


def test_inventory_git_project_uses_real_head_and_original_legacy_entry(tmp_path):
    card, ctx, data = fixture(tmp_path)
    (card.parent/'iteration-delivery.json').unlink()
    card.write_text(card.read_text(encoding='utf-8').replace('delivery_mode: filesystem\n','').replace('candidate_id: candidate-1\n',''),encoding='utf-8')
    def git(*args):
        p = subprocess.run(['git',*args],cwd=tmp_path,capture_output=True,encoding='utf-8')
        assert p.returncode == 0, p.stderr
        return p.stdout.strip()
    git('init'); git('add','.'); git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','fixture')
    head = git('rev-parse','HEAD'); data['tasks']['01']['candidate'] = head; save(ctx, data)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', '--context', ctx.name)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    task = json.loads(proc.stdout)['tasks'][0]
    assert task['delivery_mode'] == 'git' and task['candidate'] == head and task['commit_sha'] == ''
    assert task['readiness'] == 'READY' and task['acceptance_verdict'] == 'UNKNOWN'
    assert cli(tmp_path, '--preflight', card.parent, '--context', ctx.name).returncode == 0
    assert before == inventory(tmp_path)


def test_mismatch_diagnostics_separate_phase_from_candidate(tmp_path):
    card, ctx, data = fixture(tmp_path)
    data['tasks']['01'].update(phase='evidence-inspection', candidate='wrong-candidate')
    save(ctx, data)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name)
    assert proc.returncode == 3, proc.stdout + proc.stderr
    result = json.loads(proc.stdout)['tasks'][0]
    assert any('phase' in f.lower() and 'implementation' in f and 'evidence-inspection' in f for f in result['findings'])
    assert any('candidate' in f.lower() and 'wrong-candidate' in f and 'candidate-1' in f for f in result['findings'])
    assert result['acceptance_verdict'] == 'UNKNOWN'
    assert before == inventory(tmp_path)


def test_opt_in_preflight_reads_each_task_phase_without_changing_legacy_default(tmp_path):
    card, ctx, data = fixture(tmp_path)
    second = card.with_name('02-task.md')
    second.write_text(card.read_text(encoding='utf-8').replace('task_id: "01"', 'task_id: "02"').replace('Strict-TDD', 'Spike-Discovery'), encoding='utf-8')
    data['tasks']['01']['phase'] = 'evidence-inspection'
    data['tasks']['02'] = json.loads(json.dumps(data['tasks']['01']))
    data['tasks']['02']['phase'] = 'review'
    save(ctx, data)
    before = inventory(tmp_path)
    legacy = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name)
    assert legacy.returncode == 3  # Existing default is implementation, not inferred.
    assert all(t['phase'] == 'implementation' for t in json.loads(legacy.stdout)['tasks'])
    proc = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--phase-from-context')
    assert proc.returncode == 0, proc.stdout + proc.stderr
    result = json.loads(proc.stdout)
    assert result['readiness'] == 'READY'
    assert [(t['task_id'], t['phase']) for t in result['tasks']] == [('01','evidence-inspection'),('02','review')]
    assert all(t['acceptance_verdict'] == 'UNKNOWN' for t in result['tasks'])
    assert before == inventory(tmp_path)


@pytest.mark.parametrize('bad_phase', [None, '', ' padded ', 23])
def test_opt_in_rejects_missing_or_invalid_task_phase_without_fallback(tmp_path, bad_phase):
    card, ctx, data = fixture(tmp_path)
    data['tasks']['01']['phase'] = bad_phase
    save(ctx, data)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--phase-from-context')
    assert proc.returncode == 3, proc.stdout + proc.stderr
    task = json.loads(proc.stdout)['tasks'][0]
    assert task['readiness'] == 'BLOCKED' and task['phase'] is None
    assert 'context phase' in ' '.join(task['findings'])
    assert before == inventory(tmp_path)


def test_opt_in_requires_context_and_does_not_apply_to_dispatch(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    before = inventory(tmp_path)
    missing = cli(tmp_path, '--preflight', card.parent, '--phase-from-context')
    assert missing.returncode == 2 and json.loads(missing.stdout)['readiness'] == 'NEEDS_INPUT'
    both = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name,
               '--phase', 'implementation', '--phase-from-context')
    assert both.returncode == 2 and 'not allowed with argument' in both.stderr
    dispatch = cli(tmp_path, '--dispatch-check', card, '--context', ctx.name, '--phase-from-context')
    assert dispatch.returncode == 2 and 'only to --preflight' in dispatch.stderr
    assert before == inventory(tmp_path)


def test_phase_inference_does_not_expand_legacy_python_dispatch_or_preflight_api(tmp_path):
    from iter_preflight import dispatch_check, preflight
    card, ctx, _ = fixture(tmp_path)
    with pytest.raises(TypeError):
        dispatch_check(card, tmp_path, ctx.name, owner='lead', phase_from_context=True)
    with pytest.raises(TypeError):
        preflight(card.parent, tmp_path, ctx.name, phase='review', phase_from_context=True)


def test_opt_in_preserves_independent_task_and_candidate_blocking(tmp_path):
    card, ctx, data = fixture(tmp_path)
    second = card.with_name('02-task.md')
    second.write_text(card.read_text(encoding='utf-8').replace('task_id: "01"', 'task_id: "02"'), encoding='utf-8')
    data['tasks']['01']['phase'] = 'evidence-inspection'
    data['tasks']['02'] = json.loads(json.dumps(data['tasks']['01']))
    data['tasks']['02'].update(phase='review', candidate='not-current')
    save(ctx, data)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--phase-from-context')
    assert proc.returncode == 3, proc.stdout + proc.stderr
    first, second = json.loads(proc.stdout)['tasks']
    assert (first['readiness'], first['phase']) == ('READY', 'evidence-inspection')
    assert (second['readiness'], second['phase']) == ('BLOCKED', 'review')
    assert any('candidate mismatch' in f and 'not-current' in f and 'candidate-1' in f for f in second['findings'])
    assert not any('phase mismatch' in f for f in second['findings'])
    assert before == inventory(tmp_path)


def test_opt_in_never_bypasses_existing_no_progress_guard(tmp_path):
    card, ctx, data = fixture(tmp_path)
    data['tasks']['01']['phase'] = 'review'; save(ctx, data)
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    conditions = dict(inputs=['src.py'], capabilities=['executor/native-ui'], scope=['src.py'])
    for i in range(2):
        state['events'][str(i)] = dict(input=dict(action='attempt', attempt=dict(
            phase='implementation', conditions=conditions, progress=[], checkpoint='planned', remaining_work=[],
            session_seconds=None, command_seconds=None)))
    card.write_text(update_meta(card.read_text(encoding='utf-8'), {'autonomy_state':json.dumps(state)}), encoding='utf-8')
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--phase-from-context')
    assert proc.returncode == 3, proc.stdout + proc.stderr
    task = json.loads(proc.stdout)['tasks'][0]
    assert task['phase'] == 'review' and task['execution']['no_progress_streak'] == 2
    assert any('identical redispatch prohibited' in f for f in task['findings'])
    assert before == inventory(tmp_path)


def test_two_empty_attempts_block_identical_third_dispatch(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    state = load_state(parse_card(card.read_text(encoding='utf-8'))[0])
    conditions = dict(inputs=['src.py'], capabilities=['executor/native-ui'], scope=['src.py'])
    for i in range(2):
        state['events'][str(i)] = dict(input=dict(action='attempt', attempt=dict(
            phase='implementation', conditions=conditions, progress=[], checkpoint='planned GREEN',
            remaining_work=['fix'], session_seconds=None, command_seconds=None)), at='2026-11-12T00:00:00+00:00')
    card.write_text(update_meta(card.read_text(encoding='utf-8'), {'autonomy_state':json.dumps(state)}), encoding='utf-8')
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--dispatch-check', card, '--phase', 'implementation', '--context', ctx.name)
    assert proc.returncode == 3, proc.stdout + proc.stderr
    report = json.loads(proc.stdout)
    assert report['readiness'] == 'BLOCKED' and report['execution']['no_progress_streak'] == 2
    assert any('progress' in item for item in report['findings'])
    assert before == inventory(tmp_path)


def report(root, name='attempt.json', progress=None):
    data = dict(version=1, phase='implementation', candidate='candidate-1', inputs=['src.py'],
                capabilities=['executor/native-ui'], checkpoint='core GREEN', remaining_work=['review'],
                executor_id='native-session-1', terminal_evidence='observation.txt', progress=progress or [],
                commands=[], started_at='2026-11-12T00:00:00+00:00', ended_at='2026-11-12T00:00:02+00:00')
    path = root/name; path.write_text(json.dumps(data), encoding='utf-8')
    return path, data


def test_attempt_event_is_idempotent_and_does_not_consume_repairs(tmp_path, monkeypatch):
    card, _, _ = fixture(tmp_path)
    monkeypatch.chdir(tmp_path)
    record_event(card, 'claim', 'claim', 'lead')
    path, _ = report(tmp_path)
    result = record_event(card, 'attempt', 'attempt-1', 'lead', evidence=path.name, executor_state='completed')
    assert not result.get('error'), result
    assert result['fix_total'] == result['current_rounds'] == 0
    before = card.read_bytes()
    assert record_event(card, 'attempt', 'attempt-1', 'lead', evidence=path.name, executor_state='completed')['replayed']
    assert card.read_bytes() == before
    handoff = engine.render_task_envelope(card, tmp_path)['TASK_HANDOFF']
    assert handoff['delivery_mode'] == 'filesystem' and handoff['candidate_id'] == 'candidate-1'
    assert handoff['execution']['attempt_count'] == 1
    assert handoff['execution']['no_progress_streak'] == 1
    assert handoff['execution']['remaining_work'] == ['review']
    assert handoff['execution']['last_attempt']['session_seconds'] == 2


def save(path, value):
    path.write_text(json.dumps(value), encoding='utf-8')


def attempt_cli(root, card, eid, source='attempt.json', owner='lead', terminal='completed'):
    return cli(root, '--autonomy', 'attempt', card, '--event-id', eid, '--owner', owner,
               '--executor-state', terminal, '--evidence', source)


@pytest.mark.parametrize('mutation,expected', [
    ('missing', 2), ('candidate', 3), ('entry', 3), ('ui', 2), ('outside', 3), ('empty', 3),
    ('dependency', 3), ('unknown', 3), ('extra', 3), ('unknown-type', 3), ('schema', 3),
])
def test_readiness_rejects_missing_or_invalid_facts_without_writing(tmp_path, mutation, expected):
    card, ctx, data = fixture(tmp_path)
    task = data['tasks']['01']
    args = ['--context', ctx.name]
    if mutation == 'missing': args = []
    if mutation == 'candidate': task['candidate'] = 'not-current'
    if mutation == 'entry': task['tool_entry'] = str(tmp_path/'nonexistent.py')
    if mutation == 'ui': card.write_text(card.read_text(encoding='utf-8').replace('Strict-TDD','UI-Component'), encoding='utf-8')
    if mutation == 'outside': task['observations']['execution']['evidence'] = '../outside'
    if mutation == 'empty': (tmp_path/'observation.txt').write_text('', encoding='utf-8')
    if mutation == 'dependency': task['dependencies'] = [card.relative_to(tmp_path).as_posix()]
    if mutation == 'unknown': card.write_text(card.read_text(encoding='utf-8').replace('IN_PROGRESS','invalid'), encoding='utf-8')
    if mutation == 'unknown-type': card.write_text(card.read_text(encoding='utf-8').replace('Strict-TDD','not-a-type'), encoding='utf-8')
    if mutation == 'schema': card.write_text(card.read_text(encoding='utf-8').replace('schema_version: 1','schema_version: 2'), encoding='utf-8')
    if mutation == 'extra': task['invented'] = True
    save(ctx, data)
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--dispatch-check', card, *args)
    assert proc.returncode == expected, proc.stdout + proc.stderr
    assert json.loads(proc.stdout)['acceptance_verdict'] == 'UNKNOWN'
    assert inventory(tmp_path) == before


def test_empty_preflight_is_not_ready(tmp_path):
    assert json.loads(cli(tmp_path, '--preflight', tmp_path).stdout)['readiness'] == 'NEEDS_INPUT'


def test_dispatch_requires_claimed_owner_but_preflight_inventory_does_not(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    before = inventory(tmp_path)
    assert cli(tmp_path,'--preflight',card.parent,'--context',ctx.name).returncode == 0
    assert cli(tmp_path,'--dispatch-check',card,'--context',ctx.name).returncode == 2
    assert cli(tmp_path,'--dispatch-check',card,'--context',ctx.name,'--owner','lead').returncode == 2
    assert inventory(tmp_path) == before
    assert cli(tmp_path,'--autonomy','claim',card,'--event-id','claim','--owner','lead').returncode == 0
    assert cli(tmp_path,'--dispatch-check',card,'--context',ctx.name).returncode == 2
    assert cli(tmp_path,'--dispatch-check',card,'--context',ctx.name,'--owner','other').returncode == 3
    assert cli(tmp_path,'--dispatch-check',card,'--context',ctx.name,'--owner','lead').returncode == 0


def test_attempt_replay_keeps_original_snapshot_after_candidate_moves(tmp_path, monkeypatch):
    card, _, _ = fixture(tmp_path); monkeypatch.chdir(tmp_path)
    record_event(card,'claim','claim','lead')
    path, _ = report(tmp_path)
    assert not record_event(card,'attempt','attempt','lead',evidence=path.name,executor_state='completed').get('error')
    card.write_text(card.read_text(encoding='utf-8').replace('candidate_id: candidate-1','candidate_id: candidate-2'),encoding='utf-8')
    before = card.read_bytes()
    result = record_event(card,'attempt','attempt','lead',evidence=path.name,executor_state='completed')
    assert result.get('replayed'), result
    assert card.read_bytes() == before


def test_real_cli_streak_conditions_and_repeated_evidence(tmp_path):
    card, ctx, data = fixture(tmp_path)
    assert cli(tmp_path, '--autonomy', 'claim', card, '--event-id', 'claim', '--owner', 'lead').returncode == 0
    path, report_data = report(tmp_path, progress=[dict(kind='red', evidence='observation.txt', summary='assertion failed')])
    for i in range(3):
        proc = attempt_cli(tmp_path, card, str(i))
        assert proc.returncode == 0, proc.stdout + proc.stderr
    args = ['--dispatch-check', card, '--context', ctx.name, '--owner', 'lead']
    assert cli(tmp_path, *args).returncode == 3  # same evidence counted only once
    task = data['tasks']['01']
    task['phase'] = 'review'; task['candidate'] = 'candidate-2'
    card.write_text(card.read_text(encoding='utf-8').replace('candidate-1','candidate-2'), encoding='utf-8')
    save(ctx, data)
    assert cli(tmp_path, *args, '--phase', 'review').returncode == 3  # tags do not reset history
    task['capabilities'].append('executor/new-capability')
    save(ctx, data)
    assert cli(tmp_path, *args, '--phase', 'review').returncode == 2
    task['change_evidence'] = 'observation.txt'; save(ctx, data)
    assert cli(tmp_path, *args, '--phase', 'review').returncode == 0
    # A real new artifact clears the streak, even after a new process and phase.
    (tmp_path/'green.txt').write_text('raw GREEN output', encoding='utf-8')
    report_data.update(candidate='candidate-2', progress=[dict(kind='green', evidence='green.txt', summary='GREEN')])
    save(path, report_data)
    assert attempt_cli(tmp_path, card, 'new-progress').returncode == 0
    handoff = json.loads(cli(tmp_path, '--render-envelope', card, tmp_path).stdout)['TASK_HANDOFF']
    assert handoff['execution']['no_progress_streak'] == 0
    assert handoff['execution']['checkpoint']['candidate'] == 'candidate-2'
    assert handoff['acceptance_verdict'] == 'UNKNOWN'


@pytest.mark.parametrize('problem', ['running','unknown','foreign','unclaimed','outside','empty','kind','candidate','timestamp','command'])
def test_invalid_attempt_does_not_mutate_card(tmp_path, monkeypatch, problem):
    card, _, _ = fixture(tmp_path)
    monkeypatch.chdir(tmp_path)
    if problem != 'unclaimed': record_event(card, 'claim', 'claim', 'lead')
    path, data = report(tmp_path)
    owner, terminal = 'lead', 'completed'
    if problem in ('running','unknown'): terminal = problem
    if problem == 'foreign': owner = 'someone-else'
    if problem == 'outside': data['terminal_evidence'] = '../outside.json'
    if problem == 'empty': (tmp_path/'observation.txt').write_text('', encoding='utf-8')
    if problem == 'kind': data['progress'] = [dict(kind='read-more', evidence='observation.txt', summary='read')]
    if problem == 'candidate': data['candidate'] = 'wrong'
    if problem == 'timestamp': data['ended_at'] = '2026-11-11T00:00:00+00:00'
    if problem == 'command':
        save(tmp_path/'command.json', dict(status='RUNNING',tree_terminal=False,raw_exit_code=None))
        data['commands'] = ['command.json']
    save(path, data)
    before = card.read_bytes()
    result = record_event(card, 'attempt', 'attempt', owner, evidence=path.name, executor_state=terminal)
    assert result.get('error'), result
    assert card.read_bytes() == before
    assert not card.with_name(card.name+'.iter.lock').exists()


def test_attempt_preserves_budget_block_and_conflicting_replay_rejected(tmp_path, monkeypatch):
    card, _, _ = fixture(tmp_path); monkeypatch.chdir(tmp_path)
    record_event(card, 'claim', 'claim', 'lead')
    for i in range(5): record_event(card, 'fix', f'fix-{i}', 'lead')
    path, data = report(tmp_path)
    result = record_event(card, 'attempt', 'a', 'lead', evidence=path.name, executor_state='failed')
    assert not result.get('error') and result['is_fused'] and result['fix_total'] == result['current_rounds'] == 5
    before = card.read_bytes()
    data['remaining_work'] = ['different']; save(path, data)
    assert record_event(card, 'attempt', 'a', 'lead', evidence=path.name, executor_state='failed').get('error')
    assert card.read_bytes() == before


def test_attempt_measured_time_unions_overlap_and_keeps_unknown(tmp_path, monkeypatch):
    card, _, _ = fixture(tmp_path); monkeypatch.chdir(tmp_path)
    record_event(card, 'claim', 'claim', 'lead')
    path, data = report(tmp_path)
    data['ended_at'] = '2026-11-12T00:00:10+00:00'
    for i, (start,end) in enumerate([(1,5),(3,7)]):
        save(tmp_path/f'command-{i}.json', dict(version=1, argv=['python','test.py'], cwd=str(tmp_path),status='COMPLETED', tree_terminal=True, raw_exit_code=i,
             output='observation.txt', started_at=f'2026-11-12T00:00:0{start}+00:00', ended_at=f'2026-11-12T00:00:0{end}+00:00'))
    data['commands'] = ['command-0.json','command-1.json']; save(path, data)
    assert not record_event(card,'attempt','time','lead',evidence=path.name,executor_state='completed').get('error')
    execution = engine.render_task_envelope(card,tmp_path)['TASK_HANDOFF']['execution']
    assert execution['last_attempt']['command_seconds'] == 6
    assert execution['last_attempt']['session_seconds'] == 10
    assert execution['checkpoint'] is None  # planned checkpoint is not implemented progress
    data.update(started_at=None,ended_at=None,commands=[]); save(path,data)
    record_event(card,'attempt','unknown-time','lead',evidence=path.name,executor_state='completed')
    execution = engine.render_task_envelope(card,tmp_path)['TASK_HANDOFF']['execution']
    assert execution['last_attempt']['session_seconds'] is None and execution['last_attempt']['command_seconds'] is None


def test_git_identity_and_legacy_claim_do_not_require_context(tmp_path):
    card, ctx, data = fixture(tmp_path)
    (card.parent/'iteration-delivery.json').unlink()
    card.write_text(card.read_text(encoding='utf-8').replace('delivery_mode: filesystem\n','').replace('candidate_id: candidate-1\n',''),encoding='utf-8')
    def git(*args):
        proc = subprocess.run(['git',*args],cwd=tmp_path,capture_output=True,encoding='utf-8')
        assert proc.returncode == 0, proc.stderr
        return proc.stdout.strip()
    git('init'); git('add','.'); git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','fixture')
    head = git('rev-parse','HEAD')
    data['tasks']['01']['candidate'] = head; save(ctx,data)
    assert cli(tmp_path,'--autonomy','claim',card,'--event-id','legacy','--owner','lead').returncode == 0
    proc = cli(tmp_path,'--dispatch-check',card,'--context',ctx.name,'--owner','lead')
    assert proc.returncode == 0, proc.stdout+proc.stderr
    assert json.loads(proc.stdout)['candidate'] == head
    path, attempt = report(tmp_path); attempt['candidate'] = head; save(path,attempt)
    assert attempt_cli(tmp_path,card,'git-attempt').returncode == 0
    handoff = json.loads(cli(tmp_path,'--render-envelope',card,tmp_path).stdout)['TASK_HANDOFF']
    assert handoff['delivery_mode'] == 'git' and handoff['candidate_id'] == '' and handoff['commit_sha'] == ''
    assert handoff['execution']['last_attempt']['candidate'] == head


def test_terminal_timeout_attempt_counts_no_progress_without_inventing_exit(tmp_path, monkeypatch):
    card, _, _ = fixture(tmp_path); monkeypatch.chdir(tmp_path)
    record_event(card,'claim','claim','lead')
    path, data = report(tmp_path)
    save(tmp_path/'timeout.json', dict(version=1, argv=['python','test.py'],cwd=str(tmp_path),
         status='TIMED_OUT',tree_terminal=True,raw_exit_code=None,output='observation.txt',
         started_at=data['started_at'],ended_at=data['ended_at']))
    data['commands'] = ['timeout.json']; save(path,data)
    result = record_event(card,'attempt','timeout-attempt','lead',evidence=path.name,executor_state='canceled')
    assert not result.get('error'), result
    execution = engine.render_task_envelope(card,tmp_path)['TASK_HANDOFF']['execution']
    assert execution['no_progress_streak'] == 1
    assert execution['last_attempt']['commands'][0]['status'] == 'TIMED_OUT'
    assert execution['last_attempt']['commands'][0]['raw_exit_code'] is None


def test_actual_runner_receipts_feed_attempt_and_dispatch_guard(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    assert cli(tmp_path,'--autonomy','claim',card,'--event-id','claim','--owner','lead').returncode == 0
    runner = str(Path(engine.__file__).with_name('iter_run.py'))
    started = datetime.now(timezone.utc).isoformat()
    deadline = (datetime.now(timezone.utc)+timedelta(seconds=30)).isoformat()
    proc = subprocess.run([sys.executable,'-B',runner,'--deadline',deadline,'--evidence','actual-command.json',
                           '--',sys.executable,'-B','-c',"print('actual process output')"],
                          cwd=tmp_path,capture_output=True,encoding='utf-8')
    assert proc.returncode == 0, proc.stdout+proc.stderr
    receipt = json.loads((tmp_path/'actual-command.json').read_text(encoding='utf-8'))
    assert receipt['tree_terminal'] is True and receipt['raw_exit_code'] == 0
    save(tmp_path/'actual-terminal.json',dict(returncode=proc.returncode, args=proc.args))
    path, data = report(tmp_path)
    data.update(commands=['actual-command.json'],terminal_evidence='actual-terminal.json',started_at=started,
                ended_at=datetime.now(timezone.utc).isoformat())
    save(path,data)
    for eid in ('one','two'):
        assert attempt_cli(tmp_path,card,eid).returncode == 0
    check = cli(tmp_path,'--dispatch-check',card,'--context',ctx.name,'--owner','lead')
    assert check.returncode == 3, check.stdout+check.stderr
    execution = json.loads(check.stdout)['execution']
    assert execution['no_progress_streak'] == 2 and execution['last_attempt']['command_seconds'] > 0
    # A successful command with no delivered artifact is not progress or acceptance.
    assert execution['checkpoint'] is None


def test_dispatch_rejects_outside_card_before_reading(tmp_path):
    project = tmp_path / 'project'
    project.mkdir()
    outside = tmp_path / 'outside.md'
    outside.write_text('---\nPRIVATE_OUTSIDE_MARKER\n---\n', encoding='utf-8')
    proc = cli(project, '--dispatch-check', outside)
    assert proc.returncode == 3
    assert 'PRIVATE_OUTSIDE_MARKER' not in proc.stdout
    assert 'leaves project root' in ' '.join(json.loads(proc.stdout)['findings'])


@pytest.mark.parametrize('flags', [[], ['--phase-from-context']])
def test_preflight_preserves_outside_symlink_without_reading(tmp_path, flags):
    project = tmp_path / 'project'
    card, ctx, _ = fixture(project)
    outside = tmp_path / 'outside.md'
    outside.write_text('---\nPRIVATE_OUTSIDE_MARKER\n---\n', encoding='utf-8')
    (card.parent / 'outside.md').symlink_to(outside)
    before = (card.read_bytes(), ctx.read_bytes())
    proc = cli(project, '--preflight', card.parent, '--context', ctx.name, *flags)
    assert proc.returncode == 3
    result = json.loads(proc.stdout)
    assert any(t['readiness'] == 'READY' for t in result['tasks'])
    assert any('leaves project root' in ' '.join(t['findings']) for t in result['tasks'])
    assert 'PRIVATE_OUTSIDE_MARKER' not in proc.stdout
    assert before == (card.read_bytes(), ctx.read_bytes())


def test_preflight_rejects_explicit_unknown_delivery_mode(tmp_path):
    card, ctx, data = fixture(tmp_path)
    (card.parent / 'iteration-delivery.json').unlink()
    card.write_text(card.read_text(encoding='utf-8').replace('delivery_mode: filesystem',
                    'delivery_mode: not-a-mode').replace('candidate_id: candidate-1\n', ''), encoding='utf-8')
    def git(*args):
        proc = subprocess.run(['git', *args], cwd=tmp_path, capture_output=True, encoding='utf-8')
        assert proc.returncode == 0, proc.stderr
        return proc.stdout.strip()
    git('init'); git('add', '.')
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'fixture')
    data['tasks']['01']['candidate'] = git('rev-parse', 'HEAD')
    save(ctx, data)
    proc = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name)
    assert proc.returncode == 3
    assert 'delivery mode' in ' '.join(json.loads(proc.stdout)['tasks'][0]['findings']).lower()
