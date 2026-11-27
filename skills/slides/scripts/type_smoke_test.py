#!/usr/bin/env python3
"""Render synthetic layouts using isolated copies of each distributed skill.

Requires the same environment as common/scripts/build.py.
These fixtures test formatting and packaging, not the quality of real reports.
"""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


GROUP = Path(__file__).resolve().parents[1]
CASES = {
    "single-paper": (
        "slide-share",
        [
            ("Question and setup", """#twocol[
*Question*
- Can the proposed mechanism explain the target observation?
- Define the task before interpreting a result.
][
*Setup*
- Identify the compared conditions.
- Keep controls and outcome units explicit.
]"""),
            ("Evidence and interpretation", """#table(
columns: (1fr, 2fr),
[*Evidence role*], [*Explanation*],
[Setup panel], [Explain task and conditions before the outcome.],
[Result panel], [Read axes and distinguish observation from interpretation.],
)
This fixture contains no empirical results."""),
            ("Contribution and limits", """- Attribute the contribution to its source.
- Separate tested scope from proposed extensions.
- Keep unresolved questions explicit."""),
        ],
    ),
    "multi-paper": (
        "slide-share",
        [
            ("Selected studies and roles", """#table(
columns: (1fr, 1.4fr, 1.4fr),
[*Study label*], [*Role*], [*Comparison boundary*],
[Synthetic A], [Direct evidence], [One controlled setting],
[Synthetic B], [Boundary test], [A different task],
)"""),
            ("Explain before comparing", """#twocol[
*Study A*
- Explain its question and method.
- Identify its evidence boundary.
][
*Study B*
- Explain the different setting.
- Do not imply a shared benchmark.
]"""),
            ("Synthesis and discussion", """- Compare only along declared dimensions.
- Preserve source identity and incompatible conditions.
- Distinguish supported synthesis from hypotheses."""),
        ],
    ),
    "survey": (
        "slide-survey",
        [
            ("Scope and taxonomy", """#twocol[
*Organizing question*
- Which constraints distinguish approaches?
- This is a synthetic layout example, not a field survey.
][
*Classification axes*
- Representation
- Evaluation setting
- Resource constraints
]"""),
            ("Theme comparison", """#table(
columns: (1fr, 1.3fr, 1.4fr),
[*Route label*], [*Design dimension*], [*Evidence to inspect*],
[Route A], [Structured state], [Task and baseline comparability],
[Route B], [Learned state], [External validation],
)"""),
            ("Synthesis within scope", """- Separate established capabilities from missing comparisons.
- Qualify coverage and absence claims.
- Do not turn a topic overview into an obligatory proposal."""),
        ],
    ),
    "technical": (
        "slide-tech",
        [
            ("Problem and interface", """#table(
columns: (1fr, 2fr),
[*Contract*], [*Synthetic system example*],
[Input], [A validated request with a schema version],
[Output], [An auditable result or an explicit failure],
[Constraint], [No silent changes to source data],
)"""),
            ("Architecture and data flow", """#grid(
columns: (1fr, 24pt, 1fr, 24pt, 1fr, 24pt, 1fr),
align: center + horizon,
[#rect(inset: 12pt)[Input]], [$arrow.r$],
[#rect(inset: 12pt)[Validate]], [$arrow.r$],
[#rect(inset: 12pt)[Execute]], [$arrow.r$],
[#rect(inset: 12pt)[Audit]],
)

Arrows denote request flow. This is a conceptual fixture, not an implemented system."""),
            ("Key implementation contract", """#twocol[
*Interface*
#raw("validate(request) -> accepted | error", block: true)
][
*Invariants*
- Reject unsupported versions.
- Preserve original inputs.
- Report failure explicitly.
]"""),
            ("Validation and limits", """#table(
columns: (1fr, 1.5fr, 1.3fr),
[*Claim class*], [*Required evidence*], [*Fixture status*],
[Design], [Explicit architecture], [Conceptual only],
[Correctness], [Actual tests and inputs], [Not measured here],
[Performance], [Benchmark and environment], [Not measured here],
)"""),
        ],
    ),
}


def render_case(root, name, skill, pages):
    # Copy a complete skill, not a symlink to _shared or a sibling installation.
    installed = root / "isolated" / name / skill
    shutil.copytree(GROUP / skill, installed)
    deck = root / "decks" / name
    deck.mkdir(parents=True)
    shutil.copyfile(installed / "common/assets/typst-template/theme.typ", deck / "theme.typ")
    title = name.replace("-", " ").title()
    source = [
        '#import "theme.typ": *\n#show: theme\n',
        "#title-slide(config: config-page(footer: source-footer), extra: [\n",
        f"*{title} layout check*\n\nSynthetic fixture, not scientific evidence.\n",
        "#cite[Source: synthetic distribution test.]\n])\n",
        "#speaker-note[这是一份合成排版测试，不代表真实研究或系统验证。]\n",
    ]
    for heading, body in pages:
        source.extend([
            f"\n== {heading}\n\n{body}\n",
            "#cite[Source: synthetic distribution test.]\n",
            "#speaker-note[解释本页的结构、输入输出或比较条件；所有内容仅用于排版验证。]\n",
        ])
    (deck / "main.typ").write_text("".join(source), encoding="utf-8")
    subprocess.run(
        [sys.executable, str(installed / "common/scripts/build.py"), str(deck)],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True, help="new task-owned directory")
    args = parser.parse_args()
    root = args.output_dir.resolve()
    root.mkdir(parents=True, exist_ok=False)
    for name, (skill, pages) in CASES.items():
        render_case(root, name, skill, pages)
    print(f"PASS: four synthetic layouts built from standalone copies; inspect previews in {root / 'decks'}")


if __name__ == "__main__":
    main()
