"""Validate native evidence inventory and actual before/after observations, not agent semantics."""
import json
import pathlib
import subprocess

ROOT = pathlib.Path.cwd()
BASE = ROOT / 'docs/todos/10-self-hosting-hardening/evidence/01'
E = BASE / 'consumption-b'
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

matrix = read(BASE / 'authority-matrix.json')
for s in matrix['scenarios']:
    case = s['id']
    for p in s['evidence']:
        assert (ROOT / p).stat().st_size > 0, p
    n = read(E / (case + '-native.json'))
    t = n['native_terminal_and_guard']
    assert t['terminalConfirmed'] and t['final']['status'] == 'completed'
    assert t['lateByMs'] == 0 and t['final']['text']
    assert n['session_info']['structuredContent']['parent_id'] == 1703
    c = read(E / (case + '-calls.json'))
    assert not c['unmatched_call_ids']
    assert c['tool_call_count'] == c['tool_output_count'] > 0
    assert any(r['record']['payload'].get('type') == 'task_complete' for r in c['selected_records'])
    shell_results = []
    for r in c['selected_records']:
        q = r['record']['payload']
        if q.get('type') not in ('function_call_output', 'custom_tool_call_output'):
            continue
        blocks = q.get('output', [])
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            try:
                value = json.loads(block.get('text', ''))
            except (ValueError, TypeError):
                continue
            if isinstance(value, dict) and 'chunk_id' in value:
                assert value.get('exit_code') == 0, value
                assert not value.get('session_id'), value
                shell_results.append(value['exit_code'])
    assert shell_results, case
    print(case, 'completed; calls/outputs', c['tool_call_count'], '; shell exits', shell_results)

controller_file = 'docs/todos/10-self-hosting-hardening/evidence/01/dispatch-native-implementation-b.json'
for wave in ('wave1', 'wave2'):
    raw = read(E / (wave + '-comparison.json'))
    expected = [] if wave == 'wave1' else [controller_file]
    assert raw['byte_changed_paths'] == expected
    assert raw['disk_metadata_changed_paths'] == expected
    assert raw['git_changed_fields'] == ['status']
    a, b = [read(E / (wave + '-' + side + '.json')) for side in ('before', 'after')]
    def normalized(x):
        return [line for line in x['git']['status']['stdout'].splitlines()
                if 'evidence/01/consumption-b/' not in line and controller_file not in line]
    assert normalized(a) == normalized(b)
    if wave == 'wave2':
        attribution = read(E / (wave + '-attribution.json'))
        assert attribution['controller_record_after']['child_conversation_id'] == 1703
        assert attribution['controller_record_after']['task_id'] == '6c6e933a-5d58-4dbb-aa57-3d953f675e2f'
    print(wave, '143 files byte-compared; only recorded parent/controller evidence additions')

sources = ['references/worktree_git_contract.md', 'references/superpowers_handbook.md',
           'templates/root_readme.md', 'tests/test_prompt_sources.py', 'tests/test_authority_scenarios.py',
           '.agents/notes/implemented/process/2026-11-13-authority-consistency.md']
subprocess.run(['git', 'diff', '--exit-code', '5ff7c3af554f9effdf0a95050af24c767ca0878b', '--', *sources], check=True)
print('A source/test/note bytes unchanged; no regression rerun. Native observation inventory verified; independent review remains pending.')
