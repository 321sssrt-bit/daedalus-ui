# 050 学习知识产品

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`050-lesson-quiz.html`
- 复现范围：课程入口、练习作答、错答解释、重试、订正成功

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | max-width 1280px | grid 260px 1fr | 背景 `#f8fafc` |
| 侧栏 | 宽 260px，padding 24px 20px | 纵向课程列表 | 背景 `#1e3a5f`，白字 |
| 主内容 | 1fr，padding 32px 40px | 居中 max-width 640px | 白底 `#ffffff` 卡片 |
| 反馈区 | 全宽，margin-top 24px | 解释块 + 按钮行 | 错答/成功态切换 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#f8fafc` | 背景 |
| `--surface` | `#ffffff` | 主区 |
| `--text` | `#0f172a` | 文字 |
| `--muted` | `#64748b` | 说明 |
| `--accent` | `#1d4ed8` | 主按钮 |
| `--accent-light` | `#dbeafe` | 选项选中 |
| `--sidebar` | `#1e3a5f` | 侧栏 |
| `--error` | `#dc2626` | 错答 |
| `--success` | `#16a34a` | 正确 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 标题 | PingFang SC, Microsoft YaHei, sans-serif | 22px / 1.3 | 700 |
| 正文 | 同上 | 16px / 1.6 | 400 |
| 选项 | 同上 | 15px / 1.5 | 400 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 12–32px | 卡片 padding 32px |
| 控件圆角 | 8px | 选项、按钮 |
| 容器圆角 | 12px | 主卡片 |
| 边框 / 阴影 | `#e2e8f0`；shadow `0 4px 16px rgba(15,23,42,.06)` | 卡片 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 选项 `.opt` | padding 14px 18px | 白底灰边 | selected 蓝边+浅蓝底；wrong 红底；correct 绿底 |
| 提交按钮 | padding 12px 32px | 背景 `#1d4ed8` | disabled 未选题时 |
| 反馈块 `.feedback` | padding 16px 20px | 默认隐藏 | wrong 红底显示解释；correct 绿底 |
| 侧栏项 | padding 10px 14px | 透明 | active 半透明白底 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 1280px | 侧栏 260px + 主区 1fr | 选项全宽 |
| ≤768px | 侧栏折叠为顶栏 tabs | 主区 padding 20px |

## 内容与数据

- 课程：「HTTP 缓存机制」
- 单选题 4 选项 A–D；B 为错误答案，C/D 为正确
- 错答解释说明 Cache-Control 与 ETag 区别
- 订正成功页文案「订正成功」

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 选项选中 | 0.15s ease | 边框+背景 | 即时 |
| 反馈出现 | 0.2s ease | opacity 0→1 | 即时显示 |

## 复现验收清单

- [ ] 1280px 下侧栏 260px + 主区布局
- [ ] 九色令牌出现在 HTML
- [ ] 选 C 提交见绿色正确反馈
- [ ] 选 B 提交见红色解释 + 再次作答
- [ ] reduced-motion 下无 transition

## 产品边界

含：单选题、解释、重试。不含：视频课、积分、多题套卷。

## 状态地图

entry → quiz → (wrong→retry→quiz) | (correct→done)

## 正常流程

开始练习 → 选 C 或 D → 提交 → 正确 → 继续 → 订正成功页

## 异常触发与恢复

选 B（错误）→ 提交 → 红 feedback+解释 → 再次作答 → 选 B → 提交 → 绿成功 → done

## 数据变化

submitted 锁选项；retry 重置 selected/submitted

## 人工验收步骤

**正常**：开始 → 选 C → 提交 → 正确 → 继续 → 订正成功。

**异常**：开始 → 选 B → 错答解释 → 再次作答 → 选 B → 订正成功。
