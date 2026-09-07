# 027 角色权限

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`027-access-map.html`
- 复现范围：三角色切换、分组权限清单勾选、预览模式只读、保存 toast

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | 1280×800，grid 240px + 1fr | 左角色列表右权限编辑 | 圆角 14px |
| 角色侧栏 | 240px `#312e81` | 三个 role-btn 全宽 | 固定 |
| 主区 | toolbar + perms + footer | flex 列 | perms 可滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#1e1b4b` | 外背景 |
| `--surface` | `#ffffff` | 主面板 |
| `--text` | `#1e1b4b` | 标题、标签 |
| `--muted` | `#64748b` | 分组标题、hint |
| `--accent` | `#7c3aed` | 按钮、checkbox、侧栏 active |
| `--preview` | `#fef3c7` | 预览 badge 背景 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 显示字 | system-ui, sans-serif | 20px / 1.2 | 700 |
| 标题 | system-ui, sans-serif | 13–14px | 600 |
| 正文 | system-ui, sans-serif | 14px / 1.4 | 400 |
| 辅助文字 | system-ui, sans-serif | 12px | 400 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 8–28px | perm-item padding 12×14px |
| 控件圆角 | 8px | 按钮、perm 行 |
| 容器圆角 | 14px | frame |
| 边框 / 阴影 | 1px `#e2e8f0`；shadow `0 20px 60px rgba(0,0,0,.4)` | |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 角色按钮 `.role-btn` | padding 14×20px | 浅紫字透明底 | active 左 3px `#a78bfa` + 半透明紫底 |
| 权限项 | checkbox 18px + label | 灰底 `#fafafa` 边框 | preview 时 `.disabled` opacity 0.5 不可改 |
| 保存按钮 | 两处 primary | 紫底白字 | 点击 toast「权限已保存」2s |
| 预览切换 | ghost 按钮 | 边线按钮 | 切换「预览模式」badge 显示/隐藏 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280px | 240 + 1fr | 三角色各 7 项权限 |
| ≤768px | 单栏 | 侧栏可堆叠 |

## 内容与数据

- 角色：管理员（全开）、编辑者（内容部分）、查看者（全关）
- 权限分内容/成员/系统三组，含 label 与 hint
- 切换角色即时重渲染对应勾选状态；预览模式禁用 checkbox

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| Toast | 0.2s opacity | 底部居中紫条 | 压缩 |
| 预览切换 | 即时 | badge + disabled 态 | 无 |

## 复现验收清单

- [ ] 左栏三个角色可切换，标题同步
- [ ] 每组权限清单含 checkbox 与说明 hint
- [ ] 「切换预览」进入只读，badge 显示「预览模式」
- [ ] 保存按钮触发 toast
- [ ] 1280 240px 紫侧栏布局
