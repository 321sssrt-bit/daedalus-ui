# Daedalus 产品 UI 模型评测

这是一套所有答题模型共用职责、各自发明品味的公开产品 UI 测试。任务数量、顺序和验收字段以 `catalog/briefs.json` 为唯一真源。

## 进门

1. 读 `catalog/briefs.json`、`catalog/spec-template.md`、`catalog/quality.md`。
2. 按「身份与并行」确定本次 `<harness>/<model>/<reasoning-effort>`，只进入自己的答卷目录。
3. 对照题库检查自己的 `model.json`、HTML 和规范；已完成的题保留，只补缺项。
4. 每题先自定方案名与视觉方向，再完成页面和规范。职责守题库，品味守 `catalog/quality.md`。
5. 001–040 各交一个独立页面；041–050 各交一个单文件连续产品原型，完整实现题目的 `core_flow` 和 `exception`。
6. 更新本次 `model.json` 和运行回执，并在 `models/_index.json` 登记本次三段身份。
7. 运行 `python -m daedalus validate`。修复本次答卷导致的错误，直到验证通过或按「诚实弃权」收工。
8. 验证通过后运行 `python -m daedalus build --output dist`。用户另有吩咐时，再做那件事。

完成答卷必须同时满足：

- 题库中的每个编号都有一份 HTML 和一份规范，且对应 piece 为 `complete`
- 全部作品具有不同视觉身份，不是同一套皮肤换标题
- 041–050 各自能走通正常闭环，也能主动触发题定异常、恢复并重新成功
- 同一产品原型的全部状态使用同一个设计系统
- `model.json` 的三段身份、状态、文件和运行回执与实际答卷一致
- `validate` 通过且 `build` 成功产出展厅

## 身份与并行

答卷目录固定为：

`models/<harness>/<model>/<reasoning-effort>/`

三段分别表示运行框架、实际模型和思考档位；都用小写安全短名，空格转为 `-`，保留版本号里的点。任一项无法确认时，先问用户一次并给出推荐目录名。展示名称不能替代这三个可核对字段。

只在能够确认子 Agent 与主 Agent 使用**相同模型、相同思考档位**时并行。子 Agent 只用于加快互不重叠的题目，不能改变答卷能力来源。无法确认一致时由主 Agent 独立完成。

运行回执必须如实记录主模型、思考档位、是否使用子 Agent、子 Agent 数量及其负责范围。完成或弃权都要提交回执，并在收工说明中公开本次思考档位。

## 答卷密封

其他答卷完全不读：不打开、搜索、复制或比较其他 `models/` 子目录，也不打开综合展厅或装有其他答卷内容的生成数据。构建与验证只调用 `python -m daedalus`，由工具自行读盘。

答题时只编辑本次答卷目录和登记用的 `models/_index.json`；`catalog/` 与本文件只读，除非用户明确要求维护项目契约。登记时只处理自己的条目，保留其他条目。与别人做得相似视为独立品味一致，不据此翻看或重画。

## 每题交付

```text
models/<harness>/<model>/<reasoning-effort>/<id>-<scheme>.html
models/<harness>/<model>/<reasoning-effort>/<id>-<scheme>.spec.md
```

`<scheme>` 是本题独有的英文短名，使用小写和连字符。

HTML 是可离线运行的单文件 H5，使用中文文案、系统字体和内嵌 CSS/SVG，不加载外网图片、字体、脚本或样式，不安装答题依赖。041–050 的正常状态、异常状态和恢复结果都放在同一个 HTML 中，且通过页面上的明确操作抵达。

规范填写 `catalog/spec-template.md`。001–040 填视觉规范章节；041–050 继续填完产品原型补充章节。色号必须来自该题 HTML 的实际 CSS。

`model.json` 为本次答卷真源：分别记录 `harness`、`model`、`reasoningEffort`，记录模型级 `status`、pieces 和运行回执。完整答卷的模型级状态为 `complete`。

## 诚实弃权

如果工作量超过本次 Agent 能诚实完成的能力，可以停止继续答题。保留所有真实完成的 pieces，并在 `model.json` 中：

- 将模型级 `status` 标为 `forfeited`
- 写入公开短语 `我是鸡`
- 写明具体弃权原因
- 保留并登记运行回执

弃权是公开结果，不冒充完成；展厅必须显示“我是鸡”、原因和已完成数量。

## 交付工具

- `python -m daedalus validate`：检查题库、答卷、规范、身份与回执
- `python -m daedalus build --output dist`：验证后生成公开展厅
- `python -m daedalus starter --output dist/daedalus-clean.zip`：生成不含任何答卷与历史内容的干净测试包

只有维护项目时才生成 starter；正常答题不需要运行它。

## 用户另有吩咐

答卷未齐时先完成本次评测或诚实弃权，再处理用户的附加任务。答卷已齐时直接处理附加任务，不为“再优化”重画已通过的题。
