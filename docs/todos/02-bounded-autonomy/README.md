# 第二批：阶段2统一助手与有界自治

状态：ACCEPTED。第二批准入门禁通过，允许推进第三批（阶段3—4）。

## 范围与依赖

以.codeg主版本实施，保留第一批C/D证据门禁。权威助手源、真实工具协议、唯一写者、独立身份、预算幂等/恢复、旧卡只读接管、TypeSafe尺度统一。助手配置部署及另外两个副本同步在阶段4进行。

## 已实施

- 三个权威助手Prompt及共享agent_protocol；移除SKILL重复且冲突的内嵌调度。
- 卡内自治事件与单写者，临时排他锁/原子替换；默认5/10/1/2，启动前可配置。重复事件/恢复不清累计，达到上限保留FUSED/BLOCKED。
- legacy入口去重、linked worktree会诊包；可信envelope不冒填HEAD；旧卡只读报告。
- TypeSafe真实state/questions、0索引尺度换算、30/30/20/20与80/70门禁；初始UNASSESSED。

## 证据与待验

原始运行：build/stage02-20261111/runs.jsonl。autonomy-behavior-red有真实断言失败，早期autonomy-red中新增参数TypeError不算行为RED。recovery-red、release-red记录两个后续断言缺陷；对应GREEN及完整回归另存。budget-integration首轮有fixture错误，不算RED，修正后的跨进程/Worktree检查为补充回归。prompt-sources-red/green是静态契约检查，不替代真实代理行为。

Antigravity基线讨论：session1490，task b01b882b-17b3-4cb9-b7e1-0894af224dd2，已终态，原文见build/stage02-20261111/antigravity-baseline.md。采纳持久幂等、接管分析与执行分离；不采纳历史卡自动豁免，以保留已批准UNKNOWN契约。TypeSafe对原轮次机制可防无限修复的noul输出0.2；对历史豁免改变契约的输出0.33；综合裁决仍按第一批明确契约不豁免，并非以模型概率替代授权。

## 最终验收

冻结candidate03，主版本32份源码/模板/测试/决定文件与候选直接内容比较一致；完整回归55 passed，退出0，原始日志full-candidate03.log（167.48s）。笔记tree/format校验通过。

独立Antigravity：运行时session1493/task a1ecb5ff-a084-461b-aa68-869aefe8dc8a为PASS；Prompt协议session1494/task 834b712e-d200-4610-af7a-71c00652d923为PASS。两者均已终态且未参与设计。报告原文及Codex裁决见build/stage02-20261111/acceptance.json。运行时报告有不可靠行号，定位按符号核对；额外16项重跑缺持久原始输出，不增加为独立测试证明，采用主线程55项原始回归。

实际压力01发现桥接造示例SHA与unknown误解，补协议后全新session1492压力02返回UNKNOWN/BLOCKED和NEEDS_INPUT，未造字段。TypeSafe整体覆盖判断输出0.08；Codex按本批逐项事实/原始回归/独立审查裁决通过，不把模型概率当完成证明。阶段3看板、阶段4助手部署/新会话实际消费/沙箱协作/恢复和副本同步仍未完成，不计入本批准入结论。
