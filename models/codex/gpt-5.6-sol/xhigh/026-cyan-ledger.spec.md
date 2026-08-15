# 026 青光账单

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`026-cyan-ledger.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--black); color: var(--text) |
| 主要结构 `.layout` | gap: 18px; margin-top: 18px | display: grid; grid-template-columns: 310px 1fr; gap: 18px | 未单独声明 |
| 关键内容区 `.notice` | padding: 18px; margin-top: 24px; gap: 20px | display: flex; justify-content: space-between; gap: 20px | border: 1px solid var(--grid); color: var(--muted) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--black` | `#061013` | 品牌或局部强调 |
| `--panel` | `#0a1b20` | 容器与表面 |
| `--grid` | `#17343b` | 品牌或局部强调 |
| `--cyan` | `#45f3da` | 主要操作与强调状态 |
| `--text` | `#d8fff8` | 主要文字与高对比边界 |
| `--muted` | `#78a49d` | 辅助文字与弱化信息 |
| `--amber` | `#ffc857` | 品牌或局部强调 |
| `--red` | `#ff6b6b` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-monospace,"Cascadia Mono",Consolas,"Microsoft YaHei",monospace | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.plan h1` | 继承页面字体 | font-size: 29px | 由 font 简写或继承确定 |
| 分区标题 `.ledger h2` | 继承页面字体 | font-size: 22px | 由 font 简写或继承确定 |
| 辅助文字 `.top` | 继承页面字体 | font-size: 12px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `26px` | `.screen` 的 `padding` |
| 布局间距 | `18px` | `.layout` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `1px solid var(--grid)` | `.top` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.method button` | padding: 0 | border: 0; background: transparent; color: var(--amber); font: inherit | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.change` | width: 100%; padding: 12px; margin-top: 26px | border: 1px solid var(--cyan); background: transparent; color: var(--cyan); font: inherit | 未声明独立状态；保持默认样式 |
| 内容容器 `.invoice` | padding: 5px | border: 0; background: transparent; color: var(--amber); font: inherit | .invoice:hover → text-decoration: underline |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:820px)` | .layout → grid-template-columns: 1fr; .table → min-width: 650px; .ledger → overflow: auto; .screen → padding: 14px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“青光账单 · Billing Console” → “NEONSTACK // BILLING” → “workspace: northstar-lab UTC+08:00” → “$ current_plan” → “PRO / 8 SEATS” → “团队自动化、共享运行记录与 90 天历史。” → “本周期运行” → “6,840 / 10,000” → “距重置还有 12 天” → “下次扣款 · 2026-09-01” → “¥ 1,280” → “含税 / 月付”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.layout 与 .notice 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#0a1b20`、`#061013`、`#ffc857`、`#ff6b6b`、`#17343b` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.method button`、输入、选择或次操作 `.change` 与 内容容器 `.invoice` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:820px)` 条件下，布局按响应式表变化且“$ current_plan”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
