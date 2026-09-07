# 047 创作工具产品

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`047-canvas-export.html`
- 复现范围：图层/参数编辑、实时预览、导出格式、冲突阻断与修正重导

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | max-width 1280px，padding 16px 20px | 三列 grid | 背景 `#fafafa` |
| 图层参数区 | 宽 320px | 纵向 stack | 左栏，overflow-y auto |
| 预览区 | 1fr，min-height 480px | 居中 flex | 背景 `#f5f5f4` |
| 导出面板 | 宽 280px | 格式选项 + 按钮 | 右栏固定 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#fafafa` | 背景 |
| `--surface` | `#ffffff` | 面板 |
| `--text` | `#171717` | 文字 |
| `--muted` | `#737373` | 标签 |
| `--accent` | `#84cc16` | 主按钮、选中 |
| `--error` | `#ef4444` | 导出错误 |
| `--preview-bg` | `#f5f5f4` | 预览区 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题 | PingFang SC, Microsoft YaHei, sans-serif | 16px / 1.3 | 600 |
| 正文 | 同上 | 14px / 1.5 | 400 |
| 辅助文字 | 同上 | 12px / 1.4 | 400，色 `#737373` |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 12–20px | 面板 padding 16px |
| 控件圆角 | 6px | 选项、按钮 |
| 容器圆角 | 10px | 预览框 |
| 边框 / 阴影 | `#e5e5e5` | 面板分隔 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| range slider | 全宽，高 6px | track `#e5e5e5`，thumb `#84cc16` | 拖动实时更新 preview |
| 导出选项 `.export-opt` | padding 10px 14px | 白底灰边 | selected 浅绿底 `#ecfccb` |
| 导出按钮 | padding 12px 24px | 背景 `#84cc16` | disabled 灰底；冲突时不可点 |
| 告警 `.alert-error` | padding 12px 16px | 红底 | 冲突组合时显示 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 1280px | 三列 320px / 1fr / 280px | 预览圆直径 200px |
| ≤768px | 单列堆叠 | 预览区 min-height 320px |

## 内容与数据

- 图层：背景、形状、文字
- 参数：hue 0–360、sat 0–100、scale 50–150
- 格式：PNG、JPEG、SVG；选项：透明背景、CMYK 色彩
- 冲突：JPEG+透明、SVG+CMYK

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 参数变化 | 0.1s linear | preview CSS 变量更新 | 即时 |
| 导出成功 | 0.2s ease | 结果块 fade in | 即时显示 |

## 复现验收清单

- [ ] 1280px 下三列 320px / 1fr / 280px 布局
- [ ] 六色令牌出现在 HTML
- [ ] slider 拖动 preview 圆变色/缩放
- [ ] JPEG+透明触发红告警且不导出
- [ ] reduced-motion 下无 transition

## 产品边界

含：图层列表、HSL 预览圆、格式/透明/CMYK、导出结果。不含：真实文件下载、笔刷、历史版本。

## 状态地图

编辑参数实时更新 preview；exportResult 成功块。

## 正常流程

调 hue/sat/scale → 选 PNG → 导出 → 见成功结果

## 异常触发与恢复

JPEG+透明 或 SVG+CMYK → alert 阻断 → 取消冲突项 → 再导出成功

## 数据变化

preview CSS 变；冲突时不显示 exportResult

## 人工验收步骤

**正常**：调色相 → PNG 导出 → 见文件名。

**异常**：JPEG 勾选透明 → 导出见红告警 → 取消透明 → 成功。
