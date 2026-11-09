# Scientific evidence and figure reading

## Source audit

Keep provenance out of audience prose but available in `claim-sources.md`:

| Slide/claim | Source/version | Section, PDF page, figure/panel | Conditions | Metric, unit, denominator | Evidence class and boundary |
|---|---|---|---|---|---|

Verify exact quotations and preserve their scope. Mark preprints and use the versions actually read. Distinguish physical PDF page from printed page numbers. Do not imply that authors reviewed or endorsed the slides.

Use the strongest appropriate wording, not the strongest available wording:

- Observation: “Under condition X, outcome Y increased.”
- Author interpretation: “The authors interpret this as …”
- Modeling assumption: “The model assumes …”
- Fitted explanation: “The fitted coefficient suggests …”
- Causal claim: require a design supporting that causal interpretation; predictive fit alone is insufficient.

Do not exaggerate a predecessor's limitations to motivate a new method. A feature absent from selected implementations is not impossible for the method family; missing controls differ from missing mechanisms. Distinguish a paper's result, the presenter's synthesis, a working definition, and a proposal. Representative studies do not establish field-wide absence, and richer behavior does not by itself establish greater realism or validity.

## Publication status and visible attribution

- When adding a venue or publication label, verify it against publisher pages, official proceedings, or conference records. The existence of an arXiv version does not establish preprint-only status.
- Distinguish main conference, Findings, Industry Track, Workshop, journal, accepted/online-first, and preprint. If unresolved, say publication status is unconfirmed rather than claiming the paper is unpublished.
- Record the verified venue/status and lookup date separately from the exact version read or used for figures. Check figure numbers and results before substituting a published version for a preprint.
- Make each core figure traceable by author/year and figure/panel ID, beside the figure or through an unambiguous citation key. Do not rely on a truncated footer title as its only attribution.

## Figure explanation card

Prepare these answers for each core figure, normally in speaker notes:

1. What question and experimental comparison does it address?
2. What are the axes, units, range, normalization, and baseline?
3. What are the colors, symbols, panels, error bars, and uncertainty definitions?
4. What does a point, line, heatmap row, or column represent?
5. What is the denominator: agents, groups, questions, trials, trajectories, or a conditional subset?
6. Which task, model, network, prompt, and round conditions apply?
7. What pattern should the audience notice, and what do authors infer?
8. What cannot be inferred?

For equations explain variables, signs, terms, assumptions, and fitting/evaluation separately. Do not imply an LLM explicitly optimizes a fitted energy merely because the analyst models its behavior that way.

## Common traps to prevent

- Allocation points are not percentages or percentage points.
- Probability from output logits is not necessarily empirical trial accuracy.
- Opinion-prediction accuracy is not objective-task correctness.
- One-step prediction with true current states differs from rollout using predicted states.
- A share of all trajectories is not a conditional correction rate among initially wrong groups.
- A no-sign-switch category permits changes in opinion magnitude.
- An average-opinion threshold is not automatically a vote-share threshold.
- Endpoint classification does not establish a monotonic path.
- Majority reversal says nothing about truth on a subjective question.
- Fitted influence of correct neighbors does not mean agents were told which neighbor was correct.
- Prompted fixed confederate responses are not reciprocal interactions with independently updating agents.

## Original figures and provenance

Render original PDF panels rather than redrawing data from memory. Crop only; do not alter numerical values, erase contradictory series, recolor findings, or fabricate missing panels. If creating a conceptual diagram, label it as presenter-created and distinguish it from empirical evidence.

For presenter-created process diagrams, make actors, component boundaries, the environment, arrow meanings, and feedback directions explicit. Avoid crossed or ambiguous connectors and accidental duplicate actors. Match method names to operations actually shown or implemented; branching trajectories alone do not establish tree search. Keep proposals visually and verbally separate from validated architectures or results.

Use the crop script with a JSON manifest:

```json
{
  "sources": {
    "paper-a": {"pdf": "papers/paper-a.pdf", "url": "https://example.org/paper-a", "version": "v1"}
  },
  "crops": [
    {"name": "paper-a-setup", "source": "paper-a", "page": 3, "rect": [0.1, 0.12, 0.9, 0.5], "figure": "Figure 1(a–b)"}
  ]
}
```

Resolve PDF paths relative to the manifest; use 1-based physical PDF pages and normalized rectangles relative to the visible rotated page, origin top-left. The script records source/output SHA-256 hashes and render parameters. It reads local PDFs only; obtain authorized sources first. Inspect every crop for cut-off axes, unreadable legends, misleading panel selection, and stray neighboring content. Respect reuse licenses.
