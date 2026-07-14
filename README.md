## PPTX Deck Creation Kit

Agent-driven PPTX toolkit for VS Code. It creates editable PowerPoint decks
with coordinate-explicit specifications and native PPTX objects.

The GitHub Copilot plugin directory is
[pptx-deck-creation](pptx-deck-creation). Its manifest is
[pptx-deck-creation/.github/plugin/plugin.json](pptx-deck-creation/.github/plugin/plugin.json).
The portable Agentic Plugin Marketplace staging artifacts are in
[pptx-deck-creation-agentic-plugin](pptx-deck-creation-agentic-plugin).

| Package | Distribution | Purpose |
| --- | --- | --- |
| [pptx-deck-creation](pptx-deck-creation) | GitHub Copilot plugin | Full plugin distribution: agent, deck-context, specification, visual-assets, reference-analysis, OOXML, and quality-gate skills |
| [pptx-deck-creation-agentic-plugin](pptx-deck-creation-agentic-plugin) | [wshobson/agents](https://github.com/wshobson/agents) | Portable marketplace staging artifacts for Claude Code, Codex CLI, Cursor, OpenCode, Gemini CLI, and GitHub Copilot |
| [pptx-deck-creation-compact](pptx-deck-creation-compact) | [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | Compact single-skill distribution for the Agentic Awesome Skills catalog |

The plugin manifest declares the supported agent and skill paths. The workflow is
in the custom agent. Reference-deck analysis remains static documentation in
[pptx-deck-creation/skills/pptx-reference-deck-analysis](pptx-deck-creation/skills/pptx-reference-deck-analysis).

The output remains editable: titles, text, data labels, tables, charts, and
diagrams use native PowerPoint objects. Images support the slide but never make
up its entire meaningful content.

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## Sample pptx

Two stress-test decks pack dense, deliberately over-complicated layouts that
exercise every part of the toolkit. Each slide locks one design profile from the
bundled [design-profiles catalog](pptify/skills/pptx-deck-context/references/design-profiles.md)
and renders in that profile's real tokens.

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

## Extraction APIs

The `pptx-reference-deck-analysis` skill ships no importable code. It documents
an extraction and style-analysis contract for existing PPTX decks, which the
agent implements on demand with `python-pptx`. Documentation-only examples are
preserved in [pptify/skills/pptx-reference-deck-analysis/references/python-snippets.md](pptify/skills/pptx-reference-deck-analysis/references/python-snippets.md).
They are not packaged runtime modules.

The contract operations are:

- **prompt context** — compact deck context for LLM prompting (slides, styles, brand, template, layout)
- **extract file** — full deck extraction with `layout_tree`, `summary`, and OOXML render elements
- **extract path** — batch extraction over a folder, writing one JSON per deck plus a `manifest.json`
- **analyze path** — summary-only diagnostics for one deck or many
- **style master analyze** — theme colors, fonts, template usage, layout flow, and slide-level style signals

See [pptify/skills/pptx-reference-deck-analysis/SKILL.md](pptify/skills/pptx-reference-deck-analysis/SKILL.md)
for the full contract.

## OOXML Package Inspection

For existing-deck details that `python-pptx` cannot expose, the
[pptx-ooxml skill](pptify/skills/pptx-ooxml/SKILL.md) supplies safe, read-only
tools to inspect the package relationship graph, theme, masters, layouts,
notes, comments, animations, and media. It never mutates a supplied reference
deck or copies binary parts into a generated deck.

For production decks, its package-integrity check reports malformed XML, broken
internal relationships, missing content-type declarations, duplicate layout
relationships, and orphaned media or notes.

When a reference deck is a template, build a zero-based, read-only layout
catalog before planning the new deck. It records reusable layout evidence only;
the target deck is still re-authored with independent coordinates and native
objects.
