# Agent Note: 三助手配置部署与实际消费分离验收

Status: implemented

## Problem

第二批权威Prompt文件已通过验收，但Codeg三个真实助手仍是旧指令；文件更新不等于运行时采用。三个Skill副本均是独立目录，候选不能提前覆盖另外两份。

## Decision

2/3/4号助手的instructions精确采用主版本对应权威模板，保留agent、options、名称和身份。部署前保存三个目标行的身份、原指令、revision和updated_at；事务以原revision和原instructions作并发比较，更新revision及updated_at，不触碰其它助手或会话。新会话消费与配置内容相等分别取证；只读测试不得执行任务或补造批准。回滚只恢复此部署实际修改的字段，并先核对当前仍是本候选，不覆盖后续用户修改。

当前CLI没有配置写入入口，原生CUA不可用，采用已核对schema的本地SQLite事务，不复制整个运行中数据库或读取凭据。整轮PASS后才同步Skill交付源码/模板/测试/决定记录，排除build、缓存、维护任务；先备份精确目标文件，内容直接比较，不计算摘要。

## Alternatives considered

- 等待用户逐项UI编辑：贴近日常配置，但当前自动化管道不可用，会把已授权实施转回用户管理；保留为CLI/schema变化时的手动恢复路径。
- 只给助手一个模板路径：短且单源，但运行环境不保证自动读取；部署完整权威模板，模板自身要求读取共同协议。

## Testing

build/stage04-20261111/assistants-before.json保存部署前目标字段，assistants-deployed.json精确回读。三个revision从8/5/4变为9/6/5，指令与权威源相同。build/stage03-20261111/deploy_assistants.py --restore提供目标字段回滚，当前有后续变更时拒绝覆盖；--check-restore已在事务内校验旧指令并ROLLBACK，实际配置不变，原始输出restore-dry-run.json。不声称执行过提交式回退。

用户授权的2/3/4号助手只读新会话1507/1508/1509均终态完成。consumer-native-snapshots.json对conversation.assistant_snapshot.instructions与对应权威模板直接比较一致，证实原生注入；consumer-results.json保留消费结果：缺SHA/身份不启动，重启不清零，旧DONE缺收据保持UNKNOWN，拒绝默认质量分。测试前后60份保护文件直接比较无差异，见consumers-readonly-comparison.json。消费发现旧表冲突，按[可信投影决定](../architecture/2026-11-11-trustworthy-board.md)有限修复，不改历史夹具使其迁就代码。

真实沙箱已产生初始断言RED→35 GREEN；主线程反例发现不可哈希str子类，补行为断言RED→36 GREEN与回归，独立session1502批准C2。返修session1501超时取消后查询终态、保留代码/日志、主线程收尾提交；recover重复事件幂等，实际累计修复1不清零。另有明确标为受控故障注入的10次跨进程预算探针，不冒称10次真实代理失败。

## Consequences

SQLite写入不提供热采用保证，本次证据覆盖已部署指令的新会话实际只读消费，不代表存量会话热更新。仅本次只读消费采用用户授权的assistant_id例外，其它委派仍走Antigravity；整轮独立验收通过前不同步副本。与既有[有界自治协议](2026-11-11-bounded-autonomy.md)部分重叠，沿用角色和计数规则，不新增任务状态真源。首轮沙箱写者/IN_PROGRESS登记滞后至返修期间，保留完整控制器从启动自动链未覆盖的测试局限，不回填不存在的历史状态，也不把只读消费当作自动实现全链证明。
