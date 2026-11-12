# 🧩 [Strict-TDD] 核心逻辑 / 接口契约型子任务模板

完成证据遵守 `references/task_card_schema.md`，必需checks：red、green、regression（RED非零且failure_kind=assertion，其他退出0）。实现仅置TESTING；提交C并独立审查后，由主管登记真实JSON收据与持久报告、状态，提交D再严格检查。不得仅凭勾选或APPROVED字段放行。

> **适用范围**：后端领域模型、业务计算逻辑、API 接口、状态机、数据转换、工具算法等。  
> **核心铁律**：`NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`（未见有效 RED 之前严禁写生产代码）。

---

## 🎯 1. 契约定义与接口锁定 (Interfaces Contract)
- **目标行为 (Target Behavior)**：{描述一个具体的用户可观察或接口可断言的行为}
- **前置依赖 (Consumes)**：{前置任务暴露的精确函数签名、类或数据结构，无则填 None}
- **对外暴露 (Produces)**：{本任务新增或修改的函数签名、返回类型与异常定义}

---

## 🛠️ 2. TDD 红绿循环规划 (Micro TDD Loop)
- [ ] **Step 1 [RED · 编写针对性失败测试]**：在指定测试文件中设计针对该行为的单元测试用例，覆盖正常路径与异常分支。
- [ ] **Step 2 [Verify RED · 确认预期失败]**：运行最小测试命令，确认测试因“目标行为缺失”产生可解释的断言失败（退出码 != 0）。编译错误或环境问题不可视为有效 RED。
- [ ] **Step 3 [GREEN · 编写最小生产实现]**：编写仅使上述测试通过的最小生产代码（严格遵守 YAGNI 原则，不写多余代码）。
- [ ] **Step 4 [Verify GREEN · 全量回归确认]**：运行目标测试与项目全量测试套件，确认 100% PASS，将任务卡置为 `🔵 待验收 (TESTING)` 并完成 Commit。
- [ ] **Step 5 [APPROVED · 独立审查与本地冒泡]**：运行 `iter_sync.py --review-pkg` 委派独立 Reviewer 审查通过后，更新为 `🟢 已完成 (DONE)`，运行 `iter_sync.py --local`。

---

## 🛡️ 3. 确定性验收断言 (Acceptance Criteria)
- [ ] **核心单测**：`{具体单测运行命令}` 退出码为 0，用例全部通过。
- [ ] **回归门禁**：`{项目全量测试命令}` 100% 通过，无回归破坏。
- [ ] **边界测试**：空参数、越界参数及依赖超时均有对应测试捕获。
