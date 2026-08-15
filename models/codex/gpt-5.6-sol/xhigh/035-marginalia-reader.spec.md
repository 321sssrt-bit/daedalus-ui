# 035 页边茶室

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`035-marginalia-reader.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #c8bda9; color: var(--ink) |
| 主要结构 `.hero` | padding: 28px 26px 16px | 未单独声明 | 未单独声明 |
| 关键内容区 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto | position: relative | background: var(--paper); box-shadow: 0 24px 70px #463c3080; overflow: hidden |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--paper` | `#f2ead8` | 容器与表面 |
| `--card` | `#fffaf0` | 容器与表面 |
| `--ink` | `#332d25` | 主要文字与高对比边界 |
| `--muted` | `#837765` | 辅助文字与弱化信息 |
| `--tea` | `#6b8065` | 品牌或局部强调 |
| `--red` | `#a84e42` | 错误与危险反馈 |
| `--literal-7` | `#c8bda9` | HTML 中直接声明的局部色 |
| `--literal-8` | `#463c3080` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC","Microsoft YaHei",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.hero small` | 继承页面字体 | 16px / normal（浏览器默认） | letter-spacing: .12em |
| 分区标题 `.top b` | 继承页面字体 | font-size: 13px | letter-spacing: .18em |
| 辅助文字 `.mark` | 继承页面字体 | font-size: 22px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `22px 22px 12px` | `.top` 的 `padding` |
| 布局间距 | `未单独声明` | 由组件行逐项定义 |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `0 24px 70px #463c3080` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.tools button` | width: 34px; height: 30px | border: 1px solid #a99a83; background: var(--card) | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.start` | padding: 14px | border: 0; background: var(--ink); color: var(--card); font: 600 15px system-ui | 未声明独立状态；保持默认样式 |
| 内容容器 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto | background: var(--paper); box-shadow: 0 24px 70px #463c3080 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh; box-shadow: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“页边茶室” → “页边茶室 · 07” → “器物与日常” → “一只茶杯，如何记住手的温度” → “文 / 林见微 · 8 分钟阅读” → “A−” → “舒展” → “A＋” → “器物最诚实的部分，并不是刚离开窑火时的光泽，而是被日常缓慢改变之后的表面。” → “杯沿留下极浅的茶色，釉面在拇指常停的地方变得温润。它们不是瑕疵，是时间在物件上写下的小字。” → “真正耐看的东西，会把使用者也纳入设计。” → “因此，选择一只杯子时，不必先问它是否完美。把它握在手里，看看重量是否愿意停留。”。控件占位或辅助标签包括：“收藏”、“缩小字号”、“放大字号”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.toast` 状态变化 | transition: .2s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important |
| `.toast` 状态变化 | transition: .2s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.hero 与 .phone 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#c8bda9`、`#f2ead8`、`#6b8065`、`#332d25`、`#a84e42` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.tools button`、输入、选择或次操作 `.start` 与 内容容器 `.phone` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“页边茶室”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
