---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "12"
task_name: "统一默认派发与最终收口顺序"
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

# 12 · 统一默认派发与最终收口顺序

## 1. 任务执行目标与接口契约
- **主要目标**：仅维护执行流程契约：受支持Codeg路径消费03守卫；提前结构预检与全部卡登记后的最终收口明确分离，消除顺序歧义。
- **Consumes**：任务03 dispatchAfterReady接口/原生能力记录；既有共同协议、执行检查、Worktree流程图及三助手/委派模板。
- **Produces**：共同协议的权威顺序与其余引用一致：READY终态后实际派发；每卡C/独审/D/local strict；全部卡DONE后集成/全量、整轮独审及最终branch strict。其他文档只引用，不自建循环。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 核对三种流程场景及权威来源
- [ ] 统一协议/流程图/模板对03守卫和收口的引用
- [ ] 运行流程消费检查并保存真实原生顺序观察
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [ ] **experiment**：python -B -m pytest -p no:cacheprovider tests/test_workflow_sequence.py tests/test_prompt_sources.py tests/test_task_card_schema.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。
- [ ] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [ ] **interfaces**：共同协议的权威顺序与其余引用一致：READY终态后实际派发；每卡C/独审/D/local strict；全部卡DONE后集成/全量、整轮独审及最终branch strict。其他文档只引用，不自建循环。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `references/agent_protocol.md` | MODIFIED | 本任务授权范围 |
| `references/execution_readiness.md` | MODIFIED | 本任务授权范围 |
| `references/worktree_git_contract.md` | MODIFIED | 本任务授权范围 |
| `templates/assistants/iteration_planner.md` | MODIFIED | 本任务授权范围 |
| `templates/assistants/iteration_controller.md` | MODIFIED | 本任务授权范围 |
| `templates/assistants/task_tech_lead.md` | MODIFIED | 本任务授权范围 |
| `templates/sdd_implementer_prompt.md` | MODIFIED | 本任务授权范围 |
| `templates/sdd_reviewer_prompt.md` | MODIFIED | 本任务授权范围 |
| `tests/test_prompt_sources.py` | MODIFIED | 本任务授权范围 |
| `tests/test_workflow_sequence.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/12-workflow-sequence.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/12/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 场景A：检查running或非READY时不得原生派发；终态READY且身份匹配才消费03守卫并派发。只对实际已验证Codeg路径声明支持；其他宿主保留显式能力缺口。
- [ ] 场景B：提前branch结构预检可在总审前运行，但不标整轮完成；每卡仍C→独审→登记D→local strict。无变更且证据有效时不重复同范围测试或审查。
- [ ] 场景C：全部卡（包括本卡）有效DONE后，Controller执行整轮集成/全量、独立总审和最终登记候选的冻结branch strict。最后一张卡不得自要求先通过此branch strict；总审触发变更时重审受影响候选。
- [ ] 收口原件位于主checkout build/iter11-closeout/唯一UTC目录，不写回已审卡scope；README仅摘要/链接。清理前按授权保留/归档原件，不为证据注册嵌入巨型JSON。
- [ ] experiment为python -B -m pytest -p no:cacheprovider tests/test_workflow_sequence.py tests/test_prompt_sources.py tests/test_task_card_schema.py -q，经冻结runner执行；实际Codeg消费另外留会话/调用顺序原件，不把模板文本测试当原生链。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
