# P1：续接与接管只读盘点

## 范围

新增显式 `--inventory <迭代目录> --mode continue|takeover`：逐卡复用原预检与原验收审计，摘要包含实际验收、候选、阻断和可继承交接。`--details`提供同次完整preflight/handoff；同一任务作为依赖与本卡出现时复用审计。takeover额外显示旧任务缺项和授权提示，continue不自动重新接管；两种模式均不写状态，不能替代claim、实际dispatch-check、真实验证或独立审查。旧CLI和Python入口保持。

只修改维护源，不部署副本、修改业务项目或实施P2。`before/`与`baseline.patch`为本批前的P0和既有dirty基线；当前源码差异及审查快照保存在本目录。

## 真实验证

- `inventory-red.json`：实际CLI收到新入口后未能给出任务摘要，行为断言失败；`inventory-green.json`：相同用例通过。
- `inventory-cases.json`：10项通过，包含原审计PASS与缺收据UNKNOWN的区分、continue/takeover差异、详细输出、混合阶段、坏卡及项目外链接、安全库存和同次审计复用。
- `targeted.json`：最终脚本行为及受影响的就绪、自治、模板/schema、FS控制器共122项通过（47.56秒），receipt保留真实退出码与进程树终态。
- `consumer-project/evidence/p1-inventory-{continue,takeover}.json`：从此前1686隔离样例的副本实际运行两种模式，均返回原有无进展/授权阻断和UNKNOWN验收；takeover多报告缺收据。与已保存的原preflight、takeover和两份envelope逐项核对一致；退出3表示真实BLOCKED。
- `prompt-final2.json`：最终文档变更后4项模板/schema检查通过。新上下文代理真实读取候选文档及样例输出，未执行命令；首位非参与者审查未发现可复现阻断但未给正式裁决。文档纠正后，另一位非参与者对最终候选只读独审 **APPROVED**，未独立运行测试。详情见 `review.md`。

上述FS PASS检查使用合成收据和快照，只验证工具契约，不代表真实业务验收；隔离样例也不能计算真实项目节时比例。`missing`是延续旧报告的字段库存，尚未完成任务缺review_receipt不自动等于失败或需提前审查。P0旧调用和已有独审继续保留，不重复运行无关全套。
