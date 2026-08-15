# 032 危险仓封

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`032-hazard-vault.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--concrete); color: var(--ink) |
| 主要结构 `.shell` | max-width: 980px; margin: 46px auto; padding: 0 28px | 未单独声明 | 未单独声明 |
| 关键内容区 `.panel` | margin-top: 16px | display: grid; grid-template-columns: 1fr 370px | border: 5px solid var(--ink); background: var(--panel); box-shadow: 13px 13px 0 #6e6c64 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--concrete` | `#c8c5ba` | 品牌或局部强调 |
| `--panel` | `#eeeae0` | 容器与表面 |
| `--ink` | `#181a19` | 主要文字与高对比边界 |
| `--muted` | `#666a67` | 辅助文字与弱化信息 |
| `--yellow` | `#f2c230` | 主要操作与强调状态 |
| `--red` | `#c7352e` | 错误与危险反馈 |
| `--green` | `#3f7457` | 成功反馈 |
| `--white` | `#fff` | 品牌或局部强调 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Arial,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.warning h1` | 继承页面字体 | font-size: 42px; line-height: 1.03 | 由 font 简写或继承确定 |
| 分区标题 `.controls h2` | 继承页面字体 | font-size: 22px | 由 font 简写或继承确定 |
| 辅助文字 `.label` | 800 11px ui-monospace,Consolas,monospace | font 简写中声明 | letter-spacing: 2px |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `0 28px` | `.shell` 的 `padding` |
| 布局间距 | `未单独声明` | 由组件行逐项定义 |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `5px solid var(--ink)` | `.panel` 的 `border` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.gone button` | padding: 14px 22px | background: var(--ink); color: white; border: 0 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.controls input` | width: 100%; margin: 8px 0 18px; padding: 13px | border: 2px solid #646967; background: #262a28; color: white; font: 15px ui-monospace,Consolas,monospace | .controls input:focus → outline: 3px solid var(--yellow) |
| 内容容器 `.panel` | margin-top: 16px; display: grid | border: 5px solid var(--ink); background: var(--panel); box-shadow: 13px 13px 0 #6e6c64 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:800px)` | .panel → grid-template-columns: 1fr; .controls → min-height: 480px; .warning → padding: 32px; .warning h1 → font-size: 34px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“危险仓封 · 永久删除” → “SECURITY ZONE / ACCOUNT DECOMMISSION” → “永久拆除” → “「北岸资料库」” → “这不是退出登录或暂停订阅。确认后，资料库与账号关系会立即解除，恢复窗口不存在。” → “12,840 份文档与附件” → “包括历史版本和已归档内容” → “37 条自动化流程” → “所有触发器会立即停止” → “18 位成员的访问权” → “共享链接也将全部失效” → “仍想保留数据？”。控件占位或辅助标签包括：“在这里输入”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .panel 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#666a67`、`#eeeae0`、`#c8c5ba`、`#181a19`、`#3f7457` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.gone button`、输入、选择或次操作 `.controls input` 与 内容容器 `.panel` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:800px)` 条件下，布局按响应式表变化且“危险仓封 · 永久删除”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
