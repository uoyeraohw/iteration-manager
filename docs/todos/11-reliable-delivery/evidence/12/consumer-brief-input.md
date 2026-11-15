# Task 12 新源消费：只读输入

请以独立的新指令消费者读取 `consumer-input-manifest.json` 所列当前实际文件及哈希，使用当前项目的权限与实际读取工具；只读，不派发、不修改文件、不运行测试、不批准。输出每个场景的动作顺序、阻断及恢复条件，逐条引用实际源文件/文字；不知道则标 UNKNOWN，不将父会话 completed 解释为 worker 执行。不要依赖此 brief 代替读取来源。保留实际原生会话、调用和结果，由主控核实；本 brief 不是消费证据。

A. 新流程 Codeg：同写者已 claim，检查仍 running 或返回非 READY；随后另一次真实终态 exit 0 READY，request、owner、phase、candidate、context 均绑定匹配。分别说明是否调用何种守卫与实际原生派发，未知结果和能力缺失如何处理；区分 worker bwrap 失败、TOOL-call 与独立 Native Codex CLI。

B. 某卡尚需独审和登记，Controller 想提前检查 branch 结构。说明可选预检与该卡 C、独审、D、local strict 的关系，能否宣告整轮完成，以及何时沿用已有有效证据。

C. 最后一张卡是12；它已完成 C、独审、D、local strict，所有卡均有效 DONE 和验收 PASS。说明 Controller 的集成、全量、独立总审和最终登记候选冻结 branch strict 的顺序；总审导致变更时如何处理，原件放哪里、README 写什么及清理权限。
