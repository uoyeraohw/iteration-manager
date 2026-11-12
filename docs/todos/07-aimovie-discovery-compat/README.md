# AIMovie任务发现兼容性增量验收

状态：ACCEPTED。三处主版本增量及必要的新回归测试已独立验收，冻结candidate09共51份交付文件；三个安装目录逐字一致。AIMovie项目完整strict仍BLOCKED，未修改业务、任务卡或历史收据。

## 验收对象与规则

基线为已验收candidate08。精确增量为：

- `scripts/iter_sync.py`：共用任务发现器接入看板、接管报告和分支strict。
- `references/task_card_schema.md`：记录任务库存发现规则。
- `.agents/notes/implemented/architecture/2026-11-11-trustworthy-board.md`：既有决定及实际修复证据。
- `tests/test_task_discovery_compat.py`：新增5项回归，属于本切片必要交付，不只同步前三份文件。

纳入数字前缀Markdown（包括旧`01.md`）及完整frontmatter含task_id/status的文件；README和无身份元数据的辅助文档不算卡。保留status-only旧卡、空值、坏数字卡及读取失败文件的审计入口；正文示例不提供任务身份。验收针对这一明确的发现规则，不将其概括为任意损坏文档都可识别。

## 原始证据与独立复验

证据根：`build/stage10-checkpoint-resume-20261111/aimovie-acceptance01/`。

- `candidate09-manifest.json`：冻结51文件、相对candidate08的4文件完整差异；主版本与AIMovie原候选逐字一致，原实现基线也与candidate08逐字一致。冻结时PENDING原样保留，后续实际结果见本记录及最终验收JSON。
- `review-packet.json`：关键源码及行号、原始命令/输出/退出码和来源，未重造历史。
- 原AIMovie证据目录`docs/todos/01-用户体验整改与创作路径聚焦/证据/strict-compat-20261112/`保留真实3断言失败RED、33过1失败的数字文件名兼容缺陷、10过中间结果、status-only反例1失败4过及最终11过。最初collection WinError5不是行为RED，两个失败候选及修复计数2均保留。
- `full-regression.json`及原始output：冻结候选136 passed，229.97秒；统一入口COMPLETED/raw_exit_code0/tree_terminal=true/late0。
- `acceptance-probe.json`及`acceptance-probe-report.json`：真实AIMovie库存7、accepted0/7，takeover与看板任务集合一致；`--local --dry-run --strict`实际退出2，既有Markdown逐字未变。隔离Git夹具验证分支strict拒绝support-only空库存，并逐一审计4张legacy/broken卡、不放行PASS。
- `note-validation.json`：冻结笔记tree/format/archive通过；非Git环境跳过归档提交差异检查，归档0。

全新非参与Antigravity[1637](codeg://session/1637)正式APPROVED该切片，允许4文件增量部署；报告`antigravity-review.json`，原生身份与实际TypeSafe结果`review-native.json`。委派completed，300541ms、守卫late0，无新增实现或测试执行。Codex核对实际diff、原始输出及报告后接受，无发现必须修复项；不将报告中“zero silent drops”扩展到没有数字名或完整身份frontmatter的任意损坏文档，也不采纳其对未审05/06/07任务状态的一揽子概括。

TypeSafe结构化判断支持兼容性切片范围（概率0.95）；Codex最终结论为兼容性增量ACCEPTED，AIMovie完整strict未通过。两者分开记录在`typesafe-codex.json`和`codex-acceptance.json`。

## 双副本部署与实际消费

副本预检发现iter_sync和新测试已经逐字等于冻结candidate09，保留、不重写；仅将仍为candidate08的schema和笔记各补齐两份。没有覆盖来源不明的差异。`replica-sync.json`记录逐项already_equal/replace、备份和CAS恢复条件，未删除其它文件或复制build/会话/配置。

`deployment-smoke.json`及`deployment-verification.json`确认主版本和两个副本各51文件逐字一致，三个真实入口分别读取AIMovie任务7张、accepted0张，退出0，项目Markdown未变。统一入口COMPLETED/raw0/tree_terminal=true/late0。没有模板变更，不重复2/3号助手部署和旧131项检查。

## 本切片之外的阻断

AIMovie仍需独立处理真实完成收据/冻结绑定及存量任务证据问题。本切片不提供文件系统完成收据能力，不审查07迁移或本地Mock业务，不追认历史批准，也不把库存修正说成项目strict PASS。相关项目状态继续归其原任务记录；本记录只拥有iteration-manager兼容性增量的验收与部署状态。
