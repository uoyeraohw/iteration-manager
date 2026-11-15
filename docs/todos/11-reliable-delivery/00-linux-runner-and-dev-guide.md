---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "00"
task_name: "Linux截止入口与双环境开发指引"
status: "TESTING"
type: "Strict-TDD"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "95.375"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/linux-typesafe-summary.json"
tdd_verified: true
review_status: "PENDING"
review_receipt: ""
base_sha: "894dfd6d5d93d2ff99f6eddcaadbb88ee9ce44c3"
head_sha: ""
autonomy_state: "{\"version\":1,\"policy\":{\"round_limit\":5,\"total_limit\":10,\"consilium_limit\":1,\"replan_limit\":2},\"round\":0,\"total\":0,\"consilium\":0,\"replan\":0,\"writer\":\"iter11-controller-linux-20261115\",\"events\":{\"iter11-00-claim-bootstrap-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"00-linux-runner-and-dev-guide\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TODO\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T02:56:37.956892+00:00\"},\"iter11-00-attempt-bootstrap-v1\":{\"input\":{\"action\":\"attempt\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-attempt.json\",\"executor_state\":\"completed\",\"attempt\":{\"report\":{\"version\":1,\"phase\":\"implementation\",\"candidate\":\"894dfd6d5d93d2ff99f6eddcaadbb88ee9ce44c3\",\"inputs\":[\"docs/todos/11-reliable-delivery/00-linux-runner-and-dev-guide.md\",\"docs/todos/11-reliable-delivery/README.md\",\"docs/todos/11-reliable-delivery/evidence/planning/platform-migration-authorization.json\",\"docs/todos/11-reliable-delivery/evidence/planning/linux-capabilities.json\",\"docs/todos/11-reliable-delivery/evidence/planning/cli-runtime-probe.json\",\"scripts/iter_run.py\",\"scripts/iter_win_job.py\",\"tests/test_iter_run.py\",\"AGENTS.md\",\"references/checkpoint_execution.md\",\"docs/todos/11-reliable-delivery/evidence/00/bootstrap_command.py\"],\"capabilities\":[\"native-codex-cli-exec-session\",\"GNU-timeout-task00-bootstrap\",\"Linux-proc-subreaper-pidfd\",\"independent-native-review-required\"],\"checkpoint\":\"有效公共CLI断言RED、Linux隔离监督及双环境指引；最终GREEN24/2skip，定向回归141/2skip\",\"remaining_work\":[\"独立审查C\",\"批准后登记D和冻结local strict\",\"导出已审runner并运行01前完整维护基线\"],\"executor_id\":\"01a1dd24-bea9-7580-bfbd-5afac812648b\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-terminal.json\",\"progress\":[{\"kind\":\"red\",\"summary\":\"旧Linux公共CLI实际125 vs期望7；引导例外，不是导入失败\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-red-bootstrap.json.output.txt\"},{\"kind\":\"implementation\",\"summary\":\"Linux后端、通用入口、测试、AGENTS和平台契约的可审差异\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-source-manifest.json\"},{\"kind\":\"green\",\"summary\":\"最新候选24 passed/2 Windows skips；141 passed/2 skips回归，实际runner终态\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression-v2.json.output.txt\"}],\"commands\":[\"docs/todos/11-reliable-delivery/evidence/00/slice-a-exit7.json\",\"docs/todos/11-reliable-delivery/evidence/00/slice-a-green-final.json\",\"docs/todos/11-reliable-delivery/evidence/00/slice-a-green-v2.json\",\"docs/todos/11-reliable-delivery/evidence/00/slice-a-green.json\",\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression-final.json\",\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression-v2.json\",\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression.json\"],\"started_at\":null,\"ended_at\":null},\"source\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-attempt.json\",\"phase\":\"implementation\",\"delivery_mode\":\"git\",\"candidate\":\"894dfd6d5d93d2ff99f6eddcaadbb88ee9ce44c3\",\"conditions\":{\"inputs\":[\"AGENTS.md\",\"docs/todos/11-reliable-delivery/00-linux-runner-and-dev-guide.md\",\"docs/todos/11-reliable-delivery/README.md\",\"docs/todos/11-reliable-delivery/evidence/00/bootstrap_command.py\",\"docs/todos/11-reliable-delivery/evidence/planning/cli-runtime-probe.json\",\"docs/todos/11-reliable-delivery/evidence/planning/linux-capabilities.json\",\"docs/todos/11-reliable-delivery/evidence/planning/platform-migration-authorization.json\",\"references/checkpoint_execution.md\",\"scripts/iter_run.py\",\"scripts/iter_win_job.py\",\"tests/test_iter_run.py\"],\"capabilities\":[\"GNU-timeout-task00-bootstrap\",\"Linux-proc-subreaper-pidfd\",\"independent-native-review-required\",\"native-codex-cli-exec-session\"],\"scope\":[\".agents/notes/planned/iter11/00-linux-runner.md\",\"AGENTS.md\",\"docs/todos/11-reliable-delivery/evidence/00/\",\"references/checkpoint_execution.md\",\"scripts/iter_linux_job.py\",\"scripts/iter_run.py\",\"tests/test_iter_run.py\",\"tests/test_linux_runner.py\"]},\"executor_id\":\"01a1dd24-bea9-7580-bfbd-5afac812648b\",\"executor_state\":\"completed\",\"terminal_evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-terminal.json\",\"progress\":[{\"kind\":\"red\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-red-bootstrap.json.output.txt\",\"summary\":\"旧Linux公共CLI实际125 vs期望7；引导例外，不是导入失败\"},{\"kind\":\"implementation\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-source-manifest.json\",\"summary\":\"Linux后端、通用入口、测试、AGENTS和平台契约的可审差异\"},{\"kind\":\"green\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression-v2.json.output.txt\",\"summary\":\"最新候选24 passed/2 Windows skips；141 passed/2 skips回归，实际runner终态\"}],\"checkpoint\":\"有效公共CLI断言RED、Linux隔离监督及双环境指引；最终GREEN24/2skip，定向回归141/2skip\",\"remaining_work\":[\"导出已审runner并运行01前完整维护基线\",\"批准后登记D和冻结local strict\",\"独立审查C\"],\"commands\":[{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-exit7.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":7,\"started_at\":\"2026-11-15T03:02:42.216980+00:00\",\"ended_at\":\"2026-11-15T03:02:42.249670+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-green-final.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T03:01:24.552649+00:00\",\"ended_at\":\"2026-11-15T03:01:45.941627+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-green-v2.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T03:02:32.113913+00:00\",\"ended_at\":\"2026-11-15T03:02:55.658371+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-green.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T03:00:13.822426+00:00\",\"ended_at\":\"2026-11-15T03:00:35.132920+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression-final.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T03:01:54.099663+00:00\",\"ended_at\":\"2026-11-15T03:02:24.105086+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression-v2.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T03:03:00.382437+00:00\",\"ended_at\":\"2026-11-15T03:03:32.862198+00:00\"},{\"receipt\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-regression.json\",\"status\":\"COMPLETED\",\"raw_exit_code\":0,\"started_at\":\"2026-11-15T03:00:41.137517+00:00\",\"ended_at\":\"2026-11-15T03:01:11.799929+00:00\"}],\"started_at\":null,\"ended_at\":null,\"session_seconds\":null,\"command_seconds\":159.391526}},\"result\":{\"task_id\":\"00-linux-runner-and-dev-guide\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T03:08:41.451071+00:00\"},\"iter11-00-release-bootstrap-v1\":{\"input\":{\"action\":\"release\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"docs/todos/11-reliable-delivery/evidence/00/slice-a-terminal.json\",\"executor_state\":\"completed\"},\"result\":{\"task_id\":\"00-linux-runner-and-dev-guide\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"\",\"consilium_bundle\":null},\"at\":\"2026-11-15T03:08:41.538250+00:00\"},\"iter11-00-claim-review-v1\":{\"input\":{\"action\":\"claim\",\"owner\":\"iter11-controller-linux-20261115\",\"reason\":\"\",\"evidence\":\"\",\"executor_state\":\"\"},\"result\":{\"task_id\":\"00-linux-runner-and-dev-guide\",\"previous_rounds\":0,\"current_rounds\":0,\"fix_total\":0,\"consilium_count\":0,\"replan_count\":0,\"is_fused\":false,\"status\":\"TESTING\",\"blocked_reason\":\"\",\"writer\":\"iter11-controller-linux-20261115\",\"consilium_bundle\":null},\"at\":\"2026-11-15T03:10:54.899280+00:00\"}},\"blocked_reason\":\"\"}"
updated_at: "2026-11-15T03:10:54.899389+00:00"
---

