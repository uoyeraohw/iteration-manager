# 🧩 [UI-Component] 视图呈现 / 前端交互型子任务模板

完成证据遵守 `references/task_card_schema.md`，必需checks：interaction、states、visual、regression（states/visual为观测，实际检查正常/空/加载/错误和任务规定视口）。实现仅置TESTING；提交C并独立审查后，由主管登记真实JSON收据与持久报告、状态，提交D再严格检查。不得仅凭勾选或APPROVED字段放行。

> **适用范围**：前端 Web 组件、视图渲染、表单交互、动画效果、样式布局及响应式适配。  
> **核心铁律**：`Props 契约冻结 + 多状态确定性验收 + 零全局样式污染`。

---

## 🎯 1. 组件接口与数据契约 (Component Interfaces)
- **组件名称与路径**：`{组件文件相对路径}`
- **Props 契约**：{列出属性名称、类型、是否必填、默认值}
- **Events / Emits 契约**：{列出组件向上派发的事件名及携带 Payload 类型}
- **Slots / 布局插槽**：{默认插槽与具名插槽定义}

---

## 🛠️ 2. 四态呈现与交互执行流程 (Component Lifecycle & States)
- [ ] **Step 1 [契约与类型定义]**：在组件接口文件中定义 Props/Events 的 TypeScript 类型定义。
- [ ] **Step 2 [四态实现覆盖]**：
  - **默认态 (Default)**：正常数据下的视觉渲染与排版；
  - **空数据态 (Empty)**：无数据时的友好占位与引导操作；
  - **加载中态 (Loading)**：异步请求过程中的 Skeleton 或 Spinner 占位；
  - **错误态 (Error)**：接口失败时的重试机制与警示提示。
- [ ] **Step 3 [交互与可访问性验证]**：编写交互单测（Vitest / Jest / Testing Library）模拟点击、输入、焦点流转与键盘事件。
- [ ] **Step 4 [样式隔离确认]**：确认使用 Scoped CSS / CSS Modules / Tailwind，无全局样式泄露污染。
- [ ] **Step 5 [审查与本地冒泡]**：通过代码对审后更新任务卡为 `🟢 已完成 (DONE)`，运行 `iter_sync.py --local`。

---

## 🛡️ 3. 确定性验收断言 (Acceptance Criteria)
- [ ] **组件单测命令**：`{测试命令}` 全部通过，覆盖 Props 变更与事件触发。
- [ ] **视觉与快照检查**：DOM 快照比对一致，无控制台 Console Error / Warning 告警。
- [ ] **响应式适配**：在桌面端与移动端常见视口尺寸下无溢出或布局崩溃。
