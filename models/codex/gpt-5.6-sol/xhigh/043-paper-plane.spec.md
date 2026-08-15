# 043 纸鸢信箱

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`043-paper-plane.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #bccce0; color: var(--ink) |
| 主要结构 `.phone` | width: min(390px,100%); height: 760px; margin: 20px auto | display: grid; grid-template-rows: auto auto 1fr auto | background: var(--air); box-shadow: 0 25px 70px #34506f55 |
| 关键内容区 `.bubble` | max-width: 78%; padding: 11px 13px; margin: 9px 0 | 未单独声明 | background: white; border-radius: 4px 16px 16px 16px; box-shadow: 0 4px 12px #607f9b22 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--air` | `#dcecff` | 品牌或局部强调 |
| `--paper` | `#fff` | 容器与表面 |
| `--ink` | `#20334a` | 主要文字与高对比边界 |
| `--muted` | `#788ca3` | 辅助文字与弱化信息 |
| `--blue` | `#407bc1` | 品牌或局部强调 |
| `--yellow` | `#f2c75c` | 主要操作与强调状态 |
| `--ok` | `#4c9073` | 成功反馈 |
| `--danger` | `#d85858` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.compose button` | 继承页面字体 | font-size: 18px | 由 font 简写或继承确定 |
| 分区标题 `.fail-next` | 继承页面字体 | font-size: 11px | 由 font 简写或继承确定 |
| 辅助文字 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `18px 18px 12px` | `.head` 的 `padding` |
| 布局间距 | `12px` | `.head` 的 `gap` |
| 圆角 | `12px` | `.head i` 的 `border-radius` |
| 边框或阴影 | `0 25px 70px #34506f55` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.compose button` | border-radius: 50%; width: 42px | border: 0; border-radius: 50%; background: var(--blue); color: white; font-size: 18px | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.compose input` | border-radius: 20px; padding: 11px 14px | border: 1px solid #c2d1df; border-radius: 20px | 未声明独立状态；保持默认样式 |
| 内容容器 `.phone` | width: min(390px,100%); height: 760px; margin: 20px auto; display: grid | background: var(--air); box-shadow: 0 25px 70px #34506f55 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“纸鸢信箱” → “阿澄” → “在线 · 风从海边来” → “山屋小组” → “留声机” → “明天六点，旧码头见？” → “18:21” → “我带热咖啡。” → “已送达 · 18:22” → “测试：让下一条消息发送失败”。控件占位或辅助标签包括：“消息”、“发送”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .bubble 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#788ca3`、`#f2c75c`、`#20334a`、`#fff`、`#407bc1` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.compose button`、输入、选择或次操作 `.compose input` 与 内容容器 `.phone` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“纸鸢信箱”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

选择会话，输入并发送消息，在同一消息旁看到已送达状态。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

会话切换条 + 当前聊天 → 新消息已送达；测试开关开启时 → 失败气泡 → 原位重试 → 已送达。

## 正常流程

点山屋小组，输入消息并发送，消息追加到右侧且状态为“已送达”。

## 异常触发与恢复

勾选“让下一条消息发送失败”再发送；原文仍在气泡内并标红；点该气泡的“重试”后恢复为已送达。

## 数据变化

每次发送追加一条消息；失败消息保留文本但不标送达；重试只改变该消息状态，不重复创建。

## 人工验收步骤

正常：切换会话 → 输入 → 发送 → 见已送达。异常：勾测试 → 发送 → 见红色失败且原文在 → 点重试 → 见重试成功。
