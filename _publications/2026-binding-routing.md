---
title: "Legible Failures: Detecting and Repairing In-Context Binding Errors"
date: 2026-09-10
order: 2
authors: "Ravulapalli, M., Chadha, S. S., and Hari, A. M."
pdf: "https://arxiv.org/pdf/2609.11216"
status: "Preprint on arXiv, September 2026."
excerpt: "A language model can give the wrong answer about which fact goes with which item in its prompt while the right answer can still be read from its hidden state. We use that hidden signal to detect and repair the errors."
---

Give a language model a prompt such as "the box holds the key, the bag holds the
coin", then ask what the bag holds. Sometimes it answers wrong. This is called a
binding error.

A wrong answer does not show whether the model lacked the information or held it
and failed to use it. Across 16 public models, a linear probe (a simple
classifier trained on the model's hidden state) recovers the correct link more
often than chance on the trials the model gets wrong. A score built from where
the probe and the model disagree detects failures better than the model's own
confidence. Steering the hidden state toward the probe's answer, with no correct
label given, raised accuracy on all eight models tested.
