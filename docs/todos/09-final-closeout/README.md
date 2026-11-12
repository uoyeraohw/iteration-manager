# iteration-manager 技能交付收尾

状态：**Codeg主版本已初始化Git main；Codex/Gemini已实际覆盖更新。** 初始基线提交及最终核验结果记录于本次证据目录的 `final-receipt.json`。

## 已完成的交付

- 原计划阶段0—4已分批验收：见[第一批](../01-stage01-gate-repair/README.md)、[第二批](../02-bounded-autonomy/README.md)、[第三批](../03-trustworthy-board-and-deployment/README.md)。
- 后续主控链、受控检查点、AIMovie发现兼容及R7文件系统收据返修按各自记录验收，不回写旧候选状态。当前工具候选为 `SC-FS-I01-20261112-R7`。
- 2026-11-12直接核对三个真实独立目录：`.codeg/skills/iteration-manager`、`.codex/skills/iteration-manager`、`.gemini/config/skills/iteration-manager`。每处原57份活动交付文件全部等于批准的R7冻结候选，无缺失或内容差异；加上新增Git基线决定记录，当前交付清单为58份。
- 本次Git初始化后完整工具回归 **205 passed**，退出0；三个实际 `scripts/iter_sync.py --help` 入口均退出0，9份决定记录tree/format及0份archived校验通过。工具源码、模板、测试和合同未改，原独立审查继续有效；未重跑AIMovie业务或媒体验收。
- 首次收尾核对时两个技能库已是目标版本，因此当时未重复覆盖。用户随后明确授权Git初始化和覆盖更新，本次已实际覆盖两库各57份文件并各新增1份Git基线决定记录，三个安装各58份交付文件一致。Gemini的 `scripts/iter_sync.py.bak` 按既有排除规则原位保留。
- 根维护索引已纠正过期的“R5未通过”和candidate09当前状态描述；早期失败、收据、冻结及预算均未改写。

## 当前Git基线与同步

用户已明确授权在 `.codeg/skills/iteration-manager` 执行Git初始化。该目录是唯一源码仓库，分支为 `main`；现有源码、模板、测试、决定及维护任务纳入初始基线。`.gitignore` 排除build、运行证据、工作树、缓存及历史备份；原材料继续留在本机，不追造过去的提交或合并历史。

Codex/Gemini继续作为独立安装目录，不复制 `.git`、`.gitignore` 或维护任务。覆盖前已备份两库各57份原文件，并对新增决定记录保留“原本不存在”的恢复信息；只覆盖明确清单，不删除目标独有历史备份。

这次建立的是新的main初始基线，不存在旧特性分支可供合并。不推远端、不清理历史沙箱，不修改AIMovie业务工作区。后续迭代从该Git基线创建分支，完成审查后再合回main。

### Git初始化与覆盖更新证据

目录：`build/git-init-sync-20261112-120855/`，仅保留在Codeg主版本。

- `deployment-command.json`及output、`deployment.json`：实际覆盖COMPLETED/raw0/tree_terminal=true/late0；三安装各58份直接字节相等，原57份R7交付内容未变。
- `deployment-plan.json`、`replica-backups/`、`source/`：精确目标清单、覆盖前原文及本次部署源快照。`restore_replicas.py`仅恢复本次目标，遇到后续修改拒绝覆盖；本次未执行回退。
- `full-tests-command.json`及output：Git初始化后的工具回归实际命令、原始输出和终态。
- `note-{tree,format,archived}-command.json`及output：决定记录校验；`installed-entrypoints-command.json`验证三个实际入口。
- `final-receipt.json`：实际main基线提交SHA、Git状态、同步结果和最终核验；Git自身HEAD为提交的权威来源，不把报告中的文字当成合并历史。

### 历史：首次收尾核对证据

证据目录：`build/final-closeout-20261112-114653/`，仅保留在.codeg主版本。

- `installations.json`：三个安装各57份冻结文件直接比较、Git查询及主版本/Codex入口原始输出。
- `installation-command.json`及output：COMPLETED/raw1/tree_terminal=true/late0。首次库存脚本将历史 `.bak` 误计为活动交付额外项；57份内容比较均通过，原始raw1完整保留。
- `gemini-entrypoint-command.json`及output：COMPLETED/raw0/tree_terminal=true/late0，补齐未执行的Gemini入口检查。
- `closeout.json`：按既有备份排除规则登记同步结论、原始raw1的限定含义及合并阻断，不把原命令改成退出0。
- `registration-command.json`及output：检查本次索引/收尾记录、链接、原始凭据与备份，不重跑已有效的源码比较或业务门禁。
- `before/docs/todos/README.md`：本次索引改动前原文；旧R6安装备份及恢复入口仍见[任务08](../08-filesystem-receipts/README.md)。

首次收尾的TypeSafe辅助分类为 `missingRepository`，历史备份构成活动文件内容差异证据的概率为0.05。它对应当时尚未获准初始化Git的环境；当前用户新授权及实际Git初始化已解除该环境前提，不修改原始工具结果或raw1历史。
