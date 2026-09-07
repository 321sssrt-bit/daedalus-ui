# 050 复现规范 · chalkboard（学习知识产品原型）

## 规范元数据

- 规范版本：2
- 主视口：1280 × 800 px
- 对应页面：`050-chalkboard.html`
- 复现范围：黑板教室隐喻的单文件学习产品原型，含课程入口、3 题练习、答错订正、结果与解释、再次作答与订正成功反馈的全部状态与行为。

## 画布与区域布局

| 区域 | 位置与尺寸 | 说明 |
| --- | --- | --- |
| 页面底色 | 全屏，`background: var(--wall)` 叠 68deg 白色 1.6% 细纹理 | `body` flex 水平垂直居中，`padding:44px 24px 72px` |
| 黑板外框 `.board-wrap` | `width:min(1216px,100%)`，居中 | 下缘外置粉笔槽 |
| 黑板 `.board` | `border:13px solid var(--frame)`，`border-radius:6px` | 板面 `--board` 叠 115deg/63deg 两层粉笔灰纹理；内阴影 `inset 0 0 0 2px var(--frame-deep)` + `inset 0 0 90px rgba(0,0,0,.32)` |
| 板内 `.board-in` | `padding:30px 38px 40px; min-height:700px` | 所有视图容器 |
| 顶部 `.head-row` | 品牌左、步骤条右，两端对齐 | 下方 `hr.rule` 为 `2px dashed rgba(242,239,226,.34)` |
| 步骤条 `.steps` | 3 项 `.st`，间距 22px | 「进入课程 / 完成练习 / 查看结果」 |
| 粉笔槽 `.tray` | 板底外侧 `bottom:-31px;height:20px` | 3 支粉笔（黄/粉/蓝 34×8px）+ 右侧板擦道具 56×15px，`aria-hidden` |
| 三视图 `.scr` | 同容器互斥，`.on` 显示 | course / quiz / result |
| 角注 `.corner-note` | 板内右下 `right:22px;bottom:14px` | 11.5px，`rotate(-1.2deg)` 诚实说明 |
| toast `#toast` | 板内底部居中 `bottom:34px` | 绝对定位于 `.board-in` 内 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--wall` | `#232a22` | 教室墙面底色 |
| `--board` | `#2e4a3e` | 黑板板面 |
| `--board-deep` | `#26402f` | 板面深色（备用层） |
| `--frame` | `#8a6a42` | 木框与粉笔槽 |
| `--frame-deep` | `#6e5233` | 木框深侧/内描边 |
| `--chalk` | `#f2efe2` | 主粉笔字色 |
| `--dim` | `#b9c4b2` | 次级文字 |
| `--yellow` | `#f2d97a` | 强调：主按钮、题号、得分、当前步骤 |
| `--pink` | `#f0a3b8` | 答错、演示错项标记 |
| `--pink-deep` | `#d9748f` | 答错边框与订正解释框 |
| `--blue` | `#a9c9e8` | 选中态、演示提示、解释文字 |
| `--green` | `#b6dc9c` | 订正成功、已订正角标 |

### 字体

- 字体栈：`-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif`（系统字体，无外部字体）。
- 基准 `15px/1.7`；h1 27px/800；h2 23px/800（结果页 26px/800）；题文 16.5px/700；选项 14.5px；订正解释 13.5px；题号 `.q-no` 14px/800 黄色；得分 `.score` 52px/900 黄色。
- 粉笔字效果 `.chalk`：`letter-spacing:.04em` + `text-shadow:0 0 2px rgba(242,239,226,.24),0 1px 0 rgba(0,0,0,.22)`。

### 间距圆角层级

- 圆角两档：方形组件 4px；胶囊（徽标、toast、chip）999px；黑板 6px。
- 题目卡 `.q` 间距 `margin-bottom:18px`，内边距 `18px 22px 16px`；选项网格 `gap:10px`；知识点网格 `gap:18px`。
- 边框档位：`.btn` 2px dashed；`.course-card` 2px solid 50% 透明 chalk；`.q`/`.res-item` 1.5px solid 36% 透明 chalk；`.kp`/`.opt`/`.why`/`.demo-note` 1.5px dashed。

## 组件规格与状态

