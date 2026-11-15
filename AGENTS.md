# AGENTS.md

## 1. 项目定位与适用范围

`iteration-manager` 是供编码助手使用的迭代管理 Skill，不是独立业务应用。它由流程契约、助手 Prompt、Python CLI、任务卡模板及验收测试组成，围绕 `docs/todos/` 提供规划、隔离执行、证据审计、交接和看板。

先区分两类工作：

- **维护本项目**：修改此仓库的脚本、契约、模板和测试。按本次授权开发，不因加载 Skill 自动启动一轮业务迭代。
- **使用本 Skill**：在目标业务项目中运行 `/iter init`、`/iter next`、`/iter task` 或 CLI。项目路径、任务卡、证据和工作区均属于目标项目，不写到 Skill 安装目录。

本文件提供项目导航及开发、使用要点，不另立任务状态或调度协议。具体流程以 [SKILL.md](SKILL.md) 和下列权威契约为准；用户本次授权和上层指令优先。仅分析、只读接管、仅生成 Prompt 不授权写文件、实施、提交或部署。

## 2. 从任务相关的入口阅读

1. 通用入口：[SKILL.md](SKILL.md)。
2. 执行与角色：[共同执行协议](references/agent_protocol.md)。
3. 解析、类型、范围、收据与冻结：[任务卡契约](references/task_card_schema.md)。
4. 然后按任务补读，不默认遍历历史证据：
   - 规划：[Planner](templates/assistants/iteration_planner.md)、[TypeSafe 指南](references/typesafe_eval_guide.md)。
   - 整轮调度：[Controller](templates/assistants/iteration_controller.md)、[Worktree 契约](references/worktree_git_contract.md)。
   - 单卡执行：[Tech Lead](templates/assistants/task_tech_lead.md)、该卡对应的 `templates/contracts/` 契约。
   - 续接、就绪和交接：[执行检查](references/execution_readiness.md)、[检查点与命令入口](references/checkpoint_execution.md)。
   - 生成新卡：[结构化生成说明](references/template_generation.md)。
   - 维护决策：检索本项目 [.agents/notes/](.agents/notes/)，不要把历史检查点里的“待审”当作当前任务状态。

## 3. 目录和模块职责

| 位置 | 职责与维护边界 |
| --- | --- |
| `SKILL.md` | Skill 发现入口、流程摘要及资源路由；保持精简 |
| `references/` | 行为契约与专题说明；修改规则先找到对应权威文件 |
| `templates/assistants/` | Planner、Controller、Tech Lead 三助手的权威指令源 |
| `templates/contracts/` | 四种任务类型的验证契约 |
| `templates/*.md` | 根索引、迭代索引、任务卡及委派模板 |
| `scripts/iter_sync.py` | 既有 CLI 入口与兼容导出、范围/Git 门禁、索引投影、终端/HTML/HTTP 看板 |
| `scripts/iter_cli.py` | 命令分派适配；`main(argv=None) -> int` 支持程序调用 |
| `scripts/iter_queries.py` | 任务发现、状态/证据审计、业务阶段及交接查询；不依赖 CLI 层 |
| `scripts/iter_contracts.py` | 扁平 frontmatter、范围、类型 checks、收据及 Git 冻结绑定 |
| `scripts/iter_filesystem.py` | 显式 filesystem profile、候选库存及快照绑定 |
| `scripts/iter_autonomy.py`、`iter_checkpoint.py` | 唯一写者、幂等事件、持久预算、受控检查点恢复 |
| `scripts/iter_preflight.py`、`iter_inventory.py` | 派发就绪检查及只读整合盘点 |
| `scripts/iter_execution.py`、`iter_timing.py` | attempt 汇总、去重耗时与可选会话轨迹；不产生批准 |
| `scripts/iter_templates.py` | 结构化 spec 渲染和新卡预检；默认只输出 stdout |
| `scripts/iter_run.py`、`iter_win_job.py`、`iter_linux_job.py` | 截止命令执行、平台进程树回收、原始输出及命令收据 |
| `scripts/deadline_watch.js` | 可注入实际委派接口的截止守卫，不负责业务调度 |
| `scripts/skill_readonly_mcp.py` | 获准后提供逐项文件白名单的只读 MCP 通路 |
| `tests/` | pytest 行为、兼容、负例与集成测试 |
| `docs/todos/` | 此 Skill 自身的维护迭代、任务卡与正式证据，不是业务项目的任务目录 |
| `docs/releases/` | 有日期的合流、部署和消费证据记录 |
| `.agents/notes/` | 维护决策理由；不维护任务状态 |
| `build/`、`.worktrees/` | 本机运行/恢复资产及隔离工作区，不是副本交付目录 |

