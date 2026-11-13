# Agent Note: 共享查询与旧入口兼容边界

Status: implemented

## Problem

查询、CLI和看板目前共处iter_sync。拆分前需要保留可复用行为基线，避免以新模块缺失代替新增字段的真实失败，也避免把结构整理说成未经量测的性能优化。

## Decision

切片A的量测固定10/100卡，各运行三次真实board及全部envelope；统计实际subprocess Git调用，不替换Git结果。fixture构造不计时，DONE刻意缺收据，因此量测不覆盖完整已批准候选绑定。after必须复用同一脚本和参数，不因查询提取重做before。

新增字段从当前可调用iter_sync.generate_board_data取得断言RED，覆盖Git/FS与有/无检查点，envelope作为同卡字段参照。测试中的attempt是投影单元夹具，不是正式收据或真实执行历史。

iter_queries持有发现、审计、envelope及其直接依赖的Git读取和阶段解析。iter_sync重新导出全部旧符号和签名，保留CLI与HTML/HTTP。board和envelope调用同一task_handoff_projection，board只追加delivery_mode、candidate_id、execution；Git candidate_id保留已知不适用空串。坏profile不降级，board新增字段以UNKNOWN/null表示不可用。

inventory、preflight、execution直接读取query；inventory的audit字典仍只在一次调用中存在，依赖审计和envelope共用结果，下次调用重新审计。CLI模块提取、after、八文件交付回归和独审留给切片C，不宣称本切片完成03。

## Existing-note audit

- [可信投影](2026-11-11-trustworthy-board.md)：部分重叠，沿用声明/验收分离与同源投影，不改HTML机制。
- [只读盘点](../process/2026-11-13-readonly-inventory.md)：部分重叠，保留单次盘点内审计复用；不得变成跨调用缓存。
- 其它自治、FS和恢复决定未被替代。

## Alternatives considered

- 先建立100个完整批准绑定候选：能覆盖更重的Git验证，但搭建成本不适合本次有界量测；采用明确限定的五状态合成样例。TypeSafe原请求响应在本卡evidence/03/slice-a-typesafe.json。
- RED后立即抽共享投影helper：TypeSafe在当时证据下推荐此切片，随后发现旧Git envelope测试明确要求candidate_id为空串。未将UNKNOWN/null要求静默套到旧字段；保留RED检查点，由契约owner澄清不适用哨兵与未知值边界再实施。原请求响应及新增反证保存在slice-a-scope-decision.json。
- 为兼容旧测试向iter_sync注入跨模块monkeypatch转发：可保留旧观测点，但引入与查询所有权无关的注册机制。本次直接接线query，不增加转发；TypeSafe请求/响应在slice-b-typesafe.json。旧test_execution_readiness.py:180只patch同步模块，不能再观察inventory审计；白名单外测试保持原样，由主控授权后适配观测点。

## Testing

本卡evidence/03中before receipt退出0，10/100各三次，每次Git调用1次；旧同步baseline为5 passed（16.51秒）。新增四组测试均在缺少三个投影字段的断言处失败，runner真实退出1且tree_terminal为true，不是ImportError。原始RED输出保留pytest生成的空白与缩进，不修饰失败日志。

切片B沿用这四项有效RED，核心GREEN为4 passed；query与旧同步针对性检查为13 passed（slice-b-query-compat-1742.json，退出0）。B补充的4项测试没有先RED，覆盖旧签名、无反向导入、调用内复用/调用间重新审计、未知状态和坏profile拒绝。第一次单文件运行因缺PYTHONPATH收集失败（退出2），不是行为RED；后续命令显式设置PYTHONPATH为本工作区scripts，测试文件也按现有惯例补齐独立导入路径。

## Consequences

下一会话可直接消费查询层、投影GREEN和完整签名快照，不必重做before与RED。旧测试的同步模块monkeypatch观测点需要主控处理；这不是对审计复用的豁免。CLI提取、after、指定回归和独立审查仍是03剩余门禁。当前最高TESTING，不产生自批结论。
