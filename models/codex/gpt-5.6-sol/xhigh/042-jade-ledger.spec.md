# 042 青玉钱匣

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`042-jade-ledger.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #b9c5bc; color: var(--ink) |
| 主要结构 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto | 未单独声明 | background: var(--paper); box-shadow: 0 28px 70px #183a3560; overflow: hidden |
| 关键内容区 `.content` | padding: 20px | 未单独声明 | 未单独声明 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--jade` | `#123e3a` | 品牌或局部强调 |
| `--deep` | `#092925` | 品牌或局部强调 |
| `--paper` | `#eef3e6` | 容器与表面 |
| `--ink` | `#17312d` | 主要文字与高对比边界 |
| `--muted` | `#6e8078` | 辅助文字与弱化信息 |
| `--gold` | `#d2a84a` | 品牌或局部强调 |
| `--ok` | `#2f795e` | 成功反馈 |
| `--danger` | `#b54b43` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.balance` | 600 38px Georgia | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.person i` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 800 |
| 辅助文字 `.person.active` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 700 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px 22px 30px` | `.head` 的 `padding` |
| 布局间距 | `12px` | `.people` 的 `gap` |
| 圆角 | `50%` | `.person i` 的 `border-radius` |
| 边框或阴影 | `0 28px 70px #183a3560` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.primary` | width: 100%; padding: 14px; margin-top: 22px | border: 0; background: var(--jade); color: white; font-weight: 800 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.amount input` | width: 100% | border: 0; font: 36px Georgia; color: var(--ink); background: transparent | 未声明独立状态；保持默认样式 |
| 内容容器 `.seal` | width: 56px; height: 56px; border-radius: 50%; display: grid; margin: auto | border: 2px solid var(--ok); border-radius: 50%; color: var(--ok); font-size: 27px | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“青玉钱匣” → “青玉钱匣 · 可用余额” → “¥1,280.00” → “今日转账限额还剩 ¥8,000” → “转给谁” → “苏棠” → “陈野” → “木屋” → “转账金额” → “付款来源” → “钱包余额 · ¥1,280” → “青禾储蓄卡 · 可用 ¥5,000”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .content 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#6e8078`、`#2f795e`、`#092925`、`#b54b43`、`#17312d` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.primary`、输入、选择或次操作 `.amount input` 与 内容容器 `.seal` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“青玉钱匣”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

选择收款人，输入金额和资金来源，核对后确认，最终看到唯一凭证编号。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

余额首页/转账表单 → 核对面板 → 成功凭证；超额时进入余额不足面板 → 换来源 → 回核对。

## 正常流程

选收款人，输入 128，点核对；确认姓名与金额后点确认，看到 QY-814-2036。

## 异常触发与恢复

点测试链接填入 1600，在钱包来源下核对会阻止转账并显示可用 1280；点“改用青禾储蓄卡”后重新核对并确认成功。

## 数据变化

失败时不生成凭证、不宣称扣款；切换来源仅改变可用上限；确认后生成固定格式凭证。

## 人工验收步骤

正常：选陈野 → 128 → 核对 → 确认 → 见成功凭证。异常：测试超额 → 核对见余额不足 → 换储蓄卡 → 再确认成功。
