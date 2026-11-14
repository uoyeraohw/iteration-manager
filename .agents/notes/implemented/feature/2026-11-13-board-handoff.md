# Agent Note: 看板区分当前候选与历史检查点

Status: implemented

## Problem

旧详情只显示BASE/C，FS的空SHA被呈现为未知Git候选；03已经提供交付模式和有效检查点，但页面没有展示可继承的原候选、出处和剩余工作。HTTP请求等待期间也没有加载反馈。

## Decision

详情按delivery_mode分支：Git显示BASE/C，FS只显示candidate_id，未知模式明确未知。历史检查点单独显示原候选、phase、summary、source与每项progress evidence，不能冒作当前候选。空remaining_work明确不代表完成。原文链接仍只枚举sources的task/source索引，不把检查点路径变成任意文件入口。

刷新提供按钮和可读的加载/连接状态，并防止慢请求重叠；原生dialog保留Escape关闭。保持现有深色布局，不重设计。真实浏览器由根在1139×869视口执行；模板单元DOM替身只证明文本分支，不充当真实输入、四态或视觉验收。

HTTP夹具复用真实LiveBoardHandler和generate_board_data。真实Git页读取本迭代；FS、空库存、延迟页明确标记synthetic。延迟发生于/api/board边界，停止通过独立stop-file或总时长正常shutdown；不改DOM/store，不创建TaskSpace。

默认入口保留真实Git页；单元测试显式传入`--isolated-fixtures`，四个服务的库存全部来自TemporaryDirectory，并将Git样例命名为synthetic_git、全部标记synthetic。ready生成仍调用真实查询，HTTP仍使用真实处理器，不模拟返回值。真实完成卡的审计成本随库存增长，不能成为生命周期测试的隐式输入；隔离模式在生成ready时禁止读取工作区库存，默认模式通过临时checkout核对原目录选择与real_git来源标记。

## Existing-note audit

- [可信投影](../architecture/2026-11-11-trustworthy-board.md)：部分重叠，沿用同源计数、sources安全边界与声明/验收分离。
- [查询接口](../architecture/2026-11-13-query-cli-contract.md)：部分重叠，仅消费03字段，不改变字段含义或源码。
- 其余预算、FS冻结与只读盘点决定未被替代。

## Alternatives considered

- 保留统一SHA区块：改动少，但FS没有Git候选，不能准确表达交付模式。TypeSafe选择模式分区，原请求/响应保存在本卡slice-a-typesafe.json。
- 合并当前候选与检查点候选：更紧凑，但检查点可能来自较早尝试，会丢失续接出处；分开保留。
- 增大ready超时：能容纳目前8.562秒的真实审计，但不能解除与持续增长库存的耦合；保留8秒断言，选择显式临时库存入口，不复制服务生命周期实现。取舍请求和TypeSafe响应见repair-final-typesafe-a.json。

## Testing

初始可执行模板测试取得4项真实断言失败、1项通过；不是ImportError。针对模板、精确计数与HTTP路由的内环13项通过；指定五文件回归67项通过，包含HTTP夹具生命周期测试。补充测试不声称先RED。当前Windows实测允许创建symlink，HTTP越界拒绝通过，未用skip充当通过。原始输出和退出码在本卡slice-a-* runner收据；最终检查与尚未执行的真实视觉/独审以implementation-checkpoint-a.json为准。

06最终全量的旧失败原件与8.562秒ready诊断均保留。返修新增隔离行为断言先在真实库存路径取得AssertionError（repair-final-red-isolation-a.json），最小隔离实现后测试通过（repair-final-green-isolation-a.json）；该轮为7项通过。默认参数兼容断言为后补，不声称经历RED。真实UI模板、查询/CLI和四态逻辑均未变，原04浏览器交互/截图继续沿用；本次只补测试隔离证据，不产生新的真实自用或独审批准。

## Consequences

用户能区分当前候选与可继承的历史工作，未知不被误解成完成。独立HTTP服务增加少量验收夹具维护成本，但不增加产品服务或查询契约。FS夹具仅用于合法profile、字段及证据入口展示，未声明独立APPROVED。正常/空/加载/断连的真实浏览器观测仍由根完成。
