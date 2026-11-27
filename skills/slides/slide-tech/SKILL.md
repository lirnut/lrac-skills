---
name: slide-tech
description: Create and revise technical-report slides explaining a technology, algorithm, architecture, implementation, or system and its validation. Use for design reviews, implementation walkthroughs, technical evaluations, and “技术报告”“架构讲解”“算法实现汇报”“系统设计与验证”. Accept code, specifications, documentation, datasets, logs, and papers without requiring a literature review. Use slide-share for paper-centered talks and slide-survey for topic-wide route mapping.
---

# Technical Report Slides

Explain a technical problem, its solution, and what is actually implemented or verified. Do not confuse technical reporting with a progress checklist.

## 1. Establish the technical question

- Identify the audience and decision or understanding the report should support.
- Establish the problem, constraints, system boundary, maturity, source versions, and explicit output requirements.
- Use the communicative purpose, not paper count, to confirm the type. Keep the accepted type and scope during local revisions.
- Accept code, specifications, technical documents, experiments, datasets, and authorized logs. Do not require papers, a paper-selection matrix, or benchmark results that do not exist.

Read the common [presentation standards](common/references/presentation-standards.md), [production workflow](common/references/production-workflow.md), and [execution guide](common/references/execution.md).

## 2. Audit implementation and validation evidence

- Follow [evidence and figures](common/references/evidence-and-figures.md) and create `claim-sources.md` from the [blank audit](common/assets/source-audit-template.md).
- Link implementation claims to inspected versions and file/symbol locations; link measured claims to actual test or benchmark runs and conditions.
- Keep proposed design, inspected implementation, tested correctness, and measured performance distinct.
- Record runtime/hardware, workloads, metrics, baselines, repetitions, uncertainty, and evaluation limits when applicable.
- Report missing access or validation honestly. Do not execute expensive experiments, expose private code, or publish logs merely to fill slides without authorization.

## 3. Plan the technical explanation

Read [technical report strategy](references/technical-report.md).

Adapt the sequence to the report's purpose: problem and constraints → principles → design → key implementation → validation and tradeoffs → applicability and limits.
A conceptual report may stop at a clearly labeled design; a claim of deployed behavior or performance requires corresponding evidence.

- Use architecture/component diagrams for structure and data-flow or sequence diagrams for behavior.
- Explain algorithm steps, equations, interfaces, invariants, and failure handling where they matter.
- Use short readable code excerpts only to explain a consequential mechanism; keep full implementations out of audience slides.
- Use benchmark plots or acceptance matrices only when backed by actual results. Mark conceptual examples and synthetic fixtures explicitly.
- Keep rationale and tradeoffs visible; do not substitute module inventories or feature lists for an explanation.

## 4. Produce and verify

- Follow the common [Typst workflow](common/references/typst-workflow.md). Copy `common/assets/typst-template/` into a new deck directory and use the same theme as the other slide types.
- Keep editable diagrams, equations, and tables where possible. Preserve actual data and identify presenter-created diagrams separately from empirical figures.
- Explain inputs, outputs, arrow meanings, units, conditions, and limitations in the audience view or notes as needed.

```sh
python <skill-dir>/common/scripts/build.py <deck-dir>
python <skill-dir>/common/scripts/extract_figures.py <manifest.json> --output-dir <asset-dir>
```

Use the crop tool only for source PDFs; original technical diagrams need no PDF crop manifest.
Check dependencies, apply the three shared gates, and inspect every rendered page before final delivery.
Additionally confirm diagram-to-implementation consistency, traceable measurements, honest maturity labels, and reproducible validation conditions.
Deliver editable source, PDF, notes, previews, claim audit, and figure provenance where applicable. State what was inspected, tested, measured, or left unverified.
