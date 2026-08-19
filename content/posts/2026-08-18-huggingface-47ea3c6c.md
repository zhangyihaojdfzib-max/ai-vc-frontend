---
title: How Much Memory Does Your Agent Actually Need?
title_original: How Much Memory Does Your Agent Actually Need?
date: '2026-08-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-research/altk-evolve-hmm
author: ''
summary: '[翻译失败，原文如下]


  # How Much Memory Does Your Agent Actually Need?


  In ourprevious post, we comparedALTK-EvolvewithACEand showed thathowyou deliver
  an agen...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:40.044623'
---

[翻译失败，原文如下]

# How Much Memory Does Your Agent Actually Need?

In ourprevious post, we comparedALTK-EvolvewithACEand showed thathowyou deliver an agent's self-distilled guidelines — a few retrieved per task vs. the whole set injected — drives both accuracy and cost. This post steps back to the question that comes before it:how muchshould you give it?

Equipping an agent with agentic memory sounds simple: distill lessons from its past work, put them back in context, and more experience should mean better performance. It doesn't always work that way. When we scaled the evaluation toeight models— from a 30B dense model to frontier proprietary systems — one finding stood out:

Agentic memory is not a feature you switch on. It's a dose you calibrate to the model.

TL;DR

- ALTK-Evolvelets an agent learn from its own past trajectories: distilling reusable guidelines and injecting them back at inference time, with no weight updates and no human annotation.
- The right dose differs by model tier:strong models with headroom want the full guideline set, weaker models do best with a compact core plus per-task retrieval, and saturated models show no measurable gain.
- Curated retrieval can be both the most accurate and the cheapest option:gpt-oss-120b gained +16.1pp task completion at only +5% tokens — and prompt caching keeps even the full guideline set affordable in production.

ALTK-Evolvelets an agent learn from its own past trajectories: distilling reusable guidelines and injecting them back at inference time, with no weight updates and no human annotation.

The right dose differs by model tier:strong models with headroom want the full guideline set, weaker models do best with a compact core plus per-task retrieval, and saturated models show no measurable gain.

Curated retrieval can be both the most accurate and the cheapest option:gpt-oss-120b gained +16.1pp task completion at only +5% tokens — and prompt caching keeps even the full guideline set affordable in production.

## The Key Insight: Dosage Depends on Capability

Not every model benefits from the same amount of memory. Across eight models spanning the capability spectrum, we saw three recurring patterns:

- Strong models with headroomwant the full guideline set — every guideline, including rare edge-case lessons. They have the capacity to absorb and apply all of it. DeepSeek-V3.2 (671B MoE) climbed+9.5 percentage pointsin task completion when given its full self-mined guideline set.
- Smaller or weaker models get drowned by a large guideline set.For these, a tight, high-confidence core plus a handful of task-relevant guidelines retrieved per task works best. gpt-oss-120b (117B MoE) gained+16.1ppwith this selective approach — while the full guideline set gained lessandcost ~50% more tokens.
- Already-saturated models show no measurable gain.We call this the saturated pattern — the label describes what we observed, not a proven cause. The model may already have been near its ceiling on these tasks, the guidelines may not have addressed its remaining failures, or it may not have applied the guidance effectively. GLM-5 (745B MoE) sat here in our runs.

Strong models with headroomwant the full guideline set — every guideline, including rare edge-case lessons. They have the capacity to absorb and apply all of it. DeepSeek-V3.2 (671B MoE) climbed+9.5 percentage pointsin task completion when given its full self-mined guideline set.

Smaller or weaker models get drowned by a large guideline set.For these, a tight, high-confidence core plus a handful of task-relevant guidelines retrieved per task works best. gpt-oss-120b (117B MoE) gained+16.1ppwith this selective approach — while the full guideline set gained lessandcost ~50% more tokens.

Already-saturated models show no measurable gain.We call this the saturated pattern — the label describes what we observed, not a proven cause. The model may already have been near its ceiling on these tasks, the guidelines may not have addressed its remaining failures, or it may not have applied the guidance effectively. GLM-5 (745B MoE) sat here in our runs.

