# 原生只读消费场景（待 Root 执行）

请求：在本候选的新原生只读会话中，从 SKILL.md 继续本轮任务 01，定位当前依据并报告证据。不要重新打开、实现或改写已 DONE 的 01；不写文件，不从迭代 10 README 推断状态。

预期路径：SKILL.md → `docs/todos/11-reliable-delivery/README.md` 的 `iter:goal` → `docs/todos/11-reliable-delivery/01-delivery-mode-consistency.md` 和实际只读 `/data/workspace/iteration-manager/build/frozen-tools/fdcc4cce8863/scripts/iter_sync.py --render-envelope docs/todos/11-reliable-delivery/01-delivery-mode-consistency.md`（使用可用 Python，从项目根运行） → `templates/contracts/strict_tdd_contract.md` → `docs/todos/11-reliable-delivery/evidence/01/` 中 `task01-red-0354.json.output.txt`、`fix1-final-0401.json.output.txt`、`review-receipt.json` 和 `review-report.json`。读取真实原件并说明其适用候选；这些路径是待核对的导航预期，不是消费结果。

**缺失原件探针（刻意不存在，不删除任何文件）**：请求读取 `docs/todos/11-reliable-delivery/evidence/01/navigation-probe-intentionally-absent-04.txt`。消费者应指出路径不存在、缺口/UNKNOWN，不猜测 PASS、不加载 `docs/todos/10-self-hosting-hardening/README.md` 补猜。保留 01 真实 DONE 收据原样。

Root 应保存原生会话、终态和实际观察，并自行判断是否满足消费门禁；本场景文件不是消费证据。
