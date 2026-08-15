# Daedalus 50 题公开评测与展厅规格

## Problem Statement

维护者需要一套长期稳定的产品 UI 模型评测与灵感展厅。当前项目只有 40 道彼此独立的页面题，无法观察模型能否设计一个具备核心操作、结果状态和异常恢复的小程序；答卷身份也只有模型名，无法拆分运行框架和思考档位。现有打包与展厅机制缺少面向公开 GitHub 仓库的路径安全、内容隔离、统一自动检查、干净测试包和 Pages 发布闭环，旧答卷也没有可验证的思考档位，不能继续冒充新版结果。

## Solution

把项目升级并正式定义为 **Daedalus — Open Product UI Design Evaluation for AI Models**（面向 AI 模型的公开产品 UI 设计评测）。评测固定为 50 题：001–040 保留为独立页面题，041–050 增加十种单文件产品原型。每个产品原型必须完成一条正常核心操作闭环，并提供一个可触发、可恢复的异常分支。每题同时提交可量测、可验收的复现规范和非规范性的设计意图；提示词只属于设计意图，不能替代规范。

答卷身份由运行框架、模型和思考档位共同组成。主 Agent 与子 Agent 必须使用相同模型和思考档位，子 Agent 只能通过并行提速。无法诚实完成的 Agent 可以公开弃权，展厅显示“我是鸡”。旧 40 题答卷只在本地归档，所有模型以后按新版规则重做完整 50 题。

仓库使用 MIT 许可证，通过一个最高层仓库生命周期接口完成自动合规、展厅构建和干净测试包生成。GitHub Actions 调用同一接口并把临时生成物发布到 GitHub Pages；生成展厅不写回 Git 历史。项目不接数据库、不做公共投票，初期不接受社区答卷 Pull Request。

## User Stories

