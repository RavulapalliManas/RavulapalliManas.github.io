---
title: "A warm-up game with actions helps a small language model, but not enough to pay for itself"
date: 2026-10-02 15:30:00 +0530
description: "A short warm-up game in which a small language model moves around a grid helps it learn English slightly, and only when it can see its own moves. At the dose I tested, the warm-up does not pay for itself."
tags: [language models, pre-pretraining, synthetic data]
---

I gave a small language model a short game to play before it read any English. In the game, the model moves around a grid and has to remember what it saw at each spot. When the model could see its own moves, it later learned English slightly better than a model with no warm-up. When the moves were hidden, it learned English worse. The gain is real and repeats across seeds. It is also too small: at the dose I tested, spending the same tokens on English would have done more good.

## Why try this

Training a language model costs tokens. One way to cut that cost is a short warm-up on synthetic data before the real training starts. Hu et al. (2025) warmed up a 1B model on a formal language of matching brackets and reached the same loss with 33% fewer tokens. Lee et al. (2026) warmed up models on neural cellular automata and reported up to 1.6x faster convergence.

In both cases the model watches structure go by. It never acts. Language often asks for something else: keep track of things as they change, and look up a fact by where or when you saw it. A model of the hippocampus called the Tolman-Eichenbaum Machine (Whittington et al., 2020) splits this into two parts. One part learns the structure of a space. The other links that structure to what is seen there.

So the question was simple. If the warm-up has actions that move through freshly labelled content, does the model learn English faster? And if it does, is it the actions that help?

## The game

![The game](/images/posts/action-warmup/fig0_game.png)

*The game, simplified. Real games use grids from 4 x 4 to 12 x 12 and 256 possible labels.*

Each game takes place in a small grid whose edges wrap around. Every spot gets a random label, and the labels are reshuffled at the start of every game, so the model cannot memorise them. The game is written as text: a label, a move, a label, a move, and so on.

The model is graded only on predicting the labels. The label at a new spot cannot be predicted. The label at a spot the model has visited before can be predicted, but only if the model does two things. It has to work out where it is by adding up its moves, and it has to recall the label it saw there earlier.

The key control hides the moves. Every move becomes the same blank token, and everything else stays identical. If the warm-up helps only when the moves are visible, the moves are doing the work.

## The setup

Every run trained the same 51M-parameter transformer. A run had two stages:

1. A warm-up of 100M tokens of synthetic data, or no warm-up.
2. 500M tokens of English web text (FineWeb-Edu), identical in every run.

I compared five warm-ups against no warm-up:

| | Warm-up |
|---|---|
| A | None |
| B | Matching brackets (k-Shuffle Dyck), using Hu et al.'s generator |
| C | The grid game with the moves hidden |
| D | The grid game with the moves shown |
| E | The grid game with walks built from small loops |
| R | The grid game's format filled with random labels |

Each condition ran with 3 random seeds. I also trained the no-warm-up model on 300M, 400M, 650M and 800M English tokens. Those runs give a ruler: any final loss can be converted into "how much English the plain model needs to reach it". I wrote down the predictions before the runs started.

All 25 runs fit on one rented GPU (an NVIDIA L40S) in about 18 hours, for about $46.

## The actions matter

![Final loss relative to no warm-up](/images/posts/action-warmup/fig1_loss.png)

The game with visible moves (D) is the only warm-up that clearly beat no warm-up. Its final loss was 0.021 nats lower on average, and it was lower in all three seeds. The same game with hidden moves (C) finished 0.025 nats higher than no warm-up. Loop-heavy walks (E) came out level on average, with one good seed and two bad ones.

The gap between them is the cleanest result in the study. D beat C by 0.047, 0.047 and 0.045 nats in the three seeds. The only difference between the two is whether the moves were visible.

## The warm-up does not pay for itself

![Does the warm-up pay](/images/posts/action-warmup/fig2_pay.png)

A lower loss is not enough. The warm-up costs tokens too, so the fair question is whether the same tokens would have done more good as English.

They would have. The game with moves cost 100M warm-up tokens plus 500M English tokens. The plain model reaches the same loss after 517M to 529M English tokens. So the 100M game tokens were worth only 18M to 29M English tokens. Measured against each seed's own no-warm-up run, the figure is 28M to 45M. Either way it is far short of 100M. On average, every other warm-up did worse.

A smaller dose looks better. A 30M-token game with moves kept most of the benefit and landed almost exactly on the break-even line. Its 30M game tokens were worth about 21M English tokens. That comes from a single seed, so it is a lead and not a result.

## The model keeps using what the game built

![Head ablation](/images/posts/action-warmup/fig3_heads.png)

During the game, some attention heads learn to look back from a revisit to the earlier visit of the same spot. I found the four strongest such heads at the end of the game. Then I switched them off in the finished model, after all the English training.

In two of three seeds, this hurt the model's English more than switching off any of 20 random sets of four heads. Recall of facts given earlier in a prompt dropped by 5.6 and 9.8 percentage points. The in-context learning score also got worse, though that score is noisy at this model size. The same four heads in the no-warm-up model mattered less. In the third seed, the selected heads were no different from random ones.

So in two of three seeds, heads built for the game still did work in language.

## What did not work

**Loop-heavy walks (E) transferred worse than plain random walks.** E scored higher on its own game, yet two of its three seeds ended up worse at English than no warm-up. The third seed matched the random-walk game.

**Matching brackets (B) were the worst structured warm-up.** This does not contradict Hu et al. My setup differed from theirs in three ways: a smaller model, a new embedding table after the warm-up, and a shorter context. A 30M-token bracket warm-up did no better than the 100M one.

**Random labels (R) did damage.** A warm-up with nothing to learn raised the final loss by 0.26 to 0.34 nats. Those models largely failed to form induction heads during English training, the circuits that copy patterns from earlier in the text. I have not tested why.

## Limits

This is a small study. The model has 51M parameters, and the dose test has one seed per point. The grammar test could not tell the five main conditions apart. On in-context learning, the plain model came out slightly ahead of D, the opposite of what I predicted. All of the gains I measured are fractions of a percent of the total loss.

## What I would do next

The next step is a dose sweep of the action game at 10M, 20M, 30M and 50M tokens, with three seeds each. That is about 9 GPU-hours, or about $23 on the same hardware. If a small dose gives a real net saving, the idea is worth testing on a larger model.

## References

- Hu, Petty, Shi, Merrill and Linzen. *Between Circuits and Chomsky: Pre-pretraining on Formal Languages Imparts Linguistic Biases.* ACL 2025. [arXiv:2502.19249](https://arxiv.org/abs/2502.19249)
- Lee, Han, Kumar and Agrawal. *Training Language Models via Neural Cellular Automata.* 2026. [arXiv:2603.10055](https://arxiv.org/abs/2603.10055)
- Whittington, Muller, Mark, Chen, Barry, Burgess and Behrens. *The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation.* Cell 183(5), 2020. [doi:10.1016/j.cell.2020.10.024](https://doi.org/10.1016/j.cell.2020.10.024)
- Olsson et al. *In-context Learning and Induction Heads.* Transformer Circuits Thread, 2022. [link](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html)

