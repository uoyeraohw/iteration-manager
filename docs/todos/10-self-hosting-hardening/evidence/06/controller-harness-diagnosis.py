import json,subprocess,sys,tempfile,time
from pathlib import Path
root=Path.cwd()
with tempfile.TemporaryDirectory(prefix='iter06-harness-diagnosis-') as d:
    ready,stop=Path(d)/'ready.json',Path(d)/'stop'
    args=[sys.executable,'-B',str(root/'docs/todos/10-self-hosting-hardening/evidence/04/browser_harness.py'),'--ready-file',str(ready),'--stop-file',str(stop),'--duration','12','--delay','.2']
    start=time.monotonic()
    p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    while not ready.exists() and p.poll() is None and time.monotonic()-start<35:
        time.sleep(.05)
    elapsed=time.monotonic()-start
    stop.touch()
    out,err=p.communicate(timeout=15)
    print(json.dumps(dict(candidate=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),argv=args,ready=ready.exists(),ready_seconds=elapsed,exit=p.returncode,stdout=out.decode('utf8',errors='replace'),stderr=err.decode('utf8',errors='replace')),ensure_ascii=False,indent=2))
    assert ready.exists(),err
    assert p.returncode==0,err
