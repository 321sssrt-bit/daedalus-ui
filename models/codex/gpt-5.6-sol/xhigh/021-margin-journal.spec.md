# 021 边注月刊

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`021-margin-journal.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--paper); color: var(--ink) |
| 主要结构 `.entry` | width: 100%; gap: 18px; padding: 24px 6px | display: grid; grid-template-columns: 62px 1fr auto; gap: 18px | border: 0; border-bottom: 1px solid var(--rule); background: transparent; color: inherit |
| 关键内容区 `.mast` | padding: 22px clamp(24px,5vw,72px) | display: grid; grid-template-columns: 1fr auto 1fr; align-items: end | border-bottom: 1px solid var(--ink) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--paper` | `#f6f0df` | 容器与表面 |
| `--sheet` | `#fffaf0` | 品牌或局部强调 |
| `--ink` | `#262018` | 主要文字与高对比边界 |
| `--muted` | `#786f62` | 辅助文字与弱化信息 |
| `--rule` | `#b8ac98` | 品牌或局部强调 |
| `--wine` | `#7f2635` | 品牌或局部强调 |
| `--sage` | `#5e6c52` | 品牌或局部强调 |
| `--literal-8` | `#4c443a` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC","SimSun",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.mast h1` | 继承页面字体 | font-size: 33px | font-weight: 500; letter-spacing: 7px |
| 分区标题 `.lead h2` | 继承页面字体 | font-size: 46px | font-weight: 400 |
| 辅助文字 `.eyebrow` | 700 11px Arial,"Microsoft YaHei",sans-serif | font 简写中声明 | letter-spacing: 2px |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `22px clamp(24px,5vw,72px)` | `.mast` 的 `padding` |
| 布局间距 | `0` | `.columns` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `1px solid var(--ink)` | `.mast` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.entry` | width: 100%; display: grid; padding: 24px 6px | text-align: left; border: 0; border-bottom: 1px solid var(--rule); background: transparent; color: inherit | .entry:hover,.entry.active → background: var(--sheet); .entry:focus-visible → outline: 3px solid var(--wine) |
| 输入、选择或次操作 `.read` | padding: 12px 18px | border: 1px solid var(--ink); background: transparent; font: 700 12px Arial,"Microsoft YaHei",sans-serif | .read:hover → background: var(--ink); color: var(--paper) |
| 内容容器 `body` | margin: 0; min-height: 100vh | background: var(--paper); color: var(--ink) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .mast → grid-template-columns: 1fr auto; .mast .date → display: none; .columns → grid-template-columns: 1fr; .index → border-right: 0; padding-right: 0; .reader → position: static; padding: 34px 0 | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“边注月刊 · 内容目录” → “MARGIN / 第 18 期” → “边注月刊” → “二〇二六年 · 仲夏” → “目录” → “关于城市、器物与缓慢工作的五篇札记” → “01” → “一张椅子的第二次生命” → “梁雨 / 器物考” → “p. 08” → “02” → “在高架桥下种一座花园”。控件占位或辅助标签包括：“文章目录”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → scroll-behavior: auto!important; transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → scroll-behavior: auto!important; transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.entry 与 .mast 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#4c443a`、`#262018`、`#786f62`、`#fffaf0`、`#b8ac98` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.entry`、输入、选择或次操作 `.read` 与 内容容器 `body` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“边注月刊 · 内容目录”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
