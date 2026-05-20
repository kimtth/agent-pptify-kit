---
name: pptify-production-rendering
description: "Author production-ready PPTX slide structures for the current pptify plugin toolkit. Use when creating coordinate-explicit layout trees, editable PowerPoint primitives, semantic objects, shapes, tables, images, OOXML reconstruction evidence, or collision-safe slide layouts."
---

# PPTify Production Rendering

Use this skill when converting an approved deck plan into coordinate-explicit slide structures or generation code that can be validated with the available plugin tools.

- Author final coordinates directly in `layout_tree`; current plugin scripts will not choose layouts, measure browser boxes, or shrink text to fit.
- Use concise slide titles that fit the title bbox at the explicit font size.
- Keep each slide to one clear message and three to five major content groups.
- Split dense material across slides rather than relying on tiny fonts.
- Use restrained themes with explicit background objects, accent shapes, title colors, heading colors, body colors, muted colors, and source-backed metadata when a design profile is used.
- Translate design profile guidance into explicit objects, colors, spacing, typography, z-order, and bboxes.
- Use `classification: "layout_design"` for background bands, panels, dividers, and geometric ornaments.
- Use `classification: "content"` for meaningful text, tables, lines, and media.
- Supported shape names include `rect`, `round_rect`, `oval`, `triangle`, `diamond`, `hexagon`, `parallelogram`, `chevron`, `pentagon`, `trapezoid`, and arrow variants.
- Every object must include `kind`, `role`, `classification`, `content`, `style`, `bbox`, and `z_index`.
- Every text-bearing object and table must include `style.font_size` and `style.color`.
- Every line object must include `content.x1`, `content.y1`, `content.x2`, and `content.y2`.
- Every line object must include `style.line` and `style.line_width`.
- Every shape object must include `content.shape`, `style.fill`, and `style.line`.
- Use `z_index` intentionally: low values for backgrounds and decorations, higher values for text and foreground content.
- Represent charts as explicit editable shapes, lines, labels, and tables when practical, or as file-backed images when exact chart rendering is the asset requirement.
- Prefer generated primitives for new decks and OOXML reconstruction only when preserving a production source deck matters more than editability.
