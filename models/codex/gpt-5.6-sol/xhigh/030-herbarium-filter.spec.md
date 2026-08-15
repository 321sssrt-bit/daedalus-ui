# 030 植物标本筛

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`030-herbarium-filter.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--linen); color: var(--ink) |
| 主要结构 `.layout` | max-width: 1300px; margin: auto; min-height: calc(100vh - 91px) | display: grid; grid-template-columns: 270px 1fr | 未单独声明 |
| 关键内容区 `.plate` | height: 160px | position: relative; display: grid; place-items: center | background: #e2e5d3; overflow: hidden |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--linen` | `#ece8d8` | 描边与分隔 |
| `--paper` | `#faf8ed` | 容器与表面 |
| `--ink` | `#263329` | 主要文字与高对比边界 |
| `--muted` | `#738074` | 辅助文字与弱化信息 |
| `--forest` | `#315b3c` | 品牌或局部强调 |
| `--ochre` | `#be8a3c` | 品牌或局部强调 |
| `--red` | `#a94f45` | 错误与危险反馈 |
| `--line` | `#c8c6b7` | 描边与分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC","SimSun",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.filters h1` | 继承页面字体 | font-size: 21px | 由 font 简写或继承确定 |
| 分区标题 `.filter label.title` | 700 11px Arial,"Microsoft YaHei",sans-serif | font 简写中声明 | letter-spacing: 1px |
| 辅助文字 `.brand` | 继承页面字体 | font-size: 28px | letter-spacing: 4px |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `28px clamp(24px,5vw,70px)` | `.header` 的 `padding` |
| 布局间距 | `18px` | `.grid` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `1px solid var(--ink)` | `.header` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.clear` | padding: 8px 0 | border: 0; background: transparent; color: var(--red); font: 700 12px Arial,"Microsoft YaHei",sans-serif | input:focus-visible,select:focus-visible,.clear:focus-visible → outline: 3px solid var(--ochre) |
| 输入、选择或次操作 `.filter select,.filter input[type=search]` | width: 100%; padding: 10px | border: 1px solid var(--muted); background: var(--paper); color: var(--ink) | 未声明独立状态；保持默认样式 |
| 内容容器 `body` | margin: 0; min-height: 100vh | background: var(--linen); color: var(--ink) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:950px)` | .grid → grid-template-columns: repeat(2,1fr) | 交互流程与内容顺序不变 |
| `(max-width:720px)` | .layout → grid-template-columns: 1fr; .filters → border-right: 0; border-bottom: 1px solid var(--ink); .grid → grid-template-columns: 1fr; .header p → display: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“植物标本筛 · 筛选检索” → “北纬三十度植物志” → “FIELD NOTES / 2026 夏季采集” → “缩小标本范围” → “找到 6 份记录” → “名称检索” → “生境” → “全部生境” → “林下” → “水岸” → “岩隙” → “特征”。控件占位或辅助标签包括：“中文名或拉丁名”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.layout 与 .plate 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#be8a3c`、`#a94f45`、`#faf8ed`、`#263329`、`#c8c6b7` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.clear`、输入、选择或次操作 `.filter select,.filter input[type=search]` 与 内容容器 `body` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:950px)` 条件下，布局按响应式表变化且“植物标本筛 · 筛选检索”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
