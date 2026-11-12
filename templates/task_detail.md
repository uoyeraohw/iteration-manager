---
schema_version: 1
iteration: "{迭代序号}-{迭代名称}"
task_id: "{任务序号}"
task_name: "{任务名称}"
status: "⚪ 待开始 (TODO)"
type: "Strict-TDD"  # 契约模板类型: Strict-TDD | UI-Component | Refactor-Benchmark | Spike-Discovery
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "UNASSESSED"
typesafe_evidence: ""
tdd_verified: false
review_status: "PENDING"
review_receipt: "docs/todos/{迭代序号}-{迭代名称}/evidence/{任务序号}/review.json"
base_sha: ""
head_sha: ""
created_at: "YYYY-MM-DD HH:mm"
updated_at: "YYYY-MM-DD HH:mm"
---

# 📝 子任务执行卡：{任务序号} - {任务名称}

> **所属迭代**：[{迭代序号}-{迭代名称}](file:///docs/todos/{迭代序号}-{迭代名称}/README.md)  
> **当前状态**：`⚪ 待开始 (TODO)` · **预计工时**：`2-4h` · **复杂度**：`🟡 L2`  
> **当前阶段**：由下方阶段清单推导；比例表示清单完成情况，不表示工时进度。  
> **TypeSafe 质检分**：`UNASSESSED` · **TDD 实证**：`PENDING` · **对审状态**：`PENDING`

---

## 🎯 1. 任务执行目标与接口契约 (Objective & Interfaces)
明确本任务的单一核心职责、交付边界与跨任务接口契约，杜绝范围扩散与函数签名漂移：
- **主要目标**：{一句话精准概括该任务的核心实现目标}
- **交付产物**：{列出本任务必须最终生成的模块、功能或接口}
- **跨任务接口契约 (Interfaces Contract)**：
  - **Consumes (消费前置依赖)**：{前置任务暴露的精确函数签名、类或数据结构，无则填 `None`}
  - **Produces (对外暴露契约)**：{本任务向后续任务提供的精确函数名、入参类型与返回类型}

---

## 🏗️ 2. 业务阶段与微观里程碑拆解 (Execution Stages & Sub-milestones)
细化本任务内的具体业务拆解阶段（每完成一个阶段勾选 `[x]`，看板将实时感知并更新进度条）：
<!-- iter:stages -->
- [ ] **Stage 1/3: 接口契约冻结与测试设计 (RED)**：在 `test/` 中编写覆盖核心行为与异常边界的失败测试用例，运行确认有效 RED；
- [ ] **Stage 2/3: 业务核心逻辑最小化实现 (GREEN)**：编写生产代码消除 RED 报错，达成全量测试 100% PASS (YAGNI 原则)；
- [ ] **Stage 3/3: 物理三防自检与独立对审 (REVIEW)**：运行 `iter_sync.py --check-scope` 自检合规，提交 Commit 并通过独立审查。
<!-- /iter:stages -->

---

## 🛠️ 3. 按类型验证规划 (Verification Process)
本模板默认 Strict-TDD。其他 type 必须将本节与第2节替换为对应 `templates/contracts/` 流程，禁止要求 UI/重构/Spike 伪造 RED 或 tdd_verified=true。Strict-TDD 按顺序推进：
<!-- iter:verification -->
- [ ] **Step 1 [RED · 编写失败测试]**：编写测试用例，未见有效 RED 严禁写业务代码；
- [ ] **Step 2 [Verify RED · 实证测试失败]**：运行测试，确认产生预期断言失败；
- [ ] **Step 3 [GREEN · 最小化生产实现]**：仅编写使测试通过的最小代码；
- [ ] **Step 4 [Verify GREEN & Scope · 物理三防自检]**：全量单测通过，运行 `iter_sync.py --check-scope` 确认改动零越界，状态流转至 `🔵 待验收 (TESTING)`；
- [ ] **Step 5 [REVIEW & LOCAL SYNC · 独立对审与二级回写]**：通过 Reviewer 独立审查（`review_status: APPROVED`）后，更新为 `🟢 已完成 (DONE)`，运行 `iter_sync.py --local` 刷新看板。
<!-- /iter:verification -->

---

## 💡 4. 执行建议与技术考量 (Implementation Guidelines)
- **推荐架构与设计模式**：{建议采用的设计模式}；
- **潜在避坑指南**：{列出已知技术陷阱}；
- **性能与安全约束**：{关键性能要求与安全边界}。

---

## 📦 5. 新增或变更内容清单 (File & Scope Impact)
明确全部授权文件及证据目录；目录授权用结尾 `/`，不支持 glob。任务卡与所属 README 隐式允许，但冻结规格仍受保护。检查器只报告、不撤销文件：
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| :--- | :---: | :--- |
| `src/modules/example.js` | `[CREATED]` | 核心业务逻辑实现类 |
| `src/routes/api.js` | `[MODIFIED]` | 挂载新增接口路由并配置权限守卫 |
| `test/modules/example.test.js` | `[CREATED]` | 自动化单元测试用例，覆盖核心分支与异常边界 |
| `docs/todos/{迭代序号}-{迭代名称}/evidence/{任务序号}/` | `[CREATED]` | 原始输出、独立审查报告与JSON收据 |
<!-- /iter:scope -->

---

## 🛡️ 6. 确定性验收标准 (Acceptance Criteria)
<!-- iter:acceptance -->
- [ ] **代码逻辑完备**：核心接口支持预期功能，入参与返回值严格符合 `Interfaces` 契约；
- [ ] **自动化测试通过**：执行测试命令及全量测试套件 100% PASS；
- [ ] **物理三防合规**：`iter_sync.py --check-scope` 校验通过，无清单外文件越界；
- [ ] **独立对审通过**：经 Reviewer Subagent 审查达成 `Spec ✅` 与 `Quality Approved`；
- [ ] **状态冒泡回写（Zero-Root-Touch）**：更新为 `🟢 已完成 (DONE)`，运行 `iter_sync.py --local` 仅刷新所属二级迭代 `README.md`。
<!-- /iter:acceptance -->

---

## 🧾 7. 执行实证、对审记录与裁决账本 (Implementation Report, Review & Rulings Ledger)
<!-- iter:ledger -->
### 7.1 Implementer TDD 实证报告
- **Commit 范围 (`BASE_SHA..HEAD_SHA`)**：`{base_sha}..{head_sha}`
- **RED 阶段失败实证摘要**：`{记录实际运行命令及 FAIL 报错}`
- **GREEN 阶段通过实证摘要**：`{记录测试命令、通过用例数及耗时}`
- **按类型的原始证据路径**：`{按 references/task_card_schema.md 列出 checks、命令/cwd/退出码及output；非TDD任务使用对应类型名称}`

### 7.2 独立代码审查与修复轮次记录 (Code Review & Fix Loop)
- **审查结论 (Verdict)**：`{PENDING | APPROVED | NEEDS_FIX | BLOCKED；会诊不等于批准}`
- **修复轮次记录 (Fix Rounds)**：`{记录 fix round R/5 或 None}`
- **推迟的微瑕项 (Deferred Minors)**：`{无则填 None}`

### 7.3 偏差裁决账本 (Rulings Ledger)
- **计划/契约偏差裁决 (`Rulings`)**：`{格式：Ruling: <决策内容> — <原因> — <若误判代价>；若无偏差填 None}`
<!-- /iter:ledger -->

完成顺序：提交实现C（含原始输出）→独立审查C与冻结规格→按 [任务卡证据契约](file:///C:/Users/qingyu/.codeg/skills/iteration-manager/references/task_card_schema.md) 登记JSON收据、状态和账本→提交登记D→严格检查。head_sha始终指向C，不改成D。代码、测试、原始输出或规格有实质变化时，重审受影响内容。旧卡缺收据保留声明状态，严格验收为UNKNOWN，不补造批准。