1. As a maintainer, I want the project to have a distinctive name, so that it is recognizable beyond a generic “UI Test”.
2. As a maintainer, I want exactly 50 stable tasks, so that future model runs remain comparable in scope.
3. As a maintainer, I want the existing 40 page responsibilities preserved, so that the current breadth of UI inspiration is not lost.
4. As a maintainer, I want ten product prototype tasks, so that the evaluation covers product logic as well as page styling.
5. As a maintainer, I want each prototype to have a fixed product type and core task, so that different answers address the same product responsibility.
6. As a maintainer, I want five desktop and five mobile prototypes, so that neither device class dominates the advanced tasks.
7. As a maintainer, I want every prototype to include a recoverable failure, so that error handling is visible rather than assumed.
8. As a maintainer, I want all 50 works to have distinct visual identities, so that the gallery remains useful for inspiration.
9. As a maintainer, I want each prototype’s internal states to share one design system, so that the prototype feels like one product.
10. As a maintainer, I want every answer identified by harness, model, and reasoning effort, so that materially different runs are not merged.
11. As a maintainer, I want reasoning effort shown in the gallery, so that visitors can interpret results honestly.
12. As a maintainer, I want subagents restricted to the same model and reasoning effort, so that delegation changes speed rather than capability.
13. As a maintainer, I want the final run receipt to disclose subagent use, so that parallelism is visible.
14. As a maintainer, I want an Agent to be able to forfeit honestly, so that an incomplete run is not disguised as completion.
15. As a maintainer, I want forfeiture displayed as “我是鸡”, so that the result is unmistakable and consistent with the project’s tone.
16. As a maintainer, I want completed work preserved when a run forfeits, so that partial evidence is not destroyed.
17. As a maintainer, I want old unverifiable answers archived locally, so that the public gallery contains only current-rule submissions.
18. As a maintainer, I want the local archive excluded from Git, so that legacy answers never leak into the public repository.
19. As a maintainer, I want one command surface for validation, building, and starter packaging, so that local and CI behavior cannot drift.
20. As a maintainer, I want generated galleries excluded from source history, so that answer changes remain reviewable.
21. As a maintainer, I want GitHub Actions to publish the gallery, so that the live site updates without manual packaging.
22. As a maintainer, I want a clean offline test package, so that a new Agent receives the rules without seeing earlier answers.
23. As a maintainer, I want the clean package verified before release, so that sealed content cannot enter it accidentally.
24. As a maintainer, I want a single MIT license, so that reuse conditions are simple.
25. As a maintainer, I want no voting backend or visitor database, so that operating the project remains lightweight.
26. As a maintainer, I want public answer intake deferred, so that early maintenance stays manageable.
27. As a test-taking Agent, I want a precise identity convention, so that I know which submission directory I own.
28. As a test-taking Agent, I want product prototype briefs to state the normal and failure paths, so that I do not invent the acceptance target.
29. As a test-taking Agent, I want freedom over brand, visual language, layout, and concrete copy, so that the gallery continues to reveal taste.
30. As a test-taking Agent, I want the prototype specification template to list every required section, so that product logic is documented consistently.
31. As a test-taking Agent, I want a clear completion report, so that missing tasks or unverifiable metadata cannot be mistaken for success.
32. As a test-taking Agent, I want a defined forfeit path, so that I can stop honestly when the workload exceeds my capability.
33. As a visitor, I want the repository homepage to link directly to a live gallery, so that I can see the work without running commands.
34. As a visitor, I want to browse by submission and task category, so that I can explore the collection efficiently.
35. As a visitor, I want to compare the same task between submissions, so that differences in design approach are visible.
36. As a visitor, I want to open a standalone answer, so that I can experience its interaction at the intended size.
37. As a visitor, I want to read and export the associated specification, so that an inspiring direction can be reproduced.
38. As a visitor, I want personal favorites to remain only in my browser, so that the project does not collect my data.
39. As a visitor, I want complete identity metadata beside each answer, so that I know which harness, model, and effort produced it.
40. As a visitor, I want forfeited submissions clearly distinguished from complete submissions, so that partial work is not misleading.
41. As a reviewer, I want machine-readable validation results, so that objective failures are easy to reproduce.
42. As a reviewer, I want automated checks limited to observable structure and safety, so that they do not pretend to judge product quality.
43. As a reviewer, I want explicit manual steps for each prototype, so that I can verify the normal flow and exception recovery.
44. As a reviewer, I want automated compliance and human acceptance reported separately, so that evidence levels are not conflated.
45. As a security reviewer, I want submission paths confined to their declared directory, so that metadata cannot read arbitrary repository files.
46. As a security reviewer, I want answer previews sandboxed, so that submitted scripts cannot control the parent gallery.
47. As a security reviewer, I want standalone openings isolated from the gallery opener, so that a page cannot navigate or modify its origin page.
48. As a security reviewer, I want all answers self-contained, so that public pages do not load unknown external code, fonts, or images.
49. As a future maintainer, I want accepted decisions and deprecated ideas clearly recorded, so that voting or community intake is not accidentally reintroduced.
50. As a future maintainer, I want Caissa kept outside this scope, so that the future chess evaluation can evolve independently.
51. As a maintainer, I want the user to confirm harness, model, and reasoning effort before a run starts, so that platform routing cannot silently create a wrongly attributed submission.

## Implementation Decisions

