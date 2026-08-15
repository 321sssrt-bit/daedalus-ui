# 014 零频搜索

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`014-zero-frequency.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.suggestion` | width: 100%; min-height: 70px | display: grid; grid-template-columns: 40px 1fr auto; align-items: center | border: 0; border-bottom: 1px solid var(--line); background: transparent; color: var(--text) |
| 关键内容区 `.bar` | height: 62px; padding: 0 28px | display: flex; align-items: center; justify-content: space-between | border-bottom: 1px solid var(--line) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#101010` | 页面或区域背景 |
| `--surface` | `#1b1b1b` | 容器与表面 |
| `--text` | `#f4f1e8` | 主要文字与高对比边界 |
| `--muted` | `#88877f` | 辅助文字与弱化信息 |
| `--accent` | `#b7ff3c` | 主要操作与强调状态 |
| `--success` | `#7ee6a2` | 成功反馈 |
| `--danger` | `#ff5f6c` | 错误与危险反馈 |
| `--line` | `#343434` | 描边与分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.copy h1` | 继承页面字体 | font-size: 42px; line-height: 1.05 | letter-spacing: -.04em |
| 分区标题 `.logo` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 1000; letter-spacing: -.06em |
| 辅助文字 `.meta` | 继承页面字体 | font-size: 11px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `0 28px` | `.bar` 的 `padding` |
| 布局间距 | `22px` | `.bar nav` 的 `gap` |
| 圆角 | `50%` | `.search button` 的 `border-radius` |
| 边框或阴影 | `1px solid var(--line)` | `.bar` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.search button` | width: 70px; height: 70px; border-radius: 50% | border: 0; border-radius: 50%; background: var(--accent); color: #111; font-size: 28px | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.search input` | width: 100%; height: 92px; padding: 0 100px 0 0 | border: 0; background: transparent; color: var(--text); font-size: clamp(34px,6vw,72px); font-weight: 900 | 未声明独立状态；保持默认样式 |
| 内容容器 `.suggestion` | width: 100%; min-height: 70px; display: grid | border: 0; border-bottom: 1px solid var(--line); background: transparent; color: var(--text); text-align: left; font-size: 15px | .suggestion:hover → color: var(--accent) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:760px)` | .empty → grid-template-columns: 1fr; gap: 60px; .zero → font-size: 190px; .search input → height: 78px; .page → width: calc(100% - 28px); .bar nav → display: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“零频搜索 · 无结果” → “ZERO” → “FREQ” → “文章” → “项目” → “人物” → “内部知识搜索 / BETA” → “查询：会飞的鲸鱼发票” → “0 条匹配 · 0.18 秒” → “这个频段里，” → “没有任何回声。” → “我们保留了刚才的搜索词，但没有找到相符的文章、项目或成员。试着去掉形容词，或者换成更可能出现在标题里的词。”。控件占位或辅助标签包括：“搜索词”、“搜索”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.suggestion 与 .bar 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#1b1b1b`、`#f4f1e8`、`#ff5f6c`、`#b7ff3c`、`#101010` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.search button`、输入、选择或次操作 `.search input` 与 内容容器 `.suggestion` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:760px)` 条件下，布局按响应式表变化且“零频搜索 · 无结果”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
