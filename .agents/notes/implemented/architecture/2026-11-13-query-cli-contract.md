# Agent Note: 查询与CLI拆分的旧入口基线

Status: implemented

## Problem

查询、CLI和看板目前共处iter_sync。拆分前需要保留可复用行为基线，避免以新模块缺失代替新增字段的真实失败，也避免把结构整理说成未经量测的性能优化。

## Decision

切片A只落地量测夹具、兼容矩阵和旧入口RED，产品模块尚未拆分。量测固定10/100卡，各运行三次真实board及全部envelope；统计实际subprocess Git调用，不替换Git结果。fixture构造不计时，DONE刻意缺收据，因此量测不覆盖完整已批准候选绑定。after必须复用同一脚本和参数。

新增字段从当前可调用iter_sync.generate_board_data取得断言RED，覆盖Git/FS与有/无检查点，envelope作为同卡字段参照。测试中的attempt是投影单元夹具，不是正式收据或真实执行历史。

完整产品方案仍按03卡：query持有发现、审计和envelope，CLI只适配命令，iter_sync保留兼容门面和HTML/HTTP；消费者走query，不新增跨调用缓存。当前实现尚未达到这些结构条件。

## Existing-note audit

- [可信投影](2026-11-11-trustworthy-board.md)：部分重叠，沿用声明/验收分离与同源投影，不改HTML机制。
- [只读盘点](../process/2026-11-13-readonly-inventory.md)：部分重叠，保留单次盘点内审计复用；不得变成跨调用缓存。
- 其它自治、FS和恢复决定未被替代。

## Alternatives considered

- 先建立100个完整批准绑定候选：能覆盖更重的Git验证，但搭建成本不适合本次有界量测；采用明确限定的五状态合成样例。TypeSafe原请求响应在本卡evidence/03/slice-a-typesafe.json。
- RED后立即抽共享投影helper：TypeSafe在当时证据下推荐此切片，随后发现旧Git envelope测试明确要求candidate_id为空串。未将UNKNOWN/null要求静默套到旧字段；保留RED检查点，由契约owner澄清不适用哨兵与未知值边界再实施。原请求响应及新增反证保存在slice-a-scope-decision.json。

## Testing

本卡evidence/03中before receipt退出0，10/100各三次，每次Git调用1次；旧同步baseline为5 passed（16.51秒）。新增四组测试均在缺少三个投影字段的断言处失败，runner真实退出1且tree_terminal为true，不是ImportError。原始RED输出保留pytest生成的空白与缩进，不修饰失败日志。

## Consequences

下一会话可直接消费可复现输入、旧入口失败节点和完整签名快照，不必重做before与RED。代价是本检查点没有产品GREEN；共享查询/CLI提取、未知字段策略、after、指定回归和独立审查仍是03剩余门禁。当前最高IN_PROGRESS，不产生自批结论。
