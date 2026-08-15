# 012 月下花房

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`012-month-garden.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh; padding: 24px | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.app` | width: min(1180px,100%); margin: auto; min-height: calc(100vh - 48px) | display: grid; grid-template-columns: 1fr 330px | background: var(--surface); border-radius: 32px; box-shadow: 0 24px 70px #67557624; overflow: hidden |
| 关键内容区 `.join` | width: 100%; height: 48px; margin-top: 18px | position: relative | z-index: 1; background: var(--sun); border: 0; border-radius: 14px; color: #463742 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#f1ecf5` | 页面或区域背景 |
| `--surface` | `#fffdfc` | 容器与表面 |
| `--text` | `#41374d` | 主要文字与高对比边界 |
| `--muted` | `#887d91` | 辅助文字与弱化信息 |
| `--accent` | `#7f5aa2` | 主要操作与强调状态 |
| `--success` | `#4e8068` | 成功反馈 |
| `--danger` | `#bf5b67` | 错误与危险反馈 |
| `--pink` | `#e9b8c7` | 主要文字与高对比边界 |
| `--leaf` | `#9bc1a4` | 品牌或局部强调 |
| `--sun` | `#efd48c` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-rounded,"Microsoft YaHei",system-ui,sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.month h1` | 500 42px/1 Georgia,"Songti SC",serif | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.sidebar h2` | 500 30px/1.2 Georgia,"Songti SC",serif | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.sidebar small` | 继承页面字体 | 16px / normal（浏览器默认） | letter-spacing: .14em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px` | `body` 的 `padding` |
| 布局间距 | `8px` | `.controls` 的 `gap` |
| 圆角 | `32px` | `.app` 的 `border-radius` |
| 边框或阴影 | `32px` | `.app` 的 `border-radius` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.controls button` | width: 42px; height: 42px; border-radius: 50% | border: 1px solid #ddd3e2; border-radius: 50%; background: white; color: var(--text) | .controls button:hover → background: #f0e5f5 |
| 输入、选择或次操作 `.event` | display: block; width: 100%; border-radius: 8px; padding: 6px 7px; margin-top: 6px | border: 0; text-align: left; border-radius: 8px; font-size: 10px; color: var(--text) | 未声明独立状态；保持默认样式 |
| 内容容器 `.join` | width: 100%; height: 48px; border-radius: 14px; margin-top: 18px | background: var(--sun); border: 0; border-radius: 14px; color: #463742; font-weight: 900 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .app → grid-template-columns: 1fr; .sidebar → min-height: 340px; .day → min-height: 78px; .event → overflow: hidden; .calendar → padding: 24px 14px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“月下花房 · 日历” → “八月，花期正盛” → “2026 · 7 项安排 · 2 个空闲傍晚” → “周一” → “周二” → “周三” → “周四” → “周五” → “周六” → “周日” → “27” → “28”。控件占位或辅助标签包括：“上个月”、“下个月”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.app 与 .join 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#41374d`、`#9bc1a4`、`#efd48c`、`#4e8068`、`#f1ecf5` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.controls button`、输入、选择或次操作 `.event` 与 内容容器 `.join` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“月下花房 · 日历”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