# 00 · Linux截止入口与双环境开发指引

## 1. 任务执行目标与接口契约

- **目标**：按2026-11-15用户明确要求适配当前Linux，并继续支持Windows。解除本轮因Windows-only runner造成的启动阻断；在AGENTS.md说明两环境的开发、使用与验证边界。
- **Consumes**：`iter_run.run_check(argv, deadline, evidence, cwd=None)`与现有CLI；version1 runner收据及autonomy attempt消费；Windows `Job.attach/stop/close`；当前Linux的`/proc`、subreaper与pidfd能力。
- **Produces**：保持`run_check`签名、argv直接传递、CLI退出和version1收据合同；Linux专用后端`iter_linux_job.py`负责有启动门闩的独立监督进程、后代回收及真实终态；Windows继续使用Job Object。
- **平台范围**：本轮实测Linux/Python3.13.5/Node22.23.3；保留Windows路径及其平台专属测试，本机不冒称Windows复验。未支持平台、缺Linux必要能力/权限时在启动目标前拒绝，不能降级成裸命令或无终态保证的killpg。

## 2. 业务阶段
<!-- iter:stages -->
- [x] 在当前Linux公共CLI构造有效的支持行为断言RED
- [x] 实现Linux隔离监督与进程树终态，完成针对性GREEN
- [ ] 整理双环境指引、完成受影响回归及独立验收，冻结获准runner供后续卡使用
<!-- /iter:stages -->

