# [Refactor-Benchmark] 行为保持型重构 / 性能优化

新卡使用[结构化生成入口](../../references/template_generation.md)，spec.type 为 Refactor-Benchmark，delivery_mode 显式选择 git 或 filesystem。按[量测规则](../../references/refactor_evidence.md)选择与目标匹配的可比实测：结构目标可使用客观可重复结构数量；性能目标必须有真实性能 before/after，写明单位、环境、规模、工作负载、命令和目标，结构数量不能替代性能。两种目标均有时分别证明。未知或不可比较保持 UNKNOWN/BLOCKED，既有卡和更严格的冻结要求继续适用。

完成证据遵守 `references/task_card_schema.md`，必需 checks 精确为 baseline、regression、compatibility、benchmark_before、benchmark_after：compatibility 为观测，其余为成功命令，条件与数值保留原始输出。不新增 type 或必填元数据，不要求伪造 RED。

## 规划与验证

1. 声明影响范围、公共行为与接口，先取得受影响测试 baseline；范围不明或已规定全量时执行全量，覆盖不足先补行为保护测试。
2. 为目标规定指标、计数或计量方法、单位、范围、命令、候选及比较条件；性能目标另规定可比环境、规模、工作负载与目标。
3. 小步重构并保持行为；运行受影响 regression，观察兼容性，范围不明时扩大检查；保留迭代全量及任务既定要求。
4. before/after 在可比条件下实测，保留原始数据、变化与目标判断；不以结构量测证明性能，也不凭预检推断结果。
5. 冻结候选及证据，提交未参与设计、实现、测试或 RCA 的独立 Reviewer；实现仅置 TESTING。批准后主管按 Git C/D 或 FS 冻结合约登记，再 strict；不得仅凭勾选或 APPROVED 字段放行。
