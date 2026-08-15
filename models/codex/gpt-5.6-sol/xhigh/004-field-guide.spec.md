# 004 微光野外指南

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`004-field-guide.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh; padding: 28px | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.book` | width: min(1180px,100%); min-height: calc(100vh - 56px); margin: auto | display: grid; grid-template-columns: 270px 1fr | background: var(--surface); border-radius: 26px; overflow: hidden; box-shadow: 0 30px 80px #071c1888 |
| 关键内容区 `.content` | padding: 38px clamp(34px,6vw,86px) | position: relative; display: flex; flex-direction: column | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#163832` | 页面或区域背景 |
| `--surface` | `#f5f0db` | 容器与表面 |
| `--text` | `#18352f` | 主要文字与高对比边界 |
| `--muted` | `#617269` | 辅助文字与弱化信息 |
| `--accent` | `#ffcc59` | 主要操作与强调状态 |
| `--success` | `#2f765e` | 成功反馈 |
| `--danger` | `#c85a43` | 错误与危险反馈 |
| `--night` | `#0d2925` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-rounded,"Microsoft YaHei",system-ui,sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.copy h1` | 继承页面字体 | font-size: clamp(42px,6vw,76px); line-height: .96 | letter-spacing: -.06em |
| 分区标题 `.logo` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 800; letter-spacing: .06em |
| 辅助文字 `.step i` | 继承页面字体 | font-size: 12px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `28px` | `body` 的 `padding` |
| 布局间距 | `24px` | `.steps` 的 `gap` |
| 圆角 | `26px` | `.book` 的 `border-radius` |
| 边框或阴影 | `26px` | `.book` 的 `border-radius` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.btn.primary` | 未单独声明 | background: var(--text); color: white | .btn:disabled → cursor: not-allowed |
| 输入、选择或次操作 `.btn` | height: 48px; border-radius: 24px; padding: 0 24px | border: 1px solid var(--text); border-radius: 24px; background: transparent; color: var(--text); font-weight: 800 | .btn:disabled → cursor: not-allowed |
| 内容容器 `.book` | width: min(1180px,100%); min-height: calc(100vh - 56px); margin: auto; border-radius: 26px; display: grid | background: var(--surface); border-radius: 26px; box-shadow: 0 30px 80px #071c1888 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:800px)` | body → padding: 0; .book → border-radius: 0; grid-template-columns: 1fr; .rail → padding: 18px 24px; display: grid; grid-template-columns: 1fr auto; .steps → display: none; .skip → grid-column: 2 | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“微光野外指南 · 新手引导” → “GLOW” → “FIELD” → “微光野” → “标记发现” → “结伴观察” → “带走记录” → “跳过介绍” → “FIELD NOTE · 01 / 03” → “看见一束光，” → “就把它标下来。” → “拍下叶片、云和街角的小发现。微光野会记录位置与时间，替你整理成一册私人自然日志。”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.book 与 .content 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#f5f0db`、`#2f765e`、`#163832`、`#ffcc59`、`#18352f` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.btn.primary`、输入、选择或次操作 `.btn` 与 内容容器 `.book` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:800px)` 条件下，布局按响应式表变化且“微光野外指南 · 新手引导”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
