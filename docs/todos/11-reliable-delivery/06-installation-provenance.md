---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "06"
task_name: "提供安装来源清单与轻量自检"
status: "IN_PROGRESS"
type: "Strict-TDD"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "91.925"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: "e66841186450dc6bbe138bf77aac87a2a8f1232a"
head_sha: ""
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"\",\"events\":{\"iter11-06-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"06-installation-provenance\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:54:28.398693+00:00\"},\"iter11-06-red-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/06/red-attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"phase\":\"implementation\",\"candidate\":\"e66841186450dc6bbe138bf77aac87a2a8f1232a\",\"inputs\":[\"docs/todos/11-reliable-delivery/06-installation-provenance.md\",\"docs/todos/11-reliable-delivery/README.md\",\"AGENTS.md\",\"references/task_card_schema.md\"],\"capabilities\":[\"native-codex-cli-implementer\",\"approved-frozen-linux-runner\",\"Python3.11.17-pytest9.2-mcp1.30\",\"independent-native-reviewer\"],\"version\":1,\"checkpoint\":\"正常RED检查点22行为断言失败11控制通过，尚无生产实现\",\"remaining_work\":[\"新会话继承RED证据\",\"同实现者生产实现/GREEN/regression/临时安装检查\",\"C独审/D/strict\"],\"executor_id\":\"01a1dd8e-8b72-7b72-90b4-a8577ef8db2d\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/06/implementation-terminal.json\",\"progress\":[{\"kind\":\"red\",\"summary\":\"22断言失败/11通过，无导入环境错误，测试侧无功能adapter\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/06/red-01.json.output.txt\"}],\"commands\":[\"docs/todos/11-reliable-delivery/evidence/06/red-01.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/11-reliable-delivery/evidence/06/red-attempt.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"e66841186450dc6bbe138bf77aac87a2a8f1232a\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/06-installation-provenance.md\",\"docs/todos/11-reliable-delivery/README.md\",\"references/task_card_schema.md\"],\"capabilities\":[\"Python3.11.17-pytest9.2-mcp1.30\",\"approved-frozen-linux-runner\",\"independent-native-reviewer\",\"native-codex-cli-implementer\"],\"scope\":[\".agents/notes/planned/iter11/06-installation-provenance.md\",\"docs/todos/11-reliable-delivery/evidence/06/\",\"references/installation_verification.md\",\"scripts/iter_install.py\",\"tests/test_install_provenance.py\"]},\"executor_id\":\"01a1dd8e-8b72-7b72-90b4-a8577ef8db2d\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/06/implementation-terminal.json\",\"progress\":[{\"kind\":\"red\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/06/red-01.json.output.txt\",\"summary\":\"22断言失败/11通过，无导入环境错误，测试侧无功能adapter\"}],\"checkpoint\":\"正常RED检查点22行为断言失败11控制通过，尚无生产实现\",\"remaining_work\":[\"C独审/D/strict\",\"同实现者生产实现/GREEN/regression/临时安装检查\",\"新会话继承RED证据\"],\"commands\":[{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/06/red-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-15T04:55:02.045633+00:00\",\"ended_at\":\"2026-11-15T04:55:03.527041+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":1.481408}},\"result\":{\"task_id\":\"06-installation-provenance\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:57:04.584438+00:00\"},\"iter11-06-red-release-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/06/implementation-terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"06-installation-provenance\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:57:04.675084+00:00\"}},\"blocked_reason\":\"\"}"
updated_at: "2026-11-15T04:57:04.675201+00:00"
---

# 06 · 提供安装来源清单与轻量自检

## 1. 任务执行目标与接口契约
- **主要目标**：独立副本可用显式来源清单检查来源提交、交付文件漂移及当前能力；分别定义安装烟测和维护全量测试，不引入打包平台或实际部署。
- **Consumes**：现有交付白名单SKILL.md/scripts/references/templates/tests/.agents/notes；真实Git提交和已提交路径；当前发布支持边界。05支持矩阵是后续交叉核对输入，不是阻塞本卡的硬依赖。
- **Produces**：scripts/iter_install.py: build_install_manifest(source_root: Path, source_commit: str) -> dict；check_installation(installation_root: Path, manifest: dict) -> dict；main(argv=None) -> int。CLI --make-manifest --root ROOT --source-commit SHA 输出JSON；--check --root ROOT --manifest PATH 只读检查，0一致、2输入/漂移/未知来源。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 对来源不符、坏清单、漂移/缺失/越界路径取得断言RED
- [ ] 生成和只读检查来源清单GREEN
- [ ] 在白名单临时安装做烟测，记录能力边界和待审候选
<!-- /iter:stages -->

## 3. 按类型验证规划
核心行为先取得可编译测试的真实断言RED，再最小GREEN；环境错误不算RED。
<!-- iter:verification -->
- [ ] **red**：python -B -m pytest -p no:cacheprovider tests/test_install_provenance.py tests/test_cli_compatibility.py -q；由同一实现者先取得验收中具体行为断言失败，环境/导入失败不作RED；通过冻结runner。
- [ ] **green**：python -B -m pytest -p no:cacheprovider tests/test_install_provenance.py tests/test_cli_compatibility.py -q；同一实现者最小修复后通过，保留原始输出；通过冻结runner。
- [ ] **regression**：python -B -m pytest -p no:cacheprovider tests/test_install_provenance.py tests/test_cli_compatibility.py -q；覆盖本卡列出的直接接口/兼容范围，影响不明扩大；不代替整轮全量。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `scripts/iter_install.py` | MODIFIED | 本任务授权范围 |
| `references/installation_verification.md` | MODIFIED | 本任务授权范围 |
| `tests/test_install_provenance.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/06-installation-provenance.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/06/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 清单version=1、source_commit为实际完整可解析Git提交，files含精确相对path与sha256；生成前验证源文件与该提交相符，dirty源码/未知键/重复或越界路径拒绝，不凭提交标签证明来源。
- [ ] check拒绝损坏、缺失、字节漂移、符号链接越界；不读取白名单外内容，不修复/覆盖安装，不运行维护全套或产生批准。
- [ ] 输出来源和文件一致性与运行时能力分别列示；Linux正式runner不可用不会被标成READY，query可用也不代表整条执行链可用。
- [ ] 来源清单默认stdout，落盘及随副本分发在另获授权的部署阶段执行；本轮只在隔离临时目录验证，不扩大既有部署白名单或覆盖真实安装。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。

2026-11-15正常RED检查点：原生实现者01a1dd8e-8b72-7b72-90b4-a8577ef8db2d仅测试22个真实行为断言失败、11控制通过，见evidence/06/red-checkpoint.json、red-01.json/output及原生记录；生产iter_install.py不存在。guard先消费本次终态READY才启动，原生会话与测试进程树已终态，attempt后正常release，预算0/0且非FUSED，不需中断grant。接续新会话须沿用同字节RED/原始时间，不重跑；实现/GREEN/regression/临时安装、独审及C/D/strict均待完成。
<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：无；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/06/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
