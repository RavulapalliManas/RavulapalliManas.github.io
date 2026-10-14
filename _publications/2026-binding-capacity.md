---
title: "In-Context Binding Capacity in Language Models"
date: 2026-09-24
order: 3
authors: "Ravulapalli, M., and Chadha, S. S."
pdf: "https://arxiv.org/pdf/2609.30634"
status: "Preprint on arXiv, September 2026."
excerpt: "How many facts can a language model keep straight from its prompt before it mixes them up? We measure this limit across open models and find that it grows with model size."
---

We give a model a list of assignments, such as which value belongs to which
item, and measure how many it can recall before it loses track. We measure this
on 12 models at or below 3B parameters, and in a sweep over 30 open models up to
12B.

The load at which recall falls halfway to chance grows with model size as a power
law (exponent 0.820, R² = 0.73). The broader sweep shows an eightfold range
linked to how the model was pretrained. The detailed curves show no detectable
effect of pretraining recipe once size is controlled, though few modern models
are in that fit.
