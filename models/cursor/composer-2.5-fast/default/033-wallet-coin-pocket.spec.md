# 033 钱包首页

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`033-wallet-coin-pocket.html`
- 复现范围：手机框内钱包首页，含余额卡、快捷入口、流水列表与底部导航

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机框 | 390×844px，圆角 44px，边框 8px `#1a1a1a` | 宽屏 body flex 居中，外背景 `#b8d4c8` | 阴影 0 32px 64px |
| 滚动区 | flex 1，padding 8×20px，底 padding 100px | 纵向：余额卡→快捷 2 列→流水列表 | overflow-y auto |
| 底部导航 | 高 80px absolute bottom | space-around 四 tab | 边框顶 `#c8e6d8`，z 高于内容 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#e8f5f0` | 手机内背景 |
| `--surface` | `#fff` | 卡片、按钮、导航 |
| `--text` | `#0d3b2e` | 主文字 |
| `--muted` | `#5a8a7a` | 辅助 |
| `--accent` | `#00a878` | 余额渐变、active tab |
| `--in` | `#2ecc71` | 入账金额 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 余额数字 | system-ui | 36px / 1.1 | 700，-0.02em |
| 标题/按钮 | system-ui | 14–15px | 500–600 |
| 流水 | system-ui | 12–15px | 400–600 |
| 导航 | system-ui | 10px | 600 active |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 卡片圆角 | 16px | 余额卡 |
| 列表圆角 | 12px | 流水容器 |
| 快捷 gap | 12px | 2 列 grid |
| notch | 120×28px | 顶部刘海 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 余额卡 | padding 24px，gradient accent→accent2 | 白字 | 不适用交互 |
| 转出/收款 | grid 1fr 1fr，padding 16px | 白底 shadow | hover translateY -1px；点击 toast |
| 流水项 | flex，icon 40px 圆 | in/out 色区分 | 不适用 |
| 底栏 tab | icon 24px + 10px  label | muted | active：`#00a878` + 600 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 390×844 | 手机框固定尺寸 | 内容区滚动 |
| 宽屏 | body 居中，外圈 `#b8d4c8` | 手机框不变 |
| prefers-reduced-motion | 不适用 | 移除 quick-btn/toast transition |

## 内容与数据

- 余额：12,846.50 元；昨日 +128；本月支出 3,420
- 流水 4 条：工资 +8500、美团 -42.80、地铁 -6、阿杰 +200
- 导航：钱包（active）、理财、账单、我的
- Toast 文案随按钮变化

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| 快捷按钮 | 0.2s | hover 阴影/位移；toast 1.5s | 无 transition |
| Tab 切换 | 即时 | active 类切换 + toast | 不适用 |

## 复现验收清单

- [ ] 390×844 手机框含 notch 与底栏
- [ ] 余额、4 条流水、转出/收款入口齐全
- [ ] 五色令牌正确
- [ ] 底栏四 tab，钱包默认 active
- [ ] 点击有 toast 反馈
