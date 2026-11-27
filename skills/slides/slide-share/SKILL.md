---
name: slide-share
description: Create and revise evidence-grounded group-meeting or journal-club slides explaining one paper or a selected set of papers. Use for single-paper deep dives, multi-paper sharing, original-figure explanations, and “组会论文分享”“单篇精读”“多篇论文汇报”. Select by the purpose of explaining studies, not PDF count; use slide-survey for topic-wide synthesis and slide-tech for technical designs or implementations.
---

# Paper Sharing Slides

Explain what the selected studies asked, how they worked, what the evidence shows, and where their conclusions stop.

## 1. Establish the sharing task

- Identify the audience, purpose, supplied papers and exact versions, expected output, and explicit constraints. Ask only necessary questions.
- Choose single-paper depth or multi-paper sharing by the explanatory purpose; do not infer a survey from a large number of PDFs.
- Retain the established purpose and paper order during local revisions. Confirm a substantial change of selection or storyline before implementing it.
- Work without prior decks, private libraries, or a particular harness. Resolve all resources from this installed skill's base directory.

Read the common [presentation standards](common/references/presentation-standards.md), [production workflow](common/references/production-workflow.md), and [execution guide](common/references/execution.md).

## 2. Select and audit evidence

- Read [paper selection](common/references/paper-selection.md) and [evidence and figures](common/references/evidence-and-figures.md).
- Inspect full texts, methods, captions, results, and relevant supplements; abstracts alone are insufficient for final claims.
- Record a one-paper brief or a multi-paper role matrix. Do not manufacture a common mechanism from shared terminology.
- Create `claim-sources.md` from the [blank audit](common/assets/source-audit-template.md), linking claims, panels, source versions, conditions, and interpretation limits.
- When sources are unavailable, report the gap and produce only an explicitly incomplete outline, not invented findings.

## 3. Build the study explanation

Read only the relevant sharing strategy:

- [Single paper](references/single-paper.md): problem → approach → results → interpretation and limits.
- [Multiple papers](references/multi-paper.md): shared question → paper roles → necessary deep dives → fair comparison and discussion.

Explain tasks and controls before results. Preserve the chain from setup and process to observations, aggregate results, and validation when needed. Use readable original figure panels, not decorative substitutes or full-page screenshots with tiny labels.

Choose a layout for each page's job: method process, equation with definitions, figure plus reading guide, or comparison matrix. Allocate depth by explanatory burden, not equal pages per paper or a fixed page quota.

## 4. Produce and verify

- Follow the common [Typst workflow](common/references/typst-workflow.md). Use `common/assets/typst-template/` in a new deck directory; change content structure for the selected strategy, not the shared visual theme.
- Keep source in `main.typ`, appearance in `theme.typ`, and complete Chinese speaker notes in per-page `#speaker-note[...]` blocks unless the user requests other languages.
- Run the bundled tools using the current environment:

```sh
python <skill-dir>/common/scripts/build.py <deck-dir>
python <skill-dir>/common/scripts/extract_figures.py <manifest.json> --output-dir <asset-dir>
```

The Typst reference documents dependencies and options. Structural checks are not scientific or visual certification.

Apply all three shared acceptance gates. Additionally check that the listener can reconstruct each study's task, method, key result, and scope; multi-paper conclusions must retain source identity and valid comparison conditions.
Inspect every rendered page before final delivery, and recheck changed pages and affected neighbors during local iterations.
Deliver editable source, audience PDF, notes, previews, claim audit, and figure provenance as applicable. State actual checks and remaining blockers honestly.
