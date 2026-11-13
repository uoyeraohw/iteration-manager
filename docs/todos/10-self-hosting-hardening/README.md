# 迭代10 · 规则一致性、使用简化与真实自用健壮性

> **进度指示**：声明DONE [2/6] (33.3%) · 验收PASS [2/6] · 状态：🟡 进行中
> 分支：`feat/iter-10-self-hosting-hardening`；独立工作区：`.worktrees/iter-10`，从规划提交`d3bd97ab16ffed6104034a887a01eb1b4d75dc0e`创建。
> 用户已批准启动实施、精准Git提交与独立Worktree；按六卡串行验收推进。禁止部署、推送、合流或清理。

## 1. 迭代核心目标与全局约束

<!-- iter:goal -->
### 目标
把现有iteration-manager用于管理自身这轮改进：统一相互冲突的授权指令、减少手工模板转换、提供一致查询与Git/FS交接展示、整理发布事实，并在真实任务推进中验证健壮性。任务状态唯一真源仍是本目录卡片；不新建另一套任务系统。

### 基线和执行约定
- 项目：`C:/Users/qingyu/.codeg/skills/iteration-manager`，初始化观察分支main，源码提交`46ded3a4696e3bdb531d06951fce7982fa9db1cd`。
- 初始化前dirty仅未跟踪`.codegraph/`；保留，不暂存、删除或认定其获本轮修改授权。实际执行前重新核对，不把历史快照当当前状态。
- 最新用户授权：同意启动迭代10，实施、精准Git提交、创建独立Worktree；六卡串行，每卡验收PASS才进入后继。暂不部署、推送、合流或清理。初始化阶段的授权限制保留为历史，不再作为实施前提。
- 交付模式：本迭代真实任务采用Git。FS只作为新模板/看板及隔离验收样例，不把真实任务切换FS来绕开提交。
- 协调器固定为`46ded3a4696e3bdb531d06951fce7982fa9db1cd`的完整源码/契约，已在确认目标不存在后以Git树导出到主仓库`build/frozen-tools/46ded3a/`。固定绝对入口`C:/Users/qingyu/.codeg/skills/iteration-manager/build/frozen-tools/46ded3a/scripts/iter_sync.py`，runner和deadline_watch取同一目录；不更新该副本。
- 被测候选为iter-10工作区代码。所有任务卡调度/自治/正式门禁使用冻结协调器；候选查询/生成/看板作为被测对象另行验证，不能用正在修改的检查器给自己签发批准。
- 冻结版本中已知Worktree文档冲突由更高优先的当前授权、SKILL.md与共同协议约束；任务01修复候选，不修改固定副本。若固定工具发现真实门禁缺陷，停止受影响放行并保留证据，经单独裁决决定修复/迁移；不能自动更新协调器。
- **角色**：主控兼主管可协调，不写产品代码；实现owner负责同任务RED/GREEN和返修；非参与者独立Reviewer。规划/实现/测试/RCA参与者不能自审；整轮独立总审另行安排。执行前按真实工具schema确定代理路由和容量，不填虚构assistant_id。
- **调度**：01→02→03→04→05→06串行；当前卡PASS与有效收据齐备才推进后继。不同卡源白名单不交叠；后续发现接口问题返原owner重审受影响候选，不能直接让下一卡越界修改。
- **预算/时间**：保持5/10/1/2四预算及两次无进展门禁；每个实际会话按10分钟上限介入，至少90秒收尾、叶子至少120秒工作窗口。绝对UTC在实际派发即时锁定；正常检查点先交付，不将整张卡硬塞进一个会话。
- **三级验证**：内环针对节点，任务交付按卡的type checks和受影响回归，整轮在最终候选运行`python -B -m pytest -p no:cacheprovider tests -q`、真实浏览器/原生自用链、非参与者总审和冻结工具`--check-branch --strict`。
- **命令证据**：业务/测试/验收通过冻结iter_run保存同次原始输出和真实退出码；正式证据在`docs/todos/10-self-hosting-hardening/evidence/<task>/`，规划证据单独在planning/。可再生输出用现有pytest临时目录或卡内sandbox；不删除旧证据。
- **候选冻结**：Git实现C与原始输出→独审C/contract→登记D→本地strict；head_sha绑定C。新增源码或证据漂移按影响范围重审，新批准不套旧收据。
- **部署边界**：不改Codex/Gemini安装或助手配置，不迁移旧卡/旧收据，不执行真实用户业务项目。源码、样例、原生自用、安装和外部业务验收分别报告。
- **本轮非目标**：跨平台runner、FS超时恢复、新数据库/调度服务、跨调用验收缓存、第五种type及旧Refactor-Benchmark降门禁。性能只做任务03结构整理前后量测，不预设优化收益。

