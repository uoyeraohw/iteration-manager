---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "05"
task_name: "公布带证据的支持矩阵"
status: "TODO"
type: "Spike-Discovery"
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

# 05 · 公布带证据的支持矩阵

## 1. 任务执行目标与接口契约
- **主要目标**：按能力、平台和宿主公布已验证、未验证及明确不支持范围；仅维护证据支持的声明，不实施跨平台或FS恢复扩展。
- **Consumes**：2026-11-14发布记录、iter_run/checkpoint契约及本次Linux/TypeSafe/Codeg工具可用性观察；其他任务新事实仅在有原件后增补。
- **Produces**：references/support_matrix.md：能力/platform/host/status/observed_at/source_candidate/evidence/limitation；references/release_status.md只链接该矩阵；不重写历史观察为当前事实。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 逐项核对契约与有日期的能力原件
- [ ] 生成支持矩阵和发布索引路由
- [ ] 执行结构/链接检查并由新会话正确识别未验证项
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [ ] **experiment**：python -B -m pytest -p no:cacheprovider tests/test_support_matrix.py tests/test_release_index.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。
- [ ] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [ ] **interfaces**：references/support_matrix.md：能力/platform/host/status/observed_at/source_candidate/evidence/limitation；references/release_status.md只链接该矩阵；不重写历史观察为当前事实。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `references/support_matrix.md` | MODIFIED | 本任务授权范围 |
| `references/release_status.md` | MODIFIED | 本任务授权范围 |
| `tests/test_support_matrix.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/05-support-matrix.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/05/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 至少分别覆盖查询、Windows正式runner、Linux正式runner、Git批准链、FS本地绑定/正常交接、FS时间中断grant、显式安装根消费、Gemini CLI自动发现及配置注入；每行均有状态、日期、候选、来源和限制。
- [ ] 明确FS正常release/claim可用不等于FS时间中断恢复可用；Linux查询可用不等于正式命令链支持；Antigravity消费Gemini副本不等于Gemini CLI自动发现。
- [ ] 原件不能证明的范围写UNKNOWN/未验证及补齐责任和条件；不因历史493通过扩大版本、平台或宿主声明。
- [ ] 只修改矩阵/路由和其结构检查，不更改runner、恢复协议、部署配置或历史发布事实。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
