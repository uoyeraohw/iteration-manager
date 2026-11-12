# 📌 迭代详情索引：{迭代序号} - {迭代名称}

> **迭代定位**：`docs/todos/{迭代序号}-{迭代名称}/` · **关联分支**：`feat/iter-{迭代序号}` (`.worktrees/iter-{迭代序号}`)  
> **进度指示**：声明DONE [0/3] (0%) · 验收PASS [0/3] · 状态：待开始  
> **更新时间**：`YYYY-MM-DD HH:mm` · **维护机制**：`iter_sync.py --local` (Zero-Root-Touch 自治真源)

---

## 🎯 1. 迭代核心目标与全局约束 (Iteration Goal & Global Constraints)
<!-- iter:goal -->
- **业务背景**：{简要描述本迭代阶段在系统中的背景与解决的核心痛点}
- **核心目标**：
  1. {阶段目标 1}
  2. {阶段目标 2}
- **全局刚性约束 (Global Constraints)**：
  - {版本基线、依赖限制、命名规范或跨任务共享契约}
- **重点审查关注面 (Review Focus)**：
  - {列出 3~5 个最容易发生回归或边界遗漏的输入类型/故障模式，供迭代末全分支总审重点核查}
<!-- /iter:goal -->

---

## 🗂️ 2. 子任务执行概况与目录索引 (Task Breakdown Index)

| 任务序号 | 任务名称 | 核心目标概况 | 责任文件/主要改动 | 状态 | 详细卡片索引 |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **01** | `01-初始化数据表结构` | 创建核心数据模型与迁移脚本 | `src/models/*.js`, `migrations/` | ⚪ 待开始 | [01-初始化数据表结构.md](./01-初始化数据表结构.md) |
| **02** | `02-实现核心服务接口` | 编写 Controller 与 Service 业务逻辑 | `src/controllers/`, `src/services/` | ⚪ 待开始 | [02-实现核心服务接口.md](./02-实现核心服务接口.md) |
| **03** | `03-联调与集成测试` | 编写端到端 API 测试与边界断言 | `test/api/*.test.js` | ⚪ 待开始 | [03-联调与集成测试.md](./03-联调与集成测试.md) |

---

## 🛡️ 3. 迭代级整体验收与合流门禁 (Iteration Acceptance & Merge Gate)
- [ ] 所有子任务卡片状态均已经历 `⚪ 待开始 ➔ 🟡 进行中 ➔ 🔵 待验收 ➔ 🟢 已完成 (DONE)` 完整四态闭环；
- [ ] 每个子任务均具备对应type的原始证据与独立APPROVED收据；仅Strict-TDD要求有效RED/GREEN与tdd_verified=true；
- [ ] 迭代末全分支总审（Final Whole-Branch Review）已通过，工程全量测试套件 100% PASS；
- [ ] 执行 `python ~/.codeg/skills/iteration-manager/scripts/iter_sync.py --check-branch --strict` 验证 100% 满足 `Zero-Root-Touch` 隔离契约。

---

## ⚖️ 4. 迭代级裁决汇总与遗留微瑕 (Iteration Rulings & Deferred Minors)
> 汇总本迭代各子任务执行过程中登记的 `Ruling:` 决策及推迟的 `Deferred Minors`，在合入 `main` 主干前向用户透明呈报：
- **架构与接口裁决汇总 (Rulings Made)**：`None`
- **推迟的微瑕项汇总 (Deferred Minors)**：`None`

---

## 🚀 5. Worktree 推进与单迭代合流指南 (`1 Worktree = 1 Iteration`)
1. **整阶段 SDD 推进**：调用 `/iter next {迭代序号}`，由主窗口作为 Controller 逐任务派发 Implementer Subagent 与 Reviewer Subagent 连续推进；
2. **单任务专窗推进**：调用 `/iter task {迭代序号} {任务序号}`，按共同协议由技术主管组织分类型验证和独立审查，不能自审；
3. **子任务级本地冒泡**：每完成 1 个子任务并验收通过后，在当前 Worktree 分支内 `git commit` 并运行 `python ~/.codeg/skills/iteration-manager/scripts/iter_sync.py --local` 校准本文件（严禁触碰根 `docs/todos/README.md`）；
4. **迭代级主干合流**：本迭代全部子任务完成并通过全分支总审后，将该迭代分支合入 `main` 主干，在 `main` 上运行 `/iter sync` 刷新全局看板并清理 `.worktrees/iter-{迭代序号}`。
