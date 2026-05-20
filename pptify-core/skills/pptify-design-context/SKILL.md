---
name: pptify-design-context
description: "Select and apply source-backed predefined design templates and design-system prompt context from pptify-design. Use when a deck needs a predefined visual template, design context for an LLM, source-backed style profile, or design-agent prompt guidance."
---

# PPTify Design Context

Use this skill for every new generated deck unless a user-provided brand guide or reference PPTX is the explicit primary style source. A generated deck without selected design context tends to look like a default `python-pptx` artifact and is not production-ready.

## Source-Backed Rule

- Use profiles from `pptify-design/sources.json`; do not invent a new design template when the user asks for predefined templates.
- Keep source attribution and license metadata attached to the context used.
- If no catalog profile fits, use reference PPTX analysis through `pptify-plugin/extraction` helpers or package inspection, search for another public source, or ask the user for a source template.
- Record selected profile IDs, source URLs, and style lock details in `summary.design_context` before building the PPTX.

## Profile Selection

- Use `primer-primitives` for GitHub-style product, developer, or token-driven engineering decks.
- Use `fluent-ui-design-tokens` as the default for new decks, including Microsoft, M365, Teams, Power Platform, enterprise-aligned, general modern, stylish, product, app, pitch, or unspecified visual style requests.
- Use `awesome-copilot-design-agents` when the agent prompt itself needs design review, UX discovery, visual hierarchy, or accessibility framing.
- Use `corazzon-pptx-design-styles` when a broader modern style catalog or multiple visual direction options are explicitly useful. Pick one style from the catalog and lock its palette, typography, spacing, and signature element before layout planning.
- Use `likaku-mck-ppt-design-skill` for consulting, strategy, governance, or operations decks that need action-title discipline and structured native PPTX layouts.

## Tooling

List profiles:

```powershell
uv run python pptify-plugin/design/design_context_catalog.py --list --pretty
```

Load context for one or more profiles:

```powershell
uv run python pptify-plugin/design/design_context_catalog.py --profile fluent-ui-design-tokens --include-context --pretty
uv run python pptify-plugin/design/design_context_catalog.py --profile primer-primitives --include-context --pretty
uv run python pptify-plugin/design/design_context_catalog.py --profile fluent-ui-design-tokens --profile awesome-copilot-design-agents --include-context --pretty
uv run python pptify-plugin/design/design_context_catalog.py --profile corazzon-pptx-design-styles --include-context --pretty
```

## Applying Context to JSON Authoring

1. Put the selected profile payload into the agent context before writing `deck-spec.json`.
2. Translate source signals into explicit `layout_tree` objects, colors, fills, lines, typography, spacing, bboxes, and z-order.
3. Keep meaningful slide content as `classification: "content"` objects and decorative/background elements as `classification: "layout_design"` objects.
4. Use source CSS or reference deck rhythm only as design evidence; final coordinates must be authored directly in inches.
5. Record the selected profile IDs and source URLs in `summary.design_context` when the generated spec is expected to be reviewed or reused.
6. Add at least one style-derived visible design element to every normal content slide: accent band, rule, card shell, grid cell, diagram primitive, shape motif, image treatment, or pattern. A plain title-plus-bullets slide fails the design gate.

## Restrictions

- Do not copy external fonts, icon packs, photos, or binary assets unless their license and source are explicitly added.
- Do not claim the output is a Primer, Fluent UI, or Awesome Copilot artifact; these are context sources for a new `pptify` deck.
- Do not let source CSS override pptify quality gates: built decks still need zero content collisions and zero text overflows.
- Do not accept default PowerPoint theme colors, Calibri-only text boxes, plain white backgrounds, or placeholder-style bullet layouts as a finished design.