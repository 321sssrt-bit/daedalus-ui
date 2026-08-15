# 025 静页账户

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`025-quiet-folds.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--wash); color: var(--ink) |
| 主要结构 `.shell` | max-width: 1050px; margin: auto; padding: 48px 28px | 未单独声明 | 未单独声明 |
| 关键内容区 `.row` | width: 100%; gap: 15px; padding: 22px 0 | display: grid; grid-template-columns: 44px 1fr auto; gap: 15px; align-items: center | border: 0; background: transparent; color: inherit |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--wash` | `#e8e5dc` | 品牌或局部强调 |
| `--paper` | `#f8f6ef` | 容器与表面 |
| `--ink` | `#252b2d` | 主要文字与高对比边界 |
| `--muted` | `#747b78` | 辅助文字与弱化信息 |
| `--indigo` | `#334d5c` | 品牌或局部强调 |
| `--clay` | `#c76d52` | 主要操作与强调状态 |
| `--green` | `#6a806a` | 成功反馈 |
| `--line` | `#cbc7bb` | 描边与分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | "Yu Gothic UI","Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.identity h1` | 继承页面字体 | font-size: 25px | 由 font 简写或继承确定 |
| 分区标题 `.side h2` | 继承页面字体 | font-size: 13px | 由 font 简写或继承确定 |
| 辅助文字 `.mark` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 700 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `48px 28px` | `.shell` 的 `padding` |
| 布局间距 | `12px` | `.mark` 的 `gap` |
| 圆角 | `50%` | `.mark i` 的 `border-radius` |
| 边框或阴影 | `50%` | `.mark i` 的 `border-radius` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.row` | width: 100%; display: grid; padding: 22px 0 | border: 0; background: transparent; color: inherit; text-align: left | .row:focus-visible → outline: 3px solid var(--clay) |
| 输入、选择或次操作 `.avatar` | width: 72px; height: 72px; border-radius: 50%; display: grid | border-radius: 50%; background: var(--paper); color: var(--indigo); font-size: 26px | 未声明独立状态；保持默认样式 |
| 内容容器 `.glyph` | width: 34px; height: 34px; border-radius: 50%; display: grid | border-radius: 50%; border: 1px solid var(--line); color: var(--indigo) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:720px)` | .identity → grid-template-columns: 58px 1fr; .avatar → width: 58px; height: 58px; .status → grid-column: 2; .groups → grid-template-columns: 1fr; .side → display: flex; gap: 20px; overflow: auto | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“静页账户 · 账号设置” → “折页 FOLD” → “设置 / 个人账户” → “闻溪” → “wenxi@fold.studio · 个人空间” → “已完成身份验证” → “账户目录” → “个人资料” → “安全” → “通知” → “姓名与公开资料” → “头像、显示名称、个人简介”。控件占位或辅助标签包括：“已开启”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .row 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#334d5c`、`#f8f6ef`、`#cbc7bb`、`#c76d52`、`#6a806a` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.row`、输入、选择或次操作 `.avatar` 与 内容容器 `.glyph` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:720px)` 条件下，布局按响应式表变化且“静页账户 · 账号设置”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
