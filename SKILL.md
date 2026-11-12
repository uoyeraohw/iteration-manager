---
name: iteration-manager
description: >-
  全局敏捷迭代管理与分类型工程门禁。用于 /iter init、/iter next、/iter task、/iter sync，提供 docs/todos 单一真源、Worktree 隔离、TypeSafe 规划质检、持久化有界自治、原始证据与独立审查。
---

# Iteration Manager

维护主版本为 `.codeg/skills/iteration-manager`；`.codex` 与 `.gemini/config` 是真实独立副本，整轮验收和部署完成后同步同一候选。三个助手的权威指令在 `templates/assistants/`；配置落盘、新会话实际消费和副本同步分别验收，不能互相替代。

## 先选入口与授权

| 入口 | 行为 | 权威助手源 |
|---|---|---|
| `/iter init` | 新建、接管或重规划，按授权写计划/提交 | [Planner](templates/assistants/iteration_planner.md) |
| `/iter next` | 整轮依赖调度、恢复、独立整体验收 | [Controller](templates/assistants/iteration_controller.md) |
| `/iter task` | 单任务编排、分类型验证与独立审查 | [Tech Lead](templates/assistants/task_tech_lead.md) |
| `/iter sync` | 只按实际命令更新投影或执行检查 | [CLI](scripts/iter_sync.py) |

三个助手与生成的新窗口Prompt都使用 [共同执行协议](references/agent_protocol.md)，禁止重新嵌入另一套调度/修复循环。生成Prompt时保留三段：角色/授权/基线 → 任务卡/接口/依赖/类型契约 → 验收/证据/恢复/最高状态。工具名称以当前环境schema为准，不假定固定嵌套能力或并发容量。

**仅生成Prompt、评估或只读接管不授权实施、写文件或Git提交。** 可给标明执行前门禁的预览；实际执行前再校验基线。主控不写业务代码，但可以读取冻结Diff、运行独立验收。单任务执行者最高TESTING，同任务的测试作者、实现者及RCA/设计参与者不能独立对审。

## 真源与文件拓扑

```text
docs/todos/
├── README.md                     # 根总控，特性分支Zero-Root-Touch只读
└── 01-迭代名称/                   # 1 Worktree = 1 Iteration
    ├── README.md                 # 目标、约束、Review Focus、聚合投影
    ├── 01-任务.md                # 需求、接口、范围、验收、执行账本与自治事件
    └── evidence/01/              # 原始输出、独立报告、JSON收据
```

不并行维护 `.superpowers/sdd/` 或另一套任务状态。项目决定理由留在项目自己的 `.agents/notes/`，任务状态仍归docs/todos。分支只读写当前Worktree的卡片及索引，不回写主仓库副本。

## 规划与初始化

1. 读取需求、项目约定及实际cwd/分支/完整HEAD/dirty；明确写文件和Git权限。
2. 新建按单一职责拆解，锁定Consumes/Produces精确签名及依赖；每卡按type设计可验证阶段，迭代README记录Global Constraints与3—5项Review Focus。
3. 接管先 `--takeover-report`只读报告，保留历史Commit/状态/证据。缺失证据保持UNKNOWN，授权后才能迁移格式或补验。重规划登记具体Ruling与预算事件，普通裁决不自动计重规划。
4. 按 [TypeSafe指南](references/typesafe_eval_guide.md) 实际evaluate，权重30/30/20/20，总分≥80且单项≥70。未评估UNASSESSED；低分先针对具体缺口改进，不用默认85或自造评分。
5. 写入已授权的三级模板，依据type替换验证步骤。仅在相应授权下维护.gitignore的.worktrees/规则、同步根索引及精准提交本次归属文件；检查cached diff，不提交他人dirty。
6. 实际创建Worktree前运行 `--verify-committed`；非零读取诊断，Git失败不视为已提交。没有Git提交权限时交付未提交计划和明确执行依赖，不越权补提交。

## 执行与验收

四态：TODO → IN_PROGRESS → TESTING → DONE；FUSED为异常阻塞，不是第五种成功状态。缺失/非法状态UNKNOWN，不能从正文猜测。声明DONE和验收PASS分别核对。

