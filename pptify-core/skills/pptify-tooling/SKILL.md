---
name: pptify-tooling
description: "Choose and run current pptify plugin tools for PPTX creation. Use when selecting commands for agent spec authoring, reference deck analysis, extraction, document conversion, image search, icons, SVGs, infographics, or restored renderer workflows."
---

# PPTify Tooling

Use this skill when deciding which `pptify` command or plugin should be used to create a PPTX.

## Available Tools

- Install the base project with `uv sync`; install plugin helpers with `uv sync --extra plugins` when source ingestion or image helpers are needed.
- Current workspace reality check: no importable `pptify/` package or `python -m pptify` CLI is present in this snapshot. Use the standalone plugin scripts below, or restore the core renderer package before using the documented render/analyze/extract CLI commands.
- If the core renderer package is restored, render an existing coordinate-explicit JSON spec with `uv run python -m pptify input.json --out deck.pptx --audit audit.json`.
- Generate or repair JSON specs through GitHub Copilot CLI or the VS Code GitHub Copilot extension, then use the available PowerPoint generation path for this workspace.
- When a source deck should guide language, slide count, topic sequence, tone, colors, fonts, templates, and layout rhythm, use the importable helpers in `pptify-plugin/extraction` or package inspection to collect reference facts.
- Extract or analyze production PPTX files with `pptify-plugin/extraction` helpers when OOXML/media preservation or style context is required.
- List or load source-backed predefined design contexts with `uv run python pptify-plugin/design/design_context_catalog.py --list --pretty` or `uv run python pptify-plugin/design/design_context_catalog.py --profile fluent-ui-design-tokens --include-context --pretty`. Load design context for every new deck unless a user-provided brand guide or reference PPTX is the primary style source.

## Agent Rules

- Natural-language deck generation is external to plugin scripts. Use GitHub Copilot CLI or the VS Code GitHub Copilot extension to write `deck-spec.json` or a generation script.
- The saved spec should contain a complete `layout_tree` for every generated slide. The available plugin scripts can help audit or prepare context, but they do not render full decks.
- Before authoring a generation script, lock a `pptify-design` profile/style and translate it into explicit coordinates, colors, typography, and decorative primitives. `python-pptx` output that uses default placeholders, plain white backgrounds, and bullet-only slides is a quality failure.
- Do not use obsolete renderer flags such as `--provider copilot`, `--prompt`, `--prompt-file`, `--model`, or `--spec-out` unless a restored core CLI explicitly supports migration errors for them.
- Do not use obsolete layout shorthand such as `pattern`, `layout_pattern`, `composition.pattern`, `layout`, `sections`, `bullets`, `objects`, `theme`, or browser layout requests for generated slides.
- Keep secrets out of generated specs, audits, and prompt assets.
- For generated infographics, collect provider, model or deployment, auth mode, endpoint when needed, prompt, output path, and timeout before invoking `text_prompt_to_infographic.py`; capture an attempt manifest because the helper has no local fallback provider.
- Use audit collisions, overflows, and warnings as repair evidence after building a deck artifact.

## Plugin Tools

- `pptify-plugin/documents/document_to_markdown.py` converts PDF, DOCX, PPTX, XLSX, HTML, or TXT into markdown.
- `pptify-plugin/documents/document_to_raptor_tree.py` converts markdown into a structured summary tree for deck narrative planning.
- `pptify-plugin/design/design_context_catalog.py` emits source-backed design template and agent-prompt context from `pptify-design` for LLM deck authoring.
- `pptify-plugin/images/web_image_search.py` searches for web image candidates and returns JSON.
- `pptify-plugin/images/iconfy_search.py` searches Iconify icon candidates and returns SVG URLs.
- `pptify-plugin/images/raster_image_to_svg.py` wraps raster images in SVG or vector-traces them when optional `vtracer` is available; for text-heavy generated infographics, keep the raster visible and place the vector trace on a hidden final slide.
- `pptify-plugin/images/text_prompt_to_infographic.py` generates an infographic image from text using OpenAI or Azure OpenAI. With `--provider auto`, missing credentials return `missing_provider_config`; there is no built-in local SVG fallback.
- NotebookLM bridge support is unavailable unless `pptify-plugin/images/notebooklm_infographic.py` is restored; that script is absent in the current workspace snapshot.
