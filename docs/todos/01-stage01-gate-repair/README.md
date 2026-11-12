# 第一批：阶段 0—1 门禁修复

状态：ACCEPTED（阶段0—1完成）。Google Antigravity双项独立验收PASS，Codex最终核对通过；具备推进第二批条件，本次停止，不进入第二批。

## 基线与恢复

- 安装目录不是 Git 仓库：无分支、HEAD 或 dirty 可声明，不初始化 Git。
- 16 个原始源码/模板文件：`build/stage01-20261110/baseline/primary/`。
- 两个保护副本的初始内容同样保存于 `baseline/codex/`、`baseline/gemini/`。
- 助手 ID 2/3/4 的指令、revision 和更新时间：`build/stage01-20261110/assistants-before.json`。仅只读保存，本批不部署助手。
- 恢复时先核对当前文件是否仍为本次候选，只恢复本次改动；新文件逐项确认后处置，不整目录覆盖或删除。

## 范围

修改 `scripts/iter_sync.py`、任务卡/实现者/审查者/契约模板及直接相关 Skill、Worktree 和手册引用。
可新增任务卡契约、纯标准库门禁模块及针对性测试。本批不改看板渲染、自治计数器或 Codeg 助手配置。

## 任务与证据

1. 阶段0：源位置、恢复快照、卡片/证据契约冻结。
2. 1.1：恢复测试调用基线；保留业务断言，环境错误不算行为 RED。
3. 1.2：任务卡语义解析与新旧格式兼容。
4. 1.3：Git 错误拒绝放行与审查包。
5. 1.4：工作区范围检查、已有改动归属及安全恢复。
6. 1.5：按类型完成证据、严格门禁、提交/规格绑定。
7. 独立 Antigravity 验收及缺陷修复；Codex 最终验收。

每次测试的命令、时间、退出码见 `build/stage01-20261110/runs.jsonl`，原始输出见相邻日志。

## 裁决

- Ruling: 采用原地限定修改和文件快照 — 主版本非 Git，用户指定其为维护位置 — 不提供不存在的交付 SHA，保留可逐文件恢复的原始内容。
- Ruling: 复用 CLI、增加小型纯标准库门禁模块 — 避免扩大已近1900行的入口文件，同时保留既有函数调用 — 外部调用者继续从 iter_sync 导入。
- Ruling: 不采用讨论中的“C 后任意业务文件变化均使所有旧审查失效” — 后续无关任务会被误阻断 — 每个 receipt 核对自身范围和规格，分支严格门禁另检查改动覆盖。

## 外部讨论

Google Antigravity 只读讨论：会话 1483，task_id `102bddb4-aec8-483d-851f-aae62374436f`，已完成。
采纳按类型证据表、旧卡 UNKNOWN 与契约防漂移建议；不引入额外内容哈希。此讨论者不承担最终独立验收。

## 实施证据

| 切片 | 有效RED | GREEN |
| --- | --- | --- |
| 卡片语义/状态 | schema-red：2个断言失败 | schema-green：2通过 |
| Git失败/linked worktree包 | git-red：2个断言失败 | git-green：3通过 |
| 缺范围/工作区dirty | scope-red：4个断言失败 | scope-green：4通过 |
| 旧DONE与严格CLI | completion-legacy-red：2个断言失败 | completion-legacy-green：3通过 |
| 分类型收据 | receipt-type-red：2个断言失败 | receipt-type-green：2通过 |
| 代码/规格绑定与分支覆盖 | binding-red：8失败、5通过 | binding-green：21通过，含四种type的真实CLI |
| 模板投影与严格sync退出码 | sync-red：4失败、1通过 | sync-green：5通过 |
| 严格sync的干净候选 | strict-clean-red：1个断言失败 | strict-clean-green：1通过 |

baseline运行4失败/3通过，其中TypeError是测试调用失配，不计行为RED。full-candidate-01暴露新证据目录使模板白名单期望多出一项；保留原三个路径并增加新证据目录断言，不删除业务断言。最终全套结果以之后冻结候选对应日志为准。

TypeSafe输出：对“当前遗漏提交内容绑定”和“当前遗漏分支覆盖检查”分别为0.92、0.88；这是实施中快照的结构判断。Codex据实际断言失败实施绑定/覆盖修复，验收以最终运行及独立审查为准。

## 最终验收与交付

- 冻结候选：`build/stage01-20261110/candidate04/`，基线差异 `candidate04.diff`，逐文件恢复原文位于 `baseline/primary/`。
- 最终全套：`full-candidate-03.log`，39 passed，退出0；命令与时间见runs.jsonl。之前full-candidate-01/02为模板期望未增加证据目录的失败，不作为最终GREEN。
- Antigravity模板/文档验收：会话 [1488](codeg://session/1488)，task_id `d50af385-48ea-4e1c-818c-a92067866499`，completed，273855ms；报告 `antigravity-template-review.md`，PASS，无阻断。
- Antigravity运行时终审：会话 [1489](codeg://session/1489)，task_id `2f0c3a30-131d-44f2-8c66-6c44f05f5b58`，completed，156601ms；原文 `antigravity-runtime-final.md`，PASS，无阻断。该会话只读源码，未重跑测试。
- 独立运行探针：`review01-probes.log`、`runtime-probes.log`。它们验证门禁行为，不表示已接受任何真实业务项目的任务收据。
- 会话1486在676655ms后取消，未形成最终结论；会话1487在673702ms后取消，报告文件编码损坏。`antigravity-runtime-review.md`保留作失败记录，不计入验收证据；仅采用其独立可解析的探针日志和之后1489的完整终审。
- Codex最终核对：实际候选与codeg主版本逐文件直接内容比较无差异；两个保护副本源码新增/删除/变化均为空，结果 `final-source-comparison.json`。现有gemini缓存README创建于2026-10-14，不属于源码快照范围，未删除。未部署任何助手配置变更。
- 决策笔记已转implemented；树/格式校验各1篇通过，归档校验0篇通过；非Git环境的append-only检查明确跳过。没有安装目录交付SHA。

Codex采纳两项PASS的限定结论：门禁可机械检查结构、版本关系和范围；字段或非空输出不能证明测试语义、视觉质量或审查者真实身份，仍由独立Reviewer核对原始材料。不采纳报告中超出此边界的绝对防伪表述。

本批未遗留阶段0—1阻断修复项。后续仍需分批处理看板/交付信封可信性、自治流程与助手部署；旧DONE须补齐真实证据并独立审查后才可通过严格门禁。本轮全部迭代完成后，再同步另外两个真实副本。

最终TypeSafe辅助输出：对“所提供证据是否报告未解决的阶段0—1阻断”返回0.04；Codex最终结论为ACCEPTED，依据实际行为证据、独立审查与内容比对，不以概率替代验收。机器可读汇总见build/stage01-20261110/acceptance.json。审查冻结后仅追加本文验收登记，源码/模板/契约未再变化。
