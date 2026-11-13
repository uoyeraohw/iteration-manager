---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "03"
task_name: "稳定查询与CLI消费接口，保持旧入口兼容"
status: "TODO"
type: "Strict-TDD"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "92.150"
typesafe_evidence: "docs/todos/10-self-hosting-hardening/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
created_at: "2026-11-13"
updated_at: "2026-11-13"
---

# 03 · 稳定查询与CLI消费接口，保持旧入口兼容

> 声明 TODO；验收 UNKNOWN；尚无执行、RED/GREEN或独立批准。本文是已初始化计划，不授予实施、Git提交或部署权限。

## 1. 任务执行目标与接口契约

- **主要目标**：集中提供一致的任务查询与交接数据，CLI只适配命令；完成所需模块整理但不改HTML交互。为后继看板提供Git/FS候选与execution字段，旧接口可继续调用。
- **前置任务**：[02](./02-typed-template-generation.md) 验收PASS
- **Consumes**：现有audit_task_file(file_path)、discover_task_files(directory,read_root=None)、render_task_envelope(task_file,repo_dir)、generate_board_data(iter_dir)接口与TASK_HANDOFF；任务02生成样例，任务01授权边界。
- **Produces**：iter_queries提供discover_task_files(directory: Path, read_root: Path | None = None) -> list[Path]、audit_task_file(file_path: Path) -> dict、render_task_envelope(task_file: Path, repo_dir: Path) -> dict；iter_cli.main(argv: list[str] | None = None) -> int。iter_sync保留旧导入符号与main()，原generate_board_data(iter_dir: Path) -> dict仍由iter_sync导出，其cards仅追加delivery_mode,candidate_id,execution（checkpoint,remaining_work），和envelope调用同一查询结果。未知值保持UNKNOWN/null，不删除旧键。
- **唯一责任**：本卡主管持有卡片写权；一个实现owner负责白名单源文件及返修。读取相邻模块不获得修改权。初始owner未分配，不捏造会话ID。
- **共同约定**：完整阅读[迭代目标与执行约定](README.md)，继承冻结协调器、授权、独审及恢复规则。

## 2. 业务阶段与检查点

<!-- iter:stages -->
- [ ] Stage 1/3：冻结兼容矩阵，对缺失的统一投影字段取得有效断言RED
- [ ] Stage 2/3：实现共享查询接口与CLI适配，iter_sync保留兼容门面，不修改HTML
- [ ] Stage 3/3：通过导入/CLI/收据/只读回归并完成前后量测，冻结供看板消费的JSON接口
<!-- /iter:stages -->

阶段可跨会话；正常检查点保存证据并release，不以超时强杀充当切片。比例是清单比例，不是工时。

## 3. 按类型验证规划

<!-- iter:verification -->
- [ ] 读取真实基线、当前变更和前置PASS；完成context、claim与同owner dispatch-check。
- [ ] Strict-TDD：当前旧入口上的新增数据字段/同源关系先真实断言RED→GREEN；regression保留全部旧CLI与导入。另记录baseline、compatibility、benchmark_before、benchmark_after以覆盖结构整理，不要求性能提升。
- [ ] 完成必需checks：red（非零且assertion）、green（0）、regression（0）；所有原始输出、命令cwd、真实退出码和候选引用可追溯。
- [ ] 完成范围自检、冻结候选和待审输入；独立APPROVED后登记收据、DONE及D，再消费本地strict。
<!-- /iter:verification -->

### 可执行命令与证据

从精确Worktree根运行；`COORDINATOR_ROOT`为README指定冻结版本，`COMMAND_DEADLINE_UTC`与每次唯一receipt由实际派发者即时填写，不提前伪造：

```powershell
python "$env:COORDINATOR_ROOT/scripts/iter_run.py" --deadline "$env:COMMAND_DEADLINE_UTC" --evidence "docs/todos/10-self-hosting-hardening/evidence/03/regression-<唯一attempt>.json" -- python -B -m pytest -p no:cacheprovider tests/test_query_contract.py tests/test_cli_compatibility.py tests/test_sync_compatibility.py tests/test_completion_gates.py tests/test_execution_readiness.py tests/test_execution_report.py tests/test_filesystem_delivery_controller.py tests/test_worktree_concurrency.py -q
$code = $LASTEXITCODE; exit $code
```

- 上述新增测试文件由本卡在授权实施后创建，初始化时不存在不算失败或RED；不得直接运行不存在文件后声称有效RED。
- 内环选本卡具体测试节点；任务交付运行上述受影响集合。首次有效断言RED及GREEN分别使用独立receipt。原始输出与正式收据放本卡evidence目录。
- 总回归由任务06/整轮收口对实际最终候选运行，不以局部通过代替。
- Git范围命令：`python "$env:COORDINATOR_ROOT/scripts/iter_sync.py" --check-scope <实际BASE> <实际C> docs/todos/10-self-hosting-hardening/03-query-cli-contract.md --include-worktree`。
- scope/独审/strict所用候选必须相同。真实命令通过runner留证；只读协调CLI、claim/release/attempt及精准Git登记按共同协议豁免包装。
- 声明的输出路径是未来产物位置，不是已有证据；不预先写入review_receipt或SHA。

