---
title: "Visible but out-voted: in-context binding failures are query-time routing errors"
date: 2026-07-01
order: 3
authors: "Ravulapalli, M., et al."
meta: "Ravulapalli, M., et al."
status: "In preparation."
excerpt: "When a language model emits the wrong in-context binding, the correct binding is still decodable and still causally effective. The failure is in routing, not in representation."
tags:
  - Interpretability
  - In-context learning
  - Attention routing
  - Pythia
---

When a language model emits the wrong in-context binding, the correct binding
remains decodable and causally effective. The failure localises to query-time
attention routing and later-layer overwrite.

A developmental analysis over 70 pretraining checkpoints, across Pythia and
OLMo-2, shows that representation and use develop on different clocks.
