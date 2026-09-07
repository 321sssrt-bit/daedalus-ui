# 039 成功回执

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`039-success-done-ticket.html`
- 复现范围：手机成功凭证页，含票券信息、可展开明细与完成按钮

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机框 | 390×844，背景 `#ecfdf5` | 外圈 `#86efac` 居中 | scroll 区 flex 1 |
| 成功头 | 居中 check 64px + 标题 | padding-top 56px | 绿圆 check shadow |
| 票券 | dashed border 2px，padding 24 | 四行 label/value flex between | 左右半圆撕口伪元素 |
| 明细 | toggle + collapsible body | max-height 0→200px | margin-bottom 24 |
| 完成钮 | 全宽 padding 16 | 底部固定于 scroll 末 | accent 实心 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#ecfdf5` | 手机背景 |
| `--surface` | `#fff` | 票券、明细 |
| `--text` | `#064e3b` | 主文字 |
| `--muted` | `#6b9080` | 标签、明细 |
| `--accent` | `#059669` | check、编号、完成钮 |
| `--border` | `#a7f3d0` | 票券 dashed |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题 | system-ui | 24px | 700 |
| 票券值 | system-ui / Consolas | 15–16px | 600 |
| 明细 | system-ui | 13px / 1.7 | 400 |
| 完成 | system-ui | 16px | 600 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 票券圆角 | 16px | ticket |
| 完成钮圆角 | 14px | done-btn |
| check 圆 | 64px | 成功图标 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 明细 toggle | 全宽 padding 14×16 | 白底 border，chevron 下 | open：chevron 180°，body max-height 200px |
| 完成 | 全宽 | accent 白字 | 点击「已添加到「我的预约」」disabled |
| 票券行 | 4 行 | mono 编号 GH-260307-0186 | 静态 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390×844 | 固定手机框，内容可 scroll | 明细折叠默认关 |
| 宽屏 | 外圈绿居中 | 不变 |
| prefers-reduced-motion | 不适用 | details transition none |

## 内容与数据

- 标题：「挂号成功」；副：「请按时到院，凭下方编号取号」
- 编号 GH-260307-0186；时间 3月8日 09:30；内科 3 号诊台；A-042
- 明细 4 行患者/医生/地址/改期说明
- 完成按钮：「完成」

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| 展开明细 | 0.3s ease max-height | body 显示四段 | 无 transition |
| 完成 | 即时 | 文案变更 disabled | 不适用 |

## 复现验收清单

- [ ] 390×844 含成功标题、编号、时间/席位、完成钮
- [ ] 票券四字段可见
- [ ] 明细可展开/收起
- [ ] 六色令牌一致
- [ ] 完成按钮有反馈
