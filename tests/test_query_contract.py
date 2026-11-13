"""New fields are tested through the callable legacy entry before extraction."""
import json

import pytest

from iter_autonomy import load_state
from iter_sync import generate_board_data, render_task_envelope


@pytest.mark.parametrize('mode', ['git', 'filesystem'])
@pytest.mark.parametrize('has_checkpoint', [False, True])
def test_legacy_board_exposes_same_handoff_fields(tmp_path, mode, has_checkpoint):
    directory = tmp_path / 'docs/todos/03-contract'
    directory.mkdir(parents=True)
    metadata = dict(schema_version='1', task_id='03', status='IN_PROGRESS', type='Strict-TDD')
    if mode == 'filesystem':
        (directory / 'iteration-delivery.json').write_text(
            json.dumps(dict(schema_version=1, mode=mode)), encoding='utf-8')
        metadata.update(delivery_mode=mode, candidate_id='fs-candidate-a')
    state = load_state(metadata)
    if has_checkpoint:
        state['events']['attempt-a'] = {'input': {'action': 'attempt', 'attempt': {
            'candidate': 'fixed-candidate', 'phase': 'implementation',
            'checkpoint': 'valid old-entry RED', 'remaining_work': ['extract query layer'],
            'progress': [{'kind': 'red', 'evidence': 'red.txt', 'summary': 'assertion failure'}],
            'source': 'attempt.json',
        }}}
    metadata['autonomy_state'] = json.dumps(state)
    card = directory / '03-task.md'
    card.write_text('---\n' + ''.join(f'{key}: {json.dumps(value)}\n' for key, value in metadata.items())
                    + '---\n', encoding='utf-8')
    before = {path: path.read_bytes() for path in directory.iterdir()}
    handoff = render_task_envelope(card, tmp_path)['TASK_HANDOFF']
    board_card = generate_board_data(directory)['cards'][0]
    required = {'delivery_mode', 'candidate_id', 'execution'}
    assert required <= board_card.keys(), f'legacy board missing handoff fields: {required - board_card.keys()}'
    assert {key: board_card[key] for key in required} == {key: handoff[key] for key in required}
    assert board_card['delivery_mode'] == mode
    if mode == 'filesystem':
        assert board_card['candidate_id'] == 'fs-candidate-a'
    execution = board_card['execution']
    if has_checkpoint:
        assert execution['checkpoint']['summary'] == 'valid old-entry RED'
        assert execution['remaining_work'] == ['extract query layer']
    else:
        assert execution['checkpoint'] is None
    assert {path: path.read_bytes() for path in directory.iterdir()} == before