查询层、CLI 与展示层已分工，保留 `iter_sync` 的既有导入符号、签名和入口语义。`iter_sync.main()` 与 `iter_cli.main(argv)` 的返回/异常合同不同，不为统一外观静默改写。背景见 [查询与 CLI 决定](.agents/notes/implemented/architecture/2026-11-13-query-cli-contract.md)。

## 4. 哪些信息是真源

- **任务需求、范围、状态、自治事件**：所属项目、当前 Worktree 的任务卡；`autonomy_state` 是预算与事件真源，不手工清零兼容字段。
- **迭代目标、全局约束、工具固定版本**：所属迭代 README 的 `iter:goal` 区域。
- **实际执行事实**：原始命令输出、runner 收据、原生会话/浏览器记录和独立报告。
- **完成批准**：绑定候选与冻结规格的审查收据；不能只看 `status: DONE`。
- **展示**：README 的 `iter:projection`、终端和看板是投影，不手工修改它们来修正任务事实。
- **决策理由**：项目自己的 `.agents/notes/`；不另建 `.superpowers/sdd/` 或第二套可变任务账。

## 5. 开发本项目

### 环境与改动方式

- 主体是 Python 脚本，核心 CLI 使用标准库及同目录模块；Git 模式还需要 `git` 可执行文件。
- 测试使用 `pytest`；Node 用于截止守卫和看板 DOM 替身测试。守卫本身不使用 Node API，应放入支持持久异步的工具执行器；Node 测试不证明真实委派的查询/取消链。可选只读 MCP 服务另外需要 Python MCP SDK，普通 CLI 不依赖它。
- 当前仓库没有依赖锁文件或统一安装/构建入口，不默认执行 `npm install` 或新增打包体系。脚本含 Python 3.10+ 语法；这不等于已经验证所有这些版本。
- `iter_run.py` 在 Windows 使用 Job Object，在 Linux 使用逐命令独立 subreaper 监督进程、`/proc` 和 pidfd；必要能力不可用时不启动目标，不回退裸命令、`taskkill` 或仅用 `killpg`。其他平台拒绝。源码支持与实际平台验证、独审批准分别核对。
- 修改前核对 cwd、分支、完整 HEAD、dirty 及归属，亲自读取目标代码、直接契约、调用方和测试。保留既有未跟踪目录、其他人的变更和历史输出。
- 沿用现有 Python 命名、模块分工与 UTF-8 文档风格；核心能力优先复用标准库。不要顺手全仓格式化、增加依赖或抽象。
- 变更外部输入时在解析边界校验，保留未知/坏输入的拒绝行为；不能用空值、默认批准或回退 Git 掩盖错误。
- 非平凡行为/跨模块决定按上层要求使用 `write-notes-like-deepseek`，先检索既有权威记录。说明性文档整理不必另建重复决策笔记。

### 修改时要同步考虑的直接依赖

- **流程或授权规则**：对应 reference、三助手模板、委派模板、SKILL 摘要及消费测试；共同协议不复制成三套循环。
- **任务卡或收据字段**：解析器、类型 checks、Git/FS 绑定、生成器、envelope、看板/API 和相关兼容测试。
- **CLI 或查询**：旧脚本入口、可导入函数、位置参数、stdout/JSON、返回/退出码及调用方；不引入跨调用验收缓存。
- **看板**：共享查询、HTTP 证据访问边界、终端/HTML 一致性、真实浏览器交互；模板字符串测试不代替 UI 验收。
- **执行或恢复**：原生会话终态和命令树终态分开处理，保留原始失败及幂等事件，不改旧日志来迎合新实现。

### 验证按改动选择，不逐次全量

从维护仓库根目录运行。下表列测试负载；正式测试/验收执行按 [命令入口契约](references/checkpoint_execution.md) 用 `scripts/iter_run.py` 包装，记录本次真实 UTC 截止和唯一 receipt。

