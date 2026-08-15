# 020 轨道套餐

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`020-orbital-plans.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--space); color: var(--text) |
| 主要结构 `.hero` | max-width: 850px; margin: 66px auto 38px | 未单独声明 | 未单独声明 |
| 关键内容区 `.plan` | min-height: 430px; padding: 30px | position: relative | background: linear-gradient(180deg,#17142e,#0f0d22); border: 1px solid #38345b; border-radius: 26px; overflow: hidden |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--space` | `#090817` | 品牌或局部强调 |
| `--panel` | `#141229` | 容器与表面 |
| `--text` | `#f4f1ff` | 主要文字与高对比边界 |
| `--muted` | `#aaa5c4` | 辅助文字与弱化信息 |
| `--violet` | `#8f6cff` | 品牌或局部强调 |
| `--cyan` | `#62e6ff` | 主要操作与强调状态 |
| `--lime` | `#c9ff63` | 品牌或局部强调 |
| `--danger` | `#ff668a` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Inter,Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.hero h1` | 继承页面字体 | font-size: clamp(48px,7vw,92px); line-height: .98 | letter-spacing: -5px |
| 分区标题 `.plan h2` | 继承页面字体 | font-size: 26px | 由 font 简写或继承确定 |
| 辅助文字 `.price small` | 继承页面字体 | font-size: 13px | font-weight: 400 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `44px clamp(24px,5vw,76px)` | `.stars` 的 `padding` |
| 布局间距 | `18px` | `.plans` 的 `gap` |
| 圆角 | `99px` | `.status` 的 `border-radius` |
| 边框或阴影 | `1px solid #3e3a62` | `.status` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.cta` | border-radius: 12px; padding: 14px | border: 1px solid #69618e; border-radius: 12px; background: transparent; color: white | .cta:hover → border-color: var(--cyan); transform: translateY(-2px); .toggle button:focus-visible,.cta:focus-visible → outline: 3px solid var(--cyan) |
| 输入、选择或次操作 `.badge` | padding: 7px 10px; border-radius: 99px | background: var(--lime); color: #16131d; border-radius: 99px; font-size: 11px; font-weight: 900 | 未声明独立状态；保持默认样式 |
| 内容容器 `.message` | height: 24px | text-align: center; color: var(--lime); font-size: 13px | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .plans → grid-template-columns: 1fr; max-width: 520px; .plan,.plan.reco → min-height: 410px; .hero → margin-top: 45px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“轨道套餐 · 定价” → “PARALLAX°” → “● SYSTEMS NOMINAL” → “为下一次跃迁” → “选择你的” → “轨道” → “从一次个人任务到跨团队运行，算力和协作席位会随你的航程自然扩展。” → “按月” → “按年 · 省 2 个月” → “近地” → “给正在验证第一条航线的独立创作者。” → “39”。控件占位或辅助标签包括：“计费周期”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.hero 与 .plan 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#8f6cff`、`#aaa5c4`、`#090817`、`#f4f1ff`、`#141229` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.cta`、输入、选择或次操作 `.badge` 与 内容容器 `.message` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“轨道套餐 · 定价”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
