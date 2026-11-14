---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "04"
task_name: "看板展示Git/FS候选和可继承交接"
status: "TESTING"
type: "UI-Component"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "88.275"
typesafe_evidence: "docs/todos/10-self-hosting-hardening/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: "docs/todos/10-self-hosting-hardening/evidence/04/review.json"
base_sha: "2ce0705ebeeaee73f75a1dcd2882836dbc6b9d29"
head_sha: "9b9010afb8dbf0b0cf74f83c6c97605984319619"
created_at: "2026-11-13"
updated_at: "2026-11-14T01:18:23.565362+00:00"
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"root/iter10/controller\",\"events\":{\"iter10-04-claim-a\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T18:10:05.929322+00:00\"},\"iter10-04-claim-b\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T18:18:18.888694+00:00\"},\"iter10-04-attempt-a\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/attempt-a-valid.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"implementation\",\"candidate\":\"7fe4b4dcab7110c0f3f6791e5f9ef0d5a29eaa67\",\"inputs\":[\"docs/todos/10-self-hosting-hardening/04-board-handoff.md\",\"templates/board.html\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"checkpoint\":\"模板Git/FS交接、精确计数和HTTP越界实测；最终五文件67passed；真实浏览器尚未验\",\"remaining_work\":[\"真实浏览器四态/交互/视觉\",\"独立审查\"],\"executor_id\":\"b0d6567f-d3d8-4a6f-aebb-8437e57b4cb9\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/native-terminal-a.json\",\"progress\":[{\"kind\":\"green\",\"summary\":\"67 passed，symlink实测拒绝\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-final-regression-1816.json.output.txt\"}],\"commands\":[\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-red-1812.json\",\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-green-1814.json\",\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-regression-1815.json\",\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-final-regression-1816.json\",\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-note-tree-1815.json\",\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-final-note-format-1816.json\",\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-scope-1816.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/10-self-hosting-hardening/evidence/04/attempt-a-valid.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"7fe4b4dcab7110c0f3f6791e5f9ef0d5a29eaa67\",\"conditions\":{\"inputs\":[\"docs/todos/10-self-hosting-hardening/04-board-handoff.md\",\"templates/board.html\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"scope\":[\".agents/notes/implemented/feature/2026-11-13-board-handoff.md\",\"docs/todos/10-self-hosting-hardening/evidence/04/\",\"templates/board.html\",\"tests/test_board_handoff.py\",\"tests/test_board_service.py\",\"tests/test_board_truth.py\"]},\"executor_id\":\"b0d6567f-d3d8-4a6f-aebb-8437e57b4cb9\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/native-terminal-a.json\",\"progress\":[{\"kind\":\"green\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-final-regression-1816.json.output.txt\",\"summary\":\"67 passed，symlink实测拒绝\"}],\"checkpoint\":\"模板Git/FS交接、精确计数和HTTP越界实测；最终五文件67passed；真实浏览器尚未验\",\"remaining_work\":[\"独立审查\",\"真实浏览器四态/交互/视觉\"],\"commands\":[{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-final-note-format-1816.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T18:15:44.813287+00:00\",\"ended_at\":\"2026-11-13T18:15:47.124672+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-final-regression-1816.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T18:15:35.653140+00:00\",\"ended_at\":\"2026-11-13T18:15:57.822802+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-green-1814.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T18:13:34.998966+00:00\",\"ended_at\":\"2026-11-13T18:13:41.960743+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-note-tree-1815.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T18:15:08.597633+00:00\",\"ended_at\":\"2026-11-13T18:15:11.032853+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-red-1812.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-13T18:12:16.138557+00:00\",\"ended_at\":\"2026-11-13T18:12:27.337590+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-regression-1815.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T18:14:27.474611+00:00\",\"ended_at\":\"2026-11-13T18:14:56.174888+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/04/slice-a-scope-1816.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T18:16:23.589548+00:00\",\"ended_at\":\"2026-11-13T18:16:24.545649+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":72.42207}},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T18:18:47.006666+00:00\"},\"iter10-04-release-a\":{\"input\":{\"action\":\"release\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/native-terminal-a.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-13T18:18:47.355134+00:00\"},\"iter10-04-claim-browser-b\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T18:18:47.740318+00:00\"},\"iter10-04-attempt-review\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"build/review-04/attempt-review.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"evidence-inspection\",\"candidate\":\"9b9010afb8dbf0b0cf74f83c6c97605984319619\",\"inputs\":[\"docs/todos/10-self-hosting-hardening/04-board-handoff.md\",\"templates/board.html\"],\"capabilities\":[\"Codeg MCP codex independent review\"],\"checkpoint\":\"04独立Scope/Spec/Quality APPROVED，原始交互、七图和匹配源码回归核对\",\"remaining_work\":[\"登记D后local strict\"],\"executor_id\":\"15039ddf-a469-47ed-9c5a-2a732ef24dbf\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/review-report.json\",\"progress\":[{\"kind\":\"review-finding\",\"summary\":\"APPROVED；无阻断缺口，未冒称部署\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/review-report.json\"}],\"commands\":[],\"started_at\":null,\"ended_at\":null},\"source\":\"build/review-04/attempt-review.json\",\"phase\":\"evidence-inspection\",\"delivery_mode\":\"git\",\"candidate\":\"9b9010afb8dbf0b0cf74f83c6c97605984319619\",\"conditions\":{\"inputs\":[\"docs/todos/10-self-hosting-hardening/04-board-handoff.md\",\"templates/board.html\"],\"capabilities\":[\"Codeg MCP codex independent review\"],\"scope\":[\".agents/notes/implemented/feature/2026-11-13-board-handoff.md\",\"docs/todos/10-self-hosting-hardening/evidence/04/\",\"templates/board.html\",\"tests/test_board_handoff.py\",\"tests/test_board_service.py\",\"tests/test_board_truth.py\"]},\"executor_id\":\"15039ddf-a469-47ed-9c5a-2a732ef24dbf\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/review-report.json\",\"progress\":[{\"kind\":\"review-finding\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/review-report.json\",\"summary\":\"APPROVED；无阻断缺口，未冒称部署\"}],\"checkpoint\":\"04独立Scope/Spec/Quality APPROVED，原始交互、七图和匹配源码回归核对\",\"remaining_work\":[\"登记D后local strict\"],\"commands\":[],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":null}},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T18:29:46.449909+00:00\"},\"iter10-04-release-review\":{\"input\":{\"action\":\"release\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/04/review-report.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-13T18:29:46.773665+00:00\"},\"iter10-04-claim-repair-final\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"04-board-handoff\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-14T01:18:23.565362+00:00\"}},\"blocked_reason\":\"\"}"
---

