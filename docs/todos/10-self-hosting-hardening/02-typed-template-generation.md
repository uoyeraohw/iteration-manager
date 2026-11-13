---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "02"
task_name: "按类型与交付模式生成和检查任务卡"
status: "TODO"
type: "Strict-TDD"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "91.025"
typesafe_evidence: "docs/todos/10-self-hosting-hardening/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
created_at: "2026-11-13"
updated_at: "2026-11-13"
---

# 02 · 按类型与交付模式生成和检查任务卡

> 声明 TODO；验收 UNKNOWN；尚无执行、RED/GREEN或独立批准。本文是已初始化计划，不授予实施、Git提交或部署权限。

## 1. 任务执行目标与接口契约

- **主要目标**：新增不依赖模型替换段落的任务卡生成/检查入口，覆盖现有四type×Git/FS八种组合，不改变既有收据与旧卡契约。
- **前置任务**：[01](./01-authority-consistency.md) 验收PASS
- **Consumes**：iter_contracts.parse_card(content)、TYPE_CHECKS、contract_projection(content)；iter_filesystem现有冻结规则；任务01授权矩阵。旧schema_version=1，四type不改名。
- **Produces**：scripts/iter_templates.py: render_task_card(spec: dict) -> str；validate_generated_card(content: str, delivery_mode: str) -> list[str]；独立CLI `--render <spec.json>` stdout输出Markdown，`--check <card.md> --delivery-mode git|filesystem` stdout输出JSON {valid,errors}，合法退出0、输入/结构错误退出2。默认不写文件，不集成第二套状态账。
- **唯一责任**：本卡主管持有卡片写权；一个实现owner负责白名单源文件及返修。读取相邻模块不获得修改权。初始owner未分配，不捏造会话ID。
- **共同约定**：完整阅读[迭代目标与执行约定](README.md)，继承冻结协调器、授权、独审及恢复规则。

## 2. 业务阶段与检查点

<!-- iter:stages -->
- [ ] Stage 1/3：为可调用入口与八种组合建立可编译行为断言RED
- [ ] Stage 2/3：最小实现纯渲染/预检与八组合GREEN，保留未知和占位输入拒绝
- [ ] Stage 3/3：完成旧解析/FS冻结兼容、文档与独立审查
<!-- /iter:stages -->

阶段可跨会话；正常检查点保存证据并release，不以超时强杀充当切片。比例是清单比例，不是工时。

## 3. 按类型验证规划

<!-- iter:verification -->
- [ ] 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。
- [ ] 先建立可导入、可调用的最小入口使行为断言RED（例如返回空正文被断言拒绝）；ImportError、缺函数或语法错误不计RED。核心行为RED→最小GREEN，补充边界如实标注。
- [ ] 完成必需checks：red（非零且assertion）、green（0）、regression（0）；所有原始输出、命令cwd、真实退出码和候选引用可追溯。
- [ ] 完成范围自检、冻结候选和待审输入；独立APPROVED后登记收据、DONE及D，再消费本地strict。
<!-- /iter:verification -->

### 可执行命令与证据

从精确Worktree根运行；`COORDINATOR_ROOT`为README指定冻结版本，`COMMAND_DEADLINE_UTC`与每次唯一receipt由实际派发者即时填写，不提前伪造：

```powershell
python "$env:COORDINATOR_ROOT/scripts/iter_run.py" --deadline "$env:COMMAND_DEADLINE_UTC" --evidence "docs/todos/10-self-hosting-hardening/evidence/02/regression-<唯一attempt>.json" -- python -B -m pytest -p no:cacheprovider tests/test_template_generation.py tests/test_prompt_sources.py tests/test_task_card_schema.py tests/test_filesystem_receipts.py tests/test_filesystem_r7_repairs.py -q
$code = $LASTEXITCODE; exit $code
```

- 上述新增测试文件由本卡在授权实施后创建，初始化时不存在不算失败或RED；不得直接运行不存在文件后声称有效RED。
- 内环选本卡具体测试节点；任务交付运行上述受影响集合。首次有效断言RED及GREEN分别使用独立receipt。原始输出与正式收据放本卡evidence目录。
- 总回归由任务06/整轮收口对实际最终候选运行，不以局部通过代替。
- Git范围命令：`python "$env:COORDINATOR_ROOT/scripts/iter_sync.py" --check-scope <实际BASE> <实际C> docs/todos/10-self-hosting-hardening/02-typed-template-generation.md --include-worktree`。
- scope/独审/strict所用候选必须相同。真实命令通过runner留证；只读协调CLI、claim/release/attempt及精准Git登记按共同协议豁免包装。
- 声明的输出路径是未来产物位置，不是已有证据；不预先写入review_receipt或SHA。

