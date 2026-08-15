# 010 胶带工场

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`010-sticky-yard.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | color: var(--text) |
| 主要结构 `.header` | height: 78px; padding: 0 30px | display: flex; justify-content: space-between; align-items: center | background: var(--surface); border-bottom: 2px solid #6f634a; box-shadow: 0 4px 0 #766b52 |
| 关键内容区 `.board` | padding: 30px; gap: 24px | display: grid; grid-template-columns: repeat(3,minmax(250px,1fr)); gap: 24px | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#c7b894` | 页面或区域背景 |
| `--surface` | `#efe5cf` | 容器与表面 |
| `--text` | `#2b261d` | 主要文字与高对比边界 |
| `--muted` | `#6f6654` | 辅助文字与弱化信息 |
| `--accent` | `#e95034` | 主要操作与强调状态 |
| `--success` | `#44765a` | 成功反馈 |
| `--danger` | `#bd4537` | 错误与危险反馈 |
| `--yellow` | `#f5d86f` | 主要操作与强调状态 |
| `--blue` | `#a9cce2` | 品牌或局部强调 |
| `--pink` | `#e9b6bc` | 主要文字与高对比边界 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | "Comic Sans MS",ui-rounded,"Microsoft YaHei",system-ui,sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.header h1` | 继承页面字体 | font-size: 26px | 由 font 简写或继承确定 |
| 分区标题 `.colhead h2` | 继承页面字体 | font-size: 18px | 由 font 简写或继承确定 |
| 辅助文字 `.meta` | 600 11px system-ui | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `0 30px` | `.header` 的 `padding` |
| 布局间距 | `24px` | `.board` 的 `gap` |
| 圆角 | `4px` | `.column` 的 `border-radius` |
| 边框或阴影 | `2px solid #6f634a` | `.header` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.move button` | padding: 5px 8px | border: 1px solid #8f846e; background: #f4ead5; font: 700 10px system-ui | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.dialog input` | width: 100%; height: 48px; padding: 0 12px | border: 2px solid var(--text); background: white; font-size: 15px | 未声明独立状态；保持默认样式 |
| 内容容器 `.card` | padding: 18px 16px 16px | background: #fff9e9; box-shadow: 3px 5px 9px #52482f42 | .card:hover → transform: rotate(0) translateY(-3px) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .board → grid-template-columns: repeat(3,280px); .header → padding: 0 16px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“胶带工场 · 看板” → “胶带工场” → “/ 秋季发布” → “＋ 新建一条” → “还没开工” → “文案” → “为新首页写三种开场句” → “周五” → “移到进行中 →” → “研究” → “整理六位用户的首屏反馈” → “8 月 18”。控件占位或辅助标签包括：“写清要完成的事”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.card` 状态变化 | transition: .16s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important |
| `.card` 状态变化 | transition: .16s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.header 与 .board 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#6f6654`、`#44765a`、`#e95034`、`#efe5cf`、`#c7b894` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.move button`、输入、选择或次操作 `.dialog input` 与 内容容器 `.card` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“胶带工场 · 看板”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
