# 039 旅途存根

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`039-transit-keepsake.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--sky); color: var(--ink) |
| 主要结构 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; padding: 24px | 未单独声明 | background: linear-gradient(#a8d0e9 0 38%,#e7f0ed 38%); box-shadow: 0 22px 60px #315f7c44 |
| 关键内容区 `.check` | width: 66px; height: 66px; margin: 44px auto 12px | display: grid; place-items: center | border-radius: 50%; background: var(--green); color: white |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--sky` | `#b9d9ed` | 品牌或局部强调 |
| `--ticket` | `#ffe887` | 品牌或局部强调 |
| `--ink` | `#17334b` | 主要文字与高对比边界 |
| `--muted` | `#61798b` | 辅助文字与弱化信息 |
| `--blue` | `#23669b` | 品牌或局部强调 |
| `--green` | `#2b7a64` | 成功反馈 |
| `--red` | `#b9473e` | 错误与危险反馈 |
| `--literal-8` | `#a8d0e9` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `h1` | 继承页面字体 | font-size: 27px | 由 font 简写或继承确定 |
| 分区标题 `.top span` | 继承页面字体 | font-size: 12px | letter-spacing: .14em |
| 辅助文字 `.check` | 继承页面字体 | font-size: 34px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px` | `.phone` 的 `padding` |
| 布局间距 | `14px` | `.facts` 的 `gap` |
| 圆角 | `50%` | `.check` 的 `border-radius` |
| 边框或阴影 | `0 22px 60px #315f7c44` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `button` | padding: 13px | border: 1px solid var(--blue); background: transparent; color: var(--blue); font-weight: 700 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.check` | width: 66px; height: 66px; border-radius: 50%; display: grid; margin: 44px auto 12px | border-radius: 50%; background: var(--green); color: white; font-size: 34px | 未声明独立状态；保持默认样式 |
| 内容容器 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; padding: 24px | background: linear-gradient(#a8d0e9 0 38%,#e7f0ed 38%); box-shadow: 0 22px 60px #315f7c44 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“旅途存根” → “轨迹 / 凭证” → “2026.08.14” → “行程预订成功” → “你的靠窗席位已经留好” → “上海虹桥” → “SHA” → “━━ 2h 18m ━━▶” → “杭州东” → “HGH” → “凭证编号 TR-0824-61A9” → “出发时间”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .check 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#a8d0e9`、`#b9d9ed`、`#2b7a64`、`#ffe887`、`#b9473e` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `button`、输入、选择或次操作 `.check` 与 内容容器 `.phone` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“旅途存根”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
