# 046 团队协作产品

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`046-task-orbit.html`
- 复现范围：任务创建、分派、状态、活动日志、权限不足与申请恢复

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | max-width 1280px，padding 20px 24px | 三列 grid | 背景 `#f0f4f8` |
| 任务列表 | 宽 280px | 纵向 stack，gap 8px | 左栏固定宽，overflow-y auto |
| 主面板 | 1fr | 表单 + 状态 pill 行 | 中栏，padding 24px |
| 活动记录 | 宽 300px | 时间线列表 | 右栏，border-left |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#f0f4f8` | 背景 |
| `--surface` | `#ffffff` | 面板 |
| `--text` | `#1e293b` | 文字 |
| `--muted` | `#64748b` | 标签 |
| `--accent` | `#2563eb` | 主色 |
| `--warning` | `#d97706` | 受限 badge |
| `--error` | `#dc2626` | 权限拒绝 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题 | PingFang SC, Microsoft YaHei, sans-serif | 18px / 1.3 | 600 |
| 正文 | 同上 | 14px / 1.5 | 400 |
| 辅助文字 | 同上 | 12px / 1.4 | 400，色 `#64748b` |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 8–24px | 列表项 padding 12px |
| 控件圆角 | 8px | 按钮、pill |
| 容器圆角 | 12px | 面板 |
| 边框 / 阴影 | `#e2e8f0`；shadow `0 1px 3px rgba(15,23,42,.08)` | 卡片 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 任务项 `.task-item` | padding 12px 16px | 白底，圆角 8px | selected 蓝边；locked 带 warning badge |
| 状态 pill `.pill` | padding 6px 14px | 灰底 | active 蓝底白字；hover 浅蓝 |
| 权限告警 `.alert-error` | padding 14px 18px | 红底 `#fef2f2` | 权限不足时显示，阻止写入 |
| 申请 modal | 居中 400px 宽 | 白底圆角 12px | overlay 半透明；确认后 accessGranted |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 1280px | 三列 280px / 1fr / 300px | 标准尺寸 |
| ≤768px | 单列堆叠，活动记录移到底部 | 按钮全宽 |

## 内容与数据

- 默认任务含「Q3 财务报告」（locked）、「首页改版」等
- 状态：待办 / 进行中 / 已完成
- 分派成员：Alice、Bob、Carol
- 活动日志格式：时间 + 动作描述

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 任务选中 | 0.15s ease | 边框色变化 | 禁用 transition |
| modal 出现 | 0.2s ease | opacity 0→1 | 即时显示 |

## 复现验收清单

- [ ] 1280px 下三列布局边界为 280px / 1fr / 300px
- [ ] 六色令牌与 HTML 一致
- [ ] 新建任务、状态 pill、分派写入活动日志
- [ ] locked 任务改状态见红告警且不写入
- [ ] reduced-motion 下无 transition

## 产品边界

含：CRUD 任务、分派、状态、日志、权限。不含：甘特图、工时、评论线程。

## 状态地图

选中任务 / 新建表单 / 权限 modal；locked 任务只读直至 accessGranted。

## 正常流程

新建任务 → 选状态 pill → 分派 → 活动记录追加

## 异常触发与恢复

选「Q3 财务报告」→ 改状态/保存 → 权限不足不写 → 申请权限 → modal 确认 → 再改成功写入日志

## 数据变化

logs .unshift；locked 且无权限时 status/assignee 不变

## 人工验收步骤

**正常**：新建「测试任务」→ 进行中 → 分派 Alice → 日志有记录。

**异常**：点财务报告 → 改状态见红告警 → 申请权限 → 再改见日志。
