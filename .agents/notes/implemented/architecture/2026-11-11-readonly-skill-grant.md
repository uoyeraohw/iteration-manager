# Agent Note: 精确工作区的主版本只读授权

Status: implemented

## Problem

真实业务链的Antigravity叶子不能读取主版本必读契约。主控可读不等于叶子可读；原生拒绝后换副本或shell不能建立合法消费证据。用户明确允许扩展授权通路。

## Decision

新增基于现有Python MCP SDK的stdio只读接口，主控持有逐项授权文件，每次请求校验精确真实cwd、主版本根和文件清单。接口仅提供read_skill_file，不提供写入或执行。使用打开句柄最终路径核对防止路径替换，限制文件及行范围；撤销即时生效。原生文件、企业终端和写根不变。注册、实际消费与独立验收分别取证，业务链保持独立门禁。

## Alternatives considered

- ACP additionalDirectories：标准机制且集成最少，但安装版本1.4.5同时扩大读取、client写入与企业终端范围，没有只读位，不符合最小授权。
- CODEG_ACP_FS_EXTRA_ROOTS：宿主已有环境入口，但同样扩大可写根，不作为只读授权。
- 修改vendor或Codeg：可实现更深的原生权限模型，但需要二进制重建和部署；现有MCP配置已支持新会话加载，当前单工作区需求无需该代价。

## Testing

stage09保存有效断言RED及后续单元/stdio日志。核心原文与安全拒绝12项先RED再GREEN；stdio和额外行范围/独立竞态用例为补充回归。首次stdio失败为测试哨兵与错误文案重合，改为独特私有内容哨兵，不将该失败算产品RED。实际代理读取与独立裁决以维护任务README为准。

Windows核心12项GREEN、补充后19项及全套91项回归通过。真实1555读取两份主版本并拒绝非清单路径，原生idx4/6/8保留；独立1556批准Windows权限通路。后续真实测试作者1560/1565使用同一受控通路；1565取得业务DONE/FUSED独立断言RED。业务链仍缺GREEN/C/独立C审查/D，1570裁决BLOCKED；权限通过不抹去预算和命令前截止核验缺口。Linux实现未取得本轮运行证据。

## Consequences

授权不扩大原生范围，但新增SDK依赖、配置项和授权撤销责任；服务仅支持Windows与具备/proc/self/fd的Linux。服务错误cwd必须修正启动方式而非扩大授权。授权文件与服务脚本不放在叶子可写范围。先不支持多工作区通配，未来需求变化重新审查模型。

既有[有界自治](../process/2026-11-11-bounded-autonomy.md)与[助手部署](../process/2026-11-11-assistant-deployment.md)部分重叠，保留其时间、独立审查和消费分层规则；现有看板及第一批证据笔记与本授权决定无关，不移动或重写。
