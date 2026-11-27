---
name: slide-survey
description: Create and revise source-grounded survey presentations that map a research or technical topic, classify approaches, compare evidence, and synthesize progress, debates, and limits. Use for field overviews, literature-survey talks, route comparisons, and “调研报告”“领域综述”“技术路线比较”. Organize by questions and themes rather than paper count; use slide-share for study-centered explanation and slide-tech for a particular design or implementation.
---

# Survey Slides

Build a defensible map of a topic and its evidence, not a sequence of paper abstracts.

## 1. Define scope and organizing dimensions

- Establish the topic, audience, purpose, coverage boundary, available sources, and explicit constraints.
- Select by the goal of thematic synthesis, not the number of papers. Preserve the established scope during revisions.
- Choose questions, mechanisms, tasks, tradeoffs, or debates as organizing dimensions. Use chronology only when it explains meaningful change.
- Distinguish an exploratory overview from a systematic or scoping review; match search rigor and coverage claims to the actual process.

Read the common [presentation standards](common/references/presentation-standards.md), [production workflow](common/references/production-workflow.md), and [execution guide](common/references/execution.md).

## 2. Construct the evidence map

- Follow [paper selection](common/references/paper-selection.md) where papers are used and [evidence and figures](common/references/evidence-and-figures.md) for every source class.
- Track search scope, unresolved access gaps, representative selection, and each source's role in a theme. Do not imply exhaustive coverage from a few convenient examples.
- Inspect exact full texts or technical source versions before substantive claims; verify publication status separately from the version read.
- Create `claim-sources.md` using the [blank audit](common/assets/source-audit-template.md). Tie each synthesis to its underlying sources, conditions, and limitations.

## 3. Plan synthesis and page layouts

Read [survey strategy](references/survey-strategy.md).

Use a scope-appropriate progression: question and boundary → taxonomy or framework → representative approaches → fair comparisons → evidence-backed synthesis and open questions.
Do not force traditional-to-new-method chronology, a research-gap ending, or a personal research proposal.

- Use taxonomy diagrams, concept maps, theme matrices, or verified timelines to explain relationships.
- Give comparison tables explicit dimensions and readable columns; never rank incompatible benchmarks as if they shared conditions.
- Use representative figures to substantiate themes, not to turn the whole survey into repeated single-paper talks.
- Distinguish established capabilities, missing comparisons, disputed findings, and unvalidated generalizations.
- Make summaries perform a synthesis or transition rather than repeat the source list.

## 4. Produce and verify

- Follow the common [Typst workflow](common/references/typst-workflow.md) and reuse `common/assets/typst-template/` in a new output directory.
- Preserve the shared typography, footer, citations, and note conventions while replacing the starter's instructional content with a thematic storyline.
- Keep detailed comparison conditions and figure reading in per-page notes; retain qualifiers needed for accurate audience-visible claims.

```sh
python <skill-dir>/common/scripts/build.py <deck-dir>
python <skill-dir>/common/scripts/extract_figures.py <manifest.json> --output-dir <asset-dir>
```

Check dependencies as documented; compilation does not establish evidence quality or visual readability.
Apply the shared acceptance gates plus survey-specific checks: coverage matches the stated scope, categories are meaningful, comparisons are fair, absence claims are qualified, and synthesis follows from sources.
Inspect every rendered page before final delivery. Deliver editable source, PDF, notes, previews, claim audit, and provenance as applicable, clearly stating gaps or draft status.
