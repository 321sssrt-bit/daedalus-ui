# 016 混合工作室名册

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`016-studio-roster.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--surface); color: var(--text) |
| 主要结构 `.modal` | inset: 0; padding: 20px | position: fixed; display: none; place-items: center | background: #171717bb; z-index: 3 |
| 关键内容区 `.profile` | width: min(700px,100%) | display: grid; grid-template-columns: 220px 1fr | background: var(--bg); border: 3px solid var(--text); box-shadow: 12px 12px 0 var(--accent) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#ebff52` | 页面或区域背景 |
| `--surface` | `#f7f5ef` | 容器与表面 |
| `--text` | `#171717` | 主要文字与高对比边界 |
| `--muted` | `#66645f` | 辅助文字与弱化信息 |
| `--accent` | `#5d45d8` | 主要操作与强调状态 |
| `--success` | `#26754f` | 成功反馈 |
| `--danger` | `#c43d3d` | 错误与危险反馈 |
| `--orange` | `#ff7451` | 品牌或局部强调 |
| `--cyan` | `#78d5dc` | 主要操作与强调状态 |
| `--pink` | `#ed9ac2` | 主要文字与高对比边界 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.head h1` | 继承页面字体 | font-size: clamp(46px,7vw,92px); line-height: .82 | letter-spacing: -.08em |
| 分区标题 `.info h2` | 继承页面字体 | font-size: 19px | 由 font 简写或继承确定 |
| 辅助文字 `.head .meta` | 800 12px/1.5 monospace | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `28px 36px` | `.head` 的 `padding` |
| 布局间距 | `20px` | `.tools` 的 `gap` |
| 圆角 | `18px` | `.filters button` 的 `border-radius` |
| 边框或阴影 | `3px solid var(--text)` | `.head` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.filters button` | height: 36px; padding: 0 15px; border-radius: 18px | border: 2px solid var(--text); background: white; border-radius: 18px; font-weight: 800 | .filters button.active → background: var(--text); color: white |
| 输入、选择或次操作 `.contact` | height: 46px; padding: 0 18px | border: 2px solid var(--text); background: var(--text); color: white; font-weight: 900 | 未声明独立状态；保持默认样式 |
| 内容容器 `.search` | height: 40px | border: 0; border-bottom: 2px solid var(--text); background: transparent; font-size: 14px | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:980px)` | .roster → grid-template-columns: repeat(3,1fr) | 交互流程与内容顺序不变 |
| `(max-width:720px)` | .roster → grid-template-columns: 1fr 1fr; padding: 18px; .tools → display: grid; padding: 18px; .search → width: 100%; .profile → grid-template-columns: 1fr; .bigface → height: 150px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“混合工作室 · 成员目录” → “谁在” → “工作室？” → “MIXED STUDIO” → “24 MEMBERS / 6 CITIES” → “全部” → “设计” → “内容” → “技术” → “在线” → “林夏” → “视觉设计 · 上海”。控件占位或辅助标签包括：“输入名字或专长”、“搜索成员”、“关闭”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.person` 状态变化 | transition: .16s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important |
| `.person` 状态变化 | transition: .16s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.modal 与 .profile 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#ff7451`、`#66645f`、`#171717`、`#78d5dc`、`#26754f` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.filters button`、输入、选择或次操作 `.contact` 与 内容容器 `.search` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:980px)` 条件下，布局按响应式表变化且“混合工作室 · 成员目录”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
