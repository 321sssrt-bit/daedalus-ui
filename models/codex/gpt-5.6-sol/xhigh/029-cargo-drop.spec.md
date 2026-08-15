# 029 行李转运台

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`029-cargo-drop.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--terminal); color: var(--ink) |
| 主要结构 `.file` | gap: 16px; padding: 16px 18px; margin: 10px 0 | display: grid; grid-template-columns: 52px 1fr 110px auto; gap: 16px; align-items: center | background: var(--paper); box-shadow: 5px 5px 0 #111 |
| 关键内容区 `.ceiling` | height: 74px; padding: 0 clamp(24px,5vw,70px) | display: flex; align-items: center; justify-content: space-between | background: var(--ink); color: var(--paper) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--terminal` | `#d8d4c8` | 品牌或局部强调 |
| `--belt` | `#292e2f` | 品牌或局部强调 |
| `--paper` | `#fff9df` | 容器与表面 |
| `--ink` | `#202526` | 主要文字与高对比边界 |
| `--muted` | `#687071` | 辅助文字与弱化信息 |
| `--orange` | `#f36b2b` | 品牌或局部强调 |
| `--green` | `#4c8668` | 成功反馈 |
| `--red` | `#c8493d` | 错误与危险反馈 |
| `--yellow` | `#f4c447` | 主要操作与强调状态 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.heading h1` | 继承页面字体 | font-size: 42px | letter-spacing: -2px |
| 分区标题 `.belt-head h2` | 继承页面字体 | font-size: 16px | 由 font 简写或继承确定 |
| 辅助文字 `.code` | 700 13px ui-monospace,Consolas,monospace | font 简写中声明 | letter-spacing: 2px |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `0 clamp(24px,5vw,70px)` | `.ceiling` 的 `padding` |
| 布局间距 | `16px` | `.file` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `3px dashed var(--ink)` | `.drop` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.drop button` | padding: 11px 18px; margin-top: 17px | border: 0; background: var(--orange); color: white; font-weight: 800 | .drop:focus-within,.process button:focus-visible,.remove:focus-visible → outline: 3px solid var(--orange) |
| 输入、选择或次操作 `.drop` | min-height: 210px; display: grid; padding: 30px | border: 3px dashed var(--ink); background: #e7e3d7; text-align: center | .drop:focus-within,.process button:focus-visible,.remove:focus-visible → outline: 3px solid var(--orange) |
| 内容容器 `.message` | 未单独声明 | color: var(--green); font-weight: 800 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:720px)` | .heading → display: block; .heading p → margin-top: 8px; .file → grid-template-columns: 42px 1fr auto; .file .state → grid-column: 2; .process → display: block | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“行李转运台 · 文件上传” → “TRANSFER DESK // BAY 04” → “14:36” → “文件转运台” → “下一班处理任务将在 15:00 发车” → “把文件放上转运带” → “PDF、PNG、CSV · 单件不超过 200 MB” → “选择本机文件” → “待转运行李” → “02 PIECES / 31.8 MB” → “PDF” → “北岸场地勘察.pdf”。控件占位或辅助标签包括：“删除北岸场地勘察.pdf”、“删除客流记录”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.file 与 .ceiling 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#202526`、`#f36b2b`、`#d8d4c8`、`#c8493d`、`#f4c447` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.drop button`、输入、选择或次操作 `.drop` 与 内容容器 `.message` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:720px)` 条件下，布局按响应式表变化且“行李转运台 · 文件上传”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
