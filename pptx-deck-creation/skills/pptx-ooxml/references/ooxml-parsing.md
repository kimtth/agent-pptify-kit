# OOXML Parsing Reference

A `.pptx` is an Open Packaging Conventions ZIP archive. Resolve its relationship graph; do not assume sequential filenames.

| Need | Parts |
| --- | --- |
| Slide order | `ppt/presentation.xml`, `ppt/_rels/presentation.xml.rels` |
| Slide text and shapes | `ppt/slides/slideN.xml` |
| Layout, notes, images, charts | `ppt/slides/_rels/slideN.xml.rels` |
| Template geometry | `ppt/slideLayouts/`, `ppt/slideMasters/` |
| Colors and fonts | `ppt/theme/theme1.xml` |
| Notes and comments | `ppt/notesSlides/`, `ppt/comments/` |
| Media and embeddings | `ppt/media/`, `ppt/embeddings/` |

## Namespaces

- PresentationML: `http://schemas.openxmlformats.org/presentationml/2006/main`
- DrawingML: `http://schemas.openxmlformats.org/drawingml/2006/main`
- Office relationships: `http://schemas.openxmlformats.org/officeDocument/2006/relationships`
- Package relationships: `http://schemas.openxmlformats.org/package/2006/relationships`

## Result Guidance

For a read-only extraction, include slide number, relationship target, concatenated text, shape counts, notes, relationship types, and any OOXML-only markers (animations, comments, transitions, or unsupported shapes). For design context, retain theme color/font tokens without claiming a resolved RGB value when the source uses a scheme or system color.
