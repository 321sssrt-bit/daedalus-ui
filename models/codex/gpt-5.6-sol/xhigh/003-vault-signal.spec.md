# 003 信号库准入

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`003-vault-signal.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--bg); color: var(--text) |
| 主要结构 `.header` | 未单独声明 | display: grid; grid-template-columns: 1fr auto | border-bottom: 2px solid var(--line) |
| 关键内容区 `.top` | height: 46px; padding: 0 24px | display: flex; align-items: center; justify-content: space-between | background: var(--text); color: white |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#e7e4db` | 页面或区域背景 |
| `--surface` | `#f4f1e9` | 容器与表面 |
| `--text` | `#181b1d` | 主要文字与高对比边界 |
| `--muted` | `#61666a` | 辅助文字与弱化信息 |
| `--accent` | `#ff5c35` | 主要操作与强调状态 |
| `--success` | `#167954` | 成功反馈 |
| `--danger` | `#b5292f` | 错误与危险反馈 |
| `--line` | `#202426` | 描边与分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | "Arial Narrow","Microsoft YaHei",system-ui,sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.header h1` | 继承页面字体 | font-size: clamp(42px,7vw,86px); line-height: .85 | letter-spacing: -.07em |
| 分区标题 `.brief h2` | 继承页面字体 | font-size: 30px | 由 font 简写或继承确定 |
| 辅助文字 `.meta small` | 继承页面字体 | font-size: 10px | letter-spacing: .12em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `0 24px` | `.top` 的 `padding` |
| 布局间距 | `8px` | `.status` 的 `gap` |
| 圆角 | `50%` | `.status:before` 的 `border-radius` |
| 边框或阴影 | `50%` | `.status:before` 的 `border-radius` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.btn` | width: 100%; height: 56px | border: 2px solid var(--line); background: var(--text); color: white; font: 800 14px monospace | .btn:hover → background: var(--accent) |
| 输入、选择或次操作 `.code input` | width: 56px; height: 70px | border: 2px solid var(--line); background: #fffefb; text-align: center; font: 800 30px monospace | .code input:focus → box-shadow: 4px 4px 0 #ff5c3544 |
| 内容容器 `.top` | height: 46px; display: flex; padding: 0 24px | background: var(--text); color: white; font-size: 12px | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:760px)` | .body → grid-template-columns: 1fr; .brief → border-right: 0; border-bottom: 2px solid var(--line); .header h1 → font-size: 48px; .stamp → width: 110px; .verify → padding: 30px 20px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“信号库 · 邀请进入” → “VLT—07 / ACCESS CONTROL” → “验证节点在线” → “Signal” → “Vault” → “INVITATION ONLY” → “机密协作空间” → “来自：北岸实验室” → “你被邀请加入「潮汐计划」” → “这里保存尚未公开的研究记录与原型。邀请码与你的身份绑定，仅可使用一次。” → “邀请人” → “苏合 / 主理人”。控件占位或辅助标签包括：“第1位”、“第2位”、“第3位”、“第4位”、“第5位”、“第6位”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.header 与 .top 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#b5292f`、`#f4f1e9`、`#e7e4db`、`#181b1d`、`#61666a` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.btn`、输入、选择或次操作 `.code input` 与 内容容器 `.top` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:760px)` 条件下，布局按响应式表变化且“信号库 · 邀请进入”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
