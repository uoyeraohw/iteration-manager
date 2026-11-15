---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "10"
task_name: "核验跨模块故障路径的一致性"
status: "DONE"
type: "Spike-Discovery"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "80.525"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "APPROVED"
review_receipt: "docs/todos/11-reliable-delivery/evidence/10/review-receipt.json"
base_sha: "40d76d4456261a41bf1b67106becad17ecc28e29"
head_sha: "e237a068fb39d21cd80b68a12dfe9cc0d4d21827"
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"\",\"events\":{\"iter11-10-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"10-integration-fault-paths\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:39:55.322575+00:00\"},\"iter11-10-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/10/attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"phase\":\"implementation\",\"candidate\":\"40d76d4456261a41bf1b67106becad17ecc28e29\",\"inputs\":[\"docs/todos/11-reliable-delivery/10-integration-fault-paths.md\",\"docs/todos/11-reliable-delivery/README.md\",\"AGENTS.md\",\"references/task_card_schema.md\",\"tests/test_self_hosting.py\"],\"capabilities\":[\"native-codex-cli-implementer\",\"approved-frozen-linux-runner\",\"Python3.11.17-pytest9.2-mcp1.30\",\"independent-native-reviewer\"],\"version\":1,\"checkpoint\":\"隔离跨模块实验130通过，payload相关11通过，Git漂移5通过；真实原生链与批准分层，不改产品\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"executor_id\":\"01a1ddb8-4209-7662-991e-fcf18f1a74a2\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/10/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"summary\":\"隔离跨模块实验130通过，payload相关11通过，Git漂移5通过；真实原生链与批准分层，不改产品\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/10/delivery.json\"}],\"commands\":[\"docs/todos/11-reliable-delivery/evidence/10/experiment-02.json\",\"docs/todos/11-reliable-delivery/evidence/10/experiment-01.json\",\"docs/todos/11-reliable-delivery/evidence/10/git-drift-01.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/11-reliable-delivery/evidence/10/attempt.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"40d76d4456261a41bf1b67106becad17ecc28e29\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/10-integration-fault-paths.md\",\"docs/todos/11-reliable-delivery/README.md\",\"references/task_card_schema.md\",\"tests/test_self_hosting.py\"],\"capabilities\":[\"Python3.11.17-pytest9.2-mcp1.30\",\"approved-frozen-linux-runner\",\"independent-native-reviewer\",\"native-codex-cli-implementer\"],\"scope\":[\".agents/notes/planned/iter11/10-integration-fault-paths.md\",\"docs/todos/11-reliable-delivery/evidence/10/\",\"tests/test_self_hosting.py\"]},\"executor_id\":\"01a1ddb8-4209-7662-991e-fcf18f1a74a2\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/10/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/10/delivery.json\",\"summary\":\"隔离跨模块实验130通过，payload相关11通过，Git漂移5通过；真实原生链与批准分层，不改产品\"}],\"checkpoint\":\"隔离跨模块实验130通过，payload相关11通过，Git漂移5通过；真实原生链与批准分层，不改产品\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"commands\":[{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/10/experiment-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-15T05:40:42.580114+00:00\",\"ended_at\":\"2026-11-15T05:40:54.742126+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/10/experiment-02.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:41:10.684787+00:00\",\"ended_at\":\"2026-11-15T05:41:25.958122+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/10/git-drift-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:41:47.624085+00:00\",\"ended_at\":\"2026-11-15T05:41:48.838821+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":28.650083}},\"result\":{\"task_id\":\"10-integration-fault-paths\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:43:08.414050+00:00\"},\"iter11-10-release-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/10/implementation-terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"10-integration-fault-paths\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:43:08.485408+00:00\"},\"iter11-10-review-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"10-integration-fault-paths\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:43:08.566076+00:00\"},\"iter11-10-review-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"build/iter11-review/task10-review1/attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"phase\":\"evidence-inspection\",\"candidate\":\"e237a068fb39d21cd80b68a12dfe9cc0d4d21827\",\"inputs\":[\"docs/todos/11-reliable-delivery/10-integration-fault-paths.md\",\"docs/todos/11-reliable-delivery/README.md\",\"AGENTS.md\",\"references/task_card_schema.md\",\"tests/test_self_hosting.py\"],\"capabilities\":[\"native-codex-cli-implementer\",\"approved-frozen-linux-runner\",\"Python3.11.17-pytest9.2-mcp1.30\",\"independent-native-reviewer\"],\"version\":1,\"checkpoint\":\"独立Spec/Quality APPROVED\",\"remaining_work\":[\"D/冻结strict\"],\"executor_id\":\"01a1ddbb-385e-7642-9401-db08c0912af1\",\"terminal_evidence\":\"build/iter11-review/task10-review1/terminal.json\",\"progress\":[{\"kind\":\"review-finding\",\"summary\":\"独立候选APPROVED\",\"evidence\":\"build/iter11-review/task10-review1/report.json\"}],\"commands\":[\"build/iter11-review/task10-review1/scope-runner.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"build/iter11-review/task10-review1/attempt.json\",\"phase\":\"evidence-inspection\",\"delivery_mode\":\"git\",\"candidate\":\"e237a068fb39d21cd80b68a12dfe9cc0d4d21827\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/10-integration-fault-paths.md\",\"docs/todos/11-reliable-delivery/README.md\",\"references/task_card_schema.md\",\"tests/test_self_hosting.py\"],\"capabilities\":[\"Python3.11.17-pytest9.2-mcp1.30\",\"approved-frozen-linux-runner\",\"independent-native-reviewer\",\"native-codex-cli-implementer\"],\"scope\":[\".agents/notes/planned/iter11/10-integration-fault-paths.md\",\"docs/todos/11-reliable-delivery/evidence/10/\",\"tests/test_self_hosting.py\"]},\"executor_id\":\"01a1ddbb-385e-7642-9401-db08c0912af1\",\"executor_state\":\"completed\",\"terminal_evidence\":\"build/iter11-review/task10-review1/terminal.json\",\"progress\":[{\"kind\":\"review-finding\",\"evidence\":\"build/iter11-review/task10-review1/report.json\",\"summary\":\"独立候选APPROVED\"}],\"checkpoint\":\"独立Spec/Quality APPROVED\",\"remaining_work\":[\"D/冻结strict\"],\"commands\":[{\"receipt\":\"build/iter11-review/task10-review1/scope-runner.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T05:43:25.540659+00:00\",\"ended_at\":\"2026-11-15T05:43:25.652808+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":0.112149}},\"result\":{\"task_id\":\"10-integration-fault-paths\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:46:01.809241+00:00\"},\"iter11-10-review-release-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"build/iter11-review/task10-review1/terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"10-integration-fault-paths\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T05:46:01.885594+00:00\"}},\"blocked_reason\":\"\"}"
updated_at: "2026-11-15T05:46:01.903446+00:00"
---

