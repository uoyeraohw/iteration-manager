---
schema_version: 1
iteration: "10-codex-install-consumption"
task_id: "01"
task_name: "ITER10-CODEX-20261114 isolated UI card"
status: "TODO"
type: "UI-Component"
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
delivery_mode: "filesystem"
candidate_id: "iter10-codex-installed-consumption-isolated-sample"
---

# 01 · ITER10-CODEX-20261114 isolated UI card

## 1. 任务执行目标与接口契约
- **主要目标**：ITER10-CODEX-20261114: render an isolated unapproved UI consumption sample
- **Consumes**：Local isolated UI fixture only
- **Produces**：An unapproved filesystem UI task card

## 2. 业务阶段
<!-- iter:stages -->
- [ ] Describe an isolated UI sample without implementation
<!-- /iter:stages -->

## 3. 按类型验证规划
先走真实用户路径，再检查正常、空、加载、错误四态及约定视口和实际视觉。
<!-- iter:verification -->
- [ ] **interaction**：Observe sample button interaction in an isolated UI fixture; not executed by generation
- [ ] **states**：Observe loading, empty, success and error states; not executed by generation
- [ ] **visual**：Inspect sample layout at its actual viewport; not executed by generation
- [ ] **regression**：Run affected sample UI regression checks after authorized implementation; not executed here
<!-- /iter:verification -->

## 4. 交付与冻结
完整正文、阶段勾选及实证先定稿，再冻结候选并独审；审查后只登记允许的元数据及外部收据，正文变化须重新冻结与受影响重审。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `ui/sample.py` | MODIFIED | 本任务授权范围 |
| `tests/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] All four UI verification categories are present; no approval facts are generated
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
