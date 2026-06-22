# pptify-kit

Agent-driven PPTX toolkit as a VS Code plugin. Agents use bundled skills, tools, and design context to generate coordinate-explicit PowerPoint decks.

[pptify](pptify) is the plugin root. The manifest is [pptify/.github/plugin/plugin.json](pptify/.github/plugin/plugin.json), and all exposed agents, skills, scripts, and resources are bundled there.

| Package | Purpose |
| --- | --- |
| [pptify/.github/plugin/plugin.json](pptify/.github/plugin/plugin.json) | VS Code/Copilot plugin metadata |
| [pptify/agents](pptify/agents) | Custom agents (main: pptify-slides-builder) |
| [pptify/skills](pptify/skills) | Agent Skills (context prep, spec authoring, visual assets, quality gates) |
| [pptify/skills/pptify-tooling/references](pptify/skills/pptify-tooling/references) | Import-only APIs for analyzing existing PPTX decks |

The plugin manifest intentionally declares the supported Copilot component folders, `pptify/skills/` and `pptify/agents/`. The end-to-end deck-generation workflow is consolidated into the custom agent; scripts and resources are bundled inside `pptify/skills/pptify-tooling/` as support assets referenced by declared components.

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## Sample pptx

Two stress-test decks pack dense, deliberately over-complicated layouts that exercise every part of the toolkit. Each slide locks one design profile from the bundled [design-profiles catalog](pptify/skills/pptify-context-prep/references/design-profiles.md) and renders in that profile's real tokens.

| Deck | Layouts | Open | Download |
| --- | --- | --- | --- |
| **pptify-kit-stress-demo-v2.pptx** | 50 | [Office viewer](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fkimtth%2Fpptify-kit%2Fmain%2Fdocs%2Fpptify-kit-stress-demo-v2.pptx) | [.pptx](docs/pptify-kit-stress-demo-v2.pptx) |
| **pptify-kit-stress-demo.pptx** | 81 | [Office viewer](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fkimtth%2Fpptify-kit%2Fmain%2Fdocs%2Fpptify-kit-stress-demo.pptx) | [.pptx](docs/pptify-kit-stress-demo.pptx) |

### Preview &mdash; pptify-kit-stress-demo-v2.pptx (50 layouts)

<p align="center">
  <img src="docs/preview/pptify-kit-stress-demo-v2-contact-sheet.png" alt="Contact sheet of all 50 layouts in pptify-kit-stress-demo-v2.pptx" width="900">
</p>

### Preview &mdash; pptify-kit-stress-demo.pptx (81 layouts)

<p align="center">
  <img src="docs/preview/pptify-kit-stress-demo-contact-sheet.png" alt="Contact sheet of all 81 layouts in pptify-kit-stress-demo.pptx" width="900">
</p>

<!-- Slide images are rendered with PowerPoint via [render_pptx_previews.ps1](docs/generated/render_pptx_previews.ps1) and tiled into contact sheets by [make_stress_contact_sheets.py](docs/generated/make_stress_contact_sheets.py). -->

## Extraction APIs

The pptify-tooling skill ships no importable code. It documents an extraction & style-analysis **contract** for analyzing existing PPTX decks, which the agent implements on demand with `python-pptx`. Documentation-only Python examples are preserved in [pptify/skills/pptify-tooling/references/python-snippets.md](pptify/skills/pptify-tooling/references/python-snippets.md); they are not packaged runtime modules.

The contract operations are:

- **prompt context** — compact deck context for LLM prompting (slides, styles, brand, template, layout)
- **extract file** — full deck extraction with `layout_tree`, `summary`, and OOXML render elements
- **extract path** — batch extraction over a folder, writing one JSON per deck plus a `manifest.json`
- **analyze path** — summary-only diagnostics for one deck or many
- **style master analyze** — theme colors, fonts, template usage, layout flow, and slide-level style signals

See [pptify/skills/pptify-tooling/SKILL.md](pptify/skills/pptify-tooling/SKILL.md) for the full contract.
