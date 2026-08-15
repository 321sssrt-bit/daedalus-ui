# 019 市集小票

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`019-market-receipt.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--chalk); color: var(--ink) |
| 主要结构 `.receipt` | max-width: 780px; width: 100%; margin: auto; padding: 34px 42px 50px | position: relative | background: var(--paper); box-shadow: 18px 20px 0 #0b211b |
| 关键内容区 `.market` | min-height: 100vh; padding: 36px; gap: 44px | display: grid; grid-template-columns: minmax(260px,.7fr) minmax(520px,1.3fr); gap: 44px | background: radial-gradient(circle at 12% 20%,rgba(255,255,255,.06) 0 1px,transparent 2px),var(--chalk) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--chalk` | `#18372e` | 品牌或局部强调 |
| `--paper` | `#fffdf2` | 容器与表面 |
| `--ink` | `#15211d` | 主要文字与高对比边界 |
| `--muted` | `#68736d` | 辅助文字与弱化信息 |
| `--orange` | `#ff6b35` | 品牌或局部强调 |
| `--mint` | `#cdebd8` | 品牌或局部强调 |
| `--danger` | `#bc2f2a` | 错误与危险反馈 |
| `--literal-8` | `#a8c8bc` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-monospace,"Cascadia Mono",Consolas,"Microsoft YaHei",monospace | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.aside h1` | Georgia,"SimSun",serif | font-size: 66px; line-height: .95 | 由 font 简写或继承确定 |
| 分区标题 `.hours` | 继承页面字体 | line-height: 1.8 | 由 font 简写或继承确定 |
| 辅助文字 `.meta` | 继承页面字体 | font-size: 11px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `36px` | `.market` 的 `padding` |
| 布局间距 | `44px` | `.market` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `2px solid var(--mint)` | `.stamp` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.checkout` | width: 100%; padding: 17px; margin-top: 28px | border: 0; background: var(--orange); color: #1a1a16; font: 900 15px inherit; box-shadow: 5px 5px 0 var(--ink) | .checkout:hover → box-shadow: 3px 3px 0 var(--ink) |
| 输入、选择或次操作 `.remove` | margin-top: 12px | border: 0; background: transparent; color: var(--danger); font: inherit; font-size: 11px | 未声明独立状态；保持默认样式 |
| 内容容器 `.item` | display: grid; padding: 18px 0 | border-bottom: 1px dashed #b8b8ad | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .market → grid-template-columns: 1fr; padding: 18px; .aside → min-height: 280px; .aside h1 → font-size: 50px; .receipt → padding: 26px 24px; .item → grid-template-columns: 58px 1fr auto | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“市集小票 · 购物车” → “今 日 采 买” → “青苔” → “周末市集” → “新鲜抵达 / 08:00—20:00” → “产地直送 / 当日分装” → “订单编号 MKT-0719” → “你的藤编篮” → “价格已含包装回收押金” → “秋月梨 · 4 枚” → “河北赵县 / 今日采收” → “36.00”。控件占位或辅助标签包括：“购物车小票”、“减少数量”、“增加数量”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.receipt 与 .market 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#18372e`、`#15211d`、`#cdebd8`、`#fffdf2`、`#ff6b35` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.checkout`、输入、选择或次操作 `.remove` 与 内容容器 `.item` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“市集小票 · 购物车”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
