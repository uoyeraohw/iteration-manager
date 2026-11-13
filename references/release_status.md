# 发布证据索引：先区分四层事实

查源码位置看第一层，查批准范围看第二层，查实际落盘看第三层，查谁使用了什么看第四层。此处是有日期的证据入口，不维护任务状态；当前进度、05最终登记D和整轮裁决仍以[迭代记录](../docs/todos/10-self-hosting-hardening/README.md)及任务卡为准。

## 字段与读取规则

- `source_commit`：证据对应或比较的源码提交；安装行仅表示比较参照，不是安装版本声明。
- `reviewed_candidate`：原批准绑定的C或历史候选名，不把登记D当C。
- `install_target`：实际安装根；没有安装事实时为UNKNOWN。
- `observed_version`：可归属的实际版本；无标签或无法完整归属时UNKNOWN，不新造摘要。
- `consumer_evidence`：实际消费证据或UNKNOWN；测试夹具不等于原生自用，文件相等不等于新会话采用。
- `checked_at`：本次观察或原历史验收的UTC时间；历史捕获时间另见原件清单。
- `evidence_scope` / `result`：事实的覆盖边界与结果，不外推整轮、安装或外部业务通过。
- `source_pointer`：可复查原件或原生记录指针。复制品保留原字节；[捕获清单](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-observation.json)记录原绝对来源、捕获时间与范围，不能仅靠克隆恢复未捕获的main/build历史材料。

路径简称：Codeg=`C:/Users/qingyu/.codeg/skills/iteration-manager`（维护main），Codex=`C:/Users/qingyu/.codex/skills/iteration-manager`，Gemini=`C:/Users/qingyu/.gemini/config/skills/iteration-manager`；iter10为Codeg下`.worktrees/iter-10`。下表日期均为UTC。

## 一、源码：main与工作候选分开

| source_commit | reviewed_candidate | install_target | observed_version | consumer_evidence | checked_at | evidence_scope | result | source_pointer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| d3bd97ab16ffed6104034a887a01eb1b4d75dc0e | UNKNOWN | Codeg | UNKNOWN | UNKNOWN | 2026-11-13T18:33:45Z | main维护源HEAD；非iter10部署 | OBSERVED；无版本标签 | [现场观察](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-observation.json) |
| 8392193a0d9e883892f75780a63a1b16f67682c4 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 2026-11-13T18:33:45Z | iter10本次实施前固定基线；不包含05未来C/D | OBSERVED；整轮总审尚未产生 | [现场观察](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-observation.json) |

## 二、已审候选：仅原卡范围

以下收据在上述iter10基线读取；逐卡APPROVED不能替代整轮总审，也不表示安装了这些提交。

| source_commit | reviewed_candidate | install_target | observed_version | consumer_evidence | checked_at | evidence_scope | result | source_pointer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8392193a0d9e883892f75780a63a1b16f67682c4 | 997ee3753241d7f4ad5b3d68df7648d06e2adc4c | UNKNOWN | UNKNOWN | 01只读场景消费 | 2026-11-13T18:33:45Z | 01授权规则；原收据及报告范围 | APPROVED（原收据） | [01 review](../docs/todos/10-self-hosting-hardening/evidence/01/review.json) |
| 8392193a0d9e883892f75780a63a1b16f67682c4 | 03950f2ac4867291c3001daa10140e4da1efa81f | UNKNOWN | UNKNOWN | 02实现原生记录 | 2026-11-13T18:33:45Z | 02生成契约；Git/FS夹具不是业务验收 | APPROVED（原收据） | [02 review](../docs/todos/10-self-hosting-hardening/evidence/02/review.json) |
| 8392193a0d9e883892f75780a63a1b16f67682c4 | 542f2b445f499b3a2e90d92a6ed6bba20cdb1bdb | UNKNOWN | UNKNOWN | 03实现原生记录 | 2026-11-13T18:33:45Z | 03查询/CLI；170项原回归 | APPROVED（原收据） | [03 review](../docs/todos/10-self-hosting-hardening/evidence/03/review.json) |
| 8392193a0d9e883892f75780a63a1b16f67682c4 | 9b9010afb8dbf0b0cf74f83c6c97605984319619 | UNKNOWN | UNKNOWN | 04原生浏览器记录 | 2026-11-13T18:33:45Z | 04桌面Git/FS展示；FS为隔离样例 | APPROVED（原收据） | [04 review](../docs/todos/10-self-hosting-hardening/evidence/04/review.json) |

## 三、安装：只读落盘观察不等于完整版本

本次只读历史manifest列出的58条路径，加命名入口；不递归扫描安装目录。三根58/58与main相等、45/58与iter10基线相等、36/58与历史部署冻结源相等。`scripts/iter_sync.py`不同于iter10；`scripts/iter_templates.py`、`scripts/iter_queries.py`、`scripts/iter_cli.py`、`references/template_generation.md`均不存在。首次实验误写单数`iter_query.py`，原件不改，[补充实测](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-entry-observation.json)核对实际复数入口、CLI及无标签事实。没有把历史清单冒充当前完整交付清单。58路径比较在05修改SKILL之前完成；入口补测时间为2026-11-13T18:36:33Z。

