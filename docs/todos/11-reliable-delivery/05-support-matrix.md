---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "05"
task_name: "公布带证据的支持矩阵"
status: "TESTING"
type: "Spike-Discovery"
fix_rounds: 1
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "87.225"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: "bfeabf74937e4e36ce04da9082ef312ba572806c"
head_sha: ""
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":1,\"total\":1,\"consilium\":0,\"replan\":0,\"writer\":\"iter11-controller-linux-20261115\",\"events\":{\"iter11-05-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:43:22.258574+00:00\"},\"iter11-05-consumer-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/consumer-attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"evidence-inspection\",\"candidate\":\"bfeabf74937e4e36ce04da9082ef312ba572806c\",\"inputs\":[\"references/support_matrix.md\",\"docs/todos/11-reliable-delivery/evidence/05/consumer-scenario.md\"],\"capabilities\":[\"native-codex-cli\",\"approved-frozen-coordinator\"],\"checkpoint\":\"新会话正确区分Linux实测、Windows历史、Codegworker阻断和FS/Gemini未知\",\"remaining_work\":[\"C独审/D/strict\"],\"executor_id\":\"01a1dd86-9427-7f93-a004-2ce8b0d74ac7\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/05/consumer-terminal.json\",\"progress\":[{\"kind\":\"review-finding\",\"summary\":\"支持边界实际消费及原件核验，无扩大声明\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/support-consumption.json\"}],\"commands\":[],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/11-reliable-delivery/evidence/05/consumer-attempt.json\",\"phase\":\"evidence-inspection\",\"delivery_mode\":\"git\",\"candidate\":\"bfeabf74937e4e36ce04da9082ef312ba572806c\",\"conditions\":{\"inputs\":[\"docs/todos/11-reliable-delivery/evidence/05/consumer-scenario.md\",\"references/support_matrix.md\"],\"capabilities\":[\"approved-frozen-coordinator\",\"native-codex-cli\"],\"scope\":[\".agents/notes/planned/iter11/05-support-matrix.md\",\"docs/todos/11-reliable-delivery/evidence/05/\",\"references/release_status.md\",\"references/support_matrix.md\",\"tests/test_support_matrix.py\"]},\"executor_id\":\"01a1dd86-9427-7f93-a004-2ce8b0d74ac7\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/05/consumer-terminal.json\",\"progress\":[{\"kind\":\"review-finding\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/support-consumption.json\",\"summary\":\"支持边界实际消费及原件核验，无扩大声明\"}],\"checkpoint\":\"新会话正确区分Linux实测、Windows历史、Codegworker阻断和FS/Gemini未知\",\"remaining_work\":[\"C独审/D/strict\"],\"commands\":[],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":null}},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:48:15.723630+00:00\"},\"iter11-05-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"phase\":\"implementation\",\"candidate\":\"bfeabf74937e4e36ce04da9082ef312ba572806c\",\"inputs\":[\"docs/todos/11-reliable-delivery/05-support-matrix.md\",\"docs/todos/11-reliable-delivery/README.md\",\"AGENTS.md\",\"references/task_card_schema.md\",\"references/release_status.md\"],\"capabilities\":[\"native-codex-cli-implementer\",\"approved-frozen-linux-runner\",\"Python3.11.17-pytest9.2-mcp1.30\",\"independent-native-reviewer\"],\"version\":1,\"checkpoint\":\"支持矩阵按证据分层，最终5测试及8链接通过；新只读会话正确识别Linux/Windows/Codeg/FS/Gemini及安装未知边界\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"executor_id\":\"01a1dd84-62f5-7fb2-a5b6-23520a7a04e7\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/05/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"summary\":\"支持矩阵按证据分层，最终5测试及8链接通过；新只读会话正确识别Linux/Windows/Codeg/FS/Gemini及安装未知边界\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/delivery.json\"}],\"commands\":[\"docs/todos/11-reliable-delivery/evidence/05/experiment-01.json\",\"docs/todos/11-reliable-delivery/evidence/05/scenario-links.json\",\"docs/todos/11-reliable-delivery/evidence/05/experiment-final.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/11-reliable-delivery/evidence/05/attempt.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"bfeabf74937e4e36ce04da9082ef312ba572806c\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/05-support-matrix.md\",\"docs/todos/11-reliable-delivery/README.md\",\"references/release_status.md\",\"references/task_card_schema.md\"],\"capabilities\":[\"Python3.11.17-pytest9.2-mcp1.30\",\"approved-frozen-linux-runner\",\"independent-native-reviewer\",\"native-codex-cli-implementer\"],\"scope\":[\".agents/notes/planned/iter11/05-support-matrix.md\",\"docs/todos/11-reliable-delivery/evidence/05/\",\"references/release_status.md\",\"references/support_matrix.md\",\"tests/test_support_matrix.py\"]},\"executor_id\":\"01a1dd84-62f5-7fb2-a5b6-23520a7a04e7\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/05/implementation-terminal.json\",\"progress\":[{\"kind\":\"implementation\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/delivery.json\",\"summary\":\"支持矩阵按证据分层，最终5测试及8链接通过；新只读会话正确识别Linux/Windows/Codeg/FS/Gemini及安装未知边界\"}],\"checkpoint\":\"支持矩阵按证据分层，最终5测试及8链接通过；新只读会话正确识别Linux/Windows/Codeg/FS/Gemini及安装未知边界\",\"remaining_work\":[\"C独审\",\"D/冻结strict\"],\"commands\":[{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/05/experiment-01.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T04:44:10.418170+00:00\",\"ended_at\":\"2026-11-15T04:44:11.030660+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/05/experiment-final.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T04:44:32.386877+00:00\",\"ended_at\":\"2026-11-15T04:44:32.900538+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/05/scenario-links.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T04:44:37.259062+00:00\",\"ended_at\":\"2026-11-15T04:44:37.316571+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":1.18366}},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:49:33.693612+00:00\"},\"iter11-05-release-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/implementation-terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:49:33.764747+00:00\"},\"iter11-05-review-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:49:33.835543+00:00\"},\"iter11-05-review1-attempt-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"build/iter11-review/task05-review1/attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"phase\":\"evidence-inspection\",\"candidate\":\"a08ab82d84e27366d625f8e58bc4fd16acacce20\",\"inputs\":[\"docs/todos/11-reliable-delivery/05-support-matrix.md\",\"docs/todos/11-reliable-delivery/README.md\",\"AGENTS.md\",\"references/task_card_schema.md\",\"references/release_status.md\"],\"capabilities\":[\"native-codex-cli-implementer\",\"approved-frozen-linux-runner\",\"Python3.11.17-pytest9.2-mcp1.30\",\"independent-native-reviewer\"],\"version\":1,\"checkpoint\":\"矩阵质量支持；F1卡内decision缺具体结论/限制/来源/取舍\",\"remaining_work\":[\"主控补decision ledger\",\"受影响复审\",\"D/strict\"],\"executor_id\":\"01a1dd8a-0d20-7f20-aeb8-00fa7a7d381d\",\"terminal_evidence\":\"build/iter11-review/task05-review1/terminal.json\",\"progress\":[{\"kind\":\"review-finding\",\"summary\":\"F1决策账本内容不齐，整体NEEDS_FIX\",\"evidence\":\"build/iter11-review/task05-review1/report.json\"}],\"commands\":[\"build/iter11-review/task05-review1/scope-runner.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"build/iter11-review/task05-review1/attempt.json\",\"phase\":\"evidence-inspection\",\"delivery_mode\":\"git\",\"candidate\":\"a08ab82d84e27366d625f8e58bc4fd16acacce20\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/05-support-matrix.md\",\"docs/todos/11-reliable-delivery/README.md\",\"references/release_status.md\",\"references/task_card_schema.md\"],\"capabilities\":[\"Python3.11.17-pytest9.2-mcp1.30\",\"approved-frozen-linux-runner\",\"independent-native-reviewer\",\"native-codex-cli-implementer\"],\"scope\":[\".agents/notes/planned/iter11/05-support-matrix.md\",\"docs/todos/11-reliable-delivery/evidence/05/\",\"references/release_status.md\",\"references/support_matrix.md\",\"tests/test_support_matrix.py\"]},\"executor_id\":\"01a1dd8a-0d20-7f20-aeb8-00fa7a7d381d\",\"executor_state\":\"completed\",\"terminal_evidence\":\"build/iter11-review/task05-review1/terminal.json\",\"progress\":[{\"kind\":\"review-finding\",\"evidence\":\"build/iter11-review/task05-review1/report.json\",\"summary\":\"F1决策账本内容不齐，整体NEEDS_FIX\"}],\"checkpoint\":\"矩阵质量支持；F1卡内decision缺具体结论/限制/来源/取舍\",\"remaining_work\":[\"D/strict\",\"主控补decision ledger\",\"受影响复审\"],\"commands\":[{\"receipt\":\"build/iter11-review/task05-review1/scope-runner.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T04:49:42.366292+00:00\",\"ended_at\":\"2026-11-15T04:49:42.527496+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":0.161204}},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:52:19.880485+00:00\"},\"iter11-05-fix1-budget-v1\":{\"input\":{\"action\":\"fix\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"F1 Controller decision ledger missing required concrete conclusion, evidence, limitation and tradeoff\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/05/preliminary-review1.json\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":0,\"current_rounds\":1,\"fix_total\":1,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:52:19.948680+00:00\"},\"iter11-05-review1-release-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"build/iter11-review/task05-review1/terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":1,\"current_rounds\":1,\"fix_total\":1,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:52:20.017703+00:00\"},\"iter11-05-review2-claim-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"05-support-matrix\",\"previous_rounds\":1,\"current_rounds\":1,\"fix_total\":1,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T04:52:20.087771+00:00\"}},\"blocked_reason\":\"\"}"
updated_at: "2026-11-15T04:52:20.087910+00:00"
---

