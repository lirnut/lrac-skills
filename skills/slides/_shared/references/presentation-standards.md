# Shared presentation standards

## Defaults and user overrides

- Follow explicit user requirements first. Otherwise use English audience text, Chinese per-page speaker notes retaining technical terminology, and a restrained academic appearance.
- Use `@preview/sci-brain-slides:0.1.0` with its `academic` theme for all three presentation types. Keep the same visual defaults; choose page composition according to the explanatory job.
- Treat language, package, and layout as overridable defaults. Impose no default duration, slide count, background-page cap, or seconds-per-slide rule.
- Keep content in `main.typ`, appearance in `theme.typ`, and notes in per-page `#speaker-note[...]` blocks. The starter demonstrates formatting, not a mandatory storyline.

## Layout and attribution

- Use a neutral background, restrained accent colors, consistent type roles, and minimal decoration.
- Give each page one explanatory job. Keep titles visible and center body content vertically when appropriate.
- Choose a process, figure-plus-explanation, taxonomy, comparison, equation, architecture, or validation layout according to the content. Do not reduce all types to title-plus-bullets.
- Use concise source references in a fixed footer. Cite paper authors/year/section/figure/page, or technical source/version/file/run as appropriate. Keep extraction labels and audit prose out of audience text.
- Preserve source data and aspect ratios. Inspect actual labels and legends, not just image-box dimensions. Prefer original empirical panels; use clearly identified presenter-created diagrams for concepts and technical structure.
- Choose each summary's purpose: report a result, synthesize a theme, explain a bounded limitation, or bridge sections. Do not force every page to claim a gap.

## Revision and evidence boundaries

- Read the existing source and render it before editing. Preserve user work, accepted order, scientific qualifiers, and technical meaning.
- Treat spacing and font requests as local layout changes. Do not silently delete content, merge away panels, or redesign the storyline.
- Try whitespace and layout repairs before proposing a split or cut; obtain approval for substantive removal or restructuring.
- Do not mutate library records, source PDFs, repositories, or datasets merely to prepare slides.
- Require evidence for empirical claims and identify assumptions, interpretations, proposed designs, implementations, tests, and measurements separately.

## Notes, builds, and delivery

- Write complete editable notes that explain the actual figure or mechanism, not merely translate bullets. Include relevant axes, variables, actors, units, denominators, conditions, takeaways, and limits.
- Export notes and presenter metadata from source; do not maintain conflicting manual copies.
- Build into a fresh output directory. A successful compile and structural checks do not replace visual review or source auditing.
- During local iterations inspect changed pages, affected neighbors, and the contact sheet; after structural changes recheck numbering, cross-references, citations, and notes.
- Before final delivery inspect every page for unreadable figures, real font/glyph coverage, clipping, overflow, unexpected blank pages, footer clearance, and note leakage.
- Rebuild after the final edit and deliver the same reviewed revision: editable source, audience PDF, notes, previews, claim audit, and provenance where applicable.
- If evidence or artifact gates cannot pass, deliver only an explicitly labeled draft with blockers. Do not claim checks that were not performed.
- When asked what page N means, distinguish physical PDF page from displayed slide number and explain the actual content before editing unasked.
