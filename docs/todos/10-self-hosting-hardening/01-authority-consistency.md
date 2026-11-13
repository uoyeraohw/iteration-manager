---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "01"
task_name: "统一授权规则与跨入口场景"
status: "FUSED"
type: "Spike-Discovery"
fix_rounds: 0
replan_count: 0
is_blocked: true
blocked_reason: "execution deadline; slice B committed before canceled reply; explicit single-use resume-checkpoint authorization required to continue review"
typesafe_score: "88.275"
typesafe_evidence: "docs/todos/10-self-hosting-hardening/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
created_at: "2026-11-13"
updated_at: "2026-11-13T16:31:37.211266+00:00"
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"\",\"events\":{\"iter10-01-claim-01\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"01-authority-consistency\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:10:10.745424+00:00\"},\"iter10-01-attempt-a\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/attempt-implementation-a.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"implementation\",\"candidate\":\"5ff7c3af554f9effdf0a95050af24c767ca0878b\",\"inputs\":[\"docs/todos/10-self-hosting-hardening/01-authority-consistency.md\",\"references/worktree_git_contract.md\",\"references/superpowers_handbook.md\",\"templates/root_readme.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\"],\"checkpoint\":\"文档授权冲突修正、11项回归通过；真实四场景仍UNKNOWN\",\"remaining_work\":[\"四个真实新会话消费\",\"新会话继承并汇总authority-matrix\",\"独审\",\"登记strict\"],\"executor_id\":\"fcdae243-1628-427e-8f85-51ccfb4fef64\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/native-terminal-implementation-a.json\",\"progress\":[{\"kind\":\"implementation\",\"summary\":\"授权边界文档/流程图与测试差异已提交，非单纯阅读\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/implementation-checkpoint-a.json\"},{\"kind\":\"green\",\"summary\":\"11项文本/卡片回归通过\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/delivery-regression-final-a.json.output.txt\"}],\"commands\":[\"docs/todos/10-self-hosting-hardening/evidence/01/text-regression-checkpoint-a.json\",\"docs/todos/10-self-hosting-hardening/evidence/01/note-tree-checkpoint-a.json\",\"docs/todos/10-self-hosting-hardening/evidence/01/note-format-checkpoint-a.json\",\"docs/todos/10-self-hosting-hardening/evidence/01/delivery-regression-checkpoint-a.json\",\"docs/todos/10-self-hosting-hardening/evidence/01/delivery-regression-final-a.json\",\"docs/todos/10-self-hosting-hardening/evidence/01/scope-checkpoint-a.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/10-self-hosting-hardening/evidence/01/attempt-implementation-a.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"5ff7c3af554f9effdf0a95050af24c767ca0878b\",\"conditions\":{\"inputs\":[\"docs/todos/10-self-hosting-hardening/01-authority-consistency.md\",\"references/superpowers_handbook.md\",\"references/worktree_git_contract.md\",\"templates/root_readme.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\"],\"scope\":[\".agents/notes/implemented/process/2026-11-13-authority-consistency.md\",\"docs/todos/10-self-hosting-hardening/evidence/01/\",\"references/superpowers_handbook.md\",\"references/worktree_git_contract.md\",\"templates/root_readme.md\",\"tests/test_authority_scenarios.py\",\"tests/test_prompt_sources.py\"]},\"executor_id\":\"fcdae243-1628-427e-8f85-51ccfb4fef64\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/native-terminal-implementation-a.json\",\"progress\":[{\"kind\":\"implementation\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/implementation-checkpoint-a.json\",\"summary\":\"授权边界文档/流程图与测试差异已提交，非单纯阅读\"},{\"kind\":\"green\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/delivery-regression-final-a.json.output.txt\",\"summary\":\"11项文本/卡片回归通过\"}],\"checkpoint\":\"文档授权冲突修正、11项回归通过；真实四场景仍UNKNOWN\",\"remaining_work\":[\"四个真实新会话消费\",\"新会话继承并汇总authority-matrix\",\"独审\",\"登记strict\"],\"commands\":[{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/delivery-regression-checkpoint-a.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:14:16.607026+00:00\",\"ended_at\":\"2026-11-13T16:14:20.013835+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/delivery-regression-final-a.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:14:51.388012+00:00\",\"ended_at\":\"2026-11-13T16:14:55.488284+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/note-format-checkpoint-a.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:13:55.706967+00:00\",\"ended_at\":\"2026-11-13T16:13:58.342096+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/note-tree-checkpoint-a.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:13:51.358301+00:00\",\"ended_at\":\"2026-11-13T16:13:54.542208+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/scope-checkpoint-a.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:15:16.856585+00:00\",\"ended_at\":\"2026-11-13T16:15:17.832364+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/text-regression-checkpoint-a.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:13:47.114132+00:00\",\"ended_at\":\"2026-11-13T16:13:50.204893+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":17.392657}},\"result\":{\"task_id\":\"01-authority-consistency\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:18:21.808642+00:00\"},\"iter10-01-release-a\":{\"input\":{\"action\":\"release\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/native-terminal-implementation-a.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"01-authority-consistency\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:18:22.138908+00:00\"},\"iter10-01-claim-b\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"01-authority-consistency\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:19:30.265957+00:00\"},\"iter10-01-attempt-b\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/attempt-implementation-b.json\",\"executor_state\":\"canceled\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"implementation\",\"candidate\":\"612cfde035f5fc96cec9d60435296af4e84be307\",\"inputs\":[\"docs/todos/10-self-hosting-hardening/01-authority-consistency.md\",\"references/worktree_git_contract.md\",\"references/superpowers_handbook.md\",\"templates/root_readme.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\"],\"checkpoint\":\"四类原生只读消费及磁盘/Git观察已提交；父会话在提交后回复前被deadline取消，不能按normal release\",\"remaining_work\":[\"取得本次单次resume-checkpoint明确授权\",\"恢复门禁\",\"非参与者独审\",\"登记strict\"],\"executor_id\":\"6c6e933a-5d58-4dbb-aa57-3d953f675e2f\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/native-terminal-implementation-b.json\",\"progress\":[{\"kind\":\"implementation\",\"summary\":\"四个新会话原始调用/终态、磁盘变化归属和矩阵提交612cfde，整卡仍未批准\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/implementation-checkpoint-b.json\"},{\"kind\":\"green\",\"summary\":\"消费库存核验命令0且source/test/note相对A不变，复用A回归，无重复跑\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/consumption-b/verification.json.output.txt\"}],\"commands\":[\"docs/todos/10-self-hosting-hardening/evidence/01/consumption-b/verification.json\",\"docs/todos/10-self-hosting-hardening/evidence/01/consumption-b/scope.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/10-self-hosting-hardening/evidence/01/attempt-implementation-b.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"612cfde035f5fc96cec9d60435296af4e84be307\",\"conditions\":{\"inputs\":[\"docs/todos/10-self-hosting-hardening/01-authority-consistency.md\",\"references/superpowers_handbook.md\",\"references/worktree_git_contract.md\",\"templates/root_readme.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\"],\"scope\":[\".agents/notes/implemented/process/2026-11-13-authority-consistency.md\",\"docs/todos/10-self-hosting-hardening/evidence/01/\",\"references/superpowers_handbook.md\",\"references/worktree_git_contract.md\",\"templates/root_readme.md\",\"tests/test_authority_scenarios.py\",\"tests/test_prompt_sources.py\"]},\"executor_id\":\"6c6e933a-5d58-4dbb-aa57-3d953f675e2f\",\"executor_state\":\"canceled\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/native-terminal-implementation-b.json\",\"progress\":[{\"kind\":\"implementation\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/implementation-checkpoint-b.json\",\"summary\":\"四个新会话原始调用/终态、磁盘变化归属和矩阵提交612cfde，整卡仍未批准\"},{\"kind\":\"green\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/consumption-b/verification.json.output.txt\",\"summary\":\"消费库存核验命令0且source/test/note相对A不变，复用A回归，无重复跑\"}],\"checkpoint\":\"四类原生只读消费及磁盘/Git观察已提交；父会话在提交后回复前被deadline取消，不能按normal release\",\"remaining_work\":[\"取得本次单次resume-checkpoint明确授权\",\"恢复门禁\",\"登记strict\",\"非参与者独审\"],\"commands\":[{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/consumption-b/scope.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:27:30.116955+00:00\",\"ended_at\":\"2026-11-13T16:27:31.236707+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/01/consumption-b/verification.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:27:20.132815+00:00\",\"ended_at\":\"2026-11-13T16:27:20.487479+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":1.4744160000000002}},\"result\":{\"task_id\":\"01-authority-consistency\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:31:36.838079+00:00\"},\"iter10-01-closeout-b\":{\"input\":{\"action\":\"closeout\",\"owner\":\"root/iter10/controller\",\"reason\":\"execution deadline; slice B committed before canceled reply; explicit single-use resume-checkpoint authorization required to continue review\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/01/native-terminal-implementation-b.json\",\"executor_state\":\"canceled\"},\"result\":{\"task_id\":\"01-authority-consistency\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":true,\"status\":\"FUSED\",\"blocked_reason\":\"execution deadline; slice B committed before canceled reply; explicit single-use resume-checkpoint authorization required to continue review\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:31:37.211266+00:00\"}},\"blocked_reason\":\"execution deadline; slice B committed before canceled reply; explicit single-use resume-checkpoint authorization required to continue review\"}"
---

