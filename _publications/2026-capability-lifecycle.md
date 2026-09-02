---
title: "The lifecycle of a capability: acquisition, retention, loss, and repair in continued pretraining"
date: 2026-08-01
order: 2
authors: "Ravulapalli, M., et al."
meta: "Ravulapalli, M., et al."
status: "In preparation, targeting ICLR 2027."
excerpt: "A preregistered campaign on OLMo-2, with frozen hash-pinned predictions filed before launch, tracking when a capability survives continued training and when it does not."
tags:
  - Continued pretraining
  - Preregistration
  - OLMo-2
  - Evaluation
---

A preregistered campaign on OLMo-2. Predictions were frozen and hash-pinned
before launch.

With zero occurrences of a capability's data in a 200M-token continued-training
window, the Adam `beta2` setting decides survival: 0.95 kills the capability and
0.999 preserves it, 3 runs of 3 in each case. The ability to *acquire* the
capability is installed by the stage-2 anneal rather than by stage-1 scale.

The resulting failures are invisible to standard benchmarks. Four non-target
benchmarks move under 1.1 points. The same failures are repairable in 64
updates.
