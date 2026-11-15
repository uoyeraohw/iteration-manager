# Task 12 fix round 1：F2 原生证据对账交接

2026-11-15 UTC；当前 BASE `305f1d49d499ae3a5112358d57c2fefa48349261`。仅对账 F2，不更改产品、测试、契约、卡片或既有历史原件。原决策、原 grant 终态清单及原生日志摘录逐字节保留；新文件是追加的复核输入，不是新状态账。

已提交的 `codeg-probe-v2-native-excerpt.jsonl` 的 59 行包含 6 次工具调用及相应输出；首次调用（13–14 行）因 bwrap `/proc` 挂载失败，目标命令未启动，无实际命令 ID 或退出码。其余 5 次工具调用中的 10 个 `CommandExecution item_completed` 分别位于 21、29、35–40、48、54 行；均为实际 `completed`、`exit_code: 0`。逐项 ID、原生时间、实际 cwd/argv、原始行哈希及输出哈希见 `fix1-native-command-inventory.json`。调用与命令以各调用和输出之间的事件位置对应：事件未提供逐条 call ID。摘录没有命令 `item_started` 事件；真实进程开始时间 UNKNOWN，调用时间不能冒充该时间。原生完成/退出是原生事件观察，不是独立 runner 进程树终态证明。会话取消有 `codeg-probe-v2-chain.json` 原生查询证据；取消本身不能补足命令树证明。

`codeg-interruption-decision.json` 曾称无内部退出元数据，与上述原生事件冲突；`codeg-interruption-terminal.json` 仅列 experiment-04 与 controller check，遗漏这 10 条消费者读命令。`fix1-reconciled-terminal.json` 补充该事实，但没有回写原有 grant 绑定，也不能追认原 grant 有效。原始错误解释仍为历史 FAIL；独立审查仍需评估本次对账。

F1 **BLOCKED**：目前引用记录中没有明确授权 checkpoint resume 的原始用户指令；一般实施/串行推进不证明该授权。`fix1-recovery-disposition-draft.json` 仅供主控决定，不是授权、批准或恢复指令，不声称不存在其他未提供的授权。需主控取得明确权限/合规处置、按恢复契约重新评估受影响候选并取得新合规消费证据。不得将历史 grant 或后续消费追认为已获授权；本次没有新发/消费 grant、恢复、派发或修改事件。

冻结 runner 执行 `fix1-reconcile.py` 的实际收据 `fix1-reconciliation-command.json` 显示 COMPLETED、业务退出 0、进程树终态；原始输出 `fix1-reconciliation-command.json.output.txt`。脚本核对完整命令行号、ID、退出、未启动分离、原文件哈希及与 BASE 中提交字节一致。它只证明该次对账检查，不证明用户授权或任务完成。无产品/测试变化，复用 `experiment-04.json`（10 passed、退出0、runner tree_terminal true），适用性由原始 `source-manifest.json` 与独审 `review-round1-input.json` 的候选映射支持；不重复全套实验。环境为授权的 Linux Python 3.11.17 与冻结 runner；原生事件局限该次 Codeg 会话，不推广到其他宿主或工作进程。

接口：inventory 列出每个工具调用与终态命令及可复核行/哈希；reconciled-terminal 保留旧清单与增补清单的区别；recovery-disposition 为 F1 BLOCKED 的草案。`fix1-checks-proposal.json` 的 interfaces 明示尚未完成，任何结构成功均不等于任务验收。剩余 F1 明确处置和新合规证据、受影响新候选冻结与非参与者复审、主管登记 D 及冻结 local strict；全部卡有效完成后另行整轮门禁。实现者最高 TESTING，无自动批准。
