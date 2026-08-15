# 024 午夜账房

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`024-midnight-ledger.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--navy); color: var(--cream) |
| 主要结构 `.shell` | max-width: 1260px; margin: auto; min-height: 100vh | display: grid; grid-template-columns: 1.05fr .95fr | 未单独声明 |
| 关键内容区 `.seal` | width: 72px; height: 72px; margin: auto | display: grid; place-items: center | border: 1px solid var(--green); color: var(--green); border-radius: 50% |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--navy` | `#071522` | 品牌或局部强调 |
| `--panel` | `#0d2233` | 容器与表面 |
| `--cream` | `#f4eedf` | 品牌或局部强调 |
| `--muted` | `#90a0ab` | 辅助文字与弱化信息 |
| `--gold` | `#c9a65b` | 品牌或局部强调 |
| `--green` | `#72ba91` | 成功反馈 |
| `--red` | `#d46f68` | 错误与危险反馈 |
| `--literal-8` | `#294052` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC","SimSun",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.order h1` | 继承页面字体 | font-size: 52px | font-weight: 400 |
| 分区标题 `.item h2` | 继承页面字体 | font-size: 18px | font-weight: 400 |
| 辅助文字 `.brand` | 700 11px Arial,"Microsoft YaHei",sans-serif | font 简写中声明 | letter-spacing: 4px |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `54px clamp(28px,5vw,74px)` | `.order` 的 `padding` |
| 布局间距 | `18px` | `.item` 的 `gap` |
| 圆角 | `50%` | `.idx` 的 `border-radius` |
| 边框或阴影 | `1px solid #294052` | `.order` 的 `border-right` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.receipt button` | padding: 12px 24px | background: transparent; border: 1px solid var(--cream); color: var(--cream) | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.method:has(input:checked)` | 未单独声明 | border-color: var(--gold); background: rgba(201,166,91,.08) | .method:focus-within,.confirm:focus-visible → outline: 3px solid var(--cream) |
| 内容容器 `.item` | display: grid; padding: 22px 0 | border-bottom: 1px solid #294052 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .shell → grid-template-columns: 1fr; .order → border-right: 0; border-bottom: 1px solid #294052; .order h1 → margin-top: 38px; .pay → min-height: 620px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“午夜账房 · 结账” → “NOCTURNE HOUSE · SHANGHAI” → “订单终章” → “在落款之前，再核对一次你选择的物件。” → “月相黄铜台灯” → “拉丝黄铜 / 暖光 2700K / 1 件” → “¥ 1,860” → “II” → “黑檀木调光钮” → “替换配件 / 1 件” → “¥ 180” → “商品”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .seal 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#0d2233`、`#72ba91`、`#071522`、`#c9a65b`、`#294052` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.receipt button`、输入、选择或次操作 `.method:has(input:checked)` 与 内容容器 `.item` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“午夜账房 · 结账”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
