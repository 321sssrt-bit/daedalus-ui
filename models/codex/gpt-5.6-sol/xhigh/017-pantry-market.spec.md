# 017 坡上食集

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`017-pantry-market.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.header` | padding: 22px 34px | display: grid; grid-template-columns: 1fr auto 1fr; align-items: center | background: var(--surface); border-bottom: 1px solid #cfc3aa |
| 关键内容区 `.products` | gap: 18px | display: grid; grid-template-columns: repeat(3,1fr); gap: 18px | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#f3ead8` | 页面或区域背景 |
| `--surface` | `#fffaf0` | 容器与表面 |
| `--text` | `#2d3a2d` | 主要文字与高对比边界 |
| `--muted` | `#7b7a68` | 辅助文字与弱化信息 |
| `--accent` | `#c64f32` | 主要操作与强调状态 |
| `--success` | `#397453` | 成功反馈 |
| `--danger` | `#b53d36` | 错误与危险反馈 |
| `--olive` | `#697b45` | 品牌或局部强调 |
| `--mustard` | `#d9ad45` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-sans-serif,system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.herocopy h1` | 500 clamp(54px,7vw,96px)/.9 Georgia,"Songti SC",serif | font 简写中声明 | letter-spacing: -.06em |
| 分区标题 `.cathead h2` | 500 38px Georgia,"Songti SC",serif | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.eyebrow` | 继承页面字体 | font-size: 11px | font-weight: 900; letter-spacing: .13em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `22px 34px` | `.header` 的 `padding` |
| 布局间距 | `26px` | `.nav` 的 `gap` |
| 圆角 | `50%` | `.circle` 的 `border-radius` |
| 边框或阴影 | `1px solid #cfc3aa` | `.header` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.add` | width: 38px; height: 38px; border-radius: 50% | border: 1px solid var(--text); border-radius: 50%; background: transparent; font-size: 22px | .add:hover,.add.added → background: var(--text); color: white |
| 输入、选择或次操作 `.save` | width: 36px; height: 36px; border-radius: 50% | border: 0; border-radius: 50%; background: #fffaf0cc; font-size: 18px | .save.saved → color: var(--accent) |
| 内容容器 `.product` | 未单独声明 | background: var(--surface); border: 1px solid #d5c8ad | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:900px)` | .products → grid-template-columns: 1fr 1fr; .hero → grid-template-columns: 1fr; .stilllife → min-height: 360px; .nav → display: none; .header → grid-template-columns: 1fr auto | 交互流程与内容顺序不变 |
| `(max-width:560px)` | .products → grid-template-columns: 1fr; .catalog → padding: 34px 16px; .header → padding: 18px; .herocopy → padding: 46px 24px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“坡上食集 · 商店首页” → “坡上食集” → “HILLSIDE PANTRY” → “本周鲜到” → “山野调味” → “慢食礼盒” → “AUGUST HARVEST · 08” → “把山坡上的” → “八月带回家。” → “这一季的番茄、香草和小果实，被做成耐放却仍有新鲜气息的日常食物。每一罐都能追到产地和制作人。” → “逛本周新鲜到货 ↓” → “产地：云南大理 · 本周制作”。控件占位或辅助标签包括：“搜索”、“购物袋”、“收藏”、“加入购物袋”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.toast` 状态变化 | transition: .2s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important; .toast → display: none; .toast.show → display: block |
| `.toast` 状态变化 | transition: .2s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important; .toast → display: none; .toast.show → display: block |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.header 与 .products 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#d9ad45`、`#397453`、`#7b7a68`、`#fffaf0`、`#b53d36` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.add`、输入、选择或次操作 `.save` 与 内容容器 `.product` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:900px)` 条件下，布局按响应式表变化且“坡上食集 · 商店首页”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
