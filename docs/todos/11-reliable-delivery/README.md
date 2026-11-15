# 迭代11 · 可信路径一致性、使用成本与真实自用验证

> 初始化：2026-11-14 UTC · 当前checkout：`/data/workspace/iteration-manager` · 基线：`fdcc4cce88635ee81573be5991de11de650659d8`。
> 2026-11-15最新授权：适配Linux并整理Windows/Linux开发指引；新增00前置任务，随后01—12逐项验收串行推进。当前00—01完成独审和登记、02—12为TODO；冻结strict核对后产品验收2/13；实施、精准Git与Worktree授权保持。
> 独立Worktree为`.worktrees/iter-11`，分支`feat/iter-11-reliable-delivery`。先完成[00平台适配](00-linux-runner-and-dev-guide.md)，不再要求另找Windows主机；原Windows-only拒绝保留为历史证据。迁移授权见[platform-migration-authorization.json](evidence/planning/platform-migration-authorization.json)。

## 1. 迭代核心目标与全局约束
<!-- iter:goal -->
让现有交付协议不误放行、容易正确使用、可可靠续接且证据可追溯；八项意见统一纳入本轮，使用iteration-manager真实管理自身。任务卡和既有autonomy事件是唯一任务真源。

### 执行约定
- 2026-11-15用户明确授权实施、精准Git提交和创建独立Worktree，覆盖原初始化授权的相应限制；暂不部署、推送、合流或清理。真实任务交付为Git，任务初态TODO/review PENDING/tdd_verified=false。原初始化授权和证据保留，不回写成已执行事实。
- 维护源码基线与正式协调CLI固定fdcc4cce88635ee81573be5991de11de650659d8；仅runner按00显式平台迁移。候选门禁变更不自动升级协调器，不自证批准。
- 按本次用户要求严格串行00→01→02→03→04→05→06→07→08→09→10→11→12；每卡完成type证据、非参与者批准、C/D绑定和冻结local strict验收PASS后才启动下一卡。硬依赖字段保留原意，不把用户串行调度改写为规格依赖；前卡阻断时不跳卡。一个卡片一个写者，源文件单一归属。独审不得参与本任务设计/实现/测试/RCA。
- 默认预算5/10/1/2，连续两次无新增证据禁止原样第三次派发。会话与命令树终态分离，绝对UTC在真实派发时确定。
- 用户明确授权Linux适配，00先实现并独审当前平台runner，验收后仅将runner及直接依赖固定到`/data/workspace/iteration-manager/build/frozen-runners/iter11-platform-v1/`；保存C来源及逐文件SHA256，不追随候选。协调CLI仍固定fdcc4cc。00的GNU timeout限时引导例外只验证runner自身，记录真实bootstrap观察，不伪造旧runner收据。01前通过新冻结runner的完整干净基线；后续正式业务/测试/验收均走它。原十二卡中的Windows前提按此显式平台迁移接续，其余验收和预算不变。
- 无新依赖/打包平台/调度数据库/第五type/跨调用批准缓存；Linux runner扩展仅按00本次授权实施；不扩展FS时间中断grant或自动发现。按支持矩阵与实测决定后续投入。
- 不修改历史docs/todos/10或发布原件，不回写旧任务门禁；根索引仅本次main初始化登记，后续特性分支Zero-Root-Touch。
- 沿用Git C→独审→登记D→local strict；完成全部卡、整轮集成/全量和独立总审后，对最终登记候选运行冻结branch strict。提前结构预检不替代收口。
- 不执行真实安装同步、助手配置、远端推送、合流或清理。新manifest默认stdout和临时副本验证，不自动扩大部署白名单。
- 冻结协调器含已知模式审计和旧接管读取缺陷，记录为FROZEN-KNOWN-01/02。相应负例的候选/固定差异是预期修复证据；实际管理卡仅合法Git且独立核对模式，不凭固定工具PASS放行非法卡。
- 11交付并独审登记DONE后，Controller另完成独立整轮总审和最终branch strict，防止11自要求其尚未能通过的门禁。收口原件放主checkout的build/iter11-closeout/带UTC唯一目录；不写入已审任务scope，README只记摘要/引用。清理前按授权归档，未归档不得清理唯一原件。
- 全部13卡PASS后由Controller统一整轮收口；10只做隔离联合验证，11只做选定真实链审计，12只修执行流程契约。三者不互设循环批准前提。
- **实际固定入口**：`/data/workspace/iteration-manager/build/frozen-tools/fdcc4cce8863/scripts/iter_sync.py`；模板生成器和截止守卫取同一快照；runner在00通过前仍保留原快照，之后取明确批准的平台快照。逐文件Git字节和SHA256清单见planning/coordinator-manifest.json；不可随候选自动更新。
- **三级验证**：内环按卡针对性测试；任务交付完成其type检查、直接兼容/回归与独审。全部卡PASS后的集成路径为01模式→02报告→03守卫→投影/事件/交接，以及06临时安装→07测试支持、08合法批准库存；最终全量为`python -B -m pytest -p no:cacheprovider tests -q`。
- **正式命令入口**：在实际目标项目根目录使用当前平台已验收冻结的`iter_run.py --deadline 实际UTC --evidence 项目相对唯一收据 -- python -B -m pytest -p no:cacheprovider ... -q`。这里是使用形式说明，绝对UTC和真实argv由本次派发即时生成，不原样执行省略号，不回退裸命令。
- **角色与时间**：主控/主管协调，不写产品；同一owner完成核心RED/GREEN及返修，非参与者独审。按真实schema确定原生工具，不猜助手ID；每次锁定绝对UTC和正常检查点，默认10分钟介入、至少90秒收尾，已知跑不完的门禁不启动。
- **正式证据与临时输出**：逐卡`evidence/01/`至`evidence/12/`；规划原件在`evidence/planning/`；pytest临时目录和临时安装用独占临时根，运行资产在build，不覆盖原件、不清理他人输出。
- **冻结器已知限制**：FROZEN-KNOWN-01未知模式DONE审计，FROZEN-KNOWN-02旧接管读取中断。实际管理卡均用合法Git缺省；Controller和独审显式核对模式。候选负例拒绝而固定器未拒绝属于预期修复差异，固定器PASS不能覆盖该语义缺口。

