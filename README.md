<p align="center">
  <img src="docs/assets/daedalus-cover.svg" alt="Daedalus — Open Product UI Design Evaluation for AI Models" width="100%">
</p>

<p align="center">
  <strong>规则相同，品味各异。 / Same rules. Different taste.</strong><br>
  40 个独立页面 · 10 个连续产品原型 · 50 份可复现规范<br>
  40 independent pages · 10 end-to-end product prototypes · 50 reproducible specifications
</p>

<p align="center">
  <a href="#chinese">中文</a>
  · <a href="#english">English</a>
  · <a href="https://321sssrt-bit.github.io/daedalus-ui/"><strong>在线展厅 / Live Gallery</strong></a>
  · <a href="catalog/briefs.json">题库 / Briefs</a>
  · <a href="AGENTS.md">规则 / Rules</a>
  · <a href="LICENSE">MIT License</a>
</p>

---

<a id="chinese"></a>

## Daedalus 是什么

Daedalus 是一套面向 UI Agent 与模型的公开产品设计评测，也是一座可浏览的设计灵感展厅。所有参评者承担相同职责，但品牌、布局、视觉语言与具体文案都由自己决定。

项目最初受到 [Hall of One Hundred](https://miaai-lab.github.io/GLM-5.3-100-HTML-Files/) 启发；Daedalus 在独立页面之外加入可操作的连续产品原型，用来观察模型能否把界面品味延伸成一致的产品逻辑。

> 这里展示作品与证据，不制作模型排行榜。自动检查通过不等于设计优秀，也不等于用户已经验收。

## 为什么这里更偏向前端

Daedalus 有意把重点放在前端产品能力：模型能否组织信息、建立视觉语言、设计交互，并让正常流程、异常反馈与恢复操作保持一致。它不试图用同一套题目概括模型的全部软件工程能力。

对于更偏后端和系统实现的能力，本项目更倾向另设一套**国际象棋测试**。国际象棋天然要求实现彼此约束的规则框架：棋盘与局面状态、合法走子、轮次与历史、将军与胜负判断，以及王车易位、吃过路兵、升变等特殊规则。它比产品页面更适合观察模型能否把复杂规则准确地组织成可以持续验证的程序。

两条测试线互相补充，但不混成一个总分：Daedalus 观察前端产品设计与交互表达；国际象棋测试观察规则系统、状态管理和工程实现。

## 40 + 10

| 题组 | 内容 | 观察重点 |
| --- | --- | --- |
| `001–040` | 登录、编辑器、仪表盘、结账、错误页等独立页面 | 视觉广度、信息组织、页面职责 |
| `041–050` | 购物、支付、聊天、社交、媒体、协作、创作、旅行、健康、学习 | 核心操作闭环、结果状态、异常恢复 |

每份答卷以 `harness / model / reasoning effort` 三段身份登记。开始或重做答卷前，参评 Agent 必须先把预计的三段身份展示给用户并取得明确确认，避免平台转发或穿透造成错误报名。子 Agent 只能用于并行提速，并且必须与主 Agent 使用相同模型和思考档位。无法诚实完成 50 题的参评者可以保留已完成部分并公开弃权；展厅会明确显示“我是鸡”和弃权原因。

## 当前公开答卷

下表依据 [`models/_index.json`](models/_index.json) 的公开登记和各答卷 `model.json` 的状态维护；展厅构建仍以这些机器可读文件为准。

| Harness | Model | 思考档位 | 完成度 | 状态 |
| --- | --- | --- | --- | --- |
| Codex | GPT-5.6 Sol | `xhigh` | 50 / 50 | Complete |
| DeepSeek Harness | deepseek-v4-pro | `max` | 50 / 50 | Complete |
| Kimi Code | K3 | `max` | 50 / 50 | Complete |
| Grok Build | Grok 4.6 | `xhigh` | 50 / 50 | Complete |

## 怎样理解结果

- **自动合规**：检查题量、文件、规范章节、身份声明、路径安全、自包含资源与构建结果等可重复验证的事实。
- **人工体验验收**：实际操作 10 个产品原型，确认正常流程和异常恢复可用，并判断产品体验与视觉质量。
- **用户验收**：由浏览者决定哪些方案真正有启发、值得收藏或继续发展。

三层证据彼此独立，前一层不能冒充后一层。Daedalus 不提供总分、“最强模型”或跨任务能力结论。

## 浏览展厅

发布完成后，直接访问 **[Daedalus 在线展厅](https://321sssrt-bit.github.io/daedalus-ui/)**。

本地构建只依赖 Python 标准库：

```bash
python -m daedalus validate
python -m daedalus build --output dist
python -m http.server 8765 --directory dist/site
```

然后访问 `http://127.0.0.1:8765/`。使用本地网址预览可以避免浏览器无法读取映射盘 `file://` 地址的问题；关闭命令窗口即可停止预览。

展厅会显示完整答卷身份、完成或弃权状态，并允许按题目浏览。每题的“查看规范”是可量测、可验收的复现合同；设计意图和辅助提示词放在单独入口，不混入一键导出的正式规范。个人收藏只保存在当前浏览器，不会上传。

## 给新参评者的干净测试包

```bash
python -m daedalus starter --output dist/daedalus-clean.zip
```

压缩包只包含规则、题库、模板和必要工具，不包含历史答案、生成展厅、本地归档或运行会话声明。参评 Agent 应在无法访问公开答案的独立环境中使用它，完成后再由维护者导入公开仓库。

## 仓库结构

| 路径 | 内容 |
| --- | --- |
| `catalog/` | 50 道统一题目、质量要求、复现规范与设计意图模板 |
| `models/` | 按 `harness / model / reasoning effort` 隔离的当前规则答卷 |
| `daedalus/` | `validate / build / starter` 生命周期入口 |
| `gallery/` | 旧打包命令的兼容入口与答卷密封钩子 |
| `docs/adr/` | 已确认的产品与工程决策 |
| `docs/specs/` | 当前实现规格 |

旧规则答卷只保存在维护者的 Git 外本地归档中，不属于公开仓库。当前由维护者整理公开答卷，暂不接收社区答卷 Pull Request；任何人仍可依据 MIT 许可证 fork 并独立使用。

## 发布方式

`.github/workflows/pages.yml` 会依次验证仓库、构建展厅、生成干净测试包并发布 GitHub Pages。生成文件只存在于 Actions 产物与 Pages 中，不写回源码历史。

仓库所有者首次发布时，在 GitHub 的 **Settings → Pages → Build and deployment** 选择 **GitHub Actions**；之后推送到 `main` 即会自动更新展厅。

---

<a id="english"></a>

## English

### What is Daedalus?

Daedalus is an open product-design evaluation for UI agents and models, as well as a browsable gallery of design ideas. Every participant receives the same responsibilities, while choosing its own brand, layout, visual language, and copy.

The project was initially inspired by [Hall of One Hundred](https://miaai-lab.github.io/GLM-5.3-100-HTML-Files/). Daedalus adds operable, end-to-end product prototypes alongside independent interface pages to examine whether a model can extend visual taste into coherent product logic.

> Daedalus publishes work and evidence, not a model leaderboard. Passing automated checks does not prove design quality or user acceptance.

### Why focus on front-end product work?

Daedalus deliberately focuses on front-end product capability: organizing information, establishing a visual language, designing interactions, and keeping normal flows, failure feedback, and recovery actions coherent. It does not attempt to summarize a model's entire software-engineering capability with one set of briefs.

Back-end and systems capability is better examined separately—for example, with a chess benchmark covering board state, legal moves, turns, history, check and win conditions, castling, en passant, and promotion. The two evaluation tracks can complement each other without being collapsed into a single score.

### 40 + 10

| Briefs | Content | What it examines |
| --- | --- | --- |
| `001–040` | Independent pages such as sign-in, editor, dashboard, checkout, and error states | Visual range, information organization, and page responsibility |
| `041–050` | Shopping, payments, chat, social, media, collaboration, creation, travel, health, and learning | Core operation loops, result states, failure recovery, and retry success |

Each submission is registered under a three-part identity: `harness / model / reasoning effort`. Before starting or restarting a submission, the participating agent must show the expected identity to the user and receive explicit confirmation. Sub-agents may only accelerate non-overlapping work when they use the same model and reasoning effort as the main agent.

A participant that cannot honestly complete all 50 briefs may preserve its completed work and publicly forfeit. The gallery will display `我是鸡`, the forfeit reason, and the number of completed pieces instead of presenting an incomplete submission as complete.

### Current public submission

This table follows the public registry in [`models/_index.json`](models/_index.json) and each submission's status in `model.json`. Gallery builds continue to treat those machine-readable files as the source of truth.

| Harness | Model | Reasoning effort | Completion | Status |
| --- | --- | --- | --- | --- |
| Codex | GPT-5.6 Sol | `xhigh` | 50 / 50 | Complete |
| DeepSeek Harness | deepseek-v4-pro | `max` | 50 / 50 | Complete |
| Kimi Code | K3 | `max` | 50 / 50 | Complete |
| Grok Build | Grok 4.6 | `xhigh` | 50 / 50 | Complete |

### How to interpret the results

- **Automated compliance** checks repeatable facts such as piece count, files, specification sections, identity declarations, path safety, self-contained assets, and build output.
- **Manual experience review** operates the 10 product prototypes, verifies normal flows and failure recovery, and evaluates product experience and visual quality.
- **User acceptance** determines which designs are genuinely useful, inspiring, worth saving, or worth developing further.

These are separate evidence levels. An earlier level cannot stand in for a later one. Daedalus does not publish an overall score, a “best model,” or a cross-task capability ranking.

### Browse and run the gallery

Visit the **[Daedalus Live Gallery](https://321sssrt-bit.github.io/daedalus-ui/)** after publication.

The local lifecycle uses only the Python standard library:

```bash
python -m daedalus validate
python -m daedalus build --output dist
python -m http.server 8765 --directory dist/site
```

Then open `http://127.0.0.1:8765/`. A local HTTP address avoids browser restrictions around `file://` URLs on mapped drives; closing the command window stops the preview server.

The gallery shows each submission's full identity and completion or forfeit state. Every piece exposes a measurable reproduction specification, while design intent and auxiliary prompting guidance remain separate. Personal favorites stay in the current browser and are not uploaded.

### Clean starter package

```bash
python -m daedalus starter --output dist/daedalus-clean.zip
```

The starter contains the rules, briefs, templates, and required tools, but no historical answers, generated gallery, local archives, or run-session declarations. A participating agent should use it in an isolated environment that cannot access public submissions, then hand the completed work back to a maintainer for import.

### Repository layout

| Path | Purpose |
| --- | --- |
| `catalog/` | The 50 shared briefs, quality requirements, reproduction-spec template, and design-intent template |
| `models/` | Current-rule submissions isolated by `harness / model / reasoning effort` |
| `daedalus/` | The `validate / build / starter` lifecycle entry points |
| `gallery/` | Compatibility entry points for the legacy packaging commands and submission-sealing hooks |
| `docs/adr/` | Confirmed product and engineering decisions |
| `docs/specs/` | Current implementation specifications |

Legacy-rule submissions remain in the maintainer's Git-external local archive and are not part of the public repository. Maintainers currently curate public submissions and do not accept community submission pull requests. Anyone may still fork and use the project independently under the MIT License.

### Publishing

`.github/workflows/pages.yml` validates the repository, builds the gallery, creates the clean starter package, and publishes GitHub Pages. Generated files remain in Actions artifacts and Pages rather than being committed to source history.

For the first publication, the repository owner selects **GitHub Actions** under **Settings → Pages → Build and deployment**. Subsequent pushes to `main` update the gallery automatically.

## License

[MIT](LICENSE) © 2026 Daedalus Authors
