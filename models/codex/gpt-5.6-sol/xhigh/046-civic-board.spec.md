# 046 公署协作台

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`046-civic-board.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--paper); color: var(--ink) |
| 主要结构 `.shell` | min-height: 800px; max-width: 1280px; margin: auto | 未单独声明 | border-left: 1px solid #bab5a7; border-right: 1px solid #bab5a7 |
| 关键内容区 `.board` | gap: 12px; margin-top: 24px | display: grid; grid-template-columns: repeat(3,1fr); gap: 12px | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--paper` | `#ece8dc` | 容器与表面 |
| `--white` | `#faf8f1` | 品牌或局部强调 |
| `--ink` | `#222a2d` | 主要文字与高对比边界 |
| `--muted` | `#727979` | 辅助文字与弱化信息 |
| `--navy` | `#27485a` | 品牌或局部强调 |
| `--stamp` | `#b7463e` | 品牌或局部强调 |
| `--ok` | `#3f735b` | 成功反馈 |
| `--danger` | `#a33b36` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.mast h1` | 700 28px Georgia | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.column h2` | 继承页面字体 | font-size: 13px | letter-spacing: .1em |
| 辅助文字 `.mast small` | 11px ui-monospace | font 简写中声明 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `20px 30px` | `.mast` 的 `padding` |
| 布局间距 | `8px` | `.create` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `1px solid #bab5a7` | `.shell` 的 `border-left` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.create button` | padding: 0 18px | border: 0; background: var(--navy); color: white; font-weight: 700 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.create input,.create select` | padding: 11px | border: 1px solid #99968c; background: var(--white); font: inherit | 未声明独立状态；保持默认样式 |
| 内容容器 `.board` | display: grid; margin-top: 24px | 未单独声明 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:800px)` | .layout → grid-template-columns: 1fr; .board → grid-template-columns: 1fr; .log → border-left: 0; .create → grid-template-columns: 1fr | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“公署协作台” → “市务室 · 协作登记簿” → “档案日 2026-08-14 / 当前席位：编辑” → “分派：林禾” → “分派：周岑” → “分派：我” → “登记任务” → “01 · 待处理” → “核对公共座椅尺寸” → “周岑 · 14:30” → “推进状态” → “修改年度预算批次”。控件占位或辅助标签包括：“任务名称”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .board 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#727979`、`#3f735b`、`#b7463e`、`#27485a`、`#ece8dc` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.create button`、输入、选择或次操作 `.create input,.create select` 与 内容容器 `.board` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:800px)` 条件下，布局按响应式表变化且“公署协作台”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

登记任务并分派成员，把任务推进到下一状态，同时在活动记录看到对应变更。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

新建登记行 + 三栏状态板 + 活动簿；受限操作进入权限通知，可申请或返回普通任务。

## 正常流程

改任务名和成员，点登记；在待处理看到新卡并在活动簿看到记录；推进后卡进入处理中并新增记录。

## 异常触发与恢复

点“推进受限任务”，页面说明所缺权限且不记录变更；可发访问申请或返回；随后推进普通任务即可完成有权限的变更。

## 数据变化

正常创建增加任务卡和活动；推进移动原卡并增加活动；拒绝本身不改任务，申请权限才增加申请记录。

## 人工验收步骤

正常：登记新任务 → 核对分派与活动 → 推进 → 核对列和活动。异常：推进受限任务 → 确认无变更记录 → 申请或返回 → 推进普通任务成功。
