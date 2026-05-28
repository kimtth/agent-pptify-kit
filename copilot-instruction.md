# pptify Agent Instruction

Use `./.agent` as the installed pptify home for generic coding agents.

After running `pptify install`, agents should read and use:

- `./.agent/pptify-policy.md` for developer-protection and quality rules.
- `./.agent/skills/pptify-*` for deck-generation skills.
- `./.agent/agents/pptify-deck-builder.agent.md` for the end-to-end deck-generation workflow.
- `./.agent/resources/design` for predefined design profiles and template context.
- `./.agent/scripts` for source ingestion, design context loading, visual assets, extraction, and audit tools.
- `./.agent/resources/env.template` for image-provider configuration when credentials are needed.

When image generation needs OpenAI or Azure OpenAI settings, create `./.agent/.env` from `./.agent/resources/env.template` and have the user fill secrets directly in that file. Do not ask for secrets in chat or prompt dialogs.

For every new generated deck, choose and load a `resources/design` profile before authoring slides unless a user-provided brand guide or reference PPTX is the primary style source. Default to `fluent-ui-design-tokens`; for developer decks use `primer-primitives`; for consulting/governance decks use `likaku-mck-ppt-design-skill`; use `corazzon-pptx-design-styles` only when a broader modern style catalog is explicitly useful. Record the selected profile and style lock in `summary.design_context`. Plain white, Calibri-only, bullet-heavy `python-pptx`-looking decks are not production-ready.

The supported runtime install surface is `./.agent`.
