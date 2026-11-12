# Agent Note: 可信进度投影与本机证据服务

Status: implemented

## Problem

旧看板从声明DONE推断APPROVED/100%测试，缺阶段清单固定50%，Ruling冒充重规划，三个输出分别解析元数据。HTML将任务文本写入innerHTML及裸script JSON，API允许通配CORS。

## Decision

阶段清单是唯一进度源，派生当前阶段和比例；无清单未知，不称工时进度。共用语义frontmatter、自治状态及真实审计数据，分别统计声明DONE和验收PASS。Terminal/HTML/README消费同一数据。HTML用安全JSON与文本节点，证据入口只读且仅访问卡片列出的项目内产物。本机监听，禁止任意Origin/CORS与Host重绑定。

任务库存也由同一发现器提供：数字前缀Markdown（含旧 `01.md`）以及frontmatter显式含task_id/status的卡片进入看板、接管报告和分支strict；无任务元数据的验收大盘等辅助文档不计入。无编号、只有status的旧卡仍可用；坏数字卡、空task_id/status和不可读文件保守进入后续审计，正文示例不能伪装任务身份。Git完成收据与修复预算判定不因库存修复而放宽。

## Alternatives considered

- 给旧HTML逐处转义：改动较小，但三份解析与隐式DONE绿色仍重复；采用共用投影与独立静态HTML模板，减少脚本混写。
- 取消实时服务只导出：减少网络面，却丢失用户已有实时路径；保留只读服务，导出才写文件。

## Testing

2026-11-12 AIMovie存量兼容复核发现辅助文档被算作任务。真实断言RED为3 failed/1 passed；首修回归33 passed/1 failed暴露纯数字旧文件名遗漏，恢复该兼容后针对性10 passed。随后新增无编号status-only旧卡反例为1 failed/4 passed，保留status元数据入口后最终11 passed。两个失败候选均保留，未将修复计数清零。证据在项目 `docs/todos/01-用户体验整改与创作路径聚焦/证据/strict-compat-20261112/`，保存源码基线、候选、实际命令、输出和退出码。第一次pytest跨盘自动扫描到Windows受限兼容目录的collection error不算行为RED；显式 --rootdir/--confcutdir 限定本Skill测试范围后取得有效RED。未创建文件系统完成收据profile，未把旧DONE判为PASS。

build/stage03-20261111保留board-truth及board-service的断言RED/GREEN、完整回归61 passed及命令/退出码。Antigravity独立初审session1498无必须修复项，报告和浏览器原始检查同目录保存。真实浏览器覆盖声明DONE但UNKNOWN、FUSED阻塞、特殊文本不执行、筛选、抽屉、证据读取、自动刷新、空态及390px无横向溢出。round04夹具CRLF插入失败不算产品RED，round06修正夹具后完成交互。

## Consequences

README新增验收投影兼容旧表；有效PASS仍依赖第一批收据绑定检查，UI不重新解释证据真假。实际助手消费发现英文旧表保留TODO而投影已DONE/PASS：同步器支持有限的`Task`+`Status`组合及中文正式索引，仅更新精确卡片链接行的状态列，保留Commit和其它链接；空行结束表头作用域，防止误改后续普通表。不扩展为通用Markdown解析器，也不假定其它英文根索引格式已受支持。修复断言RED、针对性GREEN及回归证据归build/stage04-20261111。本机服务拒绝自定义Host别名和跨源请求。既有[有界自治决定](../process/2026-11-11-bounded-autonomy.md)部分重叠，沿用其计数真源，不新增调度。看板验证通过不表示阶段4部署/真实新会话消费/副本同步已完成，状态以维护任务为准。
