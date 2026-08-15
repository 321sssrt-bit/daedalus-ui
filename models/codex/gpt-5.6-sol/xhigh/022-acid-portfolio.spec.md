# 022 酸性作品簿

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`022-acid-portfolio.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--acid); color: var(--black) |
| 主要结构 `.layout` | min-height: calc(100vh - 78px) | display: grid; grid-template-columns: 360px 1fr | border: 3px solid var(--black); border-top: 0 |
| 关键内容区 `.bar` | height: 46px; padding: 0 14px | display: flex; align-items: center; justify-content: space-between | border: 3px solid var(--black); background: var(--white) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--acid` | `#dfff00` | 品牌或局部强调 |
| `--black` | `#0a0a0a` | 品牌或局部强调 |
| `--white` | `#f5f5ef` | 品牌或局部强调 |
| `--gray` | `#a6a6a0` | 品牌或局部强调 |
| `--pink` | `#ff4fa0` | 主要文字与高对比边界 |
| `--blue` | `#526dff` | 品牌或局部强调 |
| `--literal-7` | `#d2d2cc` | HTML 中直接声明的局部色 |
| `--literal-8` | `#444` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.bio h1` | 继承页面字体 | font-size: 54px; line-height: .82 | letter-spacing: -4px |
| 分区标题 `.head h2` | 继承页面字体 | font-size: 38px | letter-spacing: -2px |
| 辅助文字 `.bar` | 900 12px ui-monospace,Consolas,monospace | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `16px` | `.frame` 的 `padding` |
| 布局间距 | `9px` | `.actions` 的 `gap` |
| 圆角 | `50% 50% 10% 10%` | `.portrait:before` 的 `border-radius` |
| 边框或阴影 | `3px solid var(--black)` | `.bar` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.actions button` | padding: 13px | border: 2px solid var(--white); background: transparent; color: var(--white); font-weight: 900 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.work` | min-height: 260px; padding: 18px | border: 3px solid var(--black); text-align: left; color: var(--black); font: inherit | .work:hover → filter: contrast(1.12); transform: rotate(-.5deg); .work:hover → transform: none |
| 内容容器 `.bar` | height: 46px; display: flex; padding: 0 14px | border: 3px solid var(--black); background: var(--white); font: 900 12px ui-monospace,Consolas,monospace | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .layout → grid-template-columns: 1fr; .portrait → max-height: 300px; .bio h1 → font-size: 46px; .grid → grid-template-columns: 1fr; .work → min-height: 220px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“酸性作品簿 · 个人主页” → “LIN—SHE / VISUAL SYSTEMS” → “上海 ↔ 任何有好招牌的街区 / AVAILABLE FOR SELECTED PROJECTS” → “林她” → “LIN SHE” → “视觉导演 / 字体收藏者 / 慢跑新手” → “为文化、餐饮与公共空间建立有脾气的视觉系统。相信好识别不等于大声，好玩也可以很准确。” → “26” → “PROJECTS” → “8.4k” → “FOLLOWERS” → “12”。控件占位或辅助标签包括：“林她的几何肖像”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.toast` 状态变化 | transition: .2s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; .work:hover → transform: none |
| `.toast` 状态变化 | transition: .2s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; .work:hover → transform: none |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.layout 与 .bar 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#dfff00`、`#f5f5ef`、`#ff4fa0`、`#d2d2cc`、`#0a0a0a` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.actions button`、输入、选择或次操作 `.work` 与 内容容器 `.bar` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“酸性作品簿 · 个人主页”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
