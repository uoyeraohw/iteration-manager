---
name: iteration-manager
description: >-
  全局敏捷迭代管理与分类型工程门禁。用于 /iter init、/iter next、/iter task、/iter sync，提供 docs/todos 单一真源、Worktree 隔离、TypeSafe 规划质检、持久化有界自治、原始证据与独立审查。
---

# Iteration Manager

## 入口、角色与授权

| 入口 | 用途 | 权威助手源 |
|---|---|---|
| `/iter init` | 规划、接管或重规划 | [Planner](templates/assistants/iteration_planner.md) |
| `/iter next` | 整轮调度和验收 | [Controller](templates/assistants/iteration_controller.md) |
| `/iter task` | 单卡执行和独审 | [Tech Lead](templates/assistants/task_tech_lead.md) |
| `/iter sync` | 实际 CLI 投影或检查 | [CLI](scripts/iter_sync.py) |

必读[共同执行协议](references/agent_protocol.md)和[任务卡契约](references/task_card_schema.md)：共同流程、授权、角色、预算和恢复以协议为准；生成的委派 Prompt 也消费该协议。仅生成 Prompt、评估或只读接管不授权实施、写文件或 Git 提交。Controller 不写业务代码，执行者最高 TESTING；独立 Reviewer 不参与同任务的实现、测试、设计或 RCA。工具能力以实际环境为准。

## 当前任务的真源与导航

从目标项目当前 Worktree 的 `docs/todos/<当前迭代>/README.md` 读取 `iter:goal` 和当前交接摘要，并按任务索引读取准确任务卡及其证据路径；用实际 CLI 的 `--render-envelope <任务卡>` 只读获取交接。直接查看所需原件，缺失或不可读时记录 UNKNOWN/缺口，不从历史迭代猜状态或默认加载历史全文。任务卡是需求、状态和事件真源，README 的投影和看板是展示；原始输出和独立收据证明实际事实。不要另建状态账。

状态 TODO → IN_PROGRESS → TESTING → DONE，FUSED 是异常阻塞，缺失或非法为 UNKNOWN；声明 DONE 不等于验收 PASS。完成收据、冻结规格和四种类型门禁以[任务卡契约](references/task_card_schema.md)为准：[Strict-TDD](templates/contracts/strict_tdd_contract.md)、[UI-Component](templates/contracts/ui_component_contract.md)、[Refactor-Benchmark](templates/contracts/refactor_benchmark_contract.md)、[Spike-Discovery](templates/contracts/spike_discovery_contract.md)。未评估的规划为 UNASSESSED，实际 TypeSafe 门禁见[指南](references/typesafe_eval_guide.md)。

Git 交付的 Worktree、C/D 与分支门禁见 [Worktree 契约](references/worktree_git_contract.md)；显式 filesystem 交付的 profile、快照和本地收据见[任务卡契约](references/task_card_schema.md)。坏配置不降级，FS 本地 strict 不替代 Git 分支或全局门禁。源码、独审、安装、真实消费与业务验收分别核实；合流、推送、部署和清理分别授权。

## 工具和资源路由

从目标项目根以实际 skill 根和约定的冻结版本运行 [iter_sync.py](scripts/iter_sync.py)；`--help` 给出实际 CLI 参数。只读定位可用 `--takeover-report`、`--inventory`、`--preflight`、`--dispatch-check`、`--render-envelope`、`--execution-report`；`--local` 和根同步会写投影，`--dry-run` 才只读。就绪与交接见[执行检查](references/execution_readiness.md)，正式命令和恢复见[截止入口](references/checkpoint_execution.md)。

- [任务卡模板](templates/task_detail.md)、[迭代索引模板](templates/iteration_readme.md)、[根索引模板](templates/root_readme.md)、[结构化生成](references/template_generation.md)
- [Implementer](templates/sdd_implementer_prompt.md)、[Reviewer](templates/sdd_reviewer_prompt.md)、[会诊](templates/consilium_rca_prompt.md)
- [发布证据索引](references/release_status.md)、[微观工程手册](references/superpowers_handbook.md)
