# 010 看板

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`010-lane-flow.html`
- 复现范围：三列泳道看板、可拖拽/可点选卡片、新建条目模态

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 看板容器 | max-width 1280px，padding 24px 28px | 块级纵向 | 背景 `#f0f4f8` |
| 页头 | margin-bottom 24px | Flex space-between | 标题+筛选+新建按钮 |
| 三列泳道 | Grid 3×1fr，gap 20px | 每列 min-height 420px | 背景分别为 lane1/2/3 色 |
| 新建模态 | max-width 400px | fixed 居中 overlay | z-index 10 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#f0f4f8` | 页面灰蓝 |
| `--surface` | `#ffffff` | 卡片、模态 |
| `--text` | `#1e293b` | 标题 |
| `--muted` | `#64748b` | 描述、计数 |
| `--accent` | `#3b82f6` | 新建按钮、选中 outline |
| `--lane1` | `#dbeafe` | 待办列背景 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 显示字 | PingFang SC | 20px 页标题 | 700 |
| 标题 | 同上 | 14px 列头 UPPER / 卡片 h3 | 700 / 600 |
| 正文 | 同上 | 12px 卡片描述 | 400 |
| 辅助文字 | 同上 | 11px tag | 400 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 10px 卡片 gap / 20px 列 gap | |
| 控件圆角 | 8px 卡片、按钮 | |
| 容器圆角 | 12px 泳道、模态 | |
| 边框 / 阴影 | card-shadow 0 1px 3px rgba(30,41,59,.08) | |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 看板卡片 | padding 14px，draggable | 白底边框 `#cbd5e1` | hover 上浮；selected 2px accent outline；dragging 半透明 |
| 新建条目 | 高 38px | 背景 accent | hover `#2563eb`；打开模态 |
| 泳道列 | min-height 420px | 三色底 | drag-over 虚线 outline；drop 接收卡片 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 1280×800 | 三列等宽 | 标准 padding |
| 窄于 768px | 单列堆叠三泳道 | wrap padding 16px |

## 内容与数据

- 产品：泳道流 · 产品迭代看板
- 三列：待办(3)、进行中(2)、已完成(1) — 计数随拖拽/新建更新
- 卡片含标题、描述、tag
- 新建：模态填标题描述，添加到待办列

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 卡片 hover | 0.15s | translateY -1px | 关闭 |
| 拖拽 | 即时 | dragging + lane drag-over | 无 transition 依赖 |
| 新建 | 即时 | 模态 open/close | 无 |

## 复现验收清单

- [ ] 1280px 三列泳道并排，各色列背景可区分
- [ ] 卡片可 drag 到其他列，列计数自动更新
- [ ] 点击卡片出现 selected accent outline
- [ ] 「新建条目」打开模态，保存后在待办列出现新卡
- [ ] 768px 三列纵向堆叠；hex 含 `#3b82f6`、`#dbeafe`