| 改动 | 优先检查 |
| --- | --- |
| 说明性文档 | 新改链接、命令参数、原义及实际 diff；不跑无关业务测试 |
| 规则、Prompt、模板 | `tests/test_prompt_sources.py`、`tests/test_task_card_schema.py`；指令行为另验实际代理消费 |
| 新卡生成 | `tests/test_template_generation.py`、任务卡 schema 及相关 Git/FS 测试 |
| 查询、CLI、发现 | `tests/test_query_contract.py`、`tests/test_cli_compatibility.py`、`tests/test_sync_compatibility.py`、`tests/test_task_discovery_compat.py` |
| 就绪、自治、交接 | `tests/test_execution_readiness.py`、`tests/test_autonomy.py`、`tests/test_self_hosting.py` 及受影响报告测试 |
| 收据、范围、隔离 | `tests/test_completion_gates.py`、`tests/test_scope_firewall.py`、`tests/test_git_guards.py`、`tests/test_worktree_concurrency.py` 及相关 filesystem 测试 |
| 看板 | `tests/test_board_truth.py`、`tests/test_board_service.py`、`tests/test_board_handoff.py`；涉及 UI 时补真实路径与视觉观察 |
| 截止、恢复、时间 | `tests/test_iter_run.py`、`tests/test_deadline_watch.py`、`tests/test_checkpoint_resume.py` 及受影响 timing 测试 |

Linux 本次维护 checkout 为 `/data/workspace/iteration-manager/.worktrees/iter-11`，隔离解释器为 `/data/workspace/iteration-manager/build/iter11-venv/bin/python`（pytest 已安装）；系统可用 `python3`，不假设 `python` 存在。Windows 使用实际环境的 `python` 和 PowerShell。下面是负载示例，不是正式收据命令；正式门禁按命令入口包装。证据和临时输出放在本次授权的独立路径，保留旧文件。

规则/模板常用负载：

```powershell
python -B -m pytest -p no:cacheprovider tests/test_prompt_sources.py tests/test_task_card_schema.py -q
```

整轮最终候选的完整维护套件：

```powershell
python -B -m pytest -p no:cacheprovider tests -q
```

开发内环针对性检查；任务交付补齐对应 type 与受影响回归；迭代收口保留集成、全量及独立总审。已有任务明确要求的门禁不缩减。同候选/输入/环境下有效证据可沿用，指定独立复验仍实跑。修改检查器本身时，正式协调门禁使用迭代约定的冻结版本，不能由被测候选自证批准，见 [真实自用方法](references/self_hosting_acceptance.md)。

浏览器工作遵守本机默认 Moli 和按需 CDP 生命周期：用 `/data/home/.local/bin/moli`，只回收本次启动的服务。Git、worktree、证据及角色规则在两平台一致。

## 6. 在业务项目中使用 Skill

### 选择助手入口

| 入口 | 用途 |
| --- | --- |
| `/iter init` | 新建规划、接管或重规划；先分清只读/Prompt 与实际写入授权 |
| `/iter next` | 整轮依赖调度、续接、恢复与整体验收 |
| `/iter task` | 单任务编排、类型验证、独立审查和交接 |
| `/iter sync` | 调用实际 CLI 做投影同步或检查；不是实施授权 |

这些是助手工作流入口，不是 `iter_sync.py` 的同名子命令。是否自动注册或注入取决于实际宿主配置，不能只凭安装文件存在判断。

正常路径是：规划并通过 TypeSafe → 按授权提交规划 → 执行前校验 → 创建/复用隔离 Worktree → 只读盘点 → claim → 同 owner 的 dispatch-check → 实际派发 → 核对会话与命令终态 → attempt → release/closeout → 独审、登记与 strict → 整轮验收。完整步骤和例外只在共同协议维护。

### CLI 始终从目标项目根目录运行

下面的变量是路径示例，先换成实际安装根及目标项目文件；不要创建示例卡来迁就命令。使用冻结工具版本的迭代，应把 `$skillRoot` 指向其约定版本，而非可变安装目录。

```powershell
$skillRoot = "C:/Users/qingyu/.codeg/skills/iteration-manager"
$iteration = "docs/todos/01-example"
$card = "$iteration/01-task.md"

# 只读：查看用法、旧迭代差异、当前交接、已记录耗时、终端看板
python -B "$skillRoot/scripts/iter_sync.py" --help
python -B "$skillRoot/scripts/iter_sync.py" --takeover-report $iteration
python -B "$skillRoot/scripts/iter_sync.py" --render-envelope $card
python -B "$skillRoot/scripts/iter_sync.py" --execution-report $iteration
python -B "$skillRoot/scripts/iter_sync.py" --board $iteration
```

