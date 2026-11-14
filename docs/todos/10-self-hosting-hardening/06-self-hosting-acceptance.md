---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "06"
task_name: "真实自用链路与故障路径健壮性验收"
status: "TESTING"
type: "Spike-Discovery"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "87.675"
typesafe_evidence: "docs/todos/10-self-hosting-hardening/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: "7107ddb2f2256ceaea40e6ea0aeddd045220b99b"
head_sha: ""
created_at: "2026-11-13"
updated_at: "2026-11-14T01:10:27.224983+00:00"
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"\",\"events\":{\"iter10-06-claim-a\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"06-self-hosting-acceptance\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-14T01:02:36.989568+00:00\"},\"iter10-06-attempt-a\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/06/attempt-a.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"implementation\",\"candidate\":\"c5238c16b1e9c5d941d8dec3c53d273f6a074e44\",\"inputs\":[\"tests/test_self_hosting.py\",\"references/self_hosting_acceptance.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"checkpoint\":\"14项跨模块隔离契约通过，真实03 A/B/C链索引和方法已交付\",\"remaining_work\":[\"主控最终候选全量与交叉核验\",\"报告补齐/冻结独审\",\"登记C/D和strict\"],\"executor_id\":\"19637bc8-ff22-4810-b202-121b60285548\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/06/native-terminal-a.json\",\"progress\":[{\"kind\":\"green\",\"summary\":\"14 passed, 真实链索引与Note校验通过\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-targeted-2.json.output.txt\"}],\"commands\":[\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-targeted-1.json\",\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-targeted-2.json\",\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-frozen-strict-dry-run.json\",\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-native-inventory.json\",\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-native-inventory-2.json\",\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-note-tree.json\",\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-note-format.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/10-self-hosting-hardening/evidence/06/attempt-a.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"c5238c16b1e9c5d941d8dec3c53d273f6a074e44\",\"conditions\":{\"inputs\":[\"references/self_hosting_acceptance.md\",\"tests/test_self_hosting.py\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"scope\":[\".agents/notes/implemented/testing/2026-11-13-self-hosting-acceptance.md\",\"docs/todos/10-self-hosting-hardening/evidence/06/\",\"references/self_hosting_acceptance.md\",\"tests/test_self_hosting.py\"]},\"executor_id\":\"19637bc8-ff22-4810-b202-121b60285548\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/06/native-terminal-a.json\",\"progress\":[{\"kind\":\"green\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-targeted-2.json.output.txt\",\"summary\":\"14 passed, 真实链索引与Note校验通过\"}],\"checkpoint\":\"14项跨模块隔离契约通过，真实03 A/B/C链索引和方法已交付\",\"remaining_work\":[\"主控最终候选全量与交叉核验\",\"报告补齐/冻结独审\",\"登记C/D和strict\"],\"commands\":[{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-frozen-strict-dry-run.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":2,\"started_at\":\"2026-11-14T01:06:33.536804+00:00\",\"ended_at\":\"2026-11-14T01:06:53.758027+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-native-inventory-2.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-14T01:07:49.808604+00:00\",\"ended_at\":\"2026-11-14T01:07:50.058056+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-native-inventory.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-14T01:07:27.263830+00:00\",\"ended_at\":\"2026-11-14T01:07:27.492226+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-note-format.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-14T01:07:55.262012+00:00\",\"ended_at\":\"2026-11-14T01:07:57.741345+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-note-tree.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-14T01:07:51.223322+00:00\",\"ended_at\":\"2026-11-14T01:07:54.153157+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-targeted-1.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-14T01:04:24.262746+00:00\",\"ended_at\":\"2026-11-14T01:04:44.848096+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/06/slice-a-targeted-2.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-14T01:05:20.500549+00:00\",\"ended_at\":\"2026-11-14T01:05:39.455262+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":65.64830199999999}},\"result\":{\"task_id\":\"06-self-hosting-acceptance\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-14T01:10:26.929190+00:00\"},\"iter10-06-release-a\":{\"input\":{\"action\":\"release\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/06/native-terminal-a.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"06-self-hosting-acceptance\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-14T01:10:27.224983+00:00\"}},\"blocked_reason\":\"\"}"
---

# 06 · 真实自用链路与故障路径健壮性验收

> **当前状态**：声明 TESTING；14项隔离联合契约通过，真实链索引已交付；待最终全量、交叉核验与独审。

## 1. 任务执行目标与接口契约