| 组件 | 常态 | 状态变化 |
| --- | --- | --- |
| `.btn` | 2px dashed `--chalk`、4px 圆角、16px/700 | hover：背景白 7% + 边框转 solid；active：`translateY(2px)`；disabled：`opacity:.38`；变体 `.ylw` 黄 / `.pk` 粉 / `.sm` 小号 |
| 步骤 `.st` | 13px `--dim`，前置 9px 虚线空心圆 | `.done`：chalk 实心实线圆；`.now`：黄字 + 黄实心圆 + 8px 黄色光晕 |
| 知识点卡 `.kp` | 1.5px dashed 40% chalk，`--dim` 释义 | 序号 `.no` 22px/800 黄色 |
| 选项 `.opt` | 1.5px dashed 45% chalk，左对齐，`A./B./C./D.` 前缀 | hover：背景白 6%；`.sel`：2px solid `--blue` + `rgba(169,201,232,.12)` 底 + `● ` 前缀；`.demo-tag`：右侧粉色胶囊「✗ 演示错项」 |
| 题目卡 `.q` | 1.5px solid 36% chalk | `.wrong`：边框 `--pink-deep` + 右上 30px/900 粉 ✗（`rotate(8deg)`、6px 粉光晕）；`.fixed-ok`：右上 28px 绿 ✓；`.before`：题旁粉色小胶囊「曾答错 ✗」 |
| 订正解释 `.why` | — | 1.5px dashed `--pink-deep`、底色粉 8%，13.5px，`<b>` 粉色引导词 |
| 核对按钮 `#btnCheck` | 黄色「核对答案」，未答完 disabled | 答错后变粉色「返回题目，再次作答」并解禁；提示行 `.quiz-hint.bad` 粉色 |
| 得分 `.score` | 52px/900 黄色 `3<small>/3 全对</small>` | `small` 18px `--dim` |
| 订正横幅 `.fixbox` | 2px solid `--green`、绿底 8% | `.erasing` 触发板擦 `@keyframes swipe`；`.done` 时 `.xmark`→opacity 0、`.tickmark`→opacity 1；一次全对走黄色 inline 变体 |
| 结果条目 `.res-item` | 1.5px solid 36% chalk 卡 | `.ra` 绿色作答行 + `.chip-fix` 黄胶囊「首答 ✗ → 订正 ✓」；`.re` 蓝色解释行 |
| toast `#toast` | 墨底胶囊 `rgba(18,28,22,.94)` + 1px dashed chalk，`opacity:0` 下移 14px | `.on`：opacity 1 归位（.25s）；`.bad`：粉边粉字；2.4s 自动消失 |

## 响应式规则

- 仅一条布局断点 `@media (max-width:900px)`：`.kp-list` 与 `.opts` 收为单列，`.board-in` padding 收窄为 `22px 20px 32px`。
- 另一条 `@media (prefers-reduced-motion:reduce)`：全局关闭过渡与动画（`*{transition:none!important;animation:none!important}`）。

## 内容与数据

QUIZ 固定 3 题（充分条件主题，每题恰含 1 个 `demo:true` 演示错项）：

- Q1「下雨→地湿」：答案 A 充分条件；why：正推成立、逆推不成立（洒水车反例）。
- Q2「x>5 是 x>2」：答案 B 充分不必要条件；why：两问法，x=3 反例。
- Q3「被 6 整除 是 被 3 整除」：答案 A 充分不必要条件；why：6=2×3，9 反例。

状态对象 `S`：`view`（course/quiz/result）、`phase`（answer/checked）、`ans`（题 id→选项下标）、`wrongs`（本轮答错 id）、`wasWrong`（历史答错 id）、`fixed`（订正成功 id）、`everWrong`（是否曾答错）。渲染全部由 `renderQuiz()`/`renderResult()` 按 `S` 重建。

## 动效与反馈

| 触发 | 效果 |
| --- | --- |
| 选选项 | `.opt` 背景/边框 .15s 过渡，选中加 ● 与蓝底 |
| 答错提交 | 题目卡转粉边、右上 ✗ 弹出、`.why` 解释块展开、按钮变粉、粉色 toast 列出错题号 |
| 全对提交（曾答错） | 结果页板擦 `swipe` 1s 横扫（0%→100% 从左出至右出，12%/88% 透明度平台），随后 ✗→✓ 交叉淡换（.35s/.3s），横幅进入 `.done` 终态 |
| 全对提交（首答全对） | 黄色「一次全对」变体横幅，无板擦动画 |
| 按钮按下 | `translateY(2px)` 下沉 |
| toast | 淡入上移 .25s，2.4s 后淡出 |
| `prefers-reduced-motion: reduce` | 全局过渡与动画关闭；JS 内 `matchMedia` 命中时板擦动画直接落 `.done` 终态，不播横扫 |

## 复现验收清单

