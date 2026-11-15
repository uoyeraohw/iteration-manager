# Agent Note: 旧接管报告逐卡读取隔离

Status: planned; implementation candidate awaiting independent review.

## Problem and decision

旧 `--takeover-report` 在调用审计前直接解析每张卡，单卡读取错误中断整份 JSON。沿用只读 inventory 的逐卡异常隔离思路，在 CLI 新增 `_takeover_task`，只在单卡操作处记录异常、UNKNOWN 和未知 missing；目录与参数验证仍留在报告外围。成功路径仍使用原 parse/audit、字段、发现规则和顺序，不新增调度器或跨调用缓存。审计自己捕获的后续读取错误保留其 FAIL 和原因；首次解析成功所得 missing 仍为已知值。

## Existing decisions and alternatives

已检索 `.agents/notes/`：`implemented/process/2026-11-13-readonly-inventory.md` 的逐卡阻断与只读原则适用；`implemented/architecture/2026-11-13-query-cli-contract.md` 的旧入口、调用合同和无跨调用缓存边界继续有效。复用整个新 inventory 会改变旧报告形状、根目录约束及调用语义；整个报告外层捕获会丢失健康卡和错误卡，因此均未采用。不修改 query/discovery，避免改变已冻结依赖。

## Evidence and limits

`evidence/02/red-01.json`、`red-02.json` 记录修复前断言失败，分别覆盖真实坏编码、合成读取 OSError 和发现后合成删除；`green-02.json` 是最终测试输入下的四文件 GREEN/regression。末次追加的解析与审计之间删除及畸形卡用例未先 RED；测试夹具中的删除由测试显式执行，剩余文件逐字节对照。合成故障不是外部业务验收。原生命令及进程树终态见各收据；实现者不批准，C、独审、D 和冻结 local strict 留给 Controller。
