# 005 灯塔邮局

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`005-mail-lantern.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh; padding: 28px | display: grid; place-items: center | background: linear-gradient(#a8d0e4 0 62%,#6fadc8 62%); color: var(--text) |
| 主要结构 `.scene` | width: min(1050px,100%); gap: 70px | display: grid; grid-template-columns: 1fr 470px; align-items: center; gap: 70px | 未单独声明 |
| 关键内容区 `.card` | padding: 46px | position: relative | background: var(--surface); border-radius: 3px; box-shadow: 9px 10px 0 #234f6f |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#bcd9e8` | 页面或区域背景 |
| `--surface` | `#fffaf0` | 容器与表面 |
| `--text` | `#20344a` | 主要文字与高对比边界 |
| `--muted` | `#65798a` | 辅助文字与弱化信息 |
| `--accent` | `#e9683d` | 主要操作与强调状态 |
| `--success` | `#397a62` | 成功反馈 |
| `--danger` | `#be3e3e` | 错误与危险反馈 |
| `--navy` | `#234f6f` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-sans-serif,system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.card h1` | Georgia,"Songti SC",serif | font-size: 38px | 由 font 简写或继承确定 |
| 分区标题 `.card:before` | 800 10px monospace | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.icon` | 继承页面字体 | font-size: 36px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `28px` | `body` 的 `padding` |
| 布局间距 | `70px` | `.scene` 的 `gap` |
| 圆角 | `10px 10px 0 0` | `.lamp` 的 `border-radius` |
| 边框或阴影 | `10px 10px 0 0` | `.lamp` 的 `border-radius` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `input` | height: 52px; border-radius: 3px; padding: 0 14px | border: 2px solid #a4b5bc; border-radius: 3px; background: white; font-size: 16px; color: var(--text) | input:focus → box-shadow: 0 0 0 3px #234f6f22 |
| 输入、选择或次操作 `.field` | display: grid; margin: 28px 0 16px | 未单独声明 | 未声明独立状态；保持默认样式 |
| 内容容器 `.card:before` | border-radius: 50%; padding: 12px 9px | border: 2px solid var(--accent); border-radius: 50%; color: var(--accent); font: 800 10px monospace | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:820px)` | .scene → grid-template-columns: 1fr; .lighthouse → display: none; .card → max-width: 520px; margin: auto | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“灯塔邮局 · 找回密码” → “让灯塔把路寄给你” → “输入注册时的邮箱。若账号存在，我们会寄出一封仅 20 分钟有效的安全链接。” → “联系邮箱” → “寄出找回信” → “信件已寄出。请检查收件箱与垃圾邮件，” → “60” → “秒后可再次发送。” → “← 我想起密码了，回到登录”。控件占位或辅助标签包括：“海边灯塔插画”、“you@example.com”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.beam` 状态变化 | animation: sweep 6s ease-in-out infinite | 状态类或伪类改变对应 CSS 属性 | .beam → animation: none; .btn → transition: none |
| `.beam` 状态变化 | animation: sweep 6s ease-in-out infinite | 状态类或伪类改变对应 CSS 属性 | .beam → animation: none; .btn → transition: none |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.scene 与 .card 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#e9683d`、`#20344a`、`#397a62`、`#bcd9e8`、`#65798a` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `input`、输入、选择或次操作 `.field` 与 内容容器 `.card:before` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:820px)` 条件下，布局按响应式表变化且“灯塔邮局 · 找回密码”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