### Review Focus
1. 授权冲突：仅Prompt/无Git权限/他人dirty/未授权合流，任务01用新会话消费验证。
2. 类型与冻结：八种模板组合不伪造RED/批准，FS不残留动态正文与SHA，任务02验证。
3. 兼容与事实一致：旧CLI/导入、候选/检查点与各投影一致，03接口测试＋04真实UI验证。
4. 不误放行：缺证据、坏profile、越界读取、依赖未完成、预算/终态未知保持拒绝，既有测试＋06隔离负例。
5. 自用不自证：冻结协调器、候选、Reviewer和证据分离；真实新会话续接不重复验收，06汇总原生记录。
<!-- /iter:goal -->

## 2. 六卡任务索引

| 任务序号 | 任务名称 | type | 前置 | 状态 | 详细卡片索引 |
| --- | --- | --- | --- | --- | --- |
| 01 | 统一授权规则与跨入口场景 | Spike-Discovery | 无 | 🟢 已完成 / 验收:PASS | [01-authority-consistency.md](./01-authority-consistency.md) |
| 02 | 按类型与交付模式生成和检查任务卡 | Strict-TDD | 01 | 🟢 已完成 / 验收:PASS | [02-typed-template-generation.md](./02-typed-template-generation.md) |
| 03 | 稳定查询与CLI消费接口，保持旧入口兼容 | Strict-TDD | 02 | ⚪ 待开始 / 验收:UNKNOWN | [03-query-cli-contract.md](./03-query-cli-contract.md) |
| 04 | 看板展示Git/FS候选和可继承交接 | UI-Component | 03 | ⚪ 待开始 / 验收:UNKNOWN | [04-board-handoff.md](./04-board-handoff.md) |
| 05 | 建立源码、候选、安装与消费的发布证据索引 | Spike-Discovery | 04 | ⚪ 待开始 / 验收:UNKNOWN | [05-release-evidence-index.md](./05-release-evidence-index.md) |
| 06 | 真实自用链路与故障路径健壮性验收 | Spike-Discovery | 05 | ⚪ 待开始 / 验收:UNKNOWN | [06-self-hosting-acceptance.md](./06-self-hosting-acceptance.md) |

### 规划取舍
原五卡方案把查询/CLI与看板集中在一张卡，首轮TypeSafe的单一职责仅62.5，未过70门槛。现拆为03数据接口与04展示消费，源码范围不交叠；未改变的01、02、发布索引、最终自用评估沿用原结果，仅重评实质变化的03/04。不是重复刷分。
纯重构与性能优化的未来type拆分记录为本轮非目标；现有四type合同保持。当前架构不整体重写，不为压行数拆分。

## 3. 初始化质检

- 门槛：四维权重30/30/20/20；总分≥80且每维≥70。
- 真实模型：`jev-1.14.0`；五等级按score/4×100换算，不把confidence当质量分。
- 原始请求/响应、第一次不通过与实质调整均保存在[evidence/planning](evidence/planning/typesafe-summary.json)。
- 主管判断：六个责任域可串行交付；03/04通过明确接口分离，允许多会话检查点，不缩减独立审查。分数仅证明规划门禁，执行仍待授权及就绪观察。

| 卡 | 粒度 | 明确度 | 单一职责 | 可执行性 | 加权总分 |
| --- | --- | --- | --- | --- | --- |
| 01 | 94.50 | 87.75 | 83.25 | 84.75 | 88.275 |
| 02 | 94.75 | 96.00 | 85.75 | 83.25 | 91.025 |
| 03 | 97.00 | 95.50 | 88.75 | 83.25 | 92.150 |
| 04 | 93.50 | 88.75 | 90.25 | 77.75 | 88.275 |
| 05 | 87.75 | 82.50 | 80.75 | 71.50 | 81.525 |
| 06 | 82.50 | 98.75 | 80.50 | 86.00 | 87.675 |

## 4. 启动与真实自用路径

