# 013 收件箱

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`013-newsroom.html`
- 复现范围：报社收件台整页；含列表筛选（全部/未读/星标/急稿）、读稿切换、全部标记已读、星标、已处理本文、红笔批注

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | body 最小高 100vh；flex 水平居中；padding 0 12px；报纸米灰 #f2f0ea | — | body 可滚动 |
| 桌台 desk | 最大宽 1380px；min-height 100vh；`grid-template-columns:380px 1fr`；背景 #e9e6dd；左右边框 1px solid #c9c6ba | 左列 inbox 380px，右列读稿区 1fr | — |
| 左列 left | 右边框 1px solid #c9c6ba；flex column | 报头 masthead → 筛选 filters → 列表 inbox（flex:1 overflow-y auto） | 列表可滚动 |
| 报头 masthead | padding 26px 26px 18px；底边框 2px solid #1c1c1a；衬线字体 | 「晨钟报。」30px 900 字距 .22em + 期号行 | 红点句号为 #c33027 |
| 读稿区 right | padding 26px 34px 46px | storybar（操作条）→ letter（书信卡） | letter 最大宽 720px 居中 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--news` | `#f2f0ea` | 页面底 |
| `--news-2` | `#e9e6dd` | 桌面底 |
| `--ink` | `#1c1c1a` | 主文字/黑 |
| `--ink-soft` | `#4d4c46` | 次要文字 |
| `--ink-mute` | `#8b8a80` | 弱化文字 |
| `--pencil` | `#c33027` | 红笔（未读点、批注） |
| `--pencil-soft` | `#f4e0db` | 批注底 |
| `--sec` | `#5b6f9e` | 灰蓝（致信方） |
| `--hour` | `#b0872e` | 琥珀（保留） |
| `--line` | `#c9c6ba` | 主要分界线 |
| `--line-soft` | `#dedbd0` | 列表分隔 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 报头 | "Songti SC",SimSun,serif | 30px / 1 | 900 / 0.22em |
| 稿件标题（h1） | "Songti SC",SimSun,serif | 23px / 1.5 | 400 / 正常 |
| 正文 body | "Songti SC",SimSun,serif | 14px / 2.1 | 400 / 正常 |
| 列表字段 | "Microsoft YaHei","PingFang SC",sans-serif | 10.5–13px / 1.4–1.7 | 400–700 / 正常 |
| 批注 | 系统 sans | 12px / 1.9 | 400 / 正常 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 4–34px | 列表内距、读稿内距 |
| 控件圆角 | 4px、99px（筛选胶囊） | 按钮、胶囊 |
| 容器圆角 | 0（纸感直角） | desk/letter |
| 边框/阴影 | 1px solid #c9c6ba；letter 0 2px 0 rgba(0,0,0,.05)；批注 1px dashed #c33027 | 层级 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 列表项 item | grid 26px 1fr auto；padding 14px 12px；底边框 1px solid #dedbd0 | 背景透；未读（.unread）·姓名前 7px 红点；星标☆默认 #8b8a80 | 悬停 #fffdf6；当前 `.on`：左 3px 黑边 + #fffdf6；点击切换读稿；星标按钮点击 flip ★ 并红笔色 |
| 筛选胶囊 | padding 6px 13px；11.5px；圆角 99px | 边框 1px solid #c9c6ba；文字 #4d4c46 | `.on`：背景 #1c1c1a 米字；点击按条件过滤（unread/star/urgent） |
| 操作条按钮 | padding 7px 14px；11.5px；圆角 4px | 背景 #fffdf6；边框 1px solid #c9c6ba | 悬停黑边黑字；「全部标记已读」checkbox：accent #1c1c1a，勾选全部置已读并重渲染 |
| 稿件卡 letter | padding 30px 34px 26px；max-width 720px | 背景 #fffdf6；边框 1px solid #c9c6ba | 「已处理本文」点击：卡 opacity .4 300ms 后恢复并刷新未读状态 |
| 红笔批注 annotate | padding 12px 14px；虚线红框 | 背景 #f4e0db；文字 #c33027 | 静态 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 1280×800 | 380px + 1fr 双栏 | 全量可见 |
| ≤960px | 单列（列表在上，读稿在下）；left 底边框；inbox overflow visible；right padding 22px 18px 36px | 无隐藏 |

## 内容与数据

- 报头：晨钟报。晨间编辑部；第 12807 期；2026-09-04 · 星期五；读者来信 147 封
- 5 条来信（编码 101–105、时间、未读/星标/急稿标志各不同）：
  1. 市政厅新闻办「秋风夜市围栏施工通告」09:12 未读·急稿
  2. 记者·陈砚「菜价观察：豆角一周涨 3 成」08:47 未读
  3. 校对·周妈「二版两处错别字」08:15 已读·星标
  4. 读者·方爷爷「建议：多登一点老手艺栏目」07:58 已读
  5. 线人·老于「北市场 3 号库房夜里卸货」06:40 已读·急稿
- 每条正文含「致信」「时间」「批注」，批注均为主编红笔口气
- 读稿区下方归档行：归档编目：{编码}·晨间；预计见报：明日一版

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 列表项悬停 | .15s | 背景提亮 | 过渡关闭 |
| 已处理本文 | 300ms opacity | 稿件卡变淡再恢复 | 保留 |

## 复现验收清单

- [ ] 主视口：1380px 双栏报纸台，左列表右稿件，报头「晨钟报」衬线大字
- [ ] 令牌 #f2f0ea/#1c1c1a/#c33027/#5b6f9e/#c9c6ba 实际出现
- [ ] 未读项带红点；筛选「未读/星标/急稿」各显示对应子集；点条目切换右侧稿件
- [ ] 星标按钮将当前条目标 ★ 并变红笔色；「全部标记已读」后所有红点消失
- [ ] ≤960px 单列；reduced-motion 无过渡动画
