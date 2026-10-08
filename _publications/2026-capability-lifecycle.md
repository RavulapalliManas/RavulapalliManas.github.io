---
title: "Can old dogs learn new tricks? Capability dynamics along pretraining"
date: 2026-08-01
order: 2
authors: "Ravulapalli, M., et al."
status: "Submitted to ICLR 2027. Under review."
excerpt: "When a team keeps training a language model, it has to choose the data, the starting checkpoint, and how much old data to mix back in. We test whether the usual signals, training loss and benchmark scores, point to the right choices."
---

When a team keeps training a language model, it has to choose the data, the
starting checkpoint, and how much old data to mix back in. These choices are
usually guided by the training loss and by benchmark scores.

We test whether those signals lead to the right choices. We take public OLMo-2
checkpoints and train each one further several times, changing one setting per
run. We judge each model by the answers it writes. We find cases where the usual
signals point to the wrong choice, and cases where runs that look the same on
loss and benchmarks get different questions right.
