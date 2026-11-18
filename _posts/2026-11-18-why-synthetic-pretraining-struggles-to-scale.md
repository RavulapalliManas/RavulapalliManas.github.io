---
title: "Why Synthetic Pre-Pre-Training Struggles to Scale"
date: 2026-11-18 23:19:15 +0530
description: "What a synthetic warm-up must buy to justify its compute, and what a shrinking loss gap can tell us about transfer."
tags: [language models, pre-pretraining, scaling]
---

**TL;DR.** A synthetic warm-up can improve loss at every fixed text budget and still become a worse use of compute. In a model we can solve exactly, this happens when synthetic training corrects the errors that language training learns quickly, while the remaining errors respond better to text. Above a calculable budget, every positive warm-up dose loses. My grid-walk runs give a smaller empirical version of the accounting problem. The long warm-up cost about 54 million English tokens in equivalent compute and bought the loss improvement of roughly 18–29 million against the scratch ladder. Whether the same mechanism explains the real runs is a question we can test.

## A training stage before training?

Imagine teaching a language model a small game before giving it a book. In the game, the model sees a world change according to rules and learns to predict what happens next. There are no characters to sympathise with and no plot to spoil. But there are dependencies: a change here affects what can happen there, and the answer to a question may depend on something observed many steps ago.

The hope is that this practice prepares the model for language. A model reading code needs to track a variable. A model reading a story may need to keep track of where an object was left. A model answering a question about a document needs to connect the question to information earlier in the context. These are not identical problems, but they give us a reason to ask whether a carefully chosen synthetic task might teach a useful ingredient of them.

This extra stage is called *pre-pre-training*. The first “pre” comes before the familiar pre-training on natural language; the second comes from the fact that researchers apparently felt one “pre” was insufficient. The idea is serious even if the name sounds like a loading screen for another loading screen.

The practical motivation is to reduce the text, compute, or time required to reach a useful language-modeling performance. The scientific motivation is different: synthetic worlds let us control what a model experiences, so they may help us understand which kinds of structure transfer. A result can matter for one goal and fail the other. If a warm-up improves the final model but costs more compute than extra language training, it is interesting evidence about learning, but it is not yet a training shortcut.

## What is an NCA, and why use one?

A cellular automaton is a grid whose cells change according to local rules. A cell's next state depends on its current state and those of nearby cells. Repeat the update and local interactions can produce patterns that travel, interact, and change over time. In a *neural* cellular automaton, a neural network specifies the local update rule.

