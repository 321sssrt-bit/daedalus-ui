# 006 黄铜门铃

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`006-brass-keypad.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh; padding: 24px | display: grid; place-items: center | background: radial-gradient(circle at 50% 30%,#553d2b,var(--bg) 48%,var(--deep)); color: var(--text) |
| 主要结构 `.dial` | width: 150px; height: 150px; margin: auto | display: grid; place-items: center | border: 12px double #85643a; border-radius: 50%; box-shadow: inset 0 0 0 12px #2b211a |
| 关键内容区 `.panel` | padding: 46px | 未单独声明 | background: linear-gradient(#453326,#39281e) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#2b211a` | 页面或区域背景 |
| `--surface` | `#433124` | 容器与表面 |
| `--text` | `#f5e7cd` | 主要文字与高对比边界 |
| `--muted` | `#b9a486` | 辅助文字与弱化信息 |
| `--accent` | `#e0b55e` | 主要操作与强调状态 |
| `--success` | `#73b18c` | 成功反馈 |
| `--danger` | `#e36c60` | 错误与危险反馈 |
| `--deep` | `#17110d` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-monospace,"Cascadia Mono","Microsoft YaHei",monospace | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.panel h1` | 600 31px/1.2 Georgia,"Songti SC",serif | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.brand` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 800; letter-spacing: .16em |
| 辅助文字 `.dial:after` | 继承页面字体 | font-size: 46px | font-weight: 800 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px` | `body` 的 `padding` |
| 布局间距 | `8px` | `.digits` 的 `gap` |
| 圆角 | `42px` | `.device` 的 `border-radius` |
| 边框或阴影 | `1px solid #806344` | `.device` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.digits input` | height: 62px; border-radius: 8px | border: 1px solid #92724d; border-radius: 8px; background: #201711; color: var(--accent); text-align: center; font: 800 26px monospace | .digits input:focus → box-shadow: 0 0 0 3px #e0b55e22,inset 0 4px 9px #0008 |
| 输入、选择或次操作 `.feedback.good` | 未单独声明 | color: var(--success); border-color: var(--success) | 未声明独立状态；保持默认样式 |
| 内容容器 `.panel` | padding: 46px | background: linear-gradient(#453326,#39281e) | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:700px)` | .inner → grid-template-columns: 1fr; .side → display: none; .panel → padding: 36px 22px; .digits → gap: 5px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“黄铜门铃 · 二次验证” → “BELLHOUSE / 1926” → “安全通道 #481” → “端到端加密” → “本次位置：香港” → “请按下第二道门铃” → “我们已向尾号 5812 的设备发送六位验证码。正确演示码为” → “381204” → “；连续三次错误会暂时锁定。” → “确认是我本人” → “验证码” → “00:45”。控件占位或辅助标签包括：“第1位”、“第2位”、“第3位”、“第4位”、“第5位”、“第6位”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.dial 与 .panel 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#e0b55e`、`#b9a486`、`#17110d`、`#2b211a`、`#73b18c` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.digits input`、输入、选择或次操作 `.feedback.good` 与 内容容器 `.panel` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:700px)` 条件下，布局按响应式表变化且“黄铜门铃 · 二次验证”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
