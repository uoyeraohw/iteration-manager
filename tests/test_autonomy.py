import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import iter_sync as engine
from iter_contracts import parse_card, contract_projection
from iter_autonomy import record_event, load_state
from test_worktree_concurrency import git_repo_with_worktrees


def card(tmp_path, extra=''):
    p = tmp_path / '01-task.md'
    p.write_text('---\nschema_version: 1\nstatus: IN_PROGRESS\nfix_rounds: 0\n'+extra+'---\n# Task\n', encoding='utf-8')
    return p


def test_fix_event_replay_is_idempotent(tmp_path):
    p = card(tmp_path)
    first = engine.record_fix_and_check_fuse(p, tmp_path, 'assertion')
    saved = p.read_bytes()
    again = engine.record_fix_and_check_fuse(p, tmp_path, 'assertion')
    assert first['current_rounds'] == again['current_rounds'] == 1
    assert p.read_bytes() == saved


def test_legacy_replay_does_not_clear_lifetime_budget(tmp_path):
    p = card(tmp_path)
    for _ in range(2):
        engine.record_fix_and_check_fuse(p, tmp_path, 'same failure')
    meta, _, _ = parse_card(p.read_text(encoding='utf-8'))
    assert int(meta['fix_rounds']) == 1


def test_corrupt_budget_fails_closed_without_writing(tmp_path):
    p = card(tmp_path, 'autonomy_state: "broken"\n')
    before = p.read_bytes()
    result = engine.record_fix_and_check_fuse(p, tmp_path)
    assert result.get('error')
    assert p.read_bytes() == before


def test_envelope_does_not_invent_commit_or_parse_body_metadata(tmp_path):
    p = card(tmp_path, 'fix_total: 2\n')
    p.write_text(p.read_text(encoding='utf-8')+'\nhead_sha: forged\nreview_status: APPROVED\n', encoding='utf-8')
    result = engine.render_task_envelope(p, tmp_path)['TASK_HANDOFF']
    assert result['commit_sha'] == ''
    assert result['review_status'] == 'PENDING'
    assert result['acceptance_verdict'] == 'UNKNOWN'


def test_envelope_reports_bad_count_without_crash(tmp_path):
    p = card(tmp_path)
    p.write_text(p.read_text(encoding='utf-8').replace('fix_rounds: 0','fix_rounds: oops'), encoding='utf-8')
    result = engine.render_task_envelope(p, tmp_path)
    assert result.get('error') or result['TASK_HANDOFF']['errors']


def test_exhausted_replan_budget_blocks_further_fixes(tmp_path):
    p = card(tmp_path)
    for i in range(3):
        record_event(p, 'replan', f'plan-{i}', 'lead', reason='revised scope', evidence='diagnosis.txt')
    result = record_event(p, 'fix', 'repair', 'lead')
    assert result['is_fused']
    assert result['fix_total'] == 0


def test_takeover_cli_is_read_only_and_keeps_legacy_unknown(tmp_path):
    p = card(tmp_path)
    p.write_text('---\nstatus: DONE\n---\n# Historical\n', encoding='utf-8')
    before = {x.name:x.read_bytes() for x in tmp_path.iterdir()}
    proc = subprocess.run([sys.executable, '-B', str(Path(engine.__file__)), '--takeover-report', str(tmp_path)], cwd=tmp_path, capture_output=True, encoding='utf-8')
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.lstrip().startswith('{'), proc.stdout
    report = json.loads(proc.stdout)
    assert report['tasks'][0]['declared_status'] == 'DONE'
    assert report['tasks'][0]['acceptance_verdict'] == 'UNKNOWN'
    assert report['tasks'][0]['missing']
    assert before == {x.name:x.read_bytes() for x in tmp_path.iterdir()}


