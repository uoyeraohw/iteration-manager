import json

from test_session_timing import cli, write, stamp


def test_zero_observations_separates_record_integrity_from_coverage(tmp_path):
    assert cli(tmp_path, '--timing-init', 'trace.jsonl', 'session').returncode == 0
    proc = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    row = data['categories']['review']
    assert row['count'] == 0 and row['complete'] is True
    assert row['recorded_intervals_complete'] is True
    assert row['full_activity_coverage'] == 'UNKNOWN'


def test_one_complete_record_does_not_establish_full_coverage(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'session')
    write(tmp_path, 'event.json', dict(type='activity', category='review', operation='audit', target='task',
                                       started_at=stamp(1), ended_at=stamp(2), clock_basis='local_utc'))
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'event.json').returncode == 0
    row = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)['categories']['review']
    assert row['count'] == 1 and row['complete'] is True and row['recorded_intervals_complete'] is True
    assert row['full_activity_coverage'] == 'UNKNOWN'


def test_incomplete_interval_does_not_claim_recorded_completeness(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'session')
    write(tmp_path, 'event.json', dict(type='activity', category='review', operation='audit', target='task',
                                       started_at=stamp(1), ended_at=None, clock_basis='local_utc'))
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'event.json').returncode == 0
    row = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)['categories']['review']
    assert row['count'] == 1 and row['known_count'] == 0
    assert row['complete'] is False and row['recorded_intervals_complete'] is False
    assert row['full_activity_coverage'] == 'UNKNOWN'


def test_report_errors_preserve_legacy_complete_and_unknown_coverage(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'session')
    with (tmp_path/'trace.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(dict(type='finish', id='missing', ended_at=stamp(2)))+'\n')
    proc = cli(tmp_path, '--timing-report', 'trace.jsonl')
    data = json.loads(proc.stdout)
    assert proc.returncode == 2 and data['errors']
    assert all(not row['complete'] and not row['recorded_intervals_complete']
               and row['full_activity_coverage'] == 'UNKNOWN' for row in data['categories'].values())


def test_incomparable_category_clocks_and_report_read_only(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'session')
    for i, basis in enumerate(('host-a', 'host-b')):
        write(tmp_path, f'event{i}.json', dict(type='activity', category='review', operation='audit',
              target=str(i), started_at=stamp(i + 1), ended_at=stamp(i + 2), clock_basis=basis))
        assert cli(tmp_path, '--timing-import', 'trace.jsonl', f'event{i}.json').returncode == 0
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir() if p.is_file()}
    proc = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert proc.returncode == 0
    rows = json.loads(proc.stdout)['categories']
    assert rows['review']['complete'] is False
    assert rows['review']['recorded_intervals_complete'] is False
    assert rows['review']['full_activity_coverage'] == 'UNKNOWN'
    assert rows['inventory']['complete'] is True and rows['inventory']['recorded_intervals_complete'] is True
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir() if p.is_file()}