Linux Bash 从目标项目根使用实际安装根，例如：

```bash
skill_root=/absolute/path/to/iteration-manager
python3 -B "$skill_root/scripts/iter_sync.py" --help
python3 -B "$skill_root/scripts/iter_sync.py" --takeover-report docs/todos/01-example
```

`python3` 所在环境须具备相应依赖；维护测试可用上文 venv。Git/worktree、只读与写入授权和独立审查在两平台相同。

核实候选、终态、授权和证据可沿用时选 `--mode continue`；历史来源或收据不明时选 `--mode takeover`，不因“新会话”自动迁移。实际 context 的结构见 [执行检查](references/execution_readiness.md)：

```powershell
# 只读盘点；context 必须来自真实观察，不是预填 READY
python -B "$skillRoot/scripts/iter_sync.py" --inventory $iteration --mode continue --context evidence/context.json --phase-from-context

# 只读放行检查，但须已由当前写者 claim；phase 与 owner 用本次实际值
python -B "$skillRoot/scripts/iter_sync.py" --dispatch-check $card --context evidence/context.json --phase implementation --owner $owner
```

盘点不要求先 claim；实际派发仍须 claim 和逐卡检查。`--phase-from-context` 只用于 preflight/inventory，不用于 dispatch-check。新流程需 context；旧调用不被静默加上这一前提。就绪类命令的退出 0/2/3 分别为 READY/NEEDS_INPUT/BLOCKED，不是产品验收结果。

### 分清只读检查和显式写入

- `--preflight`、`--dispatch-check`、`--inventory`、`--takeover-report`、`--render-envelope`、`--execution-report`、`--check-scope`、`--verify-committed`、`--check-branch` 是只读检查/查询；显式 `--timing-trace` 另会写诊断轨迹。
- `--local` 刷新所属迭代 README；无命令选项的全局同步刷新根索引。即使加 `--strict` 也不自动变只读；只读核对使用 `--dry-run`。
- `--autonomy` 会写卡内事件/元数据，`--review-pkg` 会生成审查包，`--export-board` 会写迭代内 `board.html`；这些都需要相应写入授权。
- `--serve-board [port] [迭代目录]` 启动本地服务并打开浏览器，默认端口 8765，只监听 `127.0.0.1`。它不写任务状态；启动服务和真实浏览器验收是不同动作。
- 特性分支不能改 `docs/todos/README.md`，只能更新所属迭代；不要用 `--force-root` 绕过 Zero-Root-Touch。
- strict 的退出成功或空库存 EMPTY 不独自表示整轮完成；仍需核对各卡实际验收和既定整轮门禁。

### 新卡优先结构化生成

```powershell
# spec.json 和 card.md 均换成实际文件；两条命令默认不写卡
python -B "$skillRoot/scripts/iter_templates.py" --render spec.json
python -B "$skillRoot/scripts/iter_templates.py" --check card.md --delivery-mode git
```

渲染输出 Markdown，预检输出 JSON；合法为退出 0，输入/结构错误为 2。需要保存输出时另核对目标路径和覆盖权限。spec 的必需字段、占位符及 filesystem 规则见 [生成契约](references/template_generation.md)，生成成功不代表任务或验收已完成。

## 7. 必须保留的使用合同

