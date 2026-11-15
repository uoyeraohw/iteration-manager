---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "10"
task_name: "核验跨模块故障路径的一致性"
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

# 10 · 核验跨模块故障路径的一致性

## 1. 任务执行目标与接口契约
- **主要目标**：组合已完成模块的隔离夹具，锁定错误在派发、事件、交接和审计之间不被抹平；只补跨模块回归，不重复各卡完整测试或承担真实链审计。
- **Consumes**：01模式矩阵、02坏卡隔离、03异步守卫、06安装清单及07测试支持接口；现有tests/test_self_hosting.py及执行就绪/FS/Git夹具。
- **Produces**：tests/test_self_hosting.py受影响联合断言与evidence/10/integration-report.json；报告仅synthetic层，不产生原生验收或批准。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 复用成熟夹具定义最少跨模块断言
- [ ] 运行隔离集成负例并保持原始失败
- [ ] 交付集成结果与未覆盖边界，最高TESTING
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [ ] **experiment**：python -B -m pytest -p no:cacheprovider tests/test_self_hosting.py tests/test_execution_readiness.py tests/test_autonomy.py tests/test_checkpoint_resume.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。
- [ ] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [ ] **interfaces**：tests/test_self_hosting.py受影响联合断言与evidence/10/integration-report.json；报告仅synthetic层，不产生原生验收或批准。；核对消费者与现有合同兼容，冻结可复查产物。
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
- [ ] 坏编码卡与合法卡混合时takeover/inventory仍有完整库存；含未知模式的DONE不在envelope/board重新变PASS。
- [ ] 延迟/失败READY的guard不产生dispatch；外来owner、phase/candidate不符、依赖非PASS、两次无进展、坏幂等payload均保持拒绝和原卡字节。
- [ ] Git/FS源码/证据/正文漂移、FS拒Git grant、未知命令终态的既有成熟覆盖直接沿用适用结果；新增断言仅针对模块连接缺口，不破坏真实卡或耗尽真实预算。
- [ ] 安装清单漂移不因投影重建变成一致；临时安装受影响harness检查与维护路径脱钩。所有样例标synthetic，报告列每项命令/候选/证据，不声称真实委派。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
