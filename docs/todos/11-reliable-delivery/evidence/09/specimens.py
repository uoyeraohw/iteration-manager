"""Create actual CLI-rendered TODO planning specimens; not business execution."""
import json
import subprocess
import sys
from pathlib import Path

out = Path("docs/todos/11-reliable-delivery/evidence/09")
common = dict(version=1, iteration="example-planning", type="Refactor-Benchmark", delivery_mode="git",
              consumes="Existing public interfaces and behavior tests", scope=["src/example.py", "tests/"],
              stages=["Capture baseline and before", "Refactor, regress and measure after", "Freeze for independent review"])
examples = {
    "structure": dict(task_id="01", task_name="Generated TODO example: reduce dependency edges",
        objective="Preserve public behavior while reducing directed imports between src/example modules; no performance target.",
        produces="Stable public API and fewer directed module dependency edges",
        acceptance=["Behavior and exceptions match baseline; independent review required", "Count distinct directed imports between src/example Python modules by the same AST script before and after; target at most 4 edges"],
        verification={"baseline":"Before changes run python -m pytest tests/test_example.py -q to capture current behavior",
            "regression":"Run python -m pytest tests/test_example.py -q after changes; covers affected public interfaces and exceptions",
            "compatibility":"Observe public signatures and response behavior against baseline",
            "benchmark_before":"Run python tools/count_edges.py src/example before changes; record commit, Python environment, AST counting rules, scope, command and edge count",
            "benchmark_after":"Run the same python tools/count_edges.py src/example after changes with same environment and rules; record commit, count, change and target assessment"}),
    "performance": dict(task_id="02", task_name="Generated TODO example: improve query latency",
        objective="Preserve query behavior and reduce p95 latency at a fixed workload by at least 15 percent.",
        produces="Stable query results and measured lower p95 latency",
        acceptance=["Behavior and exceptions match baseline; independent review required", "Actual p95 latency in milliseconds improves at least 15 percent under the same environment, dataset and workload"],
        verification={"baseline":"Before changes run python -m pytest tests/test_query.py -q to capture current query behavior",
            "regression":"Run python -m pytest tests/test_query.py -q after changes; covers affected query and error paths",
            "compatibility":"Observe public query signatures and results against baseline",
            "benchmark_before":"Run python tools/bench_query.py --rows 10000 --requests 1000 before changes; record commit, hardware, OS, Python, dataset, workload, command and p95 milliseconds",
            "benchmark_after":"Run the identical python tools/bench_query.py --rows 10000 --requests 1000 on the same environment and workload after changes; record commit, p95 milliseconds, percent change and target assessment"})}
for name, specific in examples.items():
    spec = dict(common, **specific)
    sp = out / f"{name}-spec.json"
    card = out / f"{name}-card.md"
    sp.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    render = subprocess.run([sys.executable, "-B", "scripts/iter_templates.py", "--render", str(sp)], capture_output=True, text=True, encoding="utf-8")
    print(f"{name} render exit={render.returncode}", flush=True)
    if render.returncode:
        print(render.stdout, render.stderr, flush=True); sys.exit(render.returncode)
    card.write_text(render.stdout, encoding="utf-8")
    check = subprocess.run([sys.executable, "-B", "scripts/iter_templates.py", "--check", str(card), "--delivery-mode", "git"], capture_output=True, text=True, encoding="utf-8")
    print(f"{name} precheck exit={check.returncode} stdout={check.stdout.strip()} stderr={check.stderr.strip()}", flush=True)
    if check.returncode or json.loads(check.stdout) != {"valid": True, "errors": []}:
        sys.exit(1)
print("Generated TODO examples only; no business commands, measurements or approval executed.")
