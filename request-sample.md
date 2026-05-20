# Copilot Deck Request Template

Use this template when you want to ask Copilot to create a PowerPoint deck with pptify. Fill in the parts you know. If something is unknown, write `not sure` or `please recommend`.

## Copy/Paste Request

```markdown
Please create a PowerPoint deck from the request below.

Required inputs:
- Topic or deck title: <what the deck is about>
- Audience: <who will read or present this deck>
- Goal: <what the deck should explain, persuade, decide, teach, or summarize>
- Slide count: <exact number or range>
- Language: <language for slide text>
- Source material: <paste notes, list file paths, or write "none">
- Output needed: <deck spec only, PPTX deck, or both>

Content direction:
- Main message: <the single most important takeaway>
- Storyline or required sections: <ordered list, or "please propose">
- Must include: <specific topics, names, terms, metrics, dates, examples, quotes>
- Must avoid: <topics, claims, wording, visuals, sensitive details>
- Assumptions: <allowed / not allowed; if allowed, list reasonable assumptions separately>

Design direction:
- Tone: <executive, technical, sales, training, board-ready, workshop, informal, etc.>
- Visual style: <brand, reference deck, clean business, modern, dense report, simple teaching deck, etc.>
- Design context profile: <primer-primitives, fluent-ui-design-tokens, awesome-copilot-design-agents, reference deck, or please recommend>
- Color preference: <brand colors, light theme, dark theme, or "please recommend">
- Layout preference: <mostly one-column story, comparisons, grids/cards, roadmap/timeline, or "please recommend">
- Assets: <logos, images, icons, diagrams, infographic needs, or "none">
- Generated infographic provider/auth: <none, OpenAI model + key configured in terminal, or Azure endpoint + deployment + Azure CLI/Entra/API-key auth configured outside chat>
- Footer or confidentiality text: <text to show on slides, or "none">

Quality expectations:
- Keep slides readable and not overcrowded.
- Prefer one clear message per slide.
- Use concise slide text instead of paragraphs.
- Mark any assumptions clearly.
- If source material is insufficient, ask only the most important follow-up questions.
```

## Required Inputs

| Input | Why it is needed | Example |
|---|---|---|
| Topic or deck title | Defines the subject and likely title slide. | `Power Platform Admin Governance Roadmap` |
| Audience | Sets vocabulary, level of detail, and tone. | `CIO and platform admin leadership` |
| Goal | Tells Copilot what the deck must accomplish. | `Get approval for a 90-day governance plan` |
| Slide count | Controls scope and density. | `5 slides`, `8-10 slides` |
| Language | Controls slide text language. | `English`, `Korean`, `Japanese` |
| Source material | Grounds the content in facts. | `Use docs/source.md and the notes below` |
| Output needed | Clarifies what Copilot should produce. | `PPTX deck and editable deck spec` |

## Optional Inputs

| Input | When to provide it | Example |
|---|---|---|
| Main message | When there is a specific takeaway. | `Governance is now an operating model issue, not a tool issue.` |
| Storyline | When the slide order matters. | `Problem, current gaps, target model, roadmap, decision ask` |
| Required topics | When certain content must appear. | `DLP policies, environments, owner model, monitoring` |
| Required terms | When exact wording matters. | `Managed Environments`, `Center of Excellence`, `tenant isolation` |
| Metrics or dates | When numbers and timing matter. | `90 days`, `Q3 launch`, `reduce unmanaged apps by 40%` |
| Exclusions | When some topics or claims are off-limits. | `Do not mention headcount reductions` |
| Reference deck | When visual style or structure should match an existing deck. | `Use reference-style.pptx for tone and layout` |
| Design context profile | When you want a public predefined template or design system used as LLM context. | `Use primer-primitives`, `Use fluent-ui-design-tokens` |
| Brand guidance | When colors, logo, or voice are constrained. | `Use Microsoft blue, white background, restrained visuals` |
| Asset requests | When images, icons, diagrams, or infographics are needed. | `Add simple icons for policy, monitoring, ownership` |
| Generated infographic provider/auth | Required when asking for a model-generated infographic. Provide only non-secret values; configure keys or Azure login outside chat. | `Azure endpoint + gpt-image-2 + Entra auth` |
| Footer text | When every slide needs a source, date, or caveat. | `Internal draft - May 2026` |
| Appendix needs | When background material should be included but not in the main flow. | `Add hidden appendix with source summary` |

## Available Choices

### Goal Options

