"""Validate task 09 handoff artifacts without claiming independent consumption."""
import hashlib
import json
import os
import sys
from pathlib import Path

p = Path('docs/todos/11-reliable-delivery/evidence/09')
manifest = json.loads((p / 'source-manifest.json').read_text())
assert set(manifest) == {'sha256'}
for path, expected in manifest['sha256'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
consumer = json.loads((p / 'consumer-input-manifest.json').read_text())
for path, expected in consumer['sha256'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
assert 'PENDING' in consumer['status']
delivery = json.loads((p / 'delivery.json').read_text())
assert delivery['thread_id'] == os.environ['CODEX_THREAD_ID']
assert delivery['candidate']['base'] == '531c3ea6e31d2eb2a098272bfcf6cb6fe57a11b7'
for item in delivery['commands']:
    receipt = json.loads(Path(item['receipt']).read_text())
    assert receipt['status'] == 'COMPLETED' and receipt['raw_exit_code'] == 0 and receipt['tree_terminal'] is True
    assert Path(item['raw_output']).stat().st_size > 0
checks = json.loads((p / 'checks-proposal.json').read_text())
assert [(x['name'], x['kind']) for x in checks] == [('experiment','command'),('decision','observation'),('interfaces','observation')]
assert checks[0]['cwd'] == '.' and checks[0]['exit_code'] == 0
assert all(Path(x['output']).stat().st_size > 0 for x in checks)
sys.path.insert(0, 'scripts')
from iter_contracts import TYPE_CHECKS
from iter_templates import render_task_card, validate_generated_card
assert len(TYPE_CHECKS) == 4
assert tuple(TYPE_CHECKS['Refactor-Benchmark']) == ('baseline','regression','compatibility','benchmark_before','benchmark_after')
for name in ('structure','performance'):
    spec = json.loads((p / f'{name}-v2-spec.json').read_text())
    card = (p / f'{name}-v2-card.md').read_text()
    assert card == render_task_card(spec) and validate_generated_card(card, 'git') == []
    assert set(spec['verification']) == set(TYPE_CHECKS['Refactor-Benchmark'])
print('PASS: hashes, original runner receipts and raw output, check proposal, exact type keys, and rendered specimens verified; consumer pending')
