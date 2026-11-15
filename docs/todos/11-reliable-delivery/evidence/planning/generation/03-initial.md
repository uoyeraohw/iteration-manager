---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "03"
task_name: "连接就绪检查与真实委派的薄守卫"
status: "TODO"
type: "Strict-TDD"
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

# 03 · 连接就绪检查与真实委派的薄守卫

## 1. 任务执行目标与接口契约
- **主要目标**：为现有Codeg持久JavaScript执行器提供可注入的顺序守卫：同owner检查终态成功并消费READY后才调用一次真实委派；保留原生工具和事件账。
- **Consumes**：现有--dispatch-check card --context path --phase phase --owner owner；返回task_path/task_id/phase/candidate/readiness。scripts/deadline_watch.js: watchDeadline({...})保持原样。实际Codeg schema在运行时确认。
- **Produces**：scripts/dispatch_guard.js: async dispatchAfterReady({request, check, dispatch}) -> {dispatched, reason, check, delegation}；request含request_id/project_root/tool_entry/task_path/task_id/owner/phase/candidate/context；check(request) -> Promise<{state,exit_code,argv,cwd,request_id,terminal_evidence,stdout,stderr}>；dispatch(request, ready) -> Promise<原生返回>。不使用Node API。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 以可控Promise覆盖running/失败/乱序及身份不符，取得断言RED
- [ ] 完成薄守卫GREEN及既有截止守卫兼容
- [ ] 在实际Codeg schema可用时记录一条真实先检查后派发链，缺宿主则保留BLOCKED
<!-- /iter:stages -->

## 3. 按类型验证规划
核心行为先取得可编译测试的真实断言RED，再最小GREEN；环境错误不算RED。
<!-- iter:verification -->
- [ ] **red**：python -B -m pytest -p no:cacheprovider tests/test_dispatch_guard.py tests/test_deadline_watch.py -q；由同一实现者先取得验收中具体行为断言失败，环境/导入失败不作RED；通过冻结runner。
- [ ] **green**：python -B -m pytest -p no:cacheprovider tests/test_dispatch_guard.py tests/test_deadline_watch.py -q；同一实现者最小修复后通过，保留原始输出；通过冻结runner。
- [ ] **regression**：python -B -m pytest -p no:cacheprovider tests/test_dispatch_guard.py tests/test_deadline_watch.py -q；覆盖本卡列出的直接接口/兼容范围，影响不明扩大；不代替整轮全量。
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
<!-- /iter:ledger -->
