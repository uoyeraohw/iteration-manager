# 受控检查点续跑与统一截止入口

状态：ACCEPTED（冻结candidate08与Windows单任务有界分片恢复链已通过Antigravity最终验收，双副本交付完成）。四计数0/0/0/2、resume2/3保持。当时另存的三处AIMovie兼容性变更及新测试，已由任务07另行验收、部署candidate09；不改本轮历史证据或批准范围。

## 设计

保留旧recover只记录终态、不解除FUSED的契约；新增显式`resume-checkpoint`动作。由主控持有工作区外的短期授权JSON，绑定真实cwd、卡路径、完整当前HEAD、最近closeout事件、已审查检查点及非空终态/命令证据。仅干净冻结快照、无活动写者、原生会话/命令已终态的执行时间中断可续跑；预算熔断、缺证据、过期/重放冲突、错误工作区/HEAD拒绝。首次冻结独立续跑上限3，后续不能增大；每个closeout仅消费一次授权，不修改round/total/consilium/replan或旧事件。

新增`scripts/iter_run.py`，使用标准库subprocess和argv（无隐式shell），在真正启动前检查明确UTC截止，过期不启动；同次调用先创建独占证据，再运行并保存原始合并输出、UTC起止、实际子进程退出码。按剩余时间限制执行并只终止本次创建的进程树，保留终止确认；超时/未知不冒充业务exit。证据已存在拒绝覆盖。原CLI无新增依赖。

正常阶段完成复用release并保留IN_PROGRESS/TESTING；时间中断仍closeout为FUSED，不拿检查点掩盖超时。新会话继承冻结检查点，不能重置预算或把RED当GREEN。先源码/真实进程验证及独立验收，再部署2/3号模板、新会话消费，最后恢复真实GREEN/C→独立审查→D/strict。副本继续等待整链通过。

## 备选与取舍

- 扩大replan额度：改动最少，但把会话切片当语义重规划，拒绝。
- 改旧recover自动解冻：复用方便，但改变现有恢复契约，且会让普通查询解除失败熔断，拒绝。
- 新显式动作及独立单次授权：多一个可校验入口，保留旧语义；采用。授权仍需主控及独立审查核实原始身份与来源，工具校验不替代该职责。

## 实施计划

1. [x] `tests/test_checkpoint_resume.py`和`tests/test_iter_run.py`：behavior-red.txt中两项真实断言失败；初次API参数错误不算RED。既有1563—1565真实失败为协议基线，历史缺口不回填。
2. [x] `scripts/iter_checkpoint.py`负责授权/绑定/单次消费校验，`iter_autonomy.py`只接入新增分支，`iter_sync.py`增加新选项；旧调用/预算失败回归保持。
3. [x] `scripts/iter_run.py`实现命令入口，Windows Job在启动门闩前接管，确认整个Job终态，拒绝未验证的非Windows执行；测试实际exit7、过期无副作用、deadline杀子树、根先退/孤儿、日志不覆盖、清理未知、挂接失败和CLI真实消费。
4. [x] 共同协议/2、3号模板/必要叶子委派模板引用统一入口和阶段续跑；笔记保留旧决定并互链。针对性、完整套件、笔记校验，独立Antigravity验收候选。
5. [x] CAS部署2/3号与新会话消费；在原run02冻结HEAD与RED上签发本次限定授权，由实际主控/主管恢复业务，观察根不替写卡/业务。每会话570秒hard、480秒工作、90秒收尾，串行分段而不压缩必要门禁。

## Review Focus

- 旧recover、旧event重放、四计数及预算熔断不可被新动作绕过。
- 外部授权不可由叶子改写；绑定单一closeout/HEAD/工作区，不能无限重启。
- runner启动前及超时后的真实进程状态，子进程树不遗留；只终止自己创建的树。
- 原始日志不可覆盖，异常shell/超时/会话取消不冒充pytest退出码。
- 源码通过、配置部署、消费与业务整链验收分别记录。

证据目录：`build/stage10-checkpoint-resume-20261111/`。维护主版本非Git仓库，不虚构源码提交；业务沙箱精准提交仍由实际主控链负责。

