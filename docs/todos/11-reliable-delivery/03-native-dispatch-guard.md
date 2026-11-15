---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "03"
task_name: "连接就绪检查与真实委派的薄守卫"
status: "TESTING"
type: "Strict-TDD"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "86.450"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: true
review_status: "PENDING"
review_receipt: ""
base_sha: "09e916a94aaf90a8281f4ed568beed4a4a4a2816"
head_sha: ""
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"iter11-controller-linux-20261115\",\"events\":{\"iter11-03-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"03-native-dispatch-guard\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:19:20.617011+00:00\"},\"iter11-03-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/03/attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"phase\":\"implementation\",\"candidate\":\"09e916a94aaf90a8281f4ed568beed4a4a4a2816\",\"inputs\":[\"docs/todos/11-reliable-delivery/03-native-dispatch-guard.md\",\"docs/todos/11-reliable-delivery/README.md\",\"AGENTS.md\",\"scripts/deadline_watch.js\",\"references/execution_readiness.md\",\"tests/test_deadline_watch.py\"],\"capabilities\":[\"native-codex-cli-implementer\",\"approved-frozen-linux-runner\",\"Python3.11.17-pytest9.2-mcp1.30\",\"independent-native-reviewer\"],\"version\":1,\"checkpoint\":\"核心Promise/绑定检查2断言RED、最终33通过；真实冻结READY消费后仅1次Codeg调用，子shell启动BLOCKED原样保留\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"executor_id\":\"01a1dd6e-e307-7d53-9be3-0f011688cd30\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/03/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"summary\":\"核心Promise/绑定检查2断言RED、最终33通过；真实冻结READY消费后仅1次Codeg调用，子shell启动BLOCKED原样保留\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/03/delivery.json\"}],\"commands\":[\"docs/todos/11-reliable-delivery/evidence/03/red-implementer-01.json\",\"docs/todos/11-reliable-delivery/evidence/03/green-implementer-01.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/11-reliable-delivery/evidence/03/attempt.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"09e916a94aaf90a8281f4ed568beed4a4a4a2816\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/03-native-dispatch-guard.md\",\"docs/todos/11-reliable-delivery/README.md\",\"references/execution_readiness.md\",\"scripts/deadline_watch.js\",\"tests/test_deadline_watch.py\"],\"capabilities\":[\"Python3.11.17-pytest9.2-mcp1.30\",\"approved-frozen-linux-runner\",\"independent-native-reviewer\",\"native-codex-cli-implementer\"],\"scope\":[\".agents/notes/planned/iter11/03-native-dispatch-guard.md\",\"docs/todos/11-reliable-delivery/evidence/03/\",\"references/native_dispatch_adapter.md\",\"scripts/dispatch_guard.js\",\"tests/test_dispatch_guard.py\"]},\"executor_id\":\"01a1dd6e-e307-7d53-9be3-0f011688cd30\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/03/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/03/delivery.json\",\"summary\":\"核心Promise/绑定检查2断言RED、最终33通过；真实冻结READY消费后仅1次Codeg调用，子shell启动BLOCKED原样保留\"}],\"checkpoint\":\"核心Promise/绑定检查2断言RED、最终33通过；真实冻结READY消费后仅1次Codeg调用，子shell启动BLOCKED原样保留\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"commands\":[{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/03/green-implementer-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T04:20:49.382420+00:00\",\"ended_at\":\"2026-11-15T04:20:50.950771+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/03/red-implementer-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-15T04:20:20.665980+00:00\",\"ended_at\":\"2026-11-15T04:20:26.135577+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":7.037948}},\"result\":{\"task_id\":\"03-native-dispatch-guard\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:25:02.691949+00:00\"},\"iter11-03-release-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/03/implementation-terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"03-native-dispatch-guard\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:25:02.758812+00:00\"},\"iter11-03-review-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"03-native-dispatch-guard\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:25:02.829038+00:00\"}},\"blocked_reason\":\"\"}"
updated_at: "2026-11-15T04:25:02.829137+00:00"
---

