# 三助手共同执行协议

本文件管理角色、自治和恢复；任务格式及完成收据以 [task_card_schema.md](task_card_schema.md) 为准。整轮主控与单任务入口使用同一门禁。

## 先确认授权与能力

读取项目约定、cwd、分支、完整HEAD、dirty归属、任务type、Interfaces、范围和验收。只读分析/只生成Prompt不写文件、不运行实现、不提交用户已有变更；可给带“执行前需通过规划提交门禁”的预览。实际创建Worktree或执行任务前才运行 `--verify-committed`，非零时分清Git错误与dirty，不自动暂存整个docs/todos。

不假定嵌套委派、深度或并行容量。启动时阅读本环境实际工具schema；没有下级委派能力时，技术主管返回所需角色的自包含Brief，由具备工具的上层串行派发，回收后继续。缺独立审查能力保持TESTING/BLOCKED，不自行批准。

## Codeg工具协议

当本环境提供Codeg MCP时，按其实际schema调用，例如：

```json
{"assistant_id":3,"working_dir":"C:/project/.worktrees/iter-01","task":"完整Brief：目标、任务卡绝对路径、BASE、授权文件、type契约、测试命令、时限、检查点、证据、提交权限及返回格式"}
```

上例是 `delegate_to_agent` 的参数，不是命令。指定助手用 `assistant_id`，指定代理用 `agent_type`；遵守用户路由，不凭名字猜ID。保存返回的task_id与启动时间。使用 `get_delegation_status({"task_ids":["实际ID"],"wait_ms":60000})` 有界等待；运行时支持的通知可替代轮询。读取终态完整text/结果与原始证据，不能把completed或“代理停止”当验收PASS。blocked_on携带实际用户请求时只呈报受影响依赖；普通运行等待不发状态噪音。

中断、unknown或通信失败先查询原task_id及其会话/工作区，不重复派发；completed任务不能resume。需要返修时先确认原执行者终态，再以新任务携带剩余目标和已交证据，不重做已验收工作。仅在授权停止、超任务时限或无继续必要时，按工具schema使用cancel_delegation；取消后查询终态，不遗留活动命令。遵守用户时限；未另定时探索/审查以5分钟为检查点，累计10分钟必须介入停止并保留部分成果。

### 分层时间预算与超时收尾

时间预算与修复次数分开。主控以实际启动时间记录绝对hard_deadline，受本次授权及单会话10分钟介入停止上限约束；预留至少90秒closeout_reserve，work_deadline = hard_deadline - closeout_reserve。主管继承这两个绝对时点，不把整棵子树再压进固定150秒；主管的可用预算是全局剩余时间，不是叶子的单次时限。

每次派发测试、实现或审查叶子前，必须有独立至少120秒的可用工作窗口（含冷启动与工具时间）；不足就停止派发并收尾，不以缩短叶子时限或反复重启主管挤入剩余时间。叶子早交付可提前回收；不得因此省略后续门禁。等待取`min(60000, 距下一检查点/叶子截止/work_deadline的剩余毫秒)`，临近边界缩短等待；到work_deadline停止业务执行并取消未结束下级，预留窗口用于查询终态、保存证据、收尾和提交，而非继续实施。

派发前即时读取时钟，锁定`leaf_deadline = min(work_deadline, dispatch_requested_at + leaf_limit)`，默认另留10秒cancel_reserve；剩余工作窗口（扣除该余量）不足120秒不派发。Brief写确切UTC，不写“启动约某时”。派发后记录实际创建时间，核对冷启动消耗；不得后移已承诺截止。deadline、取消请求发出与确认时间分别保存，工具响应超出余量时如实记录late_by，不声称严格达标。

**临界等待、重新读钟与取消须在同一次JavaScript工具执行中连续完成，不在最后一次等待返回后回到模型再决定取消。** 使用[截止守卫](../scripts/deadline_watch.js)的完整函数体，在支持持久异步执行的工具执行器中调用；执行器yield后该循环继续运行，外层只等待同一执行单元，不重启监控。循环保存原始响应，检查点只登记事件，不停掉守卫；terminalConfirmed只说明会话终态，不证明命令终态或产品验收。无这种运行能力时，在派发前返回能力缺口，不退回逐轮模型估时。

Codeg适配示例（先在同一执行单元放入上述函数体；ID及截止必须来自真实派发）：

