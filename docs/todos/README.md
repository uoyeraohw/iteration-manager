# iteration-manager 维护任务

- [第一批：阶段 0—1 门禁修复（ACCEPTED）](01-stage01-gate-repair/README.md)
- [第二批：阶段2统一助手与有界自治（ACCEPTED）](02-bounded-autonomy/README.md)
- [第三批：阶段3—4 ACCEPTED，独立副本已同步](03-trustworthy-board-and-deployment/README.md)
- [主控链恢复：三门PASS，最终独立APPROVED（Windows单任务有界分片恢复）](04-controller-chain-validation/README.md)
- [限定工作区的主版本只读授权（ACCEPTED，Windows）](05-readonly-skill-access/README.md)
- [受控检查点续跑与统一截止入口（ACCEPTED，冻结candidate08已部署双副本）](06-checkpoint-resume/README.md)
- [AIMovie任务发现兼容性增量（ACCEPTED，candidate09三安装51文件一致）](07-aimovie-discovery-compat/README.md)
- [文件系统收据与冻结绑定（R7及七卡迁移已独立验收，六项媒体补验通过）](08-filesystem-receipts/README.md)
- [技能交付收尾：Codeg已初始化Git main，Codex/Gemini已覆盖同步](09-final-closeout/README.md)
- [迭代10：规则一致性、使用简化与真实自用健壮性（6/6 PASS，已本地合流、双副本同步）](10-self-hosting-hardening/README.md)
- [迭代11：可信路径一致性、使用成本与真实自用验证（13/13 PASS，Linux适配完成，已合入main，未部署）](11-reliable-delivery/README.md)
- [2026-11-14发布记录：主干493项通过，91份文件三安装一致，新会话显式消费通过](../releases/iteration10-20261114/README.md)
- 维护主版本：`C:/Users/qingyu/.codeg/skills/iteration-manager`。
- 2026-11-13历史初始化观察（非当前状态）：当时源码分支main，HEAD为`46ded3a4696e3bdb531d06951fce7982fa9db1cd`；迭代10尚未实施或提交。当时计划由任务05只读核查安装副本和真实消费，不从旧部署记录推断。后续合流及安装事实见上述2026-11-14发布记录。
- 历史交付基线 `SC-FS-I01-20261112-R7`：用户明确授权后，Codeg主版本已初始化Git，分支为main；当批Codex及Gemini独立副本已实际覆盖57份原交付文件并各新增1份Git基线决定记录，三安装各58份交付文件逐字节一致。维护任务、Git元数据、构建证据、缓存及历史备份不随技能同步。初始提交与最终核验见任务09及其证据目录。各旧任务中的非Git、无HEAD及早期strict结果均保留为当时事实，不代表当前主版本状态。

当前HEAD的验收投影会重新核对冻结收据。迭代10的已审文件已由迭代11后续修改，故其当前复核显示范围漂移；2026-11-14历史6/6通过及部署事实仍见原发布证据，不改写旧卡或旧收据。迭代11当前13/13验收PASS。

<!-- iter:projection -->
## 验收事实（状态声明不等于批准）

声明DONE 19/19 · 验收PASS 13/19

| 迭代 | 声明DONE | 验收PASS | 验收结论 |
| --- | --- | --- | --- |
| 01-stage01-gate-repair | 0/0 | 0/0 | EMPTY |
| 02-bounded-autonomy | 0/0 | 0/0 | EMPTY |
| 03-trustworthy-board-and-deployment | 0/0 | 0/0 | EMPTY |
| 04-controller-chain-validation | 0/0 | 0/0 | EMPTY |
| 05-readonly-skill-access | 0/0 | 0/0 | EMPTY |
| 06-checkpoint-resume | 0/0 | 0/0 | EMPTY |
| 07-aimovie-discovery-compat | 0/0 | 0/0 | EMPTY |
| 08-filesystem-receipts | 0/0 | 0/0 | EMPTY |
| 09-final-closeout | 0/0 | 0/0 | EMPTY |
| 10-self-hosting-hardening | 6/6 | 0/6 | FAIL |
| 11-reliable-delivery | 13/13 | 13/13 | PASS |
<!-- /iter:projection -->