## 4. 实施边界

保留现有CLI/旧卡/收据合同，不迁移历史、不部署副本、不清理已有目录。遇到已证实的冻结工具缺陷，记录具体影响并停止受影响门禁，交授权持有人裁决；不切换检查器绕过，也不降低本卡验收。非本卡必要的新发现只作建议。

## 5. 新增或变更内容清单

<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `scripts/iter_templates.py` | CREATED | 按类型与交付模式生成和检查任务卡 |
| `templates/task_detail.md` | MODIFIED | 按类型与交付模式生成和检查任务卡 |
| `templates/contracts/strict_tdd_contract.md` | MODIFIED | 按类型与交付模式生成和检查任务卡 |
| `templates/contracts/ui_component_contract.md` | MODIFIED | 按类型与交付模式生成和检查任务卡 |
| `templates/contracts/refactor_benchmark_contract.md` | MODIFIED | 按类型与交付模式生成和检查任务卡 |
| `templates/contracts/spike_discovery_contract.md` | MODIFIED | 按类型与交付模式生成和检查任务卡 |
| `references/template_generation.md` | CREATED | 按类型与交付模式生成和检查任务卡 |
| `tests/test_template_generation.py` | CREATED | 本卡验证与兼容检查 |
| `.agents/notes/implemented/process/2026-11-13-typed-template-generation.md` | CREATED | 本卡决定与验证记录 |
| `docs/todos/10-self-hosting-hardening/evidence/02/` | CREATED | 原始命令、观测、attempt、独审报告及JSON收据 |
<!-- /iter:scope -->

任务卡和所属迭代README按现有规则隐式允许，仅主管串行登记。其它卡、其它任务源码、根总控和安装副本不在写范围。正式证据只在本卡目录追加唯一文件，不覆写；隔离夹具使用该目录下sandbox/或系统临时目录，不修改真实业务数据。

## 6. 确定性验收标准

<!-- iter:acceptance -->
- [ ] spec必需version=1, task_id, iteration, task_name, type, delivery_mode, objective, consumes, produces, scope, stages, acceptance, verification；FS另需candidate_id。字符串非空，scope为项目相对文件/目录数组，stages/acceptance为非空文本数组，verification为该type必需check名到实际命令或观测说明的映射；未知字段/类型/版本拒绝。
- [ ] 输出初态TODO、PENDING、tdd_verified=false、typesafe_score=UNASSESSED；模板生成不等于TypeSafe通过，不生成虚假SHA或APPROVED。
- [ ] 八组合均能由现有parse_card识别；非TDD无强制RED/TRUE；FS不含非空SHA、不复制审查后需修改的动态正文，冻结前定稿规则明确。
- [ ] 拒绝空scope、越界路径、缺关键验收与未替换占位符；CLI不覆盖现有文件、不迁移旧卡。
- [ ] Refactor-Benchmark保持现有before/after门禁；纯结构重构未来契约拆分只记录讨论结论，不在本轮新增type或放宽旧门禁。
- [ ] 必需checks原件、范围核验及待审候选齐备；未将实现者自检冒作独立批准。
<!-- /iter:acceptance -->

独审与登记为上述待审条件之后的完成门禁；未发生前不预勾选。独立Reviewer不得是本卡测试/实现/设计/RCA参与者。

## 7. 执行实证与裁决账本

<!-- iter:ledger -->
### 7.1 初始化事实
- 源码观察基线：`46ded3a4696e3bdb531d06951fce7982fa9db1cd`；实际执行BASE/C/D尚未产生。
- 规划质检：91.025/100；各维及原始请求/响应见[规划证据](evidence/planning/typesafe-summary.json)。该分数不是执行批准。
- 当前状态：未派发、无活动实现命令；未取得RED/GREEN/观测/独立审查。
- 本卡预计收据位置：`docs/todos/10-self-hosting-hardening/evidence/02/review.json`，实际产生后才登记frontmatter。

### 7.2 执行时填写
实际task_id、UTC起止/检查点、候选、命令receipt、可继承产物、remaining_work、dirty归属及命令终态；未知明确UNKNOWN。每次真实终态后attempt，再release/closeout；四预算保持5/10/1/2。

### 7.3 审查与裁决
- 审查：PENDING；Reviewer未分配。
- Ruling：无执行裁决。需要改已验收共享源时退回原owner并重审受影响绑定，不在本卡偷偷扩大范围。
- Deferred Minors：无。
<!-- /iter:ledger -->
