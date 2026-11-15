# 交付模式解析的一致边界

## 问题与决定

缺省声明在无 profile 时是历史 Git 合同；显式空串和未知值不能当作缺省。文件系统交付必须同时具备有效 profile 和卡的 filesystem 声明，两边不一致时拒绝。将这个无 I/O 判断放在 contracts 纯函数，派发、审计及共享交接投影各自在加载 profile 后调用，避免不同入口的独立分支漂移。profile 加载仍由原入口负责，不改变坏 profile 的异常边界。

审计记录非法模式，即使卡尚未 DONE；FUSED 与非法状态仍分别保留 BLOCKED 与 UNKNOWN，合法旧 DONE 缺收据仍为 UNKNOWN。对于合法 profile 但非法声明，共享投影返回 UNKNOWN，由已有审计 violations 填入交接 errors 和看板 findings；坏 profile 的 envelope 保留原顶层 error 及其原文，同时附带已有完整交接结构，其中模式 UNKNOWN、验收 FAIL 和来源错误；看板保留现有回退。直接投影仍抛 profile 错误，不为投影增加新字段或跨调用缓存。

## 已有决定与取舍

- [文件系统交付](../../implemented/architecture/2026-11-12-filesystem-delivery.md)规定缺省 Git、坏 profile 故障封闭及冻结绑定，继续适用。
- [执行就绪](../../implemented/process/2026-11-12-execution-readiness-guard.md)要求显式未知模式拒绝回退；共享规则扩展至审计和展示。
- [查询与 CLI 合同](../../implemented/architecture/2026-11-13-query-cli-contract.md)要求共享投影、既有异常边界和无跨调用缓存，继续适用。没有选择让投影吞掉 profile 加载异常，因为这会改变调用方既有异常合同。

合成批准夹具只用于验证审计，不代表实际任务批准；正式候选的独立审查与登记由主管处理。
