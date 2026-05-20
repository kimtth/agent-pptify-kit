# pptify-core

Agent Skills and workflow prompts for GitHub Copilot CLI, the VS Code GitHub Copilot extension, and generic coding agents live here. The old Python GitHub Copilot SDK provider has been removed. This workspace snapshot does not contain an importable `pptify/` core package or `python -m pptify` CLI.

Agents use the files in `skills/` and `workflows/` as guidance for choosing standalone plugin tools, authoring coordinate-explicit JSON or generation scripts, using source and asset plugins, and repairing layout issues. Restore the core renderer package before relying on historical render/analyze/extract CLI commands.

## Prompt Assets

The `skills/` directory uses the Agent Skills standard: each skill is a lowercase hyphenated directory with a required `SKILL.md` file containing YAML frontmatter with `name` and `description`.

The current skill set covers:

- PPTX tooling and plugin selection.
- JSON deck spec authoring.
- Source and reference PPTX ingestion.
- Source-backed predefined design templates and design-system context from `pptify-design`.
- Visual asset generation and placement.
- Production-ready slide structure rules.
- Audit-based quality gates.
- End-to-end deck generation workflow.

For GitHub Copilot project-level discovery, this repository also includes `.github/skills/pptify-pptx-generation/SKILL.md`, which points agents at the pptify deck-generation workflow and package-local skill set.

## E2E Workflow

1. Collect missing required workflow and artifact inputs with the VS Code prompt input dialog (`vscode_askQuestions` or equivalent) before creating files or running helpers.
2. For source-backed, URL-based, or multi-source decks, prepare a markdown corpus and RAPTOR summary with the document plugins before authoring slides. Use `pptify-plugin/extraction` helpers or package inspection when a reference deck or reconstruction path is needed.
3. Prepare design context with `pptify-plugin/design/design_context_catalog.py` for every new deck unless a user-provided brand guide or reference PPTX is the primary style source. Default to `fluent-ui-design-tokens` and record the style lock in `summary.design_context`; use `corazzon-pptx-design-styles` only when a broader modern style catalog is explicitly useful.
4. Ask GitHub Copilot CLI or the VS Code GitHub Copilot extension to generate `deck-spec.json` using the project skill and package-local skills.
5. If the core renderer package is restored, render the spec with `uv run python -m pptify deck-spec.json --out deck.pptx --audit deck-audit.json`. Otherwise build with the available PowerPoint generation path and keep plugin evidence/audits beside the PPTX.
6. Check the audit or package inspection for collisions, overflows, warnings, and design-context failures. Plain white, Calibri-only, bullet-heavy `python-pptx`-looking decks are not production-ready.

## Image Generation Access

For text-to-image or infographic generation, use `.env` for provider configuration and credentials. If `.env` is missing, create it from `.env.template` and ask the user to fill the required values directly in that file before running the helper. Do not ask the user to paste API keys, tokens, or connection strings into chat or a prompt input dialog.

For OpenAI image generation, configure `PPTIFY_IMAGE_PROVIDER=openai`, `OPENAI_API_KEY`, and optionally `OPENAI_IMAGE_MODEL` in `.env`. The helper defaults to `gpt-image-1` when the model is unspecified.

The image helper has no local fallback provider. Agents must record an attempt manifest with provider, model or deployment, auth mode, prompt path, output path, status, and error details when generation fails.

For Azure `gpt-image-2` or `gpt-image-2.0` infographic generation, configure these values in `.env`:

- `PPTIFY_IMAGE_PROVIDER=azure-openai`.
- `AZURE_OPENAI_ENDPOINT`, for example `https://<resource>.services.ai.azure.com/openai/v1`.
- `AZURE_OPENAI_IMAGE_DEPLOYMENT`, for example `gpt-image-2` or the user's exact deployment name.
- Image size, defaulting to `1024x1024`.
- Auth method: Azure CLI/Entra auth or API-key auth.
- `AZURE_OPENAI_TIMEOUT`, optional, defaulting to `300`.

Use Azure CLI/Entra auth by running `az login`. For API-key auth, fill `AZURE_OPENAI_API_KEY`, `AZURE_AI_API_KEY`, or `OPENAI_API_KEY` in `.env`. `.env` is git-ignored; never commit it.

Run the image helper with the collected non-secret values:

```powershell
Copy-Item .env.template .env
# Edit .env, then run:
uv run python pptify-plugin/images/text_prompt_to_infographic.py --provider azure-openai --size "1024x1024" --prompt "Cloud governance roadmap" --output-path infographic.png --pretty
```

For OpenAI image generation, run the helper with the collected non-secret values after the user confirms access is configured.

Example:

```powershell
uv run python pptify-plugin/images/text_prompt_to_infographic.py --provider openai --size "1024x1024" --prompt "Cloud governance roadmap" --output-path infographic.png --pretty
```
