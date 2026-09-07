# 036 编辑发布

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`036-compose-thumb-post.html`
- 复现范围：手机发帖编辑器，含标题/正文、字数状态、发布与存草稿

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机框 | 390×844，背景 `#fff5f2` | 外圈 `#e8c4b8` 居中 | column 三区 |
| 顶栏 | padding 48×16×12，border-bottom | 取消左、发布右 | 发布 pill 形 |
| 表单 | flex 1 padding 20，gap 16 | 标题 input + textarea flex 1 | textarea min-height 200px scroll |
| 状态栏 | padding 12×20×28 border-top | counter 左、草稿钮右 | 固定底 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#fff5f2` | 手机背景 |
| `--surface` | `#fff` | 顶栏、状态栏 |
| `--text` | `#2d1a14` | 输入文字 |
| `--muted` | `#9a7b72` | placeholder、counter |
| `--accent` | `#ff6b4a` | 发布钮 |
| `--draft` | `#6b8cce` | 草稿钮描边 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题输入 | system-ui | 20px | 600 |
| 正文 | system-ui | 16px / 1.65 | 400 |
| 工具栏 | system-ui | 15px | 400–600 |
| counter | system-ui | 13px | 400/600 warn |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 发布钮圆角 | 20px pill | toolbar |
| 草稿钮圆角 | 20px | status-bar |
| 字数上限 | 500 | body maxlength |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 发布 | padding 8×20 | accent 底，disabled opacity 0.4 | ≥10 字 enabled；发布后「已发布」disabled |
| 取消 | 透明 | muted | 点击 toast「已放弃编辑」 |
| 存草稿 | border draft 色 | 透明底 | 点击 counter 变「草稿已保存」+ toast |
| counter | 13px | muted；>450 warn `#e6a817` 600 | 随输入更新 n/500 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390×844 | 固定手机框 | 表单区 scroll |
| 宽屏 | 居中手机框 | 不变 |
| prefers-reduced-motion | 不适用 | toast transition none |

## 内容与数据

- 标题 placeholder：「写个标题（可选）」max 60
- 正文 placeholder：「分享此刻的想法…」max 500
- 发布门槛：正文 ≥10 字
- counter 格式：「n / 500 字 · 草稿未保存/已保存」

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| 输入 | 即时 | counter、发布 enabled | 不适用 |
| 草稿/发布/取消 | toast 1.5s | 顶区 toast 淡入 | 无 transition |

## 复现验收清单

- [ ] 390×844 含标题、正文、counter、发布、存草稿
- [ ] <10 字发布 disabled，≥10 enabled
- [ ] >450 字 counter 变 warn 色
- [ ] 六色令牌一致
- [ ] 草稿保存更新 counter 状态
