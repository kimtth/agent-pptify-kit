# pptify-kit

Agent-driven PPTX toolkit packaged as a VS Code agent plugin. Coding agents use the root-level skill set, plugin tools, and predefined design context to plan and generate coordinate-explicit PowerPoint decks.

> **Sample** (densed and overcomplicated layout for stress testing): [pptify-kit-stress-demo.pptx](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fkimtth%2Fpptify-kit%2Fmain%2Fdocs%2Fpptify-kit-stress-demo.pptx)


| Package | Purpose |
| --- | --- |
| [plugin.json](plugin.json) | VS Code/Copilot plugin metadata declaring exposed component folders |
| [agents](agents) | Custom agents discovered by the plugin |
| [skills](skills) | Agent Skills discovered by the plugin |
| [scripts](scripts) | Bundled support scripts called by skills and agents |
| [resources/design](resources/design) | Predefined design profiles and template context |
| [pptify-cli](pptify-cli) | Installs the above into `./.agent/` |

The plugin manifest intentionally declares the supported Copilot component folders, `skills/` and `agents/`. The end-to-end deck-generation workflow is consolidated into the custom agent; `scripts/` and `resources/` are bundled support assets referenced by declared components.

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## Setup

```powershell
uv sync                    # base dependencies
uv sync --extra plugins    # add source conversion, image search, vector tracing
```

## Agent Install

```powershell
uv run python pptify-cli install                              # → ./.agent/
uv run python pptify-cli install --home ~                     # → ~/.agent/
uv run python pptify-cli install --home temp\pptify-install-test  # → temp\pptify-install-test\.agent\
```

See [pptify-cli/README.md](pptify-cli/README.md) for `uninstall`, `help`, and `--dry-run`.

## Image Provider Credentials

When OpenAI or Azure OpenAI image generation is needed, create a local `.env` from `resources/env.template` and fill the required provider values there. The image helper loads `.env` automatically; `.env` is git-ignored and must not be committed.

```powershell
Copy-Item resources/env.template .env
```

## Common Plugin Commands

```powershell
uv run python scripts/design/design_context_catalog.py --list --pretty
uv run python scripts/audit/audit.py deck-spec.json --json
uv run python scripts/images/iconfy_search.py --query governance --collection fluent --color 0078D4 --pretty
uv run python scripts/images/text_prompt_to_infographic.py --provider azure-openai --azure-endpoint "<endpoint>" --model "gpt-image-2" --prompt "..." --output-path out.png --pretty
```

Extraction helpers (`extraction/pptx_extractor.py`, `extraction/pptx_style_master.py`) are import APIs — load them with `importlib.util.spec_from_file_location(...)`.

## External Assets

The MiniLM ONNX model and tokenizer are not committed. Restore from the repository root:

```powershell
.\scripts\download-external-assets.ps1
```
