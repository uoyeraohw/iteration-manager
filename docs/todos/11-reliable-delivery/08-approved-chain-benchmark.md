---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "08"
task_name: "量测合法Git与FS批准库存的真实成本"
status: "TESTING"
type: "Spike-Discovery"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "82.975"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: "6a54aceb2fc540d20480f9cdb5e5a683359c8e1a"
head_sha: ""
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"iter11-controller-linux-20261115\",\"events\":{\"iter11-08-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"08-approved-chain-benchmark\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:25:52.724421+00:00\"},\"iter11-08-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/08/attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"phase\":\"implementation\",\"candidate\":\"6a54aceb2fc540d20480f9cdb5e5a683359c8e1a\",\"inputs\":[\"docs/todos/11-reliable-delivery/08-approved-chain-benchmark.md\",\"docs/todos/11-reliable-delivery/README.md\",\"AGENTS.md\",\"references/task_card_schema.md\"],\"capabilities\":[\"native-codex-cli-implementer\",\"approved-frozen-linux-runner\",\"Python3.11.17-pytest9.2-mcp1.30\",\"independent-native-reviewer\"],\"version\":1,\"checkpoint\":\"Git/FS各10/100卡逐卡合法审计PASS；四种读取操作各3次量测完成，记录调用数/字节/均值范围及单调用建议，未优化产品\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"executor_id\":\"01a1ddab-6c92-7843-84b6-2302d6156eb0\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/08/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"summary\":\"Git/FS各10/100卡逐卡合法审计PASS；四种读取操作各3次量测完成，记录调用数/字节/均值范围及单调用建议，未优化产品\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/08/delivery.json\"}],\"commands\":[\"docs/todos/11-reliable-delivery/evidence/08/fixture-test-02.json\",\"docs/todos/11-reliable-delivery/evidence/08/experiment-01.json\",\"docs/todos/11-reliable-delivery/evidence/08/delivery-validation-01.json\",\"docs/todos/11-reliable-delivery/evidence/08/artifact-validation-01.json\",\"docs/todos/11-reliable-delivery/evidence/08/fixture-test-01.json\",\"docs/todos/11-reliable-delivery/evidence/08/fixture-test-03.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/11-reliable-delivery/evidence/08/attempt.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"6a54aceb2fc540d20480f9cdb5e5a683359c8e1a\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/08-approved-chain-benchmark.md\",\"docs/todos/11-reliable-delivery/README.md\",\"references/task_card_schema.md\"],\"capabilities\":[\"Python3.11.17-pytest9.2-mcp1.30\",\"approved-frozen-linux-runner\",\"independent-native-reviewer\",\"native-codex-cli-implementer\"],\"scope\":[\".agents/notes/planned/iter11/08-approved-chain-benchmark.md\",\"docs/todos/11-reliable-delivery/evidence/08/\",\"tests/benchmarks/\",\"tests/test_approval_benchmark_fixture.py\"]},\"executor_id\":\"01a1ddab-6c92-7843-84b6-2302d6156eb0\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/08/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/08/delivery.json\",\"summary\":\"Git/FS各10/100卡逐卡合法审计PASS；四种读取操作各3次量测完成，记录调用数/字节/均值范围及单调用建议，未优化产品\"}],\"checkpoint\":\"Git/FS各10/100卡逐卡合法审计PASS；四种读取操作各3次量测完成，记录调用数/字节/均值范围及单调用建议，未优化产品\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"commands\":[{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/08/artifact-validation-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:30:01.437371+00:00\",\"ended_at\":\"2026-11-15T05:30:01.499593+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/08/delivery-validation-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:30:31.251656+00:00\",\"ended_at\":\"2026-11-15T05:30:31.311951+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/08/experiment-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:27:40.733421+00:00\",\"ended_at\":\"2026-11-15T05:29:27.887175+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/08/fixture-test-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-15T05:26:59.506164+00:00\",\"ended_at\":\"2026-11-15T05:27:01.222354+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/08/fixture-test-02.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:27:17.676632+00:00\",\"ended_at\":\"2026-11-15T05:27:20.357611+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/08/fixture-test-03.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:27:31.088256+00:00\",\"ended_at\":\"2026-11-15T05:27:33.761206+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":114.34639}},\"result\":{\"task_id\":\"08-approved-chain-benchmark\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:31:37.003721+00:00\"},\"iter11-08-release-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/08/implementation-terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"08-approved-chain-benchmark\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:31:37.089618+00:00\"},\"iter11-08-review-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"08-approved-chain-benchmark\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:31:37.207291+00:00\"}},\"blocked_reason\":\"\"}"
updated_at: "2026-11-15T05:31:37.207411+00:00"
---