### Review Focus
1. 非法显式模式原本就在冻结规格中仍须拒绝：01的合法其余Git绑定反例，10跨投影复核。
2. 一张卡读失败不能拖丢其余库存：02混合Unicode/OSError/竞态，10交叉报告。
3. 检查仍running、旧request/owner/context及委派unknown不误派发：03异步负例、11原生顺序、12默认消费。
4. 来源/快照/能力声明不能相互代替：06清单越界/漂移，07白名单临时测试，08合法收据库存，05支持矩阵。
5. 自用不自证且不循环收口：固定器缺陷保留，11审计实际链，全部卡PASS后Controller总审/最终strict，不改已审scope或嵌入巨型日志。
<!-- /iter:goal -->

## 2. 十三卡索引

| 卡 | 交付 | type | 硬依赖 | 初态 | 任务卡 |
| --- | --- | --- | --- | --- | --- |
| 00 | Linux截止入口与双环境开发指引 | Strict-TDD | 无 | TODO | [00-linux-runner-and-dev-guide.md](./00-linux-runner-and-dev-guide.md) |
| 01 | 统一交付模式解析与完成审计 | Strict-TDD | 无 | TODO | [01-delivery-mode-consistency.md](./01-delivery-mode-consistency.md) |
| 02 | 隔离旧接管报告的逐卡读取故障 | Strict-TDD | 无 | TODO | [02-takeover-report-isolation.md](./02-takeover-report-isolation.md) |
| 03 | 连接就绪检查与真实委派的薄守卫 | Strict-TDD | 01 | TODO | [03-native-dispatch-guard.md](./03-native-dispatch-guard.md) |
| 04 | 收敛当前任务的默认阅读导航 | Spike-Discovery | 无 | TODO | [04-navigation-and-support.md](./04-navigation-and-support.md) |
| 05 | 公布带证据的支持矩阵 | Spike-Discovery | 无 | TODO | [05-support-matrix.md](./05-support-matrix.md) |
| 06 | 提供安装来源清单与轻量自检 | Strict-TDD | 无 | TODO | [06-installation-provenance.md](./06-installation-provenance.md) |
| 07 | 消除维护测试对历史证据harness的运行依赖 | Refactor-Benchmark | 无 | TODO | [07-portable-test-support.md](./07-portable-test-support.md) |
| 08 | 量测合法Git与FS批准库存的真实成本 | Spike-Discovery | 01 | TODO | [08-approved-chain-benchmark.md](./08-approved-chain-benchmark.md) |
| 09 | 使新重构任务的量测匹配实际目标 | Spike-Discovery | 无 | TODO | [09-proportional-refactor-evidence.md](./09-proportional-refactor-evidence.md) |
| 10 | 核验跨模块故障路径的一致性 | Spike-Discovery | 01, 02, 03, 06, 07 | TODO | [10-integration-fault-paths.md](./10-integration-fault-paths.md) |
| 11 | 审计本轮真实自用链与检查点续接 | Spike-Discovery | 03, 10 | TODO | [11-native-self-use-audit.md](./11-native-self-use-audit.md) |
| 12 | 统一默认派发与最终收口顺序 | Spike-Discovery | 03 | TODO | [12-workflow-sequence.md](./12-workflow-sequence.md) |

