# 根的真实浏览器HTTP夹具

从iter-10根通过冻结runner运行，使用全新ready/stop文件名，且runner截止须晚于duration并保留回收时间：

```powershell
python C:/Users/qingyu/.codeg/skills/iteration-manager/build/frozen-tools/46ded3a/scripts/iter_run.py --deadline <UTC> --evidence docs/todos/10-self-hosting-hardening/evidence/04/browser-run-<unique>.json -- python -B docs/todos/10-self-hosting-hardening/evidence/04/browser_harness.py --ready-file <fresh-ready.json> --stop-file <fresh-stop> --duration 120 --delay 6
$code=$LASTEXITCODE; exit $code
```

读取ready JSON取得四个127.0.0.1动态端口、根路径和逐服务stop_file。real_git读取本迭代真实Git卡；其余明确synthetic。FS样例当前candidate与历史checkpoint不同，含remaining及三项列明sources；不是独立批准或真实历史执行证明。

根使用既有ego-browser TaskSpace5/page p1、当前1139×869视口：正常Git筛选→详情→读候选/剩余→原文→Escape；FS页核对candidate/checkpoint；empty页为空；loading页真实/api/board等待6秒；在页面打开时创建对应服务stop_file，等待刷新观察连接中断和保留快照。不要停止整个浏览器或其它服务。四态都要原生观测，不以本脚本或单元测试替代。

创建全局stop_file停止全部自有服务，也可等待duration自动停止。脚本关闭监听、等待自有线程并删除临时夹具，最后输出stopped=true/active_commands=[]；不遗留后台服务。本切片未长期启动服务，端口仅启动后分配。
