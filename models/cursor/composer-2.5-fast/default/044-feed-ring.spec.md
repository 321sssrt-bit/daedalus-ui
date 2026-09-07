# 044 社交社区产品

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`044-feed-ring.html`
- 复现范围：动态浏览、发帖编辑、可见范围、发布失败保留草稿与重试成功

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机框 | 390×844px，圆角 40px | 居中于 `#fff5f0` 背景 | border 3px `#e7e5e4` |
| 顶栏 | padding 16px | flex space-between | feed 屏固定 |
| 动态 feed | flex 1 | padding 12px 16px | overflow-y auto |
| 发帖屏 | 全屏 overlay | column：textarea + vis + actions | composeScreen |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#fff5f0` | 外背景 |
| `--surface` | `#ffffff` | 卡片、手机内 |
| `--text` | `#1c1917` | 正文 |
| `--muted` | `#78716c` | 时间戳 |
| `--accent` | `#ea580c` | FAB、选中、品牌 |
| `--accent-light` | `#ffedd5` | 头像底、可见标签 |
| `--error` | `#dc2626` | 发布失败 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 |
| --- | --- | --- | --- |
| 标题 | PingFang SC, sans-serif | 20px | 700 |
| 正文 | 同上 | 15px / 1.6 | 400 |
| 辅助 | 同上 | 11–13px | 400 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 卡片间距 | 12px | post margin-bottom |
| 控件圆角 | 12–20px | 按钮、pill |
| FAB | 44×44px 圆 | 右下角发布 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| FAB `.compose-fab` | 44px 圆 | 橙底白 + | hover 略亮 |
| 可见 pill `.vis-opt` | padding 8px 14px | 灰边白底 | selected 橙底白字 |
| 动态卡片 `.post` | 圆角 14px | 白底灰边 | — |
| 失败告警 `.alert-error` | margin 8px 16px | 红底 | 草稿保留不关闭 compose |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390×844 | 单列 feed | 标准手机框 |
| 宽屏 | 手机框居中 | 不拉伸 |

## 内容与数据

- 品牌：环圈
- 初始 feed 2 条；发布后 unshift 至顶部
- 可见范围：公开 / 仅好友 / 仅自己

## 动效与反馈

| 触发 | 时长 | 可见反馈 | reduced-motion |
| --- | --- | --- | --- |
| FAB hover | — | brightness | 禁用 transition |

## 复现验收清单

- [ ] 390 手机框与 feed 卡片结构
- [ ] FAB 打开发帖屏
- [ ] 可见范围三 pill 可切换
- [ ] 正常发布出现在 feed 顶
- [ ] 失败模拟后草稿保留、重试成功

## 产品边界

含：浏览、编辑、可见范围、发布、失败重试。不含：评论、点赞、图片、@提及。

## 状态地图

| 屏 | 元素 | 切换 |
| --- | --- | --- |
| feedScreen | feed + FAB | 默认 |
| composeScreen | textarea、vis、发布/取消 | 点 FAB |
| failMode | checkbox | 控制下次 publish |

## 正常流程

浏览 feed → 点 + → 输入内容 → 选可见范围 → 发布 → 新帖在 feed 顶部

## 异常触发与恢复

勾选「模拟发布失败」→ 点发布 → alert-error、草稿与可见范围保留 → 再点发布（不勾选）→ 成功入 feed

## 数据变化

成功：feed.unshift；失败：feed 不变，textarea/vis 保留

## 人工验收步骤

**正常**：+ → 写「测试动态」→ 仅好友 → 发布 → feed 见新帖。

**异常**：勾选模拟失败 → 发布见红告警 → 再发布 → 成功。
