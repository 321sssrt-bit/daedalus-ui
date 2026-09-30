# 050 页边 / 看懂一个小概念

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`050-margin-school.html`
- 复现范围：同一个HTML内的页边 / 看懂一个小概念正常闭环、题定异常及恢复结果。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 学习画布 | 最大1160px，内边距36px；240px目录/剩余正文，间距60px | 最小高800px，纸色背景 | 文档流，z-index:auto；纵向滚动 |
| 目录 | 右内边距30px，右边框1px | 目录标题34px宋体；课程按钮内边距18px 0 | 文档流，z-index:auto；纵向滚动 |
| 练习正文 | 内边距30px 0；上边3px | 主标题42px宋体；数字66px见方；答案三列间距16px | 文档流，z-index:auto；纵向滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#f2f0eb` | 画布 |
| `--surface` | `#ffffff` | 输入与面板 |
| `--text` | `#222222` | 主文字 |
| `--muted` | `#858077` | 辅助文字 |
| `--accent` | `#343434` | 主操作与焦点 |
| `--line` | `#d8d4ca` | 边界与底纹 |
| `--danger` | `#a23b2a` | 错误文字 |

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

课程入口进度0%，进入练习50%，答对100%。错误保留题干并显示解释，只有正确答案3可完成。wrong标记决定最终“订正成功”文案，其余两课清楚标示未开放。
关键入口、操作与结果文案按正常流程及异常恢复保留；没有网络请求、远程图片或真实资金/订单写入。示例编号与人员均为虚构。数据状态在当前页面中保存，刷新按初始样例重置（045另保存播放快照）。

### 页面专用尺寸与覆盖规则

以下为本页实际CSS中的精确覆盖，优先于基础令牌和字体表；重建时保留这些尺寸、边界、断点及排版关系。

```css
.school{max-width:1160px;margin:auto;padding:36px;display:grid;grid-template-columns:240px 1fr;gap:60px;min-height:800px}.syllabus{border-right:1px solid var(--line);padding-right:30px}.syllabus h1{font:700 34px/1.2 SimSun,serif;letter-spacing:4px;margin-bottom:36px}.syllabus button{width:100%;text-align:left;padding:18px 0;border:0;border-bottom:1px solid var(--line);border-radius:0;background:none}.syllabus button:disabled{opacity:.55}.book{padding:30px 0}.book h1{font:700 42px/1.5 SimSun,serif;letter-spacing:0;max-width:500px}.book p{max-width:580px;line-height:2}.chapter-number{font:72px/1 Georgia,serif;color:var(--line);margin-bottom:30px}.book .primary{border-radius:0;min-width:160px}.question{border-top:3px solid var(--text);padding-top:28px}.numbers{display:flex;gap:12px;margin:28px 0}.numbers span{display:grid;place-items:center;width:66px;height:66px;border-bottom:1px solid var(--text);font:32px Georgia,serif}.choices{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:26px 0}.choices button{font:28px Georgia,serif;border-radius:0;min-height:64px}.choices button[aria-pressed=true]{background:var(--text);color:var(--surface)}.explanation{padding:24px 0;border-bottom:1px solid var(--line);max-width:580px}.result{border-top:3px solid var(--text);padding-top:32px}.result .seal{border:1px solid var(--text);display:inline-block;padding:12px;font-family:SimSun,serif;margin-bottom:30px}@media(max-width:800px){.school{grid-template-columns:1fr;gap:16px;padding:24px}.syllabus{border-right:0;border-bottom:1px solid var(--line);padding:0 0 20px}.syllabus nav{display:flex;gap:16px}.syllabus button{font-size:12px}.syllabus h1{margin-bottom:12px}.book{padding:10px 0}.book h1{font-size:32px}.numbers{gap:8px}.numbers span{width:52px}}
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

只实现题库要求的页边 / 看懂一个小概念单页演示。无登录、真实服务端、第三方支付或消息网络；明确可见的模拟入口用于题定异常验收。

## 状态地图

初始可操作状态→正常流程内核对/编辑状态→成功结果；异常入口→失败反馈（保留所述数据）→纠正/重试→成功。各状态共用同一套CSS令牌和组件。

## 正常流程

课程入口→进入课程→选择3→提交答案→显示练习完成和解释，本课进度100%。

## 异常触发与恢复

进入课程→选择8或30→提交，显示错误状态与可用于订正的解释→返回题目再次作答，清除选中且提交禁用→选3→提交，显示订正成功和进度100%。

## 数据变化

课程入口进度0%，进入练习50%，答对100%。错误保留题干并显示解释，只有正确答案3可完成。wrong标记决定最终“订正成功”文案，其余两课清楚标示未开放。

## 人工验收步骤

正常：课程入口→进入课程→选择3→提交答案→显示练习完成和解释，本课进度100%。

异常及恢复：进入课程→选择8或30→提交，显示错误状态与可用于订正的解释→返回题目再次作答，清除选中且提交禁用→选3→提交，显示订正成功和进度100%。
