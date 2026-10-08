---
title: "Visible but out-voted: in-context binding failures are query-time routing errors"
date: 2026-07-01
order: 3
authors: "Ravulapalli, M., et al."
status: "In preparation."
excerpt: "When a language model links the wrong facts together from its prompt, the right link is still stored inside the model. The mistake happens when the model reads the answer out."
---

Give a language model a prompt such as "the box holds the key, the bag holds the
coin", then ask what the bag holds. Sometimes it answers wrong. This is called a
binding error.

We find that when the model makes this error, the correct link is still stored
inside it and can still be read out. The failure happens later, when the model
pulls the answer out of its memory of the prompt. We also follow this across
training, using public checkpoints of Pythia and OLMo-2, and find that storing
the link and using it develop at different times.
