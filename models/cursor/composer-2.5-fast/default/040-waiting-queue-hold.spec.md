# 040 等候

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`040-waiting-queue-hold.html`
- 复现范围：手机排队等候页，含步骤、ETA、放到一边与取消

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机框 | 390×844，背景 `#eff6ff` | 外圈 `#93c5fd` 居中 | content column flex 1 |
| 顶部 | spinner 56px + 标题 + 状态文案 | padding 56×24×0 居中 |  spinner margin-bottom 28 |
| 步骤条 | 白卡 padding 20，3 step | 竖向 timeline 左 dot 右文案 | done/active/pending 三态 |
| ETA 卡 | gradient accent，padding 18×20 | 居中 label + 28px 时间 | margin-bottom 28 |
| 操作 | margin-top auto column gap 10 | 放到一边 primary outline；取消 ghost | padding-bottom 16 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#eff6ff` | 手机背景 |
| `--surface` | `#fff` | 步骤卡 |
| `--text` | `#1e3a5f` | 标题 |
| `--muted` | `#64748b` | 状态、取消 |
| `--accent` | `#2563eb` | ETA 渐变、done dot |
| `--border` | `#bfdbfe` | 步骤卡边框、side 钮 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题 | system-ui | 22px | 700 |
| 步骤名 | system-ui | 14px | 600 |
| ETA 时间 | system-ui | 28px | 700 |
| 按钮 | system-ui | 14–15px | 500 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 步骤卡圆角 | 16px | steps |
| ETA 圆角 | 14px | eta |
| 按钮圆角 | 12px | actions |
| spinner | 56px border 4px | 顶动画 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 放到一边 | 全宽 padding 14 | 白底 accent 字 border | 点击 disabled + 改文案 + 状态说明 |
| 取消 | 全宽透明 | muted 14px | confirm 后替换 content 为已取消 |
| 步骤 | dot 24px + 连线 | done 勾；active 蓝圈 glow；pending 灰 | 静态三阶 |
| ETA | 默认「约 2 分钟」 | 白字 gradient 底 | JS 每 5s 递减 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390×844 | 固定手机框 | actions 贴底 auto margin |
| 宽屏 | 外圈蓝居中 | 不变 |
| prefers-reduced-motion | 不适用 | spinner animation none |

## 内容与数据

- 标题：「正在处理您的申请」
- 当前步骤：身份核验（进行中）
- 步骤：提交申请 done、身份核验 active、生成凭证 pending
- ETA 起始约 2 分钟
- 按钮：「放到一边，完成后通知我」「取消申请」

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| Spinner | 1s linear infinite | 旋转 | 静止 border |
| 放到一边 | 即时 | 文案与 status 更新 | 不适用 |
| 取消 | confirm 对话框 | 整页替换 | 不适用 |
| ETA | 5s interval | 分钟倒计时 | 不适用 |

## 复现验收清单

- [ ] 390×844 含当前步骤、ETA、两操作钮
- [ ] 三步 timeline 可见 done/active/pending
- [ ] 六色令牌一致
- [ ] 放到一边可点击反馈
- [ ] reduced-motion 下 spinner 不转
