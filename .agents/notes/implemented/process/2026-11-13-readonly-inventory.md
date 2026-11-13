# Agent Note: 只读续接与接管盘点

Status: implemented

## Problem

单次主控盘点需要分开读取就绪、实际验收与交接状态；不同命令各有必要信息，但反复编排造成无效等待。新会话正常续接与旧迭代接管含义不同，不能以会话是否新建来推断迁移需求。

## Decision

独立可选 `--inventory <迭代目录> --mode continue|takeover` 逐卡复用既有就绪、验收和envelope逻辑，默认输出可直接决定下一步的摘要，`--details`显示原始结构。任务及依赖的验收审计在同一盘点内按实际路径复用，不用preflight的UNKNOWN冒充验收结论。两种模式由主控按证据明确选择；接管额外给出既有缺项及迁移授权提示，续接不擅自触发接管或重跑验证。盘点不领取写者、不派发、不改变状态或产生批准，READY仍仅表示就绪。

保留旧入口、phase默认及P0显式逐卡phase选项；验收结论来自原audit而非preflight的UNKNOWN。坏卡及越界链接保留错误与库存，不拖丢其它卡；依赖/候选/预算/终态及逐次dispatch-check不被合并或豁免。

## Existing-note audit

- [可继承交接](../../implemented/process/2026-11-12-workflow-consumption.md)：部分重叠，保持其真实消费和证据复用，本篇增加只读聚合入口。
- [就绪检查](../../implemented/process/2026-11-12-execution-readiness-guard.md)：部分重叠，继续使用原phase、owner、候选和无进展规则。
- 其余既有自治/收据/恢复决定不被替代；不改业务项目，不部署副本，不实施P2。

## Alternatives considered

- 直接把preflight的UNKNOWN当成验收结果：实现简单，但无法区分真实PASS、FAIL与缺失证据；复用独立的原audit。
- 把每个旧命令输出全部拼接：可保持所有细节，但不减少上下文负担与重复审计；默认摘要并保留可展开的原结构。
- 默认把新会话视作接管：容易漏掉来源不明的历史，但会让正常续接反复补验；要求主控基于事实明确选择模式。

## Testing

先取得真实断言RED再GREEN；针对性实测覆盖混合阶段、候选与无进展阻断、未领取写者的盘点、继续/接管分支、原审计PASS和缺收据UNKNOWN、坏卡/越界、旧调用及只读。受影响的就绪、自治、模板、schema和FS控制器共122项通过（47.56秒），结果与runner终态见`build/p1-inventory-20261113/targeted.json`。复制1686隔离样例后，两种模式均经真实CLI运行并保留实际阻断；一次takeover结果与原有preflight、takeover报告及两份envelope的已保存原始结果核对一致。样例仍TESTING/UNKNOWN，不是业务项目验收。

## Consequences

摘要减少主控重复组织信息，但不能证明调用者已核对终态、授权或context新鲜度，仍须按原合同逐卡派发与验收；来源不明时选接管并保留UNKNOWN，不得通过选continue绕过现有门禁。旧入口、P2和安装副本不随本批改变。
