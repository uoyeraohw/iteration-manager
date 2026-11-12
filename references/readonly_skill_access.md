# 主版本契约的受控只读通路

当叶子的原生文件工具拒绝读取主版本时，先停止依赖该契约的任务。只有用户明确授权新增通路后，才能由主控注册本服务；原生拒绝仍有效，不调整additionalDirectories、终端根目录或写策略。

## 注册前锁定授权

`scripts/skill_readonly_mcp.py --grant <绝对JSON路径>`使用已安装的Python MCP SDK，通过stdio只提供`read_skill_file`。原CLI不依赖MCP。

授权JSON字段：`version:1`、`enabled:true`、非空`grant_id`、真实绝对`workspace`与`skill_root`目录、逐项`files`清单。工作区必须精确匹配服务实际cwd；不接受调用者提供根目录。授权文件放在叶子写范围之外，由主控持有。只列出需要交付的源码、测试、模板与文档，不列build、配置、凭据或会话。

在Antigravity现有`<GEMINI_HOME>/config/mcp_config.json`的`mcpServers`中新增单独服务器项，command使用实际Python绝对路径，args使用`-B`、脚本绝对路径、`--grant`、授权绝对路径。保留其它服务器及配置形状；只保存本项原值，不复制其它服务器凭据。回滚前核对本项仍为本次部署值，再恢复本项原值或移除本项，不能覆盖后续用户修改。

## 调用与撤销

`read_skill_file(relative_path, start_line=1, max_lines=200)`只接受规范POSIX相对文件名，必须精确命中清单；每次重新读取授权。返回原文行号、主版本绝对来源、总行数、grant_id与workspace。文件最多1 MiB，单次最多400行。拒绝链接/越界及打开句柄最终路径不匹配；仅支持Windows和有`/proc/self/fd`的Linux，其他平台拒绝读取。

设置`enabled:false`后，下次调用立即拒绝。删除注册项只影响新建连接，不能代替撤销已有服务。服务没有写入和执行工具。注册是用户级的，但授权绑定一个实际cwd，其他工作区调用失败；不修改grant来迁就错误的MCP启动cwd。

## 验收

先跑单元及真实stdio测试，再用新Antigravity会话在目标worktree实际调用新注册工具读取必读契约，并验证一个非清单的无敏感内容路径被拒绝。记录原生工具调用和返回来源，由未参与设计/实现者独立验收。配置落盘、本地stdio成功、代理completed都不能替代实际消费。业务自动链另行验收。