取得执行和Git权限后：
1. 在main精确提交本次计划与规划证据，排除.codegraph/及他人dirty；记录真实规划提交P，不伪造预设SHA。
2. 用固定协调版本执行`--verify-committed`；通过后创建/复用上述迭代Worktree，不盲目嵌套。
3. 核对工作区/分支/HEAD/dirty和指定工具权限；完成已有套件基线，结果异常则定位，不把失败叫GREEN。
4. 为当前卡准备真实context：candidate取实际HEAD，tool_entry取固定入口，authority/execution/verification观察提供项目内原件；dependencies按上表列完整卡路径。初始化不制作虚假READY context。
5. 固定协调器`--inventory --mode continue --context <真实JSON> --phase-from-context`；当前卡claim后以同owner明确phase消费dispatch-check。
6. 委派真实实现者，记录task_id与绝对截止；收齐会话和命令终态，当前写者attempt→release/closeout→envelope。
7. 每卡独立审查、Git绑定、登记、strict后才推进依赖；至少一次正常检查点由新会话续接，保留原证据和剩余目标。
8. 任务06汇总上述真实记录，而不是重新模拟一遍当作真实自用。负例放隔离样例；不故意损坏真实卡/耗尽预算。
9. 六卡PASS后做整轮集成、完整回归、非参与者总审及branch strict；授权未齐/证据未知保留未完成。合流/推送/部署/清理单独决定。

## 5. 整体验收

- [ ] 六卡均有真实type证据、独立APPROVED、有效C/D绑定和PASS，未把退出0或声明DONE代替。
- [ ] 任务01—05的原生真实自用至少覆盖一次完整调度/验收链和一次正常跨会话续接。
- [ ] 八组合模板、旧CLI/导入、Git/FS真实看板及证据读取集成通过。
- [ ] 隔离负例/恢复测试通过；静态、synthetic与native-self-use分层列证，不外推部署/外部业务通过。
- [ ] 最终候选完整回归、独立整轮报告、分支strict通过；源改动均被有效DONE白名单覆盖。
- [ ] 无活动实现命令遗留；UNKNOWN命令状态明确阻断。根索引更新和部署留在相应授权操作，不破Zero-Root-Touch。

## 6. 当前交接

任务01已完成独立APPROVED与C/D登记，D=2ecd3bc3f957ac1941b388e036a6427b717b6cc7，固定工具local strict确认PASS。实际经历正常跨会话续接及一次deadline取消后的FUSED收尾、用户明确单次授权恢复，原始事件和四预算均保留。
任务02已获新候选独立APPROVED，初审F01反例已修复，36断言RED→45GREEN，156指定回归通过；登记后固定strict核对PASS才进入03。任务03—06仍TODO，未提前派发。
历史维护结论不重开；当前源码基线与各安装现状分开，安装/消费事实由05只读核查。

### 初始化实际消费
- 现有解析器识别6张TODO卡；结构、链接、白名单无跨卡重叠及TypeSafe换算校验通过，见[evidence/planning/init-validation.json](evidence/planning/init-validation.json)。
- 实际运行当前源码的`--local`，退出0，刷新本迭代投影；这是初始化协调动作，不是任务验收。
- 实际`--inventory --mode continue`在未提供执行context时退出2，六卡NEEDS_INPUT、验收UNKNOWN；没有把计划完备误判为可派发。原始命令和输出见[evidence/planning/init-inventory.json](evidence/planning/init-inventory.json)。
- 尚未运行产品测试或真实执行链。上述调用为初始化证据，正式执行仍使用第1节冻结协调器。

<!-- iter:projection -->
## 验收事实（阶段比例不是工时）

声明DONE 2/6 · 验收PASS 2/6

| 任务 | 声明 | 验收 | 业务阶段 / 清单比例 | 工程阶段 | 阻塞原因 | 累计尝试 | 最后更新 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01-authority-consistency.md | DONE | PASS | 阶段清单已勾选完毕 / 3/3 (100%) | CHECKLIST_COMPLETE (未等同验收) | 未记录 | 0 | 2026-11-13T16:44:56.984232+00:00 |
| 02-typed-template-generation.md | DONE | PASS | 阶段清单已勾选完毕 / 3/3 (100%) | CHECKLIST_COMPLETE (未等同验收) | 未记录 | 0 | 2026-11-13T17:27:41.977460+00:00 |
| 03-query-cli-contract.md | TODO | UNKNOWN | Stage 1/3：冻结兼容矩阵，对缺失的统一投影字段取得有效断言RED / 0/3 (0%) | 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。 | 未记录 | 0 | 2026-11-13 |
| 04-board-handoff.md | TODO | UNKNOWN | Stage 1/3：固定真实用户路径、视口和四态输入，基于03字段更新详情展示 / 0/3 (0%) | 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。 | 未记录 | 0 | 2026-11-13 |
| 05-release-evidence-index.md | TODO | UNKNOWN | Stage 1/3：盘点四层事实与现有原件，区分当前/历史/未知 / 0/3 (0%) | 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。 | 未记录 | 0 | 2026-11-13 |
| 06-self-hosting-acceptance.md | TODO | UNKNOWN | Stage 1/3：整理01—05真实消费证据，隔离夹具运行故障与恢复路径 / 0/3 (0%) | 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。 | 未记录 | 0 | 2026-11-13 |
<!-- /iter:projection -->