What puts a model into one pattern rather than another isn't simply parameter count.Benchmark headroom, context-window size, architecture, guideline quality, and task distribution all appear to shape where a model lands, and separating those factors is ongoing work. The practical takeaway holds either way:the right dose of memory depends on the model, and we can calibrate it.

## Learning happens around the model, not inside it

"Memory" here doesn't mean replaying a past transcript. It means aguideline set— strategies that worked, mistakes to avoid, and edge cases — distilled from the agent's own prior trajectories. The loop is straightforward:

1. The agent attempts tasks and produces trajectories.
2. ALTK-Evolve extracts behavioral guidelines from both its successful and unsuccessful runs.
3. It consolidates those guidelines into a reusable set.
4. At inference time, the agent receives either the full guideline set or a task-relevant selection of it.

The agent attempts tasks and produces trajectories.

ALTK-Evolve extracts behavioral guidelines from both its successful and unsuccessful runs.

It consolidates those guidelines into a reusable set.

At inference time, the agent receives either the full guideline set or a task-relevant selection of it.

No model weights are updated. The learning loop changes theguidance available to the agent, not the underlying model — which is exactly why it's cheap to adopt and portable across the eight models we tested.

## Results Across the Spectrum

We evaluated onAppWorld— 585 multi-step tasks (168test_normal+ 417test_challenge) across 9 simulated apps (calendars, messaging, payments, and so on). Tasks are scored two ways: whether the agent fully completes each task (TGC — Task Goal Completion) and whethereveryvariant of a scenario passes (SGC — Scenario Goal Completion, a stricter, all-or-nothing bar). Full definitions are in the appendix.

### The three configurations we compare

Because the confusing part of any memory study iswhat's actually in the context window, we define the configurations up front.

Both memory configurations draw fromthe same guideline set, mined once (via the loop above) from AppWorld'straining splitonly. What changes between them is onlyhow that one set is delivered— thefull guideline setinjects all of it every step, whilecurated retrievaldelivers a selected subset — never how the guidelines were produced, and no test-split data ever goes into building it.

The number of guidelines a model mines depends on its own capability, so we report configurations bystrategy— "full guideline set" vs. "curated retrieval" — rather than by raw counts, which aren't comparable across models.

### The three patterns, in one view

Representative models from the eight-model sweep, measured by task completion (TGC) ontest_normal:

![image](/images/posts/ef2082f5aeb1.png)

Figure 1. Representative models in the three observed patterns. Bars show TGC on AppWorldtest_normalfor baseline vs. the best-memory configuration; the x-axis begins at 40% to make differences visible. TGC alone understates the larger SGC gains — see the SGC columns in the table below.

The figure plots TGC to keep it readable; the table adds the stricterSGCmetric, where the gains are often larger:

Reading the SGC column, the stricter metric usually moves more than TGC — DeepSeek's SGC jumps+16.1ppagainst a+9.5ppTGC gain — because good guidelines especially help an agent cleareveryvariant of a scenario, not just the average case. And the effect doesn't disappear at the top of the range: GPT-5.5 and Opus, both near the ceiling on TGC, still gain+7.2and+7.1pp SGCrespectively. Memory keeps paying off as long as a model has a remaining failure mode to target.

## The Cheapest Memory Strategy Can Also Be the Best

[翻译失败，原文如下]

A practical concern: injecting a full guideline set inflates every ReAct step's input, because the guidelines are re-sent each turn. Here's what we observed:

Table 1. Average token use per task, accumulated across agent steps, measured against the no-memory baseline.

Two takeaways:

1. Curated retrieval keeps cost near baseline.For weaker models, where selection wins on accuracy, it also wins on cost — the best of both worlds (+16.1pp TGC at only +5% tokensfor gpt-oss-120b). Better performance here doesnotrequire more inference cost.
2. Memory doesn't blow up the reasoning loop.DeepSeek runs about the same number of ReAct steps with memory as without (≈18–19 on average), so the added cost is input-token inflation, not longer trajectories.

Curated retrieval keeps cost near baseline.For weaker models, where selection wins on accuracy, it also wins on cost — the best of both worlds (+16.1pp TGC at only +5% tokensfor gpt-oss-120b). Better performance here doesnotrequire more inference cost.

