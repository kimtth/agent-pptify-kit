# pptify-kit

Agent-driven PPTX toolkit as a VS Code plugin. Agents use bundled skills, tools, and design context to generate coordinate-explicit PowerPoint decks.

[pptify](pptify) is the plugin root. The manifest is [pptify/.github/plugin/plugin.json](pptify/.github/plugin/plugin.json), and all exposed agents, skills, scripts, and resources are bundled there.

| Package | Purpose |
| --- | --- |
| [pptify/.github/plugin/plugin.json](pptify/.github/plugin/plugin.json) | VS Code/Copilot plugin metadata declaring exposed component folders |
| [pptify/agents](pptify/agents) | Custom agents discovered by the plugin |
| [pptify/skills](pptify/skills) | Agent Skills discovered by the plugin |
| [pptify/skills/pptify-tooling/scripts](pptify/skills/pptify-tooling/scripts) | Bundled support scripts called by skills and agents |
| [pptify/skills/pptify-tooling/resources/design](pptify/skills/pptify-tooling/resources/design) | Predefined design profiles and template context |

The plugin manifest intentionally declares the supported Copilot component folders, `pptify/skills/` and `pptify/agents/`. The end-to-end deck-generation workflow is consolidated into the custom agent; scripts and resources are bundled inside `pptify/skills/pptify-tooling/` as support assets referenced by declared components.

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## Sample pptx

[pptify-kit-stress-demo.pptx (densed and overcomplicated layout for stress testing)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fkimtth%2Fpptify-kit%2Fmain%2Fdocs%2Fpptify-kit-stress-demo.pptx)

## Setup

```powershell
uv sync                    # base dependencies
uv sync --extra plugins    # add source conversion, image search, vector tracing
```

## Image Provider Credentials

When OpenAI or Azure OpenAI image generation is needed, create a local `.env` from `pptify/skills/pptify-tooling/resources/env.template` and fill the required provider values there. The image helper loads `.env` automatically; `.env` is git-ignored and must not be committed.

```powershell
Copy-Item pptify/skills/pptify-tooling/resources/env.template .env
```

## Common Plugin Commands

```powershell
uv run python pptify/skills/pptify-tooling/scripts/design/design_context_catalog.py --list --pretty
uv run python pptify/skills/pptify-tooling/scripts/audit/audit.py deck-spec.json --json
uv run python pptify/skills/pptify-tooling/scripts/images/iconfy_search.py --query governance --collection fluent --color 0078D4 --pretty
uv run python pptify/skills/pptify-tooling/scripts/images/text_prompt_to_infographic.py --provider azure-openai --azure-endpoint "<endpoint>" --model "gpt-image-2" --prompt "..." --output-path out.png --pretty
```

Extraction helpers (`extraction/pptx_extractor.py`, `extraction/pptx_style_master.py`) are import APIs — load them with `importlib.util.spec_from_file_location(...)`.

## External Assets

The MiniLM ONNX model and tokenizer are not committed. Restore from the repository root:

```powershell
.\pptify\skills\pptify-tooling\scripts\download-external-assets.ps1
```