- The project name is Daedalus, with the public definition `Open Product UI Design Evaluation for AI Models`, the Chinese definition “面向 AI 模型的公开产品 UI 设计评测”, and the repository name `daedalus-ui`. The gallery is the result-browsing layer rather than the product definition.
- The repository uses MIT with the notice `Copyright (c) 2026 Daedalus Authors`.
- The catalog becomes a new schema version with exactly 50 ordered tasks.
- Tasks 001–040 retain their existing page responsibilities, must-have modules, device rules, and per-piece visual independence.
- Tasks 041–050 are, in order: shopping retail, wallet payment, instant messaging, social community, audio/video platform, team collaboration, creative tool, travel service, health habit, and learning knowledge.
- Tasks 041, 045, 046, 047, and 050 are desktop-first. Tasks 042, 043, 044, 048, and 049 are mobile-first.
- Each product prototype is a single offline HTML application with a visible entry or workspace, an editable or confirmable core operation, a result state, and one explicitly triggerable and recoverable exception.
- Shopping covers browse, variant and quantity selection, cart totals, order submission, and out-of-stock recovery.
- Wallet covers recipient selection, amount entry, confirmation, receipt, and insufficient-balance recovery.
- Messaging covers conversation selection, message composition, delivery state, failed send, and retry.
- Social covers feed browsing, composing with audience choice, publishing, draft preservation, and retry.
- Media covers discovery, playback, progress or queue changes, saved playback state, network interruption, and recovery.
- Collaboration covers task creation, assignment, status change, activity history, permission denial, and access request or safe return.
- Creative tools cover parameter or layer editing, live preview, format selection, export, unsupported export conditions, and corrected retry.
- Travel covers route search, service and seat selection, confirmation, itinerary receipt, sold-out state, and alternate selection.
- Health covers activity entry, goal progress, trend feedback, invalid data, correction, and recalculation.
- Learning covers lesson entry, exercise completion, result explanation, incorrect answer, and successful retry.
- Every piece has a normative `.spec.md` (layout, tokens, components, responsive behavior, content, motion, checks) and a non-normative `.intent.md` (design intent, audience, non-goals, reproduction prompt). Prototype specifications additionally record product boundary, state map, normal flow, exception recovery, data changes, and manual acceptance steps.
- Submission identity is composed of harness, model, and reasoning effort, stored as separate metadata fields and reflected in the submission hierarchy. Before a new or repeated answer starts, the Agent displays all three candidate values and waits for explicit user confirmation.
- A complete submission contains exactly 50 complete pieces and a run receipt. A forfeited submission has a model-level forfeited status, the phrase “我是鸡”, a reason, and any legitimately completed pieces.
- Subagents are optional. When used, they must match the main Agent’s model and reasoning effort; the receipt discloses their count and use.
- The repository lifecycle is a deep module behind one CLI seam with three caller-visible operations: validate, build, and starter. Internal parsers, renderers, scanners, and archive helpers do not become additional caller interfaces.
- Validation produces a machine-readable receipt and a non-zero exit status on failure.
- Build validates first, then creates the combined gallery, standalone galleries, offline download bundle, and Pages artifact without modifying tracked source files.
- Starter packaging validates first, then creates a clean offline package containing rules, catalog, templates, and lifecycle tooling but no answers, galleries, generated data, local archive, or session claims.
- The active submission registry contains only current-rule submissions. Legacy submissions are moved, without reading their sealed content, into a flat local archive using `unknown` where historical harness or effort is not provable.
- Generated gallery data is treated as build output and ignored by Git.
- GitHub Actions uses the same lifecycle interface as local execution, publishes the build artifact to GitHub Pages, and exposes the clean starter package as a workflow or release artifact.
- The public gallery remains a static application. Favorites stay in browser storage; no vote, analytics, account, database, or external backend is introduced.
- Answer HTML runs inside a sandboxed iframe without same-origin privilege. Standalone openings do not retain an opener relationship.
- Registry paths and declared answer filenames are normalized and rejected unless they remain inside the declared submission directory and use allowed file types.
- The initial public project is maintainer-curated and does not accept community answer PRs. Forking and independent reuse remain permitted by MIT.
- The Agent entry instructions become catalog-driven rather than hard-coding 40 tasks, and explicitly enforce identity, same-model parallelism, evidence labels, forfeit behavior, and the clean-package seal.

## Testing Decisions

