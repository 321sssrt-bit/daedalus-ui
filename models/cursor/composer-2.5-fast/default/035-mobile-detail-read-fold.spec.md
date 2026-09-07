# 035 内容详情

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`035-mobile-detail-read-fold.html`
- 复现范围：手机阅读详情，含字号调节、正文与收藏/开始操作

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机框 | 390×844，背景 `#faf6f0` | 宽屏外圈 `#d4c8b8` 居中 | column：header + scroll + footer |
| 顶栏 | padding 48×20×12，border-bottom | flex：返回 + 标题 | 背景 `#fff` |
| 正文区 | flex 1 scroll，padding 20px | 控制块 + article | 首字下沉 accent |
| 底栏 | padding 12×20×32，两按钮 flex | 收藏 + 开始 1:1 | 固定底，border-top |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#faf6f0` | 纸感背景 |
| `--surface` | `#fff` | 顶栏、底栏 |
| `--text` | `#2c2416` | 正文 |
| `--muted` | `#8a7d6b` | 标签 |
| `--accent` | `#c45c26` | 按钮、首字、控制高亮 |
| `--accent-light` | `#f5e6dc` | 控制块背景 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题 | Georgia, Songti SC | 18px / 1.35 | 600 |
| 正文 | Georgia, Songti SC | 15–21px 四档 / 1.85 | 400 |
| UI | system-ui | 12–15px | 400–600 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 控制块圆角 | 12px | 字号调节 |
| 按钮圆角 | 12px | 底栏 |
| 字号档 | 15,17,19,21 px | 4 档 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| A−/A+ | 36×36 方钮 | 白底 border | 点击改变 body font-size 与 label |
| 收藏 | flex 1 padding 14 | 描边 accent | saved：实心 accent 白字「♥ 已收藏」 |
| 开始阅读 | flex 1 padding 14 | 实心 accent | 点击文案变「继续阅读 · 第 1 段」 |
| 正文 | article#bodyText | 17px 默认 | 即时重排 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390×844 | 三栏式 column | 正文 scroll |
| 宽屏 | 手机框居中 | 不变 |
| prefers-reduced-motion | 不适用 | font-size transition none |

## 内容与数据

- 标题：「在慢邮时代读一封长信」
- 字号 label：标准 · 17px 等四档
- 正文三段，首字下沉
- 收藏/开始中文案见 HTML

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| 字号调节 | 0.2s | 正文 font-size + label | 无 transition |
| 收藏 | 即时 | 类 saved 切换 | 不适用 |

## 复现验收清单

- [ ] 390×844 手机框，标题+可调节字号+正文+双按钮
- [ ] A−/A+ 改变正文字号与 label
- [ ] 收藏可切换已收藏态
- [ ] 六色令牌正确
- [ ]  Serif 正文与首字下沉可见
