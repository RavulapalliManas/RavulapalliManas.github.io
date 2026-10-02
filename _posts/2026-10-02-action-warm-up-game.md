---
title: "A short grid game helps a language model learn English, but it doesn't pay for itself"
date: 2026-10-02 15:30:00 +0530
description: "Animals learn the structure of the world by acting in it. I gave a small language model a grid game with moves before it read English. Seeing its own moves helped a little, but the game cost more training than it saved."
tags: [language models, pre-pretraining, neuroscience]
---

**In short:** Before training a small language model on English, I had it play a simple game: wander around a grid and remember what it saw. When the model could see its own moves, it went on to learn English a little better than a model that skipped the game. When the moves were hidden, it learned English worse. The effect showed up in every run, but it was small, and the game cost more training than it saved.

## Why a game with moves?

Animals learn about the world by acting on it and watching what changes. The classic demonstration is an experiment by Held and Hein (1963). They raised pairs of kittens in the dark and let them see only inside a striped drum. One kitten in each pair walked around, turning a small carousel; its partner rode in a basket on the same carousel and was moved in exactly the same way, so the two saw the same sights. Only the kittens that walked learned to use their eyes to guide their paws and to avoid a visual drop.

There are some simple reasons why acting helps. If you cause a change, you know where it came from, and every action you choose is a small experiment. Movement also follows rules that make a world easy to map. Going north and then east puts you in the same place as going east and then north. A step south undoes a step north, and a walk around the block brings you back where you started. Rules like these are what turn a pile of separate observations into a map. Machine-learning theory points the same way: Caselles-Dupré and colleagues (2019) argue that a learner can't discover the symmetries of its world from still snapshots, and has to interact with it.

