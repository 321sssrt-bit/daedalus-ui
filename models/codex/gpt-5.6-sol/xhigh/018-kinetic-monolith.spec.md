# 018 动力方碑

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`018-kinetic-monolith.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--paper); color: var(--ink) |
| 主要结构 `.shell` | min-height: 100vh | display: grid; grid-template-columns: 88px 1fr | 未单独声明 |
| 关键内容区 `.rail` | padding: 28px 0 | display: flex; flex-direction: column; align-items: center; justify-content: space-between | border-right: 1px solid var(--ink) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--paper` | `#f2efe6` | 容器与表面 |
| `--ink` | `#11120f` | 主要文字与高对比边界 |
| `--muted` | `#6b6c64` | 辅助文字与弱化信息 |
| `--blue` | `#2249ff` | 品牌或局部强调 |
| `--red` | `#ef3e2f` | 错误与危险反馈 |
| `--line` | `#c9c7bd` | 描边与分隔 |
| `--white` | `#fffdf6` | 品牌或局部强调 |
| `--literal-8` | `#d7d3c4` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.details h1` | 继承页面字体 | font-size: clamp(54px,7vw,98px); line-height: .84 | letter-spacing: -7px |
| 分区标题 `button` | inherit | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.price small` | 继承页面字体 | font-size: 13px | font-weight: 500 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `28px 0` | `.rail` 的 `padding` |
| 布局间距 | `8px` | `.choices` 的 `gap` |
| 圆角 | `50%` | `.halo` 的 `border-radius` |
| 边框或阴影 | `1px solid var(--ink)` | `.rail` 的 `border-right` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `button` | 未单独声明 | font: inherit | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.buy` | margin-top: 26px; padding: 20px 24px | border: 0; background: var(--blue); color: white; font-weight: 900; box-shadow: 8px 8px 0 var(--ink) | .buy:hover → box-shadow: 5px 5px 0 var(--ink); .buy:focus-visible,.choice:focus-visible,.swatch:focus-visible → outline: 3px solid var(--red) |
| 内容容器 `.details` | padding: clamp(40px,6vw,82px); display: flex | 未单独声明 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .shell → grid-template-columns: 52px 1fr; .main → grid-template-columns: 1fr; .stage → min-height: 440px; .machine → height: 350px; .details → padding: 42px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“动力方碑 · ARC S1” → “A—1” → “OBJECTS FOR EVERY MORNING” → “018/050” → “2026 / EDITION 01” → “ARC OBJECTS” → “精密研磨器” → “ARC” → “S1” → “把清晨压缩成一枚准确的刻度。64 mm 平刀、零残粉风道与磁吸接粉杯，适合手冲和意式之间频繁切换。” → “¥ 2,680” → “含两年保修”。控件占位或辅助标签包括：“商品主视觉”、“ARC S1 磨豆机”、“曜石黑”、“信号红”、“岩灰”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.buy` 状态变化 | transition: .18s transform,.18s box-shadow | 状态类或伪类改变对应 CSS 属性 | *,*::before,*::after → scroll-behavior: auto!important; transition: none!important |
| `.buy` 状态变化 | transition: .18s transform,.18s box-shadow | 状态类或伪类改变对应 CSS 属性 | *,*::before,*::after → scroll-behavior: auto!important; transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .rail 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#6b6c64`、`#2249ff`、`#fffdf6`、`#ef3e2f`、`#11120f` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `button`、输入、选择或次操作 `.buy` 与 内容容器 `.details` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“动力方碑 · ARC S1”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
