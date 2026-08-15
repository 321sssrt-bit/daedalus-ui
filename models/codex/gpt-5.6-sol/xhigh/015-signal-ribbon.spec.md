# 015 信号缎带

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`015-signal-ribbon.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.node` | width: 18px; height: 18px; margin: 15px auto 0 | 未单独声明 | border: 4px solid var(--bg); border-radius: 50%; background: #c0afb1; z-index: 1 |
| 关键内容区 `.card` | padding: 18px 20px | 未单独声明 | background: var(--surface); border-radius: 18px; border: 1px solid #eadcdb |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#fff3ed` | 页面或区域背景 |
| `--surface` | `#ffffff` | 容器与表面 |
| `--text` | `#402f34` | 主要文字与高对比边界 |
| `--muted` | `#907b80` | 辅助文字与弱化信息 |
| `--accent` | `#d54f70` | 主要操作与强调状态 |
| `--success` | `#3b8065` | 成功反馈 |
| `--danger` | `#c94149` | 错误与危险反馈 |
| `--purple` | `#76569b` | 品牌或局部强调 |
| `--orange` | `#e38a42` | 品牌或局部强调 |
| `--blue` | `#5289b5` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-sans-serif,system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.head h1` | 500 clamp(42px,6vw,72px)/.95 Georgia,"Songti SC",serif | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.card h2` | 继承页面字体 | font-size: 16px | 由 font 简写或继承确定 |
| 辅助文字 `.head small` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 900; letter-spacing: .14em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `42px 0` | `.page` 的 `padding` |
| 布局间距 | `8px` | `.filter` 的 `gap` |
| 圆角 | `21px` | `.markall` 的 `border-radius` |
| 边框或阴影 | `1px solid var(--text)` | `.markall` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.filter button` | padding: 8px 13px; border-radius: 18px | border: 0; background: #eadedb; color: var(--muted); border-radius: 18px; font-weight: 700 | .filter button.active → background: var(--text); color: white |
| 输入、选择或次操作 `.filter` | display: flex; margin-bottom: 20px | 未单独声明 | .filter button.active → background: var(--text); color: white |
| 内容容器 `.card button` | border-radius: 8px; padding: 8px 12px; margin-top: 10px | border: 0; background: var(--text); color: white; border-radius: 8px; font-weight: 700 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:700px)` | .page → width: calc(100% - 24px); padding: 24px 0; .head → align-items: start; .head h1 → font-size: 46px; .markall → width: 42px; padding: 0; .markall:after → content: "✓"; font-size: 15px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“信号缎带 · 通知中心” → “RIBBON / TODAY” → “今天的信号，” → “按时间落下来。” → “全部标为已读” → “全部 6” → “未读 3” → “安全 1” → “10:42” → “刚刚” → “协作动态” → “未读”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.node 与 .card 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#76569b`、`#d54f70`、`#3b8065`、`#907b80`、`#fff3ed` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.filter button`、输入、选择或次操作 `.filter` 与 内容容器 `.card button` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:700px)` 条件下，布局按响应式表变化且“信号缎带 · 通知中心”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
