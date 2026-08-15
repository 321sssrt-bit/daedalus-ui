# 011 瑞士电流

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`011-swiss-current.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.kpis` | gap: 1px | display: grid; grid-template-columns: repeat(3,1fr); gap: 1px | border: 1px solid var(--text); background: var(--text) |
| 关键内容区 `.headline` | padding: 30px 0 18px | display: flex; justify-content: space-between; align-items: flex-end | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#f3f2ed` | 页面或区域背景 |
| `--surface` | `#ffffff` | 容器与表面 |
| `--text` | `#111111` | 主要文字与高对比边界 |
| `--muted` | `#6e706c` | 辅助文字与弱化信息 |
| `--accent` | `#244cff` | 主要操作与强调状态 |
| `--success` | `#138757` | 成功反馈 |
| `--danger` | `#e53935` | 错误与危险反馈 |
| `--grid` | `#d7d7d0` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,Helvetica,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.headline h1` | 继承页面字体 | font-size: clamp(42px,6vw,76px); line-height: .88 | letter-spacing: -.075em |
| 分区标题 `.charthead h2` | 继承页面字体 | font-size: 16px | 由 font 简写或继承确定 |
| 辅助文字 `.top small` | 700 11px/1.4 monospace | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `28px 34px` | `.page` 的 `padding` |
| 布局间距 | `1px` | `.kpis` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `4px solid var(--text)` | `.top` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.grain button` | height: 36px; padding: 0 16px | border: 0; border-right: 1px solid var(--text); background: transparent; font-weight: 800 | .grain button.active → background: var(--accent); color: white |
| 输入、选择或次操作 `.tooltipbox` | min-height: 18px; margin-top: 4px | color: var(--accent); font-weight: 800; font-size: 12px | 未声明独立状态；保持默认样式 |
| 内容容器 `body` | margin: 0 | background: var(--bg); color: var(--text) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:800px)` | .chartwrap → grid-template-columns: 1fr; .chart → border-right: 0; border-bottom: 1px solid var(--text); .headline → display: grid; gap: 22px; .kpis → grid-template-columns: 1fr; .top small → display: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“Current · 数据看板” → “CURRENT®” → “PRODUCT SIGNAL REPORT” → “2026 / Q3” → “增长不是噪声，” → “要看清来源。” → “活跃使用者” → “48,260” → “↑ 12.4%” → “关键任务完成率” → “71.8%” → “↑ 3.1%”。控件占位或辅助标签包括：“时间粒度”、“关键任务趋势折线图”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.kpis 与 .headline 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#6e706c`、`#244cff`、`#e53935`、`#f3f2ed`、`#111111` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.grain button`、输入、选择或次操作 `.tooltipbox` 与 内容容器 `body` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:800px)` 条件下，布局按响应式表变化且“Current · 数据看板”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
