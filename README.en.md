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
  · <a href="docs/specs/daedalus-50-and-open-gallery.md">Specification</a>
  · <a href="LICENSE">MIT License</a>
</p>

---

## What is Daedalus?

Daedalus is an open product-design evaluation for UI agents and models, as well as a browsable gallery of design ideas. Every participant receives the same responsibilities while choosing its own brand, layout, visual language, and copy.

The project was initially inspired by [Hall of One Hundred](https://miaai-lab.github.io/GLM-5.3-100-HTML-Files/). Daedalus adds operable, end-to-end product prototypes alongside independent interface pages to see whether large models can create attractive frontends from relatively simple prompts.

## 40 + 10

| Briefs | Content | What it examines |
| --- | --- | --- |
| `001–040` | Independent pages such as sign-in, editor, dashboard, checkout, and error states | Visual range, information organization, and page responsibility |
| `041–050` | Shopping, payments, chat, social, media, collaboration, creation, travel, health, and learning | Core operation loops, result states, and failure recovery |

## Explore the gallery

The unified [live gallery](https://321sssrt-bit.github.io/daedalus-ui/) can be browsed by submission or brief; each piece opens independently with its reproduction specification and design intent, while personal favorites remain in the current browser and are never uploaded.

## Current public submissions

Eighteen submissions are published: seventeen complete and one forfeited. The newest is at the top. Open a dedicated gallery below, or use the **[combined gallery](https://321sssrt-bit.github.io/daedalus-ui/)** to browse them together. Completion and status follow each submission's `model.json`.

| Harness | Model | Reasoning effort | Completion | Status | Gallery |
| --- | --- | --- | --- | --- | --- |
| grokbot | grokbot | `default` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/grokbot--grokbot--default/) |
| Opencode | Muse Spark 1.3 Contributor Free | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/opencode--muse-spark-1.3-contributor-free--xhigh/) |
| Codex | GPT-6.1 Sol | `ultra` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-6.1-sol--ultra/) |
| Devin | SWE-2 | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/devin--swe-2--max/) |
| Codex | GPT-6 Luna | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-6-luna--max/) |
| Grok | Grok 4.7 | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/grok--grok-4.7--xhigh/) |
| Kimi Code | K2.8 Preview | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--k2.8-preview--max/) |
| DeepSeek Harness | DeepSeek V4.1 Flash expires-on-0910 | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/deepseek-harness--deepseek-v4.1-flash-expires-on-0910--max/) |
| Cursor | Composer 2.5 Fast | `default` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/cursor--composer-2.5-fast--default/) |
| Kimi Code | Qwen3.8 Flash Next | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--qwen3.8-flash-next--xhigh/) |
| Codex | GPT-6 Astra | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-6-astra--max/) |
| Kimi Code | DeepSeek V4 Flash vision-exp | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--deepseek-v4-flash-vision-exp--max/) |
| Qoder | 3.8 Flash | `xhigh` | 13 / 50 | Forfeited (我是鸡) | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/qoder--3.8flash--xhigh/) |
| Qoder | Qwen3.8 | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/qoder--qwen3.8--max/) |
| Grok Build | Grok 4.6 | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/grok-build--grok-4.6--xhigh/) |
| Kimi Code | K3 | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--k3--max/) |
| DeepSeek Harness | deepseek-v4-pro | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/deepseek-harness--deepseek-v4-pro--max/) |
| Codex | GPT-5.6 Sol | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-5.6-sol--xhigh/) |

<details>
<summary>Run locally</summary>

The local build uses only the Python standard library:

```bash
python -m daedalus validate
python -m daedalus build --output dist
python -m http.server 8765 --directory dist/site
```

Then open `http://127.0.0.1:8765/`. Close the command window to stop the preview.

</details>

## Independent evaluation

To run an evaluation without exposing participants to existing submissions, generate a clean starter package:

```bash
python -m daedalus starter --output dist/daedalus-clean.zip
```

The package contains only the rules, briefs, templates, and required tools—no existing submissions or generated gallery. For the full product and engineering decisions, see the [project specification](docs/specs/daedalus-50-and-open-gallery.md) and [`docs/adr/`](docs/adr/).

## License

[MIT](LICENSE) © 2026 Daedalus Authors
