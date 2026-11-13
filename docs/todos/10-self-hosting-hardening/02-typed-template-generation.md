---
schema_version: 1
iteration: "10-self-hosting-hardening"
task_id: "02"
task_name: "按类型与交付模式生成和检查任务卡"
status: "IN_PROGRESS"
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
updated_at: "2026-11-13T17:13:58.289549+00:00"
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"root/iter10/controller\",\"events\":{\"iter10-02-claim-a\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:46:07.488709+00:00\"},\"iter10-02-attempt-a\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/attempt-a.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"implementation\",\"candidate\":\"f5583e542a20e00cfe9e3eae3776f32cbe9d7ae9\",\"inputs\":[\"docs/todos/10-self-hosting-hardening/02-typed-template-generation.md\",\"templates/task_detail.md\",\"scripts/iter_contracts.py\",\"scripts/iter_filesystem.py\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"checkpoint\":\"真实19项断言RED后八组合核心19项GREEN，CLI/边界/FS冻结/回归/文档待续\",\"remaining_work\":[\"CLI断言RED/GREEN\",\"输入/预检边界\",\"FS冻结兼容\",\"文档及指定回归\",\"独审/登记\"],\"executor_id\":\"5638876b-7be3-4bc9-a2da-af32c4941033\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/native-terminal-a.json\",\"progress\":[{\"kind\":\"red\",\"summary\":\"可导入可调用stub，19项行为断言失败，非导入环境失败\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-red.json.output.txt\"},{\"kind\":\"green\",\"summary\":\"八组合核心路径与基本预检19passed；初次GREEN误判HTML标记的失败原样保留\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-green-2.json.output.txt\"}],\"commands\":[\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-red.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-green.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-green-2.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-note-tree.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-note-format.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/10-self-hosting-hardening/evidence/02/attempt-a.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"f5583e542a20e00cfe9e3eae3776f32cbe9d7ae9\",\"conditions\":{\"inputs\":[\"docs/todos/10-self-hosting-hardening/02-typed-template-generation.md\",\"scripts/iter_contracts.py\",\"scripts/iter_filesystem.py\",\"templates/task_detail.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"scope\":[\".agents/notes/implemented/process/2026-11-13-typed-template-generation.md\",\"docs/todos/10-self-hosting-hardening/evidence/02/\",\"references/template_generation.md\",\"scripts/iter_templates.py\",\"templates/contracts/refactor_benchmark_contract.md\",\"templates/contracts/spike_discovery_contract.md\",\"templates/contracts/strict_tdd_contract.md\",\"templates/contracts/ui_component_contract.md\",\"templates/task_detail.md\",\"tests/test_template_generation.py\"]},\"executor_id\":\"5638876b-7be3-4bc9-a2da-af32c4941033\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/native-terminal-a.json\",\"progress\":[{\"kind\":\"red\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-red.json.output.txt\",\"summary\":\"可导入可调用stub，19项行为断言失败，非导入环境失败\"},{\"kind\":\"green\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-green-2.json.output.txt\",\"summary\":\"八组合核心路径与基本预检19passed；初次GREEN误判HTML标记的失败原样保留\"}],\"checkpoint\":\"真实19项断言RED后八组合核心19项GREEN，CLI/边界/FS冻结/回归/文档待续\",\"remaining_work\":[\"CLI断言RED/GREEN\",\"FS冻结兼容\",\"文档及指定回归\",\"独审/登记\",\"输入/预检边界\"],\"commands\":[{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-green-2.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:49:49.182544+00:00\",\"ended_at\":\"2026-11-13T16:49:51.948302+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-green.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-13T16:49:15.142841+00:00\",\"ended_at\":\"2026-11-13T16:49:18.796627+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-core-red.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-13T16:48:18.972629+00:00\",\"ended_at\":\"2026-11-13T16:48:22.880785+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-note-format.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:50:20.754715+00:00\",\"ended_at\":\"2026-11-13T16:50:23.179354+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-a-note-tree.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:50:17.054497+00:00\",\"ended_at\":\"2026-11-13T16:50:19.631724+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":15.329566}},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:54:03.083165+00:00\"},\"iter10-02-release-a\":{\"input\":{\"action\":\"release\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/native-terminal-a.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:54:03.412214+00:00\"},\"iter10-02-claim-b\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T16:54:04.844259+00:00\"},\"iter10-02-attempt-b\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/attempt-b.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"implementation\",\"candidate\":\"24a483eb7b0694ce67a5e6c0b50adb0d1cb5c160\",\"inputs\":[\"docs/todos/10-self-hosting-hardening/02-typed-template-generation.md\",\"templates/task_detail.md\",\"scripts/iter_contracts.py\",\"scripts/iter_filesystem.py\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"checkpoint\":\"CLI与边界先真实断言RED后GREEN；81项含四FS绑定兼容、111项指定回归、模板及笔记已交付\",\"remaining_work\":[\"独立审查\",\"登记D/strict\"],\"executor_id\":\"72db3dfe-466c-424e-bb74-6511fd23e455\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/native-terminal-b.json\",\"progress\":[{\"kind\":\"red\",\"summary\":\"可执行CLI输出缺失等17行为断言失败，不是导入失败\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-cli-boundary-red.json.output.txt\"},{\"kind\":\"green\",\"summary\":\"74项CLI/边界GREEN、81项兼容与111项指定交付回归\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-regression.json.output.txt\"}],\"commands\":[\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-cli-boundary-red.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-cli-boundary-green.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-compatibility.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-regression.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-note-tree.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-note-format.json\",\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-scope.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/10-self-hosting-hardening/evidence/02/attempt-b.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"24a483eb7b0694ce67a5e6c0b50adb0d1cb5c160\",\"conditions\":{\"inputs\":[\"docs/todos/10-self-hosting-hardening/02-typed-template-generation.md\",\"scripts/iter_contracts.py\",\"scripts/iter_filesystem.py\",\"templates/task_detail.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"scope\":[\".agents/notes/implemented/process/2026-11-13-typed-template-generation.md\",\"docs/todos/10-self-hosting-hardening/evidence/02/\",\"references/template_generation.md\",\"scripts/iter_templates.py\",\"templates/contracts/refactor_benchmark_contract.md\",\"templates/contracts/spike_discovery_contract.md\",\"templates/contracts/strict_tdd_contract.md\",\"templates/contracts/ui_component_contract.md\",\"templates/task_detail.md\",\"tests/test_template_generation.py\"]},\"executor_id\":\"72db3dfe-466c-424e-bb74-6511fd23e455\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/native-terminal-b.json\",\"progress\":[{\"kind\":\"red\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-cli-boundary-red.json.output.txt\",\"summary\":\"可执行CLI输出缺失等17行为断言失败，不是导入失败\"},{\"kind\":\"green\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-regression.json.output.txt\",\"summary\":\"74项CLI/边界GREEN、81项兼容与111项指定交付回归\"}],\"checkpoint\":\"CLI与边界先真实断言RED后GREEN；81项含四FS绑定兼容、111项指定回归、模板及笔记已交付\",\"remaining_work\":[\"独立审查\",\"登记D/strict\"],\"commands\":[{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-cli-boundary-green.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:56:58.804424+00:00\",\"ended_at\":\"2026-11-13T16:57:05.069757+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-cli-boundary-red.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-13T16:56:10.979696+00:00\",\"ended_at\":\"2026-11-13T16:56:24.774354+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-compatibility.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:57:29.008247+00:00\",\"ended_at\":\"2026-11-13T16:57:36.018789+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-note-format.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:58:48.629197+00:00\",\"ended_at\":\"2026-11-13T16:58:51.117739+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-note-tree.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:58:44.501096+00:00\",\"ended_at\":\"2026-11-13T16:58:47.537522+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-regression.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:58:23.199537+00:00\",\"ended_at\":\"2026-11-13T16:58:34.702922+00:00\"},{\"receipt\":\"docs/todos/10-self-hosting-hardening/evidence/02/slice-b-scope.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T16:59:11.457657+00:00\",\"ended_at\":\"2026-11-13T16:59:12.350717+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":44.991946}},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T17:02:53.787150+00:00\"},\"iter10-02-release-b\":{\"input\":{\"action\":\"release\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/native-terminal-b.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"IN_PROGRESS\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-13T17:02:54.126104+00:00\"},\"iter10-02-claim-review\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T17:02:55.512138+00:00\"},\"iter10-02-release-review-initial\":{\"input\":{\"action\":\"release\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/review-initial-rejected.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-13T17:13:40.807406+00:00\"},\"iter10-02-claim-repair\":{\"input\":{\"action\":\"claim\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T17:13:57.856282+00:00\"},\"iter10-02-review-initial\":{\"input\":{\"action\":\"attempt\",\"owner\":\"root/iter10/controller\",\"reason\":\"\",\"evidence\":\"build/review-02/attempt-initial.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"evidence-inspection\",\"candidate\":\"685ee752e1291c5652f3d7cf304dee6cb8842e43\",\"inputs\":[\"docs/todos/10-self-hosting-hardening/02-typed-template-generation.md\",\"templates/task_detail.md\",\"scripts/iter_contracts.py\",\"scripts/iter_filesystem.py\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"checkpoint\":\"独审发现F01：合法非空前导空白误拒，Scope通过，必须返修\",\"remaining_work\":[\"修复F01有效RED/GREEN\",\"受影响回归\",\"新候选独审\",\"登记strict\"],\"executor_id\":\"e1327c5c-738e-4e68-ad55-b7807837c24b\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/review-initial-rejected.json\",\"progress\":[{\"kind\":\"review-finding\",\"summary\":\"实际CLI exit2与三字段断言反例，CHANGES_REQUESTED\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/review-initial-rejected.json\"}],\"commands\":[\"build/review-02/boundary-probe-0110.json\",\"build/review-02/cli-probe-0110.json\",\"build/review-02/independent-path-0109.json\",\"build/review-02/scope-0108.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"build/review-02/attempt-initial.json\",\"phase\":\"evidence-inspection\",\"delivery_mode\":\"git\",\"candidate\":\"685ee752e1291c5652f3d7cf304dee6cb8842e43\",\"conditions\":{\"inputs\":[\"docs/todos/10-self-hosting-hardening/02-typed-template-generation.md\",\"scripts/iter_contracts.py\",\"scripts/iter_filesystem.py\",\"templates/task_detail.md\"],\"capabilities\":[\"Codeg MCP codex independent session\",\"Windows iter_run\",\"pytest\"],\"scope\":[\".agents/notes/implemented/process/2026-11-13-typed-template-generation.md\",\"docs/todos/10-self-hosting-hardening/evidence/02/\",\"references/template_generation.md\",\"scripts/iter_templates.py\",\"templates/contracts/refactor_benchmark_contract.md\",\"templates/contracts/spike_discovery_contract.md\",\"templates/contracts/strict_tdd_contract.md\",\"templates/contracts/ui_component_contract.md\",\"templates/task_detail.md\",\"tests/test_template_generation.py\"]},\"executor_id\":\"e1327c5c-738e-4e68-ad55-b7807837c24b\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/review-initial-rejected.json\",\"progress\":[{\"kind\":\"review-finding\",\"evidence\":\"docs/todos/10-self-hosting-hardening/evidence/02/review-initial-rejected.json\",\"summary\":\"实际CLI exit2与三字段断言反例，CHANGES_REQUESTED\"}],\"checkpoint\":\"独审发现F01：合法非空前导空白误拒，Scope通过，必须返修\",\"remaining_work\":[\"修复F01有效RED/GREEN\",\"受影响回归\",\"新候选独审\",\"登记strict\"],\"commands\":[{\"receipt\":\"build/review-02/boundary-probe-0110.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-13T17:08:59.296544+00:00\",\"ended_at\":\"2026-11-13T17:09:02.819187+00:00\"},{\"receipt\":\"build/review-02/cli-probe-0110.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":1,\"started_at\":\"2026-11-13T17:09:44.364998+00:00\",\"ended_at\":\"2026-11-13T17:09:48.061570+00:00\"},{\"receipt\":\"build/review-02/independent-path-0109.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T17:08:42.878819+00:00\",\"ended_at\":\"2026-11-13T17:08:46.316956+00:00\"},{\"receipt\":\"build/review-02/scope-0108.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-13T17:07:22.696666+00:00\",\"ended_at\":\"2026-11-13T17:07:23.603183+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":11.563869}},\"result\":{\"task_id\":\"02-typed-template-generation\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"root/iter10/controller\",\"consilium_bundle\":null},\"at\":\"2026-11-13T17:13:58.289549+00:00\"}},\"blocked_reason\":\"\"}"
---

