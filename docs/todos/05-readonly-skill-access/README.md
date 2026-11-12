# 限定工作区的主版本只读授权

状态：ACCEPTED（Windows目标工作区）。用户已授权扩展正式授权通路；原生文件范围不变。此任务完成不等于业务自动链PASS。

## 设计与范围

Antigravity ACP 1.4.5的additionalDirectories同时进入读取、写入及企业终端范围，不提供只读位。采用现有MCP Python SDK的stdio接口，按授权清单提供主版本文件的只读读取；不改Codeg源码、vendor二进制、账号、原生workspace或写策略，不新增通用文件/命令接口。

授权文件由主控持有，绑定精确真实worktree cwd、主版本真实根目录和逐项文件allowlist。每次请求重新校验授权，可通过enabled=false立即撤销。调用者不能传入根目录或改授权；拒绝越界、链接逃逸、非清单文件、过大文件及工作区不匹配。使用句柄最终路径核对防止打开前的路径替换泄露内容。

正式注册位置沿用Antigravity既有`<GEMINI_HOME>/config/mcp_config.json`，只增加本任务服务器项，保留其它项；无须重启Codeg。先验证本地stdio，再注册，再在实际叶子cwd进行真实MCP消费。

原生view_file的拒绝保持有效。用户新授权的是独立受控读取能力，验收改为该已注册只读能力实际读取成功；不把原生拒绝当作通过或用shell/副本/复制契约绕过。

## 文件与处理计划

1. `scripts/skill_readonly_mcp.py`提供`SkillReadGrant.read_file(relative_path, start_line=1, max_lines=200)`及单一MCP工具`read_skill_file`。先用可运行占位实现取得真实断言RED，再最小GREEN。
2. `tests/test_skill_readonly_mcp.py`覆盖原文/来源、错cwd、越界/绝对路径/非清单、链接逃逸、撤销/坏授权、大小限制、实际stdio及无写工具。安全拒绝不能泄露文件内容。
3. `references/readonly_skill_access.md`与共同协议记录条件、接口、授权/撤销和证据；既有`.agents/notes`记录选择及反例，不另建状态真源。
4. `build/stage09-readonly-authorization-20261111/`保存RED/GREEN、限定授权、配置目标项备份/回滚、原生消费证据。注册通过后真实叶子只读探针；新Antigravity非参与者独立审查，再恢复业务链。

## 门禁与Review Focus

- 原生范围/企业控制/宿主写根不变，未授权工作区不得读取。
- 授权清单只含明确主版本交付文件，不暴露build、会话、密钥或用户配置。
- 使用已安装Python MCP 1.13.1；依赖只适用于新增服务，不给原CLI加前提。
- 不复制完整MCP配置到证据，避免重复保存其它服务器凭据；恢复只移除本任务拥有且仍匹配的服务器项。
- 业务沙箱HEAD、旧卡FUSED/计数和dirty测试保留，由后续主控负责正式恢复。

## 执行证据

根因：stage09/native-policy-metadata.json与create-agent-config-bytecode.txt；会诊1552建议只读MCP通路，不是独立批准。TypeSafe输出additionalDirectories单独满足只读概率0.07、受控provider保留原生范围概率0.77；Codex据实际字段与工具工厂选择上述方案，运行时门禁另验。

- 核心12项真实断言RED后最小GREEN；补充stdio、独立竞态及行范围后19项通过。完整91项回归通过（194.29秒，exit0），原始命令/起止/退出码保存在stage09对应receipt。笔记tree/format均exit0。
- 精确grant含37项交付文件，绑定run02真实worktree。正式注册仅新增iteration-skill-readonly，保留7个其它server；registration.json只保存本项，回滚预演通过，未实际回退。
- 后续检查点维护候选独立批准后，清单逐项增加6份交付文件至43项（grant_id v2），仍只有read_skill_file工具。新Antigravity1581在相同worktree实际读取SKILL、共同协议和新检查点契约，并原生执行用户另行授权的精确runner入口成功；不是给只读server添加exec。证据在stage10的native-runner-probe.json、native-consumption-inventory.json及沙箱runner-native-probe三文件。
- 新会话1555通过新MCP工具读取Strict-TDD及共同协议；原生SQLite idx4/6返回主版本source/grant_id/workspace，idx8拒绝非清单路径。原始记录见native-probe-calls.json，监控见probe-monitor.json。
- 未参与设计/会诊的Antigravity1556独立APPROVED，见independent-review.json。采用其Windows权限通路批准；报告中“Linux得到验证”的措辞无本次Linux执行证据，不采纳该外推。Linux实现存在，运行验收仍未覆盖。
- TypeSafe对当前证据足以恢复同工作区业务验证输出0.34（模型不确定性）；Codex依据直接原生读取/拒绝证据、精确授权、91项回归与独立审查，裁决Windows权限通路通过。该裁决仅允许启动后续业务测试，不预判其结果。