# 03 · 连接就绪检查与真实委派的薄守卫

## 1. 任务执行目标与接口契约
- **主要目标**：为现有Codeg持久JavaScript执行器提供可注入的顺序守卫：同owner检查终态成功并消费READY后才调用一次真实委派；保留原生工具和事件账。
- **Consumes**：现有--dispatch-check card --context path --phase phase --owner owner；返回task_path/task_id/phase/candidate/readiness。scripts/deadline_watch.js: watchDeadline({...})保持原样。实际Codeg schema在运行时确认。
- **Produces**：scripts/dispatch_guard.js: async dispatchAfterReady({request, check, dispatch}) -> {dispatched, reason, check, delegation}；request含request_id/project_root/tool_entry/task_path/task_id/owner/phase/candidate/context；check(request) -> Promise<{state,exit_code,argv,cwd,request_id,terminal_evidence,stdout,stderr}>；dispatch(request, ready) -> Promise<原生返回>。不使用Node API。

## 2. 业务阶段
<!-- iter:stages -->
- [x] 以可控Promise覆盖running/失败/乱序及身份不符，取得断言RED
- [x] 完成薄守卫GREEN及既有截止守卫兼容
- [x] 在实际Codeg schema可用时记录一条真实先检查后派发链，缺宿主则保留BLOCKED
<!-- /iter:stages -->

## 3. 按类型验证规划
核心行为先取得可编译测试的真实断言RED，再最小GREEN；环境错误不算RED。
<!-- iter:verification -->
- [x] **red**：python -B -m pytest -p no:cacheprovider tests/test_dispatch_guard.py tests/test_deadline_watch.py -q；由同一实现者先取得验收中具体行为断言失败，环境/导入失败不作RED；通过冻结runner。
- [x] **green**：python -B -m pytest -p no:cacheprovider tests/test_dispatch_guard.py tests/test_deadline_watch.py -q；同一实现者最小修复后通过，保留原始输出；通过冻结runner。
- [x] **regression**：python -B -m pytest -p no:cacheprovider tests/test_dispatch_guard.py tests/test_deadline_watch.py -q；覆盖本卡列出的直接接口/兼容范围，影响不明扩大；不代替整轮全量。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `scripts/dispatch_guard.js` | MODIFIED | 本任务授权范围 |
| `references/native_dispatch_adapter.md` | MODIFIED | 本任务授权范围 |
| `tests/test_dispatch_guard.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/03-native-dispatch-guard.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/03/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] check必须为本次request_id，带实际argv/cwd及原生终态来源；guard核对实际argv的tool_entry/task_path/context/phase/owner与request完全一致，cwd等于project_root；命令state=completed、整数exit_code=0、单份JSON且readiness=READY；stdout中的task_path/task_id/phase/candidate均精确相符。
- [ ] check仍running、拒绝、抛错、坏JSON、退出非零、错owner/旧context路径/旧request_id或候选不符时dispatch调用数为0；READY时调用数为1。委派抛错/unknown不自动重试，不伪造终态。
- [ ] 守卫只约束经过该入口的调用，不声称拦截所有原生委派；真实会话ID/检查原件/调用顺序另存，Node替身不作原生消费证据。
- [ ] 本卡只交付代码守卫与单独契约；任务04接入权威默认指令，避免多卡改同一流程文件。
- [ ] argv/cwd和request标识只是可审计绑定，不能自证原生来源或context语义新鲜度；主控/独审核对真实命令和观察原件。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。

2026-11-15T04:25:02.772945+00:00：核心Promise/绑定检查2断言RED、最终33通过；真实冻结READY消费后仅1次Codeg调用，子shell启动BLOCKED原样保留；原生实现会话01a1dd6e-e307-7d53-9be3-0f011688cd30和命令树已确认终态。原始证据/source manifest/type checks已核对，冻结C后独审，非整轮批准。
<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：01；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/03/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
