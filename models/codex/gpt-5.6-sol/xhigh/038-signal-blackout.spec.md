# 038 信号断层

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`038-signal-blackout.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #2c2c2c; color: var(--white) |
| 主要结构 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto | position: relative | background: var(--black); overflow: hidden; border: 6px solid #090909 |
| 关键内容区 `.slash` | height: 10px; margin: 14px -20px 34px | 未单独声明 | background: var(--orange) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--black` | `#131313` | 品牌或局部强调 |
| `--panel` | `#202020` | 容器与表面 |
| `--white` | `#f4f1e8` | 品牌或局部强调 |
| `--muted` | `#99958c` | 辅助文字与弱化信息 |
| `--orange` | `#ff5a1f` | 品牌或局部强调 |
| `--ok` | `#91d18b` | 成功反馈 |
| `--literal-7` | `#2c2c2c` | HTML 中直接声明的局部色 |
| `--literal-8` | `#090909` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `h1` | 继承页面字体 | font-size: 28px | 由 font 简写或继承确定 |
| 分区标题 `.code` | 900 92px/.9 Impact,Arial | font 简写中声明 | letter-spacing: -.05em |
| 辅助文字 `p` | 继承页面字体 | line-height: 1.6 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `65px 26px 0` | `.code` 的 `padding` |
| 布局间距 | `10px` | `.actions` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `6px solid #090909` | `.phone` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `button` | padding: 14px | border: 1px solid #4d4d4d; background: var(--panel); color: var(--white); font-weight: 800; text-align: left | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto | background: var(--black); border: 6px solid #090909 | 未声明独立状态；保持默认样式 |
| 内容容器 `.ticket` | margin: 28px 0; padding: 12px | border: 1px dashed #625f58; font: 12px ui-monospace | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“信号断层” → “503” → “隧道前方暂时封闭” → “不是你的操作有问题。北区节点正在重新接线，我们保留了刚才的路线。” → “故障工单” → “SG-503-8821” → “最近更新 18:42:09” → “↻ 重新探测线路” → “← 回到首页” → “预计恢复：2 分钟内”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .slash 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#91d18b`、`#f4f1e8`、`#2c2c2c`、`#ff5a1f`、`#99958c` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `button`、输入、选择或次操作 `.phone` 与 内容容器 `.ticket` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“信号断层”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
