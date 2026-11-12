# 检查点续跑与统一命令入口

## 从冻结检查点继续，不消费重规划

旧 recover 只登记查询终态，不解除阻断。执行时间中断、已有可继承成果且原生会话和命令终态均已核实后，主控可根据本次明确授权签发外部 JSON 能力文件；叶子不得签发、延长或改写它。宿主须将该文件保留在叶子写范围之外。

从精确 Worktree 根运行：

```powershell
python <skill_root>/scripts/iter_sync.py --autonomy resume-checkpoint <卡片> --event-id <稳定ID> --owner <新主管> --resume-grant <外部授权绝对路径>
```

这是协调元数据动作，不是业务命令；在它之前不得启动新业务写者或创建未提交的运行证据。成功取得唯一写者并进入 IN_PROGRESS；原四计数和旧事件不变。旧 claim/fix、recover 不变。

授权基础字段严格为：`version:1`、稳定非空 `grant_id`、真实绝对 `workspace`、项目相对 `card`、完整当前 `head`、已审查且为 HEAD 祖先的 `checkpoint_sha`、最近 `closeout_event_id`、项目相对 `terminal_evidence`、明确 UTC `expires_at`；可另有项目相对 `interruption_review`，其余字段拒绝。终态和中断审查文件从绑定HEAD的Git blob读取，必须已提交，不能以ignored/untracked文件冒充，结构为：

```json
{"version":1,"sessions":[{"id":"实际原生会话ID","status":"canceled","source":"原始来源指针"}],"commands":[{"id":"实际原生命令ID","status":"completed","exit_code":1,"source":"原始输出指针"}]}
```

例子只说明形状，不能作为真实授权或执行证据。会话接受 completed/failed/canceled，命令必须已观察到 completed 和整数退出码。source 由主控及独立 Reviewer 对照原生记录核实，非空字符串不能自行证明真实性。

旧closeout若未采用标准`execution deadline`原因，不改写历史事件、不靠“interrupted”等关键词猜测。须由非参与者对照原生截止守卫、取消/命令终态及元数据收尾报告，独立确认属于执行时间中断；主控才可在grant中绑定其已提交的`interruption_review`。该JSON严格为`version:1,kind:"execution-deadline",verdict:"APPROVED",closeout_event_id,blocked_reason,reviewer_session,source`；reason必须同时精确匹配当前阻断与最近closeout输入。未知/被拒审查、错误绑定及真实预算熔断仍拒绝。该分类不豁免旧命令截止缺口或业务GREEN/审查门禁，来源真实性仍须人工/代理原始证据审查。

只允许干净 FUSED、writer 为空、execution deadline 中断。round/total 达上限、实际会诊/重规划预算熔断、unknown/running、错误 cwd/卡/HEAD、过期、重复 grant 或重复 closeout 均拒绝且不改卡。replan 已成功使用到2不等于“第3次被拒绝”的熔断，不能因此误杀合法时间中断。续跑次数从成功事件派生，独立固定上限3，不增加原预算、不新增可调 policy。相同事件和完整入参重放只返回旧结果（包括授权事后过期），不会再消费；新事件不能重用旧能力。

## 每个业务、测试和验收命令都走同一入口

主控/主管给每个叶子确切 `command_deadline`，不得晚于叶子取消点；为父级查询留余量。Windows 从授权项目根执行：

```powershell
python <skill_root>/scripts/iter_run.py --deadline <明确UTC> --evidence <项目相对唯一阶段名.json> -- python -B -m pytest -p no:cacheprovider tests -q
$code=$LASTEXITCODE; exit $code
```

argv 直接传递，shell=False；不得把整串 shell 文本当 argv 或用外层 exit0 代替业务结果。协调性的原生查询、只读检查、领取/释放/收尾及精准 Git 提交不需要包装，避免把 receipt 的最终写入误提交成已完成记录。

入口排他保留 receipt 和 `.output.txt`，引导进程另写 `.child.json`；已有文件不覆盖。启动前同调用核 UTC，剩余不足5秒不启动；业务在 deadline 前5秒停止等待，余量用于回收。Windows Job Object 在开启启动门闩前接管引导进程，目标及后代继承容器；正常根进程提前退出也回收后代，只有 ActiveProcesses=0 才登记 tree_terminal。Job 不可用则不启动目标，不改用 taskkill 或另一执行通路。当前实现仅支持 Windows，其他系统启动前明确拒绝。

receipt 分别保存 argv/cwd、核验/起止 UTC、原始输出、实际业务 raw_exit_code、launcher_exit_code 和状态。COMPLETED 才可按业务退出码判断；TIMED_OUT/NOT_STARTED 返回124，CLEANUP_UNKNOWN/ERROR返回125。业务本身也可能退出124/125，必须看 receipt 状态。强杀时拿不到业务退出码则保留 null，不把 launcher 被杀码当断言失败。RUNNING/不完整记录和外层会话 cancelled 不能证明命令已终态。

时间中断仍须 closeout 保留 FUSED 并释放写者；正常切片完成可 release，保留 IN_PROGRESS/TESTING。新会话继承有效 RED、C 和审查成果，不把中断伪装成阶段成功。源码、部署、实际消费和业务整链各自验收，整链未通过不发布副本。