# 10 · 核验跨模块故障路径的一致性

## 1. 任务执行目标与接口契约
- **主要目标**：组合已完成模块的隔离夹具，锁定错误在派发、事件、交接和审计之间不被抹平；只补跨模块回归，不重复各卡完整测试或承担真实链审计。
- **Consumes**：01模式矩阵、02坏卡隔离、03异步守卫、06安装清单及07测试支持接口；现有tests/test_self_hosting.py及执行就绪/FS/Git夹具。
- **Produces**：tests/test_self_hosting.py受影响联合断言与evidence/10/integration-report.json；报告仅synthetic层，不产生原生验收或批准。

## 2. 业务阶段
<!-- iter:stages -->
- [x] 复用成熟夹具定义最少跨模块断言
- [x] 运行隔离集成负例并保持原始失败
- [x] 交付集成结果与未覆盖边界，最高TESTING
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [x] **experiment**：python -B -m pytest -p no:cacheprovider tests/test_self_hosting.py tests/test_execution_readiness.py tests/test_autonomy.py tests/test_checkpoint_resume.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。
- [x] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [x] **interfaces**：tests/test_self_hosting.py受影响联合断言与evidence/10/integration-report.json；报告仅synthetic层，不产生原生验收或批准。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `tests/test_self_hosting.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/10-integration-fault-paths.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/10/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [x] 坏编码卡与合法卡混合时takeover/inventory仍有完整库存；含未知模式的DONE不在envelope/board重新变PASS。
- [x] 延迟/失败READY的guard不产生dispatch；外来owner、phase/candidate不符、依赖非PASS、两次无进展、坏幂等payload均保持拒绝和原卡字节。
- [x] Git/FS源码/证据/正文漂移、FS拒Git grant、未知命令终态的既有成熟覆盖直接沿用适用结果；新增断言仅针对模块连接缺口，不破坏真实卡或耗尽真实预算。
- [x] 安装清单漂移不因投影重建变成一致；临时安装受影响harness检查与维护路径脱钩。所有样例标synthetic，报告列每项命令/候选/证据，不声称真实委派。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。

2026-11-15T05:43:08.500518+00:00：隔离跨模块实验130通过，payload相关11通过，Git漂移5通过；真实原生链与批准分层，不改产品；原生实现会话01a1ddb8-4209-7662-991e-fcf18f1a74a2和命令树已确认终态。原始证据/source manifest/type checks已核对，冻结C后独审，非整轮批准。

2026-11-15 UTC — Task 10 isolated integration, implementer 01a1ddb8-4209-7662-991e-fcf18f1a74a2, base 40d76d4456261a41bf1b67106becad17ecc28e29; candidate is the base plus the source hashes in source-manifest.json, C pending. Coordinator fdcc4cce88635ee81573be5991de11de650659d8 remains frozen and does not approve candidate semantics.

Decision: use mature fixture APIs and candidate source for cross-module checks. The experiment preserves rejection, existing event bytes and handoff across temporary fixture checks; its JS callbacks are synthetic, not native delegation. Explicit invalid frozen Git mode is tested via a reviewed synthetic fixture rather than a schema-drift shortcut. The temporary installation manifest is a caller-supplied byte inventory, not authenticated Git provenance. After a separate fixture project's projection rebuild it still rejects drift; after restoring bytes the current payload's actual handoff and service tests run without docs. Existing checkpoint and self-hosting cases cover FS drift, FS rejection of Git grant, unknown command terminal, owner/phase/candidate/dependency, repeated no-progress and bad replay; no real task budget is used.

The exact experiment first exposed two test-interface mistakes (inventory uses path; install checker raises on mismatch): 128 passed, 2 failed, exit 1 in experiment-01, preserved. Corrected input yielded 130 passed, exit 0 in experiment-02. Nested payload receipt reports 11 passed, exit 0 and tree terminal. Existing Git source/evidence/body drift test was rerun as 5 passed after product audit/query changed since task01's prior receipt. All commands use frozen Linux runner; Python 3.11.17, pytest 9.2.0, MCP 1.30.0, external unique basetemps. Raw command/child receipts and outputs accompany these conclusions.

Interfaces: test_self_hosting assertions and integration-report.json are for review; source-manifest.json binds implementation and evidence, checks-proposal.json proposes the named Spike-Discovery checks. PASS in report describes synthetic assertions only. No native self-use, browser, Windows, actual installation, real delegate, independent approval, whole-branch gates or full suite is claimed. Controller still must observe native terminal, record attempt/release, freeze C, obtain independent review, register D, and run frozen local strict.


2026-11-15T05:46:01.904482+00:00：非参与Reviewer01a1ddbb-385e-7642-9401-db08c0912af1对Ce237a068fb39d21cd80b68a12dfe9cc0d4d21827完整候选APPROVED，独审原件及物理范围已核对；登记D后另运行冻结strict。
<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：01, 02, 03, 06, 07；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/10/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
