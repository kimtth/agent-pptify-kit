# Proposal: `pptx-deck-creation` plugin

## Preliminary checks

- [x] I have read the Code of Conduct.
- [x] I have read `docs/authoring.md`.
- [x] I have reviewed `docs/plugins.md` to confirm this is not a duplicate.
- [x] This proposal is for legitimate, constructive use cases only.
- [x] I have domain expertise in PowerPoint deck design, editable PPTX
	generation, Office Open XML package inspection, and presentation quality
	assurance.

## Component type

New plugin.

## Proposed name

`pptx-deck-creation`

## Parent plugin

Not applicable. This is a new plugin.

## Domain and expertise

Editable PowerPoint deck creation, reference-deck analysis, and quality review.

## Unique value proposition

No existing marketplace plugin provides a spec-first workflow for a
production-ready, editable PPTX deck. This proposal requires final inch-based
layout trees, native editable objects rather than image-only slides, read-only
reference-deck analysis, and geometry, accessibility, source-lineage, and OOXML
package checks. It complements file conversion rather than duplicating it.

## Primary use cases

1. Create an editable executive, sales, technical, or operational deck from a
   brief and source material.
2. Analyze a reference PPTX for theme, typography, and layout rhythm, then
   re-author a distinct deck with independent coordinates.
3. Audit a generated PPTX for layout, accessibility, and package-integrity defects.

## Cross-harness portability notes

Use portable Markdown/YAML, progressive disclosure through `references/`, and
tool-neutral action language. The agent will use the collision-safe name
`pptx-deck-creation-builder`. `python-pptx` and `defusedxml` are optional local
dependencies; no browser, renderer, MCP server, API, credentials, or online
service is required. Every agent and skill description will include a supported
trigger phrase such as “Use when …”.

## Example interactions

**User prompt:** “Create an eight-slide board update from this project brief.
Use an executive-summary-first narrative and deliver an editable PPTX.”

**Behavior:** Create a coordinate-explicit specification, a small task-specific
builder, and geometry, accessibility, source, and package-integrity audits.

**User prompt:** “Use `prior-proposal.pptx` only as visual inspiration for a
new customer proposal. Do not copy its slides.”

**Behavior:** Extract read-only design signals, then author an independent
outline and native-object layout trees.

**User prompt:** “Audit `operating-review.pptx` against its deck spec and fix
deterministic layout or package errors.”

**Behavior:** Check layout, accessibility, and OOXML integrity; repair the
specification or task-local builder, never the supplied reference deck.

## Submitter expertise

Experience creating contract-based PPTX workflows in
[mini-notebooklm-agent-pptx](https://github.com/kimtth/mini-notebooklm-agent-pptx):
source-grounded storyboard and theme contracts, precomputed layout-spec JSON,
deterministic PPTX rendering, and post-generation overlap, bounds, and text-
overflow validation. This proposal adapts those lessons into a lightweight,
portable plugin centered on coordinate-explicit deck contracts.

## Contribution plan

1. Create `plugins/pptx-deck-creation/` with `.claude-plugin/plugin.json`, a
   marketplace entry, one plugin-scoped agent, and concise skills with
   `references/` for detailed guidance.
2. Run `make generate-all` so committed native-install registries stay in sync.
3. Run `make validate STRICT=1`, `make garden STRICT=1`, `make test`, and the
   relevant `plugin-eval` portability check before opening the PR.

## Additional context

