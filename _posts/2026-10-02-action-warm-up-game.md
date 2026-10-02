---
title: "A short grid game helps a language model learn English, but does not pay for itself"
date: 2026-10-02 15:30:00 +0530
description: "Animals learn the structure of the world by acting in it. I gave a small language model a grid game with moves before it read English. Seeing its own moves helped a little, but the game cost more training than it saved."
tags: [language models, pre-pretraining, neuroscience]
---

**In short**

- Before training a small language model on English, I had it play a simple game: walk around a grid and remember what it saw.
- When the model could see its own moves, it later learned English a little better. When the moves were hidden, it learned English worse.
- The gain was consistent across runs, but small. The game cost more training than it saved.

## Why try this

Animals learn about the world by acting on it and seeing what changes. In a classic experiment, Held and Hein (1963) raised pairs of kittens in the dark and let them see only inside a striped drum. One kitten in each pair walked and turned a small carousel. Its partner rode in a basket on the same carousel and was moved in exactly the same way, so both saw the same sights. Only the walking kittens learned to use sight to guide their paws and to avoid a visual drop.

Acting helps for simple reasons. When you cause a change, you know where it came from. When you choose an action, you run a small experiment. Actions also follow rules that make a world easy to map. A step north and then east lands you where a step east and then north does. A step north is undone by a step south. A walk around a block brings you back to the start. Rules like these turn a pile of separate observations into a map. Machine-learning theory makes a similar point: Caselles-Dupré et al. (2019) argue that a learner cannot discover the symmetries of its world from still snapshots alone, and has to interact with it.

