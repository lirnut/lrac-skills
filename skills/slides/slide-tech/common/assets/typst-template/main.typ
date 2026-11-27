#import "theme.typ": *
#show: theme

// This is an instructional starter, not an empirical presentation.
#title-slide(config: config-page(footer: source-footer), extra: [
  *A source-grounded presentation*

  Replace this text with the topic, source identities, versions, and validation status.
  #cite[Replace with verified source references.]
])
#speaker-note[
  第 1 页｜开场

  介绍报告问题和来源。这里是模板说明，不是研究或测试结论。
]

== Questions and sources

#table(
  columns: (1fr, 1.5fr, 1.5fr),
  [*Source or component*], [*Question*], [*Evidence*],
  [Short source or component name], [Actual question or requirement], [Study, implementation, or validation record],
)
#cite[Replace with source sections and pages.]
#speaker-note[
  第 2 页｜来源与问题

  说明各来源提供什么依据。按分享、调研或技术报告的目标重新组织页面，不要把模板当成固定故事线。
]

== Problem and approach

#twocol[
  *Problem*
  - State the question or requirement.
  - Define the phenomenon or system boundary.
][
  *Approach*
  - Explain the task and comparison.
  - Identify controls, interfaces, or outcome units as applicable.
]
#cite[Replace with Methods section and page.]
#speaker-note[
  第 3 页｜问题与方案

  先解释 task、实验条件和 metric，再进入结果。复杂设计应拆成更多页面。
]

== Evidence and validation

*Insert a provenance-tracked figure, diagram, or validation artifact here.*

- State only the result supported by that figure.
- Preserve the task, model, units, and relevant uncertainty.
- Separate interpretation, design assumptions, and observation.

#cite[Replace with original figure number, panel, and page.]
#speaker-note[
  第 4 页｜读图

  按顺序解释坐标轴、单位、颜色、分母与实验条件，再说明结果支持什么，以及不能推出什么。
]

== Conclusions and scope

- Attribute borrowed conclusions to their sources.
- State the tested scope and known limitations.
- Do not invent a unified causal mechanism.

#cite[Replace with Discussion and Conclusion locations.]
#speaker-note[
  第 5 页｜结论与范围

  总结有依据的结论及适用范围，区分设想、实现和验证。只有用户给出时长限制时才安排时间表。
]
