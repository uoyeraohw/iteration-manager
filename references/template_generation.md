# 从结构化规格生成任务卡

新卡优先使用 `scripts/iter_templates.py`，无需从默认Strict-TDD/Git模板替换段落。现有卡不迁移；旧解析器、收据和四type门禁不变。

```powershell
python -B scripts/iter_templates.py --render spec.json
python -B scripts/iter_templates.py --check card.md --delivery-mode git
```

`--render`只向stdout输出Markdown；`--check`只向stdout输出JSON `{"valid":true,"errors":[]}`。有效输入退出0；输入、读取或结构错误退出2，错误以JSON输出。命令不写任务卡、配置或收据；需要落盘时由调用方明确选择路径及覆盖权限。`--check`必须指定git或filesystem；它只预检新生成卡，不是旧卡验收或完成门禁。命令参数用法错误由CLI报告并退出2。

## spec版本1

```json
{
  "version": 1,
  "task_id": "02",
  "iteration": "10-example",
  "task_name": "生成任务卡",
  "type": "Strict-TDD",
  "delivery_mode": "git",
  "objective": "由结构化输入生成新卡",
  "consumes": "TYPE_CHECKS",
  "produces": "render_task_card(spec) -> str",
  "scope": ["scripts/example.py", "tests/"],
  "stages": ["实现核心行为"],
  "acceptance": ["输出可由现有解析器读取"],
  "verification": {
    "red": "python -m pytest tests/test_example.py -q；确认目标断言失败",
    "green": "python -m pytest tests/test_example.py -q；确认通过",
    "regression": "python -m pytest tests/test_example.py -q；覆盖受影响接口"
  }
}
```

以上所有字段必需；未知字段、未知type或版本拒绝。除version、scope、stages、acceptance、verification外均为非空字符串；version必须是整数1（不是布尔值）。后三个数组均非空且元素为非空文本；scope使用项目相对路径，目录以`/`结尾，沿用既有路径规则，禁止绝对路径、`..`、`.git`、glob及破坏表格的分隔符。`verification`键集必须精确对应type，每个值是实际命令或观测说明：

- Strict-TDD：red、green、regression。
- UI-Component：interaction、states、visual、regression。
- Refactor-Benchmark：baseline、regression、compatibility、benchmark_before、benchmark_after。
- Spike-Discovery：experiment、decision、interfaces。

检查名复用`TYPE_CHECKS`；命令与观测的证据要求仍见[任务卡契约](task_card_schema.md)，生成不执行这些检查。非TDD不要求伪造RED或true；Refactor仍保留before/after实测门禁。

`stages`、`acceptance`及`verification`的非空文本可含前导空白（含换行），渲染保留原文；预检按清单项判断非空，不把下一项的内容算作当前必需检查的说明。纯空白仍无效。

## 占位符与Markdown

此入口把`{{identifier}}`、`${identifier}`（identifier由Unicode字母/数字/下划线、点或连字符组成）、精确`{TODO}`、`{TBD}`及`YYYY-MM-DD`定义为未替换占位符，在spec文本与生成卡正文/元数据中拒绝。旧手填模板应先转换为实际spec，不以通用大括号猜测是否填写。

`{key: value}`、`List<T>`、HTML标签、Markdown代码块及讨论TODO状态的普通文字可表达；不把任意大括号或尖括号文本当占位符。生成器拥有`iter:*`结构标记，用户文本不应伪造这些标记；CLI会预检最终结构。

## filesystem先定稿再冻结

将delivery_mode设为filesystem，并增加非空`candidate_id`；git规格不接受candidate_id。初态保持TODO、PENDING、tdd_verified=false、typesafe_score=UNASSESSED，SHA为空，不产生批准事实。FS正文不复制审查后需修改的状态结论。

执行并完成正文、ledger及勾选后，冻结源码、证据、完整卡和迭代目标，再独立审查。登记仅修改允许元数据及外部收据；正文或勾选改变须重新冻结与受影响重审。Git仍按C→独审→登记D→strict，不受FS完整正文规则替代。

Python调用：`render_task_card(spec: dict) -> str`无效规格抛ValueError；`validate_generated_card(content: str, delivery_mode: str) -> list[str]`返回错误列表，两者均不落盘。
