# Agent Note: FS完整正文与看板证据根返修

Status: implemented

## Problem

1480的R5独立验收发现，profile仍接受未知键；非Git看板将项目相对证据误从迭代目录读取；FS复用Git投影会忽略ledger、勾选和显示状态，偏离早期完整正文合同；身份首尾空白也未拒绝。R6只修空文件绑定，未关闭这四项问题。原实现稿filesystem-author-r2-rejected.py的341–352行保存过滤MUTABLE_METADATA后比较完整body的依据，不能将该被拒稿整体当作有效实现。

## Decision

Ruling-SC-FS-02恢复FS专用的完整解析正文与不可变元数据相等比较，Git contract_projection保持原样。profile精确两键，合法profile派生的项目根同时用于看板和HTTP证据读取；非法profile不列证据、不降级。FS身份拒首尾空白，仍要求两个标识不同。空库存local strict保持原结构检查语义，EMPTY/退出0不代表迭代完成。

先定稿正文、冻结、独审，再只登记允许变化的元数据和收据。已登记卡若正文不同应失败；不能覆写旧冻结或补造批准使它通过。此次实现位于隔离候选，未替换三个实际安装副本，未迁移AIMovie旧收据，最终独立验收归1480。

## Alternatives considered

- 保留现有projection并仅补一条文档裁决：能沿用动态台账登记，但仍允许完整正文反例，不能恢复原FS合同，因此不采用。
- 同时收紧Git正文：实现可统一，但破坏已有Git登记合同；只增加FS专用比较。

## Consequences

FS台账、完成勾选和正文状态改动都要求新冻结与受影响重审。旧批准、预算和例外保留其原范围；历史6次及后续两次真实失败累计8，不清零。修复不提供现实身份认证，也不将synthetic工具测试当作业务证据。原[FS架构决定](../architecture/2026-11-12-filesystem-delivery.md)仅上述比较选择被取代，其余继续适用。

## Testing

本轮针对性测试先取得15个真实断言失败、4通过（退出1）；最小修复后同一测试及邻接回归75通过（退出0）。命令与进程树终态在候选包workspace/evidence的r7-red.json及r7-green.json。勾选反向变更因旧验收清单门禁已拒绝，没有声称该用例经历RED；ledger与实际可见状态行有真实RED。最终结果以原始日志及1480独立验收为准。

## Existing-note audit

原FS架构记录部分重叠，保留并互链；本返修仅取代FS正文投影选择。可信看板与有界自治记录分别继续拥有投影和预算合同，不复制修改其规则。