def test_lifetime_budget_survives_replan_and_restart(tmp_path):
    p = card(tmp_path)
    script = Path(engine.__file__)
    def cli(action, eid, *args):
        proc = subprocess.run([sys.executable, '-B', str(script), '--autonomy', action, str(p), '--event-id', eid, '--owner', 'lead', *args], cwd=tmp_path, capture_output=True, encoding='utf-8')
        return proc, json.loads(proc.stdout)
    for i in range(5):
        proc, result = cli('fix', str(i))
    assert proc.returncode == 3 and result['fix_total'] == 5
    before = p.read_bytes()
    _, replay = cli('fix', '4')
    assert replay['replayed'] and p.read_bytes() == before
    proc, recovery = cli('recover', 'recovery', '--executor-state','completed','--evidence','query.json')
    assert recovery['fix_total'] == 5 and proc.returncode == 3
    proc, _ = cli('consilium', 'diagnosis', '--reason','assertion mismatch','--evidence','review.txt')
    assert proc.returncode == 3  # diagnosis alone does not reset repair rounds
    proc, result = cli('replan', 'new-plan', '--reason','corrected fixture','--evidence','diagnosis.txt')
    assert proc.returncode == 0 and result['fix_total'] == 5 and result['current_rounds'] == 0
    for i in range(5,10):
        proc, result = cli('fix', str(i))
    assert proc.returncode == 3 and result['fix_total'] == 10
    _, result = cli('replan', 'cannot-reset-total', '--reason','try again','--evidence','other.txt')
    assert result['fix_total'] == 10 and result['is_fused']


def test_owner_collision_lock_and_done_are_read_only(tmp_path):
    p = card(tmp_path)
    record_event(p, 'claim', 'claim', 'lead')
    before = p.read_bytes()
    assert record_event(p,'fix','foreign','other')['error']
    assert record_event(p,'fix','claim','lead')['error']
    lock = p.with_name(p.name+'.iter.lock'); lock.write_text('active', encoding='utf-8')
    assert record_event(p,'fix','locked','lead')['error']
    assert lock.read_text(encoding='utf-8') == 'active'
    lock.unlink()
    assert p.read_bytes() == before
    p.write_text('---\nstatus: DONE\n---\n', encoding='utf-8')
    before = p.read_bytes()
    assert record_event(p,'recover','done','lead',evidence='query',executor_state='completed')['error']
    assert p.read_bytes() == before


