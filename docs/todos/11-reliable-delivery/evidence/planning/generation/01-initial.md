---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "01"
task_name: "统一交付模式解析与完成审计"
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

# 01 · 统一交付模式解析与完成审计

## 1. 任务执行目标与接口契约
- **主要目标**：缺省 Git 保持兼容；显式空值、未知值及卡/profile 冲突在派发、DONE审计、envelope和board统一拒绝。
- **Consumes**：parse_card(content); load_profile(iter_dir); audit_task_file(file_path); candidate_identity(card, root, meta); task_handoff_projection(task_file, meta, state)。既有函数签名保持。
- **Produces**：scripts/iter_contracts.py: resolve_delivery_mode(meta: dict, filesystem_enabled: bool) -> str；只返回git或filesystem，非法组合抛ValueError。既有查询/派发API及JSON键不变。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 冻结包含未知模式的合法Git绑定反例和兼容矩阵，取得目标断言RED
- [ ] 共用纯解析规则，完成审计、派发与交接一致性GREEN
- [ ] 完成Git/FS受影响回归和待审候选
<!-- /iter:stages -->

## 3. 按类型验证规划
核心行为先取得可编译测试的真实断言RED，再最小GREEN；环境错误不算RED。
<!-- iter:verification -->
- [ ] **red**：python -B -m pytest -p no:cacheprovider tests/test_delivery_mode_consistency.py tests/test_query_contract.py tests/test_execution_readiness.py tests/test_completion_gates.py tests/test_filesystem_receipts.py -q；由同一实现者先取得验收中具体行为断言失败，环境/导入失败不作RED；通过冻结runner。
- [ ] **green**：python -B -m pytest -p no:cacheprovider tests/test_delivery_mode_consistency.py tests/test_query_contract.py tests/test_execution_readiness.py tests/test_completion_gates.py tests/test_filesystem_receipts.py -q；同一实现者最小修复后通过，保留原始输出；通过冻结runner。
- [ ] **regression**：python -B -m pytest -p no:cacheprovider tests/test_delivery_mode_consistency.py tests/test_query_contract.py tests/test_execution_readiness.py tests/test_completion_gates.py tests/test_filesystem_receipts.py -q；覆盖本卡列出的直接接口/兼容范围，影响不明扩大；不代替整轮全量。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `scripts/iter_contracts.py` | MODIFIED | 本任务授权范围 |
| `scripts/iter_queries.py` | MODIFIED | 本任务授权范围 |
| `scripts/iter_preflight.py` | MODIFIED | 本任务授权范围 |
| `tests/test_delivery_mode_consistency.py` | MODIFIED | 本任务授权范围 |
| `tests/test_query_contract.py` | MODIFIED | 本任务授权范围 |
| `tests/test_execution_readiness.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/01-delivery-mode-consistency.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/01/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 先构造其余收据、Git ancestry、冻结规格、check输出和验收勾选均合法的DONE卡，未知delivery_mode从contract提交起存在；断言审计不能PASS，防止用规格漂移替代合法性负例。
- [ ] 覆盖缺省git、显式git、合法filesystem、显式空串、未知模式、坏profile、缺profile及卡/profile冲突；dispatch非READY，审计非PASS，交接/看板显示UNKNOWN并列错误。
- [ ] 共享解析不导入CLI、不新增跨调用验收缓存，不改变旧导入、签名、返回/异常合同。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