| source_commit | reviewed_candidate | install_target | observed_version | consumer_evidence | checked_at | evidence_scope | result | source_pointer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| d3bd97ab16ffed6104034a887a01eb1b4d75dc0e | UNKNOWN | Codeg | UNKNOWN | UNKNOWN | 2026-11-13T18:33:45Z | 历史58路径及5入口；维护源不是iter10已部署 | OBSERVED；完整版本UNKNOWN | [逐文件比较](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-observation.json) |
| d3bd97ab16ffed6104034a887a01eb1b4d75dc0e | UNKNOWN | Codex | UNKNOWN | UNKNOWN | 2026-11-13T18:33:45Z | 历史58路径及5入口；未测安装新会话采用 | OBSERVED；完整版本UNKNOWN | [逐文件比较](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-observation.json) |
| d3bd97ab16ffed6104034a887a01eb1b4d75dc0e | UNKNOWN | Gemini | UNKNOWN | UNKNOWN | 2026-11-13T18:33:45Z | 历史58路径及5入口；未测安装新会话采用 | OBSERVED；完整版本UNKNOWN | [逐文件比较](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-observation.json) |
| d29ddc2b5858dbc22239469a552493eae6142ca2 | SC-FS-I01-20261112-R7 | Codeg/Codex/Gemini | 历史Git初始化交付 | UNKNOWN | 2026-11-12T12:16:41.568418Z | 当时三份58文件相等、205tests、无push；不是当前等同性 | HISTORICAL COMPLETED | [原始收据捕获](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-original-git-final.json) |

## 四、实际消费：真实Git自用与合成FS分列

这些是既有记录的索引，本次不重跑旧外部业务。原生终态仅证明执行会话记录存在，批准仍须结合各review中的原始checks与独立报告。原生切片可能早于最终C，列出的reviewed_candidate取原review绑定，不把会话自报SHA当最终C；01所链切片为deadline canceled，02—04所链切片为completed（见补充实测），均不是单凭终态批准。

| source_commit | reviewed_candidate | install_target | observed_version | consumer_evidence | checked_at | evidence_scope | result | source_pointer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 997ee3753241d7f4ad5b3d68df7648d06e2adc4c | 997ee3753241d7f4ad5b3d68df7648d06e2adc4c | UNKNOWN | UNKNOWN | 01原生实现终态及只读消费 | 2026-11-13T18:33:45Z | 真实Git自用；只读场景消费范围见review | RECORDED；非安装消费 | [原生记录](../docs/todos/10-self-hosting-hardening/evidence/01/native-terminal-implementation-b.json) |
| 03950f2ac4867291c3001daa10140e4da1efa81f | 03950f2ac4867291c3001daa10140e4da1efa81f | UNKNOWN | UNKNOWN | 02原生实现终态 | 2026-11-13T18:33:45Z | 真实Git任务；FS生成/冻结测试为合成夹具 | RECORDED；非安装消费 | [原生记录](../docs/todos/10-self-hosting-hardening/evidence/02/native-terminal-c.json) |
| 542f2b445f499b3a2e90d92a6ed6bba20cdb1bdb | 542f2b445f499b3a2e90d92a6ed6bba20cdb1bdb | UNKNOWN | UNKNOWN | 03原生实现终态 | 2026-11-13T18:33:45Z | 真实Git任务；查询隔离夹具不外推业务 | RECORDED；非安装消费 | [原生记录](../docs/todos/10-self-hosting-hardening/evidence/03/native-terminal-c.json) |
| 9b9010afb8dbf0b0cf74f83c6c97605984319619 | 9b9010afb8dbf0b0cf74f83c6c97605984319619 | UNKNOWN | UNKNOWN | 04原生实现终态及浏览器checks | 2026-11-13T18:33:45Z | 真实Git自用/桌面UI；FS为隔离样例 | RECORDED；非安装消费 | [原生记录](../docs/todos/10-self-hosting-hardening/evidence/04/native-terminal-a.json) |
| UNKNOWN | I01-current-FS-20261112-R7-core-v2 / replay-04-07-v2 | 当时三安装 | SC-FS-I01-20261112-R7 | R7本地Mock/FS七卡迁移及收尾 | 2026-11-12T10:12:51.023029Z | 历史7/7；排除Git全分支、真实提供商、全媒体、生产发布 | CLOSED_LOCAL_MOCK_FS（历史） | [完整验收原件捕获](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-original-r7-acceptance.md) |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P1隔离inventory样例 | 2026-11-13T18:33:45Z | README声明当批只改维护源；FS PASS为合成，不推断当前部署 | HISTORICAL；deployment.json缺失 | [P1 README原件捕获](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-original-p1-readme.md) |

## UNKNOWN由谁补齐

- 安装的完整版本、对应reviewed_candidate及新会话消费：部署owner在另获授权的部署阶段，以完整当前交付manifest、版本归属及原生新会话证据补齐；05不执行部署或改配置。
- 仅有历史候选名而无Git来源、P1 deployment.json缺失：历史证据owner提供原始来源或确认不可恢复；不补造SHA，也不因缺文件重开旧业务。
- 表中不涉及安装/消费的源码和单卡记录，其UNKNOWN由相应操作owner在该操作实际发生后补齐，不是本卡新增前置条件。
- 05独立审查、登记D、整轮总审与strict：主控在任务记录登记；本索引不预写本轮PASS，不填自身最终SHA。

结构与指针检查见`tests/test_release_index.py`，它不核准事实或替代独立审查；字段观测契约见[interfaces](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-interfaces.json)，分类依据见[decision](../docs/todos/10-self-hosting-hardening/evidence/05/slice-a-decision.json)。
