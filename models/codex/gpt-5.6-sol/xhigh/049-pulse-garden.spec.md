# 049 脉搏花园

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`049-pulse-garden.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #bccbb9; color: var(--ink) |
| 主要结构 `.progress` | margin: 28px 0; height: 180px | display: grid; place-items: center; position: relative | background: var(--leaf); border-radius: 100px; overflow: hidden |
| 关键内容区 `.form` | margin-top: 20px; padding: 16px | 未单独声明 | background: white; border: 1px solid #c9d0c2 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--leaf` | `#dcebd8` | 品牌或局部强调 |
| `--paper` | `#f8f4e9` | 容器与表面 |
| `--ink` | `#234032` | 主要文字与高对比边界 |
| `--muted` | `#728475` | 辅助文字与弱化信息 |
| `--green` | `#4e8a63` | 成功反馈 |
| `--lime` | `#aed067` | 品牌或局部强调 |
| `--ok` | `#357558` | 成功反馈 |
| `--danger` | `#c55446` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.top b` | Georgia | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 分区标题 `.progress strong` | 600 45px Georgia | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.form label` | 继承页面字体 | font-size: 11px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `20px` | `.phone` 的 `padding` |
| 布局间距 | `9px` | `.trend` 的 `gap` |
| 圆角 | `100px` | `.progress` 的 `border-radius` |
| 边框或阴影 | `0 25px 70px #33513b44` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.form button` | width: 100%; padding: 12px; margin-top: 14px | border: 0; background: var(--green); color: white; font-weight: 800 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.form input` | width: 100%; padding: 10px | border: 0; border-bottom: 2px solid var(--leaf); font: 22px Georgia | 未声明独立状态；保持默认样式 |
| 内容容器 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; padding: 20px | background: var(--paper); box-shadow: 0 25px 70px #33513b44 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“脉搏花园” → “第 18 周” → “64%” → “本周活动目标 · 192 / 300 分钟” → “近七日活动趋势” → “记录一次活动” → “时长（1–300 分钟）” → “平均心率（40–220）” → “保存并更新花园” → “测试：填入超出范围的数据”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.progress 与 .form 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#357558`、`#234032`、`#dcebd8`、`#c55446`、`#aed067` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.form button`、输入、选择或次操作 `.form input` 与 内容容器 `.phone` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“脉搏花园”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

输入活动时长和平均心率，保存后看到总分钟、百分比和今日趋势改变。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

目标/趋势总览 + 活动表单 → 保存成功；无效范围 → 字段规则错误 → 修正 → 重算成功。

## 正常流程

输入 30 分钟和 126，点保存，进度从 192 增至 222，百分比与今日柱更新。

## 异常触发与恢复

点测试入口填 980/360 并保存；错误定位两个合理范围并声明 64% 未变；点修正后自动重新保存并重算。

## 数据变化

有效记录增加总分钟并重算百分比/柱高；无效记录不改变 total 或图表。

## 人工验收步骤

正常：记录 30/126 → 保存 → 核对 222/300 和趋势。异常：点测试 → 核对进度仍 64% → 点修正 → 看成功与新进度。
