# 001 登录

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`001-telegraph.html`
- 复现范围：登录卡片整页；含样式化交互（显示/隐藏密码、空值校验、提交假延迟与成功回执、忘记密码反馈）

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | 视口尺寸 1280×800；body 内边距 32px 16px；`display:flex` 居中 | 整套背景为 28×28px 的双向细网格线（rgba(28,36,22,.035)） | body 为滚动容器；最小高 100vh |
| 卡片 sheet | 最大宽度 960px；高至少 560px；边框 1px solid #c9bd9c；阴影 0 6px 0 rgba(28,36,22,.12) | `display:grid;grid-template-columns:1fr 1fr`；左右各占 50% | 背景 #e9dfc4；相对定位；顶部中央有 11px 字距 0.35em 的淡字「远望电讯 · 每日电报」 |
| 品牌区 visual | 左栏；padding 64px 40px 40px；右侧 1px dashed #c9bd9c 分隔 | `flex;flex-direction:column;justify-content:space-between` | 背景含径向渐变 (rgba(15,110,107,.10))；SVG 图最大宽 300px 居中 |
| 表单区 form-side | 右栏；padding 72px 48px 40px | `flex;flex-direction:column;justify-content:center` | 背景 #faf6e9；内容整体垂直居中 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--paper` | `#f3ecd9` | 页面底、SVG 高光点缀 |
| `--paper-deep` | `#e9dfc4` | 卡片外框背景 |
| `--ink` | `#1c2416` | 主文字、线条 |
| `--ink-soft` | `#4c5341` | 次要文字、标签 |
| `--ink-mute` | `#8a8a70` | 弱化文字、禁用态 |
| `--teal` | `#0f6e6b` | 品牌主色、主按钮、焦点 |
| `--teal-dark` | `#0a4f4d` | 主按钮悬停、品牌字 |
| `--signal` | `#c0392b` | 错误信号、强调字 |
| `--line` | `#c9bd9c` | 边框、分隔线 |
| `--card` | `#faf6e9` | 表单卡片面 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 显示字（h1） | "Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif | 26px / 1.3 | 400（默认）/ 正常 |
| 品牌 title | 同上 | 22px / 1.4 | 800 / 0.12em |
| 正文 | 同上 | 15px / 1.5 | 400 / 正常 |
| 辅助文字 | 同上 | 11–13px / 1.8–1.9 | 400–500 / 0.08–0.35em |
| 收报机 ledger | "Courier New",Consolas,monospace | 13px / 1.8 | 400 / 正常 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 8–28px 梯度（8/10/14/18/24/28） | 字段间距、区块间距 |
| 控件圆角 | 4px | 输入框、主按钮 |
| 容器圆角 | 0（直角卡片） | sheet |
| 边框 / 阴影 | 1px solid #c9bd9c；主按钮 1px solid #0a4f4d；卡片 0 6px 0 rgba(28,36,22,.12) | 分隔与层级 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主操作（登录按钮） | 全宽；padding 14px；字号 15px；字距 .25em；圆角 4px | 背景 #0f6e6b、文字 #f6f2e2、边框 #0a4f4d；含圆点 span | 悬停：背景 #0a4f4d；按下：translateY(1px)；加载：disabled + .loading 使圆点 1s steps(2) 闪烁，文案「拍发中…」；成功：恢复可用，文案「已入局 · 发送成功」 |
| 输入框 | 全宽；padding 12px 14px；字号 15px；圆角 4px | 背景 #fffdf4；边框 1px solid #c9bd9c；placeholder #aaa98f | 焦点：边框 #0f6e6b + 3px rgba(15,110,107,.15) 光晕；密码框右侧「显示」切换按钮（12px teal 文字，点击切换 type 与文案 显示/隐藏） |
| 收报机 ledger | 全宽；padding 12px 14px；min-height 44px；等宽字体 | 背景 #f6f0dd；边框 1px dashed #c9bd9c | 空值提交：红色 `.err` 行；成功：绿色 `.ok` 行含证号；忘记密码：`.err` 行（↻ 前缀） |
| 忘记密码链接 | 12px teal 文字；虚线下边框 | 点击显示反馈行 | 悬停：颜色 #0a4f4d |
| 记住我勾选 | 12px；accent-color #0f6e6b | 默认未勾选 | 可点击切换，无其他状态（禁用不适用） |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 1280×800 | 左右两栏各 50%，sheet 最大 960px 居中 | 全量组件可见 |
| ≤820px 宽 | sheet 改单列；品牌区居顶、border-bottom dashed 分隔；SVG 图最大宽 180px；表单 padding 40px 28px 32px | 无组件隐藏；字号不变 |

## 内容与数据

- 品牌名：远望电讯（YUANWANG WIRELESS · EST. 1912）
- 标题：登录远望电讯；副文：输入您的电报员证号与密码，继续收发报文。
- 字段：电报员证号 / 邮箱（placeholder：如：MARS-0417 或 mars@yuanwang.example）；密码（placeholder：输入密码）
- 页面文案：收报机就绪：等待输入证号与密码。；还没有证号？在线申请入局
- 成功回执：`2026-09-04 09:41 证号 <值> 验证通过。今日第 3,217 封报文，等您签发。`
- 校验规则：证号或密码为空 → 对应错误行并聚焦该输入框；非空 → 900ms 延迟后成功。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 输入框聚焦 | .15s 过渡 | 边框变 teal + 光晕 | 关闭 border/box-shadow 过渡 |
| 登录提交 | 900ms setTimeout | 按钮进入加载态、圆点闪烁、文案变化，随后成功回执 | 圆点不闪烁（恒定显示） |
| 按钮按下 | .1s | translateY(1px) | 保持 |

## 复现验收清单

- [ ] 主视口 1280×800：居中的 960px 双栏卡片，左品牌区右表单区，比例 1:1
- [ ] 令牌：#f3ecd9/#e9dfc4/#1c2416/#0f6e6b/#c0392b/#c9bd9c 实际出现在 CSS 与页面
- [ ] 主按钮默认 teal 背景、悬停变深、加载禁用闪烁，成功文案替换
- [ ] 密码框「显示/隐藏」可切换输入类型与按钮文案
- [ ] ≤820px 宽切换单列，SVG 图缩至 180px
- [ ] prefers-reduced-motion 下加载圆点不闪烁
