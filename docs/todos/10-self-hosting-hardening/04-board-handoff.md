---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "04"
task_name: "看板展示Git/FS候选和可继承交接"
status: "TODO"
type: "UI-Component"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "88.275"
typesafe_evidence: "docs/todos/10-self-hosting-hardening/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
created_at: "2026-11-13"
updated_at: "2026-11-13"
---

# 04 · 看板展示Git/FS候选和可继承交接

> 声明 TODO；验收 UNKNOWN；尚无执行、RED/GREEN或独立批准。本文是已初始化计划，不授予实施、Git提交或部署权限。

## 1. 任务执行目标与接口契约

- **主要目标**：仅在展示与交互层消费任务03冻结的字段，让用户从看板辨认真实候选、检查点和剩余工作；不重写查询/CLI源码。
- **前置任务**：[03](./03-query-cli-contract.md) 验收PASS
- **Consumes**：任务03 generate_board_data(iter_dir) cards中的delivery_mode、candidate_id、execution.checkpoint/remaining_work及既有head_sha/base_sha/sources；旧卡未知语义和本地HTTP安全边界。
- **Produces**：templates/board.html 按delivery_mode展示Git BASE/C或FS candidate_id和列明证据入口；详情增加最近有效检查点及剩余工作，筛选/键盘/刷新/断连行为可观测。数据读取接口及旧CLI不变。
- **唯一责任**：本卡主管持有卡片写权；一个实现owner负责白名单源文件及返修。读取相邻模块不获得修改权。初始owner未分配，不捏造会话ID。
- **共同约定**：完整阅读[迭代目标与执行约定](README.md)，继承冻结协调器、授权、独审及恢复规则。

## 2. 业务阶段与检查点

<!-- iter:stages -->
- [ ] Stage 1/3：固定真实用户路径、视口和四态输入，基于03字段更新详情展示
- [ ] Stage 2/3：补精确计数、候选/交接展示与HTTP边界测试
- [ ] Stage 3/3：实际浏览器完成交互/状态/视觉检查，独立审查冻结模板
<!-- /iter:stages -->

阶段可跨会话；正常检查点保存证据并release，不以超时强杀充当切片。比例是清单比例，不是工时。

## 3. 按类型验证规划

<!-- iter:verification -->
- [ ] 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。
- [ ] UI按interaction/states/visual/regression四checks，实际浏览器证据必需；功能测试在可执行条件下先失败再修复，如实记录，不以导入失败冒RED。
- [ ] 完成必需checks：interaction（成功命令）、states（观测）、visual（观测）、regression（0）；所有原始输出、命令cwd、真实退出码和候选引用可追溯。
- [ ] 完成范围自检、冻结候选和待审输入；独立APPROVED后登记收据、DONE及D，再消费本地strict。
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
- [ ] Git显示BASE/C，FS显示candidate_id而非空SHA；候选模式未知明确未知。冻结证据只用现有sources的列明入口，不接受任意路径。
- [ ] 最近有效检查点保留原候选/证据出处；缺记录显示未知，remaining_work为空不推断任务完成。
- [ ] 真实桌面浏览器筛选→开详情→读候选与剩余项→打开原文→键盘关闭；记录实际视口，验证正常/空/加载/断连错误；不得DOM注入/内部store代替用户输入。
- [ ] README/终端/HTML的DONE与PASS精确计数一致；HTTP读取只读、不泄露未列明文件，路由级symlink越界拒绝；权限不足时明确未验不跳过当通过。
- [ ] 不改03查询/CLI源码。发现接口缺陷退回03并重审受影响候选；UI截图与交互分别留证，不用截图推断交互成功。
- [ ] 必需checks原件、范围核验及待审候选齐备；未将实现者自检冒作独立批准。
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
实际task_id、UTC起止/检查点、候选、命令receipt、可继承产物、remaining_work、dirty归属及命令终态；未知明确UNKNOWN。每次真实终态后attempt，再release/closeout；四预算保持5/10/1/2。

### 7.3 审查与裁决
- 审查：PENDING；Reviewer未分配。
- Ruling：无执行裁决。需要改已验收共享源时退回原owner并重审受影响绑定，不在本卡偷偷扩大范围。
- Deferred Minors：无。
<!-- /iter:ledger -->
