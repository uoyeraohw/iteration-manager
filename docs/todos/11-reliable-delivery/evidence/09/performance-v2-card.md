---
schema_version: 1
iteration: "example-planning"
task_id: "02"
task_name: "Generated TODO example: improve query latency"
status: "TODO"
type: "Refactor-Benchmark"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "UNASSESSED"
typesafe_evidence: ""
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
---

# 02 · Generated TODO example: improve query latency

## 1. 任务执行目标与接口契约
- **主要目标**：Preserve query behavior and reduce p95 latency at a fixed workload by at least 15 percent.
- **Consumes**：Existing public interfaces and behavior tests
- **Produces**：Stable query results and measured lower p95 latency

## 2. 业务阶段
<!-- iter:stages -->
- [ ] Capture baseline and before
- [ ] Refactor, regress and measure after
- [ ] Freeze for independent review
<!-- /iter:stages -->

## 3. 按类型验证规划
保持行为与接口；按目标选择可重复结构指标或真实性能指标，取得可比benchmark_before/benchmark_after实测；性能目标须记录单位、环境、规模、命令和目标，见references/refactor_evidence.md。
<!-- iter:verification -->
- [ ] **baseline**：Before changes run python -m pytest tests/test_query.py -q to capture current query behavior
- [ ] **regression**：Run python -m pytest tests/test_query.py -q after changes; covers affected query and error paths
- [ ] **compatibility**：Observe public query signatures and results against baseline
- [ ] **benchmark_before**：Run python tools/bench_query.py --rows 10000 --requests 1000 before changes; record commit, hardware, OS, Python, dataset, workload, command and p95 milliseconds
- [ ] **benchmark_after**：Run the identical python tools/bench_query.py --rows 10000 --requests 1000 on the same environment and workload after changes; record commit, p95 milliseconds, percent change and target assessment
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `src/example.py` | MODIFIED | 本任务授权范围 |
| `tests/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] Behavior and exceptions match baseline; independent review required
- [ ] Actual p95 latency in milliseconds improves at least 15 percent under the same environment, dataset and workload
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