## 3. 类型验证与引导例外
<!-- iter:verification -->
- [x] **red**：同一实现者先新增Linux公共CLI测试；在旧runner上以真实断言如`exit125 != expected7`证明功能缺失。Python/pytest/导入失败不算RED。使用本卡专属GNU timeout引导入口，同调用记录绝对UTC、argv/cwd、stdout/stderr和实际exit；明确标记bootstrap，不伪造iter_run收据。
- [x] **green**：`python3 -B -m pytest -p no:cacheprovider tests/test_iter_run.py tests/test_linux_runner.py -q`；新runner的同调用截止入口运行，保留真实runner收据和输出。
- [x] **regression**：`python3 -B -m pytest -p no:cacheprovider tests/test_iter_run.py tests/test_linux_runner.py tests/test_checkpoint_resume.py tests/test_execution_readiness.py tests/test_autonomy.py tests/test_prompt_sources.py tests/test_task_card_schema.py -q`；通过新runner；影响不明扩大。本卡验收后、01实施前另运行完整维护套件干净基线。
<!-- /iter:verification -->

引导例外仅为本卡解决“未适配runner无法测试自身适配”的启动循环：GNU timeout为独立系统入口，最长180秒并另留5秒强制回收；只用于runner开发测试，保留bootstrap真实观察，不能供后续卡替代正式runner。后续GREEN、回归及独立复验使用候选Linux runner，独立Reviewer判定原始证据；正式批准仍由fdcc4cc冻结协调器及非参与者完成，候选不能自证批准。

## 4. 交付与冻结