# 04 · 看板展示Git/FS候选和可继承交接

> **当前状态**：TESTING；06最终全量发现HTTP夹具就绪超时，定点重开测试；原UI证据保留。

## 1. 任务执行目标与接口契约

- **主要目标**：仅在展示与交互层消费任务03冻结的字段，让用户从看板辨认真实候选、检查点和剩余工作；不重写查询/CLI源码。
- **前置任务**：[03](./03-query-cli-contract.md) 验收PASS
- **Consumes**：任务03 generate_board_data(iter_dir) cards中的delivery_mode、candidate_id、execution.checkpoint/remaining_work及既有head_sha/base_sha/sources；旧卡未知语义和本地HTTP安全边界。
- **Produces**：templates/board.html 按delivery_mode展示Git BASE/C或FS candidate_id和列明证据入口；详情增加最近有效检查点及剩余工作，筛选/键盘/刷新/断连行为可观测。数据读取接口及旧CLI不变。
- **唯一责任**：本卡主管持有卡片写权；一个实现owner负责白名单源文件及返修。读取相邻模块不获得修改权。初始owner未分配，不捏造会话ID。
- **共同约定**：完整阅读[迭代目标与执行约定](README.md)，继承冻结协调器、授权、独审及恢复规则。

## 2. 业务阶段与检查点

<!-- iter:stages -->
- [x] Stage 1/3：固定真实用户路径、视口和四态输入，基于03字段更新详情展示
- [x] Stage 2/3：补精确计数、候选/交接展示与HTTP边界测试
- [x] Stage 3/3：实际浏览器完成交互/状态/视觉检查，独立审查冻结模板
<!-- /iter:stages -->

