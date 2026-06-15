# PPTify Toolkit Setup

Load this file when `skills/pptify-tooling/scripts/` is not found in the workspace and the user wants to install the optional PPTify toolkit.

The expected users are presentation and business users. Do not make Python or `uv` installation their manual task. First try bundled references and no-install helper fallbacks from `pptify-tooling`; only run setup when helper execution is essential and the user approves it. If Python is absent, install `uv` first and let `uv` install Python and create the project environment.

## Repository

| Field | Value |
|---|---|
| URL | https://github.com/kimtth/agent-pptify-kit |
| License | MIT |
| Runtime manager | `uv`, including managed Python 3.13 |

## Install

Do not clone or install this external repository automatically. First explain that the built-in awesome-copilot skill includes bundled references, while the external toolkit is only needed for helper-script execution. Continue only after the user explicitly asks to install it or confirms that helper execution is required.

Before installing dependencies, check whether `uv` already exists:

```powershell
Get-Command uv -ErrorAction SilentlyContinue
```

If `uv` is missing and the user approves runtime setup, install `uv` with the least interactive option for the current OS. On Windows, prefer `winget` when available; otherwise use the official installer script. On macOS/Linux, use the official installer script.

```powershell
# Windows, if winget is available
winget install --id astral-sh.uv -e

# Windows fallback
irm https://astral.sh/uv/install.ps1 | iex
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After `uv` is available, let `uv` manage Python and the virtual environment for this project instead of asking the user to install Python manually.

```powershell
# 1. Clone into workspace root (use a subdirectory if the root already has a project)
git clone https://github.com/kimtth/agent-pptify-kit .

# 2. Install the project Python version managed by uv; this works even when Python was absent
uv python install 3.13

# 3. Create/update the project virtual environment and install base dependencies
uv sync

# 4. Add plugin extras: source ingestion, image helpers, audit tools
uv sync --extra plugins
```

If installation is blocked by policy, permissions, network, or missing package managers, do not keep asking the user to fix the machine. Apply the graceful-degradation fallbacks in `pptify-tooling` and report the blocked helper explicitly.

## No-Install Execution

When scripts are present but `uv` is unavailable, standard-library helpers can still run with plain Python if a Python command is already available. Use this only for helpers that do not need optional packages. If neither `uv` nor Python is available and helper execution is essential, ask for consent to install `uv` first; do not ask for a manual Python install.

```powershell
function Invoke-PptifyPython {
	if (Get-Command py -ErrorAction SilentlyContinue) {
		py -3 @args
	} elseif (Get-Command python -ErrorAction SilentlyContinue) {
		python @args
	} else {
		throw "No Python command is available. Ask for consent to install uv, then use uv python install 3.13."
	}
}
```

Examples from the repository root:

```powershell
Invoke-PptifyPython pptify/skills/pptify-tooling/scripts/design/design_context_catalog.py --list --pretty
```

If the workspace root belongs to another project, ask the user before cloning. Suggest a named subdirectory, e.g. `git clone https://github.com/kimtth/agent-pptify-kit pptify-kit`.

## Module Map

| Module path | Requires extra | What it provides |
|---|---|---|
| `pptify/skills/pptify-tooling/scripts/documents/document_to_markdown.py` | plugins | Convert PDF, DOCX, HTML, or plain text to markdown for source prep |
| `pptify/skills/pptify-tooling/scripts/documents/document_to_raptor_tree.py` | plugins (optional; stdlib fallback) | Build a RAPTOR hierarchical summary tree from a markdown source |
| `pptify/skills/pptify-tooling/scripts/design/design_context_catalog.py` | none (stdlib only) | List and load bundled design profiles; returns style context for spec authoring |
| `pptify/skills/pptify-tooling/scripts/images/web_image_search.py` | plugins (optional; degrades gracefully) | Search the web for candidate images without required API keys |
| `pptify/skills/pptify-tooling/scripts/images/iconfy_search.py` | none (stdlib only) | Search Iconify icon library for SVG icons by query, collection, and hex color |
| `pptify/skills/pptify-tooling/scripts/images/raster_image_to_svg.py` | none (stdlib); vtracer for --mode vector-trace | Convert raster images to SVG wrappers; optional vector trace mode |
| `pptify/skills/pptify-tooling/scripts/images/text_prompt_to_infographic.py` | none (stdlib only) | Generate infographic images via OpenAI or Azure OpenAI (no local fallback) |
| `pptify/skills/pptify-tooling/scripts/extraction/pptx_extractor.py` | base (python-pptx) | Extract slide text, style, layout, and media metadata from a reference PPTX |
| `pptify/skills/pptify-tooling/scripts/extraction/pptx_style_master.py` | base (python-pptx) | Extract brand, template, and master-slide style facts from a reference PPTX |

## Image Generation `.env`

Create `.env` in the workspace root before invoking `text_prompt_to_infographic.py`. Never put secrets in chat or in the prompt dialog — fill the file directly in the editor or terminal.

```dotenv
# Provider: auto | openai | azure-openai
PPTIFY_IMAGE_PROVIDER=

# --- OpenAI ---
OPENAI_API_KEY=
OPENAI_IMAGE_MODEL=gpt-image-1

# --- Azure OpenAI ---
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_IMAGE_DEPLOYMENT=
```

Use `az login` when managed identity or CLI auth is preferred over an API key.

## Verification After Install

```powershell
# List available design profiles with uv
uv run python pptify/skills/pptify-tooling/scripts/design/design_context_catalog.py --list --pretty

# Or, when uv is unavailable but plain Python is available
Invoke-PptifyPython pptify/skills/pptify-tooling/scripts/design/design_context_catalog.py --list --pretty
```