The brain seems to reuse this machinery for abstract thought. The hippocampal formation supports both finding your way through space and remembering how things relate to each other. The Tolman-Eichenbaum Machine (Whittington et al., 2020), a model of this region, keeps knowledge of structure separate from what is actually seen, and that structural knowledge carries over from one environment to the next. And when people navigate a space of abstract ideas, their brains show the same grid-like signal they show when navigating a real space (Constantinescu, O'Reilly and Behrens, 2016).

Language models learn from text alone, and text is passive. Language still asks for the same skills, though: keeping track of who has what, or of what someone said a few sentences back. A language model doesn't have a body, but it can still be shown the structure that actions bring, as a written record of moves and what they led to.

There's a practical reason to try this too. Language models are expensive because they need enormous amounts of text, and one way to save some of it is a short warm-up on made-up data before the real training starts. Earlier warm-ups have worked. Hu et al. (2025) warmed up a 1B-parameter model on a simple formal language of matching brackets, and it reached the same loss (a standard measure of how well a model predicts text) with 33% fewer tokens. Lee et al. (2026) used patterns from cellular automata and reported up to 1.6 times faster convergence. In both cases, though, the model only watches patterns go by. It never acts.

So I built a warm-up in which the model moves through a world and has to keep track of where it is, and asked two questions. Does the warm-up make English cheaper to learn? And if it does, is it the moves that help?

## The game

![The game](/images/posts/action-warmup/fig0_game.png)

*A simplified example. The real games use grids from 4 x 4 to 12 x 12 and 256 possible labels.*

Each game takes place on a small grid whose edges wrap around. Every square gets a random label, and the labels are reshuffled for every game, so there's nothing to memorise. The game is written out as text: a label, a move, the next label, the next move, and so on.

The model is only scored on predicting the labels. There's no way to guess the label of a square it hasn't visited yet. For a square it has visited, the label is predictable, but only if the model works out where it is from its moves and remembers what it saw there.

In the control version, the moves are hidden: every move becomes the same blank token, and nothing else changes. If the game only helps when the moves are visible, then it's the moves doing the work.

## What I ran

Every run used the same small language model, with 51M parameters, trained in two stages: an optional 100M-token warm-up, followed by 500M tokens of English web text (FineWeb-Edu). The English was identical across runs.

I compared five warm-ups against no warm-up at all:

| | Warm-up before English |
|---|---|
| A | None |
| B | Matching brackets, the formal language used by Hu et al. |
| C | The grid game, moves hidden |
| D | The grid game, moves shown |
| E | The grid game, with walks made of small loops |
| R | The grid game's layout filled with random labels, so there is nothing to learn |

Each setting was trained three times from different random starting points. I also trained the no-warm-up model on more and less English, from 300M up to 800M tokens, which gives a yardstick: for any result, I can ask how much English the plain model would need to match it.

I wrote my predictions down before running anything. All 25 runs fit on a single rented GPU in about 18 hours, for about $46.

## Seeing the moves matters

![Final loss relative to no warm-up](/images/posts/action-warmup/fig1_loss.png)

The score here is validation loss, which measures how well the model predicts English it hasn't seen before. Lower is better.

The game with visible moves (D) was the only warm-up that clearly beat skipping the warm-up. It came out ahead in all three runs, by 0.021 on average. The same game with the moves hidden (C) made things worse, by 0.025 on average, and the loop-heavy walks (E) came out about level.

The gap between D and C is the cleanest result in the study. D beat C in every run, by 0.045 to 0.047, and the only difference between them is whether the model could see its moves.

## But it doesn't pay for itself

![Does the warm-up pay](/images/posts/action-warmup/fig2_pay.png)

The game isn't free. Those warm-up tokens cost training too, so the fair question is whether they would have done more good as English.

They would have. The model that played the game spent 100M tokens on the game and 500M on English, and the plain model matches it after 517M to 529M tokens of English alone. So the 100M game tokens were worth only 18M to 29M tokens of English. (Compared against each run's own no-warm-up partner, it's 28M to 45M. Either way, it's well short of 100M.) On average, every other warm-up did worse.

A shorter game looks more promising. With just 30M game tokens, the model kept most of the gain and landed almost exactly at break-even: those 30M tokens were worth about 21M tokens of English. That's from a single run, so I'd treat it as a hint for now.

## The model keeps what the game built

![Head ablation](/images/posts/action-warmup/fig3_heads.png)

During the game, some of the model's attention heads (the parts that decide where in the text to look) learn to look back at the earlier visit to the same square. I picked out the four strongest of these heads and switched them off in the finished model, after all of its English training.

In two of the three runs, this hurt the model's English more than switching off any of 20 random sets of four heads. Its recall of facts given earlier in a prompt dropped by 5.6 and 9.8 percentage points, and a noisier measure of learning from context got worse too. The same four heads mattered less in a model that never played the game. In the third run, though, the chosen heads behaved like random ones.

So in two of three runs, parts of the model that were built for the game were still doing useful work in language.

## What surprised me

The loop-heavy walks (E) did worse than plain random walks. E scored higher on its own game, yet two of its three runs ended up worse at English than no warm-up at all.

Matching brackets (B) did the worst of the structured warm-ups. That doesn't contradict Hu et al., because my setup was different from theirs: a smaller model, a fresh vocabulary table after the warm-up, and shorter inputs. A 30M-token bracket warm-up didn't do any better.

A warm-up with nothing to learn (R) did real damage, raising the loss by 0.26 to 0.34. These models mostly failed to develop induction heads, the circuits a model uses to copy patterns from earlier in the text. I haven't tested why.

## Caveats

This is a small model, and the shorter-game test was run only once. The grammar test couldn't tell the five main settings apart, and on the measure of learning from context, the plain model came out slightly ahead of D, the opposite of what I predicted. Every improvement in loss I measured is under 1% of the total loss.

## What's next

The obvious next step is to try shorter games, at 10M, 20M, 30M and 50M tokens with three runs each. That's about 9 GPU-hours, or roughly $23. If a short game gives a real saving, it'll be worth trying on a larger model.

## References

- Held and Hein. *Movement-produced stimulation in the development of visually guided behavior.* Journal of Comparative and Physiological Psychology 56(5), 1963. [doi:10.1037/h0040546](https://doi.org/10.1037/h0040546)
- Caselles-Dupré, Garcia-Ortiz and Filliat. *Symmetry-Based Disentangled Representation Learning requires Interaction with Environments.* NeurIPS 2019. [arXiv:1904.00243](https://arxiv.org/abs/1904.00243)
- Constantinescu, O'Reilly and Behrens. *Organizing conceptual knowledge in humans with a gridlike code.* Science 352(6292), 2016. [doi:10.1126/science.aaf0941](https://doi.org/10.1126/science.aaf0941)
- Hu, Petty, Shi, Merrill and Linzen. *Between Circuits and Chomsky: Pre-pretraining on Formal Languages Imparts Linguistic Biases.* ACL 2025. [arXiv:2502.19249](https://arxiv.org/abs/2502.19249)
- Lee, Han, Kumar and Agrawal. *Training Language Models via Neural Cellular Automata.* 2026. [arXiv:2603.10055](https://arxiv.org/abs/2603.10055)
- Whittington, Muller, Mark, Chen, Barry, Burgess and Behrens. *The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation.* Cell 183(5), 2020. [doi:10.1016/j.cell.2020.10.024](https://doi.org/10.1016/j.cell.2020.10.024)
- Olsson et al. *In-context Learning and Induction Heads.* Transformer Circuits Thread, 2022. [link](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html)
