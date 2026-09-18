---
title: The Harness Margin Opportunity
title_original: The Harness Margin Opportunity
date: '2026-09-17'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/the-harness-margin-opportunity/
author: ''
summary: '[翻译失败，原文如下]


  In short :A UC Berkeley study finds the harness sets the price of an answer : GPT-5.6
  Sol costs 71% less on Pi than on Claude Code, the s...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-18T06:56:04.602894'
---

[翻译失败，原文如下]

In short :A UC Berkeley study finds the harness sets the price of an answer : GPT-5.6 Sol costs 71% less on Pi than on Claude Code, the same model returning the same result, & none of the 42 harness comparisons shows a statistically significant quality difference. Two startups bidding on the same $250k contract earn 38% & 75% gross margins depending on what they built around the model, & the cheaper one pays back its sales cost in half the time. Effective harnesses take a deep customer understanding, relevant evals & a factory for automating hill climbing.

The better the harness, the better the business.

Berkeley published a study this week showing harnesses, the systems that control AI agents, set the price of an answer. The right harness cuts the cost of the same result by 71% without a loss of accuracy.1

![Cost of one attempt on SWE-bench Lite for seven models, cheapest harness versus most expensive, with cost multiples from 1.1x to 5.1x](/images/posts/0089a7702b27.jpg)

The data points to the opportunity for the next generation software applications : harnesses. Yes, we can use AI to do almost anything we want at work. But no, we cannot afford to provide everyone access to state of the art models for every task.

Harnesses coalesce common workflows into repeatable patterns : deterministic code or skills. The better the harness, the greater the compression, the lower the AI cost.

Imagine Theory buys a $250k a year contract for an AI associate to evaluate 5,000 companies. Two startups bid. Inferno calls a state of the art model on every step. Inferefficient runs a harness that coalesces the work into deterministic code, reserving the expensive model for the few steps that need it.

Inferno burns $131k on inference. Inferefficient burns $37k. Both carry the same cost for hosting, evaluations & the humans who check the work. Identical revenue, 38% gross margin against 75%.2

Inferno cannot copy Inferefficient. Routing to a cheap model is only safe if you know which tasks it clears, & that knowledge comes from watching ten thousand versions of the same work. The cost advantage & the moat are the same asset.

Past 8,600 evaluations Inferno loses money on every additional one. It has to ration usage, which makes it the worse product at the moment the customer finds it most valuable. Inferefficient says yes to everything.

Gross profit buys growth. On a $250k contract that costs $150k to win, Inferno waits nineteen months to earn back the sale. Inferefficient waits ten. One of these businesses can hire twice as fast as the other.

Margins will not climb to 100%. As inference gets cheaper, buyers will ask more of their agents, shifting the equilibrium over time in response to competition. The gap between the two companies is what persists.

Effective harnesses are not cocktails of exotic ingredients : a deep customer understanding, a collection of relevant evals & a factory for automating hill climbing.

That’s a recipe for a valuable, defensible software company.

1. Melissa Z. Pan, Shuo Yang, Negar Arabzadeh, Wei-Lin Chiang, Ion Stoica, & Matei Zaharia, “HarnessTax: How Much Does the Harness Matter for Coding Agents?”, 2026. Twenty-one model-harness pairs, 30 tasks each from SWE-bench Lite & Terminal-Bench 2.0, three attempts per task, costed on a fixed price list dated September 1, 2026. Across all 42 within-model harness comparisons, a two-sided Fisher exact test finds one result at p < 0.05, where chance alone would produce about two, & none survives a Holm-Bonferroni correction. Two limits : the published rollouts are sorted by cost, which destroys the task pairing & rules out a paired test, & at 90 rollouts per cell the study detects only swings of roughly fifteen points. The quality gap is undemonstrated at this sample size, not proven absent.↩︎
2. The harness swap is GPT-5.6 Sol moving from Claude Code to Pi in the same study : $1.540 to $0.441 per resolved task, the same model in both cases. That 71% reduction is measured data & is what the argument rests on. The rest is illustrative : that a company evaluation runs about seventeen benchmark-task equivalents, & that both companies carry $25k of non-inference cost of goods for hosting, evaluation infrastructure & human review. Those assumptions set the absolute margins, not the gap between them. At ten task equivalents the comparison is 59% against 81% ; at thirty it is a loss against 64%. Inferefficient stays a software business across that range & Inferno does not, which is the point.↩︎

Melissa Z. Pan, Shuo Yang, Negar Arabzadeh, Wei-Lin Chiang, Ion Stoica, & Matei Zaharia, “HarnessTax: How Much Does the Harness Matter for Coding Agents?”, 2026. Twenty-one model-harness pairs, 30 tasks each from SWE-bench Lite & Terminal-Bench 2.0, three attempts per task, costed on a fixed price list dated September 1, 2026. Across all 42 within-model harness comparisons, a two-sided Fisher exact test finds one result at p < 0.05, where chance alone would produce about two, & none survives a Holm-Bonferroni correction. Two limits : the published rollouts are sorted by cost, which destroys the task pairing & rules out a paired test, & at 90 rollouts per cell the study detects only swings of roughly fifteen points. The quality gap is undemonstrated at this sample size, not proven absent.↩︎

The harness swap is GPT-5.6 Sol moving from Claude Code to Pi in the same study : $1.540 to $0.441 per resolved task, the same model in both cases. That 71% reduction is measured data & is what the argument rests on. The rest is illustrative : that a company evaluation runs about seventeen benchmark-task equivalents, & that both companies carry $25k of non-inference cost of goods for hosting, evaluation infrastructure & human review. Those assumptions set the absolute margins, not the gap between them. At ten task equivalents the comparison is 59% against 81% ; at thirty it is a loss against 64%. Inferefficient stays a software business across that range & Inferno does not, which is the point.↩︎

---

> 本文由AI自动翻译，原文链接：[The Harness Margin Opportunity](https://tomtunguz.com/the-harness-margin-opportunity/)
> 
> 翻译时间：2026-09-18 06:56
