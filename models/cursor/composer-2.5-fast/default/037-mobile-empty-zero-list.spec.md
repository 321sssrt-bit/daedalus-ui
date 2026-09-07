# 037 列表空态

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`037-mobile-empty-zero-list.html`
- 复现范围：手机清单列表空态页，含说明、主 CTA 与底栏

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机框 | 390×844，背景 `#f3f0fa` | 外圈 `#c4b8d8` 居中 | column |
| 页头 | padding 52×20×16 | 标题 + 副统计 | border-bottom |
| 空态区 | flex 1 center | 插画 160px + 文案 + CTA 纵向居中 | padding 40×32 |
| 底栏 | 高 80px | 三 tab space-around | 清单 active |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#f3f0fa` | 手机背景 |
| `--surface` | `#fff` | 头、导航 |
| `--text` | `#3d3560` | 标题 |
| `--muted` | `#8b83a8` | 副文案 |
| `--accent` | `#7c5cbf` | CTA、active tab |
| `#c4b8d8` | `#c4b8d8` | 外圈背景、插画线 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 页标题 | system-ui | 22px | 700 |
| 空态标题 | system-ui | 18px / 1.4 | 600 |
| 说明 | system-ui | 14px / 1.65 | 400 |
| CTA | system-ui | 16px | 600 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| CTA 圆角 | 28px pill | create-btn |
| CTA padding | 16×40 | 主按钮 |
| 阴影 | 0 8px 24px rgba(124,92,191,.35) | CTA |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 去创建清单 | pill CTA | accent 底白字 shadow | hover translateY -2px；点击 disabled 1.2s 文案变化 |
| 底栏 tab | 3 项 icon 24 | muted | active accent 600；点击切换 active |
| 空态插画 | SVG 160×160 | 虚线框 + 0 徽章 | 静态 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 390×844 | 固定手机框 | 空态垂直居中 |
| 宽屏 | 外圈 lavender 居中 | 不变 |
| prefers-reduced-motion | 不适用 | CTA transition none |

## 内容与数据

- 页头：「我的清单」「共 0 项 · 按创建时间排序」
- 空态标题：「这里还是空的」
- 说明段落实 App 功能
- CTA：「去创建清单」
- 导航：清单 active、日历、发现

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| CTA 点击 | 1.2s | 文案「打开创建向导…」 | 无 hover transform |
| Tab | 即时 | active 切换 | 不适用 |

## 复现验收清单

- [ ] 390×844 手机框 + 底栏三 tab
- [ ] 空说明 + 主 CTA 可见
- [ ] 六色值在 HTML 中出现
- [ ] 清单 tab 默认 active
- [ ] CTA 可点击有反馈