```javascript
const result = await watchDeadline({
  deadlineMs: leafDeadlineMs,
  checkpoints: checkpointEpochMs,
  query: async waitMs => {
    const args = { task_ids: [taskId] };
    if (waitMs !== undefined) args.wait_ms = waitMs;
    const raw = await tools.mcp__codeg_mcp__get_delegation_status(args);
    const parsed = raw.structuredContent ?? JSON.parse(raw.content[0].text);
    return { ...parsed.tasks[0], raw };
  },
  cancel: () => tools.mcp__codeg_mcp__cancel_delegation({ task_id: taskId }),
});
text(result);
```

单个守卫管理一个实际task，不接管业务调度或卡片写权；父级仍须核对完整子树。unknown/查询失败时尝试取消并保留实际查询结果，未确认终态保持BLOCKED。`wait_ms=0`是无限等待，轮询必须省略该字段。blocked_on事件必须呈报用户；等待用户时守卫仍运行，不自动延长授权期限。

叶子的每个业务、测试和验收命令必须通过[统一截止入口](checkpoint_execution.md)`scripts/iter_run.py --deadline <明确UTC> --evidence <项目相对唯一receipt> -- <argv...>`执行；派发Brief提供确切command_deadline（不晚于取消点），入口内另留5秒回收。由入口同次核UTC、落原始输出及真实业务退出码，禁止先运行再补日志。PowerShell保存`$LASTEXITCODE`后须`exit $code`；shell退出0不代表pytest通过。124/125须看receipt状态，超时不算断言失败。原生命令补证仅作为新的来源证据，不改旧日志；进程列表不能补造历史退出码。当前入口仅支持Windows Job；入口或权限不可用就报告能力缺口，不回退裸命令。

叶子必读契约须在派发前确认其运行时具有实际读取权限；主控能读取不代表叶子能读取。出现真实拒绝时返回权限缺口，按宿主正式授权机制解决；不尝试其它工具或另一副本绕过。

用户明确授权新增受控读取能力时，可按[只读授权通路](readonly_skill_access.md)注册限定cwd和逐项文件的只读MCP服务；保持原生读写范围不变。必须先取得新会话实际调用该授权接口的证据及独立验收，再恢复依赖契约的执行；注册本身不算消费通过。

超时不是代码修复失败，不用fix虚增计数。当前唯一写者从项目根调用：

```powershell
python <skill_root>/scripts/iter_sync.py --autonomy closeout <任务卡> --event-id <稳定收尾ID> --owner <当前写者> --executor-state canceled --reason "execution deadline; 具体阻断与恢复条件" --evidence <项目内实际非空终态证据文件>
```

executor-state只接受实际查询得到的completed/failed/canceled；unknown不能冒作终态或释放活跃写者。closeout原子登记FUSED/is_blocked/原因并释放写者，不清四类计数；重放幂等，CLI退出3表示成功登记了阻断，不是实现通过。已有预算耗尽原因保留，新的收尾原因留在事件输入中。DONE不可改。普通claim/fix不能清除超时阻断，恢复须明确授权的新计划与真实补验。

用户明确授权检查点续跑时，可由主控签发工作区外短期能力，通过`--autonomy resume-checkpoint --resume-grant <外部JSON>`绑定干净HEAD、最近closeout、已审查检查点与真实终态。固定最多3次，只解除execution deadline中断、不改四预算或旧recover；真实预算熔断、重复消费和unknown拒绝。详细字段、排他收据与分阶段交接见[检查点与命令契约](checkpoint_execution.md)。主控签发，实际主管消费，叶子不得自行续签。

若主管异常退出，只有事先明确授权的父级元数据恢复者能接管：先查询并保存整个已派发子树及旧卡片写者的原生终态；确认无活动卡片写者后，以旧owner执行release并记明实际恢复者，再claim自身、closeout、精准提交卡片/证据。不得冒称自己就是旧会话，也不得在原执行者仍running/unknown时抢写。底层工具命令状态未交付时，原因和证据明确保留`UNKNOWN command state`，仅做已授权的元数据收尾，不声称进程已停止，不启动新的业务/测试执行者，不清理未知进程。当前写者正常收尾不另冷启动一名主管；父级不得因写卡权限缺口将外部BLOCKED留成卡内未阻断。

### unknown与缺输入时的返回形状

`unknown`只说明当前查询方没有可取记录，可能是会话归属或记录被回收，不能据此断定执行者已停止。由原派发会话查询并回传完整终态；同时只读核对明确工作区的git status/log及原始证据，磁盘没有变化不能证明代理已停止。终态无法确认时保留UNKNOWN/BLOCKED，不关闭或重复启动执行者。

