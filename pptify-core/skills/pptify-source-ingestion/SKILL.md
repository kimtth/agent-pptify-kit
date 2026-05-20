---
name: pptify-source-ingestion
description: "Prepare source material for pptify decks. Use when converting documents, summarizing long markdown, analyzing reference PPTX decks, extracting production PPTX files, or preserving source deck language and style."
---

# PPTify Source Ingestion

Use this skill when the user provides source documents, existing decks, URLs, or unstructured notes that should become slide content.

## Source Documents

- Convert long source documents to markdown before planning slides: `uv run python pptify-plugin/documents/document_to_markdown.py --source source.pdf --output-path source.md`.
- Build a structured summary tree when a source is long or multi-topic: `uv run python pptify-plugin/documents/document_to_raptor_tree.py --markdown-path source.md --output-path source-summary.json --title "Source" --pretty`.
- For URL-based, topic-plus-research, source-backed, or multi-source decks, combine converted/downloaded source markdown into a corpus and run the RAPTOR summary before slide planning, even when individual sources are short.
- Record the corpus path, summary path, source count, and source URLs in `summary.source_enrichment` or the companion manifest so enrichment evidence survives review.
- Use the summary tree to identify audience, thesis, slide sequence, evidence, risks, and decision points.
- Do not paste entire long documents into the deck spec; summarize into concise slide messages and cite sources in footers when needed.

## Reference PPTX

- Use the importable helpers in `pptify-plugin/extraction` or package inspection to inspect production complexity, slide text, style, brand, template, and layout-rhythm facts. The `python -m pptify --analyze-pptx` command is unavailable unless the core renderer package is restored.
- Use the extracted facts as agent context when the new deck should follow a source deck's language, slide count, topic sequence, executive tone, colors, fonts, template conventions, and layout rhythm.
- When authoring the new spec, translate `brands.primary_color`, `brands.accent_colors`, `brands.fonts`, `template.slide_size`, `template.layout_usage`, and `layout.slides[*].dominant_flow` into explicit `layout_tree` primitives, colors, typography, spacing, and coordinates.
- Use extraction helpers when the goal is reconstructing or preserving an existing production deck rather than authoring a new editable deck.
- For new editable decks, treat reference layout rhythm as prompt context; generated coordinates must be authored directly by the agent in `layout_tree` unless the slide is extracted for preserve-coordinate OOXML reconstruction.
- Never copy or mutate a referenced PPTX as the generation strategy. Use analysis as context and build a new PPTX artifact.

## Predefined Design Context

- Use `pptify-design` when the source style should come from a public predefined template or design system instead of a user-provided PPTX.
- Load selected profiles with `uv run python pptify-plugin/design/design_context_catalog.py --profile <id> --include-context --pretty` and pass the result into the agent context before JSON authoring.
- Do not treat `pptify-design` as content source material; it is design context only.

## Source-to-Deck Planning

- Convert source material into one message per slide before authoring visual structure.
- Treat charts and dashboard-style slides as source-evidence-driven exhibits; do not create generic metric or dashboard slides when the source corpus does not provide relevant data.
- Preserve important terminology, product names, metrics, dates, and user-provided wording.
- Reduce dense narrative into executive slide titles plus short sections.
- Track open assumptions in speaker notes or audit-facing summary fields instead of overcrowding slides.