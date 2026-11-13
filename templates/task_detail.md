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

新卡优先按 [结构化生成说明](../references/template_generation.md) 使用 `scripts/iter_templates.py --render spec.json`，直接生成四type×Git/FS组合；`--check`仅预检，不代表执行或批准。本手填模板仍保留兼容用途。

本模板默认Git。手工创建新FS卡时，先完成以下替换，不直接复制默认Git正文作为冻结成品；既有卡不自动改写：

1. 在frontmatter中加入下面两项并填写真实候选ID；保留base_sha/head_sha为空，不添加非空contract_sha：
   ```yaml
   delivery_mode: filesystem
   candidate_id: "{本次真实候选ID}"
   ```
2. 删除上方以 `> **当前状态**` 和 `> **TypeSafe 质检分**` 开头的两行，改为 `> **执行状态与对审结果**：读取frontmatter及review_receipt，正文不复制动态结论。`；阶段比例仍由阶段清单推导。
3. 第7.1节的Commit范围行替换为 `- **候选引用**：ID={真实candidate_id}；manifest={candidate_manifest项目相对路径}；任务快照={contract_snapshot项目相对路径}；目标快照={goal_snapshot项目相对路径}`。candidate_id是标识，不是文件路径；不得填占位SHA。
4. 第7.2节的审查结论行替换为 `- **独立审查结果入口**：由frontmatter.review_receipt指向的外部收据与报告提供；本正文不登记审查结论。`；不得在待审正文预写APPROVED，也不留下会在审查后改写的PENDING结论。
5. 实现、原始证据、阶段/验收勾选与实际ledger完成后定稿完整正文；按任务卡契约冻结并独审。之后只登记允许的元数据与收据，正文需改则生成新冻结候选并重审受影响内容。

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
- [ ] **Stage 1/3: 接口契约冻结与测试设计 (RED)**：为核心行为编写可编译测试并确认真实断言RED；按风险补充必要边界，如实标注是否经历RED，任务指定全部先RED时从其规定；
- [ ] **Stage 2/3: 业务核心逻辑最小化实现 (GREEN)**：最小实现通过针对性及受影响测试 (YAGNI 原则)；
- [ ] **Stage 3/3: 任务门禁与待审交付 (REVIEW)**：完成type证据、受影响回归及范围自检，交付可供独立审查的候选。
<!-- /iter:stages -->

---

## 🛠️ 3. 按类型验证规划 (Verification Process)
本模板默认 Strict-TDD。其他type须将第2、3、6节及实证名称替换为对应 `templates/contracts/` 内容，禁止要求UI/重构/Spike伪造RED或tdd_verified=true。默认同一实现者负责核心RED→GREEN与返修，独立Reviewer另行安排；指定角色分离优先。Strict-TDD按顺序推进：
<!-- iter:verification -->
- [ ] **Step 1 [RED · 编写失败测试]**：编写测试用例，未见有效 RED 严禁写业务代码；
- [ ] **Step 2 [Verify RED · 实证测试失败]**：运行测试，确认产生预期断言失败；
- [ ] **Step 3 [GREEN · 最小化生产实现]**：仅编写使测试通过的最小代码；
- [ ] **Step 4 [Verify GREEN & Scope · 任务交付检查]**：type必需证据与受影响回归通过，按Git/FS合同确认范围，交付TESTING候选；
- [ ] **Step 5 [REVIEW INPUT · 冻结待审输入]**：整理实际候选、原始证据与冻结规格，交给未参与测试/实现/RCA/设计的Reviewer。
<!-- /iter:verification -->

独立APPROVED及收据登记仍是DONE的必要条件，不能用上述待审输入清单代替。Git按C→审查→登记D→strict；FS完整正文先定稿→冻结→独审→只登记允许元数据/收据→strict，不在冻结正文预写尚未发生的APPROVED。

### 本任务的验证与交接约定
- **就绪前提**：{真实入口/资源、依赖、权限和验证能力；只填会改变执行方向的项}。派发时在ledger记录READY/NEEDS_INPUT/BLOCKED及事实，READY不等于验收PASS。
- **开发内环**：{针对性命令、核心行为与真实RED预期}。
- **任务交付**：{type必需checks、受影响回归命令、覆盖边界及选择依据；无法界定影响时扩大检查}。
- **迭代收口**：{所属README的集成/全量命令引用；任务既定全量要求仍保留}。
- **本次检查点**：{工作窗口内的可交付产物与剩余项；实际UTC截止在每次Brief填写}。
- **产物位置**：{正式原始证据路径；项目已有临时输出参数/环境变量映射，无则说明，不自动清理历史}。

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
- [ ] **类型验证通过**：上述任务级必需checks及受影响回归全部通过；已约定全量门禁不得缩减；
- [ ] **范围合规**：Git的 `iter_sync.py --check-scope` 或FS的完整库存/快照核对通过，无授权外变更；
- [ ] **待审材料齐备**：候选、冻结规格、原始证据及范围核对可复查，未把自检写成独立批准。
<!-- /iter:acceptance -->

完成登记门禁：独立Reviewer给出APPROVED → 主管登记收据与DONE → 按交付模式完成strict并仅刷新所属迭代README。审查、状态和投影由元数据/收据记录，不提前勾选尚未发生的事件。

---

## 🧾 7. 执行实证、对审记录与裁决账本 (Implementation Report, Review & Rulings Ledger)
<!-- iter:ledger -->
### 7.1 Implementer TDD 实证报告
- **Commit 范围 (`BASE_SHA..HEAD_SHA`)**：`{base_sha}..{head_sha}`
- **RED 阶段失败实证摘要**：`{记录实际运行命令及 FAIL 报错}`
- **GREEN 阶段通过实证摘要**：`{记录测试命令、通过用例数及耗时}`
- **按类型的原始证据路径**：`{按 references/task_card_schema.md 列出 checks、命令/cwd/退出码及output；非TDD任务使用对应类型名称}`
- **证据复用/失效范围**：`{旧候选及输入/环境、有效证据路径、本次变化和需补验项；无则None}`
- **尝试与交接**：`{实际task_id、起止/检查点时间、新增产物、剩余项、会话及命令终态；连续两次无可用新证据先改变条件，不原样重派}`
- **时间记录**：`{命令实测耗时、会话总耗时、交接时间分别记录；未知写UNKNOWN，重叠不重复加总}`

### 7.2 独立代码审查与修复轮次记录 (Code Review & Fix Loop)
- **审查结论 (Verdict)**：`{PENDING | APPROVED | NEEDS_FIX | BLOCKED；会诊不等于批准}`
- **修复轮次记录 (Fix Rounds)**：`{记录 fix round R/5 或 None}`
- **推迟的微瑕项 (Deferred Minors)**：`{无则填 None}`

### 7.3 偏差裁决账本 (Rulings Ledger)
- **计划/契约偏差裁决 (`Rulings`)**：`{格式：Ruling: <决策内容> — <原因> — <若误判代价>；若无偏差填 None}`
<!-- /iter:ledger -->

Git完成顺序：提交实现C（含原始输出）→独立审查C与冻结规格→按 [任务卡证据契约](file:///C:/Users/qingyu/.codeg/skills/iteration-manager/references/task_card_schema.md) 登记JSON收据、状态和账本→提交登记D→严格检查。head_sha始终指向C，不改成D。FS审查报告/结论写入外部收据及允许的元数据，不在审查后补写本ledger。代码、测试、原始输出或规格有实质变化时，重审受影响内容；FS完整正文漂移也会使绑定失效。旧卡缺收据严格验收为UNKNOWN，不补造批准。
