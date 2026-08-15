# 008 隐私透镜

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`008-privacy-lens.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.app` | min-height: 100vh | display: grid; grid-template-columns: 220px 1fr | 未单独声明 |
| 关键内容区 `.reason` | padding: 16px; margin: 22px 0; gap: 12px | display: grid; grid-template-columns: 32px 1fr; gap: 12px; align-items: start | background: #f2f7f4; border-radius: 16px |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#d9ece6` | 页面或区域背景 |
| `--surface` | `#ffffff` | 容器与表面 |
| `--text` | `#173e39` | 主要文字与高对比边界 |
| `--muted` | `#64817c` | 辅助文字与弱化信息 |
| `--accent` | `#0d8f7b` | 主要操作与强调状态 |
| `--success` | `#1e7a58` | 成功反馈 |
| `--danger` | `#bd4a50` | 错误与危险反馈 |
| `--sand` | `#f1e4c7` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | ui-sans-serif,system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.modal h1` | 继承页面字体 | font-size: 30px | 由 font 简写或继承确定 |
| 分区标题 `.brand` | 继承页面字体 | font-size: 22px | font-weight: 900 |
| 辅助文字 `.reason small` | 继承页面字体 | line-height: 1.45 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `30px 24px` | `.side` 的 `padding` |
| 布局间距 | `8px` | `.side nav` 的 `gap` |
| 圆角 | `10px` | `.side button` 的 `border-radius` |
| 边框或阴影 | `1px solid #bed4ce` | `.side` 的 `border-right` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.side button` | padding: 13px; border-radius: 10px | border: 0; background: transparent; text-align: left; border-radius: 10px; color: var(--muted); font-weight: 700 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.lens` | width: 76px; height: 76px; border-radius: 50%; display: grid | border-radius: 50%; background: #d9f1ea; font-size: 34px; color: var(--accent) | 未声明独立状态；保持默认样式 |
| 内容容器 `.btn` | height: 50px; border-radius: 13px | border: 1px solid #c4d7d2; border-radius: 13px; background: white; color: var(--text); font-weight: 800 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:740px)` | .app → grid-template-columns: 1fr; .side → display: none; .map → min-height: 100vh; .modal → padding: 28px; .actions → grid-template-columns: 1fr | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“步迹 · 定位权限” → “步迹” → “附近发现” → “我的路线” → “离线地图” → “隐私设置” → “允许「步迹」使用你的位置？” → “我们需要定位来显示附近的安静路线，并在你偏离路线时给出方向。位置不会用于广告，也不会公开给其他人。” → “你始终掌握开关” → “选择“仅此一次”会在关闭页面后失效；可随时在隐私设置中撤回。” → “暂不允许” → “仅此一次”。控件占位或辅助标签包括：“附近步行地图”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important; animation: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important; animation: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.app 与 .reason 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#0d8f7b`、`#bd4a50`、`#1e7a58`、`#173e39`、`#64817c` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.side button`、输入、选择或次操作 `.lens` 与 内容容器 `.btn` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:740px)` 条件下，布局按响应式表变化且“步迹 · 定位权限”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
