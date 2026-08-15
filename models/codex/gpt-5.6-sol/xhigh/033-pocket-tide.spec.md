# 033 掌中潮汐

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`033-pocket-tide.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh; padding: 24px | display: grid; place-items: center | background: #cbbca4; color: var(--ink) |
| 主要结构 `.phone` | width: min(390px,100%); height: min(820px,calc(100vh - 32px)); min-height: 680px | position: relative | background: var(--sand); border: 8px solid var(--ink); border-radius: 42px; overflow: hidden; box-shadow: 0 24px 60px rgba(36,50,45,.3) |
| 关键内容区 `.balance` | margin: 12px 16px 0; padding: 24px 22px 20px | position: relative | background: var(--paper); border: 2px solid var(--ink); box-shadow: 5px 6px 0 var(--ink) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--sand` | `#efe1ca` | 品牌或局部强调 |
| `--paper` | `#fff8e8` | 容器与表面 |
| `--ink` | `#24322d` | 主要文字与高对比边界 |
| `--muted` | `#7b817a` | 辅助文字与弱化信息 |
| `--orange` | `#d7643a` | 品牌或局部强调 |
| `--mint` | `#9fc9b2` | 品牌或局部强调 |
| `--green` | `#347659` | 成功反馈 |
| `--red` | `#b84c45` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | "Avenir Next","Microsoft YaHei",Arial,sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.top b` | 继承页面字体 | font-size: 18px | 由 font 简写或继承确定 |
| 分区标题 `.flow h2` | 22px Georgia,serif | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.amount small` | 14px Arial,sans-serif | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px` | `body` 的 `padding` |
| 布局间距 | `10px` | `.actions` 的 `gap` |
| 圆角 | `42px` | `.phone` 的 `border-radius` |
| 边框或阴影 | `8px solid var(--ink)` | `.phone` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.flow-head button` | 未单独声明 | border: 0; background: transparent; color: var(--orange); font-size: 11px | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.sheet input` | width: 100%; padding: 12px; margin-top: 6px | border: 1px solid var(--ink); background: white | .sheet.show → transform: none |
| 内容容器 `.message` | min-height: 16px; margin-top: 8px | font-size: 11px; color: var(--green) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | body → padding: 0; .phone → width: 100%; height: 100vh; border: 0; border-radius: 0 | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“掌中潮汐 · 钱包” → “潮汐钱包” → “可用余额” → “8,642.50” → “↑ 本月净流入 ¥ 1,280” → “转出” → “收款” → “银行卡” → “最近潮汐” → “查看全部” → “今天 · 8 月 14 日” → “渡口咖啡”。控件占位或辅助标签包括：“转出资金”、“关闭”、“姓名或手机号”、“0.00”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.sheet` 状态变化 | transition: .25s transform | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important |
| `.sheet` 状态变化 | transition: .25s transform | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .balance 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#7b817a`、`#fff8e8`、`#347659`、`#9fc9b2`、`#b84c45` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.flow-head button`、输入、选择或次操作 `.sheet input` 与 内容容器 `.message` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“掌中潮汐 · 钱包”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