# 01 · 统一授权规则与跨入口场景

> 声明 TODO；验收 UNKNOWN；尚无执行、RED/GREEN或独立批准。本文是已初始化计划，不授予实施、Git提交或部署权限。

## 1. 任务执行目标与接口契约

- **主要目标**：移除Worktree及相关模板与共同协议相反的自动提交/合流/清理指令，以实际新会话消费验证仅Prompt、无Git权限、他人dirty、未授权合流四类行为。
- **前置任务**：无
- **Consumes**：SKILL.md、references/agent_protocol.md、references/task_card_schema.md 在工具基线46ded3a上的授权与证据合同；不改其既有收据字段。
- **Produces**：references/worktree_git_contract.md 与共同协议一致；evidence/01/authority-matrix.json（version:1, scenarios:[{id,authority,allowed,forbidden,source_paths,observed_result,evidence}]），包含prompt_only/no_git_permission/preexisting_dirty/no_merge_permission四项；observed_result只能为PASS/FAIL/UNKNOWN，来自真实新会话而非手填推测。
- **唯一责任**：本卡主管持有卡片写权；一个实现owner负责白名单源文件及返修。读取相邻模块不获得修改权。初始owner未分配，不捏造会话ID。
- **共同约定**：完整阅读[迭代目标与执行约定](README.md)，继承冻结协调器、授权、独审及恢复规则。

