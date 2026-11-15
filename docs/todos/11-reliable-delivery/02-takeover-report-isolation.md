---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "02"
task_name: "隔离旧接管报告的逐卡读取故障"
status: "TODO"
type: "Strict-TDD"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "87.300"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
---

# 02 · 隔离旧接管报告的逐卡读取故障

## 1. 任务执行目标与接口契约
- **主要目标**：旧--takeover-report遇到不可读、编码损坏或读取竞态卡仍输出完整JSON库存，坏卡留错误，健康卡继续审计。
- **Consumes**：discover_task_files(directory); parse_card(content); audit_task_file(path)。沿用旧takeover报告read_only/tasks/next及逐卡path/declared_status/acceptance_verdict/missing/findings字段。
- **Produces**：scripts/iter_cli.py: _takeover_task(path: Path) -> dict；逐卡返回既有行结构，无法确定的missing为null，错误卡UNKNOWN或FAIL且永不PASS。保留iter_sync.main和iter_cli.main(argv)各自退出/异常合同。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 对健康卡混合UnicodeError、OSError及发现后删除构造有效断言RED
- [ ] 实现逐卡故障隔离并保留旧报告结构
- [ ] 完成CLI/发现兼容与只读回归
<!-- /iter:stages -->

## 3. 按类型验证规划
核心行为先取得可编译测试的真实断言RED，再最小GREEN；环境错误不算RED。
<!-- iter:verification -->
- [ ] **red**：python -B -m pytest -p no:cacheprovider tests/test_takeover_resilience.py tests/test_task_discovery_compat.py tests/test_cli_compatibility.py tests/test_sync_compatibility.py -q；由同一实现者先取得验收中具体行为断言失败，环境/导入失败不作RED；通过冻结runner。
- [ ] **green**：python -B -m pytest -p no:cacheprovider tests/test_takeover_resilience.py tests/test_task_discovery_compat.py tests/test_cli_compatibility.py tests/test_sync_compatibility.py -q；同一实现者最小修复后通过，保留原始输出；通过冻结runner。
- [ ] **regression**：python -B -m pytest -p no:cacheprovider tests/test_takeover_resilience.py tests/test_task_discovery_compat.py tests/test_cli_compatibility.py tests/test_sync_compatibility.py -q；覆盖本卡列出的直接接口/兼容范围，影响不明扩大；不代替整轮全量。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `scripts/iter_cli.py` | MODIFIED | 本任务授权范围 |
| `tests/test_takeover_resilience.py` | MODIFIED | 本任务授权范围 |
| `tests/test_task_discovery_compat.py` | MODIFIED | 本任务授权范围 |
| `tests/test_cli_compatibility.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/02-takeover-report-isolation.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/02/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 混合至少一张合法可读卡、一张坏编码卡、一张读取OSError卡；结果仍可解析为单份JSON，库存含所有已发现卡，健康卡结果保留，坏卡携带原因且非PASS。
- [ ] 非法目录/错误参数仍按旧合同失败；不吞掉整轮配置或参数错误，不把坏卡当空库存。
- [ ] 覆盖旧脚本入口与iter_cli.main(argv)；核对目录字节不变。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：无；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/02/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
