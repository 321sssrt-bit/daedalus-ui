# 007 空白游行

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`007-blank-parade.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text); overflow: hidden |
| 主要结构 `.created` | inset: 12%; padding: 30px | display: none; position: absolute | background: var(--surface); border: 3px solid var(--text); z-index: 4; box-shadow: 12px 12px 0 var(--text) |
| 关键内容区 `.top` | height: 64px; padding: 0 30px | display: flex; align-items: center; justify-content: space-between | border-bottom: 3px solid var(--text); background: var(--surface) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#f6f1e6` | 页面或区域背景 |
| `--surface` | `#fffdf7` | 容器与表面 |
| `--text` | `#151515` | 主要文字与高对比边界 |
| `--muted` | `#68645e` | 辅助文字与弱化信息 |
| `--accent` | `#ff4f38` | 主要操作与强调状态 |
| `--success` | `#187c5a` | 成功反馈 |
| `--danger` | `#c82f3b` | 错误与危险反馈 |
| `--blue` | `#3765eb` | 品牌或局部强调 |
| `--yellow` | `#ffd84d` | 主要操作与强调状态 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",system-ui,sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.copy h1` | 继承页面字体 | font-size: clamp(65px,9vw,138px); line-height: .78 | letter-spacing: -.09em |
| 分区标题 `.created h2` | 继承页面字体 | font-size: 38px | 由 font 简写或继承确定 |
| 辅助文字 `.logo` | 继承页面字体 | font-size: 22px | font-weight: 900; letter-spacing: -.05em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `0 30px` | `.top` 的 `padding` |
| 布局间距 | `24px` | `.top nav` 的 `gap` |
| 圆角 | `50%` | `.logo i` 的 `border-radius` |
| 边框或阴影 | `3px solid var(--text)` | `.top` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.btn.primary` | 未单独声明 | background: var(--accent); color: white | .btn:hover → box-shadow: 2px 2px 0 var(--text) |
| 输入、选择或次操作 `.avatar` | width: 34px; height: 34px; border-radius: 50%; display: grid | background: var(--yellow); border: 2px solid var(--text); border-radius: 50%; font-weight: 900 | 未声明独立状态；保持默认样式 |
| 内容容器 `.btn` | height: 56px; padding: 0 25px | border: 3px solid var(--text); background: var(--surface); font-weight: 900; box-shadow: 5px 5px 0 var(--text) | .btn:hover → box-shadow: 2px 2px 0 var(--text) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:800px)` | body → overflow: auto; .stage → grid-template-columns: 1fr; height: auto; .copy → min-height: 66vh; .art → height: 420px; .top nav → display: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“空白游行 · 欢迎” → “开场白” → “灵感墙” → “项目” → “邀请” → “WELCOME / FIRST DAY” → “这里还” → “空着。” → “很好，第一块空地属于你。建一张灵感墙，把图片、文字和没想明白的念头都先放进来。” → “创建第一张墙” → “看看示例” → “你的第一个空间”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.btn` 状态变化 | transition: .15s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important |
| `.btn` 状态变化 | transition: .15s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.created 与 .top 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#151515`、`#68645e`、`#c82f3b`、`#f6f1e6`、`#187c5a` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.btn.primary`、输入、选择或次操作 `.avatar` 与 内容容器 `.btn` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:800px)` 条件下，布局按响应式表变化且“空白游行 · 欢迎”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
