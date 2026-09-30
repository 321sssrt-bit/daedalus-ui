# 046 共构 / 把事情一起做完

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`046-blueprint-common.html`
- 复现范围：同一个HTML内的共构 / 把事情一起做完正常闭环、题定异常及恢复结果。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 工作区 | 最小800px高；220px侧栏与剩余主区 | 28px蓝图背景网格 | 文档流，z-index:auto；纵向滚动 |
| 主区 | 内边距32px 36px，表单列1fr/160px/auto | 间距12px；任务纵向间距12px | 文档流，z-index:auto；纵向滚动 |
| 记录区 | 内边距24px，边框1px | 活动行内边距8px 0，最新记录在前 | 文档流，z-index:auto；纵向滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#edf3fa` | 画布 |
| `--surface` | `#ffffff` | 输入与面板 |
| `--text` | `#173652` | 主文字 |
| `--muted` | `#668096` | 辅助文字 |
| `--accent` | `#266cad` | 主操作与焦点 |
| `--line` | `#cadce9` | 边界与底纹 |
| `--danger` | `#b94334` | 错误文字 |

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

初始3个任务，1完成。创建增加一条待开始，分派同步登记；状态仅待开始→进行中→已完成。受限发布没有写入，申请只记申请，不伪造已获权限。
关键入口、操作与结果文案按正常流程及异常恢复保留；没有网络请求、远程图片或真实资金/订单写入。示例编号与人员均为虚构。数据状态在当前页面中保存，刷新按初始样例重置（045另保存播放快照）。

### 页面专用尺寸与覆盖规则

以下为本页实际CSS中的精确覆盖，优先于基础令牌和字体表；重建时保留这些尺寸、边界、断点及排版关系。

```css
.workspace{min-height:800px;display:grid;grid-template-columns:220px 1fr;background:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:28px 28px}.sidebar{padding:32px 24px;background:var(--text);color:var(--surface)}.sidebar h1{font-size:28px;letter-spacing:3px}.sidebar button{width:100%;margin-top:18px;background:transparent;color:var(--surface);border-color:var(--muted);text-align:left}.sidebar small{color:var(--line)}.workbody{padding:32px 36px}.workhead{background:var(--page);padding:20px;border:1px solid var(--line)}.workbody h1{font-size:30px;letter-spacing:0}.entry{display:grid;grid-template-columns:1fr 160px auto;gap:12px;padding:20px;background:var(--surface);margin-top:24px;border:1px solid var(--line)}.tasklist{display:grid;gap:12px;margin:24px 0}.task{background:var(--surface);padding:20px;border-left:4px solid var(--accent);display:flex;justify-content:space-between;align-items:center;gap:20px}.activity{background:var(--surface);padding:24px;border:1px solid var(--line)}.activity li{padding:8px 0;border-bottom:1px dashed var(--line)}.permission{padding:24px;background:var(--surface);border:2px solid var(--danger);margin-top:24px}@media(max-width:900px){.workspace{grid-template-columns:1fr}.sidebar{padding:18px 24px}.sidebar nav{display:flex;gap:12px}.sidebar button{width:auto;margin:0}.sidebar p{display:none}.workbody{padding:20px}.entry{grid-template-columns:1fr}.task{align-items:flex-start;flex-wrap:wrap}}
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

只实现题库要求的共构 / 把事情一起做完单页演示。无登录、真实服务端、第三方支付或消息网络；明确可见的模拟入口用于题定异常验收。

## 状态地图

初始可操作状态→正常流程内核对/编辑状态→成功结果；异常入口→失败反馈（保留所述数据）→纠正/重试→成功。各状态共用同一套CSS令牌和组件。

## 正常流程

输入校对展览说明→选成员乙→创建并分派，任务出现在列表且记录创建/分派→点开始任务→点完成任务，活动记录两次状态推进，完成数增加。

## 异常触发与恢复

点侧栏受限发布主版本→出现缺少发布管理员权限，普通任务与受限状态未改→发出访问申请或安全返回→创建并推进一条普通任务，活动记录出现允许的变更。

## 数据变化

初始3个任务，1完成。创建增加一条待开始，分派同步登记；状态仅待开始→进行中→已完成。受限发布没有写入，申请只记申请，不伪造已获权限。

## 人工验收步骤

正常：输入校对展览说明→选成员乙→创建并分派，任务出现在列表且记录创建/分派→点开始任务→点完成任务，活动记录两次状态推进，完成数增加。

异常及恢复：点侧栏受限发布主版本→出现缺少发布管理员权限，普通任务与受限状态未改→发出访问申请或安全返回→创建并推进一条普通任务，活动记录出现允许的变更。

### 长内容折行

对界面允许输入的连续英文字符使用overflow-wrap:anywhere；flex文字子项min-width:0并可占剩余空间，操作按钮不缩小。007在768px输入40个W、036在390px输入标题40个W与正文80个W、037在390px输入30个W、046在768px输入60个W时（按本页对应项验收），内容换行且没有整页横向溢出或手机裁切。

```css
.task>div{min-width:0;flex:1;overflow-wrap:anywhere}.task>button{flex-shrink:0}
```

主区grid子项.workbody和活动记录容器min-width:0，活动记录li同样overflow-wrap:anywhere，防止同一个长标题在记录中撑开网格。