## 当前证据

- Antigravity1574只读会诊提出预算判别、单次消费、Windows孤儿回收与排他文件边界；采用约束，不采用重复resume_count双写或仅taskkill回收。
- targeted-final.txt：49 passed，49.08秒；完整直接回归123 passed，279.33秒。
- 最终候选经统一入口实际运行完整回归：candidate-full.json及其原始output，123 passed，264.08秒，真实业务exit0、Job已清空、late_by_seconds=0。源码门禁不代替叶子权限或真实业务链验收。
- 决定笔记tree/format通过；归档校验exit0，无归档记录，非Git环境跳过提交差异的append-only检查。
- 完整授权schema与入口使用见[检查点与命令契约](../../../references/checkpoint_execution.md)；源码、部署、真实消费与业务恢复分别记录。

## 独立审查与部署

Antigravity1580独立APPROVED候选06，并通过统一入口实测32项核心用例（41.30秒、真实exit0、tree_terminal=true、late0）；批准仅覆盖维护候选，可推进部署/实际消费，不批准业务整链。报告部分file链接使用证据包行号而非源码行号，定位以冻结源码为准；旧recover仍写事件并保留阻断，不采用报告“只读登记”的字面概括。宿主隔离与原始来源仍需逐次核实，不采用“彻底杜绝所有逃逸”的无限概括。

Codex核对实际复验receipt及原始输出后采用APPROVED。TypeSafe选择deploy_consume（1.0），Codex据独立报告与原始证据推进。CAS部署2/3号为revision12/9，恢复事务dry-run验证旧值后ROLLBACK；只读授权清单增加6个本候选交付文件，共43项，服务仍只有读取工具。下一步验证实际叶子runner入口及新助手消费，再签发绑定冻结快照的续跑grant。两副本仍未同步。

Antigravity1581已在精确业务worktree通过v2只读服务读取三份主版本契约，原生命令执行新runner成功：真实exit0、Job已清空、late0；原生库存的全部相关调用均终态。仅留下3份授权探针证据，无业务/测试/卡片变化，暂不由观察线程提交。

实际旧卡最近closeout `recovery-1428-closeout` 原因为非规范文本，candidate06前缀要求会误拒绝。candidate07保留旧事件，通过可选interruption_review绑定独立中断分类，显式拒绝真实预算熔断；terminal/review从绑定HEAD的Git blob读取，拒绝ignored/untracked伪冻结文件。新核心断言RED后GREEN，补充错误reason/event/verdict/kind/reviewer/未提交及预算反例；最终统一入口完整131项通过，246.21秒，真实exit0、tree_terminal=true、late0。4份变更冻结在candidate07，模板与已部署candidate06相同；下一门禁为新的独立源码审查及实际旧closeout中断分类，未完成前不签发grant。

## 实际恢复结果

独立Antigravity1584批准candidate07，并根据原生deadline/RED/收尾来源将旧closeout分类execution-deadline(APPROVED)；独立8项新增分类测试通过（38.95秒、raw0、Job清空、late0）。Codex核对实际收据后采用两项裁决；报告1563角色笔误不采纳，实际1563主控/1564主管/1565作者。

实际2号1586提交规范证据至e8dfdd7ba4f9a59dfb722f4d4ba1756d36782954，dirty空，原卡和业务/测试不变；其原生snapshot精确消费新模板。外部主控签发grant01后，1588→1589→1590真实链启动；1589成功消费单次grant，取得写者/IN_PROGRESS，0/0/0/2保持，领取提交26df457a2484ea9b21f7ab9016754e8f475e0b6e。2/3号原生snapshot均匹配权威模板。

实现者1590留下最小实现，但target命令到16:06:44.593165Z才核验，距离command deadline扣5秒收尾仅0.045835秒；入口启动后立即超时，raw_exit=null、runner/launcher124、Job清空、late0，原始输出为空。没有GREEN/full回归/C。主管1590取消后正常closeout，FUSED/写者空/四计数不变，收尾提交7ce307ac886b7eea7e3381b7a1fa6330c9b84de5；主控1588外层守卫提前取消，late0。三会话原生均cancelled；不要将未完成整链称PASS。

