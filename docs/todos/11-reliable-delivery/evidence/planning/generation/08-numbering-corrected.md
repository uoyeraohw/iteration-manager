---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "08"
task_name: "量测合法Git与FS批准库存的真实成本"
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

# 08 · 量测合法Git与FS批准库存的真实成本

## 1. 任务执行目标与接口契约
- **主要目标**：先建立合法收据、Git绑定和FS快照均实际PASS的代表库存，再量测查询/盘点/HTTP证据路径，定位单次调用内重复工作，不预设优化收益。
- **Consumes**：任务01合法模式解析；现有test_filesystem_delivery_controller/执行就绪/Git临时夹具；audit_task_file、generate_board_data、render_task_envelope、inventory及LiveBoardHandler。07测试支持提取不是功能前提。
- **Produces**：tests/benchmarks/approval_chain.py: main(argv=None) -> int；CLI --sizes 10 100 --repeats 3 --output PATH，输出环境/候选/工作负载/各次秒数/Git调用数/读取字节/批准卡数/限制。tests/test_approval_benchmark_fixture.py验证样例真实性。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 构造Git/FS合法批准库存，先断言每卡审计PASS
- [ ] 分层量测10/100卡各3次并保留原始数据
- [ ] 按单次调用剖析给出优化或维持现状的决策和后续接口
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [ ] **experiment**：python -B tests/benchmarks/approval_chain.py --sizes 10 100 --repeats 3 --output docs/todos/11-reliable-delivery/evidence/08/measurements.json；先确认合法Git/FS库存每卡PASS，通过冻结runner。
- [ ] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [ ] **interfaces**：tests/benchmarks/approval_chain.py: main(argv=None) -> int；CLI --sizes 10 100 --repeats 3 --output PATH，输出环境/候选/工作负载/各次秒数/Git调用数/读取字节/批准卡数/限制。tests/test_approval_benchmark_fixture.py验证样例真实性。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `tests/benchmarks/` | MODIFIED | 本任务授权范围 |
| `tests/test_approval_benchmark_fixture.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/08-approved-chain-benchmark.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/08/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 分别构造10/100卡Git与FS已批准样例；每张DONE均有合法类型checks/原始输出/报告及真实绑定，量测前accepted必须等于卡数；不得用缺收据的快路径代替。
- [ ] 分别记录一次board、全部envelope、一次inventory及实际HTTP证据读取的成本，样例构造不计时；真实Git执行及FS字节比较不替换成成功桩。
- [ ] 相同候选/环境/数据量至少3次，给出逐次值、均值和范围；记录硬件/Python/Git/平台、源码候选及样例限制，不从3次样本推断可靠尾延迟。
- [ ] 分析仅提出基于证据的单次调用复用机会；不实现跨调用验收缓存，不以合成性能证明真实外部业务PASS，不附带未评估的优化改码。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
