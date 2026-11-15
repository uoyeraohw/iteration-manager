---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "09"
task_name: "使新重构任务的量测匹配实际目标"
status: "TODO"
type: "Spike-Discovery"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "84.050"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
---

# 09 · 使新重构任务的量测匹配实际目标

## 1. 任务执行目标与接口契约
- **主要目标**：为未来行为保持型重构与性能优化提供两套可消费规划说明：前者量测与结构目标相关的客观指标，后者量测性能；保留四type及既有五项检查，不追溯降低旧卡门禁。
- **Consumes**：现有Refactor-Benchmark五项TYPE_CHECKS与schema1；既有合成量测限制；render_task_card(spec)及模板消费路径。08批准库存量测结果完成后交叉核对，不是本卡的硬依赖。
- **Produces**：references/refactor_evidence.md的两类目标/指标/证据选择规则；templates/contracts/refactor_benchmark_contract.md与scripts/iter_templates.py生成说明一致；verification键集不变，不加第五type或必填元数据。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 用两种真实新卡规划样例确认当前成本与指标匹配问题
- [ ] 更新目标对应的证据规则和生成说明
- [ ] 实际生成及新会话消费两类样例，核对旧卡要求保持
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [ ] **experiment**：python -B -m pytest -p no:cacheprovider tests/test_refactor_evidence_policy.py tests/test_template_generation.py tests/test_task_card_schema.py tests/test_completion_gates.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。
- [ ] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [ ] **interfaces**：references/refactor_evidence.md的两类目标/指标/证据选择规则；templates/contracts/refactor_benchmark_contract.md与scripts/iter_templates.py生成说明一致；verification键集不变，不加第五type或必填元数据。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `templates/contracts/refactor_benchmark_contract.md` | MODIFIED | 本任务授权范围 |
| `references/refactor_evidence.md` | MODIFIED | 本任务授权范围 |
| `scripts/iter_templates.py` | MODIFIED | 本任务授权范围 |
| `tests/test_template_generation.py` | MODIFIED | 本任务授权范围 |
| `tests/test_refactor_evidence_policy.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/09-proportional-refactor-evidence.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/09/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 行为保持型新任务仍有基线/兼容/回归/独审；benchmark_before/after可测任务约定的依赖数、重复入口数等可重复结构指标，无性能目标时不强制延迟/吞吐提升。
- [ ] 性能优化型明确同环境/规模/命令/单位与目标，仍要求真实Before/After性能证据；不以结构指标替代既定性能目标。
- [ ] 四type、schema1、五项检查名与收据绑定保持；既有卡、冻结规格及本轮07的Before/After要求不修改，不把未知指标当无须验证。
- [ ] 两种spec均经实际生成/预检；缺baseline、regression或任一既定检查仍拒绝。模板结构检查与真实助手是否选对指标分别留证。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：无；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/09/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
