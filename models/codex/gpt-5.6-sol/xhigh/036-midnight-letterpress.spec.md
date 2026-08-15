# 036 午夜投递

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`036-midnight-letterpress.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #080d20; color: var(--ink) |
| 主要结构 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; padding: 20px | position: relative | background: var(--night); border: 1px solid #26325f; box-shadow: 0 0 60px #5b6fff26 |
| 关键内容区 `.pulse` | width: 8px; height: 8px | 未单独声明 | border-radius: 50%; background: var(--pink); box-shadow: 0 0 14px var(--pink) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--night` | `#0e1530` | 品牌或局部强调 |
| `--panel` | `#172143` | 容器与表面 |
| `--ink` | `#eef1ff` | 主要文字与高对比边界 |
| `--muted` | `#8792bd` | 辅助文字与弱化信息 |
| `--electric` | `#91a7ff` | 品牌或局部强调 |
| `--pink` | `#ff7ab8` | 主要文字与高对比边界 |
| `--ok` | `#71e2ba` | 成功反馈 |
| `--literal-8` | `#080d20` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-monospace,"Cascadia Mono","Microsoft YaHei",monospace | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `h1` | 700 28px/1.1 system-ui | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.brand` | 继承页面字体 | font-size: 12px | letter-spacing: .16em |
| 辅助文字 `.sub` | 继承页面字体 | font-size: 12px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `20px` | `.phone` 的 `padding` |
| 布局间距 | `10px` | `.actions` 的 `gap` |
| 圆角 | `50%` | `.pulse` 的 `border-radius` |
| 边框或阴影 | `1px solid #26325f` | `.phone` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `button` | padding: 13px | border: 1px solid #3b4a7a; background: transparent; color: var(--ink); font: 600 13px inherit | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `input,textarea` | width: 100%; padding: 13px | background: var(--panel); border: 1px solid #32406f; color: var(--ink); font: inherit | input:focus,textarea:focus → box-shadow: 0 0 0 2px #91a7ff22 |
| 内容容器 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; padding: 20px | background: var(--night); border: 1px solid #26325f; box-shadow: 0 0 60px #5b6fff26 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“午夜投递” → “NIGHT POST / 23:48” → “把今天寄往明天” → “无人催促的公开信，只在你按下投递后出现。” → “草稿 01” → “标题” → “正文” → “末班车驶过桥面，像一条发亮的针脚。今晚我终于明白，安静不是没有声音，而是每种声音都有了自己的位置。” → “0 字” → “状态：仅自己可见” → “存入草稿” → “投递到凌晨”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .pulse 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#172143`、`#ff7ab8`、`#0e1530`、`#eef1ff`、`#71e2ba` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `button`、输入、选择或次操作 `input,textarea` 与 内容容器 `.phone` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“午夜投递”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
