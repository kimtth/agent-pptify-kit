---
name: pptx-ooxml
description: "Inspect an existing PPTX package with safe Office Open XML parsing when python-pptx cannot expose theme, relationship, notes, comments, animation, or layout details."
---

# PPTX OOXML Inspection

Use this skill for **read-only** inspection of an existing PowerPoint package when high-level `python-pptx` access is insufficient. It complements `pptx-reference-deck-analysis`; it does not replace the coordinate-explicit generation workflow.

Install the required `defusedxml` dependency from `requirements.txt` before running the bundled scripts.

## Boundaries

- Never modify the supplied source deck. New decks remain the responsibility of `pptx-slide-specification` and a task-specific `python-pptx` builder.
- Use OOXML when inspecting themes, masters, layouts, slide relationships, notes, comments, animations, media, or non-modeled formatting.
- Do not blindly copy XML parts into a generated deck. Treat extracted values as read-only design and content evidence.
- Use the bundled scripts only from a trusted workspace. They reject path traversal, symlinks, oversized members, and compressed archive bombs.

## Workflow

1. Run `scripts/inspect.py <deck.pptx>` for compact JSON: slide order, text, shape counts, theme colors/fonts, relationships, notes/comment-part inventory, animations, and media.
2. Run `scripts/validate_package.py <deck.pptx> --output <report.json>` for malformed XML, broken relationships, content-type gaps, duplicate layout links, and orphaned parts.
3. Run `scripts/unpack.py <deck.pptx> <output-dir>` only when raw part evidence is necessary.
4. Inspect the relevant parts:
	- `ppt/presentation.xml` — slide order and metadata
	- `ppt/slides/slideN.xml` and `_rels/slideN.xml.rels` — shapes and part relationships
	- `ppt/slideLayouts/`, `ppt/slideMasters/`, and `ppt/theme/theme1.xml` — template and design signals
	- `ppt/notesSlides/`, `ppt/comments/`, and `ppt/media/` — notes, comments, and supporting assets
5. Feed extracted palette, typography, layout, and package facts into the reference-analysis contract or `summary.design_context`.
6. Record the input deck path, inspected parts, validation report, tool version, and any unreadable XML in the analysis manifest.

## Parsing Rules

- Parse untrusted XML with `defusedxml`; do not enable entity expansion, DTD loading, or network access.
- Resolve relationship targets relative to the `.rels` owner; do not infer slide order from filenames.
- Preserve `xml:space="preserve"` semantics when collecting text.
- Treat theme colors as tokens unless fully resolved against the color scheme.
- `python-pptx` remains preferred for ordinary shape geometry and editable-text extraction; use OOXML only for the gap it fills.

See [references/ooxml-parsing.md](references/ooxml-parsing.md) for part maps, namespaces, and result-shape guidance.
