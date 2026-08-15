# 013 往来事务所

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`013-correspondence-desk.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh; padding: 22px | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.desk` | height: calc(100vh - 44px); min-height: 650px | display: grid; grid-template-columns: 205px 340px 1fr | background: var(--surface); border: 1px solid #8e8578; box-shadow: 0 22px 60px #544a3c44; overflow: hidden |
| 关键内容区 `.listhead` | height: 84px; padding: 20px | display: flex; justify-content: space-between; align-items: center | border-bottom: 3px double var(--line) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#d8d0c3` | 页面或区域背景 |
| `--surface` | `#f7f3ea` | 容器与表面 |
| `--text` | `#26231f` | 主要文字与高对比边界 |
| `--muted` | `#756e64` | 辅助文字与弱化信息 |
| `--accent` | `#9b2f2c` | 主要操作与强调状态 |
| `--success` | `#3d7455` | 成功反馈 |
| `--danger` | `#b53d36` | 错误与危险反馈 |
| `--line` | `#bdb4a5` | 描边与分隔 |
| `--ink` | `#183c4b` | 主要文字与高对比边界 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.listhead h1` | 继承页面字体 | font-size: 22px | 由 font 简写或继承确定 |
| 分区标题 `.meta h2` | 继承页面字体 | font-size: 32px | font-weight: 500 |
| 辅助文字 `.brand small` | 700 10px monospace | font 简写中声明 | letter-spacing: .14em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `22px` | `body` 的 `padding` |
| 布局间距 | `8px` | `.tools` 的 `gap` |
| 圆角 | `50%` | `.letter.unread:before` 的 `border-radius` |
| 边框或阴影 | `1px solid #8e8578` | `.desk` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.nav button.folder` | padding: 11px 8px | border: 0; background: transparent; color: #b9ccd1; text-align: left | .nav button.folder.active → color: white |
| 输入、选择或次操作 `.filter` | padding: 7px 10px | border: 1px solid var(--line); background: transparent; font: 600 11px system-ui | 未声明独立状态；保持默认样式 |
| 内容容器 `.compose` | height: 44px; margin: 34px 0 28px | border: 1px solid #f3ece0; background: transparent; color: white; font-weight: 700 | .compose:hover → background: #f3ece0; color: var(--ink) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:900px)` | .desk → grid-template-columns: 70px 300px 1fr; .nav → padding: 22px 12px; .brand → font-size: 0; .brand:before → content: "往"; font-size: 22px; .brand small,.nav .folder,.nav footer → font-size: 0 | 交互流程与内容顺序不变 |
| `(max-width:700px)` | body → padding: 0; .desk → height: 100vh; grid-template-columns: 1fr; .nav,.list → display: none; .read → padding: 24px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“往来事务所 · 收件箱” → “往来” → “事务所” → “CORRESPONDENCE / 06” → “＋ 写一封信” → “收件箱 · 3” → “星标来信 · 4” → “归档 · 128” → “本地邮局同步正常” → “最后收信：10:24” → “今日来信” → “只看未读”。控件占位或辅助标签包括：“星标”、“归档”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.desk 与 .listhead 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#d8d0c3`、`#3d7455`、`#9b2f2c`、`#b53d36`、`#756e64` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.nav button.folder`、输入、选择或次操作 `.filter` 与 内容容器 `.compose` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:900px)` 条件下，布局按响应式表变化且“往来事务所 · 收件箱”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
