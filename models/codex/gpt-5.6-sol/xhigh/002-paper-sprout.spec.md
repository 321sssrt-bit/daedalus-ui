# 002 纸芽编辑桌

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`002-paper-sprout.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.cover` | padding: 48px | display: flex; flex-direction: column; justify-content: space-between; position: relative | background: var(--ink); color: #f8f0df; overflow: hidden |
| 关键内容区 `.form` | width: min(520px,100%) | 未单独声明 | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#f2eadc` | 页面或区域背景 |
| `--surface` | `#fffdf8` | 容器与表面 |
| `--text` | `#253027` | 主要文字与高对比边界 |
| `--muted` | `#6f786e` | 辅助文字与弱化信息 |
| `--accent` | `#d94f36` | 主要操作与强调状态 |
| `--success` | `#357a55` | 成功反馈 |
| `--danger` | `#b6322b` | 错误与危险反馈 |
| `--literal-8` | `#f8f0df` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC","Noto Serif CJK SC",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.quote h1` | 继承页面字体 | font-size: clamp(46px,6vw,84px); line-height: .98 | font-weight: 500; letter-spacing: -.05em |
| 分区标题 `.form h2` | 继承页面字体 | font-size: 42px | 由 font 简写或继承确定 |
| 辅助文字 `.logo` | 800 22px/1 system-ui | font 简写中声明 | letter-spacing: .12em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `48px` | `.cover` 的 `padding` |
| 布局间距 | `18px` | `.grid` 的 `gap` |
| 圆角 | `48% 52% 60% 40%` | `.cover:after` 的 `border-radius` |
| 边框或阴影 | `80px solid #97a56a` | `.cover:after` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.cta` | width: 100%; height: 56px; border-radius: 2px 18px 2px 18px; margin-top: 10px | border: 0; background: var(--accent); color: white; font: 800 15px system-ui; border-radius: 2px 18px 2px 18px | .cta:hover → filter: brightness(.94) |
| 输入、选择或次操作 `input,select` | height: 52px; padding: 0 4px | border: 0; border-bottom: 2px solid #c8c1b5; background: transparent; font: 500 16px/1 system-ui; color: var(--text) | input:focus,select:focus → border-color: var(--accent) |
| 内容容器 `.role` | padding: 12px; border-radius: 10px | border: 1px solid #d8d0c4; background: #fffaf1; border-radius: 10px; font: 700 13px system-ui | .role.active → background: var(--text); color: white |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:820px)` | .page → grid-template-columns: 1fr; .cover → min-height: 42vh; .formwrap → margin: 0; padding: 38px 24px; border-radius: 0; .grid → grid-template-columns: 1fr | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“纸芽 · 注册” → “PAPERSPROUT” → “ISSUE 01 · BEGIN” → “从一页空白开始” → “把想法种成” → “一本作品。” → “为写作者、编辑与独立出版人准备的安静工作间。你的第一本刊物，可以从今天发芽。” → “© 2026 纸芽出版工具” → “CREATE YOUR DESK” → “建立你的编辑桌” → “两分钟完成，之后随时可以调整。” → “怎么称呼你”。控件占位或辅助标签包括：“例如：林夏”、“name@example.com”、“至少 8 位，建议包含数字”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.cover 与 .form 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#357a55`、`#d94f36`、`#f2eadc`、`#f8f0df`、`#b6322b` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.cta`、输入、选择或次操作 `input,select` 与 内容容器 `.role` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:820px)` 条件下，布局按响应式表变化且“纸芽 · 注册”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
