# TypeSafe规划质检

必须调用实际MCP `evaluate`。工具不可用或无可解析结果时记UNASSESSED，保留阻断与所需工具，不用内置主观评分代替。

## 四维统一门禁

权重 **30/30/20/20**：granularity（可独立验证粒度）、clarity（验收明确度）、single_responsibility（职责单一）、actionability（可执行性）。综合≥80/100且每维≥70/100。置信度不是评分，也不提高门禁分数。

请求采用真实 `{state,questions}` 结构。state放观察到的目标、范围、Interfaces、验收命令及约束，不放“该方案优秀”等预判。每个问题只判断一个维度：

```json
{
  "state": {
    "objective": "实现Bearer鉴权中间件",
    "scope": ["src/auth.js", "test/auth.test.js"],
    "acceptance": ["缺少Header返回401", "过期Token返回403/EXPIRED_TOKEN", "有效Token挂载req.user并调用next"],
    "command": "npm test -- test/auth.test.js"
  },
  "questions": {
    "clarity": {
      "type": "score",
      "instructions": "评价所列验收标准的客观可验证程度。",
      "criteria": ["无验收要求", "只有主观目标", "部分可验证但缺关键结果", "核心行为有明确断言与验证命令", "核心和失败边界均有明确断言与验证命令"]
    }
  }
}
```

这是单维调用示例；正式规划必须另为其余三维定义各自具体的有序criteria，同批发四个问题，不把clarity结果复制到别的维度。

## 保存尺度并换算

读取实际响应 `answers.<id>.score`、`legend`、`probabilities`、`confidence`及model。score是0索引的有序等级加权位置，N级最大N−1；五级响应2.97对应 `2.97/4*100=74.25`，不是2.97/5，也不是confidence=76分。按实际legend级数计算，等级不足2、缺维、非数值或越界记UNASSESSED并保留原始输出。

每维先换到0—100，不提前四舍五入；总分 `0.30*g + 0.30*c + 0.20*s + 0.20*a`。同时保留分布和等级文字，模型概率高不保证事实正确。最终报告分开列“TypeSafe输出”和“主管综合判断”。

保存原始请求/响应、时间、model、每维legend和换算、加权总分及项目内证据路径。只有真实四维通过后才填任务卡typesafe_score；模板初始为UNASSESSED。低分先在已授权范围改进，实际重规划消耗对应预算；超授权或不能达标呈报具体选项，由用户明确决定，不伪装自动通过。
