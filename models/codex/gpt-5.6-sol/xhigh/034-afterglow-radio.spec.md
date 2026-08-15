# 034 余晖电台

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`034-afterglow-radio.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh; padding: 24px | display: grid; place-items: center | background: #080914; color: var(--cream) |
| 主要结构 `.phone` | width: min(390px,100%); height: min(820px,calc(100vh - 32px)); min-height: 690px | position: relative | background: var(--night); border: 8px solid #05060b; border-radius: 46px; overflow: hidden; box-shadow: 0 30px 70px #000 |
| 关键内容区 `.art` | margin: 28px auto 25px; width: 100% | position: relative | background: var(--case); border: 2px solid #565a77; border-radius: 28px; overflow: hidden; box-shadow: 0 18px 32px rgba(0,0,0,.38) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--night` | `#15182a` | 品牌或局部强调 |
| `--case` | `#292c43` | 品牌或局部强调 |
| `--screen` | `#efb35d` | 品牌或局部强调 |
| `--cream` | `#fff2d3` | 品牌或局部强调 |
| `--muted` | `#9296ad` | 辅助文字与弱化信息 |
| `--pink` | `#e75b78` | 主要文字与高对比边界 |
| `--cyan` | `#5cc6c2` | 主要操作与强调状态 |
| `--black` | `#10111b` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | "Avenir Next","Microsoft YaHei",Arial,sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.info h1` | 继承页面字体 | font-size: 25px | 由 font 简写或继承确定 |
| 分区标题 `.queue h2` | 继承页面字体 | font-size: 20px | 由 font 简写或继承确定 |
| 辅助文字 `.station` | 800 10px ui-monospace,Consolas,monospace | font 简写中声明 | letter-spacing: 2px |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px` | `body` 的 `padding` |
| 布局间距 | `未单独声明` | 由组件行逐项定义 |
| 圆角 | `46px` | `.phone` 的 `border-radius` |
| 边框或阴影 | `8px solid #05060b` | `.phone` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.controls button` | 未单独声明 | border: 0; background: transparent; color: var(--cream); font-size: 29px | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.phone` | width: min(390px,100%); height: min(820px,calc(100vh - 32px)); min-height: 690px; border-radius: 46px | background: var(--night); border: 8px solid #05060b; border-radius: 46px; box-shadow: 0 30px 70px #000 | 未声明独立状态；保持默认样式 |
| 内容容器 `.controls .play` | width: 66px; height: 66px; border-radius: 50%; margin: auto | border-radius: 50%; background: var(--cream); color: var(--night); font-size: 25px; box-shadow: 0 0 0 7px #363950 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | body → padding: 0; .phone → width: 100%; height: 100vh; border: 0; border-radius: 0; .art → max-width: 330px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“余晖电台 · 正在播放” → “AFTERGLOW FM · 93.7” → “•••” → “SIDE A / 04” → “穿过没有灯的桥” → “北纬乐队 ·《夜航手册》” → “1:48” → “4:42” → “正在播放 · 高品质” → “接下来播放” → “04 穿过没有灯的桥 · 4:42” → “05 旧港口的雨 · 3:58”。控件占位或辅助标签包括：“更多”、“山脊落日与磁带封面”、“上一首”、“暂停”、“下一首”、“收藏”、“播放队列”、“定时关闭”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| `.queue` 状态变化 | transition: .25s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; .cassette → transform: translateX(-50%) |
| `.queue` 状态变化 | transition: .25s | 状态类或伪类改变对应 CSS 属性 | * → transition: none!important; .cassette → transform: translateX(-50%) |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .art 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#15182a`、`#5cc6c2`、`#10111b`、`#9296ad`、`#292c43` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.controls button`、输入、选择或次操作 `.phone` 与 内容容器 `.controls .play` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“余晖电台 · 正在播放”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