- `Inform`: summarize facts or current state.
- `Decide`: support a decision or approval.
- `Persuade`: make a case for a recommendation.
- `Teach`: explain a concept or process.
- `Report`: communicate progress, status, or metrics.
- `Plan`: show roadmap, milestones, dependencies, or next steps.

### Audience Options

- `Executive`: concise, decision-oriented, low technical detail.
- `Technical`: architecture, implementation, risks, dependencies.
- `Sales/customer`: benefits, outcomes, proof points, next steps.
- `Training/workshop`: step-by-step, examples, clear definitions.
- `Board/leadership`: strategic narrative, risk, investment, governance.
- `Operations`: process, ownership, workflow, metrics, repeatable actions.

### Tone Options

- `Executive`
- `Technical`
- `Board-ready`
- `Consulting-style`
- `Training`
- `Product pitch`
- `Operational review`
- `Neutral summary`

### Layout Preference Options

- `One-column story`: best for linear explanation.
- `Side-by-side comparison`: best for before/after, options, tradeoffs.
- `Grid/cards`: best for risks, pillars, benefits, capabilities, metrics.
- `Roadmap/timeline`: best for phases, milestones, rollout plans.
- `Process flow`: best for steps, operating models, ownership handoffs.
- `Dashboard/status`: best for KPIs, progress, issues, decisions.
- `Please recommend`: use when you want Copilot to choose per slide.

### Visual Style Options

- `Clean business`: restrained, readable, professional.
- `Executive report`: dense but organized, suitable for review meetings.
- `Modern product`: more visual, polished, lighter text.
- `Technical architecture`: diagrams, labels, clear structure.
- `Workshop/training`: simple examples, clear headings, approachable pacing.
- `Reference-matched`: follow an existing deck's rhythm, colors, and tone.

### Design Context Profile Options

- `primer-primitives`: source-backed GitHub Primer token context for developer/product decks.
- `fluent-ui-design-tokens`: source-backed Fluent UI token guidance for Microsoft, Teams, M365, and enterprise decks.
- `awesome-copilot-design-agents`: source-backed design-agent prompt context for visual hierarchy, UX discovery, and accessibility framing.
- `Reference deck`: analyze a PPTX you provide and use its style context.
- `Please recommend`: let Copilot choose from available source-backed profiles or ask for a reference.

### Asset Options

- `None`: text and simple shapes only.
- `Icons`: lightweight symbols for scanning.
- `Local images`: use image files you provide.
- `Web image suggestions`: ask Copilot to find candidate image sources.
- `Generated infographic`: ask for a generated visual summary, with OpenAI or Azure OpenAI provider details and auth mode configured outside chat.
- `Diagram`: ask for a process, architecture, or operating model diagram.

## Good Request Example

```markdown
Please create a PowerPoint deck from the request below.

Required inputs:
- Topic or deck title: Power Platform Admin Governance Roadmap
- Audience: CIO, platform owner, and Power Platform admin leadership
- Goal: Get approval for a 90-day governance roadmap
- Slide count: 6 slides
- Language: English
- Source material: Use `temp/power-platform-admin-governance.md`
- Output needed: PPTX deck and editable deck spec

Content direction:
- Main message: Governance needs a repeatable operating model, not one-off policy cleanup.
- Storyline or required sections: Title, why now, current gaps, target operating model, 90-day roadmap, decision ask
- Must include: DLP policies, environments, owner model, monitoring, admin responsibilities
- Must avoid: Budget numbers and individual team names
- Assumptions: Allowed, but list assumptions separately

Design direction:
- Tone: Executive and board-ready
- Visual style: Clean business, dense but readable
- Design context profile: fluent-ui-design-tokens
- Color preference: Microsoft blue accents on a white background
- Layout preference: Mix of comparison, cards, and roadmap/timeline
- Assets: Simple icons only, no stock photography
- Footer or confidentiality text: Internal draft - May 2026

Quality expectations:
- Keep slides readable and not overcrowded.
- Prefer one clear message per slide.
- Use concise slide text instead of paragraphs.
- Mark any assumptions clearly.
- If source material is insufficient, ask only the most important follow-up questions.
```

## Quick Checklist Before Sending

- Did I name the audience?
- Did I state the goal or decision?
- Did I give a slide count?
- Did I provide source material or permission to make assumptions?
- Did I list must-include and must-avoid items?
- Did I give style guidance or ask Copilot to recommend it?
- Did I say what output I need?