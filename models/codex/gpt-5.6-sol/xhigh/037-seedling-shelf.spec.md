# 037 新芽清单

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`037-seedling-shelf.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: #edf0e8; color: var(--ink) |
| 主要结构 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto | position: relative | background: var(--cream); border-radius: 34px; overflow: hidden; box-shadow: 0 20px 60px #49645130 |
| 关键内容区 `.leaf` | width: 48px; height: 27px | position: absolute | background: var(--mint); border: 3px solid var(--green); border-radius: 100% 0 100% 0 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--mint` | `#dff4df` | 品牌或局部强调 |
| `--cream` | `#fffdf3` | 品牌或局部强调 |
| `--ink` | `#1e3b2d` | 主要文字与高对比边界 |
| `--muted` | `#6d8878` | 辅助文字与弱化信息 |
| `--green` | `#2d8155` | 成功反馈 |
| `--sun` | `#f5b94c` | 品牌或局部强调 |
| `--danger` | `#c75b56` | 错误与危险反馈 |
| `--literal-8` | `#edf0e8` | HTML 中直接声明的局部色 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | system-ui,"Microsoft YaHei",sans-serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `h1` | 继承页面字体 | font-size: 25px | 由 font 简写或继承确定 |
| 分区标题 `.logo` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 800 |
| 辅助文字 `.empty p` | 继承页面字体 | font-size: 14px; line-height: 1.6 | 由 font 简写或继承确定 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `26px 24px 14px` | `.top` 的 `padding` |
| 布局间距 | `未单独声明` | 由组件行逐项定义 |
| 圆角 | `34px` | `.phone` 的 `border-radius` |
| 边框或阴影 | `34px` | `.phone` 的 `border-radius` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.primary` | border-radius: 14px; padding: 14px 26px; margin-top: 12px | border: 0; border-radius: 14px; background: var(--green); color: white; font-weight: 700 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.new input` | width: 100%; padding: 12px; border-radius: 10px | border: 1px solid #93bca1; border-radius: 10px; background: white; font: inherit | .new.show → display: block |
| 内容容器 `.phone` | width: min(390px,100%); min-height: 760px; margin: 20px auto; border-radius: 34px | background: var(--cream); border-radius: 34px; box-shadow: 0 20px 60px #49645130 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390 × 844 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:430px)` | .phone → margin: 0; min-height: 100vh; border-radius: 0 | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“新芽清单” → “芽册” → “这里正等第一件小事” → “把想开始的事种下来。哪怕只有五分钟，也算今天发了一颗芽。” → “种下第一件事” → “第一颗种子叫什么？” → “放进今天” → “今天” → “花园” → “回顾” → “我的”。控件占位或辅助标签包括：“事项名称”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 390 × 844 px 下，body、.phone 与 .leaf 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#c75b56`、`#2d8155`、`#fffdf3`、`#edf0e8`、`#dff4df` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.primary`、输入、选择或次操作 `.new input` 与 内容容器 `.phone` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:430px)` 条件下，布局按响应式表变化且“新芽清单”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。