## 2. 业务阶段与检查点

<!-- iter:stages -->
- [ ] Stage 1/3：对照引用链形成冲突清单和四类场景的可观察预期
- [ ] Stage 2/3：修正文档、命令及流程图，完成文本回归与真实新会话场景
- [ ] Stage 3/3：冻结候选与消费证据，非参与者审查后登记
<!-- /iter:stages -->

阶段可跨会话；正常检查点保存证据并release，不以超时强杀充当切片。比例是清单比例，不是工时。

## 3. 按类型验证规划

<!-- iter:verification -->
- [ ] 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。
- [ ] 非TDD文档任务，不要求或补造历史RED；experiment为场景核验程序成功且真实消费记录齐全，decision为冲突处置，interfaces为authority-matrix。
- [ ] 完成必需checks：experiment（成功命令）、decision（观测）、interfaces（观测）；所有原始输出、命令cwd、真实退出码和候选引用可追溯。
- [ ] 完成范围自检、冻结候选和待审输入；独立APPROVED后登记收据、DONE及D，再消费本地strict。
<!-- /iter:verification -->

### 可执行命令与证据

从精确Worktree根运行；`COORDINATOR_ROOT`为README指定冻结版本，`COMMAND_DEADLINE_UTC`与每次唯一receipt由实际派发者即时填写，不提前伪造：

```powershell
python "$env:COORDINATOR_ROOT/scripts/iter_run.py" --deadline "$env:COMMAND_DEADLINE_UTC" --evidence "docs/todos/10-self-hosting-hardening/evidence/01/regression-<唯一attempt>.json" -- python -B -m pytest -p no:cacheprovider tests/test_prompt_sources.py tests/test_task_card_schema.py tests/test_authority_scenarios.py -q
$code = $LASTEXITCODE; exit $code
```

- 上述新增测试文件由本卡在授权实施后创建，初始化时不存在不算失败或RED；不得直接运行不存在文件后声称有效RED。
- 内环选本卡具体测试节点；任务交付运行上述受影响集合并补齐本type原始观测/实验，使用唯一receipt，不增加不适用的RED要求。
- 总回归由任务06/整轮收口对实际最终候选运行，不以局部通过代替。
- Git范围命令：`python "$env:COORDINATOR_ROOT/scripts/iter_sync.py" --check-scope <实际BASE> <实际C> docs/todos/10-self-hosting-hardening/01-authority-consistency.md --include-worktree`。
- scope/独审/strict所用候选必须相同。真实命令通过runner留证；只读协调CLI、claim/release/attempt及精准Git登记按共同协议豁免包装。
- 声明的输出路径是未来产物位置，不是已有证据；不预先写入review_receipt或SHA。

## 4. 实施边界

保留现有CLI/旧卡/收据合同，不迁移历史、不部署副本、不清理已有目录。遇到已证实的冻结工具缺陷，记录具体影响并停止受影响门禁，交授权持有人裁决；不切换检查器绕过，也不降低本卡验收。非本卡必要的新发现只作建议。

