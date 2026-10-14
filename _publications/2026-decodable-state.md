---
title: "Decodable In-Context State and Model Output Across Training"
date: 2026-09-25
order: 4
authors: "Ravulapalli, M., and Chadha, S. S."
pdf: "https://arxiv.org/pdf/2609.31401"
status: "Preprint on arXiv, September 2026."
excerpt: "We follow, across training, how well a probe can read a model's stored prompt facts, how the model answers, and how much steering helps."
---

Earlier work showed that a probe can read the correct link from a model's hidden
state on trials where the model answers wrong, and that steering toward the
probe's answer can repair some of those errors. Here we follow probe accuracy,
model output, and the effect of steering across public pretraining and
post-training checkpoints.

Probe accuracy rises during Pythia pretraining. The benefit of probe-guided
steering grows from negligible to larger at two model sizes. We also show why a
probe that decodes the right answer on errors cannot, on its own, prove that the
model discarded information its output needed.
