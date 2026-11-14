# Agent Note: 结构化任务卡生成的核心切片

Status: implemented

## Problem

手工模板默认Git及Strict-TDD，其他类型与FS需要人工替换段落，容易留下不适用的验证要求或冻结后仍需修改的审查正文。

## Decision

`iter_templates`从结构化spec直接生成确定性Markdown，复用`iter_contracts.TYPE_CHECKS`、解析器和范围规则；不读写任务卡、配置或收据。生成只给出TODO、PENDING、false和UNASSESSED，不能产生执行或批准事实。FS正文只指向外部审查结果，并明确完整正文先定稿再冻结。

独立CLI提供stdout Markdown渲染与stdout JSON预检，合法退出0、输入或结构错误退出2，默认不写文件。spec严格限定版本、字段、类型与必需形状。预检针对新生成初态，不代替旧卡解析或完成验收。

非空文本允许前导空白，渲染保留原文。预检以清单项边界提取内容后用`strip()`判空，与spec非空规则一致；必需检查不能借用下一项内容。F01不通过禁止前导空白收窄输入合同，也不对渲染文本做隐式规范化。

占位符只识别显式双大括号标识符、美元大括号标识符、精确`{TODO}`/`{TBD}`与日期哨兵`YYYY-MM-DD`；普通大括号、泛型、HTML与代码块可表达。该判别由TypeSafe jev-1.14.0选择显式语法，confidence=1.0；不是质量评分或验收。

## Alternatives considered

- 在旧模板中替换占位符及段落：能直接复用手写布局，但八组合需要脆弱的文本改写，容易残留动态正文。采用直接构造章节，并保持旧模板不动。本次TypeSafe评估选择结构化渲染，模型为jev-1.14.0；它不替代测试或独立验收。

## Existing-note audit

- [FS完整正文绑定](../bug-fix/2026-11-12-filesystem-r7-acceptance-repair.md)部分相关：保留其完整正文合同，不修改已有绑定算法。
- [分层验证与检查点](2026-11-12-bounded-validation-workflow.md)部分相关：沿用核心RED→GREEN和正常切片，不减少任务交付门禁。
- 其余检索命中涉及授权、部署与盘点，不被本决定取代。

## Consequences

四类型必需检查名保持单一来源；Refactor-Benchmark仍包含前后量测。手写模板通过生成说明衔接新入口，不迁移既有卡。显式占位符语法避免误杀合法代码，代价是调用者须遵循约定的占位语法，不能期待识别任意自然语言待填提示。

## Testing

`slice-a-core-red.json`记录可调用空实现下19个真实断言失败，退出1；`slice-a-core-green.json`记录首次实现的8个失败和11个通过，原因是占位符正则误认HTML标记；`slice-a-core-green-2.json`记录修复后19项通过，退出0。原件均在本卡evidence/02目录，runner确认进程树终态；未执行交付回归，不代表独立审查通过。

切片B的`slice-b-cli-boundary-red.json`记录17失败、57通过，CLI实际执行但stdout为空触发断言失败，另有合法代码误拒和预检漏拒；`slice-b-cli-boundary-green.json`同组74通过。`slice-b-compatibility.json`补充既有Git投影和四type实际FS绑定：冻结匹配、元数据登记兼容、正文/勾选漂移拒绝和candidate不匹配拒绝；不伪造历史RED或批准。后续交付回归与独审以检查点及原件为准。

F01返修的`repair-c-red-cli-1718.json`记录36项真实断言失败及9项非空边界通过，包含三字段、空格/制表符/换行、Git/FS与真实CLI退出2的反例；`repair-c-green-1717.json`同组45通过，真实CLI完成`--render`/`--check`往返；`repair-c-regression-1717.json`指定五文件156通过。初次仅API断言RED亦保留在`repair-c-red-1717.json`，未冒称执行到CLI。返修仍待独立复审。
