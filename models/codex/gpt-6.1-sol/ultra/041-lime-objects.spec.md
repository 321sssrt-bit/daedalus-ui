# 041 日用 / 少一点，刚刚好

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`041-lime-objects.html`
- 复现范围：同一个HTML内的日用 / 少一点，刚刚好正常闭环、题定异常及恢复结果。

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面 | 最大1184px，内边距28px 32px | 居中；页眉底边2px | 文档流，z-index:auto；纵向滚动 |
| 商品区 | 剩余列宽；两列，间距20px | 主图高180px；选中轮廓3px | 文档流，z-index:auto；纵向滚动 |
| 结算区 | 340px，左内边距30px | 与商品区间距40px；左边框1px | 文档流，z-index:auto；纵向滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#f5f6ef` | 画布 |
| `--surface` | `#ffffff` | 输入与面板 |
| `--text` | `#20271c` | 主文字 |
| `--muted` | `#65705d` | 辅助文字 |
| `--accent` | `#cef05a` | 主操作与焦点 |
| `--line` | `#dce1d2` | 边界与底纹 |
| `--danger` | `#a53623` | 错误文字 |

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

陶杯单价128，托盘96，合计=单价×数量。任何选项变更使购物车失效，要求重新加入，避免旧价格或规格提交。失败时购物车保留，恢复改选后重新加入。库存按商品和颜色独立记录，原生颜色选择器与恢复按钮都刷新对应库存，不继承其他颜色的缺货。
关键入口、操作与结果文案按正常流程及异常恢复保留；没有网络请求、远程图片或真实资金/订单写入。示例编号与人员均为虚构。数据状态在当前页面中保存，刷新按初始样例重置（045另保存播放快照）。

### 页面专用尺寸与覆盖规则

以下为本页实际CSS中的精确覆盖，优先于基础令牌和字体表；重建时保留这些尺寸、边界、断点及排版关系。

```css
.shop{max-width:1184px;margin:auto;padding:28px 32px}.shop header{border-bottom:2px solid var(--text);padding-bottom:20px}.wordmark{font-size:25px;font-weight:900}.shop-grid{display:grid;grid-template-columns:1fr 340px;gap:40px;margin-top:40px}.goods{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}.goods button{padding:0;text-align:left;border:0;background:none}.product-art{height:180px;background:var(--line);display:grid;place-items:center;margin-bottom:14px}.product-art svg{width:150px;height:150px}.product-art.milk{background:var(--accent)}.product-art.sand{background:#e8dcc5}.selected .product-art{outline:3px solid var(--text);outline-offset:4px}.bill{border-left:1px solid var(--line);padding-left:30px}.total{font-size:36px;font-weight:800}.qty input{width:74px}.shop .primary{width:100%}.receipt{background:var(--accent);padding:28px;margin-top:24px}@media(max-width:900px){.shop-grid{grid-template-columns:1fr}.bill{border-left:0;border-top:1px solid var(--line);padding:24px 0 0}.shop{padding:20px}}
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

只实现题库要求的日用 / 少一点，刚刚好单页演示。无登录、真实服务端、第三方支付或消息网络；明确可见的模拟入口用于题定异常验收。

## 状态地图

初始可操作状态→正常流程内核对/编辑状态→成功结果；异常入口→失败反馈（保留所述数据）→纠正/重试→成功。各状态共用同一套CSS令牌和组件。

## 正常流程

点选慢饮陶杯或托盘→选择颜色与数量→加入购物车→核对合计→提交订单→下方绿色回执显示编号与金额。

## 异常触发与恢复

点击“让当前规格缺货”→加入购物车→提交订单，出现具体商品/规格和可用0件，回执不出现；点“改选有货颜色”→重新加入→提交，生成回执。

## 数据变化

陶杯单价128，托盘96，合计=单价×数量。任何选项变更使购物车失效，要求重新加入，避免旧价格或规格提交。失败时购物车保留，恢复改选后重新加入。库存按商品和颜色独立记录，原生颜色选择器与恢复按钮都刷新对应库存，不继承其他颜色的缺货。

## 人工验收步骤

正常：点选慢饮陶杯或托盘→选择颜色与数量→加入购物车→核对合计→提交订单→下方绿色回执显示编号与金额。

异常及恢复：点击“让当前规格缺货”→加入购物车→提交订单，出现具体商品/规格和可用0件，回执不出现；点“改选有货颜色”→重新加入→提交，生成回执。