- The highest test seam is the repository lifecycle CLI. Tests invoke its validate, build, and starter operations against temporary repository fixtures and inspect exit codes, receipts, and produced artifacts.
- Tests exercise external behavior rather than private parsers or renderer helpers. Internal functions receive focused tests only when a failure cannot be diagnosed reliably through the lifecycle seam.
- Catalog tests prove that task IDs are exactly 001–050, ordered and unique, with five desktop and five mobile prototype tasks and complete required fields.
- Submission tests prove that path identity and manifest identity agree, complete submissions contain exactly 50 complete pieces, duplicate IDs and slugs fail, and missing files fail.
- Forfeit tests prove that a forfeited submission requires the public phrase and a reason, may preserve completed pieces, and is rendered distinctly from a complete submission.
- Parallelism receipt tests prove that declared subagents cannot differ from the main model or reasoning effort.
- Path-security tests attempt parent traversal, absolute paths, alternate separators, encoded traversal, registry escape, and unsupported extensions; all must fail before file contents are embedded.
- HTML compliance tests prove that answers are self-contained, declare character encoding and viewport, avoid external URLs and imports, include reduced-motion handling, and contain no duplicate element IDs.
- Specification tests prove that all `.spec.md` files use specification version 2, contain measurable layout, token, component, responsive and acceptance sections, reference their exact HTML, and use colors present in that HTML. Tasks 041–050 also contain the complete product-prototype sections.
- Intent tests prove that every piece has a matching `.intent.md` with intent version 1, while prompt or design-intent headings inside `.spec.md` are rejected.
- Prototype static checks require the declared core-flow and exception evidence in the specification, but do not claim the interaction works.
- Manual prototype acceptance follows each specification’s stated steps and records whether the normal result and exception recovery were actually observed.
- Gallery tests prove that complete, missing, and forfeited states render correctly; harness, model, effort, and status are visible; and only common available tasks can be compared.
- Browser security tests prove that preview iframes are sandboxed and answer scripts cannot read or modify the parent gallery.
- Standalone-opening tests prove that opened answers have no usable opener reference and cannot redirect the gallery.
- Build tests prove that validation failure produces no publishable partial artifact, a successful build creates every required hall, and repeated builds from the same inputs are equivalent apart from explicitly injected build metadata.
- Starter-package tests inspect the archive contents and prove that no model answer, generated gallery, embedded gallery data, local archive, session claim, secret, or absolute machine path is present.
- Git hygiene tests prove that build outputs, local archive, caches, environment files, and session claims are ignored while source answers and specifications remain trackable.
- Workflow checks prove that CI validates before publishing and that Pages receives only the validated build artifact.
- The existing model-local validator and current packer provide prior art for semantic token checks, self-contained HTML checks, specification-section checks, and offline hall generation. Shared, general checks move behind the lifecycle seam; model-specific copy tokens do not become universal requirements.
- Verification reporting distinguishes file existence, automated compliance, built artifact, browser security smoke test, manual prototype acceptance, and user acceptance.

## Out of Scope

- Generating the new 50-piece answers for any model.
- Retrofitting unverifiable reasoning-effort labels onto old answers.
- Public voting, preference aggregation, analytics, accounts, databases, or external form services.
- Community answer Pull Requests, user prefixes, open submission moderation, or community identity verification.
- A global score, leaderboard, or claim that subjective preference is an objective model capability measure.
- Cryptographic proof that a third-party harness actually used its declared model or reasoning effort.
- Supporting legacy 40-piece answers as active current-version submissions.
- Caissa or any chess evaluation design and implementation.
- Creating a GitHub repository, configuring a remote, committing, pushing, enabling Pages, or publishing a release without separate authorization.
- Installing local dependencies, initializing Matt tooling, or adding a separate issue-tracker workflow.
- External fonts, images, package managers, application servers, or runtime databases for answer pages.

## Further Notes

- Current decision records remain the reason history. Deprecated voting and community-intake ADRs must not be treated as current requirements.
- The clean test package improves operational sealing but cannot prevent a model with independent internet access from searching the public repository. Runs described as sealed must occur in an environment where public answers are unavailable.
- Reasoning-effort labels are harness-native descriptions. Labels from different harnesses are displayed for transparency but are not normalized into one cross-harness scale.
- Local legacy archiving is a reversible but material filesystem move and requires explicit execution authorization before implementation performs it.
- This specification is stored locally because the repository currently has no configured GitHub remote, issue tracker, or `ready-for-agent` label vocabulary. It has not been published as an Issue.