## 5. 新增或变更内容清单

<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `references/worktree_git_contract.md` | MODIFIED | 统一授权规则与跨入口场景 |
| `references/superpowers_handbook.md` | MODIFIED | 统一授权规则与跨入口场景 |
| `templates/root_readme.md` | MODIFIED | 统一授权规则与跨入口场景 |
| `tests/test_prompt_sources.py` | MODIFIED | 本卡验证与兼容检查 |
| `tests/test_authority_scenarios.py` | CREATED | 本卡验证与兼容检查 |
| `.agents/notes/implemented/process/2026-11-13-authority-consistency.md` | CREATED | 本卡决定与验证记录 |
| `docs/todos/10-self-hosting-hardening/evidence/01/` | CREATED | 原始命令、观测、attempt、独审报告及JSON收据 |
<!-- /iter:scope -->

任务卡和所属迭代README按现有规则隐式允许，仅主管串行登记。其它卡、其它任务源码、根总控和安装副本不在写范围。正式证据只在本卡目录追加唯一文件，不覆写；隔离夹具使用该目录下sandbox/或系统临时目录，不修改真实业务数据。

## 6. 确定性验收标准

<!-- iter:acceptance -->
- [ ] 四类新会话只返回符合授权的行动，不写业务/不提交/不清理；以原生调用记录和磁盘/Git只读核对支撑，不仅靠回答承诺。
- [ ] git add整个docs/todos、Prompt前自动补Commit、自动合流销毁不再作为无条件指令；仍保留执行前提交门禁。
- [ ] 原历史记录不改写，权限缺口仅阻断相应动作；旧预算、TDD与独审规则不降级。
- [ ] 必需checks原件、范围核验及待审候选齐备；未将实现者自检冒作独立批准。
<!-- /iter:acceptance -->

独审与登记为上述待审条件之后的完成门禁；未发生前不预勾选。独立Reviewer不得是本卡测试/实现/设计/RCA参与者。

## 7. 执行实证与裁决账本

<!-- iter:ledger -->
### 7.1 初始化事实
- 源码观察基线：`46ded3a4696e3bdb531d06951fce7982fa9db1cd`；实际执行BASE/C/D尚未产生。
- 规划质检：88.275/100；各维及原始请求/响应见[规划证据](evidence/planning/typesafe-summary.json)。该分数不是执行批准。
- 当前状态：未派发、无活动实现命令；未取得RED/GREEN/观测/独立审查。
- 本卡预计收据位置：`docs/todos/10-self-hosting-hardening/evidence/01/review.json`，实际产生后才登记frontmatter。

### 7.2 执行记录
- 规划提交P：d3bd97ab16ffed6104034a887a01eb1b4d75dc0e；Worktree已创建，固定协调器46ded3a已导出。完整基线314 passed，runner原件见evidence/01/baseline-suite.json。
- 切片A：实现会话1702 / fcdae243-1628-427e-8f85-51ccfb4fef64，正常completed；提交5ff7c3af554f9effdf0a95050af24c767ca0878b。11项受影响回归通过，六个命令已终态；已attempt→release→envelope。正式原件见implementation-checkpoint-a.json及native-terminal-implementation-a.json。
- 切片B：新会话1703 / 6c6e933a-5d58-4dbb-aa57-3d953f675e2f从A交接续接，未重跑未受影响回归。四类真实新会话与磁盘/Git观察提交612cfde035f5fc96cec9d60435296af4e84be307，type原件见implementation-checkpoint-b.json、consumption-b/及authority-matrix.json。场景观察PASS不表示整卡验收PASS。
- B在提交后回复前触及截止守卫，实际canceled；最后Git命令原始exit0，四叶子由原派发者已查completed且命令终态齐全。主控查询嵌套ID为unknown属于查询归属限制，未据此推断停止，沿用原派发原件。已attempt并closeout为FUSED、writer释放；四预算仍0/0/0/0。
- 用户已明确授权本次单次resume-checkpoint，原文见resume-b-authority.txt；终态清单见terminal-for-resume-b.json。下一步绑定干净HEAD签发一次能力后恢复，只推进独审/登记，不重做已有效工作。暂无独立APPROVED。

### 7.3 审查与裁决
- 审查：PENDING；Reviewer未分配。
- Ruling：无执行裁决。需要改已验收共享源时退回原owner并重审受影响绑定，不在本卡偷偷扩大范围。
- Deferred Minors：无。
<!-- /iter:ledger -->
