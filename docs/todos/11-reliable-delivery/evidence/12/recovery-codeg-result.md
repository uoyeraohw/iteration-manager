八个实际源文件均已通过本宿主的只读 shell 读取，SHA256 与清单全部一致；当前 HEAD 为 `1454a69b8e22e157df93f9e706502ba90833fabc`。

**A. Codeg 新流程派发**

- 同一写者已 claim 后，在支持该路径的 Codeg 持久 JavaScript 执行器中，使用冻结的 `dispatchAfterReady({request, check, dispatch})`，由守卫执行该卡的 `--dispatch-check`。检查仍 running、失败、非 READY、未知或绑定不符时，**不得原生派发**。随后另一次检查只有在真实终态、exit 0、READY 和所需绑定均匹配时，才可通过守卫调用实际原生派发；还须独立核实 claim、context 新鲜度、授权及原始回调证据。见 [agent_protocol.md:37](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:37)、[agent_protocol.md:66](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:66) 和 [execution_readiness.md:3](/data/workspace/iteration-manager/.worktrees/iter-11/references/execution_readiness.md:3)。
- 派发抛错或结果 UNKNOWN 时先查询原调用，不盲目重派；终态无法确认则保持 UNKNOWN/BLOCKED。缺持久执行器、真实工具或终态证据时，记录能力缺口、责任人和恢复条件，不回退裸派发。叶子必读文件的实际读取权限也须事先核实，真实拒绝不能绕过。见 [agent_protocol.md:66](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:66)、[agent_protocol.md:114](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:114)、[agent_protocol.md:132](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:132)。
- Codeg TOOL-call 适配、worker 实际工具执行与业务结果是不同证据。历史 worker CLI 的 bwrap 启动失败仍为 BLOCKED；父会话 completed 不能证明子命令执行或模板消费。独立 Native Codex CLI 的已证明能力也不能证明 Codeg worker 成功。[agent_protocol.md:68](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:68)

**B. 提前检查 branch**

Controller 可以做可选的 EARLY branch 结构预检，但它既不是最终验收，也不是最后一张卡完成的前提。该卡仍须依次完成实现及原始输出提交 C、独立审查 C 和冻结规格、登记收据与状态并提交 D、运行 `--local --strict`；收据的 `head_sha` 绑定 C。卡尚需独审和登记时，不能宣告整轮完成。[agent_protocol.md:142](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:142)、[agent_protocol.md:146](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:146)

同候选、输入及相关环境下的有效证据可在核对原件和适用范围后沿用；指定独立复验仍须实跑。新候选须分析影响，受影响检查重跑、受影响内容独审并重新冻结绑定；沿用测试输出不等于沿用失效批准。[agent_protocol.md:162](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:162)、[agent_protocol.md:164](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:164)

**C. 最后一张卡 12 已完成**

在题设的所有卡均有效 DONE 且各自验收 PASS 后，Controller 依次完成整轮集成路径、全量回归、独立整轮总审，再对**最终登记候选**运行冻结的 `--check-branch --strict`。总审造成候选变化时，受影响内容须重新独审并重新绑定，验证按影响判断重跑或沿用；最终 strict 和独审不能由被测候选自证批准。[agent_protocol.md:146](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:146)、[iteration_controller.md:12](/data/workspace/iteration-manager/.worktrees/iter-11/templates/assistants/iteration_controller.md:12)

收口原件按约定放在主 checkout 的 `build/iter11-closeout/<唯一UTC目录>`，README 只记摘要及链接；保留原件，归档和清理另需授权，合流、推送和部署也分别核对授权。[agent_protocol.md:148](/data/workspace/iteration-manager/.worktrees/iter-11/references/agent_protocol.md:148)

**SHA256：全部 MATCH**

| 实际源文件 | SHA256 |
|---|---|
| `references/agent_protocol.md` | `2b741176951d6bbe3a5ec125031bba8b5f2030e608b49e40ac0e50ee64a44163` |
| `references/execution_readiness.md` | `0be61f90079d5ba62842daece48f46881bd533fcdc48ce7cc015545335acaf05` |
| `references/worktree_git_contract.md` | `2f9199de428593c5dbd0999c17582f0a2a47b0d2474a731550d4e80736ef0373` |
| `templates/assistants/iteration_planner.md` | `2f8e0a31828db9635fb83aed5a333ee19178b6b3ad798c1b9b4b0f50e0eb6bc4` |
| `templates/assistants/iteration_controller.md` | `e1f30e7661e0b2058375f48abfa1e749f176d0ab58d3df1f23362cd1b9be3747` |
| `templates/assistants/task_tech_lead.md` | `2f78dd7445e06f77c61f63ed44cdb4149a9987743b3b94ed3debf56d877f0b1b` |
| `templates/sdd_implementer_prompt.md` | `15cd0b50b9faa12fbd062d0ada6af73338ba8cc16861b54297c87d61aab8498e` |
| `templates/sdd_reviewer_prompt.md` | `22067ebc67949289388d475bad26715049d83b20649be51601f4dfa4a0bc3fb5` |

本次环境提供的 `CODEX_THREAD_ID` 和 `CODEX_SESSION_ID` 均为 `01a1de1c-ab55-7fc1-afb2-967831d7e712`；`CODEG_SESSION_ID` 未提供，故为 UNKNOWN。题述新的未来恢复授权及独立安全基线批准不改变历史失败或 UNKNOWN 记录。本次仅为只读源消费，不构成任务批准或完整原生 worker 执行证据。