- 状态为 `TODO → IN_PROGRESS → TESTING → DONE`，`FUSED` 表示异常阻塞；缺失或非法状态保持 `UNKNOWN`。声明 DONE 与验收 PASS 分开核对。
- 四 type 为 `Strict-TDD`、`UI-Component`、`Refactor-Benchmark`、`Spike-Discovery`，按 [任务卡契约](references/task_card_schema.md) 使用不同 checks，不给非 TDD 任务伪造 RED。
- 规划 TypeSafe 四维权重 30/30/20/20，总分至少 80 且每维至少 70；没有真实 evaluate 为 UNASSESSED，置信度不当质量分。
- 一个任务卡一个写者；实现者最高 TESTING。Controller/Tech Lead 不写业务代码，独立 Reviewer 不能参与本任务设计、实现、测试或 RCA。此处是使用这些角色时的边界，不把普通仓库维护自动切换为指定执行者模式。
- Git 交付：实现提交 C → 独审 C/冻结规格 → 登记收据及状态 D → `--local --strict`；`head_sha` 绑定 C，不冒填 D。
- FS 交付必须显式配置合法 `iteration-delivery.json`；先完成正文/ledger/勾选并冻结完整候选，再独审，登记后不能改冻结正文。坏配置不回退 Git，FS 本地收据不能替代 Git 分支/全局 strict，也不能使用 Git resume grant。
- 默认预算为单轮修复 5、累计 10、会诊 1、重规划 2；换会话不重置。连续两次无新增证据不原样第三次派发。FUSED、未知终态和缺权限不能靠改状态解锁。
- 时间中断恢复、单次 grant、截止监控及取消只按 [共同协议](references/agent_protocol.md) 和 [恢复契约](references/checkpoint_execution.md)；会话 completed 不代表命令树已结束。
- 获准开迭代时遵守 `1 Worktree = 1 Iteration`、`.worktrees/iter-{XX}` 和 `feat/iter-{XX}-*`；规划提交门禁、合流、推送、发布、清理分别核对授权。

## 8. 维护源、部署和最新发布资料

2026-11-14 Windows 发布记录中的维护源为 `C:/Users/qingyu/.codeg/skills/iteration-manager`；本次 Linux 工作源是上述 checkout，不等同于该 Windows 路径或安装部署。历史 Windows 环境的以下安装副本彼此独立，不是链接或同一 Git 工作区：

- Codex：`C:/Users/qingyu/.codex/skills/iteration-manager`。
- Gemini：`C:/Users/qingyu/.gemini/config/skills/iteration-manager`。

2026-11-15 本机只读观察：Linux 的 `/data/home/.codeg/skills/iteration-manager` 是已安装目录，`/data/home/.codex/skills/iteration-manager` 和 `/data/home/.gemini/config/skills/iteration-manager` 均指向该目录的符号链接；与上述历史 Windows 独立副本不同。它不是本次 worktree，本次未同步或验证其采用候选，使用时重新核对实际路径与版本。

副本同步是另一个获准部署动作，不是 `/iter sync` 的功能。现有交付白名单是 `SKILL.md`、`scripts/`、`references/`、`templates/`、`tests/`、`.agents/notes/`；不复制 `.git`、`.gitignore`、维护 `docs/todos/`、`build/`、缓存或历史备份。本文件 `AGENTS.md` 不在既有白名单内，不因新增而自动部署。

整轮验收及部署授权就绪后再同步同一候选；覆盖前核对目标漂移、精确备份并保留恢复路径。三助手模板更新不等于宿主配置更新，配置回读也不等于新会话采用。只读授权通路的注册、实际消费和撤销按 [受控读取契约](references/readonly_skill_access.md)，不照搬历史数据库写入方法或助手 ID。

发布资料按观察日期和操作范围读取：

- [2026-11-14 迭代10发布记录](docs/releases/iteration10-20261114/README.md)：本地合流、双副本同步、显式安装根的新会话消费及回滚材料入口。
- [发布分层索引](references/release_status.md)：保留 2026-11-13 等历史观察，不覆盖为最新安装事实。
- [迭代10记录](docs/todos/10-self-hosting-hardening/README.md)：当轮六卡与整轮审查；其当时“未部署/未合流”不否定后续另获授权的发布。

2026-11-14 发布记录中的 493 项通过是该发布候选的历史实测，不是本次或未来版本的测试结果。已验证的是显式安装根消费；Gemini CLI 自动发现、当前助手自动注入及真实 FS 业务生命周期不能据此认定通过。完整维护套件应在维护仓库运行，安装副本缺少部分测试依赖的维护 harness；不为跑副本全量而擅自扩大部署清单。

交付时给出实际修改、适用候选、检查及原始证据、真实缺口；不要把源码完成、安装落盘、新会话采用和外部业务通过合并成一个 PASS。

本次 Linux 源码及测试证据以 task00 原始收据和独立审查为准；历史 Windows 验证见有日期发布记录，本次 Linux 会话未重跑 Windows Job 实测。安装落盘、新会话消费及外部业务验证分别核实。