- [ ] 1280×800 下黑板居中，木框 13px、粉笔槽与三支粉笔可见
- [ ] 顶部步骤条 3 项随视图切换正确呈现 done/now 态
- [ ] 课程视图含课程卡（第 3 讲徽标、标题、meta、3 知识点格、开始按钮、诚实说明）
- [ ] 练习视图顶部有蓝色虚线演示提示条，每题恰含 1 个粉色「✗ 演示错项」
- [ ] 未答完 3 题时「核对答案」禁用，提示「还差 N 题未作答」
- [ ] 选演示错项提交后：错题卡粉边 + 右上 ✗ + 订正解释 + 粉色按钮与 toast
- [ ] 返回后错题清空答案、保留「曾答错 ✗」签与绿 ✓ 角标，改对后可重新提交
- [ ] 订正全对后结果页出现绿色订正横幅（板擦横扫 → ✗ 换 ✓）与逐题「首答 ✗ → 订正 ✓」
- [ ] 「从头再来一次」完整重置 `S` 并回到课程视图，toast 确认
- [ ] 开启系统减弱动效后无过渡/动画，横幅直接呈现已订正终态
- [ ] 页面不含 `data:` URI、`http:` 外链与外部字体

---

以下章节仅 041–050 必填；001–040 到此结束。

## 产品边界

- 单页学习原型：课程浏览 → 练习作答 → 判分与解释 → 订正重交 → 结果复盘，全部在同一个 HTML 内完成。
- 不做账号、进度存储、题库服务；数据为页内固定 3 题，成绩即时计算并有诚实标注。
- 答错不是死路：系统永远允许返回改选并重新提交，直到正确。

## 状态地图

| 状态 | 进入条件 | 可执行操作 |
| --- | --- | --- |
| course | 初始 / 再来一次 | 点「开始练习」 |
| quiz·answer | 进入练习 / 答错后返回 | 选择各题选项（单选可换）、答完点「核对答案」 |
| quiz·checked（有错题） | 提交且存在错题 | 查看 ✗ 与订正解释，点「返回题目，再次作答」 |
| result·首答全对 | 从未答错且全对 | 查看逐题解释，点「从头再来一次」 |
| result·订正全对 | 曾答错且本轮全对 | 查看订正横幅与首答/订正记录，点「从头再来一次」 |

## 正常流程

1. 课程视图点「开始练习 →」→ 步骤 1 转 done、视图切到练习。
2. 三题各选正确答案 → 「核对答案」解禁，提示变「3 题已答完，可以核对答案」。
3. 提交 → 步骤 2 done、视图切结果，黄字「3/3 全对」+ 黄色一次全对横幅 + 逐题解释，toast「3 题全对，课堂过关」。

## 异常触发与恢复

- 异常名：练习答案错误。触发：选择页面上明示的粉色「✗ 演示错项」（或任何错误选项）并提交。
- 反馈：错题卡粉边 + 右上大粉 ✗ + 粉笔「订正解释」块 + 粉色 toast 点名错题；按钮变「返回题目，再次作答」。
- 恢复：点返回 → 仅清空错题答案、保留正确选择与「曾答错 ✗」记录，题目挂绿 ✓ 角标；按解释改对后重新提交 → 结果页绿色「订正成功」横幅播板擦擦除 ✗ 改判 ✓，逐题卡显示「首答 ✗ → 订正 ✓」，完成恢复闭环。

## 数据变化

- `S.ans` 随选择写入/清空；`doCheck()` 重算 `S.wrongs`；答错的题并入 `S.wasWrong` 并置 `S.everWrong=true`。
- `backToQuiz()` 删除错题的 `S.ans` 项、清空 `S.wrongs`，`wasWrong` 保留（故显示「曾答错 ✗」与绿 ✓）。
- 全对提交时 `S.fixed = S.wasWrong.slice()`，结果页据此渲染订正横幅与 `.chip-fix`。
- 「从头再来一次」将 `S` 七个字段全部复位并回到 course。

## 人工验收步骤

正常闭环：

1. 打开页面，确认课程视图与步骤条初始态。
2. 点「开始练习」，三题全选正确答案，提交。
3. 确认结果页「3/3」+ 一次全对黄色横幅 + 逐题解释，无订正横幅。

异常恢复：

1. 「从头再来一次」回到课程，重新进入练习。
2. Q1–Q3 各选「✗ 演示错项」，点「核对答案」。
3. 确认粉 ✗、订正解释、粉色按钮与 toast；点「返回题目，再次作答」。
4. 确认错题答案被清空且带「曾答错 ✗」签，按解释改选正确答案，重新提交。
5. 确认结果页绿框订正横幅播板擦横扫并定格 ✗→✓，逐题卡带「首答 ✗ → 订正 ✓」，全部为最终正确作答。