收尾时记录外层命令UNKNOWN；观察主控随后从原生1590 SQLite idx26直接补证：step status3、field6=124，全部27步骤终态。此为新补证，不改旧日志。native1590-edit.json证实部分实现由1590 idx24写入（仅尾部换行归一化比较）；当时仍未验证，dirty为该源码及3份超时证据、resume已用1/3。后续实际恢复如下，不将旧超时追认为GREEN。

## 最新：GREEN、独立审查及登记D已完成

- 实际2号1594冻结未验证成果为P=`abc66d1b94a2d93384a6976f177f411876a2357d`。外部grant02实际由1596(2)→1599(3)消费；主管不改业务/测试、不另派实现者，fresh target与full分别31 passed、真实exit0，两receipt均COMPLETED/tree_terminal=true/late0。作者仍1590，验证者1599；四计数0/0/0/2、resume2/3、writer空。
- 测试候选C0=`ea3715920165b53e683cee245c120d33e176bd50`；随后终态及释放证据冻结到最终审查C=`7653000f199c516286152b9b107d80da9be1be23`。C0..C代码/测试不变，但收据必须绑定完整C。原始审查包为stage10/business-review-packet.json。
- 实际1604(2)→1606(3)组织Reviewer1607；76文件scope实跑通过，Reviewer在截止前未交最终报告，按时取消。原生库存补证idx14/24/26均status3、exit0；TypeSafe结果不代替其未交付裁决。上层串行桥接全新非参与Antigravity1608，business-review-final02.json明确APPROVED、无must-fix；Codex读取实际差异及报告后采用。
- 实际1611(2)→1612(3)登记D=`5e3dc1c7518b2516c56479c8e2e2167df515c86e`，最终D2=`8e3feeb02928d99ecaf157a29efd15dfb4298333`。C..D2仅卡片/迭代README允许元数据和两份注册文件review.json、review-report.md。收据作者1590/Reviewer1608，head_sha=C，contract_sha=BASE；业务与测试未改。
- local strict真实exit2，唯一错误Missing or incomplete acceptance checklist；envelope命令exit0但acceptance_verdict=FAIL。registration-4cab5d27-*原始证据保留；DONE/APPROVED声明不等于最终验收。卡中组合验收条目包含strict自身，尚未勾选，不改冻结文字或检查器来规避。
- 全新非参与Antigravity1614对BASE..D2语义审查APPROVED，并批准受控收尾事务：先登记明确标为待验证的候选声明，再实际运行local strict/envelope/branch strict；仅实际全通、dirty空且外部主控核验后接受，失败保留输出并另提交恢复未完成声明。报告branch-review-final03.json，未执行事务即不能称PASS。报告关于“无活动进程”仅按本任务已确认终态解释，不外推到系统所有进程。

## 历史：证据目录写入阻断

实际2号1617准备收尾brief时，Filesystem MCP拒绝stage10的closure-*写入；本线程查询list_allowed_directories确认该服务只允许D:/Code/Node/Project、D:/Code/Golang/src/heygem。1617已completed，尚未派3号，没有D3/D4或新的三门收据；不得换shell/工具/另一会话重试同一被拒写入。

当时业务HEAD为D2，dirty空，writer空，四计数0/0/0/2、resume2/3；主仓库main为BASE且clean。acceptance为FAIL，整链BLOCKED，两个真实副本保持candidate03。TypeSafe对权限处置选择permission（confidence0.99）；Codex依据实际拒绝停止受影响写入。

当时恢复条件为宿主正式放行本任务stage10外置证据目录，不将只读MCP改为通用写入/执行。用户已在后续消息明确授权，实际落实和消费见下节；旧截止未后移，新切片另定明确UTC窗口。

## 最新：限定授权与受控收尾实跑通过

