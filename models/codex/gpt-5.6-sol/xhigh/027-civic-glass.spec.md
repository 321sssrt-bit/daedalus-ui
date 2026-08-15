# 027 公民彩窗

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`027-civic-glass.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--stone); color: var(--ink) |
| 主要结构 `.header` | margin-bottom: 28px | display: flex; justify-content: space-between; align-items: start | 未单独声明 |
| 关键内容区 `.workspace` | gap: 18px; margin-top: 18px | display: grid; grid-template-columns: 1fr 310px; gap: 18px | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--stone` | `#e7e2d8` | 品牌或局部强调 |
| `--paper` | `#f8f4ea` | 容器与表面 |
| `--ink` | `#21323a` | 主要文字与高对比边界 |
| `--muted` | `#6d7779` | 辅助文字与弱化信息 |
| `--blue` | `#315ba6` | 品牌或局部强调 |
| `--amber` | `#e7a83e` | 品牌或局部强调 |
| `--red` | `#bb4d4d` | 错误与危险反馈 |
| `--green` | `#4f7d6a` | 成功反馈 |
| `--line` | `#b9b7ae` | 描边与分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | "Trebuchet MS","Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.header h1` | Georgia,"SimSun",serif | font-size: 35px | 由 font 简写或继承确定 |
| 分区标题 `.role h2` | Georgia,"SimSun",serif | font-size: 24px | 由 font 简写或继承确定 |
| 辅助文字 `.header p` | 继承页面字体 | font-size: 13px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `38px 28px` | `.hall` 的 `padding` |
| 布局间距 | `16px` | `.seal` 的 `gap` |
| 圆角 | `50%` | `.role:after` 的 `border-radius` |
| 边框或阴影 | `3px solid var(--ink)` | `.crest` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.check` | width: 30px; height: 30px | border: 1px solid var(--line); background: transparent; color: transparent; font-size: 18px | .role:focus-visible,.check:focus-visible,.save:focus-visible → outline: 3px solid var(--amber) |
| 输入、选择或次操作 `.save` | padding: 13px 20px | border: 0; background: var(--ink); color: var(--paper); font-weight: 800 | .role:focus-visible,.check:focus-visible,.save:focus-visible → outline: 3px solid var(--amber) |
| 内容容器 `.message` | height: 20px; margin-top: 16px | color: var(--green); font-size: 12px; font-weight: 700 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .workspace → grid-template-columns: 1fr; .roles → grid-template-columns: 1fr; .preview → order: -1 | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“公民彩窗 · 角色权限” → “议事厅权限册” → “北岸社区协作空间 · 最后修订 2026-08-14” → “保存权限方案” → “管理员” → “治理空间、成员与全部内容” → “编辑者” → “创建、编辑并组织公开内容” → “访客” → “查看获邀内容并参与讨论” → “管理员的权限” → “点击方印切换预览”。控件占位或辅助标签包括：“角色选择”、“已允许”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.header 与 .workspace 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#315ba6`、`#6d7779`、`#bb4d4d`、`#f8f4ea`、`#21323a` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.check`、输入、选择或次操作 `.save` 与 内容容器 `.message` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“公民彩窗 · 角色权限”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
