# Agent Note: 单次检查点续跑与命令截止入口

Status: implemented

## Problem

真实链已取得可继承的断言失败 RED，但会话时间中断的 FUSED 只能通过语义重规划恢复，run02 的两次 replan 已消费。命令日志又缺少同调用启动前截止核验。原四类预算不可扩大，旧 recover 不得变成解冻入口。

## Decision

新增 resume-checkpoint，外部主控授权绑定工作区、任务卡、HEAD、最近 closeout、已审查检查点和原生终态来源。干净冻结快照才可进入 IN_PROGRESS 并取得新写者；四计数和旧事件不变。成功事件派生续跑计数，固定最多三次，不另建可漂移的计数副本。相同事件完整入参重放幂等；同 grant_id 或 closeout 不得消费两次。

历史closeout的实际原因并非统一前缀，单凭字符串会误拒绝run02。保留旧原文，通过可选interruption_review绑定独立审查者、确切旧原因及最近closeout，由审查者核对原生时间中断来源；真实预算熔断仍直接拒绝。终态与分类证据从绑定HEAD的Git blob读取，不消费未提交/ignored的伪冻结证据。

统一 iter_run 先排他创建证据，启动前再核 UTC，预留五秒收尾。Windows 使用 Job Object 和启动门闩：受控 Python 引导进程进入 Job 后才接收 argv，目标及后代均属于该 Job；退出时终止并确认整个 Job 清空，避免 taskkill 根进程消失后漏杀后代。原始业务退出码和入口状态分开，超时返回124，未知清理返回125。

收尾证据写入另按用户本次明确授权处理：仅在Codex既有Filesystem MCP参数中追加本任务`build/stage10-checkpoint-resume-20261111`的绝对目录，不增加用户主目录或Skill根目录。保留原有目录及其它配置，记录本项前后文本并以精确匹配恢复。新会话须实际读取允许目录并通过该Filesystem接口创建唯一证据文件，配置落盘不能代替消费；旧会话拒绝不以shell重试绕过。只读Skill MCP保持无写入/执行工具，此项授权不改变既有只读决定。

## Existing notes audit

- [持久预算](../../implemented/process/2026-11-11-bounded-autonomy.md)：部分重叠，保留旧 recover 与四预算决定，仅增加独立续跑入口。
- [只读授权](../../implemented/architecture/2026-11-11-readonly-skill-grant.md)：部分重叠，保持只读 server 无执行工具；新 runner 走用户显式执行授权。
- 其余既有笔记不涉及检查点动作或命令截止入口，保持不变。

## Alternatives considered

- 增加 replan_limit 最少改动，但混淆时间分片和语义重规划，拒绝。
- 旧 recover 自动清阻断可复用 CLI，但破坏旧调用并穿透失败预算，拒绝。
- taskkill /T 简单，但根已退出时无法约束孤儿后代；采用有启动门闩的 Job 容器。
- 改写旧closeout原因或按interrupted关键词放行都省实现，但分别破坏历史或擅自推断；采用有独立来源、精确绑定的显式分类。
- 扩大Filesystem到用户目录可减少逐目录配置，但超出本次证据目录授权；改用另一写工具能省配置，但不能解决已发生的拒绝。采用用户批准的精确目录配置，并验证新会话实际消费。

## Testing

build/stage10-checkpoint-resume-20261111/behavior-red.txt 保存两项真实断言失败（未知动作拒绝恢复、runner未返回实际exit7）；最初API缺参失败不算RED。targeted-final.txt 的49项通过覆盖新动作、旧预算/recover、Windows实际exit7、过期不启动、父进程先退仍回收后代、超时不碰无关进程、清理未知不报PASS、Job挂接失败不启动及CLI。完整套件与独立审查、部署、实际消费状态以维护任务06为准。维护源码验收与真实业务全链分开，未完成链保持BLOCKED。

## Consequences

授权 JSON 是主控批准的能力文件而非密码学签名；宿主必须保证叶子不能改写工作区外文件，主控核实原生来源。工具只检查证据形状与绑定，不替代来源真实性审查。旧调用与预算保持，新动作增加显式交接成本而不重做有效RED。runner只在Windows启动，其他系统明确拒绝，避免交付未验证的进程回收路径。外层取消或不完整receipt不能证明命令终态，仍需原生补证。

[分层验证与可交付检查点](2026-11-12-bounded-validation-workflow.md)将正常阶段release作为优先交接路径；本篇仍仅管理真实时间中断的Git恢复，不提供FS grant或预算豁免。
