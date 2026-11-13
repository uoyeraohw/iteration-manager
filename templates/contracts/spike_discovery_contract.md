# 🧩 [Spike-Discovery] 技术探针 / 方案预研型子任务模板

完成证据遵守 `references/task_card_schema.md`，必需checks：experiment、decision、interfaces（后两项为观测，结论及接口可复查，不要求tdd_verified=true）。实现仅置TESTING；Git提交C后独审，主管登记真实JSON收据与持久报告、状态，提交D再严格检查。FS先定稿完整正文并冻结候选和证据，再独审，主管只登记允许的元数据与收据并运行本地strict。不得仅凭勾选或APPROVED字段放行。

> **适用范围**：高不确定性技术调研、第三方 SDK/API 试用、PoC 可行性验证、架构决策选型。  
> **核心铁律**：`物理沙箱隔离 + 产出 ADR 架构决策 + 冻结后续任务 Interfaces`（不产出直接业务代码）。

---

## 🎯 1. 探针目标与核心疑问 (Objective & Key Questions)
- **预研主题**：{需要摸清的关键技术点或选型}
- **待解答的关键疑问 (Spike Questions)**：
  1. 疑问 1：{例如：该库是否原生支持 Node.js ESM 模块？}
  2. 疑问 2：{例如：高并发调用下是否存在内存泄漏？}
  3. 疑问 3：{例如：错误码重试机制是否完善？}

---

## 🛠️ 2. 探针实验执行流程 (Spike Process)
- [ ] **Step 1 [沙箱实验目录准备]**：在项目 `scratch/spike-{主题}/` 隔离目录下编写一次性验证脚本，严禁污染业务主代码。
- [ ] **Step 2 [PoC 原型编码与验证]**：针对待解答的核心疑问编写最小可运行原型，验证关键 API 行为并记录实际输出。
- [ ] **Step 3 [整理架构决策记录 (ADR)]**：形成标准 ADR 文档（包含 Context 背景、Decision 决策、Consequences 优劣与后续代价）。
- [ ] **Step 4 [冻结后续任务 Interfaces 契约]**：将预研确定的数据结构与函数签名正式写出，作为后续正式开发任务卡的输入契约。
- [ ] **Step 5 [审查与本地验收]**：归档技术总结并交付TESTING候选；独立审查批准后由主管按交付模式登记收据和DONE，再运行对应的本地strict检查。

---

## 🛡️ 3. 确定性验收断言 (Acceptance Criteria)
- [ ] **核心疑问全部解答**：在任务卡iter:ledger 第7.1节明确列出每个问题的实测结论（Go / No-Go）。
- [ ] **产物归档**：产出清晰的架构决策记录（ADR）或技术总结备忘。
- [ ] **契约解冻**：后续关联业务任务卡的 `Consumes / Produces` 签名已明确，消除技术盲区。