桥接Brief只填写实际提供或工具核实的cwd、完整BASE/C/contract引用、卡片路径、角色回避名单和证据。缺字段写UNKNOWN并列出原派发者需补齐的输入；状态为NEEDS_INPUT，不伪造哈希、角色名、证据路径或已获授权。示例必须标明“示例，不能执行”，不能放入声称可立即派发的Brief。dirty不等于允许清理；保留他人改动，执行前按具体门禁和归属解决，不要求全局清空。

## 唯一写者与独立审查

同一任务卡同时只有一个写者。技术主管领取逻辑写者owner；下级测试作者/实现者只写各自授权文件，任务卡变更由主管串行登记；确需实现者写卡时先交接，回收前主管不并发写。其它角色只返回证据。`--autonomy claim/release`登记写者；release需已查询终态及证据。物理临时锁遗留时先核对无活动写者，再在授权内移除该精确锁；不自动破锁。

测试作者、实现者、本任务RCA/方案设计参与者均不能担任独立Reviewer。独立Reviewer读取冻结规格、实际候选与原始输出，返回发现及裁决；主管可读冻结Diff并运行独立验收。实现者最高TESTING。会诊不是APPROVED；建议先核对正确性、契约、范围与授权，不自动采纳方案A，不放宽失败路径。

提交实现C及原始输出 → 独立审查C与冻结规格 → 主管登记JSON收据、报告及状态 → 提交登记D → `--local --strict`。head_sha绑定C，不冒填当前HEAD。整轮全部验收PASS后独立全分支审查及 `--check-branch --strict`；合流、发布、删除另按授权执行。

## 持久预算与恢复

`autonomy_state`是任务卡内自治事件/计数的唯一真源，JSON以单行JSON字符串存于扁平frontmatter。`fix_rounds`是兼容投影；不手工清零。启动前可选 `autonomy_policy` JSON字符串，字段默认 `round_limit=5,total_limit=10,consilium_limit=1,replan_limit=2`；运行后策略变化需要明确迁移，不能会话重启时另设默认。普通Ruling不计重规划。

```powershell
python <skill_root>/scripts/iter_sync.py --autonomy claim <任务卡> --event-id <稳定ID> --owner <主管会话ID>
python <skill_root>/scripts/iter_sync.py --autonomy fix <任务卡> --event-id <修复尝试ID> --owner <主管会话ID> --reason <实际失败>
python <skill_root>/scripts/iter_sync.py --autonomy consilium <任务卡> --event-id <会诊ID> --owner <主管会话ID> --reason <根因问题> --evidence <诊断输入路径>
python <skill_root>/scripts/iter_sync.py --autonomy replan <任务卡> --event-id <重规划ID> --owner <主管会话ID> --reason <已核对的裁决> --evidence <会诊及授权证据路径>
python <skill_root>/scripts/iter_sync.py --autonomy recover <任务卡> --event-id <回收ID> --owner <主管会话ID> --executor-state completed --evidence <查询原任务终态的证据>
```

每次已完成而失败的修复记录一次fix，同一次回收始终复用事件ID；同ID不同输入拒绝写入。第5次失败停止修复，允许预算内诊断与重规划；会诊在启动前消耗预算；重规划只重置当前轮，不清累计。累计10次、会诊或重规划超额时保留FUSED，验收为BLOCKED，不继续自动修复、不扩大范围。恢复查询、重复回收、重启均不能清零。

退出2表示数据/归属错误；退出3为预算阻塞。达到上限保存代码、原始输出、完整引用、未闭环问题、活动命令终态及恢复条件，向实际权限持有人请求具体决策，不反复问“继续吗”。恢复需要新证据/经授权计划或显式预算迁移；不能只改状态恢复绿色。旧 `--record-fix`入口保留并按head_sha+摘要去重，新流程必须使用显式ID。

## 接管、新建与重规划

旧迭代先 `--takeover-report <迭代目录>` 只读列状态、缺项和补验建议。保留历史Commit/状态/原始证据，缺收据为UNKNOWN，不补造历史RED/APPROVED。格式迁移与补验只有取得相应授权才写入；严格门禁不因“存量”自动豁免。

新建按type生成可验证阶段与Interfaces，再按 [TypeSafe指南](typesafe_eval_guide.md) 实际评估；无真实结果为UNASSESSED。重规划保留历史证据，在ledger记录具体Ruling及范围、依赖和补验影响；超授权只阻塞受影响部分，继续独立的已授权工作。
