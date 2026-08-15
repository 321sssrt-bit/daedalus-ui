# 044 落日广场

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`044-sunset-club.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #e7b7ac; color: var(--ink) |
| 主要结构 `.phone` | width: min(390px,100%); height: 760px; margin: 20px auto | 未单独声明 | background: var(--cream); overflow: auto; box-shadow: 0 25px 65px #773d4b44 |
| 关键内容区 `.top` | padding: 18px 20px | position: sticky; display: flex; justify-content: space-between | z-index: 2; background: var(--sunset); color: white |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--sunset` | `#ff795f` | 品牌或局部强调 |
| `--peach` | `#ffd1b8` | 品牌或局部强调 |
| `--cream` | `#fff7e9` | 品牌或局部强调 |
| `--ink` | `#4a2730` | 主要文字与高对比边界 |
| `--muted` | `#9a6b6a` | 辅助文字与弱化信息 |
| `--purple` | `#77558e` | 品牌或局部强调 |
| `--ok` | `#38856c` | 成功反馈 |
| `--danger` | `#bd3f54` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.composer textarea` | inherit | font 简写中声明 | 由 font 简写或继承确定 |
| 分区标题 `.row button` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 700 |
| 辅助文字 `.meta` | 继承页面字体 | font-size: 12px | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `18px 20px` | `.top` 的 `padding` |
| 布局间距 | `10px` | `.author` 的 `gap` |
| 圆角 | `20px 20px 6px 20px` | `.post` 的 `border-radius` |
| 边框或阴影 | `0 25px 65px #773d4b44` | `.phone` 的 `box-shadow` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.row button` | padding: 9px 16px | border: 0; background: var(--purple); color: white; font-weight: 700 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.composer textarea` | width: 100%; height: 88px; padding: 13px | border: 0; background: #fff0df; color: var(--ink); font: inherit | 未声明独立状态；保持默认样式 |
| 内容容器 `.avatar` | width: 38px; height: 38px; border-radius: 50%; display: grid | border-radius: 50%; background: var(--peach); font-weight: 800 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; height: 100vh | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“落日广场” → “晚风 24°C” → “今天的云像一封没有封口的信。” → “所有人可见” → “仅好友可见” → “仅自己可见” → “发布此刻” → “测试：让本次发布失败” → “岚岛” → “12 分钟前 · 海堤” → “风把潮声推到城市的台阶上。” → “♡ 42 回应 7”。控件占位或辅助标签包括：“可见范围”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .top 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#77558e`、`#ff795f`、`#4a2730`、`#bd3f54`、`#ffd1b8` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.row button`、输入、选择或次操作 `.composer textarea` 与 内容容器 `.avatar` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“落日广场”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

浏览动态，编辑自己的文字并选择可见范围，发布后在流首看到它。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

动态浏览/顶部编辑器 → 发布成功插入首条；测试失败 → 草稿保留反馈 → 恢复重试 → 成功首条。

## 正常流程

浏览现有两条动态，修改文字和范围，点发布，在首条看到内容、范围和“刚刚”。

## 异常触发与恢复

勾“让本次发布失败”后发布；错误条说明未发布，文本和范围均不变；点“恢复后重试”后成功。

## 数据变化

成功增加一条动态并清空编辑器；失败不增加动态、不清空草稿、不重置范围。

## 人工验收步骤

正常：改文字 → 选仅好友 → 发布 → 首条核对。异常：写新草稿 → 选仅自己 → 勾失败 → 发布 → 核对草稿/范围保留 → 重试成功。
