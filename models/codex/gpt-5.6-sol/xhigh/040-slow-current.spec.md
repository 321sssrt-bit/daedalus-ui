# 040 缓流队列

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`040-slow-current.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #d9d7e8; color: var(--ink) |
| 主要结构 `.orb` | width: 180px; height: 180px; margin: 70px auto 38px | display: grid; place-items: center | border-radius: 50%; background: radial-gradient(circle at 38% 33%,#fff 0 8%,#b9c8e5 28%,var(--violet) 70%); box-shadow: 0 18px 45px #7167a84d; color: white |
| 关键内容区 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; padding: 26px 24px | 未单独声明 | background: var(--mist); box-shadow: 0 24px 70px #58547730 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--mist` | `#eceafa` | 品牌或局部强调 |
| `--card` | `#faf9ff` | 容器与表面 |
| `--ink` | `#2d2b49` | 主要文字与高对比边界 |
| `--muted` | `#817e9d` | 辅助文字与弱化信息 |
| `--violet` | `#7167a8` | 品牌或局部强调 |
| `--blue` | `#8db9cf` | 品牌或局部强调 |
| `--ok` | `#5f927f` | 成功反馈 |
| `--danger` | `#b76a77` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `h1` | 继承页面字体 | font-size: 25px | 由 font 简写或继承确定 |
| 分区标题 `.top` | 继承页面字体 | font-size: 12px | 由 font 简写或继承确定 |
| 辅助文字 `.orb b` | 继承页面字体 | font-size: 38px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `26px 24px` | `.phone` 的 `padding` |
| 布局间距 | `12px` | `.step` 的 `gap` |
| 圆角 | `50%` | `.orb` 的 `border-radius` |
| 边框或阴影 | `0 24px 70px #58547730` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `button` | padding: 12px; border-radius: 12px | border: 1px solid #b8b4d0; border-radius: 12px; background: transparent; color: var(--ink); font-weight: 600 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.orb` | width: 180px; height: 180px; border-radius: 50%; margin: 70px auto 38px; display: grid | border-radius: 50%; background: radial-gradient(circle at 38% 33%,#fff 0 8%,#b9c8e5 28%,var(--violet) 70%); box-shadow: 0 18px 45px #7167a84d; color: white | 未声明独立状态；保持默认样式 |
| 内容容器 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; padding: 26px 24px | background: var(--mist); box-shadow: 0 24px 70px #58547730 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh; box-shadow: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“缓流队列” → “静默处理” → “任务 W-214” → “68%” → “正在校准颜色” → “作品正在穿过最后一道门” → “预计还需 1 分 20 秒，可以安心离开此页。” → “已接收 12 个素材” → “版式检查完成” → “生成交付文件” → “放到一边” → “取消任务”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → animation: none!important; transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → animation: none!important; transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.orb 与 .phone 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#eceafa`、`#2d2b49`、`#5f927f`、`#8db9cf`、`#817e9d` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `button`、输入、选择或次操作 `.orb` 与 内容容器 `.phone` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“缓流队列”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
