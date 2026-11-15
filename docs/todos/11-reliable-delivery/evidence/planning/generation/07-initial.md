---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "07"
task_name: "消除维护测试对历史证据harness的运行依赖"
status: "TODO"
type: "Refactor-Benchmark"
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

# 07 · 消除维护测试对历史证据harness的运行依赖

## 1. 任务执行目标与接口契约
- **主要目标**：把可复用浏览器/HTTP测试支持代码移至tests/support，使白名单副本能够运行相应维护测试，保留历史harness原件和原测试行为。
- **Consumes**：docs/todos/10-self-hosting-hardening/evidence/04/browser_harness.py的filesystem_fixture(root)、main()及原参数；tests/test_board_handoff.py两处消费者；既有scripts查询/服务接口。
- **Produces**：tests/support/browser_harness.py: filesystem_fixture(root: Path)与main()保留既有参数语义、ready/stop/isolated-fixtures；测试仅从tests/support加载。历史evidence原件不改。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 取得原维护测试基线及同环境Before量测
- [ ] 提取测试支持并保持隔离模式/参数/HTTP行为
- [ ] 白名单临时副本复验、After量测与兼容观察
<!-- /iter:stages -->

## 3. 按类型验证规划
保持外部行为与接口；同环境同数据量取得benchmark_before与benchmark_after实测。
<!-- iter:verification -->
- [ ] **baseline**：python -B -m pytest -p no:cacheprovider tests/test_board_handoff.py tests/test_board_service.py -q；在修改前保留实际维护基线，通过冻结runner。
- [ ] **regression**：python -B -m pytest -p no:cacheprovider tests/test_board_handoff.py tests/test_board_service.py tests/test_harness_portability.py -q；覆盖提取后的隔离库存、参数、HTTP与临时副本。
- [ ] **compatibility**：观察filesystem_fixture/main参数、ready/stop与HTTP输出一致；历史harness及证据字节不变；保留可复查报告。
- [ ] **benchmark_before**：修改前在同一Windows/Python/样例参数下，对受影响harness检查运行3次，记录各次耗时与历史路径依赖数，通过冻结runner。
- [ ] **benchmark_after**：修改后复用Before脚本/参数/环境运行3次，对比耗时与依赖数；不预设提速，通过冻结runner。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `tests/support/` | MODIFIED | 本任务授权范围 |
| `tests/test_board_handoff.py` | MODIFIED | 本任务授权范围 |
| `tests/test_harness_portability.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/07-portable-test-support.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/07/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 两个harness消费者均不依赖维护docs/todos路径；只有白名单文件的临时副本可运行受影响测试，缺少维护历史目录不再造成harness加载失败。
- [ ] 隔离模式不读真实checkout库存，非隔离参数语义、HTTP边界、加载/错误/正常状态及原超时约定不降低；历史harness及日志字节不变。
- [ ] 按现有Refactor-Benchmark保留baseline/regression/compatibility/benchmark_before/benchmark_after。相同Windows/Python/临时样例参数，对受影响harness检查做3次Before/After，报告耗时与历史路径依赖数，不承诺提速。
- [ ] 本卡不宣称所有平台全套已可用；安装烟测、维护回归与真实浏览器观察分别记录，涉及实际浏览器使用Moli并管理自有CDP生命周期。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
