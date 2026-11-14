# 🧩 [Refactor-Benchmark] 架构重构 / 性能优化型子任务模板

新卡可用[结构化生成入口](../../references/template_generation.md)，spec.type设为Refactor-Benchmark，delivery_mode显式选择git或filesystem；不强制RED，benchmark_before/benchmark_after及独审门禁不变。

完成证据遵守 `references/task_card_schema.md`，必需checks：baseline、regression、compatibility、benchmark_before、benchmark_after（compatibility为观测，前后量测条件与数值保留原始输出）。实现仅置TESTING；非参与者独审后，主管按Git的C/D或FS冻结合同登记收据与状态，再严格检查。不得仅凭勾选或APPROVED字段放行。

> **适用范围**：模块重构、分层解耦、SQL/查询优化、并发加速、依赖升级、技术债消除。  
> **核心铁律**：`Zero Behavioral Change (零功能漂移) + Baseline Benchmark (实测基线比对)`。

---

## 🎯 1. 重构范围与性能基线 (Scope & Baseline)
- **重构目标模块**：`{重构影响的文件或类路径}`
- **外部黑盒契约**：声明外部调用方使用的公共接口，要求签名与行为 100% 保持向后兼容。
- **现状性能基线 (Before)**：
  - 核心耗时 / 延迟：`{P95 / P99 / 平均耗时}`
  - 资源占用：`{内存 / CPU / 数据库查询次数}`
  - 性能测试脚本 / 命令：`{benchmark 运行命令}`

---

## 🛠️ 2. 安全重构与验证流程 (Safe Refactoring Process)
- [ ] **Step 1 [锁死现有行为 (Baseline Lock)]**：在重构前取得约定影响范围的测试基线；范围不明或任务规定全量时运行全量。已有同候选/输入/环境的有效基线可复用；覆盖不足先补旧行为保护测试，不伪造RED。
- [ ] **Step 2 [渐进式重构实现]**：小步调整内部结构，保持外部接口与行为，每步运行针对性检查。
- [ ] **Step 3 [消除功能漂移]**：任务交付运行受影响回归并核对兼容性；影响不明扩大范围，迭代末仍需全量回归，不逐小步重复全套。
- [ ] **Step 4 [收集优化后实测数据 (After)]**：在完全相同的环境与数据量下，运行基准测试脚本，记录新数据并计算提升比例。
- [ ] **Step 5 [待审交付]**：冻结候选与可比基线证据，提交独立Reviewer；APPROVED后主管按交付模式登记DONE并本地strict，FS不再改冻结正文。

---

## 🛡️ 3. 确定性验收断言 (Acceptance Criteria)
- [ ] **任务回归**：`{受影响回归命令、范围与选择依据}` 全部通过，功能及异常路径无漂移；既定全量要求仍执行。
- [ ] **量化提升实证**：在任务卡iter:ledger 第7.1节附带清晰的 Before vs After 数据对比表。
- [ ] **兼容性验证**：公共 API 返回结构与 HTTP 状态码完全一致。
