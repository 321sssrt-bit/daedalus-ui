# 047 色谱锻造厂

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`047-chroma-forge.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--void); color: var(--ink) |
| 主要结构 `.app` | min-height: 800px; max-width: 1280px; margin: auto | display: grid; grid-template-columns: 250px 1fr 280px | 未单独声明 |
| 关键内容区 `.poster` | width: 430px; height: 520px | position: relative | background: #f24eb4; overflow: hidden; box-shadow: 20px 20px 0 #4ce1da |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--void` | `#15111f` | 品牌或局部强调 |
| `--panel` | `#251d32` | 容器与表面 |
| `--ink` | `#f5efff` | 主要文字与高对比边界 |
| `--muted` | `#9d8eaf` | 辅助文字与弱化信息 |
| `--magenta` | `#f24eb4` | 品牌或局部强调 |
| `--cyan` | `#4ce1da` | 主要操作与强调状态 |
| `--ok` | `#7ee59d` | 成功反馈 |
| `--danger` | `#ff6b68` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-monospace,"Cascadia Mono","Microsoft YaHei",monospace | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.poster h1` | 900 54px/1 Arial | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.brand` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 900 |
| 辅助文字 `label` | 继承页面字体 | font-size: 11px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `22px` | `.tools,.export` 的 `padding` |
| 布局间距 | `未单独声明` | 由组件行逐项定义 |
| 圆角 | `50%` | `.shape` 的 `border-radius` |
| 边框或阴影 | `1px solid #413450` | `.tools,.export` 的 `border-right` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.export button` | width: 100%; padding: 13px; margin-top: 12px | border: 0; background: var(--cyan); color: #10141a; font-weight: 900 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `input[type=color]` | width: 100%; height: 40px | background: none; border: 1px solid #554361 | 未声明独立状态；保持默认样式 |
| 内容容器 `.layer` | padding: 10px; margin: 8px 0 | border: 1px solid #463a54 | .layer.active → color: var(--cyan) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .app → grid-template-columns: 1fr; .tools,.export → border: 0; .poster → transform: scale(.75) | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“色谱锻造厂” → “CHROMA FORGE / 色谱锻造厂” → “图层” → “◉ 主形状 / 圆环” → “T 标题 / CHROMA” → “▧ 背景 / 洋红” → “背景颜色” → “圆环模糊” → “px” → “实时预览 · POSTER_08” → “1080 × 1350” → “不按”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → animation: none!important; transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → animation: none!important; transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.app 与 .poster 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#7ee59d`、`#f5efff`、`#251d32`、`#15111f`、`#ff6b68` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.export button`、输入、选择或次操作 `input[type=color]` 与 内容容器 `.layer` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“色谱锻造厂”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

改变颜色或模糊参数，在实时预览确认效果，选择格式并得到导出文件结果。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

图层/参数栏 + 实时画布 + 导出栏；冲突组合 → 错误结果 → 修正格式 → 成功结果。

## 正常流程

改背景颜色，拖动模糊，选 PNG，点导出，看到 POSTER_08.png 和大小。

## 异常触发与恢复

点“选择不支持组合”自动形成 SVG + 42px 模糊并阻止导出；点“改为 PNG 并重试”立刻得到成功结果。

## 数据变化

参数实时改变预览；失败不生成文件；修正只改变格式，保留作品颜色与模糊值。

## 人工验收步骤

正常：调颜色/模糊 → 选 PNG → 导出成功。异常：点测试组合 → 核对 SVG 冲突 → 改 PNG 重试 → 成功且预览参数保留。