依赖图无环；硬依赖维持规划结果。2026-11-15用户另要求按00前置、01—12编号串行验收，因此当前不越过阻断卡推进独立后续任务；这是本轮调度约束，不改变任务技术依赖或验收要求。

## 3. 八项意见覆盖

| 原意见 | 责任卡 |
| --- | --- |
| 1 | 01, 10 |
| 2 | 02, 10 |
| 3 | 03, 10, 11, 12 |
| 4 | 04, 12 |
| 5 | 06, 07, 10 |
| 6 | 08 |
| 7 | 09 |
| 8 | 05, 11 |

原意见4的历史190KB README不在特性分支跨迭代改写；04提供摘要路由及新模板约束。原意见7保留四type和旧卡门禁，通过新任务指标选择降低无关量测。原意见8本轮交付支持矩阵，不顺带扩展平台或FS恢复。

## 4. 规划质量与取舍

- 使用真实MCP `mcp__typesafe__evaluate` / `jev-1.14.0`，权重30/30/20/20，总分至少80且每维至少70；以实际legend最大索引换算，confidence不作得分。
- r1的原04/09未通过；拆分后r2的04/11仍未通过；第二次实质修订把导航04、流程12、隔离集成10和原生审计11分开，r3相应任务通过。未变交付沿用原分数，编号映射和全部原始失败保留在[summary](evidence/planning/typesafe-summary.json)。
- 规划检查修正了最终strict自循环、check的实际argv/cwd/request绑定、独立任务不随能力缺口全部阻塞，以及固定器已知缺陷。该检查参与设计，不是后续产品独立APPROVED。
- 方案取舍：采用现有CLI/事件账的薄适配和白名单临时自检；没有引入新调度平台、打包体系或跨调用批准缓存。此为本轮规划决定，尚非实现结果。

| 卡 | 粒度 | 明确度 | 单一职责 | 可执行性 | 总分 | 原始来源 |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | 84.50 | 78.00 | 74.75 | 82.00 | 80.100 | r1/01 |
| 02 | 92.50 | 83.00 | 88.75 | 84.50 | 87.300 | r1/02 |
| 03 | 87.00 | 85.00 | 92.25 | 82.00 | 86.450 | r1/03；执行性r4 |
| 04 | 88.00 | 84.25 | 86.75 | 78.50 | 84.725 | r3/04 |
| 05 | 93.50 | 76.25 | 94.25 | 87.25 | 87.225 | r2/05 |
| 06 | 94.00 | 92.75 | 89.50 | 90.00 | 91.925 | r1/05 |
| 07 | 87.50 | 77.75 | 79.75 | 81.00 | 81.725 | r1/06 |
| 08 | 85.75 | 83.00 | 83.75 | 78.00 | 82.975 | r1/07 |
| 09 | 90.25 | 77.75 | 85.25 | 83.00 | 84.050 | r1/08 |
| 10 | 81.75 | 77.00 | 85.25 | 79.25 | 80.525 | r2/10 |
| 11 | 87.50 | 92.75 | 92.50 | 74.75 | 87.525 | r3/11；执行性r4 |
| 12 | 79.75 | 85.00 | 78.00 | 77.25 | 80.475 | r3/12；执行性r4 |

