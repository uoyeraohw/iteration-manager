# 🧩 [Strict-TDD] 核心逻辑 / 接口契约型子任务模板

新卡可用[结构化生成入口](../../references/template_generation.md)，spec.type设为Strict-TDD，delivery_mode显式选择git或filesystem；本合同的有效RED与独审门禁不变。

完成证据遵守 `references/task_card_schema.md`，必需checks：red、green、regression（RED非零且failure_kind=assertion，其他退出0）。实现仅置TESTING；非参与者独审后，由主管按Git的C/D或FS冻结合同登记收据与状态，再严格检查。不得仅凭勾选或APPROVED字段放行。

> **适用范围**：后端领域模型、业务计算逻辑、API 接口、状态机、数据转换、工具算法等。  
> **核心铁律**：`NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`（未见有效 RED 之前严禁写生产代码）。

---

## 🎯 1. 契约定义与接口锁定 (Interfaces Contract)
- **目标行为 (Target Behavior)**：{描述一个具体的用户可观察或接口可断言的行为}
- **前置依赖 (Consumes)**：{前置任务暴露的精确函数签名、类或数据结构，无则填 None}
- **对外暴露 (Produces)**：{本任务新增或修改的函数签名、返回类型与异常定义}

---

## 🛠️ 2. TDD 红绿循环规划 (Micro TDD Loop)
- [ ] **Step 1 [RED · 核心行为测试]**：编写可编译的核心行为测试；按风险补充必要正常/异常边界，注明哪些补充测试经历RED。任务要求所有指定行为先RED时从其规定。
- [ ] **Step 2 [Verify RED · 确认预期失败]**：运行最小测试命令，确认“目标行为缺失”的真实断言失败（退出码 != 0）；编译错误、缺依赖、空测试集或挂死都不是有效RED。
- [ ] **Step 3 [GREEN · 编写最小生产实现]**：编写仅使上述测试通过的最小生产代码（严格遵守 YAGNI 原则，不写多余代码）。
- [ ] **Step 4 [Verify GREEN · 分层回归]**：开发内环运行目标与受影响测试；任务交付完成下面约定的regression，保留原始证据并交付TESTING候选。影响不明扩大检查，不自动缩减既定全量门禁。
- [ ] **Step 5 [REVIEW INPUT · 待审交付]**：整理冻结规格、候选及原始证据；同一实现者可以负责RED/GREEN和返修，Reviewer必须独立。独审APPROVED后由主管登记DONE并运行本地strict，FS不再改冻结正文。

---

## 🛡️ 3. 确定性验收断言 (Acceptance Criteria)
- [ ] **核心单测**：`{具体单测运行命令}` 退出码为 0，用例全部通过。
- [ ] **任务回归门禁**：`{受影响回归命令及覆盖范围/选择依据}` 全部通过；迭代README另定义集成路径与全量回归。
- [ ] **边界测试**：`{契约涉及的空值、越界、依赖失败等必要边界及命令}` 通过，保留失败路径和保密检查。