Memory doesn't blow up the reasoning loop.DeepSeek runs about the same number of ReAct steps with memory as without (≈18–19 on average), so the added cost is input-token inflation, not longer trajectories.

The real efficiency lever in production isprompt caching: the static portion of the guideline set is identical across steps and can be cached, cutting effective cost substantially. Cache-aware prompt design — keeping the shared guideline-set prefix stable so it stays cacheable — is worth engineering for. We also hypothesize thatcontext-window sizeplays a role: models with larger windows may absorb the full guideline set more effectively, while smaller-context models benefit more from retrieval that keeps injected content compact. We have not yet run controlled experiments isolating this factor.

## Memory Should Be Calibrated, Not Merely Accumulated

The lesson isn't to give an agent everything it has learned. It's to give it the amount of experience it can actually use.

- Forweak models, that means a compact core plus a few task-specific lessons — which, conveniently, is also the cheapest option.
- Forstrong models with headroom, it means preserving the full guideline set, kept affordable in production via prompt caching.
- Forsaturated models, it means spending no extra context until their remaining failure modes are better understood.

Forweak models, that means a compact core plus a few task-specific lessons — which, conveniently, is also the cheapest option.

Forstrong models with headroom, it means preserving the full guideline set, kept affordable in production via prompt caching.

Forsaturated models, it means spending no extra context until their remaining failure modes are better understood.

The gains are real across the board — automatic, leakage-free, and requiring no human annotation — but only when the dose fits the model.

## What's Next

This is a starting point, not the finish line:

- A learned selector.Our current retrieval ranks guidelines by cosine similarity, which we've shown doesn't perfectly predict which guidelines help a given task. A selector trained on outcome signal is the natural next step.
- Memory for very weak models.Below a minimum capability baseline, self-distillation lacks signal. Teacher-distilled memory for very weak models is a separate problem we're exploring.
- Beyond AppWorld.These results are validated on AppWorld — a rigorous multi-step benchmark, but a single one. Broader agent benchmarks and real-world deployments are in progress.
- Isolating context window.As above, we want controlled experiments that separate context-window size from raw capability.

A learned selector.Our current retrieval ranks guidelines by cosine similarity, which we've shown doesn't perfectly predict which guidelines help a given task. A selector trained on outcome signal is the natural next step.

Memory for very weak models.Below a minimum capability baseline, self-distillation lacks signal. Teacher-distilled memory for very weak models is a separate problem we're exploring.

Beyond AppWorld.These results are validated on AppWorld — a rigorous multi-step benchmark, but a single one. Broader agent benchmarks and real-world deployments are in progress.

Isolating context window.As above, we want controlled experiments that separate context-window size from raw capability.

Try theALTK-Evolvelibrary— which includes the extraction, consolidation, and retrieval pipeline used here —or read thefull technical reportfor the complete method and ablations.

## Appendix: Understanding the Metrics

AppWorld tasks are graded by two metrics, both reported as percentages (higher is better):

- TGC — Task Goal Completion.The share of individual tasks the agent completes fully and correctly. This is the headline"did it get the job done"number.
- SGC — Scenario Goal Completion.A stricter, all-or-nothing metric. Eachscenariobundles several variants of the same task (the same request with different data, phrasing, or edge conditions). SGC counts a scenario as passing only if the agent succeeds oneveryvariant. It measuresreliability— an agent that solves a task most of the time but fails on one variant scores on TGC but not on SGC.

TGC — Task Goal Completion.The share of individual tasks the agent completes fully and correctly. This is the headline"did it get the job done"number.

SGC — Scenario Goal Completion.A stricter, all-or-nothing metric. Eachscenariobundles several variants of the same task (the same request with different data, phrasing, or edge conditions). SGC counts a scenario as passing only if the agent succeeds oneveryvariant. It measuresreliability— an agent that solves a task most of the time but fails on one variant scores on TGC but not on SGC.

---

> 本文由AI自动翻译，原文链接：[How Much Memory Does Your Agent Actually Need?](https://huggingface.co/blog/ibm-research/altk-evolve-hmm)
> 
> 翻译时间：2026-08-19 03:07
