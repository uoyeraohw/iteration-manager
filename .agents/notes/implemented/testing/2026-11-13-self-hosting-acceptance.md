# Agent Note: 自用链证据分层与跨模块隔离契约

Status: implemented

## Problem

本轮已经有01—05真实会话和成熟单模块测试。再次模拟委派或复制全部测试会把合成数据误当真实使用，也无法证明inventory、dispatch、attempt、envelope和审计投影的联合契约。短叶子窗口不能承载最终全量。

## Decision

新测试直接复用现有数据夹具和CLI函数，组合跨模块断言；原始真实链只读取01—05卡事件、原生会话及runner收据，保留候选和终态。报告分static、synthetic、native-self-use，candidate绑定已观察BASE而不猜最终SHA。方法详见[自用验收](../../../../references/self_hosting_acceptance.md)。

TypeSafe实际未决方法评估选择compose（confidence 0.99），原请求响应在evidence/06/slice-a-typesafe.json；采用其夹具组合方向，而非补评既定六卡计划。Spike不伪造RED。首次3项失败是新测试对看板API误用，不是产品缺陷；修正签名和非空cards断言后14项通过，原输出保留。

真实03 A/B/C正常续接沿用前序RED、before及检查点，不把completed替代批准。04浏览器未受影响，保留67项及原始观察；05正文漂移正确拒绝与后续新绑定分别记录。固定协调器不改，01—05产品与旧收据不改。

## Existing-note audit

- [分层验证](../process/2026-11-12-bounded-validation-workflow.md)：部分重叠，本篇仅落地本轮联合测试与原始证据索引，不修改其验证层级。
- [就绪门禁](../process/2026-11-12-execution-readiness-guard.md)：部分重叠，继续拥有owner、attempt和无进展语义，本篇不新建事件账。
- 现有冻结/预算/恢复决定未被替代；不扩大FS恢复或部署范围。

## Alternatives considered

- 调用旧测试函数整套重演：减少新断言，但只重复已有局部覆盖，难以说明跨模块消费关系；复用其夹具而非测试主体。
- 新建独立夹具框架：隔离清楚，但重复成熟数据及冻结合同，维护成本更高；不采用。

## Testing

定向命令为`python -B -m pytest -p no:cacheprovider tests/test_self_hosting.py -q`，经固定runner留存slice-a-targeted-1/2原件，最终14passed。Note tree/format经实际Skill脚本从项目根执行，receipt在evidence/06。最终候选全量、交叉核验及独审仍由主控完成，不将旧输出冒称最终候选重跑。

## Consequences

新增少量联合契约测试，真实使用证据可追溯到原层级，避免复制平台和伪造成功。代价是主控仍须消费真实候选、全量结果及独审；报告不能代替这些门禁。完整安装和外部业务没有本轮证据，保持UNKNOWN。
