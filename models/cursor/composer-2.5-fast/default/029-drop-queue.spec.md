# 029 文件上传

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`029-drop-queue.html`
- 复现范围：拖放/选择上传区、队列至少三文件含大小状态、删除与开始处理进度

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | 1280×800 flex 列 padding 32×40px | 顶说明 +  dropzone + 队列 + 操作 | 深色 `#151b2e` |
| 拖放区 | padding 48px 虚线框 | 居中 SVG + 文案 | margin-bottom 24px |
| 文件队列 | grid 行：1fr 100px 120px 80px | flex:1 可滚动列表 | gap 10px |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#0c1222` | 外背景 |
| `--surface` | `#151b2e` | 面板 |
| `--text` | `#e2e8f0` | 主字 |
| `--muted` | `#64748b` | 大小、hint |
| `--accent` | `#38bdf8` | 拖放 hover、待处理 badge、主按钮 |
| `--success` | `#34d399` | 已完成状态 |
| `--warn` | `#fbbf24` | 处理中状态 |
| `--danger` | `#f87171` | 删除 hover |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 显示字 | system-ui, sans-serif | 20px / 1.2 | 600 |
| 标题 | system-ui, sans-serif | 13px uppercase | 600 |
| 正文 | system-ui, sans-serif | 13–15px | 500 |
| 辅助文字 | Cascadia Code, Consolas, monospace | 13px | 400（文件名区混用 sans） |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 10–48px | file-row padding 14×16px |
| 控件圆角 | 6–12px | dropzone、行、按钮 |
| 容器圆角 | 12px | frame |
| 边框 / 阴影 | 2px dashed `#1e293b`；solid `#1e293b` 行边框 | |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| Dropzone | tabindex 0，hidden file input | 虚线框 | hover/dragover accent 边 + 浅蓝底；Enter/Space 触发选择 |
| 状态 pill | 12px 胶囊 | queued 蓝底 / processing 黄底 / done 绿底 | 开始处理后逐条 600ms 流转 |
| 删除 `.btn-icon` | 32×32 | 灰边 | hover 红字红边；点击移除行 |
| 开始处理 | padding 12×24px | 天蓝底深字 | 全 done 或空队列 disabled |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 1280px | 四列 file-row grid | 初始 3 文件 |
| ≤768px | 列宽压缩 | 大小列 80px |

## 内容与数据

- 标题「批量文件上传」；格式说明 PDF/DOCX/PNG，最大 50MB
- 初始三文件：品牌手册_v3.pdf 4.2MB、门店照片_合集.zip 28.6MB、Logo_矢量稿.svg 156KB
- 状态文案：待处理 / 处理中 / 已完成
- 新增文件通过选择或拖放追加，大小自动格式化为 MB

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 处理流水线 | 600ms/文件 | 状态 queued→processing→done | 保留状态切换 |
| dragover | 0.15s | 边框与背景 | 压缩 |

## 复现验收清单

- [ ] 虚线拖放区可点击与拖放添加文件
- [ ] 初始至少两份（实际三份）文件含名称、大小、状态
- [ ] × 删除单行，计数更新
- [ ] 「开始处理」逐条变更状态至已完成
- [ ] 1280 深色终端风布局
