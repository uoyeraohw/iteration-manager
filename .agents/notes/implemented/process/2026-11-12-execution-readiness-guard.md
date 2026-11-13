# Agent Note: 只读就绪检查与无进展派发门禁

Status: implemented

## Problem

第一批协议已要求正常检查点、连续两次无进展不原样重派、分层验证，但现有脚本只记录修复预算和Git引用，无法执行就绪检查或携带可继承的检查点。用户批准第二批脚本优化，明确不扩展FS恢复、不迁移AIMovie、不部署副本。

## Decision

在现有CLI增设只读 `--preflight <迭代目录>` 与 `--dispatch-check <卡片> --phase <阶段>`，动态观察从显式 `--context <项目相对JSON>`读取。盘点不要求claim；实际派发检查必须已有claimed writer且owner匹配，主控在派发期间维持写权。缺输入返回NEEDS_INPUT，阻断返回BLOCKED；READY不表示验收PASS。复用现有scope、预算、Git/FS身份及依赖验收，不运行测试、不写卡、不读取凭据。

执行上下文使用version1、tasks按task_id索引，提供phase、真实candidate、inputs、capabilities、dependencies、tool_entry、checkpoint、remaining_work及带证据的authority/execution/verification观察；UI另要求ui-entry。动态输入不写进被冻结的目标正文，也不向iteration-delivery.json增加键；README仍持有工具版本、交付模式与分层验证约定。

现有 `--autonomy` 增加opt-in的attempt动作，使用原evidence参数读取项目内执行报告，先核对会话及命令终态，再把原报告与规范化快照加入现有autonomy_state.events。记录不消费/重置四预算，不新增状态账。稳定事件重放比较原报告及参数，返回原快照，不随当前候选移动重算历史；旧动作签名、payload和行为保持。命令COMPLETED须有真实整数退出码；TIMED_OUT/NOT_STARTED/ERROR且tree_terminal=true可记录为失败历史，不计为有效RED/GREEN，未知命令终态仍拒绝。这样真实超时也可进入无进展账，而不把完成状态或退出码伪造为通过。

连续两次没有新增可用产物时，新dispatch-check禁止相同输入/范围/能力的重派；改变条件须附依据，不能只改会话/候选标签。新增产物须有非空项目内原始证据，重复引用不算新进展；脚本只核对结构与来源路径，真实RED/UI语义仍由独立Reviewer核实。

交接输出只增加字段：交付模式/FS候选、最近尝试、可继承检查点、剩余工作及分列时长。没有记录时为UNKNOWN/空值，不推断纯开发或TDD编写耗时。旧调用不强制携带context、不自动记录attempt，也不被新就绪检查拦住。

`--preflight --phase-from-context`是显式可选的混合阶段盘点方式，逐卡使用context中非空合法的phase；不传此选项的现有调用仍默认implementation。`--phase`与新选项互斥，新选项不适用于逐卡dispatch-check；缺context保持NEEDS_INPUT，缺/非法phase及候选不匹配保持BLOCKED。阶段与候选不匹配保留原通用finding，并分别报告请求/实际值，便于定位；不改变现有owner、预算、无进展或验收条件。后续[只读盘点](2026-11-13-readonly-inventory.md)也显式复用该逐卡阶段选择，不扩展到dispatch-check。

派发检查在读取任务卡前拒绝解析后越出项目根的路径；preflight发现任务时保留越界链接作为BLOCKED项，不读取目标内容，也不丢弃安全任务。显式未知delivery_mode拒绝回退Git，未声明模式的旧Git任务仍沿用原默认。

## Alternatives considered

- 在旧claim中强制preflight：可覆盖所有调用，但会给现有调用增加未约定前提；仅新派发入口opt-in，不改变claim/recover。
- 外置可变JSONL尝试账：便于单独统计，但增加双写与恢复分歧；沿用卡内事件，报告是不可覆盖的输入证据而非第二状态源。
- 把动态观察写进README执行约定：便于集中读取，但冻结正文随每次尝试漂移；固定约定保留README，动态观察用显式项目内context。
- 自动将所有旧调用改为从context取phase：可少写参数，但会改变旧默认值和已有阻断结果；仅显式opt-in的盘点逐卡采用context，单卡派发保持原合同。

## Testing

核心就绪、无进展拦截及终态超时登记均取得真实断言RED/GREEN，证据在build/batch2-execution-20261112。针对性兼容及端到端测试60项通过（41.44秒），包含真实iter_run命令收据接入attempt与第三次派发拦截、FS与真实Git项目CLI、只读、缺输入/越界、同证据重复、条件变更、幂等、计数及阻断保持。独审发现未claim也可READY的所有权窗口，补真实RED后收紧逐卡派发前提，全套235项通过（202.70秒）。主代理另以真实RED定位未知type未阻断、候选移动导致历史attempt不能幂等重放；修复后执行受影响的新接口、自治、原Git恢复及模板/schema测试，84项通过（50.70秒），未重跑无关全套。合成项目工具验证不冒充AIMovie业务验收。

末次非参与者仅复核上述边界，指出已claim后省略owner会错误返回BLOCKED而非约定NEEDS_INPUT；主代理补真实RED后修正非空外来owner判定，新接口及自治测试50项通过（20.69秒）。其余窄范围未提出明确偏差。四场景指令消费覆盖旧FS调用、UI/media缺观察、无进展重派和正常/超时交接；独审不替代主代理最终验收，也不把未重跑的整套声称为最终候选全量运行。

P0阶段改进中，阶段/候选单独诊断、混合阶段盘点及旧Python入口边界分别先取得真实断言RED再GREEN；最终候选受影响的就绪、自治、模板和schema检查64项通过（31.33秒）。复制的1686隔离样例以一次新盘点得到真实无进展和授权阻断，验收仍UNKNOWN；结果与当前代码的运行收据在`build/p0-phase-20261113/`。本批不实施P1/P2、不部署副本，未重跑先前三批的全套；独审及代理场景证据以该目录记录为准。

提交前独审发现越界卡在检查前读取，以及显式未知模式误判为Git READY；隔离真实CLI复现后，分别取得行为断言RED/GREEN，缺省Git兼容用例通过。证据位于`build/main-delivery-20261113/`。

## Consequences

脚本不接管原生委派，控制器必须在新派发前消费dispatch-check结果；观察及产物的语义真实性仍需原始证据审查。当前只落地新流程显式入口，不能宣称所有旧派发已被自动拦截。FS原恢复缺口仍保持。

## Existing-note audit

[第一批规则](2026-11-12-bounded-validation-workflow.md)部分重叠，承接其方向，不改真实验证、旧卡及冻结门禁；[有界自治](2026-11-11-bounded-autonomy.md)继续拥有预算/锁/终态语义；[检查点续跑](2026-11-11-checkpoint-resume.md)仅支持原Git恢复，不被本批扩展。