1. 按 [Worktree契约](references/worktree_git_contract.md) 核对 `.worktrees/iter-{XX}` 与 `feat/iter-{XX}-*`、基线、dirty归属、规划提交和约定基线检查。
2. 按type执行真实验证；领取唯一卡片写者，实际使用环境支持的委派工具并记录task_id、时限及检查点。无下级工具时由有能力的上层串行桥接，不伪造派发。
3. 失败按持久预算处理：默认单轮5、累计10、会诊1、重规划2；重启/重复回收不清零。第5次失败后停止修复，预算内诊断/重规划；达累计或其它上限保存成果、证据、具体BLOCKED及恢复条件。不自动方案A，不扩大授权。
4. 完成实现C及原始证据后，派非参与者独立审查冻结规格、C和真实证据。测试作者/实现者/RCA参与者均不能自审。停止、completed、exit0或格式检查不等于产品验收。
5. 独立APPROVED后登记JSON收据、报告和DONE，head_sha绑定C，再提交登记D并运行 `--local --strict`。代码/测试/原始证据/冻结规格变化重审受影响内容；纯登记和后续无关任务不无故推翻旧审查。
6. 全部任务验收PASS后独立全分支总审与 `--check-branch --strict`，完整汇总Rulings、Deferred Minors及真实缺口。合主干、推远端、发布和清理Worktree按各自授权，不自动执行。

预算字段、事件幂等、恢复查询及真实工具调用见 [共同协议](references/agent_protocol.md)；所有收据/按type门禁见 [任务卡契约](references/task_card_schema.md)。会诊只提供建议，不产生APPROVED。旧DONE缺收据UNKNOWN，不补造历史红绿或批准。

获准文件快照交付时，可按任务卡契约显式启用迭代内 `iteration-delivery.json` 的 filesystem 模式；本地strict核对当前收据、源码/证据快照、冻结任务规格及迭代目标。缺/坏配置不作宽松降级，不自动迁造旧收据，预算与类型门禁不变；分支及全局Git提交前提不因此豁免。

业务/测试/验收统一使用[截止入口](references/checkpoint_execution.md)`scripts/iter_run.py`保存同调用核验和原始证据；时间中断可在主控显式单次授权下`resume-checkpoint`续跑，不改变四预算或旧recover。源码验收、模板部署、真实消费和业务整链分开记录。

## CLI：从对应项目根目录运行

用实际安装路径替换 `<skill_root>`，不要假定当前目录是Skill根。

```powershell
python <skill_root>/scripts/iter_sync.py --verify-committed [仓库路径]
python <skill_root>/scripts/iter_sync.py --takeover-report <迭代目录>
python <skill_root>/scripts/iter_sync.py --render-envelope <任务卡> [仓库路径]
python <skill_root>/scripts/iter_sync.py --check-scope <BASE> <C> <任务卡> --include-worktree
python <skill_root>/scripts/iter_sync.py --review-pkg <BASE> <C> [任务ID] [仓库路径]
python <skill_root>/scripts/iter_sync.py --local --strict [迭代目录或Worktree]
python <skill_root>/scripts/iter_sync.py --check-branch --strict [仓库路径] [基准分支]
python <skill_root>/scripts/iter_sync.py [主干工作区路径]
```

范围检查包括暂存/未暂存/未追踪，`--baseline-dirty <JSON路径数组文件>`只提示归属，不豁免。检查器只读不回滚。根同步有特性分支保护；`--local`只刷新所属迭代。默认同步报告警告，strict失败/UNKNOWN返回非零。查看看板用 `--board` 或 `--serve-board`，显式导出用 `--export-board`；显示投影不能替代证据验收。

## 资源

- [任务卡模板](templates/task_detail.md)、[迭代索引](templates/iteration_readme.md)、[根索引](templates/root_readme.md)
- [Implementer委派](templates/sdd_implementer_prompt.md)、[Reviewer委派](templates/sdd_reviewer_prompt.md)、[会诊](templates/consilium_rca_prompt.md)
- 类型契约：[Strict-TDD](templates/contracts/strict_tdd_contract.md)、[UI](templates/contracts/ui_component_contract.md)、[重构](templates/contracts/refactor_benchmark_contract.md)、[Spike](templates/contracts/spike_discovery_contract.md)
- [微观工程手册](references/superpowers_handbook.md)、[Worktree契约](references/worktree_git_contract.md)

维护Skill本身时，在Skill根运行 `python -B -m pytest -p no:cacheprovider tests -q`。实际代理行为和浏览器/部署证据按对应阶段另验，静态文本检查不代替运行。