更正记录：08/09的两处旧卡号引用已更新，原始输入/生成结果保留。完整延迟工具目录确认Codeg schema已暴露，先前不可用判断不准确；仅03/11/12执行性按新事实做r4重评并通过，不另做设计重规划。原始误观察、请求/响应及更正见[initialization-corrections.json](evidence/planning/initialization-corrections.json)。

## 5. Linux迁移与历史启动交接

00已完成Linux后端和AGENTS双环境指引：F1真实RED后关闭，核心30通过/2 Windows跳过、受影响回归147通过/2跳过；完整维护基线在Python3.11.17/pytest9.2/MCP1.30及仓外临时根取得513通过/2跳过。C3独立复审批准，新[审查及环境证据](evidence/00/review-report-v2.json)保留初始快照遗漏、509/4失败/2跳过及MCP2不兼容观察。runner固定同一获批C2六文件；协调器仍fdcc4cc，不部署。

最新要求已把00平台适配加入本轮，恢复条件改为在当前Linux上完成00、独审和冻结；不再等待Windows环境。真实TypeSafe四维为90.25/99.50/99.00/93.25，加权95.375，原件见[linux-typesafe-summary.json](evidence/planning/linux-typesafe-summary.json)。协作运行时已实际读取必读契约；Codeg本地子会话则因bwrap启动失败，二者分开记录，不能宣称Codeg链已通过。

以下为Linux迁移授权前的启动历史；不代表最新恢复条件。

2026-11-15已执行本次启动授权：精准提交125份归属规划/证据文件，冻结`--verify-committed`退出0后创建独立Worktree；当前执行位置为`/data/workspace/iteration-manager/.worktrees/iter-11`。主checkout保留main和规划提交，不从迭代分支回写根索引。

- **当前结论**：第01卡就绪BLOCKED，十二卡仍为TODO/验收UNKNOWN，0次attempt、0个写者、无活动产品执行者。没有产品实现、pytest、RED/GREEN、独审或完成收据。
- **实测能力缺口**：同调用以确切UTC截止尝试冻结runner基线入口，实际退出125并报告`This runner requires Windows Job Objects; no command started`，未生成runner收据，pytest未启动。此为启动拒绝观察，不是行为RED或测试失败。见[原始错误](evidence/startup/baseline-launch.stderr.txt)及[完整调用观察](evidence/startup/baseline-launch.observation.json)。
- **真实自用观察**：91个冻结文件再次核对一致；规划门禁成功；同候选完整盘点退出3，第01卡execution/verification均BLOCKED，后续卡还受本次串行约束阻断。主控已消费结果，因此没有claim、派发或伪造attempt。见[盘点原件](evidence/startup/startup-inventory.stdout.txt)。这些事实仅覆盖启动协调和能力拒绝路径，不代表完整原生交付链健壮性已通过。
- **恢复条件**：环境所有者提供可访问的Windows执行入口与工作区；Controller在同一适用候选核对冻结工具、实际Codeg读取/委派能力、独审角色及正式干净基线，再生成新鲜context、claim和同owner dispatch-check。旧[startup-context.json](evidence/startup/startup-context.json)只绑定规划提交`80621f1`，是历史BLOCKED观察；后续证据登记提交不把它自动变成当前READY。
- **串行边界**：第01卡完成type证据、独审、C/D和local strict验收PASS前不启动02—12；不修改硬依赖或降低门禁。暂不部署、推送、合流或清理。

