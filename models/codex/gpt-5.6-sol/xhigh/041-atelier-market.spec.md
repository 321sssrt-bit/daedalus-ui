# 041 格物市集

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`041-atelier-market.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--cream); color: var(--ink) |
| 主要结构 `.shell` | max-width: 1280px; margin: auto; min-height: 800px; padding: 24px 42px | 未单独声明 | 未单独声明 |
| 关键内容区 `.panel` | padding-left: 30px | 未单独声明 | border-left: 1px solid #bbae9b |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--clay` | `#bb5b39` | 主要操作与强调状态 |
| `--cream` | `#f5ead6` | 品牌或局部强调 |
| `--paper` | `#fffaf0` | 容器与表面 |
| `--ink` | `#2d261f` | 主要文字与高对比边界 |
| `--muted` | `#807367` | 辅助文字与弱化信息 |
| `--olive` | `#68704a` | 品牌或局部强调 |
| `--ok` | `#39705a` | 成功反馈 |
| `--danger` | `#a63d35` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `h1` | 600 48px/1.05 Georgia,"Songti SC" | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.panel h2` | 28px Georgia | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.eyebrow` | 700 12px ui-monospace | font 简写中声明 | letter-spacing: .12em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px 42px` | `.shell` 的 `padding` |
| 布局间距 | `34px` | `.layout` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `2px solid var(--ink)` | `.nav` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.add,.checkout` | width: 100%; margin-top: 18px; padding: 14px | border: 0; background: var(--clay); color: white; font-weight: 800 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.good` | padding: 12px | border: 1px solid #cdbda8; background: var(--paper); text-align: left | .good.selected → outline: 3px solid var(--clay) |
| 内容容器 `.cart` | margin-top: 22px; padding: 16px | background: var(--paper); border: 1px solid #cdbda8 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:800px)` | .shell → padding: 20px; .layout → grid-template-columns: 1fr; .goods → grid-template-columns: 1fr 1fr; .panel → border-left: 0; padding-left: 0 | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“格物市集” → “器物 · 今日可送达 购物袋” → “AUTUMN OBJECTS / 08” → “让会被每天触碰的东西，值得多看一眼。” → “层叠台灯” → “¥329 · 榉木与棉纸” → “折线托盘” → “¥168 · 手工铜” → “晨雾花器” → “¥246 · 灰陶” → “柔和向下的光，适合床头最后二十页。” → “颜色 / 规格”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .panel 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#bb5b39`、`#807367`、`#68704a`、`#f5ead6`、`#2d261f` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.add,.checkout`、输入、选择或次操作 `.good` 与 内容容器 `.cart` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:800px)` 条件下，布局按响应式表变化且“格物市集”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

从浏览器物开始，选规格和数量，加入购物袋，核对动态金额并生成可核对订单号。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

商品浏览 → 选中商品/规格/数量 → 购物袋 → 正常订单回执；缺货则进入错误条 → 改选规格 → 回购物袋。

## 正常流程

选择任一商品；选燕麦白并调数量；点“加入购物袋”看到明细和合计；点“提交订单”看到 GM-260814 回执。

## 异常触发与恢复

点“测试：让当前规格库存不足”会切到暮蓝并显示具体库存错误，订单不生成；点错误内“改为燕麦白”，再提交即可成功。

## 数据变化

商品、规格和数量决定购物袋行及金额；缺货时不产生订单号；恢复后使用新规格和当前数量生成回执。

## 人工验收步骤

正常：选折线托盘 → 数量加到 2 → 加入 → 核对 ¥336 → 提交并见回执。异常：触发库存不足 → 确认错误且无订单号 → 改燕麦白 → 再提交成功。
