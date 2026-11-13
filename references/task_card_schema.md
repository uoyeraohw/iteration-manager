# 任务卡与验收证据契约（schema_version: 1）

本文件是第一批门禁的行为契约。Skill版本号与任务卡格式版本互相独立。

## 声明状态不等于验收

状态保留 TODO、IN_PROGRESS、TESTING、DONE 和异常熔断 FUSED。只读取完整frontmatter中的完整合法值；未知值返回UNKNOWN，不从正文示例猜测状态。
无schema_version的旧卡仍可读取声明状态；旧DONE缺收据时验收为UNKNOWN，不能通过严格门禁。不写回或补造tdd_verified、review_status。
验收结果为PASS、FAIL、UNKNOWN、BLOCKED；仅PASS可以放行。非DONE不自动变成DONE，也不表示整轮已完成。

## 新卡结构

frontmatter使用扁平key:value，必需字段为schema_version、task_id、type、status；完成时还需base_sha、head_sha、review_status和review_receipt。
支持JSON双引号、YAML单引号和无引号标量，不接受重复键。未知版本拒绝验收。

范围、验收和实证区域使用成对标记：

```markdown
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| :--- | :--- | :--- |
| `src/example.py` | MODIFIED | 任务职责 |
<!-- /iter:scope -->

<!-- iter:acceptance -->
- [ ] 明确行为及验证命令
<!-- /iter:acceptance -->

<!-- iter:ledger -->
执行命令、结果、独立审查和裁决记录。
<!-- /iter:ledger -->
```

旧卡范围表按语义标题识别，允许历史第4节与现有第5节；白名单只来自表格第一列，不取职责说明中的代码示例。
路径相对项目根目录，使用/；允许显式dir/目录授权，不支持glob，禁止绝对路径、..、仓库外路径与.git元数据。空/缺失名单拒绝范围检查。
默认隐式允许当前任务卡和所属迭代README；它们仍受冻结规格检查，不能借此偷改需求。

## 范围检查

旧调用保持检查BASE..HEAD已提交差异。提交前显式加--include-worktree，同时检查暂存、未暂存和未追踪文件。
可选--baseline-dirty传入启动时记录的JSON路径数组；结果单独列出preexisting_files，不把它们悄悄排除检查，也不宣称执行者已取得这些文件的修改权限。
检查器只读，不撤销任何文件。已存在的变更发生后续变化时仍需由主控核对归属，不能据路径清单推断作者。

## 完成收据

任务卡review_receipt指向项目内JSON。字段为：

```json
{
  "schema_version": 1,
  "task_id": "01",
  "type": "Strict-TDD",
  "task_path": "docs/todos/01-example/01-task.md",
  "base_sha": "完整提交引用",
  "head_sha": "被审实现提交C",
  "contract_sha": "冻结规格提交（C或C的祖先）",
  "implementer": "实现会话标识",
  "reviewer": "独立审查会话标识",
  "verdict": "APPROVED",
  "review_report": "docs/todos/01-example/evidence/01/review.txt",
  "checks": [
    {"name": "red", "kind": "command", "command": "python -m pytest ...", "cwd": ".", "exit_code": 1, "failure_kind": "assertion", "summary": "实际目标断言失败，非编译/环境错误", "output": "docs/todos/01-example/evidence/01/red.txt"}
  ]
}
```

示例省略其余必需检查，不能直接作为有效收据。完整提交引用必须由Git解析验证；不另建内容哈希体系。
implementer与reviewer必须不同，review_report和所有output必须存在、非空、在项目内。command检查有命令、项目内cwd和整数退出码；observation检查有可复查产物和summary。

按type必需的checks名称：

- Strict-TDD：red、green、regression。red必须非零、failure_kind=assertion；green/regression必须退出0，tdd_verified=true。
- UI-Component：interaction、states、visual、regression。states/visual是观测证据，其余为成功命令；必须覆盖正常/空/加载/错误及任务规定的实际视觉检查。
- Refactor-Benchmark：baseline、regression、compatibility、benchmark_before、benchmark_after。compatibility为观测，其余为成功命令；实测条件和数值写入对应原始输出。
- Spike-Discovery：experiment、decision、interfaces。experiment为成功命令，decision/interfaces为观测产物。不要求伪造RED或tdd_verified=true。

这些结构检查验证证据完整性与版本关系；测试是否真正证明目标、视觉质量是否合格及审查者独立性，由独立Reviewer阅读原始证据确认。工具不把字段声明当作完整语义验收。

验证范围按[共同协议](agent_protocol.md)分为开发内环、任务交付、迭代收口。新卡的regression写明受影响范围、命令与选择依据，迭代另保留全量回归；旧卡明确要求的全量门禁不被新模板自动替换。checks名称、kind、退出码及有效RED要求不变；补充测试是否经历RED如实标注。UI仍覆盖正常/空/加载/错误，具体可触发状态及视口在规划时说明，不靠换模板删既定要求。

正常检查点、证据复用说明使用现有正文/ledger。新流程按[执行检查与交接](execution_readiness.md)使用显式context和只读CLI，attempt归入既有autonomy_state.events；不新增卡片必填字段，不给旧调用增加前置条件。主控消费就绪结果并核实原始证据。冻结审查前完成正文记录，登记时遵守以下Git/FS各自合同。

## 审查后变化

