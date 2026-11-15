"""Synthetic approval fixtures exercise validators, never real task approval."""
import json
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_sync import audit_task_file, generate_board_data, render_task_envelope
from test_worktree_concurrency import git_repo_with_worktrees, run_cmd
from test_execution_readiness import fixture, cli
from test_filesystem_delivery_controller import fixture as fs_done_fixture

def make_reviewed_candidate(wt, kind="Strict-TDD", declaration=""):
    """Synthetic receipt fixture: tests structure/version gates, not real task acceptance."""
    base = run_cmd(["git", "rev-parse", "HEAD"], wt).stdout.strip()
    card = wt / "docs/todos/01-iter-one/01-task.md"
    evidence = wt / "docs/todos/01-iter-one/evidence/01"
    evidence.mkdir(parents=True)
    names = {"Strict-TDD": ["red", "green", "regression"],
             "UI-Component": ["interaction", "states", "visual", "regression"],
             "Refactor-Benchmark": ["baseline", "regression", "compatibility", "benchmark_before", "benchmark_after"],
             "Spike-Discovery": ["experiment", "decision", "interfaces"]}[kind]
    observations = {"states", "visual", "compatibility", "decision", "interfaces"}
    checks = []
    for name in names:
        output = evidence / (name + ".txt")
        output.write_text("synthetic fixture: " + name, encoding="utf-8")
        check = {"name": name, "kind": "observation" if name in observations else "command",
                 "summary": "synthetic fixture observed result", "output": output.relative_to(wt).as_posix()}
        if name not in observations:
            check.update(command="python -m pytest tests/test_behavior.py", cwd=".", exit_code=1 if name == "red" else 0)
        if name == "red":
            check["failure_kind"] = "assertion"
        checks.append(check)
    report = evidence / "review.txt"
    report.write_text("synthetic independent review fixture", encoding="utf-8")
    readme = card.parent / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + '\n<!-- iter:goal -->\nFrozen iteration goal.\n<!-- /iter:goal -->\n', encoding="utf-8")
    card.write_text(f'---\nschema_version: 1\ntask_id: "01"\ntype: {kind}\nstatus: TESTING\n'
                    f'{declaration}base_sha: {base}\nhead_sha: ""\nreview_status: PENDING\n'
                    f'tdd_verified: {"true" if kind == "Strict-TDD" else "false"}\n'
                    'review_receipt: docs/todos/01-iter-one/evidence/01/review.json\n---\n'
                    '## 1. Objective\nKeep behavior stable.\n'
                    '<!-- iter:scope -->\n| File path | Role |\n| --- | --- |\n'
                    '| `src/a.py` | implementation |\n'
                    '| `docs/todos/01-iter-one/evidence/01/` | evidence |\n<!-- /iter:scope -->\n'
                    '<!-- iter:acceptance -->\n- [x] Observable behavior\n<!-- /iter:acceptance -->\n'
                    '<!-- iter:ledger -->\nPending report\n<!-- /iter:ledger -->\n', encoding="utf-8")
    (wt / "src").mkdir(exist_ok=True)
    (wt / "src/a.py").write_text("value = 1\n", encoding="utf-8")
    run_cmd(["git", "add", "."], wt)
    run_cmd(["git", "commit", "-m", "implement reviewed task"], wt)
    head = run_cmd(["git", "rev-parse", "HEAD"], wt).stdout.strip()
    receipt = {"schema_version": 1, "task_id": "01", "type": kind,
               "task_path": card.relative_to(wt).as_posix(), "base_sha": base,
               "head_sha": head, "contract_sha": head, "implementer": "implementer-session",
               "reviewer": "independent-review-session", "verdict": "APPROVED",
               "review_report": report.relative_to(wt).as_posix(), "checks": checks}
    receipt_path = evidence / "review.json"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    text = card.read_text(encoding="utf-8").replace("status: TESTING", "status: DONE").replace('head_sha: ""', f"head_sha: {head}").replace("review_status: PENDING", "review_status: APPROVED")
    card.write_text(text, encoding="utf-8")
    run_cmd(["git", "add", "."], wt)
    run_cmd(["git", "commit", "-m", "record approval and evidence"], wt)
    return card, receipt_path, receipt


@pytest.mark.parametrize("declaration,expected", [("", "PASS"), ("delivery_mode: git\n", "PASS"), ("delivery_mode: UNKNOWN\n", "FAIL"), ("delivery_mode: \"\"\n", "FAIL")])
def test_done_git_mode_is_validated_at_frozen_contract(git_repo_with_worktrees, declaration, expected):
    _, wt, _ = git_repo_with_worktrees
    card, _, receipt = make_reviewed_candidate(wt, declaration=declaration)
    frozen = run_cmd(["git", "show", receipt["contract_sha"] + ":" + card.relative_to(wt).as_posix()], wt).stdout
    assert declaration in frozen
    result = audit_task_file(card)
    assert result["verdict"] == expected, result


