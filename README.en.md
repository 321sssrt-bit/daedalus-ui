<p align="center">
  <img src="docs/assets/daedalus-cover.svg" alt="Daedalus — Open Product UI Design Evaluation for AI Models" width="100%">
</p>

<p align="center">
  <strong>Same rules. Different taste.</strong><br>
  40 independent pages · 10 end-to-end product prototypes · 50 reproducible specifications
</p>

<p align="center">
  <a href="README.md">中文</a>
  · <strong>English</strong>
  · <a href="https://321sssrt-bit.github.io/daedalus-ui/"><strong>Live Gallery</strong></a>
  · <a href="catalog/briefs.json">Briefs</a>
  · <a href="AGENTS.md">Rules</a>
  · <a href="LICENSE">MIT License</a>
</p>

---

## What is Daedalus?

Daedalus is an open product-design evaluation for UI agents and models, as well as a browsable gallery of design ideas. Every participant receives the same responsibilities, while choosing its own brand, layout, visual language, and copy.

The project was initially inspired by [Hall of One Hundred](https://miaai-lab.github.io/GLM-5.3-100-HTML-Files/). Daedalus adds operable, end-to-end product prototypes alongside independent interface pages to examine whether a model can extend visual taste into coherent product logic.

> Daedalus publishes work and evidence, not a model leaderboard. Passing automated checks does not prove design quality or user acceptance.

## Why focus on front-end product work?

Daedalus deliberately focuses on front-end product capability: organizing information, establishing a visual language, designing interactions, and keeping normal flows, failure feedback, and recovery actions coherent. It does not attempt to summarize a model's entire software-engineering capability with one set of briefs.

Back-end and systems capability is better examined separately—for example, with a chess benchmark covering board state, legal moves, turns, history, check and win conditions, castling, en passant, and promotion. The two evaluation tracks can complement each other without being collapsed into a single score.

## 40 + 10

| Briefs | Content | What it examines |
| --- | --- | --- |
| `001–040` | Independent pages such as sign-in, editor, dashboard, checkout, and error states | Visual range, information organization, and page responsibility |
| `041–050` | Shopping, payments, chat, social, media, collaboration, creation, travel, health, and learning | Core operation loops, result states, failure recovery, and retry success |

Each submission is registered under a three-part identity: `harness / model / reasoning effort`. Before starting or restarting a submission, the participating agent must show the expected identity to the user and receive explicit confirmation. Sub-agents may only accelerate non-overlapping work when they use the same model and reasoning effort as the main agent.

A participant that cannot honestly complete all 50 briefs may preserve its completed work and publicly forfeit. The gallery will display `我是鸡`, the forfeit reason, and the number of completed pieces instead of presenting an incomplete submission as complete.

## Current public submissions

This table follows the public registry in [`models/_index.json`](models/_index.json) and each submission's status in `model.json`. Gallery builds continue to treat those machine-readable files as the source of truth. Select a harness, model name, or “Open gallery” link to visit that model's dedicated gallery.

| Harness | Model | Reasoning effort | Completion | Status | Gallery |
| --- | --- | --- | --- | --- | --- |
| [Codex](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-5.6-sol--xhigh/) | [GPT-5.6 Sol](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-5.6-sol--xhigh/) | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-5.6-sol--xhigh/) |
| [DeepSeek Harness](https://321sssrt-bit.github.io/daedalus-ui/submissions/deepseek-harness--deepseek-v4-pro--max/) | [deepseek-v4-pro](https://321sssrt-bit.github.io/daedalus-ui/submissions/deepseek-harness--deepseek-v4-pro--max/) | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/deepseek-harness--deepseek-v4-pro--max/) |
| [Kimi Code](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--k3--max/) | [K3](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--k3--max/) | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--k3--max/) |
| [Grok Build](https://321sssrt-bit.github.io/daedalus-ui/submissions/grok-build--grok-4.6--xhigh/) | [Grok 4.6](https://321sssrt-bit.github.io/daedalus-ui/submissions/grok-build--grok-4.6--xhigh/) | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/grok-build--grok-4.6--xhigh/) |

## How to interpret the results

- **Automated compliance** checks repeatable facts such as piece count, files, specification sections, identity declarations, path safety, self-contained assets, and build output.
- **Manual experience review** operates the 10 product prototypes, verifies normal flows and failure recovery, and evaluates product experience and visual quality.
- **User acceptance** determines which designs are genuinely useful, inspiring, worth saving, or worth developing further.

These are separate evidence levels. An earlier level cannot stand in for a later one. Daedalus does not publish an overall score, a “best model,” or a cross-task capability ranking.

## Browse and run the gallery

Visit the **[Daedalus Live Gallery](https://321sssrt-bit.github.io/daedalus-ui/)** after publication.

The local lifecycle uses only the Python standard library:

```bash
python -m daedalus validate
python -m daedalus build --output dist
python -m http.server 8765 --directory dist/site
```

Then open `http://127.0.0.1:8765/`. A local HTTP address avoids browser restrictions around `file://` URLs on mapped drives; closing the command window stops the preview server.

The gallery shows each submission's full identity and completion or forfeit state. Every piece exposes a measurable reproduction specification, while design intent and auxiliary prompting guidance remain separate. Personal favorites stay in the current browser and are not uploaded.

## Clean starter package

```bash
python -m daedalus starter --output dist/daedalus-clean.zip
```

The starter contains the rules, briefs, templates, and required tools, but no historical answers, generated gallery, local archives, or run-session declarations. A participating agent should use it in an isolated environment that cannot access public submissions, then hand the completed work back to a maintainer for import.

## Repository layout

| Path | Purpose |
| --- | --- |
| `catalog/` | The 50 shared briefs, quality requirements, reproduction-spec template, and design-intent template |
| `models/` | Current-rule submissions isolated by `harness / model / reasoning effort` |
| `daedalus/` | The `validate / build / starter` lifecycle entry points |
| `gallery/` | Compatibility entry points for the legacy packaging commands and submission-sealing hooks |
| `docs/adr/` | Confirmed product and engineering decisions |
| `docs/specs/` | Current implementation specifications |

Legacy-rule submissions remain in the maintainer's Git-external local archive and are not part of the public repository. Maintainers currently curate public submissions and do not accept community submission pull requests. Anyone may still fork and use the project independently under the MIT License.

## Publishing

`.github/workflows/pages.yml` validates the repository, builds the gallery, creates the clean starter package, and publishes GitHub Pages. Generated files remain in Actions artifacts and Pages rather than being committed to source history.

For the first publication, the repository owner selects **GitHub Actions** under **Settings → Pages → Build and deployment**. Subsequent pushes to `main` update the gallery automatically.

## License

[MIT](LICENSE) © 2026 Daedalus Authors
