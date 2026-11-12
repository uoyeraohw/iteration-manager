import io
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from iter_sync import parse_task_stages_and_micro_state,generate_board_data,build_html_dashboard,render_terminal_board,sync_local_iteration


def test_checklist_overrides_stale_frontmatter_without_inferred_progress():
    text = '---\nstatus: DONE\nstage_current: bogus\nstage_progress: 100%\n---\n<!-- iter:stages -->\n- [x] Stage A\n- [ ] Stage B\n<!-- /iter:stages -->\nRuling: naming correction\n'
    state = parse_task_stages_and_micro_state(text,'DONE')
    assert state['stage_pct'] == 50
    assert state['stage_current'] == 'Stage B'
    assert state['replan_count'] == 0


def test_no_checklist_is_unknown_even_when_declared_done():
    state = parse_task_stages_and_micro_state('---\nstatus: DONE\n---\n','DONE')
    assert state['stage_pct'] is None
    assert state['stage_progress'] == 'UNKNOWN'
    assert state['tdd_step'] == 'UNKNOWN'


def test_legacy_done_never_becomes_accepted_in_any_projection(tmp_path):
    (tmp_path/'01.md').write_text('---\nstatus: DONE\ntask_name: Missing evidence\n---\n',encoding='utf-8')
    (tmp_path/'README.md').write_text('> **进度指示**：old\n',encoding='utf-8')
    data=generate_board_data(tmp_path)
    assert data['done'] == 1
    assert data.get('accepted') == 0
    assert data['cards'][0].get('acceptance_verdict') == 'UNKNOWN'
    stream=io.StringIO(); render_terminal_board(tmp_path,stream)
    assert 'UNKNOWN' in stream.getvalue() and 'APPROVED' not in stream.getvalue()
    sync_local_iteration(tmp_path)
    assert '验收PASS' in (tmp_path/'README.md').read_text(encoding='utf-8')


def test_script_terminator_and_task_text_never_enter_html_sink(tmp_path):
    payload='</script><img src=x onerror=alert(1)> & "'
    (tmp_path/'01.md').write_text('---\nstatus: TODO\ntask_name: '+json.dumps(payload)+'\n---\n',encoding='utf-8')
    data=generate_board_data(tmp_path); data['iteration_name']=payload
    html=build_html_dashboard(data)
    assert payload not in html
    assert 'innerHTML' not in html
    assert '\\u003c/script' in html
