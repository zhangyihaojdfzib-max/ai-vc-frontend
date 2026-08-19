---
title: Birds Don't Fly Like Planes. Neither Does AI.
title_original: Birds Don't Fly Like Planes. Neither Does AI.
date: '2026-08-18'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/birds-dont-fly-like-planes-neither-does-ai/
author: ''
summary: '[翻译失败，原文如下]


  In short :Qwen3.6-35B-A3B generates 2.2x faster than Qwen3.8-27B, yet finishes slower
  because it thinks 3.1x longer. Across 25 tasks, qua...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:04.083304'
---

[翻译失败，原文如下]

In short :Qwen3.6-35B-A3B generates 2.2x faster than Qwen3.8-27B, yet finishes slower because it thinks 3.1x longer. Across 25 tasks, quality is tied. Measure time to answer, not token speed.

Your laptop can now run a model as capable as nearly anything in the cloud. I swapped Qwen3.8-27B into my agent & it works brilliantly. This bird flies differently than a plane.

This little Qwen model ranks #1 of 135 models, scoring 52 on Artificial Analysis’s Intelligence Index, a point above GLM-5.2, the state-of-the-art open-source model from Z.ai, at 753b parameters.1A laptop model beats a recognizable, frontier-class cloud peer roughly 28 times its size.

How does a bumblebee achieve the same flight as an airliner? Bigger models can store more knowledge, so they can skip straight to an answer, like an expert in many different fields. Smaller models don’t have as much memorized, so they must reason more, almost from first principles, to close that gap.2

I saw this firsthand when benchmarking the DeepSeek V4 cloud model against two local models. I compared them on the same work, 25 venture-capital tasks (researching startups, summarizing articles, transcribing podcasts), scored by a judge model.3

Qwen3.8-27B is dense : it uses every chapter in the book on every question. Book skimmers DeepSeek & Qwen 3.6 35b (another local model I threw into the test), flips only to the relevant chapters for a question.4

These models provide identically good answers. But the speed varies. The local Qwen 35b shreds at top speed, but needs to think about 7.2x more than the cloud model, crossing the line 9 seconds after DeepSeek. The newest Qwen model is three seconds faster, & the cloud is 6 seconds faster yet.

The cloud model jumps to the right answer ; the local models contemplate & debate internally at different rates of speed & accuracy.

For example : on one triage task, the 35B spent 993 tokens to produce six words, “Classification: Scheduling / Action: Respond.” 1000 tokens of deliberation before the response is a hummingbird’s sprint to a honeysuckle. The bumblebee needed 369 thinking tokens, buzzing along at half the speed.

Local models can achieve the same result as cloud models, but they’ll take a different flight path to get there.

1. Artificial Analysisranks the incumbent here, Qwen3.8-27B, #1 of 135 models on the Intelligence Index, scoring 52, a point above GLM-5.2’s 51, a 753b-parameter frontier model Z.ai shipped two months earlier. The same page ranks it #23 of 135 on output tokens per task, 160M weighted tokens against a class median of 43M. Intelligence rank & verbosity rank move independently, & that’s the trade this whole post is about.↩︎
2. The imitation-gap explanation. Smaller models produce fluent chain-of-thought that’s more likely to drift logically inconsistent, because they have a sparser map of nearby correct examples to draw on once forced off the direct path to an answer. SeeChain of Thought in Large Language Models: Elicited Reasoning or Constrained Imitation?I covered the general shape of this tradeoff, trading inference-time compute for capability, inWhen Models Learn.↩︎
3. Method. 25 venture-capital tasks (researching startups, summarizing articles, transcribing podcasts) drawn from my own agent queue. A separate judge model, deepseek-v4-pro, scored outputs blind on completeness, accuracy & conciseness, 3 points each for 9 total. max_tokens was 4096 for every run. Both local models were served through Ollama on the same MLX runtime, so the comparison isn’t confounded by runtime differences. I established the judge’s noise floor by re-scoring identical outputs, which returned a mean absolute difference of 0.16.↩︎
4. Qwen3.6-35B-A3B is a 35b parameter model with 3b active parameters per token, a sparse mixture-of-experts architecture, 256 total experts with 8 routed & 1 shared active per token. PerQwen’s model card on Hugging Face&vLLM’s model recipe.↩︎

Artificial Analysisranks the incumbent here, Qwen3.8-27B, #1 of 135 models on the Intelligence Index, scoring 52, a point above GLM-5.2’s 51, a 753b-parameter frontier model Z.ai shipped two months earlier. The same page ranks it #23 of 135 on output tokens per task, 160M weighted tokens against a class median of 43M. Intelligence rank & verbosity rank move independently, & that’s the trade this whole post is about.↩︎

The imitation-gap explanation. Smaller models produce fluent chain-of-thought that’s more likely to drift logically inconsistent, because they have a sparser map of nearby correct examples to draw on once forced off the direct path to an answer. SeeChain of Thought in Large Language Models: Elicited Reasoning or Constrained Imitation?I covered the general shape of this tradeoff, trading inference-time compute for capability, inWhen Models Learn.↩︎

Method. 25 venture-capital tasks (researching startups, summarizing articles, transcribing podcasts) drawn from my own agent queue. A separate judge model, deepseek-v4-pro, scored outputs blind on completeness, accuracy & conciseness, 3 points each for 9 total. max_tokens was 4096 for every run. Both local models were served through Ollama on the same MLX runtime, so the comparison isn’t confounded by runtime differences. I established the judge’s noise floor by re-scoring identical outputs, which returned a mean absolute difference of 0.16.↩︎

Qwen3.6-35B-A3B is a 35b parameter model with 3b active parameters per token, a sparse mixture-of-experts architecture, 256 total experts with 8 routed & 1 shared active per token. PerQwen’s model card on Hugging Face&vLLM’s model recipe.↩︎

---

> 本文由AI自动翻译，原文链接：[Birds Don't Fly Like Planes. Neither Does AI.](https://www.tomtunguz.com/birds-dont-fly-like-planes-neither-does-ai/)
> 
> 翻译时间：2026-08-19 03:07
