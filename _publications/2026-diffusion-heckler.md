---
title: "A Heckler in the Hidden State: Correctness Signals in Diffusion Language Models"
date: 2026-09-29
order: 5
authors: "Miglani, A., Chadha, S. S., Li, K., and Ravulapalli, M."
pdf: "https://arxiv.org/pdf/2609.36783"
status: "Preprint on arXiv, September 2026."
excerpt: "Diffusion language models write code by repeatedly filling in a partly masked sequence. We test whether their hidden activations encode whether the code is correct, and whether that signal can improve generation."
---

Across six diffusion models, linear probes tell passing code from failing code,
with the strongest signal generally beyond the early layers. Controls with small
changes to meaning support a link to correctness rather than surface style
alone.

The probes give no consistent advantage over the model's own confidence.
Steering along the probe's direction did not reliably improve generation in the
settings we tested, while steering the opposite way made it worse.
