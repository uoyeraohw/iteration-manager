---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "06"
task_name: "真实自用链路与故障路径健壮性验收"
status: "TODO"
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
base_sha: ""
head_sha: ""
created_at: "2026-11-13"
updated_at: "2026-11-13"
---

# 06 · 真实自用链路与故障路径健壮性验收

> 声明 TODO；验收 UNKNOWN；尚无执行、RED/GREEN或独立批准。本文是已初始化计划，不授予实施、Git提交或部署权限。

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
实际task_id、UTC起止/检查点、候选、命令receipt、可继承产物、remaining_work、dirty归属及命令终态；未知明确UNKNOWN。每次真实终态后attempt，再release/closeout；四预算保持5/10/1/2。

### 7.3 审查与裁决
- 审查：PENDING；Reviewer未分配。
- Ruling：无执行裁决。需要改已验收共享源时退回原owner并重审受影响绑定，不在本卡偷偷扩大范围。
- Deferred Minors：无。
<!-- /iter:ledger -->
