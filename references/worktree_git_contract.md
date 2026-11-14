# 🛡️ Worktree 并行敏捷迭代、Zero-Root-Touch 与单迭代合流契约 (v2.0)

在多迭代演进与高并发工程协作中，[`iteration-manager`](file:///C:/Users/qingyu/.codeg/skills/iteration-manager/SKILL.md) 深度融合了 Superpowers 的 `using-git-worktrees` 与 `finishing-a-development-branch` 最佳实践，确立了 **「主干规划提交基线 + `1 Worktree = 1 Iteration` + `Zero-Root-Touch` 目录级物理隔离 + 单迭代主干合流」** 的全生命周期契约。

---

## 证据持久化与只读门禁

本契约服从本次用户授权及[共同执行协议](agent_protocol.md)。仅生成Prompt、评估或只读接管不授权写文件、实现、提交或创建Worktree；只交付标明执行前门禁的预览。Git提交、合流、推送、发布和清理分别按各自授权执行，验收通过不产生这些权限。

新卡遵守 [task_card_schema.md](task_card_schema.md)：实现提交C含代码、测试与原始输出，独立Reviewer核对C及冻结规格；APPROVED后登记JSON收据、状态和报告，提交D，再对干净候选运行严格门禁。head_sha绑定C，不改成D。仅状态/账本登记免重审，代码/规格/原始输出变化必须重审受影响内容。不同type使用各自证据，不为非TDD任务补造RED。

审查包目录通过 `git rev-parse --git-path iter_reviews` 定位，兼容linked worktree的.git文件。临时审查包不代替项目证据目录：清理Worktree前将原始输出、最终报告与收据保留在可检出的证据目录。--check-scope --include-worktree只读检查，已有dirty由主控核对归属，不自动checkout/reset/clean。Git失败、无效引用、缺规格/证据或未知状态均不放行。

## 📌 1. 核心架构原则：为什么采用 `1 Worktree = 1 Iteration` 与 `Zero-Root-Touch`？

### 1.1 前置铁律：Worktree 创建前的「规划基线提交门禁 (Pre-Worktree Commit Gate)」
- **Git Worktree 的底层机制约束**：`git worktree add .worktrees/iter-{XX} -b feat/iter-{XX} main` 仅会从 `main` 分支的**已提交 Git Commit 树**中检出文件，主工作区中未追踪（Untracked）或未提交（Unstaged/Staged）的 `docs/todos/` 文件**绝对不会自动进入新 Worktree**！
- **规划提交与执行门禁分离**：
  1. **规划落盘**：仅在写入授权内生成三级文档；只有Git提交授权才逐个精准暂存本次归属文件，检查cached diff后提交。禁止 `git add .` 或暂存整个 `docs/todos/`，不夹带他人dirty。
  2. **执行前门禁**：实际创建Worktree或执行任务前必须运行 `python <skill_root>/scripts/iter_sync.py --verify-committed`。非零先读取诊断，区分Git错误与未提交规划；没有Git提交权限时交付未提交计划和执行依赖，不自动补Commit，不启动受阻执行。仅生成Prompt不触发该提交流程。

### 1.2 分支与工作区粒度法则：`1 Worktree = 1 Iteration`
- **工作区路径标准**：统一放置于项目根目录下的 `.worktrees/iter-{两位序号}`（如 `.worktrees/iter-02`）；创建前确认已忽略 `.worktrees/`，缺规则时只在获准范围内修改 `.gitignore`；
- **分支命名标准**：统一采用 `feat/iter-{两位序号}-{迭代短名}`（如 `feat/iter-02-user-auth`）；
- **工作区内相对路径准则（防跨目录串写）**：进入 `.worktrees/iter-{XX}` 后，所有子智能体必须读写**当前 Worktree 下的 `docs/todos/{XX}-*/` 文件**，严禁通过指向主仓库原工作区的绝对路径去修改主工作区中的 `docs/todos/` 文件！
- **黄金合流平衡点**：
  1. **子任务级（Per-Task）**：Git模式按实现C → 非参与者独审 → 主管登记D → `--local --strict` 顺序推进；提交须有授权且只包含本次归属文件，卡片及迭代README由唯一卡片写者维护；
  2. **单迭代级（Per-Iteration）**：全部任务验收PASS并通过迭代末独立总审及分支strict后，交付候选与证据；未授权合流时保留Worktree与分支，不合入main、不推送、不清理。

### 1.3 Zero-Root-Touch 目录级物理隔离原则
**最安全的防冲突机制是不产生任何交叉写集合：**
1. **分支开发态绝对禁止触碰根文档**：在 Worktree 分支内，**严禁以任何形式修改、格式化或提交根目录 `docs/todos/README.md`**；
2. **任务卡为状态真源，二级索引为投影**：当前Worktree任务卡持有任务状态，`docs/todos/{迭代}/README.md` 的聚合投影由获准的 `python iter_sync.py --local` 幂等维护；
3. **主干统一最终一致性聚合**：获准合流后，仅在根索引写入授权内于 `main` 执行 `/iter sync` 刷新根 `docs/todos/README.md`，提交仍需Git授权。

---

## 🗂️ 2. Worktree 三级文档读写权限矩阵 (Read/Write Scope Matrix)

| 文件层级与路径 | 读权限 | 写权限 | 行为准则与物理防御机制 |
| :--- | :---: | :---: | :--- |
| **所属迭代目录**<br>`docs/todos/{当前迭代}/*` | 🟢 允许 | 按授权及角色 | 目录边界不是整目录写权；任务卡及迭代README由唯一卡片写者维护，实现者只写授权文件并返回证据，投影由获准的 `iter_sync.py --local` 更新。 |
| **外部迭代目录**<br>`docs/todos/{非当前迭代}/*` | 🟢 允许 | 🔴 **严禁** | **跨迭代防污染**：严禁修改其他迭代的任务卡或文档，由 `iter_sync.py --check-branch` 审计拦截。 |
| **总控路线图与看板**<br>`docs/todos/README.md` | 🟢 允许 | 🔴 **严禁** | **Zero-Root-Touch 零触碰红线**：`iter_sync.py` 内置特性分支写入锁，非 `main` 分支调用时自动拒绝修改根 `README.md`。 |

---

## 🔄 3. Worktree 四阶段全生命周期操作规程

```mermaid
flowchart TD
    A["核对本次授权 / cwd / 分支 / HEAD / dirty归属"] --> Q{"仅Prompt或只读？"}
    Q -->|是| Preview["只交付预览与执行前门禁，不写文件或提交"]
    Q -->|否| G1
    subgraph Phase0 ["阶段零：授权内规划与执行前门禁"]
        G1["按写入授权落盘规划"] --> G2["有Git权限才精准暂存归属文件 / 检查cached diff / 提交"]
        G2 --> G3["真正执行或创建Worktree前 --verify-committed；失败停止受影响执行"]
    end

    subgraph Phase1 ["阶段一：Worktree 隔离探针与干净基线 (Setup)"]
        P1["Step 0: 检测 git-dir vs git-common-dir 及分支名"] --> P2["创建/进入 .worktrees/iter-{XX} (feat/iter-{XX})"]
        P2 --> P3["确认 Worktree 内 docs/todos/{XX}-* 已检出 + 运行 Clean Baseline Test"]
    end

    subgraph Phase2 ["阶段二：分支内 SDD 循环与二级冒泡 (Per-Task Loop)"]
        T1["按type完成实现与证据，最高TESTING；获准提交C"] --> T2["独立Reviewer审查C与冻结规格"]
        T2 --> T3["APPROVED后唯一写者登记收据 / DONE / 提交D"]
        T3 --> T4["--local --strict 核对验收PASS"]
    end

    subgraph Phase3 ["阶段三：迭代末总审与合规预检 (Pre-Merge Gate)"]
        F1["运行 iter_sync.py --check-branch --strict 验证零触碰与四态门禁"] --> F2["派发 Final Whole-Branch Reviewer 全分支总审"]
        F2 --> F3["汇总展示全部 Rulings 与 Deferred Minors 并呈报合流菜单"]
    end

    subgraph Phase4 ["阶段四：按各自授权收尾"]
        M0{"核对合流 / 推送 / 清理各自授权"} -->|未授权| Keep["保留分支与Worktree，交付证据"]
        M0 -->|仅执行已授权动作| M1["获准合流后验证合流结果"]
        M1 --> M2["获准才在main同步根索引并精准提交"]
        M2 --> M3["另有清理授权且证据已持久化才移除Worktree / 分支"]
    end

    Phase0 --> Phase1 --> Phase2 --> Phase3 --> Phase4
```

### 阶段一：启动期隔离探针与基线验证（融合 `using-git-worktrees`）
1. **确认授权与规划已提交**：实际创建Worktree或执行任务前运行 `python <skill_root>/scripts/iter_sync.py --verify-committed`；失败不自动暂存、提交或清理，权限缺口只阻塞对应动作；
2. **检测现有隔离状态（严禁盲目嵌套创建 Worktree）**：
   依次运行 `git rev-parse --git-dir`、`git rev-parse --git-common-dir` 与 `git branch --show-current`（注意排除 `git rev-parse --show-superproject-working-tree` 子模块情形）；
3. **创建或复用 `.worktrees/iter-{XX}`**：
   - 若尚未处于独立 Worktree，先执行 `git check-ignore -q .worktrees` 确认 `.worktrees/` 已被忽略；
   - 仅有创建授权且门禁通过后执行 `git worktree add .worktrees/iter-{XX} -b feat/iter-{XX}-{slug} main`；
4. **干净基线测试（Verify Clean Baseline）**：
   在开始第 1 个子任务前，必须运行一次项目测试套件，确保工作区基线 100% 绿灯。

### 阶段三 & 四：迭代收尾菜单与合流清理（融合 `finishing-a-development-branch`）
当本迭代所有子任务均已流转为 `🟢 已完成 (DONE)`、通过全分支总审且 `python iter_sync.py --check-branch --strict` 返回 `PASSED` 后，向用户汇总本迭代所有的 `Rulings` 与 `Deferred Minors`，并呈现标准收尾选项：
这些是待选择的收尾方式，不是自动执行指令。未取得相应授权时采用保留现状；合流授权不包含推送或删除授权。

1. **Option 1：获准本地合入 `main` 主干并同步全局看板**
   - 切回主工作区根目录，`git checkout main` ➔ `git merge --no-ff feat/iter-{XX}-{slug}`；
   - 在 `main` 上运行测试套件确认合流结果全绿；
   - 仅有根索引写入和提交授权时运行 `python <skill_root>/scripts/iter_sync.py` 并精准提交；
   - 仅有清理授权且原始证据已持久化时执行 `git worktree remove .worktrees/iter-{XX}` 与 `git branch -d feat/iter-{XX}-{slug}`；否则保留。
2. **Option 2：获准推送远程分支并创建 Pull Request**（保留 `.worktrees/iter-{XX}` 供后续 PR 迭代）。
3. **Option 3：保持当前 Worktree 与分支原状**（稍后手动处理）。

---

## 🚫 4. 负向约束红线清单 (Negative Constraints Checklist)

- [x] **红线 1**：严禁在 `docs/todos/` 规划文件尚未 `git commit` 入主干前直接执行 `git worktree add`；
- [x] **红线 2**：严禁在 Worktree 分支内通过主仓库原绝对路径跨工作区读写主仓库的 `docs/todos/` 文件；
- [x] **红线 3**：严禁在 Worktree 分支开发态修改、格式化或提交根总控 `docs/todos/README.md`；
- [x] **红线 4**：严禁跳步流转四态（Implementer 只能置为 `🔵 待验收`，唯有 Reviewer Subagent 给出 `Approved` 后才可置为 `🟢 已完成`）；
- [x] **红线 5**：严禁在 `git worktree remove` 报存在未追踪文件时擅自使用 `--force` 强删（必须先向用户展示未提交文件清单并征询处置方式）。
