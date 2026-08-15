# 001 夜航通行证

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`001-night-pass.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.shell` | min-height: 100vh | position: relative; display: grid; grid-template-columns: minmax(320px,1.2fr) minmax(420px,.8fr) | 未单独声明 |
| 关键内容区 `.panel` | margin: 24px; min-height: calc(100vh - 48px); padding: clamp(32px,5vw,68px) | display: flex; flex-direction: column; justify-content: center | background: color-mix(in srgb,var(--surface) 88%,transparent); border: 1px solid var(--line); border-radius: 28px; backdrop-filter: blur(22px); box-shadow: 0 30px 80px #0008 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#070914` | 页面或区域背景 |
| `--surface` | `#11152a` | 容器与表面 |
| `--text` | `#f7f4ff` | 主要文字与高对比边界 |
| `--muted` | `#9ba4c4` | 辅助文字与弱化信息 |
| `--accent` | `#9d7cff` | 主要操作与强调状态 |
| `--success` | `#57e3b4` | 成功反馈 |
| `--danger` | `#ff6e8a` | 错误与危险反馈 |
| `--line` | `#282e4c` | 描边与分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Inter,ui-sans-serif,system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.hero h1` | 继承页面字体 | font-size: clamp(54px,7.4vw,112px); line-height: .86 | letter-spacing: -.07em |
| 分区标题 `.panel h2` | 继承页面字体 | font-size: 32px | 由 font 简写或继承确定 |
| 辅助文字 `.eyebrow` | 700 12px/1 system-ui | font 简写中声明 | letter-spacing: .18em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `52px 6vw` | `.brand` 的 `padding` |
| 布局间距 | `12px` | `.mark` 的 `gap` |
| 圆角 | `50%` | `.planet` 的 `border-radius` |
| 边框或阴影 | `1px solid var(--accent)` | `.planet` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.primary` | height: 56px; border-radius: 14px | border: 0; border-radius: 14px; background: var(--accent); color: #0c0820; font-weight: 800; font-size: 15px | .primary:hover → transform: translateY(-2px) |
| 输入、选择或次操作 `input` | width: 100%; height: 54px; border-radius: 14px; padding: 0 50px 0 16px | border: 1px solid var(--line); border-radius: 14px; background: #0b0e1e; color: var(--text); font-size: 16px | input:focus → box-shadow: 0 0 0 4px #9d7cff25 |
| 内容容器 `.panel` | margin: 24px; min-height: calc(100vh - 48px); border-radius: 28px; padding: clamp(32px,5vw,68px); display: flex | background: color-mix(in srgb,var(--surface) 88%,transparent); border: 1px solid var(--line); border-radius: 28px; box-shadow: 0 30px 80px #0008 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:820px)` | .shell → grid-template-columns: 1fr; .brand → min-height: 48vh; .panel → margin: 0 16px 16px; min-height: auto; .hero h1 → font-size: 60px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“夜航通行证 · 登录” → “ORBITAL / 夜航” → “private workspace · 04” → “回到你的” → “工作轨道” → “项目、决定和灵感都在原处。完成身份确认，继续上一段航程。” → “亚洲节点运行正常” → “欢迎回来” → “使用夜航账号进入控制台” → “账号” → “密码” → “显示”。控件占位或辅助标签包括：“登录表单”、“邮箱或成员编号”、“至少 8 位”、“显示密码”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `input` 状态变化 | transition: .2s | 状态类或伪类改变对应 CSS 属性 | *,*:before,*:after → scroll-behavior: auto!important; transition-duration: .01ms!important; animation-duration: .01ms!important; animation-iteration-count: 1!important |
| `.primary` 状态变化 | transition: transform .2s | 状态类或伪类改变对应 CSS 属性 | *,*:before,*:after → scroll-behavior: auto!important; transition-duration: .01ms!important; animation-duration: .01ms!important; animation-iteration-count: 1!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .panel 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#ff6e8a`、`#f7f4ff`、`#282e4c`、`#11152a`、`#9d7cff` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.primary`、输入、选择或次操作 `input` 与 内容容器 `.panel` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:820px)` 条件下，布局按响应式表变化且“夜航通行证 · 登录”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
