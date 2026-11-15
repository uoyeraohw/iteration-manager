---
schema_version: 1
iteration: "11-reliable-delivery"
task_id: "11"
task_name: "审计本轮真实自用链与检查点续接"
status: "TODO"
type: "Spike-Discovery"
fix_rounds: 0
replan_count: 0
is_blocked: false
blocked_reason: ""
typesafe_score: "87.525"
typesafe_evidence: "docs/todos/11-reliable-delivery/evidence/planning/typesafe-summary.json"
tdd_verified: false
review_status: "PENDING"
review_receipt: ""
base_sha: ""
head_sha: ""
---

# 11 · 审计本轮真实自用链与检查点续接

## 1. 任务执行目标与接口契约
- **主要目标**：只审计预先选择的一条本轮真实管理链和一次真实正常检查点续接；核对原生身份、候选、顺序和证据，不实现产品、不改测试、不承担整轮回归。
- **Consumes**：Controller在推进期间保存的evidence/planning/native-source-index.json来源指针（不是任务状态账）；03真实守卫链、10隔离报告，以及被选中任务的原生会话/runner/attempt/独审/C-D/local strict原件。
- **Produces**：evidence/11/audit_native_chain.py: main(argv=None) -> int；--sources PATH --output PATH生成robustness-report.json与native-chain-index.json，沿用既定报告schema。脚本仅校验记录引用/身份/顺序/候选，语义真实性由非参与者核对原件。

## 2. 业务阶段
<!-- iter:stages -->
- [ ] 从Controller来源指针中选择一条完成链和一次正常续接
- [ ] 运行隔离审计探针并人工核对原生来源
- [ ] 交付报告及明确缺口供本卡独审，不执行整轮收口
<!-- /iter:stages -->

## 3. 按类型验证规划
隔离实验，保留可复查决定与后续接口，不虚构测试或批准。
<!-- iter:verification -->
- [ ] **experiment**：python -B docs/todos/11-reliable-delivery/evidence/11/audit_native_chain.py --sources docs/todos/11-reliable-delivery/evidence/planning/native-source-index.json --output docs/todos/11-reliable-delivery/evidence/11/robustness-report.json；缺原件返回2不补造，通过冻结runner。
- [ ] **decision**：在本卡ledger及独立报告记录实测结论、限制、来源和取舍；未知保持UNKNOWN/BLOCKED，不以结构检查代替语义验收。
- [ ] **interfaces**：evidence/11/audit_native_chain.py: main(argv=None) -> int；--sources PATH --output PATH生成robustness-report.json与native-chain-index.json，沿用既定报告schema。脚本仅校验记录引用/身份/顺序/候选，语义真实性由非参与者核对原件。；核对消费者与现有合同兼容，冻结可复查产物。
<!-- /iter:verification -->

## 4. 交付与冻结
提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
| `.agents/notes/planned/iter11/11-native-self-use-audit.md` | MODIFIED | 本任务授权范围 |
| `docs/todos/11-reliable-delivery/evidence/11/` | MODIFIED | 本任务授权范围 |
<!-- /iter:scope -->

## 6. 确定性验收标准
<!-- iter:acceptance -->
- [ ] 输入sources逐项提供task_id/session_id、候选、check命令argv/cwd/request_id/UTC、实际dispatch和终态、runner收据、attempt/release、独审、C/D及local strict原件路径；缺项、未知终态或顺序倒置输出FAIL/UNKNOWN/BLOCKED并返回2，不能补造记录。
- [ ] experiment为python -B docs/todos/11-reliable-delivery/evidence/11/audit_native_chain.py --sources docs/todos/11-reliable-delivery/evidence/planning/native-source-index.json --output docs/todos/11-reliable-delivery/evidence/11/robustness-report.json，经冻结runner保存真实退出码。至少一条本轮真实完整链、一次新会话正常继承，逐例核对原生身份与原件；不以历史链或synthetic桩替代。
- [ ] 审计范围仅选中完整链与续接；其他卡只链接已有报告。保留static/synthetic/native-self-use分层、冻结协调器已知缺陷与所有FAIL；元数据来源清单不提供状态、调度或批准。
- [ ] 本卡只交付探针、报告及来源索引，不改产品/测试/共同协议。11登记DONE后仍由Controller等全部12卡PASS再做最终全量/独立总审/最终branch strict；相应收口原件不写本卡scope。
- [ ] 实际Codeg、Windows runner或原件不足时相应case为BLOCKED/UNKNOWN并列补齐责任/条件，本卡不宣称安装已部署或外部FS业务通过。
<!-- /iter:acceptance -->

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->

## 8. 接口依赖与执行边界

- **硬依赖**：03, 10；依赖须有合法完成收据，优先顺序不自动新增硬依赖。
- **初始化状态**：仅规划已落盘；未实施、未测试、未独审、未提交，不产生验收PASS。
- **执行前提**：补齐产品执行授权、规划提交/隔离Worktree、Windows正式runner和所需原生能力；按迭代README消费实际context。
- **证据目录**：`docs/todos/11-reliable-delivery/evidence/11/`；按卡独占，原件不覆盖。
- **完成规则**：实现者最高TESTING；冻结C后由非参与者独审，再登记D与本地strict。整轮收口由Controller在全部卡PASS后执行。
