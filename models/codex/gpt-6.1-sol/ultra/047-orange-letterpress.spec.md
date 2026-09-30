# 047 字场 / 一张海报的工作室

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`047-orange-letterpress.html`
- 复现范围：同一个HTML内的字场 / 一张海报的工作室正常闭环、题定异常及恢复结果。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 工作室 | 最小800px高；三列270px / 1fr / 230px | 侧栏与导出栏分别内边距28px 24px和28px 20px | 文档流，z-index:auto；纵向滚动 |
| 实时预览 | canvas固有600px×760px，显示最大高560px | 棋盘24px背景；居中；画布阴影0 8px 20px | 文档流，z-index:auto；纵向滚动 |
| 导出结果 | 230px栏，按钮上间距20px | 深底浅字；下载链接内边距14px | 文档流，z-index:auto；纵向滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#e6e2da` | 画布 |
| `--surface` | `#fffaf1` | 输入与面板 |
| `--text` | `#2d2924` | 主文字 |
| `--muted` | `#81796d` | 辅助文字 |
| `--accent` | `#f39a3f` | 主操作与焦点 |
| `--line` | `#c9c2b7` | 边界与底纹 |
| `--danger` | `#a43d28` | 错误文字 |

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

标题最长16字符、副标题28字符，日轮60–220px。真实canvas导出600×760图片；错误组合不创建Blob或下载。每次改参数隐藏旧下载结果，再次导出替换旧对象URL。
关键入口、操作与结果文案按正常流程及异常恢复保留；没有网络请求、远程图片或真实资金/订单写入。示例编号与人员均为虚构。数据状态在当前页面中保存，刷新按初始样例重置（045另保存播放快照）。

### 页面专用尺寸与覆盖规则

以下为本页实际CSS中的精确覆盖，优先于基础令牌和字体表；重建时保留这些尺寸、边界、断点及排版关系。

```css
.studio{min-height:800px;display:grid;grid-template-columns:270px 1fr 230px}.tools{padding:28px 24px;background:var(--surface);border-right:1px solid var(--line)}.tools h1{font-size:27px;font-family:SimSun,serif}.canvas-zone{padding:28px;display:grid;place-items:center;align-content:center;background-image:linear-gradient(45deg,var(--line) 25%,transparent 25%),linear-gradient(-45deg,var(--line) 25%,transparent 25%),linear-gradient(45deg,transparent 75%,var(--line) 75%),linear-gradient(-45deg,transparent 75%,var(--line) 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0}.canvas-zone canvas{max-height:560px;max-width:100%;width:auto;box-shadow:0 8px 20px #00000020}.export{padding:28px 20px;background:var(--text);color:var(--surface)}.export h2{font-size:20px}.export small{color:var(--line)}.export label{color:var(--line)}.export button{width:100%;margin-top:20px}.export a{display:block;background:var(--accent);color:var(--text);padding:14px;text-align:center;font-weight:700;margin-top:16px}.check{display:flex;align-items:center;gap:8px}.check input{width:18px;min-height:18px}.size{accent-color:var(--accent);padding:0;border:0;background:none}.caption{font:12px Consolas,monospace;color:var(--muted);padding:14px;background:var(--page)}@media(max-width:1000px){.studio{grid-template-columns:220px 1fr}.export{grid-column:1/-1}.canvas-zone canvas{max-height:420px}}@media(max-width:600px){.studio{grid-template-columns:1fr}.canvas-zone{padding:20px}.canvas-zone canvas{max-height:460px}.export{grid-column:auto}}
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

只实现题库要求的字场 / 一张海报的工作室单页演示。无登录、真实服务端、第三方支付或消息网络；明确可见的模拟入口用于题定异常验收。

## 状态地图

初始可操作状态→正常流程内核对/编辑状态→成功结果；异常入口→失败反馈（保留所述数据）→纠正/重试→成功。各状态共用同一套CSS令牌和组件。

## 正常流程

修改标题和日轮大小→看到画布即时变化→选择PNG→导出海报→出现尺寸/文件KB与可下载文件，点击获得PNG图片。

## 异常触发与恢复

保持透明背景开启→格式选JPEG→导出，指出不支持透明且无下载结果→选PNG或关闭透明→重新导出，出现成功与下载文件。

## 数据变化

标题最长16字符、副标题28字符，日轮60–220px。真实canvas导出600×760图片；错误组合不创建Blob或下载。每次改参数隐藏旧下载结果，再次导出替换旧对象URL。

## 人工验收步骤

正常：修改标题和日轮大小→看到画布即时变化→选择PNG→导出海报→出现尺寸/文件KB与可下载文件，点击获得PNG图片。

异常及恢复：保持透明背景开启→格式选JPEG→导出，指出不支持透明且无下载结果→选PNG或关闭透明→重新导出，出现成功与下载文件。
