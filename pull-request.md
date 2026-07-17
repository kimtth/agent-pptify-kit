## Pull Request Checklist

- [x] I have read and followed the [CONTRIBUTING.md](https://github.com/github/awesome-copilot/blob/main/CONTRIBUTING.md) guidelines.
- [x] I have read and followed the [Guidance for submissions involving paid services](https://github.com/github/awesome-copilot/discussions/968).
- [x] My contribution adds a new instruction, prompt, agent, skill, workflow, or canvas extension file in the correct directory.
- [x] The file follows the required naming convention.
- [x] The content is clearly structured and follows the example format.
- [x] I have tested my instructions, prompt, agent, skill, workflow, or canvas extension with GitHub Copilot.
- [x] I have run `npm start` and verified that `README.md` is up to date.
- [x] I am targeting the `staged` branch for this pull request.

---

## Description

Adds the `pptify` plugin for PowerPoint deck authoring with GitHub Copilot. The plugin helps users plan, specify, review, and improve presentation decks through Copilot-native guidance rather than a bundled runtime generator.

This submission is refactored in response to feedback from https://github.com/github/awesome-copilot/issues/1848. The earlier version was reviewed as too specific for this repository and too dependent on external runtime code. This version narrows the contribution to repository-native Copilot assets:

- removed bundled PPTX runtime code, setup scripts, install steps, and external tool execution paths;
- moved content into the official `awesome-copilot` source layout with one top-level agent and five top-level skills;
- changed reference-deck analysis and visual/tooling guidance into documentation-only workflows;
- kept external tools optional and user-directed rather than installed, configured, or run by the plugin;
- added a plugin manifest that references the top-level source files instead of shipping a generated runtime artifact.

**Agent**

- `pptify-slides-builder` - guides the end-to-end PowerPoint deck workflow, including narrative strategy, slide planning, coordinate-explicit slide specification, visual direction, and quality review.

**Skills**

- `pptify-context-prep` - prepares narrative framework, source material, audience needs, constraints, and bundled design profiles before authoring a deck spec.
- `pptify-slide-spec` - helps author or repair coordinate-explicit deck specs, including layout groups, objects, bounding boxes, tables, images, lines, shapes, and collision-safe content.
- `pptify-visual-assets` - provides guidance for planning and placing icons, images, SVGs, infographics, and other visual assets in deck layouts.
- `pptify-reference-deck-analysis` - documents reference PPTX analysis workflows for extracting reusable structure, style, and layout signals from existing decks.
- `pptify-quality-gates` - validates and repairs deck specs and PPTX outputs against audit criteria such as collisions, overflow, hierarchy, asset layering, and reference-deck alignment.

Validation completed locally:

```powershell
npm run plugin:validate
npm run build
```

Both commands completed successfully, and `pptify` was validated as a plugin. The `pptify-*` skills also validate successfully. The current `staged` branch has an unrelated pre-existing `skill:validate` failure in `aws-cloudwatch-investigation` due to an invalid skill name.

---

## Type of Contribution

- [ ] New instruction file.
- [ ] New prompt file.
- [x] New agent file.
- [x] New plugin.
- [x] New skill file.
- [ ] New agentic workflow.
- [ ] New canvas extension.
- [ ] Update to existing instruction, prompt, agent, plugin, skill, workflow, or canvas extension.
- [ ] Other (please specify):

---

## Additional Notes

This PR is intended to address the #1848 maintainability concern directly: the plugin no longer bundles or runs the previous PPTX generation runtime. It now contributes reusable Copilot guidance for deck planning, slide specification, visual asset planning, reference analysis, and quality review.

### Preview Materials

The following sample decks demonstrate the kind of editable PowerPoint output that the workflow is designed to help users plan and review. They are examples only; they are not required runtime assets for this plugin.

**Preview: 60 layouts — current V3 native-object stress suite**

- [Office viewer - PPTX](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fkimtth%2Fpptify-kit%2Fmain%2Fdocs%2Fpptify-kit-stress-demo-v3.pptx)

![Contact sheet of all 60 layouts in pptify-kit-stress-demo-v3.pptx](https://raw.githubusercontent.com/kimtth/agent-pptify-kit/refs/heads/main/docs/preview/pptify-kit-stress-demo-v3-contact-sheet.png)

**Preview: 50 layouts**

- [Office viewer - PPTX](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fkimtth%2Fpptify-kit%2Fmain%2Fdocs%2Fpptify-kit-stress-demo-v2.pptx)

![Contact sheet of all 50 layouts in pptify-kit-stress-demo-v2.pptx](https://raw.githubusercontent.com/kimtth/agent-pptify-kit/refs/heads/main/docs/preview/pptify-kit-stress-demo-v2-contact-sheet.png)

**Preview: 81 layouts**

- [Office viewer - PPTX](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fkimtth%2Fpptify-kit%2Fmain%2Fdocs%2Fpptify-kit-stress-demo.pptx)

![Contact sheet of all 81 layouts in pptify-kit-stress-demo.pptx](https://raw.githubusercontent.com/kimtth/agent-pptify-kit/refs/heads/main/docs/preview/pptify-kit-stress-demo-contact-sheet.png)

---

By submitting this pull request, I confirm that my contribution abides by the [Code of Conduct](../CODE_OF_CONDUCT.md) and will be licensed under the MIT License.
