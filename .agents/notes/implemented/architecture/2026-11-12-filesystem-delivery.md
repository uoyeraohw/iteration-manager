# Agent Note: 显式文件系统收据与冻结绑定

Status: implemented

## Problem

AIMovie采用获准文件快照交付，默认Git提交绑定不适用。跳过Git而不绑定代码、原始证据和冻结规格，会把缺证据误投影为通过；复制一套类型校验又会使默认门禁与新模式漂移。

## Decision

本记录关于FS任务contract_projection的选择由[完整正文绑定返修](../bug-fix/2026-11-12-filesystem-r7-acceptance-repair.md)部分取代；以下保留原决定及原验证的历史归属，其他路径、空文件与Git边界继续适用。新候选尚待1480独立验收，未部署安装副本。

文件系统模式由迭代内iteration-delivery.json显式启用，缺配置沿用Git、坏配置故障封闭。共享validate_receipt保留默认Git合同，仅在明确filesystem参数下校验当前文件系统收据身份；独立iter_filesystem模块负责路径包含、scope完整库存、逐字节快照、任务contract_projection及迭代README目标绑定。普通scope源与快照允许零字节，仍须存在、为文件、在项目内并逐字节一致；check.output、报告、manifest及规格/目标文件保持非空。contained默认调用保持非空，仅文件绑定与scope库存显式允许空文件。源码、check.output和冻结快照不能交叠；不建立内容哈希替代合同。分支与全局strict遇到该profile直接记录门禁违规，不把本地文件系统收据替代原Git完成收据；普通非strict汇总仍可展示本地投影。

收据明确标记current-filesystem-review-v1与当前带时区时间，不允许非空Git SHA。唯一新增check形式是文件系统UI原生interaction observation，必须说明工具、时间和原始输出；RED和regression不借此跳过命令与退出码。历史例外、缺证据与预算分别保留，工具不自动签发旧任务收据。

## Alternatives considered

- 复制完整FS类型校验：可以隔离新模式，但两份被拒稿已暴露类型、kind和路径接口误用；采用共享校验减少漂移。
- 只豁免Git并恒定UNKNOWN：能显示兼容入口，但不能完成冻结验证；不采用。
- 为旧卡补造SHA/历史收据或把预算归零：可获得表面绿色，却丢失来源和限制；拒绝。

## Testing

公共audit_task_file四类synthetic正例取得真实断言RED（4 failed，退出1）；修正候选针对性84 passed，补充scope/状态/目标/真实symlink负例后43 passed，R4完整工具回归180 passed（171.50秒，退出0）。R4两名独审批准后，主控新增clean Git反例，发现分支与全局strict错误接受无Git SHA的文件系统收据；2个真实断言失败，按一个失败候选累计登记，退回作者加入口边界，不沿用被反例推翻的审查结论。原始命令、时间、退出码与进程树终态位于build/filesystem-controller-r3。synthetic夹具只验证检查器，不是AIMovie业务完成证据。R5完整回归182通过并完成受影响独审。真实AIMovie当前收据实跑暴露21个历史空日志被错误拒绝，兼容候选累计从6续7；R6保留全部历史空文件和冻结候选，仅修正源/快照的非空误用。新增测试先在公共API取得2个真实断言失败、3通过；3处错误字段访问先按现有violations接口修正，不将夹具异常当RED。R6完整回归186通过、两安装副本各50通过，受影响新非参与者独审APPROVED。07格式清单另冻结重审后，实际安装入口local strict退出0、AIMovie7/7通过。原始命令与结果见项目current-closeout-20261112记录。

## Consequences

文件系统本地strict可以核对当前候选与证据漂移，旧卡不会因此自动通过。正式业务补验与当前独审收据仍由实际任务负责人取得。快照和manifest需放源scope之外，目录授权会使新增文件触发重审。分支/全局提交前提不被本地模式免除。

## Existing-note audit

[可信看板](2026-11-11-trustworthy-board.md)部分重叠：继续使用其统一库存与真实状态投影；[有界自治](../process/2026-11-11-bounded-autonomy.md)部分重叠：预算真源及熔断保持，不在新模块另建预算。其余命中的checkpoint/stage01笔记管理历史阶段与截止协议，与本次绑定决定无冲突。

