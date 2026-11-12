# 🧩 [Refactor-Benchmark] 架构重构 / 性能优化型子任务模板

完成证据遵守 `references/task_card_schema.md`，必需checks：baseline、regression、compatibility、benchmark_before、benchmark_after（compatibility为观测，前后量测条件与数值保留原始输出）。实现仅置TESTING；提交C并独立审查后，由主管登记真实JSON收据与持久报告、状态，提交D再严格检查。不得仅凭勾选或APPROVED字段放行。

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
- [ ] **Step 1 [锁死现有行为 (Baseline Lock)]**：在重构前运行现有全量测试，确认 100% GREEN；若既有测试覆盖不足，先为旧逻辑补充高保真保护网测试！
- [ ] **Step 2 [渐进式重构实现]**：小步快跑（Tiny Commits）调整内部架构，保持接口外表不变，每改动一小步即刻运行测试验证。
- [ ] **Step 3 [消除功能漂移]**：运行全量测试套件，确认零回归故障（0 Failures / 0 Regressions）。
- [ ] **Step 4 [收集优化后实测数据 (After)]**：在完全相同的环境与数据量下，运行基准测试脚本，记录新数据并计算提升比例。
- [ ] **Step 5 [审查与本地冒泡]**：通过独立审查后更新任务卡为 `🟢 已完成 (DONE)`，运行 `iter_sync.py --local`。

---

## 🛡️ 3. 确定性验收断言 (Acceptance Criteria)
- [ ] **回归测试**：全量测试套件 100% PASS，无任何功能与异常逻辑漂移。
- [ ] **量化提升实证**：在任务卡iter:ledger 第7.1节附带清晰的 Before vs After 数据对比表。
- [ ] **兼容性验证**：公共 API 返回结构与 HTTP 状态码完全一致。
