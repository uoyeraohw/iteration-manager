# 迭代10已本地合流并同步安装副本

2026-11-14完成本地发布。Codeg继续作为维护源；Codex、Gemini各91份交付文件与维护源逐字节一致。主干全量493项通过。两个独立新会话已显式加载各安装根，并执行其实际脚本；不是仅凭文件一致或help退出0判定消费。

## 合流版本与原验收

- 主仓库：`C:/Users/qingyu/.codeg/skills/iteration-manager`，分支`main`。
- 合流前主干：`d3bd97ab16ffed6104034a887a01eb1b4d75dc0e`；保留恢复引用`backup/iter10-premerge-20261114`。
- 迭代分支：`feat/iter-10-self-hosting-hardening`，交付HEAD `2b295843a2ca34dd630aece6aab88b8c0eb428b3`。
- 本地`--no-ff`合流提交：`26652bad2fcfb7c883d8e9a8bcad4aeb96160816`。本次安装清单绑定此提交；后续发布登记只增加本报告/证据、更新根索引，不改变91份交付文件。
- 六卡、整轮独审和分支严格门禁沿用[原始迭代记录](../../todos/10-self-hosting-hardening/README.md)。任务卡、05有日期的发布观察及06健壮性报告均未改写。
- 合流后的实际主仓库执行`python -B -m pytest -p no:cacheprovider tests -q`：**493 passed in 410.05s**；runner为COMPLETED/raw0/tree_terminal=true。见[原始输出](evidence/main-tests.json.output.txt)与[收据](evidence/main-tests.json)。
- 主干实际`iter_sync.py .`刷新根投影：6项DONE、6项验收PASS，见[evidence/root-sync.json.output.txt](evidence/root-sync.json.output.txt)。旧迭代EMPTY只表示本扫描器未发现任务卡，不改写其历史验收结论。

## 双副本与回滚备份

| 安装目录 | 交付文件 | 备份原文件 | 修改既有文件 | 新增 |
| --- | ---: | ---: | ---: | ---: |
| `C:/Users/qingyu/.codex/skills/iteration-manager` | 91 | 72 | 18 | 19 |
| `C:/Users/qingyu/.gemini/config/skills/iteration-manager` | 91 | 72 | 18 | 19 |

范围固定为`SKILL.md`、`scripts/`、`references/`、`templates/`、`tests/`、`.agents/notes/`。从Codeg已提交Git清单取源，保存源字节快照；覆盖前全量及逐路径检查目标漂移，以同目录临时文件原子替换。没有删除文件；历史`.bak`、缓存和其它非交付文件不覆盖、不清理。没有复制Git元数据、维护`docs/todos`或build证据。

[部署原始记录](evidence/deployment.json)和[完整清单/备份映射](evidence/deployment-plan.json)保存实际路径。两个消费会话结束后，主控再次核对91份文件、备份存在及历史备份字节，见[最终核验](evidence/verification.json)。

本地恢复包保留在：

```text
C:/Users/qingyu/.codeg/skills/iteration-manager/build/iter10-release-20261114-101008/
  source/                  # 本次91份源文件快照
  replica-backups/0/        # Codex原72份文件
  replica-backups/1/        # Gemini原72份文件
  preserved-backups/       # 历史备份的额外保留副本
  deployment-plan.json
  restore_replicas.py
```

从主仓库运行只读恢复预检：

```powershell
python -B build/iter10-release-20261114-101008/restore_replicas.py --check
```

部署后预检已通过，74个实际变化路径可恢复（两副本各18个既有变更、19个新增）。**获准回滚时**将`--check`换成`--apply`：逐路径恢复原文件、移除本次新增文件；任何后续用户修改都使预检拒绝，不覆盖后续工作，目录和无关文件保留。本次未执行回滚。主干如需撤销本次合流，可在新的撤销授权下使用`git revert -m 1 26652bad2fcfb7c883d8e9a8bcad4aeb96160816`保留历史；恢复引用不要求破坏性reset。

## 新会话已实际消费各安装根

| 新会话 | 实际消费安装 | 原生身份 | 结果 |
| --- | --- | --- | --- |
| Codeg #1729 / Codex | `.codex/skills/iteration-manager` | `01a1d7d9-46d2-71c2-b0b9-321bc12e6415` | 通过 |
| Codeg #1730 / Antigravity | `.gemini/config/skills/iteration-manager` | `73f429df-53de-4b18-be12-78412da1b0d4` | 通过 |

两个会话分别从实际副本读取SKILL及新规格，自己构造带独立marker的UI-Component/filesystem隔离样例；运行该安装的iter_run、iter_templates、iter_sync：

1. 生成新卡退出0，保留四类UI验收及candidate_id，初态TODO/review_status PENDING/tdd_verified=false，不产生批准事实。
2. 新卡预检退出0，返回`valid:true`。
3. `scope: ["../escape"]`退出2并返回结构化错误，没有生成越界文件。
4. 对真实迭代10执行只读takeover-report退出0，六项均DONE且验收PASS。

两个最终runner均COMPLETED/raw0/tree_terminal=true。主控读取探针源码、原始输出、收据及原生工具调用后验收；没有重跑有效消费测试。Codex首次探针误把生成卡初态字段写为`acceptance_verdict`，原始raw1及输出保留在[evidence/codex/sandbox/](evidence/codex/sandbox/)；改为真实字段`review_status`后沿用已有效生成/预检输出，在continuation补完其余检查。此失败属于验收探针，不是产品RED。

可追溯原件：

- [Codex命令与输出](evidence/codex/sandbox/continuation/probe-results.json)、[最终收据](evidence/codex/sandbox/continuation/probe-run.json)、[原生JSONL调用/返回摘录](evidence/codex-native-calls.json)。安装SKILL和新生成规范的原生返回与当前安装文本核对一致。
- [Gemini副本命令与输出](evidence/gemini/probe-results.json)、[最终收据](evidence/gemini/probe-run.json)、[原生执行调用](evidence/gemini-native-calls.json)、[原生文档读取及返回](evidence/gemini-native-document-calls.json)。原生SQLite只读提取，三份规范返回与安装文本一致。
- [Codex派发/终态守卫](evidence/codex-session-native.json)、[Antigravity派发/终态守卫](evidence/gemini-session-native.json)、[主控最终核验](evidence/verification.json)。completed本身不代替上述功能断言。

## 证据边界与保留状态

本次通过的是**显式指定安装根的新会话消费**。Gemini副本由真实新Antigravity会话消费；Gemini CLI原生自动发现，以及助手配置自动注入仍未验证，本次未改助手配置。未新增真实filesystem业务生命周期验收；原迭代的历史缺口及R06-01非阻断发现继续保留。

完整维护套件在Codeg主仓库执行。安装白名单内的`tests/test_board_handoff.py`仍引用维护`docs/todos`中的浏览器harness，因此本次不宣称安装副本可以脱离维护证据运行完整维护套件；不为此扩大部署白名单。

Worktree `.worktrees/iter-10`及迭代分支保留；没有推送、合流到远端、清理Worktree或删除分支。已存在的未跟踪`.codegraph/`保持原样且不提交。备份包为本机恢复资产，未随Skill或发布证据副本复制。
