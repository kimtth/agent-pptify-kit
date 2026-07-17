---
title: PPTX Deck Creation Architecture
description: Architecture for the editable, native-object PPTX deck creation plugin.
author: PPTX Deck Creation maintainers
ms.date: 2026-07-10
ms.topic: architecture
keywords:
  - PowerPoint
  - PPTX
  - python-pptx
estimated_reading_time: 4
---

## PPTX Deck Creation Architecture

This workspace is a VS Code Copilot plugin for creating editable PowerPoint
PPTX decks. The plugin directory is `pptify`.

## Plugin Components

- `pptify/.github/plugin/plugin.json` - VS Code/Copilot plugin metadata
- `pptify/agents/pptx-builder.agent.md` - Main agent for editable PPTX creation
- `pptify/skills/` - Guidance for narrative, specifications, assets, reference analysis, and quality checks
- `pptify/skills/pptx-reference-deck-analysis/` - Read-only reference-deck analysis and safe OOXML package inspection
  - extraction contract — slide structure, shapes, text, media
  - style-master contract — design, theme, colors, typography
  - `references/reference-deck-analysis-patterns.md` — documentation-only reference-deck analysis patterns, not runtime modules
  - `scripts/inspect.py` — compact relationship, theme, slide, notes, comments, animation, and media report
  - `scripts/unpack.py` — bounded safe extraction and formatted XML for raw-part review
  - `scripts/validate_package.py` — read-only package-integrity report for XML, relationships, content types, and orphaned parts

## Workflow

The agent guides users through a 6-step deck specification process:

1. **Understand the request** - Gather the audience, decision, narrative framework, and source facts
2. **Set the design direction** - Select the brand or design profile and document the visual rules
3. **Plan the deck** - Map the approved framework to a slide outline
4. **Author the specification** - Generate a coordinate-explicit JSON layout tree
5. **Build the PPTX** - Use a small task-specific `python-pptx` builder when a file is required
6. **Check and repair** - Validate the specification, PPTX package, geometry, accessibility, and rendered preview

## Extraction APIs

The `pptx-reference-deck-analysis` skill ships no importable code. It documents an
extraction and style-analysis contract that the agent implements on demand with
`python-pptx`; its small bundled scripts safely parse OOXML read-only when raw
package details are required. Historical Python snippets remain documentation only.
They are not packaged modules.

Reference templates are cataloged read-only by zero-based source slide index,
layout role, usable regions, placeholder roles, visual structures, and reuse
constraints. The catalog informs target layout choices but never authorizes
copying or mutation of the source deck.

## Editable Content Policy

The deck's title, message, data, labels, diagrams, and tables must be native
PowerPoint objects. Images may support a slide, but an image cannot be the
slide's only meaningful content. The plugin provides design guidance and
extraction contracts, not hosted infrastructure or a generic renderer.

## Data Contracts

Generated deck specs use explicit coordinates:

- Slide size, groups, object IDs, bounding boxes, roles, styles, z-order
- Text: explicit font size, color, alignment
- Shapes/lines: explicit fill, stroke, endpoints
- Images (object): `content.path` or `content.blob_base64`, plus `content.alt`
- Image provenance (separate manifest): provider, model, prompt path, status, error details
- Layout policy: safe margin, content bottom, footer top, and minimum gap
- Accessibility: document language, presentation title, and per-slide reading order
- Source lineage: source ID, evidence locator, claim type, and verification status