以下初始化观察截至2026-11-14；其中授权、提交和Worktree状态已由2026-11-15启动记录接续，不能作为最新执行结论。原始观察文件保持不变。

- **已做**：实际TypeSafe质检、冻结Git工具导出、十二份实际CLI生成/初态预检、任务及初始化context落盘。后续CLI盘点原件在planning/；这些不是产品测试或完成批准。
- **未做**：产品实现、正式pytest、独审、Git提交、Worktree执行、安装同步与整轮验收。历史493通过仍只是11月14日发布候选的旧证据。
- **初始化授权**：只覆盖本次规划/注册，来源[authorization.json](evidence/planning/authorization.json)。产品实施和Git/Worktree执行授权待Controller在启动时核对，不能把初始化当任意后续操作批准。
- **能力**：当前Linux/Python3.13.5不能执行Windows Job正式runner；已从完整延迟工具目录发现Codeg委派/查询/取消schema，实际目标工作区与执行链仍未验证。补齐责任为后续Controller与环境所有者，恢复条件是同候选可使用的Windows工作区、真实Codeg schema/原生调用及独审能力；不静默换实现或声称已支持。
- **Git/Worktree**：规划尚未提交；`--verify-committed`应保持拒绝，不能创建工作区绕过。获相应授权后精准提交本次归属文件得到P，用固定器验证后创建`.worktrees/iter-11`和计划分支；不暂存他人dirty。
- **context**：[initial-context.json](evidence/planning/initial-context.json)如实记录NEEDS_INPUT/BLOCKED，不是待执行READY样板。实际派发前重读候选、phase、输入、能力和授权；当前无人claim，不制造attempt。

## 6. 后续执行与自用验收

1. `/iter next 11`接续本目录；采用2026-11-15实施/Git/Worktree授权及逐项验收串行约束，先核对实际checkout/HEAD/dirty、冻结快照与就绪能力。规划提交/隔离工作区及正式基线完成前不实施。
2. 保存真实观察context并运行固定器inventory；claim后以同owner消费逐卡dispatch-check的完整终态。受支持Codeg再通过03守卫真实派发，保存会话/命令身份。
3. 确认会话及命令树终态后attempt→release/closeout；检查点继承已有有效证据，不清预算，不重复同候选已有效验证。
4. 每卡C→独审→登记D→固定local strict。11只审计选定链与正常续接；12完成默认流程消费。全部卡PASS后Controller执行集成/最终全量、整轮独审及最终branch strict。
5. 收口原件保存在主checkout build的唯一UTC目录，README仅链接；未安全保留原件前不清理。部署、推送、合流和清理均分别核对授权。

## 7. 整轮验收

- [ ] 十三卡具备各自type证据、非参与者批准、合法C/D绑定与PASS。
- [ ] 完整链和真实新会话检查点继承有本轮原始证据，03/12的先消费后派发得到实际证明。
- [ ] 10隔离跨模块反例、08合法Git/FS量测、06/07临时安装检查和05支持声明各有边界清楚的原件。
- [ ] 最终候选整轮集成/完整维护套件、独立总审及冻结最终branch strict通过。
- [ ] 所有FAIL/UNKNOWN/BLOCKED、Deferred Minors和发布/自动发现/FS业务缺口如实保留，未越权部署或清理。

<!-- iter:projection -->
## 验收事实（阶段比例不是工时）

声明DONE 4/13 · 验收PASS 4/13

