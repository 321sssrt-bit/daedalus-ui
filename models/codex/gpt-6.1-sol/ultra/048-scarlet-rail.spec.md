# 048 山海线 / 去远一点的地方

## 规范元数据

- 规范版本：2
- 主视口：390 × 844 px
- 对应页面：`048-scarlet-rail.html`
- 复现范围：同一个HTML内的山海线 / 去远一点的地方正常闭环、题定异常及恢复结果。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 手机画布 | 390px，内边距28px 24px | 纸色背景，报头底边2px | 文档流，z-index:auto；纵向滚动 |
| 路线搜索 | 出发/箭头/抵达三列1fr/28px/1fr，间距8px | 主标题34px宋体，竖向路线表单 | 文档流，z-index:auto；纵向滚动 |
| 座位与票据 | 座位两列间距10px；票据内边距24px | 顶部红边8px，虚线2px，票据标题30px | 文档流，z-index:auto；纵向滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#faf5e9` | 画布 |
| `--surface` | `#ffffff` | 输入与面板 |
| `--text` | `#312d26` | 主文字 |
| `--muted` | `#8b8171` | 辅助文字 |
| `--accent` | `#b9392f` | 主操作与焦点 |
| `--line` | `#e5dbca` | 边界与底纹 |
| `--danger` | `#9f3127` | 错误文字 |

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

两个班次票价都86。成功凭证包含查询时的路线日期快照，班次与座位按当前选择；售罄不生成凭证，不改变路线日期。重新搜索刷新查询快照并隐藏旧回执。
关键入口、操作与结果文案按正常流程及异常恢复保留；没有网络请求、远程图片或真实资金/订单写入。示例编号与人员均为虚构。数据状态在当前页面中保存，刷新按初始样例重置（045另保存播放快照）。

### 页面专用尺寸与覆盖规则

以下为本页实际CSS中的精确覆盖，优先于基础令牌和字体表；重建时保留这些尺寸、边界、断点及排版关系。

```css
.rail{padding:28px 24px}.rail h1{font-family:SimSun,serif;font-size:34px;line-height:1.45}.rail-head{padding-bottom:22px;border-bottom:2px solid var(--text)}.rail-hero{display:flex;align-items:center;justify-content:space-between;padding:26px 0}.rail-symbol{width:75px;height:90px;border:3px solid var(--accent);border-radius:40px 40px 12px 12px;display:grid;place-items:center;color:var(--accent);font-size:40px}.route{display:grid;grid-template-columns:1fr 28px 1fr;gap:8px;align-items:end}.route input,.route select{border:0;border-bottom:1px solid var(--text);border-radius:0;background:transparent;padding-left:0}.rail .primary{width:100%;border-radius:0;margin-top:18px}.rail .train{width:100%;text-align:left;background:var(--surface);margin:10px 0;padding:18px;border-radius:0}.train[aria-pressed=true]{border:2px solid var(--accent)}.seats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px}.seat[aria-pressed=true]{background:var(--accent);color:var(--surface)}.ticket{border-top:8px solid var(--accent);padding:24px;background:var(--surface);margin-top:24px}.ticket .cut{border-top:2px dashed var(--line);margin:20px -24px;padding-top:20px}.ticket h2{font-family:SimSun,serif;font-size:30px}.rail .status{font-family:Consolas,monospace;letter-spacing:2px;font-size:12px}.rail button.secondary{margin-top:12px;width:100%}
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

只实现题库要求的山海线 / 去远一点的地方单页演示。无登录、真实服务端、第三方支付或消息网络；明确可见的模拟入口用于题定异常验收。

## 状态地图

初始可操作状态→正常流程内核对/编辑状态→成功结果；异常入口→失败反馈（保留所述数据）→纠正/重试→成功。各状态共用同一套CSS令牌和组件。

## 正常流程

选择路线和日期→查询班次→选08:40或11:20→选1A→核对订单→确认预订→看到路线/日期/班次/座位/编号的行程凭证。

## 异常触发与恢复

查询→选1B触发售罄检查→核对→确认，指出1B已售罄，路线日期不丢→返回改选1A→再次核对确认，生成凭证。

## 数据变化

两个班次票价都86。成功凭证包含查询时的路线日期快照，班次与座位按当前选择；售罄不生成凭证，不改变路线日期。重新搜索刷新查询快照并隐藏旧回执。

## 人工验收步骤

正常：选择路线和日期→查询班次→选08:40或11:20→选1A→核对订单→确认预订→看到路线/日期/班次/座位/编号的行程凭证。

异常及恢复：查询→选1B触发售罄检查→核对→确认，指出1B已售罄，路线日期不丢→返回改选1A→再次核对确认，生成凭证。