@pytest.mark.parametrize("mode,profile", [("UNKNOWN", None), ("", None), ("filesystem", None), ("git", "valid"), ("UNKNOWN", "valid"), ("filesystem", "broken")])
def test_invalid_modes_rejected_by_dispatch_audit_and_board(tmp_path, mode, profile):
    card, ctx, _ = fixture(tmp_path)
    card.write_text(card.read_text().replace("delivery_mode: filesystem", "delivery_mode: " + json.dumps(mode)), encoding="utf-8")
    path = card.parent / "iteration-delivery.json"
    if profile is None:
        path.unlink()
    elif profile == "broken":
        path.write_text('{}', encoding="utf-8")
    assert cli(tmp_path, '--autonomy', 'claim', card, '--event-id', 'claim', '--owner', 'lead').returncode == 0
    proc = cli(tmp_path, '--dispatch-check', card, '--context', ctx.name, '--owner', 'lead')
    assert proc.returncode == 3
    assert any(word in ' '.join(json.loads(proc.stdout)['findings']).lower() for word in ('delivery', 'profile'))
    audit = audit_task_file(card)
    assert audit['verdict'] != 'PASS' and audit['violations'], audit
    board = generate_board_data(card.parent)['cards'][0]
    assert board['delivery_mode'] == 'UNKNOWN' and board['findings'], board
    envelope = render_task_envelope(card, tmp_path)
    if profile == 'broken':
        assert envelope.get('error')
    else:
        handoff = envelope['TASK_HANDOFF']
        assert handoff['delivery_mode'] == 'UNKNOWN' and handoff['errors'], handoff


def test_valid_filesystem_done_control(tmp_path):
    card, _, _ = fs_done_fixture(tmp_path)
    assert audit_task_file(card)['verdict'] == 'PASS'
    assert generate_board_data(card.parent)['cards'][0]['delivery_mode'] == 'filesystem'
    assert render_task_envelope(card, tmp_path)['TASK_HANDOFF']['delivery_mode'] == 'filesystem'


@pytest.mark.parametrize('meta,enabled,expected', [
    ({}, False, 'git'), ({'delivery_mode': 'git'}, False, 'git'),
    ({'delivery_mode': 'filesystem'}, True, 'filesystem'),
    ({'delivery_mode': ''}, False, None), ({'delivery_mode': 'unknown'}, False, None),
    ({'delivery_mode': 'filesystem'}, False, None), ({}, True, None),
    ({'delivery_mode': 'git'}, True, None), ({'delivery_mode': None}, False, None),
])
def test_pure_resolution_boundary(meta, enabled, expected):
    from iter_contracts import resolve_delivery_mode
    if expected is None:
        with pytest.raises(ValueError):
            resolve_delivery_mode(meta, enabled)
    else:
        assert resolve_delivery_mode(meta, enabled) == expected


@pytest.mark.parametrize('status,verdict', [('FUSED', 'BLOCKED'), ('bad-status', 'UNKNOWN')])
def test_invalid_mode_preserves_fused_and_unknown_status(tmp_path, status, verdict):
    card = tmp_path / '01-task.md'
    card.write_text('---\nstatus: ' + status + '\ndelivery_mode: unknown\n---\n', encoding='utf-8')
    result = audit_task_file(card)
    assert result['verdict'] == verdict and result['violations']


def test_missing_receipt_legacy_done_remains_unknown(tmp_path):
    card = tmp_path / '01-task.md'
    card.write_text('---\nstatus: DONE\n---\n', encoding='utf-8')
    assert audit_task_file(card)['verdict'] == 'UNKNOWN'


def test_undeclared_card_conflicts_with_filesystem_profile(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    card.write_text(card.read_text().replace('delivery_mode: filesystem\n', ''), encoding='utf-8')
    proc = cli(tmp_path, '--dispatch-check', card, '--context', ctx.name, '--owner', 'lead')
    assert proc.returncode == 3 and 'profile' in proc.stdout.lower()
    assert audit_task_file(card)['violations']
    assert generate_board_data(card.parent)['cards'][0]['delivery_mode'] == 'UNKNOWN'
    handoff = render_task_envelope(card, tmp_path)['TASK_HANDOFF']
    assert handoff['delivery_mode'] == 'UNKNOWN' and handoff['errors']


@pytest.mark.parametrize('change', ['missing-profile', 'broken-profile', 'conflict'])
def test_done_filesystem_profile_errors_are_reported(tmp_path, change):
    card, _, _ = fs_done_fixture(tmp_path)
    assert audit_task_file(card)['verdict'] == 'PASS'  # Synthetic control before mutation.
    profile = card.parent / 'iteration-delivery.json'
    if change == 'missing-profile':
        profile.unlink()
    elif change == 'broken-profile':
        profile.write_text('{}', encoding='utf-8')
    else:
        card.write_text(card.read_text().replace('delivery_mode: filesystem', 'delivery_mode: git'), encoding='utf-8')
    result = audit_task_file(card)
    assert result['verdict'] != 'PASS' and any('profile' in v.lower() for v in result['violations']), result


@pytest.mark.parametrize('mode', ['absent', 'git', 'filesystem'])
def test_valid_mode_dispatch_with_claimed_owner(tmp_path, mode):
    import subprocess
    card, ctx, data = fixture(tmp_path)
    if mode != 'filesystem':
        (card.parent / 'iteration-delivery.json').unlink()
        replacement = '' if mode == 'absent' else 'delivery_mode: git\n'
        card.write_text(card.read_text().replace('delivery_mode: filesystem\n', replacement), encoding='utf-8')
        def git(*args):
            result = subprocess.run(['git', *args], cwd=tmp_path, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        git('init'); git('add', '.')
        git('-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid', 'commit', '-m', 'fixture')
        data['tasks']['01']['candidate'] = git('rev-parse', 'HEAD')
        ctx.write_text(json.dumps(data), encoding='utf-8')
    assert cli(tmp_path, '--autonomy', 'claim', card, '--event-id', 'claim', '--owner', 'lead').returncode == 0
    result = cli(tmp_path, '--dispatch-check', card, '--context', ctx.name, '--owner', 'lead')
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)['delivery_mode'] == ('git' if mode == 'absent' else mode)
    assert generate_board_data(card.parent)['cards'][0]['delivery_mode'] == ('git' if mode == 'absent' else mode)
    assert render_task_envelope(card, tmp_path)['TASK_HANDOFF']['delivery_mode'] == ('git' if mode == 'absent' else mode)
