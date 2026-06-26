# pptify Architecture

This workspace is a VS Code Copilot plugin for creating PowerPoint PPTX deck specifications. The plugin root is `pptify`.

## Plugin Components

- `pptify/.github/plugin/plugin.json` — VS Code/Copilot plugin metadata
- `pptify/agents/pptify-slides-builder.agent.md` — Main agent for spec generation and deck design workflow
- `pptify/skills/` — Domain-specific guidance (context strategy, spec authoring, visual assets, quality validation)
- `pptify/skills/pptify-reference-deck-analysis/` — Documents the extraction & style-analysis contract for existing PPTX decks (no importable bundled code)
  - extraction contract — slide structure, shapes, text, media
  - style-master contract — design, theme, colors, typography
  - `references/python-snippets.md` — documentation-only Python snippets, not runtime modules

## Workflow

The agent guides users through a 6-step deck specification process:

1. **Understand the Goal** — Gather business context, audience, narrative framework
2. **Design Strategy** — Select design direction and visual system
3. **Plan Slide Structure** — Map business framework to slide outline
4. **Spec Authoring** — Generate coordinate-explicit JSON specification
5. **Quality Validation** — Verify design context and styling consistency
6. **Response Contract** — Output structured JSON with validation status

## Extraction APIs

The pptify-reference-deck-analysis skill ships no importable code. It documents an extraction & style-analysis **contract** (inputs, outputs, JSON shapes) that the agent implements on demand with `python-pptx` to analyze reference decks or existing presentations. Historical Python snippets are retained as documentation in `references/python-snippets.md`, but they are not packaged modules.

Users integrate external services (LLM APIs, image generation) in their own pipelines; PPTify provides spec guidance and the extraction contract, not infrastructure.

## Data Contracts

Generated deck specs use explicit coordinates:

- Slide size, groups, object IDs, bounding boxes, roles, styles, z-order
- Text: explicit font size, color, alignment
- Shapes/lines: explicit fill, stroke, endpoints
- Images (object): `content.path` or `content.blob_base64`, plus `content.alt`
- Image provenance (separate manifest): provider, model, prompt path, status, error details
