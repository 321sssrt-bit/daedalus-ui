# 045 夜航电台

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`045-nocturne-radio.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--black); color: var(--ink) |
| 主要结构 `.shell` | max-width: 1280px; min-height: 800px; margin: auto; padding: 24px 34px | 未单独声明 | 未单独声明 |
| 关键内容区 `.disc` | width: 220px; height: 220px | display: grid; place-items: center | border: 1px solid var(--acid); border-radius: 50%; box-shadow: 0 0 60px #c9ff4f20 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--black` | `#08090b` | 品牌或局部强调 |
| `--panel` | `#15171d` | 容器与表面 |
| `--ink` | `#f1f0e8` | 主要文字与高对比边界 |
| `--muted` | `#8f929a` | 辅助文字与弱化信息 |
| `--acid` | `#c9ff4f` | 品牌或局部强调 |
| `--violet` | `#8d68ff` | 品牌或局部强调 |
| `--ok` | `#6ed3a4` | 成功反馈 |
| `--danger` | `#ff665e` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.player h1` | 继承页面字体 | font-size: 34px | 由 font 简写或继承确定 |
| 分区标题 `.library h2` | 继承页面字体 | font-size: 13px | 由 font 简写或继承确定 |
| 辅助文字 `.nav b` | 继承页面字体 | 16px / normal（浏览器默认） | letter-spacing: .18em |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `24px 34px` | `.shell` 的 `padding` |
| 布局间距 | `28px` | `.layout` 的 `gap` |
| 圆角 | `50%` | `.disc` 的 `border-radius` |
| 边框或阴影 | `1px solid #343740` | `.nav` 的 `border-bottom` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.queue button` | width: 100%; padding: 7px | text-align: left; border: 0; background: transparent; color: var(--muted) | .queue button.active → color: var(--ink) |
| 输入、选择或次操作 `.disc` | width: 220px; height: 220px; border-radius: 50%; display: grid | border: 1px solid var(--acid); border-radius: 50%; box-shadow: 0 0 60px #c9ff4f20 | 未声明独立状态；保持默认样式 |
| 内容容器 `.cover` | width: 55px; height: 55px; display: grid | background: linear-gradient(135deg,var(--violet),#2a1939); font-size: 24px | .show:nth-of-type(2) .cover → background: linear-gradient(135deg,#d2683c,#422018); .show:nth-of-type(3) .cover → background: linear-gradient(135deg,#3d8e8b,#102b32) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:850px)` | .layout → grid-template-columns: 1fr; .studio → grid-template-columns: 1fr; .library → display: none | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“夜航电台” → “NOCTURNE / 夜航” → “收藏状态：” → “未保存” → “今晚值得听” → “潮汐之后” → “声音纪录” → “凌晨建筑学” → “城市谈话” → “暗室植物” → “自然观察” → “READY / 00:00”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → animation: none!important; transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → animation: none!important; transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .disc 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#15171d`、`#8d68ff`、`#8f929a`、`#f1f0e8`、`#c9ff4f` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.queue button`、输入、选择或次操作 `.disc` 与 内容容器 `.cover` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:850px)` 条件下，布局按响应式表变化且“夜航电台”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

从左侧发现节目，开始播放，调整进度或队列，保存当前播放位置。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

节目库 → 播放室（暂停/播放/进度/队列）→ 保存状态；中断 → 错误通知 → 重连 → 原位置继续。

## 正常流程

选节目，点开始播放，拖动进度，换队列项目，再点保存进度，页眉显示保存结果。

## 异常触发与恢复

点“模拟网络中断”，播放暂停并显示保留时间；点“重新连接并继续”，按钮恢复为播放中且进度值不回退。

## 数据变化

选择节目改变标题；进度与队列可变；保存写入页眉状态；异常只暂停并保留 lastProgress。

## 人工验收步骤

正常：选凌晨建筑学 → 播放 → 拖进度 → 改队列 → 保存并看页眉。异常：播放中模拟中断 → 核对进度 → 重连 → 确认继续播放。
