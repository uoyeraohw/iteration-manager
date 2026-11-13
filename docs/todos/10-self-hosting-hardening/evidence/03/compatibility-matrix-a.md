# 03 切片A：基线与兼容矩阵

基线 `f879bba28326af84fd9217a70c390a35887ec62b`，分支 `feat/iter-10-self-hosting-hardening`。未修改产品源码。旧接口完整函数签名及原board/card键集已由同次真实调用打印在 `slice-a-before-1732.json.output.txt`，不是预期值清单。

| 对象 | 现有事实与证据 | 切片A覆盖 | 续接门禁 |
| --- | --- | --- | --- |
| 旧导入 | `iter_sync`函数及导入函数签名原件在before输出首行 | 已记录真实签名 | 提取后逐项保留，包括私有旧导入；query不得反向依赖sync/CLI |
| 旧同步 | strict local/global、未提交候选、中文/英文旧表 | 原有5项测试通过，baseline receipt | 提取后重跑受影响项 |
| 新增投影 | 当前board缺delivery_mode/candidate_id/execution；envelope可调用 | Git/FS × 有/无checkpoint，4个断言RED | 同源GREEN，旧键不丢失，读取不写入 |
| Git候选 | `test_execution_readiness.py:562`明确断言candidate_id为空串；commit_sha另列 | 源码静态事实，未重跑该测试 | 主控澄清已知Git不适用空串是否保留；未知字段UNKNOWN/null要求不静默改写 |
| CLI phase | `iter_sync.py:877,917`默认implementation | 静态定位 | 新旧CLI实测默认、显式phase、位置参数 |
| CLI退出 | 当前调用/打包1、范围2、自治阻塞3，成功0；runner124/125独立 | 旧同步0/2实测；其余未验 | 新增CLI测试覆盖0/1/2/3、未知选项无写入和timing帮助 |
| 导入时机 | 当前main内延迟加载命令模块 | 静态定位 | inventory/preflight/execution改走query；仅main加载CLI；无跨调用缓存 |
| 量测 | 10/100固定五状态循环，3次，各为board+全部envelope | before成功，原始秒数与Git调用清单齐备 | 用同脚本相同参数，最终提取后测after；不把混合合成样例外推为完整已批准收据绑定性能 |

量测脚本：`python -B docs/todos/10-self-hosting-hardening/evidence/03/benchmark_projection.py --label after`，外层仍须指定冻结runner、实际授权截止和唯一receipt。fixture使用系统临时目录，构造时间不计入，脚本参数固定；没有跨调用缓存。

本切片尚无GREEN、benchmark_after、八文件任务回归或独审。不得将本矩阵、baseline成功或runner终态当作03 PASS。