# 08 · 量测合法Git与FS批准库存的真实成本

## 1. 任务执行目标与接口契约
- **主要目标**：先建立合法收据、Git绑定和FS快照均实际PASS的代表库存，再量测查询/盘点/HTTP证据路径，定位单次调用内重复工作，不预设优化收益。
- **Consumes**：任务01合法模式解析；现有test_filesystem_delivery_controller/执行就绪/Git临时夹具；audit_task_file、generate_board_data、render_task_envelope、inventory及LiveBoardHandler。07测试支持提取不是功能前提。
- **Produces**：tests/benchmarks/approval_chain.py: main(argv=None) -> int；CLI --sizes 10 100 --repeats 3 --output PATH，输出环境/候选/工作负载/各次秒数/Git调用数/读取字节/批准卡数/限制。tests/test_approval_benchmark_fixture.py验证样例真实性。

## 2. 业务阶段
<!-- iter:stages -->
- [x] 构造Git/FS合法批准库存，先断言每卡审计PASS
- [x] 分层量测10/100卡各3次并保留原始数据
- [x] 按单次调用剖析给出优化或维持现状的决策和后续接口
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [x] **experiment**：python -B tests/benchmarks/approval_chain.py --sizes 10 100 --repeats 3 --output docs/todos/11-reliable-delivery/evidence/08/measurements.json；先确认合法Git/FS库存每卡PASS，通过冻结runner。
- [x] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [x] **interfaces**：tests/benchmarks/approval_chain.py: main(argv=None) -> int；CLI --sizes 10 100 --repeats 3 --output PATH，输出环境/候选/工作负载/各次秒数/Git调用数/读取字节/批准卡数/限制。tests/test_approval_benchmark_fixture.py验证样例真实性。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `tests/benchmarks/` | MODIFIED | 本任务授权范围 |
| `tests/test_approval_benchmark_fixture.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/08-approved-chain-benchmark.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/08/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 分别构造10/100卡Git与FS已批准样例；每张DONE均有合法类型checks/原始输出/报告及真实绑定，量测前accepted必须等于卡数；不得用缺收据的快路径代替。
- [ ] 分别记录一次board、全部envelope、一次inventory及实际HTTP证据读取的成本，样例构造不计时；真实Git执行及FS字节比较不替换成成功桩。
- [ ] 相同候选/环境/数据量至少3次，给出逐次值、均值和范围；记录硬件/Python/Git/平台、源码候选及样例限制，不从3次样本推断可靠尾延迟。
- [ ] 分析仅提出基于证据的单次调用复用机会；不实现跨调用验收缓存，不以合成性能证明真实外部业务PASS，不附带未评估的优化改码。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。

2026-11-15T05:31:37.112372+00:00：Git/FS各10/100卡逐卡合法审计PASS；四种读取操作各3次量测完成，记录调用数/字节/均值范围及单调用建议，未优化产品；原生实现会话01a1ddab-6c92-7843-84b6-2302d6156eb0和命令树已确认终态。原始证据/source manifest/type checks已核对，冻结C后独审，非整轮批准。

# Task 08 decision and ledger material — 2026-11-15 UTC

Decision: retain the current product implementation. This is a measurement spike; no optimization or cross-call acceptance cache was implemented. The candidate observed was Git HEAD `6a54aceb2fc540d20480f9cdb5e5a683359c8e1a` plus the uncommitted source hashes recorded in `measurements.json` and `source-manifest.json`. No future implementation commit is asserted.

The synthetic workloads adapt `tests/test_completion_gates.py::make_reviewed_candidate` and `tests/test_filesystem_delivery_controller.py::fixture`: independent per-card scopes, real Git C/registration histories or filesystem manifests and byte snapshots, frozen cards/goals, check outputs and review reports. All receipts, reports, commands and approvals in those workloads are synthetic: they do not claim real execution, independent human review or business acceptance. Every audit had to return PASS and the untimed board accepted count had to equal size before any trial. The retained temporary workload roots are in measurements.

| Mode | Cards / accepted | Operation | Mean seconds | Range seconds | Git calls per trial | Path-read bytes per trial |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| git | 10 / 10 | board | 0.5579 | 0.5367–0.5797 | 221,221,221 | 36360,36360,36360 |
| git | 10 / 10 | all_envelopes | 0.6737 | 0.6118–0.7363 | 250,250,250 | 24830,24830,24830 |
| git | 10 / 10 | inventory | 0.6469 | 0.6090–0.6690 | 260,260,260 | 31070,31070,31070 |
| git | 10 / 10 | http_evidence | 0.5618 | 0.5546–0.5658 | 222,222,222 | 36427,36427,36427 |
| git | 100 / 100 | board | 6.0656 | 6.0288–6.1262 | 2201,2201,2201 | 363600,363600,363600 |
| git | 100 / 100 | all_envelopes | 6.7058 | 6.5659–6.8386 | 2500,2500,2500 | 248300,248300,248300 |
| git | 100 / 100 | inventory | 7.2009 | 6.9934–7.3303 | 2600,2600,2600 | 310700,310700,310700 |
| git | 100 / 100 | http_evidence | 5.9955 | 5.8173–6.1178 | 2202,2202,2202 | 363667,363667,363667 |
| filesystem | 10 / 10 | board | 0.0242 | 0.0238–0.0248 | 0,0,0 | 55610,55610,55610 |
| filesystem | 10 / 10 | all_envelopes | 0.0209 | 0.0203–0.0215 | 0,0,0 | 42750,42750,42750 |
| filesystem | 10 / 10 | inventory | 0.0235 | 0.0228–0.0241 | 0,0,0 | 49010,49010,49010 |
| filesystem | 10 / 10 | http_evidence | 0.0273 | 0.0236–0.0314 | 0,0,0 | 55727,55727,55727 |
| filesystem | 100 / 100 | board | 0.2529 | 0.2304–0.2689 | 0,0,0 | 555650,555650,555650 |
| filesystem | 100 / 100 | all_envelopes | 0.2084 | 0.2034–0.2122 | 0,0,0 | 427500,427500,427500 |
| filesystem | 100 / 100 | inventory | 0.2726 | 0.2566–0.2911 | 0,0,0 | 490100,490100,490100 |
| filesystem | 100 / 100 | http_evidence | 0.2387 | 0.2359–0.2434 | 0,0,0 | 555767,555767,555767 |

Each comma-separated count is an actual trial; in this sample each count and byte value was constant, so its mean and range equal that value. The inventory was BLOCKED for completed cards, while its acceptance verdicts were PASS: readiness and acceptance are separate. Fixture construction, the pretrial audit, board acceptance check, HTTP server startup/shutdown and source hashing were excluded. Time includes actual operation, assertions and, for HTTP, the stdlib client request and full body read; the handler first generates the complete board. Git counts are launched Git subprocesses, not simulated calls. Bytes count only bytes returned by `Path.read_bytes` and UTF-8 encoded text returned by `Path.read_text`; they include FS source/snapshot reads, but exclude Git subprocess reads, other Python I/O, kernel I/O and socket traffic. No browser or UI interaction was measured.

The Git 100-card board launched 2201 Git processes per trial, and HTTP launched 2202; the latter handler generates the board before reading evidence. `scripts/iter_contracts.py::validate_binding` resolves base/head/contract independently and reads both contract and head versions of card and goal; this workload deliberately uses the same commit for head and contract. Those are concrete within-call repetition candidates, but this experiment does not isolate their cost or prove a speedup. `iter_inventory.inventory` already reuses audits inside one inventory call. A future change could investigate invocation-local reuse keyed by resolved immutable commit and path, preserving separate error handling, working-tree drift, mutable inputs and all binding/compatibility tests; establish a controlled before/after on the same fixture before adopting it. No reuse across calls is proposed.

Limits: three samples characterize these runs only and do not establish robust tail latency, production load, human approval, other platforms, real external business completion, or a comparison to task 07. Git and FS workloads have different binding mechanisms and are not an equivalence or speedup experiment. The code uses synthetic Spike cards and simple small files, on the recorded Linux 4-vCPU AMD EPYC VM, Python 3.11.17 and Git 2.47.3; `measurements.json` has precise environment and all individual timings.

Interfaces for a future consumer: `tests/benchmarks/approval_chain.py:main(argv=None) -> int`, `--sizes <positive integers> --repeats <positive integer> --output PATH`, and JSON fields `environment`, `base`, `source_sha256`, `definitions`, `workloads[].approved_count`, and `workloads[].operations[].trials`. Count definitions and limitations must travel with results. Context is synthetic; no new FS recovery or platform support is implied.

Evidence: `fixture-test-01.json` and raw output preserve the initial two Git failures caused by a shared multi-card candidate; `fixture-test-03.json` and raw output record 4 passing tests after per-card commits, including real source drift rejection and neighbor preservation in both modes. `experiment-01.json` and raw output record the complete matrix, exit 0 and terminal tree. No fake TDD RED is claimed for this Spike. Independent candidate C, review of C and frozen specification, registration D, and frozen local strict remain with the controller; this document is material for the existing card ledger, not a new state ledger.

<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：01；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/08/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
