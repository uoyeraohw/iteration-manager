# Agent Note: Worktree执行门禁不创造Git权限

Status: implemented

## Problem

Worktree合同仍要求初始化后强制暂存整个docs/todos、生成Prompt前补Commit，以及迭代验收后立即合流并销毁Worktree。正文与流程图均有这些指令，与共同协议的仅Prompt只读、精准提交和分项授权冲突。相邻手册把迭代目标称为最高权威，也可能使Ruling越过用户边界。

## Decision

Worktree正文、流程图、工程手册与根索引模板共同遵循现有共同协议：仅Prompt只交付预览；实际执行或创建Worktree前保留--verify-committed。没有提交权限时返回未提交计划及执行依赖，不补Commit。已有dirty按归属保留，目录边界不等于整目录写权；提交只包含获准归属文件并检查cached diff。

合流、推送、发布与清理分别需要授权。验收通过只说明候选满足门禁，不授予这些权限；未授权时保留Worktree与分支。任务卡及迭代README继续由唯一写者维护；本次实现者只返回证据。四预算、type必需证据和非参与者独审均保持原合同。

文本回归直接读取实际源文件，覆盖四场景预期及旧冲突语句，不用模拟会话生成通过结论。TypeSafe对该测试路径选择source_assertions；原始请求和响应见本卡evidence/01/typesafe-checkpoint-a.json。

## Alternatives considered

- 只在文首加授权声明：改动少，但旧的强制命令和流程图仍直接指导行动；本次同步修正正文、图与邻接入口。
- 模拟会话填写四场景PASS：便于自动化，但不能证明新会话实际消费；仅做源文本回归，原生消费由主控后续桥接。

## Existing-note audit

- [分层验证与检查点](2026-11-12-bounded-validation-workflow.md)：部分重叠，继续沿用type验证与跨会话证据复用，本篇修复相邻授权矛盾，不取代原决定。
- 有界自治、检查点续跑及workflow-consumption笔记的终态、预算和角色合同保持；其余现有记录属于部署、查询、FS或看板，无本次取代关系。不删除或归档历史。

## Testing

切片A运行真实文本回归及任务卡schema回归；命令、原始输出和退出码见implementation-checkpoint-a.json指向的runner收据。非TDD文档任务不补造RED。四类真实新会话消费尚未发生，authority-matrix的observed_result保持UNKNOWN；独立审查和整卡type证据仍由后续阶段完成。

## Consequences

可在授权范围内继续工作，同时不为生成Prompt制造提交副作用。代价是无Git权限时真正执行仍被规划提交门禁阻断，需授权持有人解决；静态测试只能锁定文字合同，原生工具行为仍须新会话观察与独审。