[Lee and colleagues](https://arxiv.org/html/2603.10055v2) generate sequences from many such systems, represent their states as tokens, and train a language model to predict them. The model can encounter different rules in different sequences. The appeal is that the data contain temporal and spatial dependencies without the meanings, facts, and word frequencies of English. If some training transfers to language after the model's token embeddings are replaced, something beyond a shared vocabulary must be involved.

That still leaves a large gap between *something transfers* and *we know exactly what transferred*. A model may exploit regularities in NCA sequences without learning a general algorithm for inferring arbitrary hidden rules. The paper studies attention and finds evidence consistent with useful transferable structure. Those observations motivate interventions; they do not, on their own, identify the full computation that causes a later language gain.

## Does the benefit disappear with scale?

The results depend on which corpus and budget you choose. The OpenWebText and FineWeb-Edu comparisons in the revised NCA paper make this unusually clear.

In the November 2026 revision of the NCA paper, the authors report an OpenWebText perplexity improvement over scratch of 8.6% for a 400-million-parameter model and 5.8% for a 3-billion-parameter model. On FineWeb-Edu, the reported improvement goes in the other direction: 4% at 1.6 billion parameters and 6% at 3 billion, with the language budget also scaled. The 3-billion-parameter FineWeb-Edu run retains a perplexity advantage through 98 billion language tokens. These are relative perplexity comparisons in the authors' settings, not estimates of a universal scaling law. [Source: Lee and colleagues, Figure 3 and Section 5.1.](https://arxiv.org/html/2603.10055v2)

Those comparisons change several things together. Model size, the amount and kind of language data, synthetic dose, and training recipe can all matter. When the gap changes, it is tempting to blame the largest model in the room. But size is not the only suspect.

[**Rethinking Pre-pretraining**](https://arxiv.org/html/2610.40051v1), by Stern and colleagues, gives a strong reason to be careful. In their reproduction of an NCA setup, they recover a perplexity gain under the original initialization. Changing the embedding initialization improves the scratch baseline more and makes the two results indistinguishable in that comparison. They did not retune the NCA dose under that alternative initialization in the reproduction, so this does not establish the best possible NCA result under it.

The same study then tests several synthetic curricula under shared compute budgets. Across its tested regimes, synthetic pre-pre-training does not beat allocating that compute to natural-language training on validation loss. Its search is not exhaustive: for example, the larger compute settings receive a reduced hyperparameter search, and the tested synthetic shares do not cover every possible schedule. Those limits matter, but so does the result. A method must compete with the best practical alternative, not merely with the first baseline we happened to train.

The two papers therefore give us a productive tension, not a verdict that one experiment can simply erase the other. Architecture, initialization, data, optimizer, budget and selection differ. The task is to find out which differences change the conclusion.

## What my grid walks add to the puzzle

I arrived at a related question from a different synthetic world. In my [earlier experiment](/writing/2026/10/action-warm-up-game/), a small model saw records of walks on a grid. The labels at locations changed between episodes. On a revisit, the model could benefit from remembering an earlier label and using the intervening moves to determine whether it had returned.

The model did not choose the moves. It read traces that had already been generated. That distinction matters: this was a test of learning from action information, not an experiment in active exploration.

The main comparison used a 51-million-parameter model. One condition saw the direction of each move; another saw the same kind of walks with directions hidden. After the synthetic stage, the token embeddings were reinitialized and the models trained on the same amount of English. Across three seeds, the visible-move condition had lower final English validation loss than both the hidden-move condition and the no-warm-up baseline. The visible-versus-hidden gap was about 0.045–0.047 nats.

[![The English validation loss of visible-move and hidden-move grid warm-ups for three seeds](/images/posts/action-warmup/paired-loss.svg)](/images/posts/action-warmup/paired-loss.svg)

*Each line connects one seed across conditions. Lower loss is better. The [plotted values](/images/posts/action-warmup/paired-loss.csv) come from the experiment's score summary.*

The comparison suggests that the information provided by moves matters in this recipe. It does not isolate a single spatial computation: hiding the directions also makes the synthetic prediction problem harder, changing the learning signal. Nor does it show that an NCA model works the same way. The experiment is a useful analogy with its own controls, not an NCA replication.

There is a second clue. I identified attention heads that looked from revisits toward earlier visits during the game, then disabled them after English training. In two of three seeds, disabling those heads harmed recall and the in-context probe more than any of 20 sampled random head sets. In the third, the effect was not clearly separated from random sets. This tells us that some heads selected during synthetic training matter to the final model in these tests. It does **not** show that those heads caused the warm-up's language-loss advantage, or that the same computation survived unchanged.

Even the less convenient observations are informative. Loop-heavy walks improved the grid task but generally transferred worse than ordinary walks. A random-label control hurt later language performance. More synthetic practice, or better performance on the synthetic task, is not automatically more useful practice for language.

## The break-even condition

Suppose I train a scratch model and a warm-started model on the same amount of English. The warmed model gets a lower validation loss. How much extra text would the scratch model need to reach that loss? Call that amount the warm-up's **effective transfer**, measured in language tokens. Hernandez and colleagues use this idea to measure transfer from text to Python. Here it lets us price a synthetic stage in the same units as its alternative. [*Scaling Laws for Transfer*, Section 1.2.](https://arxiv.org/html/2102.01293)

Fix the model size and language training recipe. Let <math><mi>D</mi></math> be the number of language tokens, <math><mi>S</mi></math> the number of synthetic tokens, and <math><mi>κ</mi></math> the ratio of their training costs per token, synthetic over language. Write <math><msub><mi>L</mi><mn>0</mn></msub></math> for scratch validation loss and <math><msub><mi>L</mi><mi>w</mi></msub></math> for warm-started validation loss. If the scratch curve falls strictly over the relevant range and reaches the warmed loss, define the extra text <math><mi>δ</mi></math> by

<math display="block" aria-label="Scratch loss at D plus delta equals warmed loss at D and S">
  <msub><mi>L</mi><mn>0</mn></msub><mo>(</mo><mi>D</mi><mo>+</mo><mi>δ</mi><mo>)</mo>
  <mo>=</mo><msub><mi>L</mi><mi>w</mi></msub><mo>(</mo><mi>D</mi><mo>,</mo><mi>S</mi><mo>)</mo><mo>.</mo>
</math>

At that loss, scratch costs the equivalent of <math><mrow><mi>D</mi><mo>+</mo><mi>δ</mi></mrow></math> language tokens. The warmed run costs <math><mrow><mi>D</mi><mo>+</mo><mi>κ</mi><mi>S</mi></mrow></math>. Subtract the two. The warm-up wins on training compute exactly when

<math display="block" aria-label="Effective transfer delta exceeds the cost of the synthetic stage kappa S">
  <mi>δ</mi><mo>&gt;</mo><mi>κ</mi><mi>S</mi><mo>.</mo>
</math>

This also gives a **loss threshold**. With the compute spent on the warm-up, the scratch model could have processed another <math><mrow><mi>κ</mi><mi>S</mi></mrow></math> tokens. Call the observed loss gain <math><mi>G</mi><mo>=</mo><msub><mi>L</mi><mn>0</mn></msub><mo>(</mo><mi>D</mi><mo>)</mo><mo>−</mo><msub><mi>L</mi><mi>w</mi></msub><mo>(</mo><mi>D</mi><mo>,</mo><mi>S</mi><mo>)</mo></math>. The warm-up wins if that gain exceeds what the same compute would have bought on the scratch curve.

<math display="block" aria-label="The observed gain must exceed the loss gain from spending the warm-up budget on language">
  <mi>G</mi><mo>&gt;</mo>
  <msub><mi>L</mi><mn>0</mn></msub><mo>(</mo><mi>D</mi><mo>)</mo><mo>−</mo>
  <msub><mi>L</mi><mn>0</mn></msub><mo>(</mo><mi>D</mi><mo>+</mo><mi>κ</mi><mi>S</mi><mo>)</mo><mo>.</mo>
</math>

This form is useful when inversion is unstable. A flat scratch curve makes a tiny change in loss look like a large change in effective tokens. If I can run scratch at the full equivalent budget, I can compare losses there directly. If I only have a bracket of scratch runs, I have to report how I interpolated between them.

### The grid runs, with the warm-up on the bill

[![Across three seeds, the 100M-token warm-up cost the equivalent of 54M English tokens and matched 18–29M extra English tokens. The single 30M run cost 16M and matched 21M.](/images/posts/synthetic-pretraining/grid-compute-break-even.png)](/images/posts/synthetic-pretraining/grid-compute-break-even.png)

*The scratch reference is a single-seed ladder of independently trained runs. The cost uses the study's estimated training FLOPs, with a smaller output vocabulary during the synthetic stage. [Endpoint data](/images/posts/synthetic-pretraining/grid-endpoints.csv).*

In seed zero, the 100-million-token warm-up took the held-out loss from 3.67214 to 3.65663 at the same English budget. The scratch ladder puts the equal-compute target at 3.64351, so the warm-up would have needed about 0.0286 nats of improvement. It delivered about 0.0155. The result cleared the first comparison and fell short in the second.

Against the scratch ladder, the estimated compute penalty is about 5–7% across the three long runs. The shorter warm-up comes out about 0.9% ahead in its one run. I also recalculated the study's paired checkpoint comparison in FLOPs. It asks how much compute a warm-started model has spent when it first reaches its paired scratch run's final loss. The long warm-ups range from a 1.9% penalty to a 2.5% saving on that measure. The short run saves 3.7%.

The paired comparison uses three different loss targets and allows a partly trained model to stop before it reaches the end of its learning-rate schedule. The ladder compares run endpoints, but its scratch reference comes from just one seed. The long warm-up consistently falls short against that reference. A claim about savings across training schedules needs a stronger baseline curve and a replicated short dose.

The result also leaves room for a different objective. If unique English text is scarce, the right comparison may be another pass over the same text. If generating or procuring data is costly, the accounting should include that too. Here I am comparing training arithmetic for one model size and one loss target. Stern and colleagues actually made repeated text a baseline and found it stronger than their tested synthetic curricula under that constraint. [*Rethinking Pre-pretraining*, Section 5.](https://arxiv.org/html/2610.40051v1)

### When trying a larger dose can help

Fix a target loss and let <math><msub><mi>δ</mi><mi>∗</mi></msub><mo>(</mo><mi>S</mi><mo>)</mo></math> be the number of language tokens saved at that target by a synthetic dose of size <math><mi>S</mi></math>. The target stays fixed as I change the dose. If the benefit starts at zero and has diminishing returns, its initial slope bounds what every later dose can buy:

<math display="block" aria-label="For a concave dose response, language tokens saved at dose S are at most the initial slope times S">
  <msub><mi>δ</mi><mi>∗</mi></msub><mo>(</mo><mi>S</mi><mo>)</mo>
  <mo>≤</mo><msup><msub><mi>δ</mi><mi>∗</mi></msub><mo>′</mo></msup><mo>(</mo><msup><mn>0</mn><mo>+</mo></msup><mo>)</mo><mi>S</mi><mo>.</mo>
</math>

The inequality follows because a concave curve lies below its initial tangent. If the initial slope is at or below <math><mi>κ</mi></math>, **no positive dose can beat scratch** under these assumptions. If the initial slope is higher, a short warm-up can pay while longer ones lose. The first doses matter more for this decision than the point where the curve finally plateaus.

This is a conditional result. A computation might only emerge after a minimum amount of practice, producing a dose response that rises slowly and then steepens. The grid experiment has too few doses and seeds to establish either shape. To discriminate between them, I would add small doses around the origin and enough intermediate doses to detect an onset, measuring every arm at the same loss target.

## A shrinking loss gap can come from a permanent head start

Take the simplest model of transfer. Suppose the warm-up moves the model a fixed distance along the scratch learning curve, so the same positive <math><mi>δ</mi></math> works throughout language training. For a power-law curve with floor <math><msub><mi>L</mi><mi>∞</mi></msub></math>, scale <math><mi>A</mi></math>, and exponent <math><mi>α</mi><mo>&gt;</mo><mn>0</mn></math>, this gives

<math display="block" aria-label="Scratch loss equals a floor plus A times D to the negative alpha. Warm-started loss equals scratch loss at D plus delta.">
  <mtable columnalign="left" rowspacing="0.5em">
    <mtr><mtd>
      <msub><mi>L</mi><mn>0</mn></msub><mo>(</mo><mi>D</mi><mo>)</mo><mo>=</mo>
      <msub><mi>L</mi><mi>∞</mi></msub><mo>+</mo><mi>A</mi><msup><mi>D</mi><mrow><mo>−</mo><mi>α</mi></mrow></msup><mo>,</mo>
    </mtd></mtr>
    <mtr><mtd>
      <msub><mi>L</mi><mi>w</mi></msub><mo>(</mo><mi>D</mi><mo>,</mo><mi>S</mi><mo>)</mo><mo>=</mo>
      <msub><mi>L</mi><mn>0</mn></msub><mo>(</mo><mi>D</mi><mo>+</mo><mi>δ</mi><mo>)</mo><mo>.</mo>
    </mtd></mtr>
  </mtable>
</math>

Taking the difference and expanding in <math><mfrac><mi>δ</mi><mi>D</mi></mfrac></math> gives the following approximation once the language budget is much larger than the head start:

<math display="block" aria-label="The loss gap is approximately A alpha delta divided by D to the power alpha plus one">
  <msub><mi>L</mi><mn>0</mn></msub><mo>(</mo><mi>D</mi><mo>)</mo><mo>−</mo>
  <msub><mi>L</mi><mi>w</mi></msub><mo>(</mo><mi>D</mi><mo>,</mo><mi>S</mi><mo>)</mo>
  <mo>≈</mo><mfrac><mrow><mi>A</mi><mi>α</mi><mi>δ</mi></mrow><msup><mi>D</mi><mrow><mi>α</mi><mo>+</mo><mn>1</mn></mrow></msup></mfrac><mo>.</mo>
</math>

As the curve flattens, the same horizontal distance buys less vertical improvement. Relative perplexity improvement shrinks too, since it is one minus the exponential of the negative loss gap. This is a counterexample to interpreting a shrinking perplexity advantage as evidence of forgetting. It uses a power-law illustration of the kind used in language scaling work, with a constant shift imposed as a hypothesis. [Hoffmann and colleagues, Section 3.3.](https://arxiv.org/html/2203.15556)

The absolute compute saved in this model is equivalent to <math><mrow><mi>δ</mi><mo>−</mo><mi>κ</mi><mi>S</mi></mrow></math> language tokens. It stays constant. The **fraction** saved at matched loss is

<math display="block" aria-label="Fraction of scratch compute saved equals delta minus kappa S divided by D plus delta">
  <mfrac><mrow><mi>δ</mi><mo>−</mo><mi>κ</mi><mi>S</mi></mrow><mrow><mi>D</mi><mo>+</mo><mi>δ</mi></mrow></mfrac><mo>.</mo>
</math>

[![On an illustrative power-law curve, both the loss gap and the percentage compute saving shrink with more language training even though the absolute token saving is constant.](/images/posts/synthetic-pretraining/fixed-head-start.png)](/images/posts/synthetic-pretraining/fixed-head-start.png)

*Illustrative curves. The head start and the warm-up cost are held fixed.*

A fixed warm-up can therefore keep saving the same absolute amount of compute and still become negligible as a share of a much longer run. To keep saving a fixed percentage as the language budget grows, the effective transfer that remains after paying for the warm-up must grow with the budget. Conversely, an actual reversal, from saving compute to costing more, needs something besides the flattening in this model. The effective head start might shrink, the baseline might improve, or the training recipe might change. This argument varies language exposure at a fixed model size. It makes no prediction about how the head start changes with parameter count.

There is a practical falsification test. Estimate the horizontal shift on an early, prespecified part of the curves. Use the scratch curve and that one shift to predict the later warmed loss. If the prediction misses beyond independent training-run variation, a constant shift is inadequate for that recipe. When both curves are nearly flat, compare the predicted and observed losses directly. The uncertainty on the inverse, measured in tokens, can be large even when the uncertainty in loss is small.

## Four explanations for a shrinking advantage

Suppose a carefully controlled experiment finds a smaller language-loss gap after more training. What could that mean? At least four explanations deserve to compete. They can coexist, and none is established by a shrinking gap alone.

**1. The scratch model catches up.** The warm-up may accelerate the acquisition of a useful capability that language training can also teach. In this picture, the NCA model keeps the capability, but the scratch model gradually acquires a functionally comparable one. A smaller performance gap need not mean the early model forgot anything.

**2. Later training changes access to the early capability.** A model may retain information from synthetic training but stop using it, use it through a different pathway, or lose task performance altogether. These are different outcomes. A decline on the original synthetic task is evidence of declining behaviour on that task; it does not by itself prove that a specific circuit was erased.

Stern and colleagues observe that performance on the synthetic distributions deteriorates after the switch to language. Interleaving synthetic examples preserves that performance in their experiment, but does not establish a statistically clear improvement in language validation loss. Keeping a skill and making that skill useful for language are two separate hurdles.

**3. The curriculum runs out of useful signal.** More trajectories do not necessarily mean more transferable structure. The revised NCA paper finds that the relationship between dose and downstream benefit depends on the state alphabet: the smallest tested alphabet continues improving over the explored budgets, while larger alphabets plateau or decline. That is evidence of dose and generator dependence, not a direct count of distinct algorithms the model has learned.

I wrote to Seungwook Han to ask whether larger models might need larger synthetic doses. The published dose results make the next step clear: vary the generator and dose independently, rather than assuming that one fixed token budget is fair at every model size. A plateau could reflect redundancy, difficulty, optimization, or mismatch with the target domain; the curve alone cannot pick a winner.

**4. The comparison rewards a weak starting point.** Synthetic training changes weights before language training. Some of its apparent benefit may overlap with improvements available from initialization, learning-rate schedules, or optimizer choices. That is why the Stern initialization result matters. The NCA authors also compare against first-order-statistics and mimetic initialization controls and report remaining gains. These controls address particular alternatives; neither study has ruled out every other initialization or training recipe.

## A model in which the warm-up helps and still loses

The break-even test tells us whether to pay for a warm-up. It leaves open how a method can clear that test at one budget and fail it at another. For that, suppose the synthetic task and the language task agree on the best answer. Give them the same starting point and let them differ in which errors they correct fastest. This is a deliberately favourable model of transfer. By giving both tasks the same optimum, we can ask what different learning rates do on their own. Wu and colleagues study shared-predictor transfer with finite-sample SGD. Buna, Liu and Rebeschini study fixed-budget allocation for approximating the update between two ridge optima. Here the readout is final language loss, and both tasks share their optimum. [Wu et al., Section 2.](https://arxiv.org/abs/2208.01857) [Buna, Liu and Rebeschini, Sections 2–3.](https://arxiv.org/html/2609.16262v1)

### Start with two ways of seeing the same answer

Take a linear predictor with squared loss and a shared teacher <math><msup><mi>w</mi><mo>∗</mo></msup></math>. An input with feature vector <math><mi>x</mi></math> has label <math><msup><mi>x</mi><mo>⊤</mo></msup><msup><mi>w</mi><mo>∗</mo></msup></math>. If the current parameter error is <math><mi>ε</mi><mo>=</mo><mi>w</mi><mo>−</mo><msup><mi>w</mi><mo>∗</mo></msup></math>, the squared prediction error is <math><msup><mrow><mo>(</mo><msup><mi>x</mi><mo>⊤</mo></msup><mi>ε</mi><mo>)</mo></mrow><mn>2</mn></msup></math>. Averaging over inputs gives the two population losses:

<math display="block" aria-label="Language loss is one half the error weighted by the language second moment. Synthetic loss uses the synthetic second moment.">
  <mtable columnalign="left" rowspacing="0.5em">
    <mtr><mtd>
      <msub><mi>F</mi><mi>ℓ</mi></msub><mo>(</mo><mi>w</mi><mo>)</mo><mo>=</mo>
      <mfrac><mn>1</mn><mn>2</mn></mfrac><msup><mi>ε</mi><mo>⊤</mo></msup><msub><mi>H</mi><mi>ℓ</mi></msub><mi>ε</mi><mo>,</mo>
    </mtd></mtr>
    <mtr><mtd>
      <msub><mi>F</mi><mi>s</mi></msub><mo>(</mo><mi>w</mi><mo>)</mo><mo>=</mo>
      <mfrac><mn>1</mn><mn>2</mn></mfrac><msup><mi>ε</mi><mo>⊤</mo></msup><msub><mi>H</mi><mi>s</mi></msub><mi>ε</mi><mo>.</mo>
    </mtd></mtr>
  </mtable>
</math>

The matrices are the input second moments for language and synthetic data. Give both matrices the same orthonormal eigenvectors. You can get this setting with independent features of different variances in each corpus. A feature that varies often gets a larger weight in that corpus's loss. It also gets a stronger corrective gradient. Write <math><msub><mi>λ</mi><mi>i</mi></msub></math> for the language eigenvalue of direction <math><mi>i</mi></math> and <math><msub><mi>μ</mi><mi>i</mi></msub></math> for its synthetic counterpart. Take both to be positive.

Under gradient flow, training subtracts the gradient continuously. The language error in direction <math><mi>i</mi></math> obeys <math><msub><mover><mi>ε</mi><mo>˙</mo></mover><mi>i</mi></msub><mo>=</mo><mo>−</mo><msub><mi>λ</mi><mi>i</mi></msub><msub><mi>ε</mi><mi>i</mi></msub></math>. Its solution multiplies the starting error by <math><msup><mi>e</mi><mrow><mo>−</mo><msub><mi>λ</mi><mi>i</mi></msub><mi>t</mi></mrow></msup></math> after language training time <math><mi>t</mi></math>. Write <math><msub><mi>a</mi><mi>i</mi></msub></math> for direction <math><mi>i</mi></math>'s initial contribution to the language loss, half its language eigenvalue times its squared starting error. Squaring the error gives the factor of two in the loss exponent.

A synthetic warm-up of duration <math><mi>u</mi></math> first contracts the very same error at rate <math><msub><mi>μ</mi><mi>i</mi></msub></math>. The contractions multiply. At equal language exposure, therefore, the warmed loss in every direction is the scratch loss times <math><msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><msub><mi>μ</mi><mi>i</mi></msub><mi>u</mi></mrow></msup></math>. Every direction with initial error benefits. In particular, a shrinking aggregate gap in this system needs no loss of an acquired skill.

### Make the two runs spend the same amount

Now fix total budget <math><mi>T</mi></math> in units of language training time. Let one unit of synthetic flow cost <math><mi>κ</mi></math> units of language flow. This ratio applies to the idealized dynamics. In a Transformer experiment it must be measured for the actual recipe. Scratch gets language time <math><mi>T</mi></math>. With synthetic duration <math><mi>u</mi></math>, the warmed run gets <math><mi>T</mi><mo>−</mo><mi>κ</mi><mi>u</mi></math> of language. Multiply the two contractions and collect the terms that depend on <math><mi>u</mi></math>. Define <math><msub><mi>r</mi><mi>i</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>i</mi></msub><mo>−</mo><mi>κ</mi><msub><mi>λ</mi><mi>i</mi></msub></math>. The matched-compute prediction is

<math display="block" aria-label="Warm loss at a fixed total budget is the sum of the remaining scratch loss per direction times an exponential in the synthetic rate advantage and dose.">
  <mi>L</mi><mo>(</mo><mi>T</mi><mo>,</mo><mi>u</mi><mo>)</mo><mo>=</mo>
  <munder><mo>∑</mo><mi>i</mi></munder>
  <msub><mi>a</mi><mi>i</mi></msub>
  <msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><msub><mi>λ</mi><mi>i</mi></msub><mi>T</mi></mrow></msup>
  <msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><msub><mi>r</mi><mi>i</mi></msub><mi>u</mi></mrow></msup><mo>.</mo>
</math>

The sign of <math><msub><mi>r</mi><mi>i</mi></msub></math> gives the comparison that matters. A positive synthetic learning rate can still come with a negative <math><msub><mi>r</mi><mi>i</mi></msub></math>. In that direction the synthetic stage learns something useful, but the language updates it displaces would have learned more. At fixed compute, the benefit depends on **which errors remain** and **which dataset corrects those errors faster per unit of compute**.

To see whether more synthetic data can rescue a losing run, define the remaining scratch loss in direction <math><mi>i</mi></math> at budget <math><mi>T</mi></math> as <math><msub><mi>b</mi><mi>i</mi></msub><mo>=</mo><msub><mi>a</mi><mi>i</mi></msub><msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><msub><mi>λ</mi><mi>i</mi></msub><mi>T</mi></mrow></msup></math>. Differentiate the matched-compute loss with respect to dose:

<math display="block" aria-label="The slope at zero dose is minus twice the sum of remaining scratch losses times the rate advantages. The second derivative is nonnegative.">
  <mtable columnalign="left" rowspacing="0.5em">
    <mtr><mtd>
      <msub><mi>L</mi><mi>u</mi></msub><mo>(</mo><mi>T</mi><mo>,</mo><mn>0</mn><mo>)</mo><mo>=</mo>
      <mo>−</mo><mn>2</mn><munder><mo>∑</mo><mi>i</mi></munder><msub><mi>b</mi><mi>i</mi></msub><msub><mi>r</mi><mi>i</mi></msub><mo>,</mo>
    </mtd></mtr>
    <mtr><mtd>
      <msub><mi>L</mi><mrow><mi>u</mi><mi>u</mi></mrow></msub><mo>(</mo><mi>T</mi><mo>,</mo><mi>u</mi><mo>)</mo><mo>=</mo>
      <mn>4</mn><munder><mo>∑</mo><mi>i</mi></munder>
      <msub><mi>b</mi><mi>i</mi></msub><msubsup><mi>r</mi><mi>i</mi><mn>2</mn></msubsup>
      <msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><msub><mi>r</mi><mi>i</mi></msub><mi>u</mi></mrow></msup><mo>≥</mo><mn>0</mn><mo>.</mo>
    </mtd></mtr>
  </mtable>
</math>

The loss is convex in dose. If the slope at zero is nonnegative, the loss can only stay the same or rise as we add synthetic training. **Zero is a global optimum over all feasible doses.** If the slope is negative, a small positive dose improves loss. The best interior dose is where the slope rises to zero. Otherwise the best dose is at the upper budget bound. This proves the dose result in this model. Real training could violate convexity, for example if useful transfer starts only after the model has learned a prerequisite.

### Why an optimal dose can go to zero

Take a fast language direction and a slow one. Denote them by <math><mi>f</mi></math> and <math><mi>s</mi></math>. Suppose the fast direction favours synthetic updates, so <math><msub><mi>r</mi><mi>f</mi></msub><mo>&gt;</mo><mn>0</mn></math>, while the slow direction favours language, so <math><msub><mi>r</mi><mi>s</mi></msub><mo>&lt;</mo><mn>0</mn></math>. At zero dose the sign depends on the ratio of the fast direction's benefit to the slow direction's cost. After simplification the ratio is

<math display="block" aria-label="The ratio of the fast benefit to the slow cost decays exponentially with the budget.">
  <mfrac>
    <mrow><msub><mi>a</mi><mi>f</mi></msub><msub><mi>r</mi><mi>f</mi></msub></mrow>
    <mrow><msub><mi>a</mi><mi>s</mi></msub><mo>|</mo><msub><mi>r</mi><mi>s</mi></msub><mo>|</mo></mrow>
  </mfrac>
  <msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><mo>(</mo><msub><mi>λ</mi><mi>f</mi></msub><mo>−</mo><msub><mi>λ</mi><mi>s</mi></msub><mo>)</mo><mi>T</mi></mrow></msup><mo>.</mo>
</math>

If this ratio starts above one, set it equal to one and solve for the budget. This gives

<math display="block" aria-label="The budget threshold equals the log of the initial ratio divided by twice the difference of language rates.">
  <msub><mi>T</mi><mo>∗</mo></msub><mo>=</mo>
  <mfrac>
    <mrow><mi>ln</mi><mo>(</mo>
      <mfrac>
        <mrow><msub><mi>a</mi><mi>f</mi></msub><msub><mi>r</mi><mi>f</mi></msub></mrow>
        <mrow><msub><mi>a</mi><mi>s</mi></msub><mo>|</mo><msub><mi>r</mi><mi>s</mi></msub><mo>|</mo></mrow>
      </mfrac><mo>)</mo>
    </mrow>
    <mrow><mn>2</mn><mo>(</mo><msub><mi>λ</mi><mi>f</mi></msub><mo>−</mo><msub><mi>λ</mi><mi>s</mi></msub><mo>)</mo></mrow>
  </mfrac><mo>.</mo>
</math>

Below that budget, a small dose helps. At the threshold and above it, convexity rules out a compute win at any positive dose. The location of an interior optimum follows from setting the full dose derivative to zero. The log of the ratio above is divided by <math><mn>2</mn><mo>(</mo><msub><mi>r</mi><mi>f</mi></msub><mo>−</mo><msub><mi>r</mi><mi>s</mi></msub><mo>)</mo></math>, and the result is clipped to the feasible interval from zero to <math><mi>T</mi><mo>/</mo><mi>κ</mi></math>.

[![In a shared-optimum toy model, the same fixed synthetic dose always helps at equal language exposure. At equal total compute it starts ahead and falls behind. The optimal dose drops to zero once slow errors dominate.](/images/posts/synthetic-pretraining/two-mode-transfer.png)](/images/posts/synthetic-pretraining/two-mode-transfer.png)

*Calculated example. The upper curves use a fixed dose and share the same scratch reference. The lower curve optimizes the dose separately at each total budget. Its rising segment is capped by the available compute, which can all go to synthetic data in this shared-teacher example. All parameters are illustrative.*

Both models approach the same solution. The warm-up always helps at equal language exposure. It loses at equal compute once the errors it corrects especially cheaply have mostly disappeared. Reverse the advantage so that synthetic training corrects the slow direction more cheaply and an equal-compute benefit can persist to arbitrarily long budgets in this model. The hypothesis about which errors the warm-up improves therefore has a consequence you can look for. The equations vary budget at fixed model size. A claim about parameter scaling would require measuring how initial errors and relative rates change across sizes.

The model also gives a test of timing. With shared eigenvectors and the same optimum, any interleaving with the same total time on each dataset gives the same final error. Within a direction it only changes the order of multiplying exponentials. If replay changes final loss under matched budgets and controlled schedules, at least one assumption fails. Differing optima, interactions between directions, optimizer state, and changing features can all produce order effects. Replay alone would not tell us which caused one.

### Where the power law and the head start come from

The model also contains the constant-shift story as a special case. Suppose every synthetic rate is the same multiple <math><mi>m</mi></math> of the corresponding language rate, so <math><msub><mi>μ</mi><mi>i</mi></msub><mo>=</mo><mi>m</mi><msub><mi>λ</mi><mi>i</mi></msub></math>. An interval <math><mi>u</mi></math> of synthetic training is then exactly equivalent to <math><mi>m</mi><mi>u</mi></math> units of language training. This is true direction by direction, so it is true for the total loss. At equal compute the replacement buys a net head start of <math><mo>(</mo><mi>m</mi><mo>−</mo><mi>κ</mi><mo>)</mo><mi>u</mi></math>. The size of the loss gap can change with budget, but its sign cannot reverse. The reversal in the two-direction example comes from variation in synthetic usefulness across directions.

Here is one way this model produces the power-law curve from earlier. Replace the discrete directions with a continuum of decay rates. Give the initial loss a density proportional to <math><msup><mi>λ</mi><mrow><mi>α</mi><mo>−</mo><mn>1</mn></mrow></msup></math> near zero, with an exponential cutoff at large rates. Write <math><mi>K</mi><mo>&gt;</mo><mn>0</mn></math> for the scale of that density and <math><msub><mi>t</mi><mn>0</mn></msub><mo>&gt;</mo><mn>0</mn></math> for the cutoff parameter. The scratch loss above its floor is the sum of what remains at all rates:

<math display="block" aria-label="Scratch loss above the floor is the integral over rates of their remaining contribution.">
  <mi>F</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo>
  <mi>K</mi><msubsup><mo>∫</mo><mn>0</mn><mi>∞</mi></msubsup>
  <msup><mi>λ</mi><mrow><mi>α</mi><mo>−</mo><mn>1</mn></mrow></msup>
  <msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><mo>(</mo><mi>T</mi><mo>+</mo><msub><mi>t</mi><mn>0</mn></msub><mo>)</mo><mi>λ</mi></mrow></msup>
  <mi>d</mi><mi>λ</mi><mo>.</mo>
</math>

Substitute <math><mi>z</mi><mo>=</mo><mn>2</mn><mo>(</mo><mi>T</mi><mo>+</mo><msub><mi>t</mi><mn>0</mn></msub><mo>)</mo><mi>λ</mi></math>. The remaining integral is the gamma function <math><mi>Γ</mi><mo>(</mo><mi>α</mi><mo>)</mo></math>, independent of training time. All the time dependence is in the factor outside the integral:

<math display="block" aria-label="Scratch loss above the floor is K times gamma of alpha divided by twice the shifted budget raised to alpha.">
  <mi>F</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo>
  <mfrac>
    <mrow><mi>K</mi><mi>Γ</mi><mo>(</mo><mi>α</mi><mo>)</mo></mrow>
    <msup><mrow><mo>[</mo><mn>2</mn><mo>(</mo><mi>T</mi><mo>+</mo><msub><mi>t</mi><mn>0</mn></msub><mo>)</mo><mo>]</mo></mrow><mi>α</mi></msup>
  </mfrac><mo>.</mo>
</math>

Each error decays exponentially, while their sum decays as a power law. As training proceeds, progressively slower errors account for more of the remaining loss. Uniform acceleration shifts this curve. Selective acceleration changes which errors are left, so one shift may fail to predict the curve. The rate density is an assumption of the example. It would take separate evidence to infer anything about the spectrum of a language model from a measured learning curve.

### What survives beyond quadratic losses?

The exact dose result depends on the solvable model. A first-order comparison survives under smooth deterministic gradient flow, even when the language objective changes curvature along the trajectory and the evaluation set differs from the training set.

Let <math><msub><mi>g</mi><mi>ℓ</mi></msub></math> and <math><msub><mi>g</mi><mi>s</mi></msub></math> be the language and synthetic training gradients. Let <math><msub><mi>w</mi><mi>T</mi></msub></math> be the endpoint of language-only training. Write <math><msub><mi>J</mi><mi>T</mi></msub></math> for its Jacobian with respect to the starting weights <math><msub><mi>w</mi><mn>0</mn></msub></math>. This Jacobian transports a small change at the start into a change at the endpoint. The held-out loss is <math><mi>R</mi></math>. To compute the transport, differentiate the language gradient flow with respect to its initial condition. Starting from the identity matrix, the derivative of the Jacobian obeys

<math display="block" aria-label="The time derivative of the Jacobian is minus the language Hessian along the trajectory times the Jacobian.">
  <msub><mover><mi>J</mi><mo>˙</mo></mover><mi>t</mi></msub><mo>=</mo><mo>−</mo>
  <msup><mo>∇</mo><mn>2</mn></msup><msub><mi>F</mi><mi>ℓ</mi></msub><mo>(</mo><msub><mi>w</mi><mi>t</mi></msub><mo>)</mo>
  <msub><mi>J</mi><mi>t</mi></msub><mo>.</mo>
</math>

Replace a tiny initial interval of language with an equally costly synthetic interval. The change at the start, per unit of synthetic time, is <math><mo>−</mo><msub><mi>g</mi><mi>s</mi></msub><mo>+</mo><mi>κ</mi><msub><mi>g</mi><mi>ℓ</mi></msub></math>, with both gradients evaluated at the common start. One way to see the subtraction is to factor the scratch run into the small language interval being replaced and the shared language continuation. At dose zero, the two continuations coincide. Their common change with dose cancels when we take the difference. The remaining change comes from transporting the difference between the two early updates. Apply the chain rule and change the sign to express the gain <math><msub><mi>G</mi><mi>T</mi></msub></math> as scratch held-out loss minus warm held-out loss at the same total budget.

<math display="block" aria-label="Marginal gain at zero dose is the inner product of the transported validation gradient with the difference between the synthetic gradient and the compute-equivalent language gradient.">
  <msubsup><mi>G</mi><mi>T</mi><mo>′</mo></msubsup><mo>(</mo><mn>0</mn><mo>)</mo><mo>=</mo>
  <msup><mi>q</mi><mo>⊤</mo></msup><mo>(</mo>
  <msub><mi>g</mi><mi>s</mi></msub><mo>−</mo><mi>κ</mi><msub><mi>g</mi><mi>ℓ</mi></msub>
  <mo>)</mo><mo>,</mo>
  <mspace width="0.8em"/>
  <mi>q</mi><mo>=</mo><msubsup><mi>J</mi><mi>T</mi><mo>⊤</mo></msubsup><mo>∇</mo><mi>R</mi><mo>(</mo><msub><mi>w</mi><mi>T</mi></msub><mo>)</mo><mo>.</mo>
</math>

The gradient that matters is the gradient of the **future** validation loss with respect to the starting point. Immediate agreement between a synthetic update and a language update can be misleading. A direction that helps today can have little influence after the rest of training. For the quadratic language loss, the transport is simply multiplication by the language contraction in each direction. Substitution recovers the zero-dose slope above, with the sign reversed because the equation now measures gain.

In real pre-pre-training, switching vocabularies can reset parameters and Adam can carry or discard momentum. Training also uses discrete batches and schedules. Rather than treating the gradient formula as a Transformer prediction, we can estimate the comparison with a small fork experiment. Spend equal FLOPs on a short synthetic prefix and a language prefix, apply identical transition rules in both arms, then continue on the same text. Evaluate their held-out loss difference as continuation length grows. A standard uninterrupted language-only arm measures the cost of imposing a transition at all. A separate finite-dose experiment still has to establish whether any useful training budget is saved.

## What experiment would separate them?

The first milestone should be modest: establish a reproducible gap under a fair comparison before trying to explain its disappearance. Select one NCA generator and one language distribution. Train scratch and synthetic-warm-up models with comparable tuning opportunities, record all training stages, and measure held-out language loss against **total** compute, including the synthetic stage. Include strong initialization and language-only baselines. A matched-language-token comparison can still be shown, but it answers a different question: whether extra synthetic work helps, not whether it is the best use of that work.

Then vary model size and language budget separately. Start with one size and several language budgets, and test the constant-shift prediction on later checkpoints. Repeat a small set of those budgets at a second size. That gives a comparison at equal language exposure alongside the comparisons designers usually make, where the language budget increases with model size. Screen synthetic doses on development runs and choose the dose and useful effect threshold before opening fresh confirmation runs. A larger dose that restores the same-text gap but still fails break-even would change the interpretation of transfer while leaving the compute decision unchanged. The independent unit for uncertainty is the training run, not the number of evaluation sentences. If models share a warm-up checkpoint, their later branches do not become independent histories merely because their continuation seeds differ.

For the efficiency comparison, pick a held-out loss target above the floor both arms can reach. Compare costs at that target and report the curves on both language and total-compute axes. A checkpoint early in a long run can have a different learning-rate schedule from a shorter run trained to finish there. Use independently scheduled endpoint runs to check a result based on intermediate crossings.

The two-rate model suggests a cheaper check before any circuit intervention. On a development corpus, use scratch checkpoints to define groups of examples whose remaining loss improves quickly and slowly over a specified budget window. Freeze the grouping rule and the window. Assign fresh examples using a scratch trajectory held out from the final comparison. Then test on independently trained pairs whether the synthetic prefix gains mainly on the faster group and loses ground on the slower one. Using separate runs for group assignment prevents a noisy scratch loss from defining its own apparent gain. These groups are behavioural measurements, so a successful prediction would still leave the internal mechanism open. Failure would count against this particular explanation of the crossover.

Only after a stable gap is established should we ask what happens inside the model. Build a separate, controlled rule-inference evaluation with held-out rules and initial states. Check that simple shortcuts cannot solve it, and include cases where a plausible strategy should fail. At checkpoints during language training, ask:

- **Behaviour:** Can each model infer and apply a rule, including after the rule changes?
- **Information:** Can a held-out probe recover the rule or state from its activations? A successful probe shows information is available to the probe, not that the model uses it.
- **Causal use:** When a targeted intervention changes the relevant information, does the model's behaviour change as predicted? Compare against matched control interventions and test for general damage to the model.
- **Recovery:** Can the earlier behaviour be restored by a controlled intervention or a small amount of retraining? Recovery would constrain the explanation, but it would not by itself reveal a unique original circuit.

If scratch models acquire similar behaviour while the warm-started models retain theirs, the evidence would support functional convergence. If warm-started models lose causal use while information remains decodable, a change in readout or routing becomes plausible. If both decline, erasure and reorganization remain possible. A failed probe or intervention could also miss a distributed representation. None of these results alone proves that the tested computation caused the language-loss gap. That requires an intervention that changes the putative computation and measures the effect on subsequent language learning, with controls for the disruption it introduces.

## The question behind the question

The larger idea is that training history may matter even when two models finish with similar language loss. One may reach a solution through synthetic experience; another may reach comparable predictions through language alone. Equal scores do not guarantee identical internal strategies. Conversely, different internal patterns do not prove a consequential difference in what the models can do.

I am interested in developmental timing for that reason. An early experience might help a model acquire a capability, change how later training uses it, or leave little trace that matters for the final objective. These possibilities lead to different engineering decisions. If scratch models simply catch up, the synthetic phase may be valuable only at small budgets. If a useful capability becomes inaccessible, preserving or reintroducing it could be worth testing. If it remains intact but has little relevance to language, more preservation may solve the wrong problem.

This is also why I would hold off on introducing a new architecture at the start. A TEM-inspired model, replay schedule, or more elaborate generator may eventually be useful, but each adds decisions before we know which failure it needs to fix. First establish the gap, give the baseline a fair chance, and make the competing explanations disagree on a measurement. The synthetic world should earn its place in the training budget—and the theory should earn its place in the story.

## References

- Lee, Han, Kumar and Agrawal. [*Training Language Models via Neural Cellular Automata*](https://arxiv.org/abs/2603.10055v2), 2026.
- Stern, Rocktäschel, Locatelli and Ruis. [*Rethinking Pre-pretraining*](https://arxiv.org/abs/2610.40051v1), 2026.
- Wu, Zou, Braverman, Gu and Kakade. [*The Power and Limitation of Pretraining-Finetuning for Linear Regression under Covariate Shift*](https://arxiv.org/abs/2208.01857), 2022.
- Buna, Liu and Rebeschini. [*Compute-Optimal Pretrain–Fine-tune in Ridge Gradient Descent*](https://arxiv.org/abs/2609.16262v1), 2026.
- Hu, Petty, Shi, Merrill and Linzen. [*Between Circuits and Chomsky: Pre-pretraining on Formal Languages Imparts Linguistic Biases*](https://arxiv.org/abs/2502.19249), 2025.
- Ravulapalli. [*Can a model learn language more efficiently by navigating a tiny world?*](/writing/2026/10/action-warm-up-game/), 2026.
