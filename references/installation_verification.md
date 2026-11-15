# 安装来源与轻量检查

来源仓库根目录使用完整 Git 提交生成清单，输出仅到 stdout；保存或随副本分发须另获部署授权：

```bash
python3 -B scripts/iter_install.py --make-manifest --root /path/to/source --source-commit FULL_COMMIT
python3 -B scripts/iter_install.py --check --root /path/to/installation --manifest /path/to/manifest.json
```

清单为 `version: 1`、完整 `source_commit` 和 `files` 数组，每项仅含相对 `path` 与小写 SHA256。生成检查 Git 提交对象、交付白名单的已提交文件集合、暂存区、源目录实际集合和逐字节内容；不读取白名单外的项目文件。白名单为 `SKILL.md`、`scripts/`、`references/`、`templates/`、`tests/`、`.agents/notes/`。未提交或忽略的额外白名单文件、缺失、漂移和符号链接均拒绝；仓库其他区域的变更不作为交付源码。检查要求清单与安装白名单集合及字节一致，拒绝未知键、重复键或路径、越界和符号链接；不修改、安装或修复文件。成功退出 0，输入错误或不一致退出 2。

清单必须由可信来源保管：检查独立副本只核对调用者提供的摘要，不能在无 Git 源的副本中证明提交存在、清单完整或来源可信，也不是签名或审查批准。文件检查假定目录在检查期间不被其他写者并发替换；不要把它作为对抗并发目录替换的沙箱。

输出分开列来源/文件结果与运行时能力。query、runner、平台后端的存在仅是文件观察；runner 存在时仍为 UNKNOWN，缺失则 UNAVAILABLE，完整执行链始终 UNKNOWN；Linux 另观察 pidfd API 和 proc 子进程列表是否可访问，缺少前提为 UNAVAILABLE；这些观察不证明实际权限或子回收可用。Windows 的 Job Object 执行保持未知。不启动命令、不实测平台原语，不以 query 存在推出可派发。Linux 源码使用 subreaper、proc、pidfd，Windows 源码使用 Job Object；当前 Windows 实测未验证。实际 runner 使用须另以对应平台的原始收据和命令树终态核实。

安装烟测应在隔离临时目录复制白名单、用可信清单检查、注入漂移并确认拒绝；它不运行维护全套。维护全量须在维护仓库以该轮冻结 runner 和外部临时根运行，不能因副本烟测成功推断全套通过。安装落盘、宿主发现、新会话消费和外部业务验收各需独立授权或证据。
