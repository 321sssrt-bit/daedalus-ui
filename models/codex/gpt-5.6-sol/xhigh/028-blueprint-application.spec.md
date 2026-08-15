# 028 蓝图申请册

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`028-blueprint-application.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--blue); color: var(--ink) |
| 主要结构 `.layout` | max-width: 1180px; margin: auto; padding: 30px; gap: 22px | display: grid; grid-template-columns: 240px 1fr; gap: 22px | 未单独声明 |
| 关键内容区 `.form` | padding: 42px 48px | 未单独声明 | background: var(--paper); box-shadow: 12px 12px 0 var(--deep) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--blue` | `#123f6a` | 品牌或局部强调 |
| `--deep` | `#092944` | 品牌或局部强调 |
| `--paper` | `#edf5f7` | 容器与表面 |
| `--ink` | `#14334a` | 主要文字与高对比边界 |
| `--muted` | `#627d8c` | 辅助文字与弱化信息 |
| `--cyan` | `#68c8d4` | 主要操作与强调状态 |
| `--red` | `#d45b51` | 错误与危险反馈 |
| `--white` | `#fff` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.nav h1` | 继承页面字体 | font-size: 27px; line-height: 1.1 | 由 font 简写或继承确定 |
| 分区标题 `.sheet-head h2` | 继承页面字体 | font-size: 34px | 由 font 简写或继承确定 |
| 辅助文字 `.nav .doc` | 11px ui-monospace,Consolas,monospace | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `30px` | `.layout` 的 `padding` |
| 布局间距 | `22px` | `.layout` 的 `gap` |
| 圆角 | `0` | `input,select,textarea` 的 `border-radius` |
| 边框或阴影 | `1px solid rgba(237,245,247,.35)` | `.nav` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.nav button` | display: block; width: 100%; padding: 14px 0 | text-align: left; border: 0; border-top: 1px solid rgba(237,245,247,.2); background: transparent; color: #bdd3dc | .nav button:hover → color: white |
| 输入、选择或次操作 `input,select,textarea` | width: 100%; padding: 12px; border-radius: 0 | border: 1px solid #8da9b5; background: var(--white); color: var(--ink); font: 14px inherit; border-radius: 0 | input:focus,select:focus,textarea:focus → outline: 3px solid var(--cyan) |
| 内容容器 `.message` | min-height: 18px | font-size: 12px; color: var(--blue) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:820px)` | .layout → grid-template-columns: 1fr; padding: 16px; .nav → position: static; .nav button → display: inline-block; width: auto; .form → padding: 28px 24px; .grid → grid-template-columns: 1fr | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“蓝图申请册 · 长表单” → “FORM / URB-27B” → “城市微更新” → “申请蓝图” → “01 / 项目基本信息” → “02 / 场地与方案” → “03 / 负责人确认” → “已填写 0 / 6 个必填项” → “空间使用申请” → “所有尺寸以公制填写” → “DRAFT” → “SAVED”。控件占位或辅助标签包括：“例：桥下雨水花园”、“说明计划解决的问题与使用方式”、“如 NS-014”、“120”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | html → scroll-behavior: auto; * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | html → scroll-behavior: auto; * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.layout 与 .form 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#68c8d4`、`#d45b51`、`#edf5f7`、`#123f6a`、`#fff` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.nav button`、输入、选择或次操作 `input,select,textarea` 与 内容容器 `.message` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:820px)` 条件下，布局按响应式表变化且“蓝图申请册 · 长表单”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
