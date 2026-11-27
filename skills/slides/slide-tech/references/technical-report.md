# Technical report strategy

## Frame the report around a question

Choose the relevant emphasis rather than imposing every section:

| Purpose | Explanatory emphasis |
|---|---|
| Principle or algorithm explanation | Inputs, assumptions, state/update rules, worked example, complexity, limits |
| Design review | Requirements, constraints, alternatives, architecture, interfaces, risks, validation plan |
| Implementation walkthrough | Actual versions, component responsibilities, control/data flow, key code, tests, failure handling |
| Technical evaluation | Evaluation question, workloads, baselines, protocol, measured outcomes, uncertainty, tradeoffs |

Identify the audience's background and decisions. Do not turn a technical report into a development diary. A design-stage report can be complete without benchmarks if its scope is explicit.

## Keep maturity and evidence separate

- Label proposals and expected benefits as unvalidated.
- Trace an implementation statement to actual code, configuration, or a versioned specification. A specification is not proof of runtime conformance.
- Describe a passing test as a check under stated inputs, not a proof of universal correctness.
- Use actual runs for performance claims. Record the code revision, environment, workload, metric, baseline, repetitions, and uncertainty when available.
- Distinguish a toy worked example from a benchmark and a demo from operational reliability.
- Explain missing tests or measurements as limits; do not insert plausible numbers.

## Select page layouts by technical job

### Problem and constraints

Use a compact requirements table or an annotated input/output example. State what success means before presenting a solution. Separate functional requirements from latency, cost, security, or deployment constraints.

### Architecture

Use a component diagram with explicit boundaries and responsibilities. Label arrows with data or operations. Distinguish implemented, external, optional, and proposed components using a consistent legend. Avoid accidental duplicate actors and crossed connectors.

### Behavior and algorithms

Use a numbered flow, sequence diagram, or state transition. Align equations with variable definitions and the relevant step. Explain initialization, update rules, termination, and failure behavior where applicable. A branching picture alone does not establish a search algorithm.

### Implementation

Pair a small code excerpt or interface signature with its role in the architecture. Identify the version and symbol in the audit. Keep secrets and proprietary details out of public artifacts. Prefer an explicit statement of inspected behavior to an unsupported claim that a component was tested.

### Validation and tradeoffs

Use a test/requirement matrix or readable plots. Show units and conditions, identify baseline fairness, and explain error bars. Separate correctness, speed, resource consumption, maintainability, and deployment constraints instead of declaring one method unconditionally best.

### Conclusions

Summarize the supported capabilities, costs, limits, and next validation needs. Do not imply planned work is complete or require a research-gap narrative.

## Technical acceptance checks

- Can the audience follow a representative input through the system?
- Do diagrams, terminology, and code excerpts agree with the inspected version?
- Are proposed, implemented, tested, and measured claims visibly distinguishable?
- Can a reader locate each substantive implementation or measurement source?
- Are important failure cases and applicability limits stated?
- Do notes explain the mechanism rather than merely read the labels?
