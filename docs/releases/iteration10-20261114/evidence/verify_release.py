"""Controller acceptance using frozen commands, bytes, and actual native calls."""
import base64
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def terminal(path, code=0):
    r = read(path)
    assert (r['status'], r['raw_exit_code'], r['tree_terminal']) == ('COMPLETED', code, True), str(path)
    return r
def normalize(text):
    return text.replace('\r\n', '\n')
def strings(value):
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings(v)]
    if isinstance(value, str):
        result = [value]
        if value.startswith(('{', '[')):
            try:
                result += strings(json.loads(value))
            except json.JSONDecodeError:
                pass
        return result
    return []

plan = read(HERE / 'deployment-plan.json')
assert plan['source_head'] == '26652bad2fcfb7c883d8e9a8bcad4aeb96160816'
assert len(plan['files']) == 91
for item in plan['items']:
    source, dest = Path(item['source']), Path(item['root']) / item['relative']
    assert source.read_bytes() == dest.read_bytes() == (ROOT / item['relative']).read_bytes()
    if item['existed']:
        assert Path(item['backup']).is_file()
for item in plan['preserved_nonactive_backups']:
    assert Path(item['path']).read_bytes() == Path(item['snapshot']).read_bytes()
assert subprocess.run(['git','diff','--quiet','HEAD','--','SKILL.md','scripts','references','templates','tests','.agents/notes'], cwd=ROOT).returncode == 0
for name in ['main-tests', 'root-sync', 'deploy-command', 'native-collection', 'native-documents']:
    terminal(HERE / (name + '.json'))
assert '493 passed in 410.05s' in (HERE / 'main-tests.json.output.txt').read_text(encoding='utf-8')

codex = HERE / 'codex-consumption/sandbox/continuation'
gemini = HERE / 'gemini-consumption'
terminal(codex.parent / 'probe-run.json', 1)  # Preserved erroneous probe assertion, not product RED.
consumer_summaries = []
for name, path, installation in [('codex', codex, Path('C:/Users/qingyu/.codex/skills/iteration-manager')),
        ('gemini', gemini, Path('C:/Users/qingyu/.gemini/config/skills/iteration-manager'))]:
    receipt = terminal(path / 'probe-run.json')
    results = read(path / 'probe-results.json')
    commands = results['commands'] if isinstance(results, dict) else [r for r in results if not r['argv'][0].startswith('internal:')]
    assert [r['returncode'] for r in commands] == [0,0,2,0]
    for command in commands:
        assert Path(command['argv'][2]).is_relative_to(installation)
    assert normalize(commands[0]['stdout']) == (path / 'card.md').read_text(encoding='utf-8')
    assert json.loads(commands[1]['stdout']) == dict(valid=True, errors=[])
    rejected = json.loads(commands[2]['stdout'])
    assert rejected['valid'] is False and '../escape' in str(rejected['errors'])
    takeover = json.loads(commands[3]['stdout'])
    assert takeover == read(path / 'takeover.json') and takeover['read_only'] is True
    assert len(takeover['tasks']) == 6
    assert all(t['declared_status']=='DONE' and t['acceptance_verdict']=='PASS' and not t['findings'] for t in takeover['tasks'])
    card = (path / 'card.md').read_text(encoding='utf-8')
    assert 'ITER10-' + name.upper() + '-20261114' in card
    assert 'status: "TODO"' in card and 'review_status: "PENDING"' in card and 'tdd_verified: false' in card
    assert all('**' + key + '**' in card for key in ('interaction','states','visual','regression'))
    assert not (path.parent / 'escape').exists()
    consumer_summaries.append(dict(name=name, installation=str(installation),
        command_exit_codes=[0,0,2,0], actual_iteration_acceptance='6/6 PASS',
        runner_status=receipt['status'], tree_terminal=receipt['tree_terminal']))

native = read(HERE / 'codex-native-calls.json')
calls_text = normalize('\n'.join(strings(native['calls'])))
outputs_text = normalize('\n'.join(strings(native['outputs'])))
for rel in ['SKILL.md','references/template_generation.md']:
    installed = Path('C:/Users/qingyu/.codex/skills/iteration-manager') / rel
    assert installed.read_text(encoding='utf-8').rstrip() in outputs_text
assert 'scripts/iter_run.py --deadline' in calls_text
assert 'sandbox\\\\continuation' in calls_text or 'sandbox/continuation' in calls_text
docs = read(HERE / 'gemini-native-document-calls.json')['calls']
for rel in ['SKILL.md','references/template_generation.md','references/execution_readiness.md']:
    installed = Path('C:/Users/qingyu/.gemini/config/skills/iteration-manager') / rel
    matching = [c for c in docs if c['args'].get('AbsolutePath') == installed.as_posix()]
    assert matching and matching[0]['status'] == 3
    returned = [normalize(s['text']) for s in matching[0]['payload_strings'] if s['field']=='.14.4']
    assert installed.read_text(encoding='utf-8') in returned
commands = read(HERE / 'gemini-native-calls.json')['calls']
assert any(c['status']==3 and '/.gemini/config/skills/iteration-manager/scripts/iter_run.py --deadline' in c['args'].get('CommandLine','') for c in commands)
result = dict(verified_at=datetime.now(timezone.utc).isoformat(), verdict='PASS',
    payload_source_head=plan['source_head'], files_equal_per_installation=[91,91,91],
    main_tests='493 passed in 410.05s', consumers=consumer_summaries,
    primary_provenance='Codex native JSONL tool calls/outputs; Antigravity native SQLite read/command steps; actual installed docs returned and scripts executed',
    preserved_initial_failure='Codex probe expected nonexistent acceptance_verdict; initial raw1 kept, corrected to review_status, reused valid render/check evidence',
    boundaries=['Explicit-root new-session consumption, not native automatic discovery',
        'Gemini copy consumed by actual new Antigravity session, not Gemini CLI',
        'No real filesystem business lifecycle acceptance added',
        'Maintenance suite runs in Codeg; deployed board test harness remains maintenance docs dependency',
        'No assistant configuration change, push, branch deletion or Worktree cleanup'])
with (HERE / 'verification.json').open('x', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(json.dumps(result, ensure_ascii=False, indent=2))
