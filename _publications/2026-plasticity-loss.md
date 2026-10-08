---
title: "Load-dependent loss of plasticity in small language models"
date: 2026-06-01
order: 4
authors: "Ravulapalli, M., et al."
status: "In preparation."
excerpt: "A small model that learns a skill and then loses it has a harder time relearning it than a model that never learned it at all."
---

We train small language models on a task where they have to link facts in their
prompt. If a model learns the skill and then loses it, it has a harder time
learning it again than a model that never learned it.

The ability to learn the skill also fades quickly once training stops asking for
it. The harder the task, the shorter the window in which the model can still
pick it up.
