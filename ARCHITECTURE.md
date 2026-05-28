# pptify Architecture

This workspace snapshot is a VS Code agent plugin for PPTX generation plus local helper tools. The plugin root inside this repository is `pptify`. It does not contain an importable `pptify/` core renderer package or a `python -m pptify` command.

## Current Components

- `pptify/.github/plugin/plugin.json`: VS Code/Copilot plugin metadata. It declares `agents/` and `skills/` as exposed plugin component folders.
- `pptify/agents`: Custom agents discovered directly by Copilot from the plugin root.
- `pptify/skills`: Agent Skills discovered directly by Copilot from the plugin root.
- `pptify/skills/pptify-tooling/scripts/documents`: document-to-markdown and markdown-to-RAPTOR helpers bundled as support assets for the declared skills and agents.
- `pptify/skills/pptify-tooling/scripts/design`: source-backed design context catalog loader for `pptify/skills/pptify-tooling/resources/design`.
- `pptify/skills/pptify-tooling/scripts/images`: web image search, Iconify search, raster-to-SVG conversion, and OpenAI/Azure OpenAI infographic generation.
- `pptify/skills/pptify-tooling/scripts/audit`: standalone content-region collision audit for layout-tree JSON specs.
- `pptify/skills/pptify-tooling/scripts/extraction`: importable PPTX extraction and style-master analysis helpers.
- `pptify/skills/pptify-tooling/resources/design`: local source-backed design context packs and attribution metadata.

The end-to-end deck-generation workflow is consolidated into `pptify/agents/pptify-deck-builder.agent.md`; there is no separate `workflows/` directory.

## Execution Model

Plugin scripts are called directly by file path and write JSON to stdout:

```powershell
uv run python pptify/skills/pptify-tooling/scripts/design/design_context_catalog.py --list --pretty
uv run python pptify/skills/pptify-tooling/scripts/images/text_prompt_to_infographic.py --provider auto --prompt "Cloud governance roadmap" --output-path infographic.png --pretty
uv run python pptify/skills/pptify-tooling/scripts/audit/audit.py deck-spec.json --json
```

Extraction helpers are import APIs; load those modules with `importlib.util.spec_from_file_location(...)`.

## Data Contracts

The prompt assets still use the agent-coordinate contract for generated deck specs:

- Each generated slide should have explicit slide size, groups, object IDs, bboxes, roles, styles, and z-order.
- Text-bearing objects should carry explicit font size and color.
- Lines should carry explicit endpoints and line style.
- Shapes should carry explicit shape, fill, and line style.
- Image-model attempts must record provider, model or deployment, prompt path, output path, status, and error details when generation fails.

In this snapshot, that contract is planning/audit context. There is no local renderer package that consumes the full layout tree and writes a PPTX from `python -m pptify`.

## Image Generation Boundary

`pptify/skills/pptify-tooling/scripts/images/text_prompt_to_infographic.py` supports `openai`, `azure-openai`, and `auto` provider selection. It deliberately has no local fallback image provider. If credentials or provider configuration are missing, or the provider returns an error, the caller should persist the failure manifest and avoid describing substitute artwork as model-generated.

Provider configuration and credentials are loaded from `.env`. Create `.env` from `pptify/skills/pptify-tooling/resources/env.template` when image generation is needed, fill the required values locally, and keep `.env` out of git.

## Optional Assets

The MiniLM ONNX model and tokenizer are downloaded on demand and ignored by git:

- `pptify/skills/pptify-tooling/scripts/external/all-MiniLM-L12-v2/*`

Restore with:

```powershell
.\pptify\skills\pptify-tooling\scripts\download-external-assets.ps1
```

`document_to_raptor_tree.py` uses the local MiniLM ONNX model when restored, then falls back to deterministic local embeddings when the optional assets are absent.

## Quality Gates

For generated artifacts, use the standalone audit plugin and PPTX package inspection scripts/helpers to confirm slide count, hidden-slide metadata, media counts, and collision status.

## Known Gaps

- Prompt assets may still mention restored-renderer paths conditionally; treat them as unavailable unless a core renderer package is restored.
