# 048 山线行程

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`048-alpine-route.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #c7d5d0; color: var(--ink) |
| 主要结构 `.hero` | height: 185px; padding: 22px | 未单独声明 | background: linear-gradient(160deg,#7fa69d,var(--pine)); color: white |
| 关键内容区 `.trip` | width: 100%; padding: 12px; margin: 7px 0 | display: flex; justify-content: space-between | border: 1px solid #b8c9c4; background: white |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--snow` | `#f3f6f1` | 品牌或局部强调 |
| `--pine` | `#173f38` | 品牌或局部强调 |
| `--ice` | `#cce1dc` | 品牌或局部强调 |
| `--ink` | `#17322e` | 主要文字与高对比边界 |
| `--muted` | `#70847f` | 辅助文字与弱化信息 |
| `--orange` | `#e67b3d` | 品牌或局部强调 |
| `--ok` | `#2f8065` | 成功反馈 |
| `--danger` | `#bb4d3f` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.hero h1` | 继承页面字体 | font-size: 29px | 由 font 简写或继承确定 |
| 分区标题 `.route input` | inherit | font 简写中声明 | 由 font 简写或继承确定 |
| 辅助文字 `.confirm` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 800 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `22px` | `.hero` 的 `padding` |
| 布局间距 | `8px` | `.route` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `0 24px 70px #2b4b4455` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.search button` | width: 100%; padding: 11px; margin-top: 11px | border: 0; background: var(--pine); color: white | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.route input` | width: 100%; padding: 8px | border: 0; border-bottom: 1px solid #9fb4ae; font: inherit | 未声明独立状态；保持默认样式 |
| 内容容器 `.trip` | width: 100%; padding: 12px; margin: 7px 0; display: flex | border: 1px solid #b8c9c4; background: white; text-align: left | .trip.active → outline: 3px solid var(--orange) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“山线行程” → “MOUNTAIN LINE / 山线” → “从城市，去更高的地方” → “今日山口晴 · 18°C” → “搜索山线班次” → “3 个班次 · 路线条件已保存” → “08:20 → 10:05” → “晨雾号 · 售罄检查” → “¥86” → “09:10 → 11:02” → “青松号 · 余 8 席” → “¥92”。控件占位或辅助标签包括：“出发地”、“目的地”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.hero 与 .trip 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#e67b3d`、`#17322e`、`#bb4d3f`、`#f3f6f1`、`#2f8065` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.search button`、输入、选择或次操作 `.route input` 与 内容容器 `.trip` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“山线行程”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

搜索出发到目的地，选择可用班次和座位，确认后得到行程编号。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

路线搜索 → 班次与座位 → 成功凭证；售罄班次 → 错误反馈 → 改选可用项 → 再确认。

## 正常流程

搜索路线，选青松号和 7B，点确认，看到 ML-814-7B 凭证。

## 异常触发与恢复

选标注“售罄检查”的晨雾号并确认；错误指出班次售罄且路线字段保留；点改选后再确认成功。

## 数据变化

搜索更新路线摘要；选择改变班次和座位；售罄不生成凭证；恢复设置为 09:10/7A。

## 人工验收步骤

正常：搜索 → 选 09:10/7B → 确认 → 核对凭证。异常：选 08:20 → 确认见售罄 → 确认路线仍在 → 改选 → 再确认成功。
