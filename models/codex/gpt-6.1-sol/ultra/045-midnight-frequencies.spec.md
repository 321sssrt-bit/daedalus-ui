# 045 频率 / 给夜晚一点空间

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`045-midnight-frequencies.html`
- 复现范围：同一个HTML内的频率 / 给夜晚一点空间正常闭环、题定异常及恢复结果。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面 | 最大1180px，内边距32px | 页眉横排，底边1px | 文档流，z-index:auto；纵向滚动 |
| 播放舞台 | 剩余列宽，内边距36px，唱片区高260px | 唱片直径240px，播放按钮64px | 文档流，z-index:auto；纵向滚动 |
| 发现队列 | 300px，与舞台间距40px | 每条内边距22px 12px；选中左边3px | 文档流，z-index:auto；纵向滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#0b1526` | 画布 |
| `--surface` | `#14233a` | 输入与面板 |
| `--text` | `#f1f4fa` | 主文字 |
| `--muted` | `#94a4bc` | 辅助文字 |
| `--accent` | `#58c9d9` | 主操作与焦点 |
| `--line` | `#2a3d58` | 边界与底纹 |
| `--danger` | `#ff968a` | 错误文字 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 一级标题 | Segoe UI, Microsoft YaHei, sans-serif | 40px / 1.2；600px以下32px（页面专用覆盖见区域表及内容说明） | 700 / -1.2px |
| 区块标题 | 同上 | 22px / 1.35 | 700 / normal |
| 正文、控件 | 同上 | 14px / 1.6 | 400，主操作700 / normal |
| 辅助文字 | 同上 | 12px / 1.6 | 400 / normal |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 12px与16px | 行间距与文字段后间距 |
| 控件圆角 | 基础8px；专用覆盖按区域及组件说明 | 原生输入、次操作 |
| 容器内边距 | 基础24px；600px以下18px | 通用box容器 |
| 边框 / 焦点 | 边框1px；焦点3px，向外3px | line边界与accent轮廓 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主操作 | 最小高44px；内边距10px 18px | accent底，on字，粗体700 | hover亮度94%；focus-visible外轮廓3px；disabled透明度40%；点击结果见流程 |
| 输入或选择 | 宽100%，最小高44px；内边距10px 12px | surface底，text字，line边框1px | 原生编辑/选中；焦点accent；非法值出现中文说明且不提交 |
| 反馈与结果 | 反馈最小高26px，上间距14px；结果按区域表排列 | role=status或alert；成功显示凭证/结果文字 | 失败danger文字；隐藏结果不占空间，恢复成功显示；hover不适用 |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 | 按区域表布局，正文自然纵向滚动 | 原生输入和按钮宽度不越过容器 |
| 桌面缩至768px / 手机扩至600px以上 | 桌面专用多列按页面CSS断点折叠；手机固定最大390px居中，外层28px内边距 | 手机框圆角28px，阴影0 16px 60px；600px以下一级标题32px |

## 内容与数据

三段合成声音各120秒。切换内容从0开始；进度可拖到0–120秒；中断停计时，重连保留位置继续。保存快照写localStorage，不可用时明确仅本页记下。自动恢复不强行自动发声。
关键入口、操作与结果文案按正常流程及异常恢复保留；没有网络请求、远程图片或真实资金/订单写入。示例编号与人员均为虚构。数据状态在当前页面中保存，刷新按初始样例重置（045另保存播放快照）。

### 页面专用尺寸与覆盖规则

以下为本页实际CSS中的精确覆盖，优先于基础令牌和字体表；重建时保留这些尺寸、边界、断点及排版关系。

```css
.radio{max-width:1180px;margin:auto;padding:32px}.radio header{padding-bottom:20px;border-bottom:1px solid var(--line)}.radio h1{font-size:48px;font-weight:300}.radio-grid{display:grid;grid-template-columns:1fr 300px;gap:40px;margin-top:36px}.stage{background:radial-gradient(ellipse at 50% 30%,#243f65,var(--page));border:1px solid var(--line);padding:36px}.orbit{height:260px;display:grid;place-items:center;position:relative}.orbit svg{width:240px;height:240px}.track-title{font-size:30px}.play{width:64px;height:64px;border-radius:50%;font-size:24px;color:var(--page)}.progress{padding:0;accent-color:var(--accent);border:0;background:transparent}.queue button{width:100%;text-align:left;border:0;border-bottom:1px solid var(--line);border-radius:0;padding:22px 12px;background:none}.queue button[aria-pressed=true]{border-left:3px solid var(--accent);background:var(--surface)}.queue strong{font-size:16px}.track-number{font:14px Consolas,monospace;color:var(--accent);margin-right:12px}.radio .actions{margin-top:18px}.radio .feedback{min-height:52px}@media(max-width:850px){.radio-grid{grid-template-columns:1fr}.radio{padding:20px}.radio h1{font-size:36px}.stage{padding:24px}.orbit{height:200px}.orbit svg{width:180px;height:180px}}
```

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | prefers-reduced-motion |
| --- | --- | --- | --- |
| 进入页面 | 0ms，无进入动画 | 内容立即出现 | 不添加连续动画 |
| 操作 | 0ms，同步更新 | 数据、选中、中文失败/成功反馈立即更新 | 禁用CSS动画及过渡，保留结果文字 |

## 复现验收清单

- [ ] 主视口区域边界与表格尺寸一致，没有横向溢出。
- [ ] 使用七个色值和系统字体，所有资源都在本文件内。
- [ ] 键盘Tab焦点有3px轮廓；按钮最小高44px。
- [ ] 按正常流程可看到最终结果且数据变化正确。
- [ ] 按异常步骤主动失败，原数据保持，再恢复并成功。
- [ ] 768px桌面或390px手机可用；减少动态模式不丢反馈。

## 产品边界

只实现题库要求的频率 / 给夜晚一点空间单页演示。无登录、真实服务端、第三方支付或消息网络；明确可见的模拟入口用于题定异常验收。

## 状态地图

初始可操作状态→正常流程内核对/编辑状态→成功结果；异常入口→失败反馈（保留所述数据）→纠正/重试→成功。各状态共用同一套CSS令牌和组件。

## 正常流程

点发现队列中的内容→点击播放，按钮变暂停且进度每秒增加→拖动进度至35秒→保存播放状态，显示曲名/0:35/播放中；刷新会恢复已保存位置并等待点击播放。

## 异常触发与恢复

播放并拖到35秒→模拟网络中断，暂停且保留0:35，继续播放按钮被拦截→重新连接，继续播放→从35秒推进，反馈连接成功。

## 数据变化

三段合成声音各120秒。切换内容从0开始；进度可拖到0–120秒；中断停计时，重连保留位置继续。保存快照写localStorage，不可用时明确仅本页记下。自动恢复不强行自动发声。

## 人工验收步骤

正常：点发现队列中的内容→点击播放，按钮变暂停且进度每秒增加→拖动进度至35秒→保存播放状态，显示曲名/0:35/播放中；刷新会恢复已保存位置并等待点击播放。

异常及恢复：播放并拖到35秒→模拟网络中断，暂停且保留0:35，继续播放按钮被拦截→重新连接，继续播放→从35秒推进，反馈连接成功。
