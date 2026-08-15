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

## Current public submissions

Five complete submissions are now published. Open a dedicated gallery below, or use the **[combined gallery](https://321sssrt-bit.github.io/daedalus-ui/)** to browse them together.

| Harness | Model | Reasoning effort | Completion | Status | Gallery |
| --- | --- | --- | --- | --- | --- |
| Codex | GPT-5.6 Sol | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/codex--gpt-5.6-sol--xhigh/) |
| DeepSeek Harness | deepseek-v4-pro | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/deepseek-harness--deepseek-v4-pro--max/) |
| Kimi Code | K3 | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/kimi-code--k3--max/) |
| Grok Build | Grok 4.6 | `xhigh` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/grok-build--grok-4.6--xhigh/) |
| Qoder | Qwen3.8 | `max` | 50 / 50 | Complete | [Open gallery →](https://321sssrt-bit.github.io/daedalus-ui/submissions/qoder--qwen3.8--max/) |

## Browse and reuse

The gallery can be browsed by submission or by brief. Every piece opens independently and includes its reproduction specification and design intent. Personal favorites remain in the current browser and are never uploaded.

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