# 05 · 公布带证据的支持矩阵

## 1. 任务执行目标与接口契约
- **主要目标**：按能力、平台和宿主公布已验证、未验证及明确不支持范围；仅维护证据支持的声明，不实施跨平台或FS恢复扩展。
- **Consumes**：2026-11-14发布记录、iter_run/checkpoint契约及本次Linux/TypeSafe/Codeg工具可用性观察；其他任务新事实仅在有原件后增补。
- **Produces**：references/support_matrix.md：能力/platform/host/status/observed_at/source_candidate/evidence/limitation；references/release_status.md只链接该矩阵；不重写历史观察为当前事实。

## 2. 业务阶段
<!-- iter:stages -->
- [x] 逐项核对契约与有日期的能力原件
- [x] 生成支持矩阵和发布索引路由
- [x] 执行结构/链接检查并由新会话正确识别未验证项
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [x] **experiment**：python -B -m pytest -p no:cacheprovider tests/test_support_matrix.py tests/test_release_index.py -q；通过冻结runner保留真实退出码，另按本卡验收完成实际消费或实验。
- [x] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [x] **interfaces**：references/support_matrix.md：能力/platform/host/status/observed_at/source_candidate/evidence/limitation；references/release_status.md只链接该矩阵；不重写历史观察为当前事实。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `references/support_matrix.md` | MODIFIED | 本任务授权范围 |
| `references/release_status.md` | MODIFIED | 本任务授权范围 |
| `tests/test_support_matrix.py` | MODIFIED | 本任务授权范围 |
| `.agents/notes/planned/iter11/05-support-matrix.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/05/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 至少分别覆盖查询、Windows正式runner、Linux正式runner、Git批准链、FS本地绑定/正常交接、FS时间中断grant、显式安装根消费、Gemini CLI自动发现及配置注入；每行均有状态、日期、候选、来源和限制。
- [ ] 明确FS正常release/claim可用不等于FS时间中断恢复可用；Linux查询可用不等于正式命令链支持；Antigravity消费Gemini副本不等于Gemini CLI自动发现。
- [ ] 原件不能证明的范围写UNKNOWN/未验证及补齐责任和条件；不因历史493通过扩大版本、平台或宿主声明。
- [ ] 只修改矩阵/路由和其结构检查，不更改runner、恢复协议、部署配置或历史发布事实。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。

2026-11-15T04:49:33.780052+00:00：支持矩阵按证据分层，最终5测试及8链接通过；新只读会话正确识别Linux/Windows/Codeg/FS/Gemini及安装未知边界；原生实现会话01a1dd84-62f5-7fb2-a5b6-23520a7a04e7和命令树已确认终态。原始证据/source manifest/type checks已核对，冻结C后独审，非整轮批准。

2026-11-15 F1决策补记（主控记录，产品文件未变）：采用references/support_matrix.md的有日期/候选/宿主/限制快照，并在references/release_status.md仅追加路由；具体取舍和接口依据见evidence/05/matrix-decision.md及.agents/notes/planned/iter11/05-support-matrix.md。选择逐能力公布证据边界，接受维护原件/build链接在安装白名单副本内可能缺失的成本；不为消除缺链擅自扩展部署清单、平台能力或宣称新安装采用。
实测结论与来源：experiment-final.json及其.output.txt在最终矩阵源码取得5通过；scenario-links.json为8链接无缺失；support-consumption.json、consumer-native.jsonl和consumer-guard.json记录新会话正确区分各项。Linux正式runner只绑定00获批C2 3f949f8及其六文件冻结快照；00/review-report-v2.json核对48e731e的Python3.11.17/pytest9.2/MCP1.30完整基线513通过、2 Windows跳过到C3的源码适用性，这不是本卡全量新实测。
限制：Windows当前UNKNOWN，493只来自2026-11-14发布26652ba（docs/releases/iteration10-20261114/README.md）；03/native-codeg-chain.json保留实际READY后一次工具调用与worker bwrap启动BLOCKED，completed不证明命令成功；FS正常release/claim不能替代不支持的Git中断grant或未知的完整外部业务；显式Antigravity消费不证明Gemini CLI自动发现/注入；Linux符号链接观察不等于历史Windows独立副本或本候选已安装。各缺口的责任与客观补齐条件逐行列于矩阵，未来06—12/部署/外部验收均不在当前结论内。
独审原件preliminary-review1.json对矩阵事实/技术质量已支持，仅F1卡内记录不足；本次只补允许的ledger、预算/审查事件与报告原件，不修改冻结规格/goal或产品/测试/矩阵。原测试证据适用，不重复运行；新候选仍由同一非参与Reviewer定点复审。
<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：无；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/05/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