- **主要目标**：把本迭代01—05的真实使用链、隔离负例及最终候选独立验收结合，验证Skill管理自身项目时不绕门禁、不丢失证据、不重复执行。
- **前置任务**：[05](./05-release-evidence-index.md) 验收PASS
- **Consumes**：固定协调工具46ded3a、本迭代01—05真实卡片与原生会话/runner证据、最终被测候选C；现有tests夹具和新模板生成入口；绝不修改01—05源码/收据来迁就测试。
- **Produces**：tests/test_self_hosting.py隔离契约回归；references/self_hosting_acceptance.md记录可复用自用方法；evidence/06/robustness-report.json包含version,candidate,coordinator_commit,cases[{id,layer,expected,observed,result,evidence}],unverified；layer只能static/synthetic/native-self-use，结论PASS/FAIL/UNKNOWN/BLOCKED。
- **唯一责任**：本卡主管持有卡片写权；一个实现owner负责白名单源文件及返修。读取相邻模块不获得修改权。初始owner未分配，不捏造会话ID。
- **共同约定**：完整阅读[迭代目标与执行约定](README.md)，继承冻结协调器、授权、独审及恢复规则。

## 2. 业务阶段与检查点

<!-- iter:stages -->
- [ ] Stage 1/3：整理01—05真实消费证据，隔离夹具运行故障与恢复路径
- [ ] Stage 2/3：候选完整回归、旧协调器与新候选只读交叉检查、一次真实跨会话检查点续接
- [ ] Stage 3/3：冻结实验报告与原始证据，交非参与者独审；整轮总审在本卡登记PASS后进行，不作为本卡待审前置。
<!-- /iter:stages -->

阶段可跨会话；正常检查点保存证据并release，不以超时强杀充当切片。比例是清单比例，不是工时。

## 3. 按类型验证规划

<!-- iter:verification -->
- [ ] 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。
- [ ] Spike实验无需伪造RED；新增测试如发现真实缺陷保留失败并退回原owner。experiment含实测链路，decision为边界结论，interfaces为报告字段及恢复交接。最终全量独立于单卡检查。
- [ ] 完成必需checks：experiment（成功命令）、decision（观测）、interfaces（观测）；所有原始输出、命令cwd、真实退出码和候选引用可追溯。
- [ ] 完成范围自检、冻结候选和待审输入；独立APPROVED后登记收据、DONE及D，再消费本地strict。
<!-- /iter:verification -->

### 可执行命令与证据

从精确Worktree根运行；`COORDINATOR_ROOT`为README指定冻结版本，`COMMAND_DEADLINE_UTC`与每次唯一receipt由实际派发者即时填写，不提前伪造：

```powershell
python "$env:COORDINATOR_ROOT/scripts/iter_run.py" --deadline "$env:COMMAND_DEADLINE_UTC" --evidence "docs/todos/10-self-hosting-hardening/evidence/06/regression-<唯一attempt>.json" -- python -B -m pytest -p no:cacheprovider tests/test_self_hosting.py -q
$code = $LASTEXITCODE; exit $code
```

- 上述新增测试文件由本卡在授权实施后创建，初始化时不存在不算失败或RED；不得直接运行不存在文件后声称有效RED。
- 内环选本卡具体测试节点；任务交付运行上述受影响集合并补齐本type原始观测/实验，使用唯一receipt，不增加不适用的RED要求。
- 总回归由任务06/整轮收口对实际最终候选运行，不以局部通过代替。
- Git范围命令：`python "$env:COORDINATOR_ROOT/scripts/iter_sync.py" --check-scope <实际BASE> <实际C> docs/todos/10-self-hosting-hardening/06-self-hosting-acceptance.md --include-worktree`。
- scope/独审/strict所用候选必须相同。真实命令通过runner留证；只读协调CLI、claim/release/attempt及精准Git登记按共同协议豁免包装。
- 声明的输出路径是未来产物位置，不是已有证据；不预先写入review_receipt或SHA。

## 4. 实施边界

保留现有CLI/旧卡/收据合同，不迁移历史、不部署副本、不清理已有目录。遇到已证实的冻结工具缺陷，记录具体影响并停止受影响门禁，交授权持有人裁决；不切换检查器绕过，也不降低本卡验收。非本卡必要的新发现只作建议。

## 5. 新增或变更内容清单

