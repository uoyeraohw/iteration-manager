"""Executable template unit tests; not native browser acceptance evidence."""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from iter_sync import build_html_dashboard, generate_board_data


def template_render(data, expression):
    script = re.findall(r'<script>(.*?)</script>', build_html_dashboard(data), re.S)[0]
    # Minimal DOM boundary for text rendering, not a browser or interaction claim.
    harness = r'''
class Element {
 constructor(tag){this.tag=tag;this.children=[];this.dataset={};this.textContent='';}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=nodes;}
 setAttribute(k,v){this[k]=v;}
 remove(){}
 showModal(){this.open=true;}
 close(){this.open=false;}
}
const nodes={};
const document={getElementById(id){return nodes[id]??=new Element(id);},
 createElement(tag){return new Element(tag);},querySelectorAll(){return nodes.filters.children;}};
const location={protocol:'file:'};
document.getElementById('board-data').textContent=JSON.stringify(DATA);
function flatten(n){return [n.textContent,...n.children.map(flatten)].join('\n');}
'''.replace('DATA', json.dumps(data, ensure_ascii=False))
    result = subprocess.run(['node', '-e', harness + script + '\n' + expression],
                            capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize('mode', ['git', 'filesystem', 'UNKNOWN'])
def test_mode_specific_candidate_and_historical_checkpoint(tmp_path, mode):
    (tmp_path / '01.md').write_text('---\nstatus: IN_PROGRESS\n---\n', encoding='utf-8')
    data = generate_board_data(tmp_path)
    data['cards'][0].update(delivery_mode=mode, candidate_id='synthetic-fs-current',
        base_sha='base-original', head_sha='git-current', execution={
            'checkpoint': {'candidate': 'historical-candidate', 'phase': 'implementation',
                'summary': 'valid checkpoint', 'source': 'attempt-original.json',
                'progress': [{'kind': 'red', 'evidence': 'original-red.txt', 'summary': 'assertion failed'}]},
            'remaining_work': ['native browser acceptance']})
    text = template_render(data, "openDetail(data.cards[0]);console.log(JSON.stringify(flatten(nodes['detail-content'])));")
    if mode == 'filesystem':
        assert 'candidate_id synthetic-fs-current' in text
        assert 'BASE ' not in text and '实现C ' not in text
    elif mode == 'git':
        assert 'BASE base-original' in text and '实现C git-current' in text
        assert 'synthetic-fs-current' not in text
    else:
        assert 'UNKNOWN · 交付模式未知' in text
        assert 'git-current' not in text and 'synthetic-fs-current' not in text
    for value in ('historical-candidate', 'attempt-original.json', 'original-red.txt',
                  'assertion failed', 'native browser acceptance'):
        assert value in text


def test_missing_checkpoint_and_empty_remaining_do_not_imply_completion(tmp_path):
    (tmp_path / '01.md').write_text('---\nstatus: TODO\n---\n', encoding='utf-8')
    data = generate_board_data(tmp_path)
    text = template_render(data, "openDetail(data.cards[0]);console.log(JSON.stringify(flatten(nodes['detail-content'])));")
    assert 'UNKNOWN · 无有效检查点记录' in text
    assert '未列出剩余工作；不代表任务完成' in text


def test_html_exact_counts_are_rendered_not_just_embedded(tmp_path):
    from test_filesystem_delivery_controller import fixture
    card, _, _ = fixture(tmp_path)
    (card.parent / '02.md').write_text('---\nstatus: DONE\n---\n', encoding='utf-8')
    data = generate_board_data(card.parent)
    assert (data['done'], data['accepted'], data['total']) == (2, 1, 2)
    assert template_render(data, "console.log(JSON.stringify([nodes.declared.textContent,nodes.accepted.textContent]));") == ['2 / 2', '1 / 2']


@pytest.mark.parametrize('isolated', [True, False])
def test_browser_harness_isolated_mode_never_reads_checkout(tmp_path, monkeypatch, capsys, isolated):
    import importlib.util

    script = Path(__file__).resolve().parents[1] / 'docs/todos/10-self-hosting-hardening/evidence/04/browser_harness.py'
    spec = importlib.util.spec_from_file_location('isolated_browser_harness', script)
    harness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(harness)
    if not isolated:
        checkout = tmp_path / 'checkout'
        iteration = checkout / 'docs/todos/10-self-hosting-hardening'
        iteration.mkdir(parents=True)
        (iteration / '01.md').write_text('---\nstatus: TODO\n---\n', encoding='utf-8')
        monkeypatch.setattr(harness, 'ROOT', checkout)
    ready, stop = tmp_path / 'ready.json', tmp_path / 'stop'
    monkeypatch.setattr(sys, 'argv', [str(script), '--ready-file', str(ready),
        '--stop-file', str(stop), '--duration', '.01', '--delay', '0'] +
        (['--isolated-fixtures'] if isolated else []))
    original = harness.generate_board_data
    visited = []

    def fixture_only(directory):
        if isolated:
            assert not directory.is_relative_to(harness.ROOT), 'isolated mode read checkout inventory'
        visited.append(directory)
        return original(directory)

    monkeypatch.setattr(harness, 'generate_board_data', fixture_only)
    harness.main()
    info = json.loads(ready.read_text(encoding='utf-8'))
    assert len(visited) == 4
    git_name = 'synthetic_git' if isolated else 'real_git'
    assert set(info['services']) == {git_name, 'synthetic_fs', 'synthetic_empty', 'synthetic_loading'}
    assert info['services'][git_name]['synthetic'] is isolated
    if not isolated:
        assert Path(info['services']['real_git']['iter_dir']) == iteration
    assert all(directory.is_relative_to(Path(info['synthetic_root']))
               for directory in visited if isolated or directory != iteration)
    assert not Path(info['synthetic_root']).exists()
    assert json.loads(capsys.readouterr().out.splitlines()[-1])['active_commands'] == []


def test_browser_http_harness_lifecycle_and_synthetic_provenance(tmp_path):
    import http.client
    import time
    script = Path(__file__).resolve().parents[1] / 'docs/todos/10-self-hosting-hardening/evidence/04/browser_harness.py'
    ready, stop = tmp_path/'ready.json', tmp_path/'stop'
    process = subprocess.Popen([sys.executable, '-B', str(script), '--ready-file', str(ready),
        '--stop-file', str(stop), '--duration', '12', '--delay', '.2', '--isolated-fixtures'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        end = time.monotonic()+8
        while not ready.exists() and process.poll() is None and time.monotonic()<end:
            time.sleep(.05)
        assert ready.exists(), 'Harness failed to publish ready JSON'
        info=json.loads(ready.read_text(encoding='utf-8'))
        assert 'real_git' not in info['services']
        assert len(info['services']) == 4
        assert all(service['synthetic'] for service in info['services'].values())
        assert all(Path(service['iter_dir']).is_relative_to(Path(info['synthetic_root']))
                   for service in info['services'].values())
        assert info['services']['synthetic_empty']['total']==0
        for name in ('synthetic_fs', 'synthetic_loading'):
            service=info['services'][name]
            connection=http.client.HTTPConnection('127.0.0.1', service['port'], timeout=4)
            started=time.monotonic(); connection.request('GET','/api/board')
            response=connection.getresponse(); data=json.loads(response.read()); connection.close()
            assert response.status==200
            if name=='synthetic_loading':
                assert time.monotonic()-started>=.18
            card=data['cards'][0]
            assert card['delivery_mode']=='filesystem'
            assert card['candidate_id']=='synthetic-fs-current-a'
            assert card['execution']['checkpoint']['candidate']=='synthetic-fs-original-a'
            assert card['execution']['remaining_work']
            assert len(card['sources'])==3
        service=info['services']['synthetic_fs']
        connection=http.client.HTTPConnection('127.0.0.1',service['port'],timeout=4)
        connection.request('GET','/api/evidence?task=01-task.md&source=2')
        response=connection.getresponse()
        assert response.status==200 and b'SYNTHETIC' in response.read()
        connection.close()
        Path(service['stop_file']).touch()
        stop.touch()
        stdout,stderr=process.communicate(timeout=5)
        assert process.returncode==0, stderr.decode()
        assert json.loads(stdout.decode('utf-8').splitlines()[-1])['active_commands']==[]
        assert not Path(info['synthetic_root']).exists()
    finally:
        stop.touch(exist_ok=True)
        if process.poll() is None:
            process.communicate(timeout=5)