Git审查绑定C和contract_sha，不绑定随后登记状态的提交D。允许更新固定执行元数据、复选框完成标记和ledger内容，其他任务卡正文及接口/范围/验收文字必须与冻结规格一致。FS不使用此正文豁免，见下方完整正文绑定。
所属迭代README的目标/全局约束区域也要与冻结版本一致。
实现后当前任务白名单内文件变化会使该收据失效；后续无关任务不使它无故失效。分支严格门禁另核对分支改动是否被有效DONE收据范围覆盖。
严格审查读取已提交且无未提交变更的候选；先提交实现，再生成包、独立审查并登记收据，提交状态与证据后检查。
原始证据不能只保存在待删除Worktree的私有.git目录。清理Worktree前保留到项目证据目录。

## 兼容与退出码

任务库存共用发现规则：数字前缀Markdown（兼容 `01.md` 和 `01-task.md`）或frontmatter显式含task_id/status的文件为任务卡；README和无任务元数据的辅助报告不计入。兼容无编号、只有status的旧卡；坏数字卡、空task_id/status或不可读文件仍进入审计，不能因格式错误静默漏检；正文示例不提供身份。

既有CLI和导入函数保留。范围/分支/规划门禁不通过为退出2，调用或打包失败为退出1，现有熔断退出3不变。
--local/全局sync默认只刷新投影并报告审计警告；使用--strict时发现失败/未知门禁返回非零。看板/README/Terminal分别显示声明DONE与实际验收PASS，不能将声明绿色替代严格验收。

## 进度与自治投影

业务阶段以成对iter:stages标记内复选清单为唯一真源，旧卡兼容语义标题。stage_current/stage_progress只推导，旧frontmatter同名值忽略；无清单UNKNOWN，声明DONE也不推断100%。工程清单使用iter:verification或旧语义标题，全部勾选不等于验收PASS。Ruling数不作重规划次数。预算事件与计数以autonomy_state为准，普通字段只兼容旧卡。进度比例是清单比例，不是工时估计。

README的iter:projection区域是可再生只读投影，不修改卡片；查询看板/API不写项目，--local/sync或--export-board为显式写入。服务只监听127.0.0.1，无通配CORS；原始证据入口只读卡中列出的项目内产物，不接收任意文件路径。

## 显式文件系统交付（当前审查，不迁造历史）

仅本地迭代检查支持显式文件系统收据：在实际 `<root>/docs/todos/<数字>-<非空名>/iteration-delivery.json` 写入 `{"schema_version":1,"mode":"filesystem"}`，精确键集仅为schema_version与mode，未知键也拒绝。没有配置沿用Git；配置存在但非法、越界或损坏时拒绝验收，不降级。默认Git、分支与全局的提交前提不豁免。看板列举证据及HTTP证据读取使用同一合法profile派生的项目根；非法profile不提供证据入口，不降级为Git根。

任务卡保持schema1及成对scope/acceptance/ledger标记，新增 `delivery_mode: filesystem`、非空 `candidate_id`；完成时仍需review_status APPROVED和review_receipt。文件系统收据必须明确 `receipt_kind: current-filesystem-review-v1`、`delivery_mode: filesystem`，task_id/type/task_path/candidate_id与卡精确一致，recorded_at为带时区ISO时间。实现者与审查者标识不同，报告与输出存在且非空。卡片和收据均不得带非空base_sha/head_sha/contract_sha；不得用占位SHA或当前审查冒充历史批准。

四类checks沿用上文名称及退出码要求。文件系统UI-Component的interaction另允许原生工具观测：kind为observation，并有非空source_tool、带时区observed_at、summary及非空output。该特例不适用于red、regression或其它command检查。Strict-TDD仍要求有效断言RED与tdd_verified=true。结构检查不代替Reviewer对原始输出、独立性和实际行为的判断。

收据另指向三个项目内文件：

- `candidate_manifest`：JSON含相同candidate_id、非空files数组，每项为 `{"path":"源项目相对路径","snapshot":"冻结项目相对路径"}`。源与快照按解析后的路径去重、两集合不交叠，逐字节比较。所有scope文件、目录内当前文件和check.output都要覆盖；仅注册的review_receipt/review_report可不作为目录源项。目录中新文件、缺文件、路径越界、别名重复或字节漂移使绑定失效。源不能超scope/check.output；manifest和快照放scope之外，避免递归冻结。
- `contract_snapshot`：冻结任务卡全文；FS专用比较保留parse_card得到的完整正文及去除MUTABLE_METADATA后的元数据。仅既定执行元数据可变；ledger、完成勾选和正文显示状态也必须与冻结内容相等，不能指向当前卡自身或其别名。上文Git的contract_projection动态正文合同不变。
- `goal_snapshot`：冻结所属迭代README全文；比较其目标/全局约束节与当前迭代README同节，缺节或漂移拒绝。不能指向当前README本身，也不读取项目根README替代。

先完成待审正文与真实原始证据并冻结候选，再由非参与者审查，最后登记当前时间收据及可变元数据；登记不能再改冻结正文。FS收据的implementer/reviewer必须非空、无首尾空白且不同；此校验不证明现实人员身份。历史用户例外只适用于其原范围，不自动豁免新收据字段或补足缺失原始证据。只有合法profile使 `--local --strict` 采用文件系统绑定而不要求Git提交；类型检查、验收清单和累计预算仍生效。它仍是结构与证据门禁，空库存的EMPTY/退出0不表示整轮完成，未完成卡也不会自动成为DONE。分支与全局strict遇到此profile拒绝放行，不能用文件系统收据替代其Git完成收据；普通非strict汇总仍可展示本地验收投影。