<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `tests/test_self_hosting.py` | CREATED | 本卡验证与兼容检查 |
| `references/self_hosting_acceptance.md` | CREATED | 真实自用链路与故障路径健壮性验收 |
| `.agents/notes/implemented/testing/2026-11-13-self-hosting-acceptance.md` | CREATED | 本卡决定与验证记录 |
| `docs/todos/10-self-hosting-hardening/evidence/06/` | CREATED | 原始命令、观测、attempt、独审报告及JSON收据 |
<!-- /iter:scope -->

任务卡和所属迭代README按现有规则隐式允许，仅主管串行登记。其它卡、其它任务源码、根总控和安装副本不在写范围。正式证据只在本卡目录追加唯一文件，不覆写；隔离夹具使用该目录下sandbox/或系统临时目录，不修改真实业务数据。

## 6. 确定性验收标准

<!-- iter:acceptance -->
- [ ] 至少一项真实任务完成inventory→claim→同owner dispatch-check→原生委派→命令收据→attempt→release→独审→C/D收据→strict链，至少一次新会话继承有效检查点而不无依据重跑。
- [ ] 隔离样例验证：缺授权、外来writer、缺context、候选/phase不符、依赖未PASS、连续两次无进展第三次拒绝、幂等重放/改payload拒绝、坏卡/未知DONE/FS漂移、根索引越权拒绝。
- [ ] runner/守卫超时与unknown、四预算、受控resume及FS拒绝Git grant复用既有有效测试或精准补验；不在真实卡制造假失败、耗尽预算或强杀用户服务。
- [ ] 本轮新增缺陷仅在满足既定合同所必需时返还原任务 owner；如需改已验收源，停止依赖、按影响范围重审并生成新绑定，禁止在06白名单外顺手修复。
- [ ] 主控、实现者、测试作者、设计/RCA参与者不作为该任务独立Reviewer；整轮另用非参与者聚焦接口/真实自用/全量证据；协调器与候选都不能单独自我批准。
- [ ] 全量 `python -B -m pytest -p no:cacheprovider tests -q` 在最终候选执行；真实浏览器沿用04有效证据或因变化精准补验。
- [ ] 隔离负例成功拦截不叫业务失败；静态/合成/原生真实自用分层报告。没有部署/用户业务项目整链证据不作该层通过声明。
- [ ] 必需checks原件、范围核验及待审候选齐备；未将实现者自检冒作独立批准。
<!-- /iter:acceptance -->

独审与登记为上述待审条件之后的完成门禁；未发生前不预勾选。独立Reviewer不得是本卡测试/实现/设计/RCA参与者。

## 7. 执行实证与裁决账本

<!-- iter:ledger -->
### 7.1 初始化事实
- 源码观察基线：`46ded3a4696e3bdb531d06951fce7982fa9db1cd`；实际执行BASE/C/D尚未产生。
- 规划质检：87.675/100；各维及原始请求/响应见[规划证据](evidence/planning/typesafe-summary.json)。该分数不是执行批准。
- 当前状态：未派发、无活动实现命令；未取得RED/GREEN/观测/独立审查。
- 本卡预计收据位置：`docs/todos/10-self-hosting-hardening/evidence/06/review.json`，实际产生后才登记frontmatter。

### 7.2 执行时填写
- 实现Codeg1723/session01a1d793-e65a-7251-8c92-b82981f6cf0c，task19637bc8-ff22-4810-b202-121b60285548原生completed；产品cd808bf3，正常检查点c5238c16；native-terminal-a.json含原始查询与完整截止守卫。所有命令tree_terminal=true，无活动命令。attempt→release，四预算未重置。
- 隔离测试14passed（首跑3项新测试API误用及首次提取器错误期待strict顶层0，均保留原件，不称产品缺陷或有效RED）。真实03 A/B/C正常续接及完整链、04浏览器和05正文漂移正确拒绝均分层索引。
- 本次06派发调用前协调命令仍由工具报告running，主控回收输出时才消费READY。保留此过程缺口，不把06本次派发当作严格的“先消费后委派”正例；完整合规链使用已有03原件，后续派发须等待并消费READY再调用。
- 当前剩余最终候选全量、冻结/候选交叉核验、范围与独审。实现/测试/Note不再变化时独立全量涵盖14项，不额外重复同输入定向测试。

### 7.3 审查与裁决
- 审查：PENDING；Reviewer未分配。
- Ruling：无执行裁决。需要改已验收共享源时退回原owner并重审受影响绑定，不在本卡偷偷扩大范围。
- Deferred Minors：无。
<!-- /iter:ledger -->
