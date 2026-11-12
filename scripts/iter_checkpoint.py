"""Controller-issued checkpoint capabilities, separate from repair budgets.

The host protects the external grant; reviewers establish native provenance.
This module checks bindings and evidence shape, not cryptographic authenticity.
"""
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from iter_contracts import contained, relative_path

RESUME_LIMIT = 3
TERMINAL = ('completed', 'failed', 'canceled')


def utc(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError('Explicit UTC timestamp required')
    return parsed


def read_grant(path):
    if not path:
        raise ValueError('External controller resume grant required')
    path = Path(path).resolve(strict=True)
    if path.is_relative_to(Path.cwd().resolve()):
        raise ValueError('Resume grant must be outside the workspace')
    if path.stat().st_size > 65536:
        raise ValueError('Resume grant too large')
    grant = json.loads(path.read_text(encoding='utf-8'))
    fields = {'version', 'grant_id', 'workspace', 'card', 'head', 'checkpoint_sha',
              'closeout_event_id', 'terminal_evidence', 'expires_at'}
    if (not isinstance(grant, dict) or set(grant) not in (fields, fields | {'interruption_review'})
            or type(grant['version']) is not int or grant['version'] != 1):
        raise ValueError('Invalid resume grant schema')
    if any(not isinstance(grant[k], str) or not grant[k].strip() for k in set(grant) - {'version'}):
        raise ValueError('Resume grant fields must be nonempty text')
    return grant


def git(root, *args):
    try:
        proc = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired as error:
        raise ValueError('Git checkpoint query timed out; no mutation') from error
    if proc.returncode:
        raise ValueError('Git checkpoint check failed: ' + proc.stderr.strip())
    return proc.stdout.strip()


def validate_resume(task_file, state, status, grant):
    root = Path.cwd().resolve()
    if Path(grant['workspace']).resolve(strict=True) != root:
        raise ValueError('Resume workspace/cwd mismatch')
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise ValueError('Resume must run from exact repository/worktree root')
    if contained(root, grant['card']) != task_file.resolve():
        raise ValueError('Resume card mismatch')
    if status != 'FUSED' or state['writer']:
        raise ValueError('Resume requires FUSED checkpoint with no writer')
    policy = state['policy']
    if (state['round'] >= policy['round_limit'] or state['total'] >= policy['total_limit']
            or state['consilium'] > policy['consilium_limit'] or state['replan'] > policy['replan_limit']
            or state.get('blocked_reason') in ('total repair budget exhausted', 'replan budget exhausted',
                'consilium budget exhausted', 'round repair budget exhausted; bounded diagnosis/replan required')):
        raise ValueError('Checkpoint resume cannot bypass budget or non-deadline block')
    events = state['events']
    closeouts = [(k, v) for k, v in events.items() if v['input']['action'] == 'closeout']
    if not closeouts or closeouts[-1][0] != grant['closeout_event_id']:
        raise ValueError('Grant must bind latest closeout')
    closeout = closeouts[-1][1]
    if (closeout['input']['executor_state'] not in TERMINAL
            or closeout['result']['writer'] or closeout['result']['status'] != 'FUSED'):
        raise ValueError('Invalid terminal deadline closeout')
    prior = [v['input']['resume_grant'] for v in events.values()
             if v['input']['action'] == 'resume-checkpoint' and not v['result'].get('is_fused')]
    if len(prior) >= RESUME_LIMIT:
        raise ValueError('Checkpoint resume limit exhausted (3)')
    if any(g['grant_id'] == grant['grant_id'] or g['closeout_event_id'] == grant['closeout_event_id'] for g in prior):
        raise ValueError('Grant or closeout already consumed')
    if utc(grant['expires_at']) <= datetime.now(timezone.utc):
        raise ValueError('Resume grant expired')
    for key in ('head', 'checkpoint_sha'):
        if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', grant[key]):
            raise ValueError('Full checkpoint SHA required')
    if git(root, 'rev-parse', 'HEAD') != grant['head']:
        raise ValueError('Resume HEAD mismatch')
    git(root, 'merge-base', '--is-ancestor', grant['checkpoint_sha'], grant['head'])
    lock = task_file.resolve().relative_to(root).as_posix() + '.iter.lock'
    if git(root, 'status', '--porcelain', '--untracked-files=all', '--', '.', ':(exclude,literal)' + lock):
        raise ValueError('Resume requires clean frozen worktree')
    standard = (state.get('blocked_reason', '').startswith('execution deadline')
                and closeout['input']['reason'].startswith('execution deadline'))
    if not standard or 'interruption_review' in grant:
        if 'interruption_review' not in grant:
            raise ValueError('Nonstandard closeout requires independent typed interruption review')
        review = committed_json(root, grant['interruption_review'])
        fields = {'version', 'kind', 'verdict', 'closeout_event_id', 'blocked_reason', 'reviewer_session', 'source'}
        if (not isinstance(review, dict) or set(review) != fields or type(review['version']) is not int
                or review['version'] != 1 or review['kind'] != 'execution-deadline' or review['verdict'] != 'APPROVED'
                or review['closeout_event_id'] != grant['closeout_event_id']
                or review['blocked_reason'] != state.get('blocked_reason')
                or review['blocked_reason'] != closeout['input']['reason']
                or any(not isinstance(review[k], str) or not review[k].strip() for k in fields - {'version'})):
            raise ValueError('Invalid or unbound independent interruption review')
    terminal = committed_json(root, grant['terminal_evidence'])
    if not isinstance(terminal, dict) or terminal.get('version') != 1:
        raise ValueError('Invalid terminal evidence schema')
    for kind in ('sessions', 'commands'):
        records = terminal.get(kind)
        if not isinstance(records, list) or not records:
            raise ValueError('Nonempty session and command evidence required')
        for record in records:
            if (not isinstance(record, dict) or not record.get('id') or not record.get('source')
                    or record.get('status') not in TERMINAL):
                raise ValueError('Running/unknown or unsourced terminal record')
            if kind == 'commands' and (record['status'] != 'completed' or type(record.get('exit_code')) is not int):
                raise ValueError('Command requires observed completion and actual exit code')
    if utc(grant['expires_at']) <= datetime.now(timezone.utc):
        raise ValueError('Resume grant expired during validation')
    return len(prior) + 1


def committed_json(root, path):
    """Read evidence from the bound HEAD, not an ignored/untracked local file."""
    contained(root, path)
    return json.loads(git(root, 'show', 'HEAD:' + relative_path(path)))
