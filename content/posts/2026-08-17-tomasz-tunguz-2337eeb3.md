---
title: When Models Learn
title_original: When Models Learn
date: '2026-08-17'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/test-time-training-impact/
author: ''
summary: '[翻译失败，原文如下]


  In short :Explains test-time training through the analogy of a GPS learning a persistent
  shortcut around daily traffic rather than a one-...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:04.134026'
---

[翻译失败，原文如下]

In short :Explains test-time training through the analogy of a GPS learning a persistent shortcut around daily traffic rather than a one-time reroute: the model takes a gradient step on the prompt it's answering, so its weights change as it works. Traces three implications, flat memory instead of a linearly growing KV-cache, the provider cost of serving a separate model per user, & faster inference, then states the tension as a tradeoff between serving long context and serving many people, & grounds it in concrete use cases, a coding agent that earns back its per-user cost over a long session versus a one-off query a shared frozen model handles just as well.

Every model you’ve ever used froze the day its training ended. The answers are the same even if you have used it every day.

What if a model kept learning as you use it?

A GPS learns a persistent shortcut around daily traffic on northbound Highway 101, not just a one-time reroute. Test-time training does that to a model as it works.1As you use the AI, the model changes its weights, changes how it thinks about its memories, to answer you better.

The changes are more profound than finding an off-ramp to an access road past a highway junction chokepoint.

Memory requirements plummet. A standard transformer keeps a KV-cache, a running record of every earlier token, so its memory grows linearly with context, every additional token adds to the running record. Test-time training folds that history into a fixed-size set of weights instead of a growing cache, so memory stays flat no matter how long the conversation runs.

The model provider now has to serve a separate model to each person. Once a model updates on your prompt, it is no longer the model that answered your neighbor’s, so a single checkpoint serving millions of users becomes millions of slightly different models, each shaped by the person using it. That divergence is the provider’s problem to solve: a GPU provider needs a copy in flight per user instead of one shared copy for everyone, which means more compute, more chips, to serve the same number of people.

It’s much faster. Stanford research on small models indicates it can be up to 2.7 times faster, because a test-time trained model’s inference latency stays constant no matter how long the context runs, the way a standard transformer’s does not.2In-Place TTT also ships drop-in, lifting a 4b model to competitive 128k-context performance with no retraining.3

Here is the tension. Standard AI is limited by memory, test-time AI is limited by compute & chips, so a provider picks based on whether it’s serving long context or serving many people.

That cost is only worth paying where personalization earns its keep. A coding agent that learns your codebase’s conventions, the resilient persistent bugs, ultimately should provide some form of lock-in via memory, so the per-user cost pays for itself. A one-off customer support question doesn’t need any of that. A shared, frozen, potentially fine-tuned model answers it just as well & costs the provider far less to serve.

Test-time training will be a key part of the discourse throughout the end of 2026 & beyond. It has the potential to change the current economics of AI.

1. Sun et al., Learning to (Learn at Test Time): RNNs with Expressive Hidden States↩︎
2. End-to-End Test-Time Training for Long Context↩︎
3. In-Place Test-Time Training↩︎

Sun et al., Learning to (Learn at Test Time): RNNs with Expressive Hidden States↩︎

End-to-End Test-Time Training for Long Context↩︎

In-Place Test-Time Training↩︎

---

> 本文由AI自动翻译，原文链接：[When Models Learn](https://www.tomtunguz.com/test-time-training-impact/)
> 
> 翻译时间：2026-08-19 03:07
