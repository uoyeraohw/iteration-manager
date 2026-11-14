# Agent Note: 发布事实按源码、候选、安装与消费分层索引

Status: implemented

## Problem

维护main、特性分支已审C、独立安装副本和原生消费各有不同证据。历史三副本同步、R7本地Mock/FS七卡关闭及P1源码增量不能用来断言iter10当前部署或整轮通过。

## Decision

`references/release_status.md`采用四层事实表，各行保留来源提交、已审候选、安装目标、观测版本、消费证据、时间、范围、结果与来源指针。无法归属时写UNKNOWN并附补齐owner和条件；05最终D和整轮结论仍只在任务记录登记，不制造自引用SHA。

安装核验只读取历史manifest的58条显式路径和命名入口，逐字节比较，不计算新摘要。首次实验查询入口误写单数，补测实际`iter_queries.py`和CLI，保留原件及纠正记录。58/58等于main只是有限清单事实，不是完整当前版本证明；TypeSafe实际分类选择bounded，原请求/响应留在本卡证据。

main/build不随Worktree，少量历史原件以完整原字节捕获，另记原绝对路径、时间、范围；未捕获来源仍保留原指针，不把转述叫原件。结构测试只验证字段和链接，不替代事实核查。

### 既有决定检索

与[Git主版本与副本同步](2026-11-12-canonical-git-repository.md)、[助手配置与消费](2026-11-11-assistant-deployment.md)部分重叠：保留它们的部署授权、白名单与原生采用契约；本决定只新增证据索引，不取代或归档旧决定。其它命中为授权、查询、FS和盘点决定，不被本次取代。

## Alternatives considered

- 直接沿用历史58文件同步收据作为当前版本：来源清楚、读取少，但不能覆盖后续源码和真实当前部署，故保留为历史行并实测当前白名单。
- 把四层归并成一项发布状态：查询简短，但会把单卡APPROVED、main维护和安装消费互相替代，故采用有日期、有范围的分层事实表。

## Testing

成功experiment及逐文件原始观察、分类decision、字段interfaces和定向测试均在`docs/todos/10-self-hosting-hardening/evidence/05/slice-a-*`。新增测试属于Spike结构检查，没有声称TDD RED。Note执行实际Skill的tree/format校验；独立审查与strict由主控后续执行。

## Consequences

维护者可直接定位批准、安装与消费各自证据；代价是索引保留长提交引用和时间边界，不能自动跟随状态投影更新。安装完整版本、新会话消费及缺失P1 deployment原件仍需对应owner在授权阶段补齐，不阻止发布事实索引如实交付UNKNOWN。
