# 045 音视频平台

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`045-play-cinema.html`
- 复现范围：内容发现、播放、进度/队列、断网暂停与重连续播

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | max-width 1280px，padding 24px 32px | 单列 | 背景 `#0d0d0d` |
| 发现网格 | 4 列 grid | gap 16px | discover 屏 |
| 播放器区 | grid 1fr + 280px | 左播放右队列 | player 屏 |
| 播放器 | aspect-ratio 16/9 | 黑底居中 | — |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#0d0d0d` | 页面背景 |
| `--surface` | `#1a1a1a` | 卡片 |
| `--text` | `#f5f5f5` | 文字 |
| `--muted` | `#737373` | 时长 |
| `--accent` | `#e11d48` | 品牌、进度条 |
| `--accent2` | `#fbbf24` | 暂停态 |
| `--success` | `#22c55e` | 播放中 |

### 字体

PingFang SC；标题 14–24px；控件 13px。

### 间距、圆角

卡片圆角 12px；按钮 padding 8px 16px。

## 组件规格与状态

| 组件 | 默认 | 状态 |
| --- | --- | --- |
| 内容卡片 | 灰渐变 thumb | hover 玫红边 |
| 进度条 | 高 6px | fill 玫红，宽度=进度比 |
| state-badge | 12px pill | playing/paused/offline 三色 |
| 模拟断网 | danger 按钮 | 触发后显示重连 |

## 响应式规则

1280 四列；≤768 两列+单列播放器。

## 内容与数据

8 条内容含 title、dur(秒)、emoji；progress 秒级；queue 数组。

## 动效与反馈

进度 fill transition 0.3s；offline 时 transition none；reduced-motion 全禁。

## 复现验收清单

- [ ] 发现 4 列网格与播放布局
- [ ] 播放/暂停/seek +30s
- [ ] 断网暂停保留进度
- [ ] 重连从原进度继续
- [ ] 队列切换内容

## 产品边界

含：发现、播放、进度、队列、断网恢复。不含：弹幕、会员、下载、多集联播。

## 状态地图

discover ↔ player；playing/offline 子状态。

## 正常流程

点内容 → 播放 → 调进度/队列 → 状态 badge 更新

## 异常触发与恢复

点「模拟网络中断」→ 暂停+offline badge+告警含当前时间 → 点「重新连接」→ 继续播放

## 数据变化

progress 递增；offline 时 timer 停；重连后 timer 恢复；不重置 progress

## 人工验收步骤

**正常**：选纪录片 → 播放 → +30s → 见进度变。

**异常**：播放中点断网 → 见暂停与进度保留 → 重连 → 继续走秒。
