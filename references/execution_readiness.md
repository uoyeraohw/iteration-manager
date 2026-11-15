# 派发前检查与可继承交接

新建迭代或明确获准采用本流程时，从项目根目录使用冻结的工具版本：准备观察上下文 → `--preflight`盘点 → `--autonomy claim`领取唯一写者 → 按[共同协议](agent_protocol.md#新流程的默认派发codeg-已验证的-tool-call-适配)由守卫执行同写者 `--dispatch-check` 后派发 → 查询真实终态 → 当前写者登记attempt → release或超时closeout → 输出envelope。preflight不要求先claim，不授予写权；逐卡dispatch-check必须确认已claim且owner匹配。检查只读，不保留另一个调度锁，主控须在整个派发期间维持唯一写者。整轮盘点不要求所有卡READY后才能做独立任务；已DONE卡不能再派发，会在逐卡结果中标为BLOCKED。

旧claim/recover/release、旧卡及原strict门禁不新增context前提，也不会自动记录尝试。本工具不调用原生委派接口；新流程的主控必须在**每次实际派发前**消费检查结果。不得用旧claim绕过新流程的BLOCKED。`--preflight`/`--dispatch-check`只读，不跑业务测试、不写卡、不签发批准；READY只表示观察齐备，不是产品验收。

## 用观察上下文检查就绪

以下是结构示例，路径、候选和观察均须用本项目实际值替换，不能直接当作执行事实：

```json
{
  "version": 1,
  "tasks": {
    "01": {
      "phase": "implementation",
      "candidate": "实际完整HEAD或FS candidate_id",
      "inputs": ["docs/todos/01-demo/01-task.md", "src/entry.py"],
      "capabilities": ["指定执行者/原生UI能力"],
      "dependencies": [],
      "tool_entry": "C:/实际冻结版本/scripts/iter_sync.py",
      "checkpoint": "本窗口计划交付核心GREEN",
      "remaining_work": ["独立审查"],
      "observations": {
        "authority": {"status": "READY", "summary": "实际授权范围", "evidence": "evidence/authority.txt"},
        "execution": {"status": "READY", "summary": "指定执行者已能读取必读契约", "evidence": "evidence/access.txt"},
        "verification": {"status": "READY", "summary": "所需验证入口与资源可用", "evidence": "evidence/tools.txt"}
      }
    }
  }
}
```

```powershell
python <skill_root>/scripts/iter_sync.py --preflight docs/todos/01-demo --context evidence/context.json --phase implementation
python <skill_root>/scripts/iter_sync.py --preflight docs/todos/01-demo --context evidence/context.json --phase-from-context
python <skill_root>/scripts/iter_sync.py --dispatch-check docs/todos/01-demo/01-task.md --context evidence/context.json --phase implementation --owner <当前写者>
```

- JSON顶层精确两键version/tasks；任务项使用上例字段，可另加`required_observations`字符串数组和`change_evidence`路径。未知字段拒绝。
- 盘点同阶段任务可显式传`--phase <实际阶段>`；不同阶段混合时可显式选择`--phase-from-context`，逐卡读取该卡context的phase并在结果中显示。主控使用前须核对context阶段与本次授权目标一致；脚本不独立证明context是最新状态。两选项互斥，缺context为NEEDS_INPUT；对应任务phase缺失、空白或非法为BLOCKED，不回退默认。此选项用于`--preflight`或`--inventory`盘点，不用于派发；派发前`--dispatch-check`仍须明确传该卡实际`--phase`和已claim的owner。
- 不使用新选项的旧调用保持默认`implementation`及原退出码；不会因context里有不同phase而隐式改为READY。阶段/候选不匹配仍BLOCKED，保留原通用提示，并分别给出请求/观察阶段或实际/上下文候选，以便一次定位；检查不改变预算、授权或独审门禁。
- candidate必须匹配实际项目完整HEAD或显式FS配置下的candidate_id；从真实项目根运行。scope来自卡片，不接受context另报白名单。inputs为项目内现有文件，capabilities为明确能力标签，均非空、去重。执行约定的工具版本仍由README持有，tool_entry必须指向本次真实调用入口。
- 未知任务type或非法已声明schema版本不能通过新就绪检查；type决定必要验证契约。旧卡读取和迁移授权边界保持不变。
- dependencies显式列项目内前置任务卡；每张都用原收据及冻结绑定核对有效DONE，不能只看状态。空数组表示无依赖，主控仍需对照卡片核实完整性。
- authority/execution/verification均需观察；UI-Component另需`ui-entry`，包含真实入口、对象来源及实际视口的证据。媒体等额外要求放`required_observations`，如`["native-media"]`，并在observations提供对应事实。能力标签和文件存在不证明真实交互，独审仍读原始证据。
- observation.status可为READY/NEEDS_INPUT/BLOCKED；summary非空，READY必须有项目内非空evidence。未知或不可用按实际填写，不把计划写成已观察事实。
- 退出0为READY，2为NEEDS_INPUT，3为BLOCKED。dispatch-check缺已claim写者或owner为NEEDS_INPUT，外来owner为BLOCKED。缺context不改卡；错误配置、预算阻塞、UNKNOWN/FUSED/DONE卡不会READY。阶段名、候选标签和换会话不清无进展历史。

## 在唯一事件账记录尝试

主控查询原生会话终态并收齐命令终态后，让当前已claim的写者消费项目内唯一尝试报告。下级只返回报告与原始证据，不并发写卡。报告不能覆盖历史；稳定event-id重试必须使用同一报告内容。重放返回原事件快照与结果，候选后来移动也不重算历史；同ID改报告或参数仍拒绝。

```powershell
python <skill_root>/scripts/iter_sync.py --autonomy attempt <任务卡> --event-id <稳定尝试ID> --owner <当前写者> --executor-state completed --evidence evidence/attempt-01.json
```

报告精确字段如下（示例，所有事实须替换）：

```json
{
  "version": 1,
  "phase": "implementation",
  "candidate": "实际完整HEAD或FS candidate_id",
  "inputs": ["src/entry.py"],
  "capabilities": ["指定执行者/原生UI能力"],
  "checkpoint": "本次实际交付有效RED",
  "remaining_work": ["最小实现", "GREEN", "独立审查"],
  "executor_id": "原生会话ID",
  "terminal_evidence": "evidence/native-terminal.json",
  "progress": [{"kind": "red", "summary": "具体断言失败", "evidence": "evidence/red-output.txt"}],
  "commands": ["evidence/red-command.json"],
  "started_at": "2026-11-12T00:00:00+00:00",
  "ended_at": "2026-11-12T00:01:00+00:00"
}
```

progress只接受red/implementation/green/root-cause/review-finding，逐项附非空项目内原始产物和摘要；无产物用空数组。checkpoint是摘要，**没有新增progress时不会成为可继承成果**。计划、阅读量或重复证据路径不算新进展；复用旧证据保留原路径，不复制改名冒充新增。

commands列真实`iter_run.py`项目内receipt；必须version1、cwd匹配、argv非空、tree_terminal=true及可读output（输出可以为空）。COMPLETED必须有真实整数raw_exit_code，失败退出也可登记。TIMED_OUT/NOT_STARTED/ERROR只在进程树确认终态时可作为失败历史登记，保留状态和未知exit，不能当RED/GREEN。RUNNING/CLEANUP_UNKNOWN及未确认终态拒绝。会话terminal_evidence与`executor-state`仍需对照原生结果；不能把会话停止当命令停止。

时间用带时区ISO，未知起止成对null；命令收据未启动或无完整区间时耗时为null。已知区间须有序且在已知会话区间内。命令区间取并集，避免重叠重复累加；它是runner起止区间（含收尾），不是纯测试编写、CPU或模型推理耗时。会话耗时单列，未记录交接耗时不推算。

attempt只写现有autonomy_state.events的规范化报告快照，不增加/清零四预算、不抢写者、不解除FUSED、不替代release/closeout。真正超时仍按原协议closeout；命令终态未知时保留阻断，不因尝试记录而重派。FS恢复仍不支持，不能套Git resume grant。

## 第三次派发必须带来变化

从事件顺序派生连续无新增证据的次数，重启、换会话、release、普通recover/replan不清此记录。达到两次后：

1. inputs、卡片scope和capabilities均相同 → BLOCKED。
2. 条件确有改变但缺change_evidence → NEEDS_INPUT。
3. 改变条件并附项目内非空change_evidence → 可继续其它就绪检查，但不解除预算/超时阻断。

缩小切片或修改输入时使用新的冻结输入文件引用并说明改变依据；不要只改phase/candidate/会话标签。卡片scope变化需原授权，不能通过删验收来解锁。脚本比较规范化引用与标签，不分析文件语义；主控及独审核实变化是否真的解决缺口。没有attempt记录的历史不推测为“两次失败”。

## 交接直接继承成果，不重读整个项目

`--render-envelope`保留原schema_version及全部旧键，追加delivery_mode、candidate_id与execution。FS candidate_id与真实卡/收据交叉核对；Git仍使用原commit_sha/base_sha，未登记则为空，不拿当前HEAD填造交付SHA。

execution包含attempt_count、no_progress_streak、last_attempt（报告源、会话、候选、条件、命令与分项时长）、checkpoint（最近一次新增产物及其原候选）、remaining_work。无记录时last_attempt/checkpoint为null、计数0、remaining_work为空，不表示任务已完成。旧候选成果保留来源，按受影响范围核实可复用性；交接摘要不是批准，真实验证、独立审查和新候选收据绑定照旧。

## 主控实际消费，不只展示报告

### 一次只读盘点，明确续接或接管

```powershell
python <skill_root>/scripts/iter_sync.py --inventory docs/todos/01-demo --mode continue --context evidence/context.json --phase-from-context
python <skill_root>/scripts/iter_sync.py --inventory docs/todos/01-demo --mode takeover --context evidence/context.json --phase implementation --details
```

`--mode`必填：已核实候选、终态、授权与证据仍适用的同一迭代续接选continue；旧迭代的历史基线、收据或来源不明选takeover，额外报告`missing`及迁移/补验授权提示。模式是调用方选择，不证明条件已满足，不能用continue抹掉缺口或绕过原合同。

`missing`沿用旧接管报告的字段库存，不按任务阶段自动判断逾期：尚未完成的任务缺`review_receipt`本身不等于失败或需要提前审查。按实际状态、验收结论和任务合同判断，只有需要迁移或补验证据时才请求相应授权。

摘要逐卡给出readiness与findings、实际验收审计的acceptance_verdict及receipt、候选与交付模式、writer/阻断、checkpoint与remaining_work；READY与验收PASS分别判断。同一次调用加`--details`会附上该次preflight及完整handoff结构，保留证据路径，不额外重复审计；再次调用则重新读取和检查当前状态。依赖和任务本身在同一次盘点中复用同一次审计结果；越界或坏卡保留BLOCKED/UNKNOWN，其它卡仍逐项返回。空目录NEEDS_INPUT；整体退出0/2/3分别为READY/NEEDS_INPUT/BLOCKED，不要求所有卡READY才能继续独立任务。

`--inventory`只做读取，不能建立写者、终态、授权或context新鲜度；phase选择遵守前述`--phase`/`--phase-from-context`规则。领取写者后每次实际派发仍须调用原`--dispatch-check --phase <实际阶段> --owner <当前写者>`。不改旧CLI、任务卡或批准收据；新候选、真实验证和独立审查照旧。

1. 逐卡读取preflight结果，选择无依赖和写冲突的READY卡；其他卡的BLOCKED不成为整轮停工条件。claim后检查同owner的dispatch-check，非READY不派发该步骤。
2. 按[共同协议](agent_protocol.md#新流程的默认派发codeg-已验证的-tool-call-适配)消费守卫后调用当前环境真实委派工具，保存实际会话ID；先读完整终态及原始命令收据，再由唯一写者记录attempt。只有原生查询确认终态，才能release或closeout；报告里的executor_id不是终态证明。
3. 下次会话从envelope.execution的checkpoint、source和remaining_work开始：核对原候选及适用范围，只做剩余工作。预算阻塞/未知终态不通过“换阶段”绕过；正常release不要求resume grant。
4. 同候选重复回收、换窗口和汇总报告不触发另一轮全套验收。交付时在现有Brief/审查报告逐项列出：`检查/覆盖行为 → 原候选及证据路径 → 本次变更/输入/环境影响依据 → 沿用或重跑及责任人`；没有变化且证据有效则直接沿用，指定独立复验项仍实跑。影响不明扩大检查；新候选仍需受影响独审及新冻结绑定，不复制旧批准。
5. 主管回收时核对交接字段与原始产物，主控接收后只补缺失项和跨任务门禁，不再逐卡派一名相同范围审查者。真实行为、type必需证据和独立审查仍保留。

## 只读耗时报告：先看重复与重叠

从项目根运行，输出JSON到stdout，不更新卡片、索引、预算或验收状态：

```powershell
python <skill_root>/scripts/iter_sync.py --execution-report docs/todos/01-demo
```

- 读取可识别任务卡的现有autonomy_state.events，不执行命令、不复查今天的可变receipt来改写历史。逐卡保留库存，项目外符号链接卡在发现及读取前拒绝且不读内容，坏卡/快照冲突在errors列出，退出2；正常报告退出0。无记录/缺时间不是零耗时。
- task_count为库存数，attempt_count为有效卡的attempt事件数；会话按executor_id、命令按项目内规范化receipt路径跨卡去重。相同身份的起止/命令终态快照冲突会报警，冲突项不计入known部分，完整量为null；原生ID必须使用原始真实ID，不得重复编造。
- timing分别列session/command的resource_seconds（去重后的累计区间）和observed_union_seconds（区间并集）。known_*仅统计已知非冲突部分；对应*_time_complete及complete标示完整性。有坏卡或无attempt旧卡时整体保持不完整。
- observed_span_seconds只是已记录区间的最早起点至最晚终点，可能含间隙；iteration_elapsed_seconds为null。phases只按报告的phase原文分组；同一命令/会话可能跨phase引用，各组不能相加当迭代墙钟。空命令列表、未启动或缺时间保持未知。
- 命令区间含runner收尾，会话区间含等待；两者互有重叠，不能相加，也不能拆成测试编写、纯开发、推理或工具延迟。报告不生成READY/APPROVED，不承诺业务节时比例。

## 可选会话轨迹：定位盘点与未覆盖区间

只在本次授权写诊断证据时使用，目标路径必须在项目根内、父目录已存在；一条轨迹由一个主控串行写入。默认调用不写轨迹。以下`<skill_root>`是实际冻结版本，示例路径须按授权替换：

```powershell
python <skill_root>/scripts/iter_sync.py --timing-init evidence/timing.jsonl <真实会话ID>
python <skill_root>/scripts/iter_sync.py --preflight docs/todos/01-demo --context evidence/context.json --phase evidence-inspection --timing-trace evidence/timing.jsonl
python <skill_root>/scripts/iter_sync.py --inventory docs/todos/01-demo --mode continue --context evidence/context.json --phase-from-context --timing-trace evidence/timing.jsonl
python <skill_root>/scripts/iter_sync.py --timing-import-receipt evidence/timing.jsonl evidence/verify.json --category verification --operation test --target 01
python <skill_root>/scripts/iter_sync.py --timing-report evidence/timing.jsonl
```

初始化独占创建，不覆盖原文件。预检和盘点仅在显式传`--timing-trace`时按UTC记录开始、结束、实际参数、结果；中断会留下未完成区间。区间是脚本调用内部的检查时间，不包括完整进程启动或外层等待。`--dispatch-check`不支持该参数。runner导入直接读取本项目已确认进程树终态的原始收据；标签由调用者指定，不推断测试类型。相同收据快照去重，冲突标错且不算入已知值。

会话边界、审查或交接可由主控基于真实原始记录准备项目内JSON，再显式`--timing-import evidence/timing.jsonl evidence/observation.json`。会话观察格式为`{"type":"session","clock_basis":"local_utc","started_at":"带时区时间或null","ended_at":"带时区时间或null"}`；活动观察格式为`{"type":"activity","category":"review","operation":"独立审查","target":"01","clock_basis":"local_utc","started_at":"带时区时间或null","ended_at":"带时区时间或null"}`。分类为inventory/execution/verification/review/handoff/other；来源路径指向该观察文件，调用者须在观察文件以外保留并核对原始会话/工具证据，不将转录本身当真实性证明。`clock_basis`是调用者核实的共同时间基准，不能仅因都标UTC就假定跨机器时钟同步；工具本机计时与本机runner为`local_utc`。不同或未记录的基准不做跨源并集及未覆盖计算。未知不造时间；多个会话边界或不合法区间报错。不得将敏感内容写入轨迹。

上级确认真实会话终态后，可以追加独立观察文件并沿用`--timing-import`：`{"type":"session_terminal","session_id":"与轨迹头一致的真实会话ID","clock_basis":"local_utc","started_at":"原生来源起点或null","ended_at":"原生来源终点","terminal_state":"completed"}`。终态仅接受completed/failed/canceled；其来源文件及原始原生终态必须保留。报告将已有session起点和追加终点关联，原session和终态观察各保留来源；原start不修改。同源相同快照幂等；不同ID、相互冲突的起止/终态或基准不兼容拒绝或报告错误且耗时未知。没有可靠起点仍未知；不将委派墙钟自动当会话边界。

新轨迹在盘点完成记录中追加`phase_details`，逐卡保存当次检查阶段`checked_phase`、成功读取的`context_phase`与`phase_match`；未读取或非法时为null，不在报告时重新读取context。原`observed_phases`仍保留，含义为当次检查结果的phase，不保证是context的实际阶段；旧轨迹没有`phase_details`时保持缺失，不追溯推断。旧CLI结果、阶段门禁和默认值不变。

报告只读取，分别给出分类已知累计与并集、已观察跨度、同一operation及target的重复调用原始事实。分类中的`complete`保持原义：已记录项时间均已知、报告没有全局错误且同类区间时钟可比；`recorded_intervals_complete`是其同值明确别名。没有记录时它也可能为true，并不证明活动全程被记录；`known_resource_seconds=0`只表示已记录部分为零，不代表真实活动没有耗时。`full_activity_coverage`目前恒为`UNKNOWN`，不从记录数量推断活动是否存在或是否覆盖全程。重复不自动等于多余：需核对候选、输入、授权和状态有无变化。会话边界和已记录活动时间完整、无冲突且时钟可比时才计算未覆盖墙钟＝会话区间减已记录活动并集；它不是推理、开发、空闲或浪费，也不证明全程覆盖。会话、等待、命令可重叠，不能相加。旧字段、退出码、`--execution-report`和任务卡均不变；轨迹不是验收或派发授权。
