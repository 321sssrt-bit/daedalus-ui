# 031 发布确认

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`031-confirm-launch-check.html`
- 复现范围：桌面端单次发布确认对话框，含后果说明、勾选门禁与确认/返回操作

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | 全视口，内容区 max-width 720px 水平居中 | flex 垂直水平居中，padding 24px | 背景 `#0a1628`，无滚动 |
| 确认卡片 | 卡片 padding 32×36px，圆角 16px | 纵向堆叠：标题→副文案→后果块→元数据网格→勾选→按钮 | 背景 `#122038`，边框 `#2a4060` |
| 操作区 | 卡片底部，按钮区 flex-end | 右对齐两按钮，gap 12px；768px 以下改为 column-reverse 全宽 | 确认按钮默认 disabled |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#0a1628` | 页面背景 |
| `--surface` | `#122038` | 卡片背景 |
| `--text` | `#e8eef7` | 主文字 |
| `--muted` | `#7a8fa8` | 辅助文字 |
| `--accent` | `#f0a030` | 强调、确认按钮、后果左边框 |
| `--ok` | `#3dd68c` | 成功 toast |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题 | system-ui, PingFang SC | 22px / 1.3 | 600 |
| 正文 | system-ui, PingFang SC | 14–15px / 1.6 | 400 |
| 辅助 | system-ui | 11–12px / 1.4 | 400，元数据 uppercase 0.08em |
| 等宽 | Cascadia Code, Consolas | 12px | 400 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 卡片内边距 | 32px 36px | 主容器 |
| 区块间距 | 24–28px | 段落与表单间距 |
| 控件圆角 | 10px | 按钮、元数据块 |
| 容器圆角 | 16px | 卡片 |
| 阴影 | 0 24px 48px rgba(0,0,0,.35) | 卡片 elevation |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 确认按钮 | padding 11×22px | 背景 `#f0a030`，文字 `#1a1200` | disabled：opacity 0.35；hover 非 disabled：`#ffb84d`；点击后文案「发布中…」再「已发布」 |
| 返回按钮 | 同尺寸，透明底 | 边框 `#2a4060`，文字 `#7a8fa8` | hover：背景 `#1a2d4a`；点击后 disabled，卡片 opacity 0.6 |
| 勾选行 | checkbox 18px + label | label 含 em 高亮 prod 环境 | 未勾选时确认 disabled；勾选后确认可用 |
| 后果块 | 左 border 3px accent | 背景 `#1a2d4a` | 不适用 hover |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 1280×800 | 卡片 720px 居中 | 元数据 2 列 grid |
| ≤768px | 卡片 padding 24×20 | 元数据 1 列；按钮 column-reverse 全宽 |
| prefers-reduced-motion | 不适用 | 移除 btn/toast transition |

## 内容与数据

- 标题：「确认发布「秋季促销页 v2.3」？」
- 副文案说明不可一键撤回
- 后果句含 **prod 环境全部节点约 90 秒切换** 与 CDN 15 分钟
- 元数据：production/cn-east、#8842
- 勾选文案须含「prod 环境」
- Toast：「已提交发布任务 · 可在部署日志查看进度」

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| 确认发布 | 600ms 延迟 | toast 自底部滑入 | 无 transition |
| 勾选变化 | 即时 | 确认按钮 enabled/disabled | 不适用 |
| 返回 | 即时 | 卡片变淡、按钮文案变化 | 不适用 |

## 复现验收清单

- [ ] 1280 宽下卡片 720px 居中，三区（badge、卡片、toast）结构正确
- [ ] 五色令牌与 HTML CSS 变量一致
- [ ] 未勾选时确认按钮 disabled，勾选后可点
- [ ] 768px 以下按钮纵向全宽排列
- [ ] reduced-motion 下无 transition