提交C包含源码、测试、正文及原始输出；非参与者独审C/冻结规格后登记D和local strict。主控只协调、不写产品代码。获准后将C中的runner及直接依赖导出到主checkout的`build/frozen-runners/iter11-platform-v1/`，保存来源及逐文件SHA256；后续不自动追随候选。协调CLI仍固定fdcc4cc，只有runner进行本次显式平台迁移。原Windows-only快照及启动拒绝不覆盖。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `scripts/iter_run.py` | MODIFIED | 后端选择与共同收据/启动门闩 |
| `scripts/iter_linux_job.py` | ADDED | Linux监督、后代回收和终态确认 |
| `tests/test_iter_run.py` | MODIFIED | 通用行为及Windows专属条件 |
| `tests/test_linux_runner.py` | ADDED | Linux真实进程与负例 |
| `AGENTS.md` | MODIFIED | Windows/Linux开发与使用指引 |
| `references/checkpoint_execution.md` | MODIFIED | Linux命令入口与平台终态合同 |
| `.agents/notes/planned/iter11/00-linux-runner.md` | ADDED | 选择、迁移和限制理由 |
| `docs/todos/11-reliable-delivery/evidence/00/` | ADDED | 本卡原始证据、独审与收据 |
<!-- /iter:scope -->

## 6. 确定性验收
<!-- iter:acceptance -->
- [ ] 当前Linux的公共CLI真实执行并保留stdout、argv/cwd、实际exit7；业务exit124/125与TIMED_OUT/ERROR可区分；过期及剩余不足回收窗口不启动目标，收据及sidecar不覆盖、路径不能越界。
- [ ] 真实验证超时、父先退出的孤儿、多级后代及setsid另开会话；返回前回收并确认本次完整树终态，无延迟文件副作用；无关进程仍存活。缺必要内核能力、准备/启动门闩失败、清理不确定时不能返回成功或伪造tree_terminal。
- [ ] SIGTERM等可处理的外部中断触发回收；不可证明的强杀/不完整收据保持UNKNOWN，不能由外层会话停止补造终态。并行调用隔离，不能在长期主控进程全局设置subreaper。
- [ ] Windows Job实现保持原语义，Windows专属测试按平台明确标记；Linux不得导入WinDLL执行路径；不在本机声称Windows通过，不承诺macOS或容器越权逃逸防护。
- [ ] AGENTS.md分别给出实际维护/安装路径、Python与shell命令、deadline/退出传播、平台进程机制、依赖/浏览器/临时输出及验证状态；CLI从目标项目根运行和独立副本部署边界在两环境一致，不自动部署。
- [ ] 沿用现有version1收据供attempt/恢复/耗时消费；正式协调器仍用冻结fdcc4cc，不改预算、任务状态语义或旧批准，完成独审/登记/strict后才推进01。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
尚未实施；用户最新平台适配要求授权此00前置迁移，保留原十二卡目标、顺序与验收。Codeg原生读探针遇到bwrap启动故障，保留原件；当前协作通路另行核实，不把工具schema或probe completed当产品PASS。

2026-11-15原生实现会话`01a1dd24-bea9-7580-bfbd-5afac812648b`已正常终态；会话UTC原件未提供，attempt时间保持null，不把外层请求时间冒作会话起止。有效RED见slice-a-red-bootstrap（退出1，断言125 != 7）；最新真实runner GREEN24通过/2 Windows跳过，受影响回归141通过/2跳过，另有exit7/stdout实测。原始命令收据均COMPLETED且tree_terminal=true。当前最高TESTING，未独审/未批准；窗口内主动补充启动中断、缺pidfd、监督进程丢失和并发隔离反例，历史输出全部保留。实际来源及剩余项见evidence/00/slice-a-delivery.json。
<!-- /iter:ledger -->

## 8. 执行边界

- 无硬依赖；本次显式前置00，验收PASS后恢复01—12串行。
- 不修改12拥有的共同协议流程段落；其旧Windows-only句在本次用户授权和平台迁移约定范围内由checkpoint_execution/AGENTS的Linux合同接续，12收敛默认流程时同步更新，避免两卡共享可变源码范围。
- 不修改历史迭代/发布原件、根索引或实际安装副本；不部署、推送、合流或清理。
