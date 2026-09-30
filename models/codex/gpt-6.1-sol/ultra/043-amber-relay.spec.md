# 043 回声 / 传一封短笺

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`043-amber-relay.html`
- 复现范围：同一个HTML内的回声 / 传一封短笺正常闭环、题定异常及恢复结果。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机画布 | 390px，最小844px，内边距0 | 纵向排列，不横向滚动 | 文档流，z-index:auto；纵向滚动 |
| 会话导航 | 内边距16px 24px，按钮间距8px | 横向两个会话，圆角24px | 文档流，z-index:auto；纵向滚动 |
| 对话与编辑区 | 对话内边距24px，最小高410px；编辑下内边距24px | 气泡最大宽85%，内边距14px 18px | 文档流，z-index:auto；纵向滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#fff7e9` | 画布 |
| `--surface` | `#ffffff` | 输入与面板 |
| `--text` | `#483424` | 主文字 |
| `--muted` | `#9b8069` | 辅助文字 |
| `--accent` | `#b96b32` | 主操作与焦点 |
| `--line` | `#efddc0` | 边界与底纹 |
| `--danger` | `#ad3434` | 错误文字 |

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

每个会话有独立消息数组。空内容不增加记录；失败消息只改变状态，重试原条不增加消息数量。输入内容用textContent展示，不执行用户HTML。
关键入口、操作与结果文案按正常流程及异常恢复保留；没有网络请求、远程图片或真实资金/订单写入。示例编号与人员均为虚构。数据状态在当前页面中保存，刷新按初始样例重置（045另保存播放快照）。

### 页面专用尺寸与覆盖规则

以下为本页实际CSS中的精确覆盖，优先于基础令牌和字体表；重建时保留这些尺寸、边界、断点及排版关系。

```css
.relay{padding:0}.relay header{padding:26px 24px 20px;border-bottom:2px solid var(--text)}.relay h1{font-size:30px}.threads{display:flex;gap:8px;padding:16px 24px;background:var(--line)}.threads button{border-radius:24px;padding:8px 14px}.threads button[aria-pressed=true]{background:var(--text);color:var(--page)}.conversation{padding:24px;min-height:410px}.bubble{max-width:85%;border-radius:16px 16px 16px 0;padding:14px 18px;background:var(--surface);border:1px solid var(--line);margin:14px 0}.outgoing{margin-left:auto;border-radius:16px 16px 0 16px;background:var(--line)}.stamp{color:var(--accent);font:12px/1.6 Consolas,monospace;letter-spacing:2px}.composer{padding:0 24px 24px}.composer textarea{min-height:80px}.composer button{border-radius:8px}.message-text{white-space:pre-wrap;overflow-wrap:anywhere}.fail-toggle{font-size:12px;background:none;padding:8px;min-height:44px}.relay footer{padding:16px 24px;border-top:1px dashed var(--muted);font-size:12px}
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

只实现题库要求的回声 / 传一封短笺单页演示。无登录、真实服务端、第三方支付或消息网络；明确可见的模拟入口用于题定异常验收。

## 状态地图

初始可操作状态→正常流程内核对/编辑状态→成功结果；异常入口→失败反馈（保留所述数据）→纠正/重试→成功。各状态共用同一套CSS令牌和组件。

## 正常流程

选择好友甲或书友组→输入一句话→发送→原会话增加气泡并显示已送达；切换回来消息仍保留。

## 异常触发与恢复

点击让下一条发送失败→输入短笺→发送，气泡原文保留并标发送失败→点该气泡重试发送，状态改为已送达，没有复制新气泡。

## 数据变化

每个会话有独立消息数组。空内容不增加记录；失败消息只改变状态，重试原条不增加消息数量。输入内容用textContent展示，不执行用户HTML。

## 人工验收步骤

正常：选择好友甲或书友组→输入一句话→发送→原会话增加气泡并显示已送达；切换回来消息仍保留。

异常及恢复：点击让下一条发送失败→输入短笺→发送，气泡原文保留并标发送失败→点该气泡重试发送，状态改为已送达，没有复制新气泡。
