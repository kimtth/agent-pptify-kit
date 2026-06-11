---
name: pptify-tooling
description: "Command reference for pptify plugin tools. Use when looking up plugin script syntax or the workspace reality check."
---

# PPTify Tooling

## Workflow

1. Run the workspace and runtime readiness checks before invoking any plugin script.
2. Treat Python and `uv` as agent-managed runtime details, not business-user prerequisites. If they are missing, use no-install fallbacks first unless the requested helper is essential.
3. If helper execution is essential and Python is missing, install `uv` first after user consent; then use `uv python install 3.13` and `uv sync` to create the Python environment. Do not ask the user to manually install Python.
4. If `uv` is missing, ask before running the `uv` bootstrap in `references/toolkit-setup.md`.
5. Ask before cloning or installing any optional external toolkit.
6. Run helper scripts only after the toolkit path and runtime are ready, or apply the documented graceful fallbacks.
7. Treat the renderer import check as diagnostic; current external toolkit installs helper scripts, not `python -m pptify`.

## Runtime Setup

Use this only after the user approves runtime setup. Install `uv` first if it is missing; `uv` then installs the required Python version and creates the project virtual environment through `uv sync`, so a separate manual Python install is not required.

```powershell
uv python install 3.13     # managed Python for this project
uv sync                    # base project
uv sync --extra plugins    # add source ingestion and image helpers
```

If `uv` itself is not installed, read `references/toolkit-setup.md` and use the OS-specific bootstrap there only after consent.

## Runtime Readiness

Run this check before invoking helper scripts. It works from either the plugin root or the repository root.

```powershell
$toolingRoot = @("skills\pptify-tooling", "pptify\skills\pptify-tooling") |
	Where-Object { Test-Path (Join-Path $_ "scripts\README.md") } |
	Select-Object -First 1
$pythonCommand = if (Get-Command py -ErrorAction SilentlyContinue) { "py -3" } elseif (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { $null }

[pscustomobject]@{
	ToolingRoot = $toolingRoot
	Pyproject = Test-Path "pyproject.toml"
	Uv = [bool](Get-Command uv -ErrorAction SilentlyContinue)
	PythonCommand = $pythonCommand
}
```

## Workspace Detection

Run this check **before** invoking any plugin script. Do not assume the toolkit is present.

```powershell
# PowerShell
Test-Path "skills\pptify-tooling\scripts\README.md"
```
```bash
# bash / macOS / Linux
test -f skills/pptify-tooling/scripts/README.md && echo "present" || echo "missing"
```

**Decision table — act on the result before continuing:**

| Tooling scripts found | `pyproject.toml` found | Runtime found | Action |
|---|---|---|---|
| Yes | Yes | `uv` | Proceed with `uv run python <tooling-root>/scripts/...` commands |
| Yes | Yes | Python only | Run stdlib-only helpers with `python <tooling-root>/scripts/...`; ask before bootstrapping `uv` for dependency-managed helpers |
| Yes | No | Any | Use stdlib-only helpers when possible; for optional dependencies, ask whether to install the toolkit in a writable workspace or apply fallbacks |
| No | — | Any | **Read [`references/toolkit-setup.md`](references/toolkit-setup.md) now** (before responding), then ask whether to install the optional toolkit or apply graceful fallbacks |
| Yes | Yes | None | Apply no-install fallbacks first; if helper execution is essential, ask before installing `uv`, then run `uv python install 3.13` and `uv sync --extra plugins` |

**Optional toolkit install:**

Do not clone or install the external toolkit automatically. Ask the user before fetching code from `https://github.com/kimtth/agent-pptify-kit`.

If the user approves installation:

```powershell
# Clone into the workspace root (or a subdirectory if another project already occupies it)
git clone https://github.com/kimtth/agent-pptify-kit .
uv python install 3.13
uv sync --extra plugins
```

If the workspace root already belongs to a different project, ask the user where to place the toolkit before cloning.

**Graceful degradation — if install is not possible, apply these fallbacks:**

| Affected skill | Blocked capability | Fallback |
|---|---|---|
| `pptify-context-prep` | Document-to-markdown conversion, RAPTOR summary, design profile loading | Ask the user to paste source content directly; load `references/design-profiles.md` from `pptify-context-prep` for bundled design profile guidance |
| `pptify-visual-assets` | Icon search, image search, raster→SVG, infographic generation | Use `bbox` placeholder objects with descriptive `content.alt`; omit image objects rather than leaving them empty |
| `pptify-quality-gates` | Spec audit via `audit.py` | Apply the manual checklist rules in that skill; skip the `audit.py` output check |
| `pptify-deck-generation` | End-to-end PPTX render via `pptify` CLI | Stop and inform the user — PPTX generation requires the renderer; do not produce a partial artifact |

**No-install helper coverage:**

These helpers are safe to try with the detected plain-Python command (`py -3` on Windows when available, otherwise `python`) when `uv` is unavailable because they rely on the standard library for their default path: `design_context_catalog.py`, `audit.py`, `iconfy_search.py`, `raster_image_to_svg.py` in default embedded-raster mode, and `document_to_raptor_tree.py` with local deterministic embeddings. Dependency-managed helpers such as document conversion, web image crawling, vector tracing, and test runs should use `uv` or fall back gracefully.

**Renderer reality check:**

```powershell
# Diagnostic only; this currently fails in the external toolkit
uv run python -c "import pptify; print('renderer present')"
```

If the import fails with `ModuleNotFoundError: No module named 'pptify'`, the `python -m pptify` render command is unavailable. This is expected for the current external toolkit. Use standalone plugin scripts for all non-render steps, and do not claim that `uv sync` restores the renderer.

## Plugin Scripts

| Purpose | Command |
|---|---|
| Convert document to markdown | `uv run python skills/pptify-tooling/scripts/documents/document_to_markdown.py --source <file> --output-path out.md` |
| Build RAPTOR summary tree | `uv run python skills/pptify-tooling/scripts/documents/document_to_raptor_tree.py --markdown-path source.md --output-path summary.json --title "Title" --pretty` |
| List design profiles | `uv run python skills/pptify-tooling/scripts/design/design_context_catalog.py --list --pretty` |
| Load design profile context | `uv run python skills/pptify-tooling/scripts/design/design_context_catalog.py --profile fluent-ui-design-tokens --include-context --pretty` |
| Search web images | `uv run python skills/pptify-tooling/scripts/images/web_image_search.py --query "topic" --max-num 8 --pretty` |
| Search Iconify icons | `uv run python skills/pptify-tooling/scripts/images/iconfy_search.py --query governance --collection fluent --color 0078D4 --max-num 8 --pretty` |
| Raster to SVG | `uv run python skills/pptify-tooling/scripts/images/raster_image_to_svg.py --source logo.png --output-path logo.svg --pretty` |
| Generate infographic | `uv run python skills/pptify-tooling/scripts/images/text_prompt_to_infographic.py --provider azure-openai --size "1024x1024" --prompt "..." --output-path out.png --pretty` |
| Audit spec | `uv run python skills/pptify-tooling/scripts/audit/audit.py deck-spec.json --json` |
| Run tests | `uv run python -m unittest discover -s tests -v` |
