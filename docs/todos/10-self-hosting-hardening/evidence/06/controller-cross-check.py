"""Controller validation: compare fixed coordinator and candidate read-only handoffs."""
import json, os, subprocess, sys
from pathlib import Path
root=Path.cwd()
sys.path.insert(0,str(root/'scripts'))
from iter_queries import audit_task_file, render_task_envelope
directory=root/'docs/todos/10-self-hosting-hardening'
frozen='C:/Users/qingyu/.codeg/skills/iteration-manager/build/frozen-tools/46ded3a/scripts/iter_sync.py'
rows=[]
for card in sorted(directory.glob('[0-9][0-9]-*.md')):
    p=subprocess.run([sys.executable,'-B',frozen,'--render-envelope',str(card),str(root)],capture_output=True,text=True,encoding='utf8',env={**os.environ,'PYTHONIOENCODING':'utf8'})
    assert p.returncode==0,(card.name,p.stdout,p.stderr)
    old=json.loads(p.stdout)['TASK_HANDOFF']
    new=render_task_envelope(card,root)['TASK_HANDOFF']
    audit=audit_task_file(card)
    for key in ('task_id','status','commit_sha','base_sha','acceptance_verdict','writer','fix_rounds','fix_total','consilium_count','replan_count','blocked_reason','delivery_mode','candidate_id','execution'):
        assert old[key]==new[key],(card.name,key,old[key],new[key])
    assert audit['verdict']==new['acceptance_verdict']
    rows.append(dict(task=new['task_id'],status=new['status'],acceptance=audit['verdict'],head=new['commit_sha'],checkpoint=new['execution']['checkpoint']))
assert [r['acceptance'] for r in rows]==['PASS']*5+['UNKNOWN']
print(json.dumps(dict(version=1,candidate=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),fixed_tool=frozen,comparison='audit and handoff identity/status/binding/budget/execution',rows=rows,result='PASS'),ensure_ascii=False,indent=2))
