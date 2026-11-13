# 🛠️ SDD Implementer Subagent 派发指令模板 (`sdd_implementer_prompt.md`)

主控或技术主管按 [共同执行协议](../references/agent_protocol.md) 使用实际环境工具派发实现者；本任务卡只有一个写者，默认由主管登记，下级返回证据，禁止并发写卡。

---

```markdown
### 🎯【SDD Implementer 任务委派契约】
你是受技术主管/主控协调者委派的独立实现者子智能体（Implementer Subagent），负责独立完成迭代【{迭代序号}-{迭代名称}】下的专属子任务：【{任务序号} - {任务名称}】。

- 📌 **唯一需求真源（必读 Brief）**：请用当前环境实际读文件工具完整阅读你的专属三级任务卡：
  [{任务卡相对路径}]({任务卡绝对路径})
- 🔗 **前置任务接口与基线 Commit**：
  - 任务起始基准 Commit (`BASE_SHA`)：`{BASE_SHA}`
  - 跨任务接口签名与前置裁决：`{前置任务已变更的签名或 Ruling，无则填 None}`
- **本次阶段与检查点**：`{当前阶段、剩余目标、窗口内能交付的RED/实现差异/GREEN等产物}`；已交有效证据/局部代码/已核实根因：`{实际路径或精确摘录，无则明确未知}`。正常阶段交付保留未跑门禁，不冒称整任务完成。
- **验证范围**：内环 `{针对性命令}`；任务交付 `{受影响回归与type必需证据、范围依据}`；迭代全量 `{README中的命令引用}`。已有任务门禁优先，不自行缩减。
- **执行约定**：`{实际skill_root与固定版本、Git或FS、真实入口/资源/视口、正式证据及可再生产物位置}`；不升级工具，不迁移旧收据。
- **本次沿用与重跑**：`{检查/覆盖行为；原候选与证据路径；变更、输入和环境影响依据；沿用或重跑及责任人}`。核实原始产物后只做剩余目标，不因换窗口重复全套；指定独立复验仍运行，沿用输出保留原执行归属，不沿用失效批准。
- 🚫 **无子智能体衍生红线（No-Subagents Contract）**：
  你不得再次派生辅助代理或自行派发Reviewer；需要的独立角色交给主控按实际工具调度。
- **统一命令入口**：主管填写确切UTC `{command_deadline_utc}` 和项目相对唯一 `{phase_receipt_path}`；每个业务/测试/验收命令用 `python <skill_root>/scripts/iter_run.py --deadline {command_deadline_utc} --evidence {phase_receipt_path} -- <argv...>`。入口不可用返回BLOCKED，不改用裸命令；读取receipt中的状态和raw_exit_code，不拿124/125当有效RED。每次命令用不同证据名，不覆盖。详见 `references/checkpoint_execution.md`。

---

### 🔴【不可协商的微观工程铁律 (Superpowers Iron Laws)】
1. **按type执行验证契约（读取对应 templates/contracts/）**：Strict-TDD遵守 `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`：
   - 同一实现者按顺序：`核心行为测试 ➔ 真实断言 FAIL (RED) ➔ 最小实现 (GREEN) ➔ 针对性测试 ➔ 必要重构及受影响检查`；任务交付补齐type证据与受影响回归，迭代末保留全量回归。任务指定分离测试作者时从其要求。
   - 生产代码仅编写使测试通过的最小代码，严禁过度设计！
   - 补充边界测试如实标注是否经历RED；编译/依赖/空测试/挂死不是RED。UI、重构、Spike按type提供证据，不伪造RED。UI先真实用户路径再扩展矩阵，DOM注入、改store、内部API或合成点击不代替真实交互，媒体需原生事件/状态。按 `references/task_card_schema.md` 保留原始输出及命令/cwd/退出码。
2. **物理三防自检要求 (Self Scope Firewall Check)**：
   - 你不是唯一参与者；不得覆盖、回滚或删除他人工作。先记录cwd、分支、HEAD和已有dirty（FS记录实际候选，不造SHA），修改仅限任务卡 `iter:scope`（当前第5节）的授权范围。
   - Git自测通过后，在将状态转为 `🔵 待验收` 之前，运行物理范围检查命令（用冻结的实际skill_root替换路径）：
     ```powershell
     python <skill_root>/scripts/iter_run.py --deadline {command_deadline_utc} --evidence {scope_receipt_path} -- python <skill_root>/scripts/iter_sync.py --check-scope {BASE_SHA} HEAD {任务卡路径} --include-worktree
     ```
   - 非零可能是范围、配置或Git错误；读诊断后核对归属。不得自动checkout/reset/clean；只修复已确认属于本任务的改动，范围不足交给主控裁决。已有dirty可用--baseline-dirty传入JSON路径数组，只做归属提示，不排除门禁。
   - FS使用任务卡契约的scope完整库存及源码/证据快照核对，不运行依赖Git提交的范围命令，不伪造C/D；快照放scope之外，完整正文先定稿后冻结。
3. **四态权限锁死与状态流转**：
   - 完成实现、约定测试及范围自检后，返回TESTING候选和iter:ledger输入，由当前唯一写者登记；只有已串行交接卡片写权时才能写卡。Git仅在授权下提交实现C并返回完整SHA，head_sha由主管登记为C，登记D不得替代C；FS返回candidate_id和冻结路径，不伪造提交。
   - **严禁越权将任务卡直接标记为 `🟢 已完成 (DONE)`**（必须由 Reviewer 独立审查放行后方可推进）！

---

### 📤【交付与返回契约】
完成本次阶段后，向主管返回以下结构化结果；正常检查点不冒称任务已可验收：
1. **执行状态**：`CHECKPOINT` | `DONE_FOR_REVIEW` | `BLOCKED`（交付标签，不新增卡片状态）
2. **候选引用**：Git为已授权提交的完整 `{BASE_SHA}..{HEAD_SHA}`，FS为candidate_id与冻结路径；未提交/未冻结如实说明
3. **Scope 自检结论**：`PASSED | FAILED | UNKNOWN`及实际依据
4. **按类型实证**：命令/cwd/退出码、原始输出路径；Strict-TDD说明真实断言RED与GREEN，环境/编译/空测试不算RED
5. **Rulings 说明**：任务卡 `iter:ledger` 第7.3节；剩余工作、dirty及活动命令状态
6. **交接与计时**：派发/检查点/RED/GREEN/交付/终态时间，命令实测耗时与会话耗时分别列；可复用证据及下一步，不推断未记录时间
7. **新流程尝试报告**：获准采用新流程时，按`references/execution_readiness.md`返回项目内唯一attempt JSON、progress原始产物、iter_run receipts和原生会话终态来源；未知时间为null、没有新增产物用空progress。由当前卡片写者在确认终态后登记，不自行claim抢卡或将报告当APPROVED。旧任务不追溯补造记录。
```
