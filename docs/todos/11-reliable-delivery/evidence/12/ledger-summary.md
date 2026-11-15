# Task 12 交接记录（供唯一写者择实登记）

2026-11-15 UTC，BASE `3de06e0e3715b9f65d7caaf3bdba872a33df0f8c`，实现会话 `01a1ddcf-b505-7cc1-baac-d53be61431ab`。本产物是交接输入，不是任务卡事件账、完成批准或独审。

## 决定、依据及取舍

- 共同协议 `references/agent_protocol.md` 为新流程派发与整轮顺序权威；执行检查、Worktree图和助手/委派模板引回该协议。依据 task12 卡、README iter:goal、`references/native_dispatch_adapter.md` 与 `scripts/dispatch_guard.js`。没有增设调度器或状态账；保持角色隔离、预算、现有旧卡门禁及 C/D 绑定。
- Codeg 已验证 TOOL-call 路径使用同一次持久执行器中的 `dispatchAfterReady`；同 owner claim、真实检查终态、退出0、READY 与 request/argv/cwd/任务/阶段/候选绑定均必需。检查回调按实际 `tools.exec_command` 终态封装原始 stdout/stderr 与终态标识，派发回调调用实际 `delegate_to_agent`；仍须独立核实 claim、上下文新鲜度、原生原件和派发参数。运行中、失败、非READY、未知或不匹配不派发；未知派发结果先查询，缺能力记 BLOCKED、责任人与恢复条件。守卫不认证回调且不能拦截绕过路径。截止查询取消仍使用原生 schema 和 `deadline_watch.js`。
- 来源 `docs/todos/11-reliable-delivery/evidence/03/native-codeg-chain.json` 记录过真正的 TOOL-call 次序，但 worker 的 CLI 因 bwrap 启动失败；父会话 completed 不证明 worker 执行或指令消费。任务06 Native Codex CLI 正常链是不同宿主能力，不能覆盖该缺口。本候选两条真实新源消费均由主控后续执行，当前 PENDING。
- 场景 B 的 EARLY 结构预检仅可选，不是最终验收或卡关闭先决条件。每卡按 C → 非参与独审 → 登记 D → 冻结 local strict。场景 C 全部卡（含12）有效 DONE 与验收 PASS 后，Controller 做集成/全量、独立总审，最终登记候选才做冻结 branch strict；总审造成变更须对受影响候选重新独审。有效同候选证据不无故重跑，既定独立复验仍执行。取舍是允许早发现结构问题，但不给它最终放行权或循环前提。
- 收口原始产物按本迭代约定保留主 checkout `build/iter11-closeout/<唯一UTC目录>`，不写已审卡 scope；README 仅摘要和链接，归档/清理另需授权。未执行部署、合流、推送或清理。

## Interfaces 与观察

`dispatchAfterReady({request, check, dispatch})` 接收 `request_id/project_root/tool_entry/task_path/task_id/owner/phase/candidate/context`；`check` 返回真实 `state/exit_code/argv/cwd/request_id/terminal_evidence/stdout/stderr`，`dispatch` 返回原生结果；`dispatched` 只说明调用过回调，不是 worker 成功。详细信任边界以 `references/native_dispatch_adapter.md` 为准。流程图节点 T1→T2→T3→T4、F0→F1→F2→F3 表示卡闭合和全卡后门禁；EARLY 为可选旁支。

冻结 Linux runner 实验 `experiment-04.json`：2026-11-15T06:07:46Z 开始、退出0、进程树终态，`experiment-04.json.output.txt` 为 10 passed；合成测试检验适配骨架的 READY、pending、非READY 和带引号路径，不能代替实际原生消费。之前实验 01/02/03 分别在后续源码或测试变化前运行，原件保留。环境为指定 Python 3.11.17 / pytest 9.2.0 / MCP 1.30 与冻结 Linux runner；不扩展为其他平台或真实 worker 验证。

剩余：主控分别完成 Codeg 守卫只读探针和新源实际消费、独立 Native Codex CLI 新源消费，保存原件并裁决缺口；再冻结 C、非参与者独审、登记 D 与冻结 local strict。全部卡完成后 Controller 整轮集成/全量、总审和最终 branch strict。独审/整轮/安装/外部业务均未完成；实现者最高 TESTING。
