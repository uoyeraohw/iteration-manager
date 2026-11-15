---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "04"
task_name: "收敛当前任务的默认阅读导航"
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

# 04 · 收敛当前任务的默认阅读导航

## 1. 任务执行目标与接口契约
- **主要目标**：只调整默认导航：助手定位当前迭代目标、任务交接和证据链接，不默认加载历史全文或工具返回；不修改派发/收口规则。
- **Consumes**：现有SKILL.md入口、templates/iteration_readme.md及--render-envelope输出；共同协议和任务卡契约仍为必读权威文件。
- **Produces**：SKILL.md改为角色/授权/真源摘要与资源路由，具体流程链接共同协议；迭代模板增加当前交接/原件索引，不嵌入原始JSON或日志。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 记录进入当前任务所需的直接文档及原件路径
- [ ] 更新入口和迭代模板的导航路由
- [ ] 运行导航检查并由新会话定位一次当前任务及失败证据
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [ ] **experiment**：python -B -m pytest -p no:cacheprovider tests/test_navigation_paths.py tests/test_prompt_sources.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。
- [ ] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [ ] **interfaces**：SKILL.md改为角色/授权/真源摘要与资源路由，具体流程链接共同协议；迭代模板增加当前交接/原件索引，不嵌入原始JSON或日志。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `SKILL.md` | MODIFIED | 本任务授权范围 |
| `templates/iteration_readme.md` | MODIFIED | 本任务授权范围 |
| `tests/test_navigation_paths.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/04-navigation-paths.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/04/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 对本轮01任务的continue场景，新会话能够指出当前iter:goal、01任务卡/envelope、Strict-TDD契约和01证据目录；查阅01原件失败时明确缺口，不加载10迭代README全文来猜测当前状态。
- [ ] SKILL中原执行步骤归并为共同协议链接，授权边界、四type、真假验收、Git/FS区别和CLI入口仍有直接路由；本卡不重新定义顺序或改动共同协议正文。
- [ ] 新迭代模板包含当前交接摘要/证据路径，链接目标存在且项目内；不内嵌原始JSON/原生工具响应。历史10迭代和发布原件字节不变。
- [ ] 正式experiment为python -B -m pytest -p no:cacheprovider tests/test_navigation_paths.py tests/test_prompt_sources.py -q，经冻结runner执行；另保存一次真实新会话导航消费记录，测试结构通过不代替消费。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
