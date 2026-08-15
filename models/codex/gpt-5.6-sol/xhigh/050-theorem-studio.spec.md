# 050 定理研习室

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`050-theorem-studio.html`
- 复现范围：复现该单文件页面的布局制度、设计令牌、核心组件状态与题定职责。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 `body` | margin: 0 | 未单独声明 | background: var(--paper); color: var(--ink) |
| 主要结构 `.shell` | max-width: 1280px; min-height: 800px; margin: auto | display: grid; grid-template-columns: 270px 1fr | 未单独声明 |
| 关键内容区 `.board` | margin-top: 28px; min-height: 570px; padding: 34px | 未单独声明 | border: 1px solid #4d6c65; box-shadow: inset 0 0 35px #071c18 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--chalk` | `#153b36` | 品牌或局部强调 |
| `--board` | `#0e2d29` | 品牌或局部强调 |
| `--paper` | `#f1ead7` | 容器与表面 |
| `--ink` | `#26312e` | 主要文字与高对比边界 |
| `--muted` | `#807d70` | 辅助文字与弱化信息 |
| `--yellow` | `#efcf68` | 主要操作与强调状态 |
| `--ok` | `#67ba8b` | 成功反馈 |
| `--danger` | `#e77b6e` | 错误与危险反馈 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页面正文 `body` | Georgia,"Songti SC","Microsoft YaHei",serif | 16px / normal（浏览器默认） | 由 font 简写或继承确定 |
| 显示字 `.syllabus h1` | 继承页面字体 | font-size: 24px | 由 font 简写或继承确定 |
| 分区标题 `.concept h2` | 继承页面字体 | font-size: 32px | 由 font 简写或继承确定 |
| 辅助文字 `.lesson.active` | 继承页面字体 | 16px / normal（浏览器默认） | font-weight: 700 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 主要内距 | `28px 22px` | `.syllabus` 的 `padding` |
| 布局间距 | `30px` | `.concept` 的 `gap` |
| 圆角 | `0` | 全局保持直角 |
| 边框或阴影 | `1px solid #bcb39d` | `.syllabus` 的 `border-right` |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主要操作 `.submit` | padding: 12px 22px; margin-top: 12px | background: var(--yellow); color: #18332e; border: 0; font-weight: 800 | 未声明独立状态；保持默认样式 |
| 输入、选择或次操作 `.option` | display: block; width: 100%; padding: 13px; margin: 9px 0 | border: 1px solid #628079; background: transparent; color: white; text-align: left | .option.selected → background: #315f56 |
| 内容容器 `.board` | margin-top: 28px; min-height: 570px; padding: 34px | border: 1px solid #4d6c65; box-shadow: inset 0 0 35px #071c18 | 未声明独立状态；保持默认样式 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280 × 800 px 主视口 | 按“画布与区域布局”保持完整结构 | 按“组件规格与状态”显示默认状态 |
| `(max-width:800px)` | .shell → grid-template-columns: 1fr; .syllabus → display: none; .room → padding: 20px; .concept → grid-template-columns: 1fr; .formula → min-height: 150px | 交互流程与内容顺序不变 |

## 内容与数据

必须保留的可见文案顺序包括：“定理研习室” → “微观概率 · 第一章” → “理解随机，而不是背答案” → “01 样本空间” → “02 独立事件” → “03 条件概率” → “04 贝叶斯更新” → “第 03 课 · 条件概率” → “课程进度 2 / 4” → “已知一件事发生后，世界会变窄。” → “条件概率不是重新掷骰子，而是在已经知道 B 发生的范围里，再数 A 占多少。” → “完成阅读，进入练习”。数值、日期和状态文字沿用页面初始值及其操作后的格式。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接呈现最终状态 | * → transition: none!important |
| 用户操作 | 0ms | 通过文案、颜色或显隐即时反馈 | * → transition: none!important |

## 复现验收清单

- [ ] 在 1280 × 800 px 下，body、.shell 与 .board 的尺寸和排列符合布局表。
- [ ] 规范登记的主色 `#26312e`、`#efcf68`、`#e77b6e`、`#153b36`、`#807d70` 均来自 HTML，背景、正文、弱化与强调层级对应一致。
- [ ] 主要操作 `.submit`、输入、选择或次操作 `.option` 与 内容容器 `.board` 的默认及状态样式可实际观察。
- [ ] 在 `(max-width:800px)` 条件下，布局按响应式表变化且“定理研习室”仍可操作。
- [ ] 启用 `prefers-reduced-motion: reduce` 后，页面按动效表关闭或压缩非必要动画，同时保留状态反馈。


## 产品边界

进入条件概率课程，完成阅读和练习，查看解释，并最终提交正确答案。 本单文件只实现上述任务及题定异常恢复；相邻账户、后台与真实服务能力不在复现范围。

## 状态地图

课程目录/概念讲解 → 单题练习 → 错误解释 → 再次作答 → 订正成功与进度更新。

## 正常流程

点进入练习，选择 B，提交，看到订正成功和课程进度 3/4。

## 异常触发与恢复

选择页面提供的 A 或 C 并提交；错误面板解释条件后样本空间为 3 枚蓝球；点再次作答，改选 B 并提交成功。

## 数据变化

选项只改变本次 answer；错误不更新课程进度；正确后进度从 2/4 更新到 3/4。

## 人工验收步骤

正常：进入练习 → 选 B → 提交 → 见成功/3-4。异常：选 A → 提交 → 阅读解释 → 再次作答 → 选 B → 提交 → 见订正成功。
