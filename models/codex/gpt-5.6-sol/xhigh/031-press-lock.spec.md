# 031 开印确认

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`031-press-lock.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0; min-height: 100vh | 未单独声明 | background: var(--news); color: var(--ink) |
| 主要结构 `.page` | max-width: 1040px; margin: 50px auto; padding: 0 28px; gap: 60px | display: grid; grid-template-columns: 1fr 360px; gap: 60px | 未单独声明 |
| 关键内容区 `.confirm` | padding: 26px | position: sticky | border: 4px solid var(--ink); background: #faf8f1; box-shadow: 9px 9px 0 var(--ink) |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--news` | `#f3f0e7` | 品牌或局部强调 |
| `--ink` | `#171715` | 主要文字与高对比边界 |
| `--muted` | `#6f6c65` | 辅助文字与弱化信息 |
| `--red` | `#d52b1e` | 错误与危险反馈 |
| `--blue` | `#1a55a5` | 品牌或局部强调 |
| `--green` | `#347254` | 成功反馈 |
| `--literal-7` | `#aaa59a` | HTML 中直接声明的局部色 |
| `--literal-8` | `#faf8f1` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC","SimSun",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.proof h1` | 继承页面字体 | font-size: 64px; line-height: .95 | letter-spacing: -3px |
| 分区标题 `.confirm h2` | 继承页面字体 | font-size: 30px; line-height: 1.08 | 由 font 简写或继承确定 |
| 辅助文字 `.paper` | 继承页面字体 | font-size: 20px | font-weight: 900; letter-spacing: 4px |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `13px clamp(24px,5vw,70px)` | `.top` 的 `padding` |
| 布局间距 | `60px` | `.page` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `7px double var(--ink)` | `.top` 的 `border-block` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.publish` | width: 100%; padding: 15px | border: 0; background: var(--red); color: white; font-weight: 900 | .publish:disabled → background: #b0aca4; color: #e7e4dd; cursor: not-allowed; .publish:focus-visible,.back:focus-visible,input:focus-visible → outline: 3px solid var(--blue) |
| 输入、选择或次操作 `.check input` | margin-top: 3px | 未单独声明 | 未声明独立状态；保持默认样式 |
| 内容容器 `.back` | width: 100%; padding: 13px | border: 0; background: transparent; color: var(--blue) | .publish:focus-visible,.back:focus-visible,input:focus-visible → outline: 3px solid var(--blue) |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:820px)` | .page → grid-template-columns: 1fr; .confirm → position: static; .proof h1 → font-size: 48px; .article → columns: 1 | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“开印确认 · 发布确认” → “城 市 侧 面” → “终校版 · VOL. 082 / PAGE A1” → “城市 / 公共空间” → “凌晨四点，” → “菜市场开始发光” → “记者 周砚 摄影 许之遥 最后编辑于 14:28” → “第一辆货车倒进巷口时，天还是深蓝色。摊主掀开绿色帆布，水汽从蔬菜箱里升起，临街的灯一盏盏亮了。” → “这座市场将在今天结束后进入三个月改造。新的设计保留原本的尺度，也把雨水、废弃菜叶和每天最拥挤的十分钟重新纳入考虑。” → “对附近居民来说，它从来不只是一处买菜的地方。钥匙寄放在熟悉的摊位，错过快递的人在这里问一圈，总能得到线索。” → “改造团队说，他们要保护的不是怀旧外观，而是那些没有被写进制度、却真实运转了二十年的协作。” → “不可撤回操作”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.page 与 .confirm 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#6f6c65`、`#d52b1e`、`#f3f0e7`、`#171715`、`#aaa59a` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.publish`、输入、选择或次操作 `.check input` 与 内容容器 `.back` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:820px)` 条件下，布局按响应式表变化且“开印确认 · 发布确认”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
