---
title: "Ideas on Creating Artificial Life in Silico"
date: 2026-10-08 12:00:00 +0530
description: "Notes on building an agent the way biology builds an animal: a body that must stay alive, feelings that tune how it learns, memory, a model of the world, and a childhood. What I expected, what I tried, and what broke."
tags: [artificial life, reinforcement learning, neuroscience]
---

**In short:** Most reinforcement-learning agents are given a score to maximise and nothing else. An animal is different. It has a body that can fail, and everything it does serves the job of staying alive. I'm exploring what happens if you build an agent that way. This post describes the ideas, one design principle I now believe in, and the first thing that went wrong.

## Why start from a body?

An animal doesn't wake up with a reward function. It wakes up hungry. Food, water, sleep, and safety are things its body needs, and the body keeps draining them. The drive to act comes from that drain. "Reward" is closer to relief than to a prize.

Reinforcement learning has a name for this view. Keramati and Gutkin (2014) called it homeostatic reinforcement learning: the agent has internal variables it must keep near a set point, and reward is the reduction of the gap between where those variables are and where they should be. A meal is rewarding because you were hungry, and for no other reason.

I like this idea for a practical reason, and a philosophical one. The practical reason is that the agent gets a reason to act in every situation, with no hand-written list of goals. The philosophical reason is that it makes survival the root of the whole system. Everything else becomes a tool for staying alive.

## What a living agent might need

Here is the list of parts I think an artificial organism needs. None of these is new on its own. Each has a literature behind it. The bet is on what happens when they are put together and made to depend on each other.

**A body with needs.** A few internal variables that fall over time and can be refilled, and a way for the agent to die. The world has to be able to hurt it.

**Feelings as settings, not as rewards.** In the brain, chemicals such as dopamine, serotonin, and noradrenaline don't carry the content of an experience. They change how the brain learns and decides: how fast to update, how much to explore, how far ahead to care. Doya (2002) laid out this mapping as a theory of how the brain sets its own learning parameters. I'm treating "emotion" in an agent the same way. A feeling is a signal that tunes a setting, such as exploration or learning speed, and it has a measurable job.

**Curiosity.** An animal that only ever acts on current needs never finds anything new. Curiosity pushes the agent toward situations it can't yet predict. Pathak and colleagues (2017) is a standard starting point for this in machine learning.

**Memory.** Where was the water? Where did the danger come from? An organism that forgets every place it has been has to rediscover its world each time.

**A model of the world.** The agent learns to predict what happens next, and uses the prediction to imagine before it acts. Predictions that fail are also a signal that something has changed.

**Planning, with a price.** Thinking costs energy, in a brain and in a computer. A sensible agent thinks longer only when the extra thought is likely to change its choice, and only when it trusts its own model enough to rely on it.

**A childhood.** Animals don't start by facing the full world. A parent protects the young, shows them things, and gradually lets them take over. I want the agent to go through early life under a caregiver before it is on its own, so that its first learning happens in a safe, structured setting.

## One principle I now believe in

Feelings should change how the agent learns. They shouldn't be added to what it is paid.

This sounds like a small point, and it turned out to matter a lot. If you add an internal signal such as curiosity or arousal straight into the reward, you quietly change what the agent is trying to do. It starts optimising the signal. A bonus for novelty that never goes away turns into a bonus for staying alive and wandering, whether or not that gets anything done.

There is a classic result that tells you when a bonus is safe. Ng, Harada, and Russell (1999) showed that a reward bonus leaves the best behaviour unchanged only if it has a particular form, a difference between the value of two states (this is called potential-based shaping). Anything outside that form can change what the agent learns to want.

So the rule I'm working with has two parts. Either a signal carries information the agent could not get any other way, or it controls a setting that has a measurable target. If it does neither, it doesn't belong in the agent.

## A testbed

I'm using Crafter (Hafner, 2022), a 2D survival game. The agent has to gather resources, craft tools, eat, drink, sleep, and avoid monsters. It rewards a long chain of skills, it has day and night, and it can kill the agent. That makes it a good small stand-in for a world with a body and a risk.

## What went wrong first

My first build had all of the parts above, assembled together. It did worse than a plain baseline agent that had none of them.

That was a useful result, even though I didn't want it. I then added the parts one layer at a time, and every layer lowered the score. Looking into why, I found the same story in several places. Each part was added because the brain has one. Each part sent out its signal whether or not the signal was ready to be useful. Some started out carrying no information and then changed as they learned, so the main learner was always chasing a moving input. Some added reward terms that pulled the agent toward the wrong goal. One part made planning decisions from a very weak model of the world. The agent wasn't short of information to begin with, so the extra parts mostly added noise.

This lines up with a lesson from software engineering: build in order, and check each part on its own before it joins the rest.

## What did work

One effect held up in repeated tests. Making the body's needs press harder, to a moderate level, helped the agent learn faster, and pushing the pressure too far stopped helping. Much of the gain seemed to come through how much the agent explored, which is a setting, and not through the reward. That fits the principle above: the body shaped how the agent learned.

## Where this goes next

Three things I plan to do:

1. Give each part an entry test. A part joins the agent only if it passes a check on its own signal and doesn't lower the score of the agent without it.
2. Rewrite the body's reward as the relief of a need, and move curiosity and arousal into the role of controlling settings.
3. Try the body-and-feeling ideas inside a stronger world-model agent, to see whether they help a learner that already predicts well.

I don't know yet whether any of this beats a good baseline. The honest status is that the ideas are clear, the first assembly failed, and the way to find out which ideas are worth keeping is to add them back one at a time.

## References

- Doya, K. (2002). Metalearning and neuromodulation. *Neural Networks*, 15(4-6), 495-506.
- Hafner, D. (2022). Benchmarking the spectrum of agent capabilities (Crafter). *ICLR 2022*.
- Keramati, M. and Gutkin, B. (2014). Homeostatic reinforcement learning for integrating reward collection and physiological stability. *eLife*, 3, e04811.
- Ng, A., Harada, D. and Russell, S. (1999). Policy invariance under reward transformations: theory and application to reward shaping. *ICML 1999*.
- Pathak, D., Agrawal, P., Efros, A. and Darrell, T. (2017). Curiosity-driven exploration by self-supervised prediction. *ICML 2017*.