| 任务 | 声明 | 验收 | 业务阶段 / 清单比例 | 工程阶段 | 阻塞原因 | 累计尝试 | 最后更新 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00-linux-runner-and-dev-guide.md | DONE | PASS | 阶段清单已勾选完毕 / 3/3 (100%) | CHECKLIST_COMPLETE (未等同验收) | 未记录 | 2 | 2026-11-15T03:48:53.290510+00:00 |
| 01-delivery-mode-consistency.md | DONE | PASS | 阶段清单已勾选完毕 / 3/3 (100%) | CHECKLIST_COMPLETE (未等同验收) | 未记录 | 1 | 2026-11-15T04:07:19.729474+00:00 |
| 02-takeover-report-isolation.md | DONE | PASS | 阶段清单已勾选完毕 / 3/3 (100%) | CHECKLIST_COMPLETE (未等同验收) | 未记录 | 0 | 2026-11-15T04:18:48.386112+00:00 |
| 03-native-dispatch-guard.md | DONE | PASS | 阶段清单已勾选完毕 / 3/3 (100%) | CHECKLIST_COMPLETE (未等同验收) | 未记录 | 1 | 2026-11-15T04:31:36.497630+00:00 |
| 04-navigation-and-support.md | TODO | UNKNOWN | 记录进入当前任务所需的直接文档及原件路径 / 0/3 (0%) | experiment：python -B -m pytest -p no:cacheprovider tests/test_navigation_paths.py tests/test_prompt_sources.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。 | 未记录 | 0 | UNKNOWN |
| 05-support-matrix.md | TODO | UNKNOWN | 逐项核对契约与有日期的能力原件 / 0/3 (0%) | experiment：python -B -m pytest -p no:cacheprovider tests/test_support_matrix.py tests/test_release_index.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。 | 未记录 | 0 | UNKNOWN |
| 06-installation-provenance.md | TODO | UNKNOWN | 对来源不符、坏清单、漂移/缺失/越界路径取得断言RED / 0/3 (0%) | red：python -B -m pytest -p no:cacheprovider tests/test_install_provenance.py tests/test_cli_compatibility.py -q；由同一实现者先取得验收中具体行为断言失败，环境/导入失败不作RED；通过冻结runner。 | 未记录 | 0 | UNKNOWN |
| 07-portable-test-support.md | TODO | UNKNOWN | 取得原维护测试基线及同环境Before量测 / 0/3 (0%) | baseline：python -B -m pytest -p no:cacheprovider tests/test_board_handoff.py tests/test_board_service.py -q；在修改前保留实际维护基线，通过冻结runner。 | 未记录 | 0 | UNKNOWN |
| 08-approved-chain-benchmark.md | TODO | UNKNOWN | 构造Git/FS合法批准库存，先断言每卡审计PASS / 0/3 (0%) | experiment：python -B tests/benchmarks/approval_chain.py --sizes 10 100 --repeats 3 --output docs/todos/11-reliable-delivery/evidence/08/measurements.json；先确认合法Git/FS库存每卡PASS，通过冻结runner。 | 未记录 | 0 | UNKNOWN |
| 09-proportional-refactor-evidence.md | TODO | UNKNOWN | 用两种真实新卡规划样例确认当前成本与指标匹配问题 / 0/3 (0%) | experiment：python -B -m pytest -p no:cacheprovider tests/test_refactor_evidence_policy.py tests/test_template_generation.py tests/test_task_card_schema.py tests/test_completion_gates.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。 | 未记录 | 0 | UNKNOWN |
| 10-integration-fault-paths.md | TODO | UNKNOWN | 复用成熟夹具定义最少跨模块断言 / 0/3 (0%) | experiment：python -B -m pytest -p no:cacheprovider tests/test_self_hosting.py tests/test_execution_readiness.py tests/test_autonomy.py tests/test_checkpoint_resume.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。 | 未记录 | 0 | UNKNOWN |
| 11-native-self-use-audit.md | TODO | UNKNOWN | 从Controller来源指针中选择一条完成链和一次正常续接 / 0/3 (0%) | experiment：python -B docs/todos/11-reliable-delivery/evidence/11/audit_native_chain.py --sources docs/todos/11-reliable-delivery/evidence/planning/native-source-index.json --output docs/todos/11-reliable-delivery/evidence/11/robustness-report.json；缺原件返回2不补造，通过冻结runner。 | 未记录 | 0 | UNKNOWN |
| 12-workflow-sequence.md | TODO | UNKNOWN | 核对三种流程场景及权威来源 / 0/3 (0%) | experiment：python -B -m pytest -p no:cacheprovider tests/test_workflow_sequence.py tests/test_prompt_sources.py tests/test_task_card_schema.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。 | 未记录 | 0 | UNKNOWN |
<!-- /iter:projection -->
