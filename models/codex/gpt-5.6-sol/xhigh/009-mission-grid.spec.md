# 009 北辰调度台

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`009-mission-grid.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.app` | min-height: 100vh | display: grid; grid-template-columns: 78px 1fr | 未单独声明 |
| 关键内容区 `.panel` | 未单独声明 | 未单独声明 | border: 1px solid var(--line); background: var(--surface); border-radius: 14px; overflow: hidden |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#0b1114` | 页面或区域背景 |
| `--surface` | `#111b20` | 容器与表面 |
| `--text` | `#e8f2ed` | 主要文字与高对比边界 |
| `--muted` | `#72858a` | 辅助文字与弱化信息 |
| `--accent` | `#48e49e` | 主要操作与强调状态 |
| `--danger` | `#ff6868` | 错误与危险反馈 |
| `--amber` | `#ffc65c` | 品牌或局部强调 |
| `--line` | `#223239` | 描边与分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Inter,ui-sans-serif,system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.head h1` | 继承页面字体 | font-size: 28px | 由 font 简写或继承确定 |
| 分区标题 `.ph h2` | 继承页面字体 | font-size: 15px | 由 font 简写或继承确定 |
| 辅助文字 `.logo` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 1000 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `20px 12px` | `.rail` 的 `padding` |
| 布局间距 | `14px` | `.icons` 的 `gap` |
| 圆角 | `12px` | `.logo` 的 `border-radius` |
| 边框或阴影 | `1px solid var(--line)` | `.rail` 的 `border-right` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.filters button` | border-radius: 20px; padding: 6px 11px | border: 1px solid var(--line); background: transparent; color: var(--muted); border-radius: 20px; font-size: 11px | .filters button.active → color: #07100c; background: var(--accent) |
| 输入、选择或次操作 `.icon` | width: 42px; height: 42px; border-radius: 10px | border: 0; border-radius: 10px; background: transparent; color: var(--muted); font-size: 18px | .icon.active,.icon:hover → background: var(--surface); color: var(--accent) |
| 内容容器 `.panel` | border-radius: 14px | border: 1px solid var(--line); background: var(--surface); border-radius: 14px | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:900px)` | .stats → grid-template-columns: 1fr 1fr; .grid → grid-template-columns: 1fr; .app → grid-template-columns: 60px 1fr; .content → padding: 22px 16px; .queue th:nth-child(3),.queue td:nth-child(3) → display: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“北辰调度台 · 工作总览” → “2026 年 8 月 14 日 · 星期五” → “早上好，林队长。系统等你下令。” → “09:42:16” → “今日待调度” → “18” → “↑ 3 个新到” → “按时完成率” → “94%” → “↑ 6% 本周” → “在线成员” → “12”。控件占位或辅助标签包括：“主导航”、“总览”、“任务”、“信号”、“团队”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.app 与 .panel 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#111b20`、`#ff6868`、`#72858a`、`#223239`、`#e8f2ed` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.filters button`、输入、选择或次操作 `.icon` 与 内容容器 `.panel` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:900px)` 条件下，布局按响应式表变化且“北辰调度台 · 工作总览”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