# 02 · 按类型与交付模式生成和检查任务卡

> **当前状态**：IN_PROGRESS；验收FAIL；独审发现F01，返实现owner修复，未放行后继。

## 1. 任务执行目标与接口契约

- **主要目标**：新增不依赖模型替换段落的任务卡生成/检查入口，覆盖现有四type×Git/FS八种组合，不改变既有收据与旧卡契约。
- **前置任务**：[01](./01-authority-consistency.md) 验收PASS
- **Consumes**：iter_contracts.parse_card(content)、TYPE_CHECKS、contract_projection(content)；iter_filesystem现有冻结规则；任务01授权矩阵。旧schema_version=1，四type不改名。
- **Produces**：scripts/iter_templates.py: render_task_card(spec: dict) -> str；validate_generated_card(content: str, delivery_mode: str) -> list[str]；独立CLI `--render <spec.json>` stdout输出Markdown，`--check <card.md> --delivery-mode git|filesystem` stdout输出JSON {valid,errors}，合法退出0、输入/结构错误退出2。默认不写文件，不集成第二套状态账。
- **唯一责任**：本卡主管持有卡片写权；一个实现owner负责白名单源文件及返修。读取相邻模块不获得修改权。初始owner未分配，不捏造会话ID。
- **共同约定**：完整阅读[迭代目标与执行约定](README.md)，继承冻结协调器、授权、独审及恢复规则。