The brain seems to reuse this machinery for abstract thought. The hippocampal formation supports both finding your way through space and remembering how things relate. A model of that region, the Tolman-Eichenbaum Machine (Whittington et al., 2020), keeps knowledge of structure separate from what is seen, and that structural knowledge carries over from one environment to the next. People who navigate a space of abstract ideas show the same grid-like brain signal as people who navigate a real space (Constantinescu, O'Reilly and Behrens, 2016).

Language models learn from text alone, and text is passive. Yet language needs the same skills: keeping track of who has what, or of what was said a few sentences ago. A model has no body, but it can still get the structure that actions bring, as a record of moves and what they led to.

There is also a practical reason to try. Language models are expensive because they learn from enormous amounts of text. One way to save some of that text is a short warm-up on made-up data before the real training. Earlier warm-ups helped. Hu et al. (2025) warmed up a 1B-parameter model on a simple formal language of matching brackets. It reached the same loss, a standard measure of how well a model predicts text, with 33% fewer tokens. Lee et al. (2026) warmed up models on patterns from cellular automata and reported up to 1.6 times faster convergence. In both cases the model only watches patterns go by. It never acts.

So I built a warm-up in which the model moves through a world and has to keep track of where it is. Then I asked two questions. Does the warm-up make English cheaper to learn? And if it does, is it the moves that help?

## The game

![The game](/images/posts/action-warmup/fig0_game.png)

*A simplified example. The real games use grids from 4 x 4 to 12 x 12 and 256 possible labels.*

Each game takes place on a small grid whose edges wrap around. Every square gets a random label, and the labels change every game, so nothing can be memorised. The game is written as text: a label, a move, the next label, the next move, and so on.

The model is scored only on predicting the labels. It cannot predict the label of a square it has never visited. It can predict the label of a square it has visited before, but only by working out where it is from its moves and recalling what it saw there.

The control version hides the moves. Every move becomes the same blank token, and nothing else changes. If only the version with visible moves helps, the moves are what matter.

## The experiment

Every run used the same small language model, with 51M parameters. Each run had two stages:

1. An optional warm-up of 100M tokens.
2. 500M tokens of English web text (FineWeb-Edu), the same English in every run.

I compared five warm-ups against no warm-up:

| | Warm-up before English |
|---|---|
| A | None |
| B | Matching brackets, the formal language used by Hu et al. |
| C | The grid game, moves hidden |
| D | The grid game, moves shown |
| E | The grid game, with walks made of small loops |
| R | The grid game's layout filled with random labels, so there is nothing to learn |

I trained each setting three times, from different random starting points. I also trained the model with no warm-up on more and less English, from 300M to 800M tokens. That gives a yardstick: for any result, I can ask how much English the plain model needs to match it.

I wrote down my predictions before running anything. All 25 runs took about 18 hours on one rented GPU and cost about $46.

## Result 1: the moves matter

![Final loss relative to no warm-up](/images/posts/action-warmup/fig1_loss.png)

The score here is validation loss: how well the model predicts English it has never seen. Lower is better.

The game with visible moves (D) is the only warm-up that clearly beat no warm-up. It came out ahead in all three runs, by 0.021 on average. The same game with hidden moves (C) made the model worse, by 0.025 on average. Loop-heavy walks (E) came out level on average.

The gap between D and C is the clearest result. D beat C in every run, by 0.045 to 0.047. The only thing that separates them is whether the moves were visible.

## Result 2: the game does not pay for itself

![Does the warm-up pay](/images/posts/action-warmup/fig2_pay.png)

The game also costs training. The fair test is whether the same tokens would have done more good as English.

They would have. The model that played the game spent 100M tokens on the game and 500M on English. The plain model matches it after 517M to 529M tokens of English alone. So the 100M game tokens were worth only 18M to 29M tokens of English. Measured against each run's own no-warm-up partner, the figure is 28M to 45M. Either way, it falls well short of 100M. On average, every other warm-up did worse.

A shorter game looks better. With 30M game tokens, the model kept most of the gain and landed almost exactly at break-even. Its 30M game tokens were worth about 21M tokens of English. That comes from a single run, so treat it as a hint.

## Result 3: the model reuses what the game built

![Head ablation](/images/posts/action-warmup/fig3_heads.png)

During the game, some attention heads, the parts of the model that decide where to look, learn to look back at the earlier visit to the same square. I found the four strongest of these heads and switched them off in the finished model, after all its English training.

In two of the three runs, this hurt the model's English more than switching off any of 20 random sets of four heads. Its recall of facts given earlier in a prompt dropped by 5.6 and 9.8 percentage points. A noisier measure of learning from context also got worse. The same four heads mattered less in the model that never played the game. In the third run, the chosen heads behaved like random ones.

So in two of three runs, parts of the model built for the game were still doing useful work in language.

## Surprises

Loop-heavy walks (E) did worse than plain random walks. E scored higher on its own game, yet two of its three runs ended up worse at English than no warm-up.

Matching brackets (B) did worst of the structured warm-ups. This does not contradict Hu et al., because my setup differs from theirs: a smaller model, a fresh vocabulary table after the warm-up, and shorter inputs. A 30M-token bracket warm-up did no better.

A warm-up with nothing to learn (R) did real damage: its loss was 0.26 to 0.34 higher. These models mostly failed to form induction heads, the circuits a model uses to copy patterns from earlier in the text. I have not tested why.

## Limits

The model is small, and the shorter-game test was run once. The grammar test could not tell the five main settings apart. On the measure of learning from context, the plain model came out slightly ahead of D, the opposite of what I predicted. Every improvement in loss I measured is under 1% of the total loss.

## Next

The next step is to test shorter games: 10M, 20M, 30M and 50M tokens, three runs each. That is about 9 GPU-hours, or about $23. If a short game gives a real saving, it is worth trying on a larger model.

## References

- Held and Hein. *Movement-produced stimulation in the development of visually guided behavior.* Journal of Comparative and Physiological Psychology 56(5), 1963. [doi:10.1037/h0040546](https://doi.org/10.1037/h0040546)
- Caselles-Dupré, Garcia-Ortiz and Filliat. *Symmetry-Based Disentangled Representation Learning requires Interaction with Environments.* NeurIPS 2019. [arXiv:1904.00243](https://arxiv.org/abs/1904.00243)
- Constantinescu, O'Reilly and Behrens. *Organizing conceptual knowledge in humans with a gridlike code.* Science 352(6292), 2016. [doi:10.1126/science.aaf0941](https://doi.org/10.1126/science.aaf0941)
- Hu, Petty, Shi, Merrill and Linzen. *Between Circuits and Chomsky: Pre-pretraining on Formal Languages Imparts Linguistic Biases.* ACL 2025. [arXiv:2502.19249](https://arxiv.org/abs/2502.19249)
- Lee, Han, Kumar and Agrawal. *Training Language Models via Neural Cellular Automata.* 2026. [arXiv:2603.10055](https://arxiv.org/abs/2603.10055)
- Whittington, Muller, Mark, Chen, Barry, Burgess and Behrens. *The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation.* Cell 183(5), 2020. [doi:10.1016/j.cell.2020.10.024](https://doi.org/10.1016/j.cell.2020.10.024)
- Olsson et al. *In-context Learning and Induction Heads.* Transformer Circuits Thread, 2022. [link](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html)