阶段可跨会话；正常检查点保存证据并release，不以超时强杀充当切片。比例是清单比例，不是工时。

## 3. 按类型验证规划

<!-- iter:verification -->
- [x] 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。
- [x] UI按interaction/states/visual/regression四checks，实际浏览器证据必需；功能测试在可执行条件下先失败再修复，如实记录，不以导入失败冒RED。
- [x] 完成必需checks：interaction（成功命令）、states（观测）、visual（观测）、regression（0）；所有原始输出、命令cwd、真实退出码和候选引用可追溯。
- [x] 完成范围自检、冻结候选和待审输入；独立APPROVED后登记收据、DONE及D，再消费本地strict。
<!-- /iter:verification -->

### 可执行命令与证据

从精确Worktree根运行；`COORDINATOR_ROOT`为README指定冻结版本，`COMMAND_DEADLINE_UTC`与每次唯一receipt由实际派发者即时填写，不提前伪造：

```powershell
python "$env:COORDINATOR_ROOT/scripts/iter_run.py" --deadline "$env:COMMAND_DEADLINE_UTC" --evidence "docs/todos/10-self-hosting-hardening/evidence/04/regression-<唯一attempt>.json" -- python -B -m pytest -p no:cacheprovider tests/test_board_handoff.py tests/test_board_truth.py tests/test_board_service.py tests/test_query_contract.py tests/test_filesystem_delivery_controller.py -q
$code = $LASTEXITCODE; exit $code
```

- 上述新增测试文件由本卡在授权实施后创建，初始化时不存在不算失败或RED；不得直接运行不存在文件后声称有效RED。
- 内环选本卡具体测试节点；任务交付运行上述受影响集合并补齐本type原始观测/实验，使用唯一receipt，不增加不适用的RED要求。
- UI真实交互输出归interaction成功检查命令关联的原生观测记录；states/visual分别留原件。不能用截图或字段声明代替真实输入。
- 总回归由任务06/整轮收口对实际最终候选运行，不以局部通过代替。
- Git范围命令：`python "$env:COORDINATOR_ROOT/scripts/iter_sync.py" --check-scope <实际BASE> <实际C> docs/todos/10-self-hosting-hardening/04-board-handoff.md --include-worktree`。
- scope/独审/strict所用候选必须相同。真实命令通过runner留证；只读协调CLI、claim/release/attempt及精准Git登记按共同协议豁免包装。
- 声明的输出路径是未来产物位置，不是已有证据；不预先写入review_receipt或SHA。

## 4. 实施边界

保留现有CLI/旧卡/收据合同，不迁移历史、不部署副本、不清理已有目录。遇到已证实的冻结工具缺陷，记录具体影响并停止受影响门禁，交授权持有人裁决；不切换检查器绕过，也不降低本卡验收。非本卡必要的新发现只作建议。

## 5. 新增或变更内容清单

<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `templates/board.html` | MODIFIED | 看板展示Git/FS候选和可继承交接 |
| `tests/test_board_truth.py` | MODIFIED | 本卡验证与兼容检查 |
| `tests/test_board_service.py` | MODIFIED | 本卡验证与兼容检查 |
| `tests/test_board_handoff.py` | CREATED | 本卡验证与兼容检查 |
| `.agents/notes/implemented/feature/2026-11-13-board-handoff.md` | CREATED | 本卡决定与验证记录 |
| `docs/todos/10-self-hosting-hardening/evidence/04/` | CREATED | 原始命令、观测、attempt、独审报告及JSON收据 |
<!-- /iter:scope -->

任务卡和所属迭代README按现有规则隐式允许，仅主管串行登记。其它卡、其它任务源码、根总控和安装副本不在写范围。正式证据只在本卡目录追加唯一文件，不覆写；隔离夹具使用该目录下sandbox/或系统临时目录，不修改真实业务数据。

## 6. 确定性验收标准