## 4. 实施边界

保留现有CLI/旧卡/收据合同，不迁移历史、不部署副本、不清理已有目录。遇到已证实的冻结工具缺陷，记录具体影响并停止受影响门禁，交授权持有人裁决；不切换检查器绕过，也不降低本卡验收。非本卡必要的新发现只作建议。

## 5. 新增或变更内容清单

<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `scripts/iter_sync.py` | MODIFIED | 稳定查询与CLI消费接口，保持旧入口兼容 |
| `scripts/iter_queries.py` | CREATED | 稳定查询与CLI消费接口，保持旧入口兼容 |
| `scripts/iter_cli.py` | CREATED | 稳定查询与CLI消费接口，保持旧入口兼容 |
| `scripts/iter_inventory.py` | MODIFIED | 稳定查询与CLI消费接口，保持旧入口兼容 |
| `scripts/iter_preflight.py` | MODIFIED | 稳定查询与CLI消费接口，保持旧入口兼容 |
| `scripts/iter_execution.py` | MODIFIED | 稳定查询与CLI消费接口，保持旧入口兼容 |
| `tests/test_sync_compatibility.py` | MODIFIED | 本卡验证与兼容检查 |
| `tests/test_cli_compatibility.py` | CREATED | 本卡验证与兼容检查 |
| `tests/test_query_contract.py` | CREATED | 本卡验证与兼容检查 |
| `.agents/notes/implemented/architecture/2026-11-13-query-cli-contract.md` | CREATED | 本卡决定与验证记录 |
| `docs/todos/10-self-hosting-hardening/evidence/03/` | CREATED | 原始命令、观测、attempt、独审报告及JSON收据 |
<!-- /iter:scope -->

任务卡和所属迭代README按现有规则隐式允许，仅主管串行登记。其它卡、其它任务源码、根总控和安装副本不在写范围。正式证据只在本卡目录追加唯一文件，不覆写；隔离夹具使用该目录下sandbox/或系统临时目录，不修改真实业务数据。

## 6. 确定性验收标准

<!-- iter:acceptance -->
- [ ] 新增字段的行为测试先在当前可调用generate_board_data上断言RED；不得以新模块ImportError作RED。相同卡envelope与board的交付模式/候选/检查点/剩余工作值一致，旧键与旧默认保持。
- [ ] 旧CLI参数组合与位置参数、phase默认implementation、旧0/1/2/3退出码和未知选项无写入保持；不修改runner124/125语义；帮助覆盖timing命令。
- [ ] 保留iter_sync现有被导入函数/类的签名和行为；新查询模块不导入CLI或iter_sync；inventory/preflight/execution通过查询层读取，测试证明不存在反向依赖；仅在main调用时加载CLI。
- [ ] generate_board_data仍可通过旧入口调用，HTML/HTTP渲染留在iter_sync且本卡不改模板；卡片缺收据、非法profile、候选漂移、预算、只读及同次审计复用均不放宽。
- [ ] 按10/100卡固定样例，记录同环境前后至少3次原始耗时及Git调用次数；禁止新加跨调用缓存，不把合成测量叫真实工时，测量只评价改动影响不要求虚构性能提升。
- [ ] 仅当前白名单源码可写；后继看板任务只消费本接口，不再修改这些源码，接口缺陷返还本owner并按合同重审。
- [ ] 必需checks原件、范围核验及待审候选齐备；未将实现者自检冒作独立批准。
<!-- /iter:acceptance -->

独审与登记为上述待审条件之后的完成门禁；未发生前不预勾选。独立Reviewer不得是本卡测试/实现/设计/RCA参与者。

## 7. 执行实证与裁决账本

<!-- iter:ledger -->
### 7.1 初始化事实
- 源码观察基线：`46ded3a4696e3bdb531d06951fce7982fa9db1cd`；实际执行BASE/C/D尚未产生。
- 规划质检：92.150/100；各维及原始请求/响应见[规划证据](evidence/planning/typesafe-summary.json)。该分数不是执行批准。
- 当前状态：未派发、无活动实现命令；未取得RED/GREEN/观测/独立审查。
- 本卡预计收据位置：`docs/todos/10-self-hosting-hardening/evidence/03/review.json`，实际产生后才登记frontmatter。

### 7.2 执行时填写
实际task_id、UTC起止/检查点、候选、命令receipt、可继承产物、remaining_work、dirty归属及命令终态；未知明确UNKNOWN。每次真实终态后attempt，再release/closeout；四预算保持5/10/1/2。

### 7.3 审查与裁决
- 审查：PENDING；Reviewer未分配。
- Ruling：无执行裁决。需要改已验收共享源时退回原owner并重审受影响绑定，不在本卡偷偷扩大范围。
- Deferred Minors：无。
<!-- /iter:ledger -->