用户明确授权证据目录后，仅在Codex既有Filesystem MCP args追加stage10绝对目录，保留原两个D盘根与其它配置，不增加Skill根或用户根。filesystem-evidence-directory-authorization.json保存精确项前后及CAS恢复条件；新2号1622与3号1623实际list_allowed_directories并通过Filesystem写入唯一权限证据，旧拒绝未改写，未将只读Skill MCP增加写工具。

实际1622(2)→1623(3)按1614批准的事务执行，D3=`5f02a7600c8f97e521c2845fa697f6e7cc8cd125`只登记候选声明及ledger，D4=`2827ee3490de93bf4f1683b8d014c6c11cb34564`提交本地投影。三门local strict/render-envelope/check-branch strict均COMPLETED/raw_exit_code0/tree_terminal=true/late0，envelope内部acceptance_verdict=PASS、errors=[]，head_sha仍绑定C。原始命令、receipt/output/child见closure02-b4e0bd00-20261112T014338Z-delivery.json；实际身份由closure02-controller-228ce0aa-verification.json补证，原卡UNKNOWN身份不追改。

观察主控亲读D2..D4实际diff及原始三门证据，再通过统一入口独立复验三门，均exit0且envelope内部PASS，最终HEAD仍D4、dirty空。证据observer-final-gates.json及observer-local/envelope/branch三组receipt/output/child。C..D4仅两注册文件及允许卡/README元数据，代码测试/冻结规格/自治原文不变；四计数0/0/0/2、resume2/3、writer空，main仍BASE且clean。笔记tree/format/archive三项校验exit0，非Git环境仅跳过归档提交差异检查，无归档记录。

以上实跑完成后进入独立最终验收；历史RED前置截止缺口、超时、旧strict FAIL全部保留。实际最终裁决与部署结果如下。

## 最终验收与冻结候选部署

全新非参与Antigravity[1629](codeg://session/1629)完整读取最终增量原始证据包、合并只读Git查询、实际调用TypeSafe并保存正式报告。`final-chain-acceptance03.json`分别批准candidate08及限定目录授权、实际完整链，无must-fix，允许50文件副本同步。其原生Git退出0、TypeSafe原始结果和身份见`final-review-attempt03-native.json`；委派completed、307659ms、守卫late0。此前1624/1626均按时取消且未交正式裁决，不计批准；1626已完成的TypeSafe结果不能代替Reviewer裁决。

Codex依据原始三门receipt、实际差异及独立报告采用APPROVED，最终业务HEAD保持D4，收据仍绑定C。结论范围为“Windows单任务经有界分片恢复完成”，不外推为一次无中断全自动、多任务或生产验证。

两个真实副本在同步前逐字匹配既有candidate03，没有目标归属冲突。按candidate08清单各同步50文件；仅覆盖本次交付路径，未复制build、会话、配置或凭据，未删除其它文件。备份、精确恢复条件和逐项操作见`candidate08-replica-sync.json`及`candidate08-replica-backup/`。同步后各50文件与冻结候选逐字一致，两个副本的iter_sync/iter_run入口各自实际退出0；统一入口收据`candidate08-replica-smoke02.json`为COMPLETED/raw0/tree_terminal=true/late0。首轮smoke误要求自定义iter_sync帮助输出含argparse的usage，断言失败已保留；修正外置检查后通过，未改交付代码。

同步前发现主目录`iter_sync.py`、`task_card_schema.md`及`trustworthy-board`笔记已有AIMovie任务库存兼容性并行改动，时间晚于本轮独立三门实跑。保留这三处当前改动；本次部署严格来自已批准的冻结candidate08，不能称主目录全部现状与副本相同。这三项增量由AIMovie兼容性改动的负责会话另行验收、冻结并同步，不混入本轮批准。来源及差异见`candidate08-primary-drift.json`。维护记录和证据仍只保留在主版本。

后续用户明确要求继续验收上述增量。实际审查、136项回归、Antigravity1637独立批准及candidate09三安装51文件对齐，见[任务07](../07-aimovie-discovery-compat/README.md)。本节candidate08冻结证据和当时差异记录不回写成后续状态。
