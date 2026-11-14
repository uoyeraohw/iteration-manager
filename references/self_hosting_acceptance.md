# 真实自用验收：先分证据层，再连接原始链

本方法用于Skill管理自身迭代。任务卡仍是状态真源，报告只索引证据；READY、completed、命令退出0、独审APPROVED及strict PASS各有不同含义。

## 一条链保留每个身份

按真实任务追踪 inventory → claim → 同owner dispatch-check → 原生委派 → runner原始命令收据 → attempt → release → 独审 → 实现C/登记D → 冻结协调器strict。inventory可能因其它卡阻断，必须读取目标卡条目，不能只看整轮顶层结果。

- inventory/context保存观察时的candidate、phase、授权来源和依赖；claim事件与dispatch owner必须一致。
- 原生记录保存task/session身份及终态；runner另核对status、raw_exit_code、tree_terminal和原始输出。completed不代替命令或批准。
- attempt保留旧candidate及真实剩余项，release后handoff保留检查点。下一会话context应显式引用前序产物；不因换会话重跑有效RED或清预算。
- 独审读取实际C和冻结契约；实现/测试/设计参与者不能独审。登记D不冒充C；新候选需要受影响重审及新绑定。
- strict用冻结协调器，不用候选检查器给自己批准。只读复核可用`--local --strict --dry-run`，保留runner原件，不刷新主控投影。

## 三层分别报告

| layer | 能证明的内容 | 不能推出的结论 |
| --- | --- | --- |
| static | 已读契约、原始证据路径、候选和角色引用 | 测试实际运行或真实委派 |
| synthetic | 隔离临时项目真实CLI/函数行为与负例拦截 | 原生跨会话、真实用户项目验收 |
| native-self-use | 本轮真实委派、检查点、原始runner、独审与登记 | 已部署、完整安装、新安装会话消费或外部业务PASS |

报告固定为`version,candidate,coordinator_commit,cases[{id,layer,expected,observed,result,evidence}],unverified`。candidate只写已观察提交；报告产生后的提交在交接中另列，不自引用未来SHA。result只用PASS/FAIL/UNKNOWN/BLOCKED；未跑全量保持UNKNOWN并明确主控责任。

## 隔离测试组合成熟夹具，不复制整套测试

`tests/test_self_hosting.py`直接复用`test_execution_readiness.fixture/cli/inventory/report/save`、`test_filesystem_delivery_controller.fixture`和现有临时Git worktree夹具。新断言锁定inventory、dispatch、事件持久化、envelope、audit及board之间的一致性：缺授权/context、foreign writer、candidate/phase不符、依赖未PASS、两次无进展拒第三次、幂等/改payload拒、坏数字卡/未知DONE、FS源码/证据/正文漂移、特性分支根同步拒绝且字节不变。

runner/守卫unknown与超时、5/10/1/2预算、受控resume和FS拒Git grant沿用已有`test_iter_run.py`、`test_deadline_watch.py`、`test_autonomy.py`、`test_checkpoint_resume.py`等测试定义，由主控在最终候选全量运行。测试定义存在不是本次执行通过；不损坏真实卡制造超时，不在叶子窗口启动已知不能完成的全量。

## 本轮可复用结论

任务06的`evidence/06/native-chain-inventory.json`逐层保留01—05卡/收据、03 A/B/C身份、candidate、终态和原路径。03 A取得旧入口有效RED，B继承后GREEN，C继承A/B及裁决后完成CLI和after；before/after原样保留，after略慢，不宣称提速。

04真实浏览器、67项回归、截图及正常/空/加载/断连观察保留原路径；06未修改看板产品，沿用，不重跑浏览器。05登记正文漂移的strict拒绝属于正确拦截，随后定点独审绑定dc5d868，旧/新报告及收据全部保留。完整安装与外部用户业务仍UNKNOWN。

本检查点只交付隔离测试、原始证据清单、方法和Note及定向GREEN。主控负责最终候选全量、候选与冻结工具交叉核验、范围核验、非参与者独审和后续C/D/strict；最高TESTING。