<!-- iter:acceptance -->
- [x] Git显示BASE/C，FS显示candidate_id而非空SHA；候选模式未知明确未知。冻结证据只用现有sources的列明入口，不接受任意路径。
- [x] 最近有效检查点保留原候选/证据出处；缺记录显示未知，remaining_work为空不推断任务完成。
- [x] 真实桌面浏览器筛选→开详情→读候选与剩余项→打开原文→键盘关闭；记录实际视口，验证正常/空/加载/断连错误；不得DOM注入/内部store代替用户输入。
- [x] README/终端/HTML的DONE与PASS精确计数一致；HTTP读取只读、不泄露未列明文件，路由级symlink越界拒绝；权限不足时明确未验不跳过当通过。
- [x] 不改03查询/CLI源码。发现接口缺陷退回03并重审受影响候选；UI截图与交互分别留证，不用截图推断交互成功。
- [x] 必需checks原件、范围核验及待审候选齐备；未将实现者自检冒作独立批准。
<!-- /iter:acceptance -->

独审与登记为上述待审条件之后的完成门禁；未发生前不预勾选。独立Reviewer不得是本卡测试/实现/设计/RCA参与者。

## 7. 执行实证与裁决账本

<!-- iter:ledger -->
### 7.1 初始化事实
- 源码观察基线：`46ded3a4696e3bdb531d06951fce7982fa9db1cd`；实际执行BASE/C/D尚未产生。
- 规划质检：88.275/100；各维及原始请求/响应见[规划证据](evidence/planning/typesafe-summary.json)。该分数不是执行批准。
- 当前状态：未派发、无活动实现命令；未取得RED/GREEN/观测/独立审查。
- 本卡预计收据位置：`docs/todos/10-self-hosting-hardening/evidence/04/review.json`，实际产生后才登记frontmatter。

### 7.2 执行时填写
- A实际task_id=b0d6567f-d3d8-4a6f-aebb-8437e57b4cb9，Codeg会话1718；原生completed，守卫无超期。实现C=c2d90643cc391168e0e424843c761e9291629d99，检查点7fe4b4d；4项有效断言RED，最终指定五文件67passed。实际Windows symlink创建及HTTP越界拒绝通过，未skip。原件见evidence/04/native-terminal-a.json与implementation-checkpoint-a.json。
- 主控attempt首次漏两个必需时间键，被固定工具退出2拒绝，保留attempt-a.json和coordination-report-rejection.json；另存attempt-a-valid.json以null保留未知时间，成功登记后release/claim，不清预算。
- B主控原生ego-browser TaskSpace5/p1，1139×869：真实Git三卡PASS筛选、03详情BASE/C、列明收据链接弹窗、Escape；04真实检查点/剩余项。FS/empty/loading使用明确隔离合成输入，仍经真实HTTP和原生用户输入。手动刷新时间改变，停止自有FS服务触发断连，原快照保留。见browser-*-b.json及对应output/screenshot、states-observation.json、visual-observation.json。
- 浏览器TaskSpace正常finish；自有HTTP服务由stop-file正常退出，browser-service-b.json为COMPLETED/exit0/tree_terminal=true。主控独立五文件回归controller-regression-b.json为67passed；无活动实现或测试命令。未部署/推送/合流/清理Worktree。
- TypeSafe进入独审判断submit（0.65概率；不作批准）；完整原件typesafe-ui-review-readiness.json。剩余：独立Reviewer、登记C/D及固定strict。

### 7.3 审查与裁决
- 定点重开：06最终全量490passed/1failed，test_board_handoff.py:94固定8秒等待未等到ready；同脚本隔离观测8.562秒后ready=true、exit0、stderr空。证据在06/controller-full-regression与controller-harness-diagnosis；只重开受影响夹具/测试可靠性，禁止06越白名单修复。产品UI未改则沿用04真实交互/截图/四态证据，需新绑定独审及strict。06暂停放行，预算和历史事件保留。
- 审查：Codeg独立会话1719，真实session 01a1d627-da6f-75c3-87c5-5431d61a2594；Scope/Spec/Quality APPROVED，issues=[]。冻结C/contract=9b9010afb8dbf0b0cf74f83c6c97605984319619；报告及原生终态完整收录于evidence/04/review-report.json，收据evidence/04/review.json。
- Ruling：无执行裁决。需要改已验收共享源时退回原owner并重审受影响绑定，不在本卡偷偷扩大范围。
- Deferred Minors：无。
<!-- /iter:ledger -->
