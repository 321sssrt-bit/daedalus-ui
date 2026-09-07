# 023 收藏夹

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`023-pin-chest.html`
- 复现范围：分类 Tab 切换、七条收藏卡片、单条移除与计数更新

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | 1280×800，圆角 16px 白面板 | flex 列 | 外背景 `#eef2ff` |
| 页头 | padding 28×36px | 标题左、计数 badge 右 | 固定 |
| Tab 栏 | padding 20×36px 0，底边线 | 水平 flex gap 8px | 与内容区分隔 |
| 内容网格 | flex:1，padding 24×36px，3 列 grid | gap 16px | `overflow-y: auto` |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#eef2ff` | 外背景 |
| `--surface` | `#ffffff` | 面板 |
| `--text` | `#1e1b4b` | 标题 |
| `--muted` | `#6366a0` | 描述、副标题 |
| `--accent` | `#6366f1` | Tab 选中、badge |
| `--danger` | `#ef4444` | 删除 hover |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 显示字 | system-ui, sans-serif | 26px / 1.2 | 700 |
| 标题 | system-ui, sans-serif | 15px / 1.35 | 600 |
| 正文 | system-ui, sans-serif | 13px / 1.45 | 400 |
| 辅助文字 | system-ui, sans-serif | 11–14px | 500–600 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 8–36px | 卡片 padding 18px |
| 控件圆角 | 6–12px | pin、tab |
| 容器圆角 | 16px | 主 frame |
| 边框 / 阴影 | 1px `#e0e7ff`；shadow `0 8px 32px rgba(99,102,241,.12)` | |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| Tab `.tab` | padding 10×18px | 灰字透明底 | active `#f5f3ff` 底 + 2px 底边 `#6366f1`；hover 浅紫底 |
| 收藏 Pin | 相对定位，右上角 × 按钮 28px | `#fafaff` 底 | hover 阴影；删除后从数组移除并重渲染 |
| 计数 Badge | padding 6×14px 胶囊 | `#e0e7ff` 底 accent 字 | 随 items.length 更新 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280px | 3 列 grid | 四 Tab：全部/阅读/设计/工具 |
| ≤768px | 2 列 grid | Tab 可横向滚动（默认 flex） |

## 内容与数据

- 标题「我的收藏夹」；副标题「稍后阅读、灵感与工具」
- 初始 7 条，分类 read/design/tool
- 切换 Tab 过滤；空分类显示「该分类暂无收藏」
- 点击 × 移除对应项，badge 显示「N 项」

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| Pin hover | 0.15s | 阴影与边框 | 压缩 |
| 删除 | 即时 | 卡片消失、计数减一 | 无动画 |

## 复现验收清单

- [ ] 四个分类 Tab 可切换并过滤列表
- [ ] 至少六条收藏（实际七条）含类型、标题、描述
- [ ] 点击 × 可删除一条，总数 badge 同步
- [ ] 1280 三列网格，768 两列
- [ ] accent `#6366f1` 用于选中 Tab 与 badge