## 2. 业务阶段与检查点

<!-- iter:stages -->
- [x] Stage 1/3：为可调用入口与八种组合建立可编译行为断言RED
- [x] Stage 2/3：最小实现纯渲染/预检与八组合GREEN，保留未知和占位输入拒绝
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

### 7.2 执行记录
- BASE=2ecd3bc3f957ac1941b388e036a6427b717b6cc7，01有效PASS后才派发。root/iter10/controller唯一写者；实现者不写卡与README。冻结协调器始终46ded3a。
- A会话1709 / 5638876b-7be3-4bc9-a2da-af32c4941033正常completed，提交f5583e542a20e00cfe9e3eae3776f32cbe9d7ae9。最小可调用入口取得19项真实断言RED；首次GREEN有HTML标记误判8失败，修正后19passed。原始失败没有覆盖，见slice-a-core-red/green/green-2。初始实现尚未GREEN的验证失败未冒作RED或已完成的失败修复回收。
- B会话1710 / 72db3dfe-466c-424e-bb74-6511fd23e455从A交接续接，正常completed，提交24a483eb7b0694ce67a5e6c0b50adb0d1cb5c160。CLI/边界17项断言RED→74项GREEN；八组合及四个实际FS绑定兼容81passed，指定五文件回归111passed；模板、说明、笔记及树/格式/范围检查已交付。兼容补充测试未经历RED，未补造。A/B全部12个runner命令COMPLETED、tree_terminal=true，退出按各原件保留；无活动命令。
- 已分别记录attempt→release→envelope，证据见implementation-checkpoint-a/b.json、native-terminal-a/b.json及handoff-a/b.json。最高TESTING，验收UNKNOWN。待独立Reviewer核对全部需求、实际源码与原始证据；批准不从实现者自检推断。
- 与01相同，C后审查runner临时原件保留build/review-02/，完整原文与原生终态归档到新review-report.json这一登记文件；其余源码/测试/check.output不在C后变化。四预算5/10/1/2及无进展门禁保持。

### 7.3 审查与裁决
- 审查：PENDING；Reviewer未分配。
- Ruling：TypeSafe采用结构化纯渲染而非模型替换段落；占位规则使用明确标记{{identifier}}、${identifier}、{TODO}/{TBD}及YYYY-MM-DD，保留合法泛型/代码/Markdown/普通TODO正文。规则与判别性测试及文档一致，原始问题/选项/响应见A/B检查点；不迁移旧卡、不放宽已有四type收据门禁。
- Deferred Minors：无。
- 初审1711/e1327c5c-738e-4e68-ad55-b7807837c24b正常completed，Scope PASSED、CHANGES_REQUESTED。F01：合法非空文本前导空白在stages/acceptance/verification误拒，真实CLI exit2；接受既有TypeSafe Important裁决及原反例，返回实现owner修复，不收窄输入合同。初审原文、runner及守卫归档review-initial-rejected.json。
- 协调登记异常：首次生成attempt因本机默认GBK解码context失败，后续PowerShell未短路而先release；无活动执行者或源码变化。主控重新claim后用显式UTF-8补记同一真实attempt，事件保留，四预算不变。后续命令按退出码短路，不将首条外层exit0视为全部成功。
<!-- /iter:ledger -->