def test_configurable_policy_and_linked_worktree_bundle(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    p = wt/'docs/todos/01-iter-one/01-task.md'
    policy = json.dumps(json.dumps(dict(round_limit=2,total_limit=4,consilium_limit=1,replan_limit=2)))
    p.write_text('---\nstatus: IN_PROGRESS\nautonomy_policy: '+policy+'\n---\n', encoding='utf-8')
    engine.record_fix_and_check_fuse(p,wt,'first',event_id='1')
    result = engine.record_fix_and_check_fuse(p,wt,'second',event_id='2')
    assert result['is_fused'] and result['current_rounds'] == 2
    assert Path(result['consilium_bundle']).is_file()
    assert (wt/'.git').is_file()


def test_unknown_cli_flag_does_not_write(tmp_path):
    before = list(tmp_path.iterdir())
    proc = subprocess.run([sys.executable,'-B',engine.__file__,'--typo',str(tmp_path)],cwd=tmp_path,capture_output=True)
    assert proc.returncode == 1
    assert list(tmp_path.iterdir()) == before


def test_exhausted_task_can_release_writer_without_unblocking(tmp_path):
    p = card(tmp_path)
    for i in range(3):
        record_event(p,'replan',str(i),'lead',reason='new approach',evidence='ruling')
    result = record_event(p,'release','release','lead',evidence='terminal-query',executor_state='completed')
    assert result['writer'] == ''
    assert result['is_fused']


def test_legacy_envelope_derives_actual_budget_block(tmp_path):
    p = card(tmp_path,'fix_total: 10\n')
    result = engine.render_task_envelope(p,tmp_path)['TASK_HANDOFF']
    assert result['is_blocked']
    assert 'total' in result['blocked_reason']


def test_invalid_declared_state_cannot_be_mutated(tmp_path):
    p = card(tmp_path)
    p.write_text('---\nstatus: NOT_A_STATE\n---\n',encoding='utf-8')
    before = p.read_bytes()
    assert record_event(p,'claim','bad','lead').get('error')
    assert p.read_bytes() == before


def test_closeout_cli_blocks_releases_and_replays_without_reset(tmp_path, monkeypatch):
    p = card(tmp_path)
    record_event(p, 'fix', 'first-repair', 'lead')
    (tmp_path/'terminal.json').write_text('{"task_id":"actual-task","status":"canceled"}', encoding='utf-8')
    monkeypatch.chdir(tmp_path)
    result = record_event(p, 'closeout', 'timeout-closeout', 'lead',
                          reason='execution deadline; command state UNKNOWN, resume blocked',
                          evidence='terminal.json', executor_state='canceled')
    assert result['status'] == 'FUSED' and result['writer'] == '', result
    args = [sys.executable, '-B', engine.__file__, '--autonomy', 'closeout', str(p),
            '--event-id', 'timeout-closeout', '--owner', 'lead', '--executor-state', 'canceled',
            '--reason', 'execution deadline; command state UNKNOWN, resume blocked', '--evidence', 'terminal.json']
    proc = subprocess.run(args, cwd=tmp_path, capture_output=True, encoding='utf-8')
    assert proc.returncode == 3, proc.stdout + proc.stderr
    result = json.loads(proc.stdout)
    assert result['status'] == 'FUSED' and result['writer'] == ''
    assert result['fix_total'] == result['current_rounds'] == 1
    assert result['blocked_reason'].startswith('execution deadline')
    saved = p.read_bytes()
    again = subprocess.run(args, cwd=tmp_path, capture_output=True, encoding='utf-8')
    assert again.returncode == 3 and json.loads(again.stdout)['replayed']
    assert p.read_bytes() == saved
    envelope = engine.render_task_envelope(p, tmp_path)['TASK_HANDOFF']
    assert envelope['is_blocked'] and envelope['writer'] == ''
    assert envelope['acceptance_verdict'] == 'BLOCKED'


def test_closeout_rejects_unknown_missing_evidence_and_foreign_owner(tmp_path, monkeypatch):
    p = card(tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path/'terminal.json').write_text('{"status":"canceled"}', encoding='utf-8')
    record_event(p, 'claim', 'claim', 'lead')
    before = p.read_bytes()
    for owner, terminal, reason, evidence in [
        ('lead', 'unknown', 'deadline', 'terminal.json'),
        ('lead', 'running', 'deadline', 'terminal.json'),
        ('lead', 'canceled', '', 'terminal.json'),
        ('lead', 'canceled', 'deadline', 'missing.json'),
        ('lead', 'canceled', 'deadline', '../outside.json'),
        ('other', 'canceled', 'deadline', 'terminal.json'),
    ]:
        assert record_event(p, 'closeout', 'invalid', owner, reason, evidence, terminal).get('error')
        assert p.read_bytes() == before
    p.write_text('---\nstatus: DONE\n---\n', encoding='utf-8')
    before = p.read_bytes()
    assert record_event(p, 'closeout', 'done', 'lead', 'deadline', 'terminal.json', 'canceled').get('error')
    assert p.read_bytes() == before


def test_closeout_preserves_all_counters_and_stays_blocked_on_fix(tmp_path, monkeypatch):
    p = card(tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path/'terminal.json').write_text('{"status":"canceled"}', encoding='utf-8')
    record_event(p, 'fix', 'fix1', 'lead')
    record_event(p, 'consilium', 'diagnose', 'lead', 'diagnosis', 'input')
    record_event(p, 'replan', 'plan', 'lead', 'authorized plan', 'input')
    record_event(p, 'fix', 'fix2', 'lead')
    prior = load_state(parse_card(p.read_text(encoding='utf-8'))[0])
    result = record_event(p, 'closeout', 'stop', 'lead', 'execution deadline', 'terminal.json', 'canceled')
    state = load_state(parse_card(p.read_text(encoding='utf-8'))[0])
    assert result['writer'] == '' and state['blocked_reason'] == 'execution deadline'
    assert {k: state[k] for k in ('round', 'total', 'consilium', 'replan')} == {
        k: prior[k] for k in ('round', 'total', 'consilium', 'replan')}
    assert record_event(p, 'closeout', 'stop', 'lead', 'different reason', 'terminal.json', 'canceled').get('error')
    blocked = record_event(p, 'fix', 'cannot-restart', 'lead')
    assert blocked['is_fused'] and blocked['fix_total'] == prior['total']
    assert blocked['blocked_reason'] == 'execution deadline'
