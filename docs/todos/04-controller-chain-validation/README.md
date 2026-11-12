# 新会话主控自动实现链验证

状态：ACCEPTED（Windows单任务有界分片恢复链三门PASS，Antigravity1629最终APPROVED）。四计数0/0/0/2、resume2/3保持；candidate08交付完成。当时另存的三处AIMovie兼容性增量及新测试，后由任务07单独验收并部署candidate09，不改变本轮主控链批准的范围。

## 当前续跑能力门禁

用户授权的受控续跑与统一入口已完成candidate07源码验收（完整131项及Antigravity1584独立APPROVED），2/3号revision12/9和实际契约消费已验证。两次外部grant实际消费，四预算未清零或增加；fresh GREEN和回归均31 passed，由1599验证1590实现。最终审查C=`7653000f199c516286152b9b107d80da9be1be23`经独立1608批准，实际1611(2)→1612(3)登记D及D2；D2当时HEAD=`8e3feeb02928d99ecaf157a29efd15dfb4298333`、dirty空、writer空，卡DONE/APPROVED但acceptance=FAIL。

原local strict exit2与envelope内部FAIL原样保留。独立Antigravity1614批准BASE..D2语义审查及受控候选声明事务；1617的Filesystem写入拒绝后未继续执行。用户随后明确授权精确stage10目录，正式追加Codex既有Filesystem MCP该目录参数，新1622(2)→1623(3)实际消费并执行事务。最终D4=`2827ee3490de93bf4f1683b8d014c6c11cb34564`；三门实跑及观察主控独立三门复验均raw exit0、Job终态，envelope内部PASS。业务dirty空、writer空，main仍BASE且clean，C/收据/冻结正文不变。非参与Antigravity1629最终正式APPROVED，无must-fix；Codex核对原始证据后接受，并同步已批准candidate08到两个副本，各50文件逐字一致、入口smoke通过。结论为“Windows单任务经有界分片恢复完成”，不声称无中断一次跑通或多任务/生产验证。报告、同步备份和主目录并行增量边界见[06最终验收](../06-checkpoint-resume/README.md#最终验收与冻结候选部署)。

## 历史：有界RED切片及独立裁决

- 主控1563→主管1564→测试作者1565：启动检查点2157383早于作者派发；作者通过新只读MCP消费主版本，保留旧断言并拆分DONE/FUSED正例。原生step18嵌套PowerShell语法错误不算RED；step20同调用落盘真实pytest原文，开始14:19:29.2475238Z、结束14:19:34.6870078Z、exit1，2 failed/29 passed，DONE/FUSED均AssertionError。step20缺少同次命令的显式截止前置核验，这个要求仍未达标，不能用实际未超时替代。测试检查点完整SHA为f9c57bccf3114a0209d0e7455c83af7ac458316b，未形成实现C。
- 作者14:19:38.422取消，主控14:21:08.814确认取消，均在各自hard前，late0。主管已提交RED但未完成release/closeout，卡片当时仍IN_PROGRESS且writer指向已取消主管。新2号主控1566只按既有元数据恢复授权核实三会话原生cancelled、1565全部21步骤终态，release旧owner→claim新owner→closeout，退出0/0/3；没有新子会话或业务执行。最终HEAD为6da91b3bb67f13961b87302a3c0a7509a334e143，dirty空，卡FUSED/is_blocked=true/writer空，round/total/consilium/replan=0/0/0/2。
- 新非参与者Antigravity1570独立裁决：RED技术有效，可供后续GREEN继承；安全收尾有效，命令前截止核验仍有缺口；完整链BLOCKED，无实现C、GREEN/回归、C独立批准、收据/D或最终严格门禁。replan已2/2，不能隐式重置/扩大；需明确授权的新恢复计划/预算，或独立审查通过的受控检查点恢复能力，再合法解除FUSED。采用该裁决，记录中“收据D”指登记收据及登记提交D，不能替代实现C。
- 验收1568在60秒启动阶段未建立external_id，未产出报告；1569五分钟读取后被守卫取消，未产出结论；均非批准。最终1570消费单一原始证据包，93.367秒完成独立报告。相关attempt/monitor原样保留。
- 主版本stage09/证据：red-slice-monitor.json、native1565-inventory.json、metadata-closeout-monitor.json、chain-audit-packet.json、chain-independent-review.json；沙箱evidence/01/phase-red-author-pytest.txt及recovery-1428-*保留命令、来源、动作和收尾。观察线程未写业务、测试或卡片，也未冒称自行桥接后的自动全链通过。

当时的推进决定为先完善受控检查点续跑与统一命令截止执行入口，再继承现有RED进入GREEN；不以增加replan次数掩盖会话切片问题。该恢复能力现已批准并实际消费，当前剩余门禁以上节为准。

## 历史：新通路后的首次续跑与切片方案

主控1558→主管1559→作者1560实际消费新MCP读取两份主版本契约，但在140秒有效叶子窗口只完成schema与两份契约读取，未发出业务/测试命令。主控/主管启动及登记占用至13:59:33（根启动13:55:06），剩余窗口不能完成多叶子全链；未拆分模型/冷启动/工具耗时，不认定各自占比。

外部同次守卫14:04:26.303确认主控取消，早于hard14:04:36.263约9.960秒，late0；作者也按提前10秒余量取消。主管已closeout释放writer，主控提交c528844；dirty只保留原1531测试，计数round0/total0/consilium0/replan1。无新RED/C/D/GREEN或独立批准。原生1560库存全部已终态，只有schema读取及两个MCP读取，无run_command/edit/write；这是新补证，不回填卡内当时UNKNOWN。证据stage09/chain-resume-monitor.json、native1560-inventory.json及沙箱resume-*。

Antigravity1562会诊建议阶段切片及免replan的超时恢复。采用阶段切片方向，但不直接改recover清除FUSED：这会改变已有恢复契约且需额外身份/阻断类型验证。当时明确批准第2次语义重规划用于RED切片，现已使用；原方案是成功阶段检查点复用既有release（保持IN_PROGRESS、不清计数），不当成失败closeout、不消耗replan，真正截止/失败才FUSED。该切片仍在完成收尾前被取消，实际结果以上节为准，不能把它记作正常检查点成功。每会话570秒hard、480秒工作与90秒收尾，测试叶子显式上限240秒受剩余work_deadline夹紧。会诊声称schema优化能将读取压到30秒无测量依据，不采纳该数字，也不跳过实际工具要求。

## 新授权通路已验收

用户明确授权扩展后，采用限定cwd/37项清单的只读MCP，不改变native view_file或写策略。新会话1555实际读取主版本，非清单拒绝；Antigravity1556独立批准Windows目标工作区权限通路。详见[只读授权维护任务](../05-readonly-skill-access/README.md)及stage09证据。旧原生接口拒绝仍有效，本次验收条件是新授权接口实际消费，不再要求原生view_file放行。下面历史调查记录保留当时状态。

## 历史：源码批准、部署与消费后，叶子权限阻止续跑

- 从原生数据库C:/Users/qingyu/.gemini/antigravity-acp/conversations/ca3de2db-41c1-4240-9af3-0dc7e6801c91.db（mode=ro）恢复7个run_command记录；steps[28]保存完整pytest合并输出、END_UTC及EXIT_CODE=1。开始02:47:38.4358915Z，结束02:47:42.0816335Z，早于会话取消02:47:49.667Z。外层PowerShell字段退出0，不能替代pytest退出1。未补造PID或拆分不存在的stdout/stderr。
- 原生edit步骤26与当前测试文件逐字一致；实际1 failed, 29 passed，DONE断言False is True失败，FUSED因同一测试提前失败尚未执行。证据恢复的是历史实际RED，不是当前重新运行，也不追认当时未交付链路为通过。旧卡/旧日志保留。
- 主管原始rollout第65/76行：02:46:33.495等待60000ms，02:47:33.541返回；第80/87行：02:47:39.836再次查询，02:47:49.654才发取消。等待虽在截止前返回，模型轮次仍跨过截止；测试命令也在截止后3.436秒启动。
- candidate05截止守卫把临界等待/读钟/取消放在同次工具执行，派发前锁定确切deadline，保留取消余量并分别记请求/确认；叶子启动前检查截止、同调用落输出/实际退出码。6项受控时钟行为回归、2项助手来源检查及完整72项回归（132.85秒）通过；真实时钟工具执行器本地回调探针确认同次执行可在预留窗口取消，不是实代理消费GREEN。冻结候选build/stage07-terminal-deadline-20261111/candidate05；其manifest保留冻结时状态，后续验收和部署状态见本节与stage08证据，不回写历史快照。
- 另发现原作者读取.codeg契约被pre-tool hook拒绝（steps[6].error_details），随后使用另一副本。下一轮必须先通过宿主正式机制解决叶子真实读取权限，不重复该绕过路径；本次未改权限配置。
- 历史两次Antigravity只读派发1534/1535返回Usage Limit Reached。后续1541已完成464256ms的实质独立审查，1543已完成44082ms的原生权限探针，故不再把旧额度错误当作当前不可用证明；未切换账号、凭据或代理绕过。
- Antigravity独立审查1541明确批准candidate05源变更与原命令终态补证。采用该APPROVED；不采用报告将1534/1535旧额度错误沿用为当前阻断的结论，也不采用“先完成新指令消费再部署”的倒置建议。按已约定顺序推进：源码审查→CAS部署→新会话消费→整链最终验收。
- 真实worktree cwd下的Antigravity探针1543，native view_file读取主版本templates/contracts/strict_tdd_contract.md仍被pre-tool hook拒绝outside allowed workspace directories；遇拒绝即停止，无替代工具/副本/改cwd绕过。Skill根目录审查可读不能替代叶子权限。
- 2/3号CAS部署从revision 10/7升到11/8，指令精确等于冻结candidate05；保留1/4号及其它字段。--check-restore事务校验旧指令后ROLLBACK，配置未回退。只读新会话1547/1548均completed，原生assistant_snapshot.instructions与权威模板逐字相同；两者正确保留权限阻断、UNKNOWN、四计数及部署/消费/PASS分离。
- 正式权限机制只读调查1546未在5分钟内交付报告，守卫于12:48:29.986Z请求取消、12:48:30.030Z确认，早于12:48:39.975Z截止，lateByMs=0；原生两条只读搜索命令均有终态（exit1缺rg、exit0 Select-String）。这是实际Codeg会话守卫证据，不是业务自动链PASS。尚未确认可用的限定只读授权入口；未改安全策略。CODEG_ACP_FS_EXTRA_ROOTS会增加可写根，不能作为本次只读授权方案。
- 本轮TypeSafe输出：当前额度阻断0.08、叶子读取已就绪0.08、源码审查门禁已批准0.67。Codex依据1541明确报告、1543真实拒绝及部署/原生快照裁决：源码/部署/只读消费门禁已满足，业务整链仍因权限BLOCKED。模型分值不替代直接证据。
- 原补证阶段TypeSafe对命令终态直接证据0.87、行为断言RED0.87、等待后跨截止0.78；这是模型输出。Codex按原始END_UTC/EXIT_CODE/断言和调用时间裁决终态缺口已消除；业务链的叶子命令前核验与全链截止仍待实测。
- 证据：build/stage07-terminal-deadline-20261111/recovered-commands.json、recovered-pytest-output.txt、supervisor-wait-events.json、typesafe-terminal.json、antigravity-quota-results.json。recover_native_commands.py可重读同一原生记录，未运行业务命令。
- 后续证据：build/stage08-resume-20261111/的candidate05-review.md、candidate05-review-record.json、permission-probe.json、assistants-before.json、assistants-deployed.json、restore-dry-run.json、candidate05-consumers.json、consumer-native-snapshots.json、permission-research-watch.json、permission-research-native-steps.json及typesafe-gates.json。维护源与39文件冻结候选、沙箱HEAD/dirty及原生测试内容的最终核对见observer-checks.json。

## run02原交付记录（补证前）

## 历史run02：收尾生效，当时完整链BLOCKED

- 主控[1528](codeg://session/1528)→主管1529→测试作者1531，原生instructions与2/3号新模板一致；主控550768ms内终态completed，主管375137ms，不再受150秒子树限制。
- claim提交21b5dfb394ee4aa767e6e39d74708cde47912c07、IN_PROGRESS提交4943bccbd4d6010acf2216f7ab35050b2b1db375均早于首次测试派发。叶子有至少120秒工作窗口。
- 测试作者canceled，留下未暂存测试；未交付有效RED及底层命令终态，未启动实现/独立Reviewer，无C/D、GREEN或批准收据。原测试命令状态UNKNOWN，不据取消推断进程停止。
- 主管正常执行closeout（退出3）：卡片FUSED/is_blocked=true、writer空、四计数均0；提交521ae3c1054ea81e356e4d5e9e68a36a1259403e。主控证据最终HEAD 44617b354ea783a8e2faf9084741ecd35c80beee；BASE 6eaed6a2b1b7694acb243d091302802273953a5c。观察主线程未补卡/代写实现或代派正常角色。
- 主线程独立branch strict退出2；envelope退出0但内部BLOCKED。主控/主管已完成、作者已取消；底层命令终态仍UNKNOWN。
- 叶子声明截止02:47:35Z，实际取消02:47:49.667Z，晚14.667秒；实际会话147130ms小于150秒，不能用后者掩盖绝对截止偏差。
- Antigravity[1533](codeg://session/1533)独立验收：修复机制APPROVED、实际收尾COMPLIANT、时限DEVIATION、完整链BLOCKED。TypeSafe选择blocked（1.0），这是模型输出；Codex根据缺失产物与严格门禁裁决整链BLOCKED。
- 证据：build/stage06-budget-closeout-20261111/（修复RED/GREEN/66项回归/冻结候选/部署备份），其run02/含controller-result、native-sessions、observer-checks、antigravity-review及新沙箱。

## run01历史（原样保留）

## 已验证与尚缺证据

- 主控：[新会话1516](codeg://session/1516)，真实采用2号助手已部署指令，并委派3号主管1517；主管先claim及登记IN_PROGRESS，提交8dd53507dc7b79f981dd8b4c27d314d8156e6733后才派出测试作者1518。旧沙箱“初始领卡滞后”的证据缺口在本次得到覆盖。
- 主控自动查询、取消、交接并再次委派主管1519、作者1520，最后尝试主管1521做收尾；观察主线程未代写业务实现/补登记/代派正常链角色。
- 未形成有效RED，没有测试或业务实现变化，无实现C、登记D、APPROVED收据、GREEN/回归或全分支独立通过。基线1 passed不作GREEN，envelope退出0内部仍UNKNOWN。
- 主控运行626251ms（约10分26秒）后由观察主线程停止，较10分钟硬检查点晚26秒；六个执行会话原生状态均cancelled。1520调用过run_command/view_file但未交付命令终态输出，不能据会话取消推定所有底层进程终态。
- Antigravity独立只读验收[1522](codeg://session/1522)，task 7e1230f6-f31e-4ea4-ac75-10d8ec13fef4，结论BLOCKED。主线程在干净最终HEAD独立运行branch strict仍退出2，原因是任务未DONE且无有效收据覆盖；不是仅由未提交日志造成的失败。

## 本轮暴露的问题

1. **验证预算配比不合理**：每子任务150秒是本次观察主线程设置的测试限制，不是Skill默认。将主管及整棵子树装入150秒，导致首次测试叶子到绝对截止仅约32秒，第二次约47秒。本次未隔离启动/服务/工具耗时，不能断言预算是未交付的唯一原因，也不能外推为所有主控链不可行。
2. **超时回收偏晚**：两任主管实际162129/162890ms；主控记录的5分钟检查点也未精确到点。后续应缩短临近截止的等待，预留取消、查询终态和写证据的余量。
3. **阻断收尾未落卡**：外部已BLOCKED，卡仍IN_PROGRESS、is_blocked=false、blocked_reason空，writer仍为已取消的supervisor-resume-19b73406。收尾主管被取消；观察主线程保留原样，不替写后再声称自动链闭环。恢复前需先核对所有原执行终态，再按明确交接权限回收owner和登记阻断。

## 证据与综合裁决

证据根：`build/stage05-controller-chain-20261111/run01/`。

- `baseline.json`、`setup-commands.json`、`planning-score.json`：新离线Git仓库、TODO基线、规划真实四维90.7。
- `native-sessions.json`：实际派发、父子关系、取消终态；max_messages=0返回的消息数不作实际活跃度依据。`author-session-details.json`保存带实际消息的查询。
- `observer-checks.json`：业务/测试相对BASE无差异，主仓库及Worktree干净，根索引、三份37文件交付源码、助手1—4配置未变化；主控原生snapshot.instructions与权威模板一致。
- `observer-gates.json`、`branch-clean-final.log`、`envelope-final.log`：独立门禁命令、退出码及完整输出。
- `antigravity-review.md`：独立验收原文。保留其BLOCKED与问题事实；不采纳“失败严格只归因于预算”的排他因果措辞，也不将max_messages=0的统计解释为一般性的MCP消息统计缺陷。
- `typesafe-outcome.json`：TypeSafe完成概率0.02、叶子预算不足概率0.83、卡片已完整收尾概率0.12；这是模型判断。Codex依据真实派发、Git时序、缺失产物与独立验收裁定本轮BLOCKED。

## 历史：candidate05补证后的恢复门禁

1. 原命令终态已经由本次原生补证满足；保留旧卡FUSED/计数/未提交测试和旧未知日志，不回填历史。恢复不需要再次请求用户批准普通已授权步骤。
2. 新授权只读MCP通路已通过实际消费及独立验收；后续Antigravity叶子使用iteration-skill-readonly/read_skill_file读取主版本契约，保留原生拒绝和精确cwd，不换副本/工具绕过。
3. candidate05独立源码审查、CAS部署及新会话只读消费已完成；不重复有效门禁。解除权限阻断后启动新的2号主控会话恢复链：先核对原生终态和dirty归属，按授权replan登记恢复，不清累计计数；保存DONE/FUSED分离的有效RED，再用另一实现者GREEN/回归、非参与者审查C、登记D及严格门禁。
4. 实测守卫的请求/确认时间、叶子命令前截止核验与同调用证据落盘；无模型插入临界等待与取消。工具调用仍有延迟时如实报告，不把相对150秒未超当绝对截止达标。完整验收通过前不更新两个真实副本。

旧作者会话不恢复，业务卡不由观察线程补写。上列为candidate05时点的恢复记录，后续推进与当前恢复条件见本文首节及维护任务06。
