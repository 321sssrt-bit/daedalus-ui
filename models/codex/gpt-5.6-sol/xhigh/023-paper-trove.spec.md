# 023 纸上藏品

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`023-paper-trove.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--desk); color: var(--ink) |
| 主要结构 `.board` | max-width: 1180px; margin: 28px auto; padding: 38px; gap: 34px; min-height: 580px | display: grid; grid-template-columns: repeat(3,1fr); gap: 34px | background: var(--cork); border: 12px solid #60432e; box-shadow: inset 0 0 40px rgba(63,35,17,.28),8px 10px 0 rgba(44,24,12,.25) |
| 关键内容区 `.card` | padding: 21px 18px 18px; min-height: 210px | position: relative; display: flex; flex-direction: column | background: var(--paper); box-shadow: 4px 6px 9px rgba(54,31,18,.25) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--desk` | `#8b5e3c` | 品牌或局部强调 |
| `--cork` | `#bd8a5b` | 品牌或局部强调 |
| `--paper` | `#fff8df` | 容器与表面 |
| `--ink` | `#3b2b23` | 主要文字与高对比边界 |
| `--muted` | `#79685a` | 辅助文字与弱化信息 |
| `--blue` | `#4d73a8` | 品牌或局部强调 |
| `--red` | `#bd4c45` | 错误与危险反馈 |
| `--tape` | `#d9cea8` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | "Segoe Print","KaiTi",cursive | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.title h1` | 继承页面字体 | font-size: 34px | 由 font 简写或继承确定 |
| 分区标题 `.title p` | 继承页面字体 | font-size: 13px | 由 font 简写或继承确定 |
| 辅助文字 `.tabs button` | 700 13px Arial,"Microsoft YaHei",sans-serif | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `32px` | `.desk` 的 `padding` |
| 布局间距 | `4px` | `.tabs` 的 `gap` |
| 圆角 | `50%` | `.card:nth-child(even):before` 的 `border-radius` |
| 边框或阴影 | `6px 8px 0 rgba(40,20,10,.24)` | `header` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.tabs button` | padding: 9px 13px | border: 0; border-bottom: 2px solid transparent; background: transparent; color: var(--muted); font: 700 13px Arial,"Microsoft YaHei",sans-serif | .tabs button.active → color: var(--blue); .remove:focus-visible,.tabs button:focus-visible → outline: 3px solid var(--blue) |
| 输入、选择或次操作 `.board` | margin: 28px auto; padding: 38px; display: grid; min-height: 580px | background: var(--cork); border: 12px solid #60432e; box-shadow: inset 0 0 40px rgba(63,35,17,.28),8px 10px 0 rgba(44,24,12,.25) | 未声明独立状态；保持默认样式 |
| 内容容器 `.card` | padding: 21px 18px 18px; min-height: 210px; display: flex | background: var(--paper); box-shadow: 4px 6px 9px rgba(54,31,18,.25) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:900px)` | .board → grid-template-columns: repeat(2,1fr); padding: 28px; .desk → padding: 18px | 交互流程与内容顺序不变 |
| `(max-width:620px)` | header → display: block; .tabs → overflow: auto; .board → grid-template-columns: 1fr; .card → transform: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“纸上藏品 · 收藏夹” → “纸上藏品” → “把值得回来的东西，钉在看得见的地方。” → “全部” → “去处” → “阅读” → “器物” → “6 枚藏品” → “去处 / PLACE” → “雾岭步道” → “雨停后两小时最好走。” → “从收藏夹取下”。控件占位或辅助标签包括：“收藏分类”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; .card → transform: none |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; .card → transform: none |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.board 与 .card 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#4d73a8`、`#d9cea8`、`#3b2b23`、`#bd4c45`、`#fff8df` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.tabs button`、输入、选择或次操作 `.board` 与 内容容器 `.card` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:900px)` 条件下，布局按响应式表变化且“纸上藏品 · 收藏夹”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
