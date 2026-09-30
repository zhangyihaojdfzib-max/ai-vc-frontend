---
title: How Databricks rolls out frontier models to 12,000 employees on Day 1
title_original: How Databricks rolls out frontier models to 12,000 employees on Day
  1
date: '2026-09-28'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-databricks-rolls-out-frontier-models-12000-employees-day-1
author: ''
summary: '[翻译失败，原文如下]


  Providing our employees access to frontier AI capabilities is a top priority at
  Databricks, and consequently, it is important to us for t...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-30T08:14:50.032859'
---

[翻译失败，原文如下]

Providing our employees access to frontier AI capabilities is a top priority at Databricks, and consequently, it is important to us for them to use new models instantly when they become available. At the same time, it is nontrivial to give more than 12,000 people rapid access to a new model because:

1. Models that are marketed as frontier often aren’t.For example, Opus 5.0 was more expensive and ranked lower on both quantitative and qualitative quality scores among our engineers compared with Opus 4.8. Migrating to a model that regresses the frontier can meaningfully hurt a company, rather than help it. In our experience, substantial care is required when evaluating models before migrating workloads en masse to new models.
2. Naive use of a new model can explode costs.When we released GPT Astra to a control group with no associated cost mitigations, theaverage developer spent 60% morethan before gaining access to Astra. An overnight 60% cost increase with a user population of more than 10,000 is very difficult for a company to plan around. Once we better understood which tasks Astra is uniquely great at, we were able to steer usage to substantially reduce overall costs.

This post discusses a set of techniques we’ve employed to give most employees at Databricks “Day 1” access to new models, while allowing us to assess whether models are indeed good long-term workhorses. These techniques rely heavily onUnity Gatewayto adaptively release, evaluate, and incorporate new models. The week of September 21 was a critical test of these abilities when Opus 5, GPT-6 Sol and GPT-Luna were released in rapid succession. During the week, Databricks provided all employees with Day 1 access, and by Day 3, we had gathered enough data to confirm that these models were on the efficiency frontier, leading to their incorporation into our broader infrastructure.

## The Model Release Lifecycle

At a high level, new model releases at Databricks go through a pipeline that looks as follows:

1. Immediately make new models available to all employees, on an "experimental" basis.
2. Constrain usage of new models based on a per-user budget.
3. After gathering enough data, decide whether to promote the model to production (or even make it the default).

![](/images/posts/61dfabe3cabc.png)

### Step 1: Make new models available immediately

To make model management across closed and open model providers easier, we leverage our ownDatabricks Unity Gatewayfor all internal use. This is our central hub for AI governance, cost management, and observability, so it's natural that we start here.

The Gateway is where we enable all employees to access the newly released model. Server-side configuration is not enough, though. Our employees are using Claude Code, Codex, and theOmnigentmeta-harness on their laptops, and we need to distribute the new model configuration to them.

That's whereUnity Gateway CLI(UG CLI) comes in. The UG CLI is already running on everyone's laptop, deployed via our Mobile Device Management. Whenever someone starts Claude Code, Codex, or Omnigent, the UG CLI runs to check for new models, tools and skills, and updates the local harness's configuration. UG also lets us centrally designate default vs. experimental models, prepare models forsmart routing, and collect traces to evaluate each model rollout.

We configured Unity Gateway to push experimental configurations for Opus 5.5 and Sol 6. These models now show up with this tag, so that employees can select it but understand it's a new model that may or may not be best in class or stick around forever:

![](/images/posts/a225a63f65ad.png)

Claude Code / model output clearly designates Ous 5.5 as Experimental

### Step 2: Constrain usage using a per-user budget

We have previouslywritten abouthow we configure per-user budgets for AI spend. Since then, we have expanded our total budget architecture to include four principal budgets, each defined on a per-user basis:

1. Monthly maximum: Each user has an overall monthly spending ceiling across all models.
2. Daily runaway limit: Every user has a daily max, which can be raised directly in Slack to avoid accidental spending from a runaway session.
3. [New!] Quality frontier budget: We allocate a certain fraction of the monthly budget to the most premium models at the quality frontier, such as GPT Astra and Claude Fable. (Fable is not currently rolled out internally due to Anthropic data retention policies, but we are working closely to implement their new policy.) This reflects the intent that these models should not be used as daily drivers, but instead selected for specialized tasks where they are uniquely suited, to justify the 2-3x cost increase over the next quality tier.
4. [New!] Experimental budget: Another fraction of the monthly budget is allocated for the usage of new, untested models. Here, we aim to balance speed of adoption with the downside risk of widely exposing a model that is not on the efficiency frontier.

On day one of the model launch, we made Opus 5.5 and Sol 6 available to all employees via Unity Gateway and tagged them for the experimental budget. We then used the next few days to collect data to decide what to do next — drop the experimental tag or remove it from the model catalog that our developers see.

![](/images/posts/edb3de92c7b6.png)

Budget setup overview, reflecting the four budgets

### Step 3: Promote or drop the model

In order to determine whether the model is at the efficiency frontier, we rely on three signals:

1. Benchmark data:We have a set of private benchmarks that test a suite of tasks, including offline benchmarks such as document reasoning, workspace search, and our own Genie product, as well as online benchmarks in which we run two models side-by-side and compare outputs for pull request creation. We continue to expand and tune these benchmarks; in an ideal world, our benchmarks are sufficient to quickly determine the cost and quality of any new model release.
2. User-reported quality:The experimental model release provides a wealth of anecdotal data on how people feel about the new model. We find that a group of power users is eager to try out new models and compare their experiences over Slack and survey responses.
3. Cost tracking via OpenTelemetry traces:Unity Gateway logs all traces in a central location, along with cost information. We can compare how pilot users spent money on the prior generation of models versus the latest models on a per-session basis.  This does not necessarily tell us quality, but it gives us a good measure of the cost.

For Opus 5.5 and Sol 6, all three metrics tell us a pretty consistent story.

Benchmarks, such as ourOfficeQA Pro V2, show that Opus 5.5 is clearly on the cost/quality frontier, a huge step up on both axes from Opus 5. GPT-6 Sol scores somewhere in between GPT-5.6 Sol and GPT-5.6 Terra on both cost and quality.

![](/images/posts/85c4617965ff.png)

User reportsbroadly agree that for engineering and debugging tasks (the vast majority of our early adopters are engineers), Opus 5.5 is a big step up in quality from Opus 5 and Opus 4.8, and its writing style is vastly preferred. Whereas GPT-6 Sol is occasionally a downgrade in quality compared to GPT-5.6 Sol.

Cost trackingallowed us to compare early adopters' usage with the same group's usage a week earlier. Maintaining the same cohort proved crucial because early adopters tend to be power users of AI rather than average users.

We wanted to normalize costs to a $/session basis, since users who are trying out a new model will sometimes increase their usage in terms of number of sessions as they experiment. We found that using a basic $/session comparison was still misleading because the distribution of sessions was also changing: early adopters were tryingharder problemswith the new models than their average session.

[翻译失败，原文如下]

As a result, we stratified sessions based on whether they were single- or multi-turn and whether they made any file edits, and then reweighted the distribution accordingly. The table below shows the results for Opus 5.5 vs. Opus 4.8 and GPT-6 Sol vs. GPT-5.6 Sol.

Cost comparison

Old Model (avg $/session)

New Model (avg $/session)

Delta

Opus 4.8 vs. Opus 5.5

$5.94/session (Opus 4.8)

$4.23 (Opus 5.5)

GPT-5.6 Sol vs. GPT-6 Sol

$4.52/session (GPT-5.6 Sol)

$2.34/session (GPT-6 Sol)

The GPT numbers are not too surprising given that the price was cut by 50%. But we were pleased that Opus 5.5 also represents a significant price reduction for our real workloads, given our prior experience with Opus 5.

## What we decided

We were able to provide employees experimental access to Opus 5 and GPT-6 Sol and Luna on Day 1 of model launch. Within three days, we had gathered enough data to confirm that these models were on the efficiency frontier and decided to move them out of the experimental budget and into standard circulation as generally available models.

Over the next week, we will go a step further for Opus 5.5 to make it thedefaultfor Claude Code, given its clear position as higher-quality and lower-cost than its predecessors.

Our experience with GPT-6 Sol suggests that it will not replace GPT-5.6 Sol as the default for Codex. However, we will include GPT-6 Sol in our smart router’s toolkit, given its cost advantage over 5.6 Sol.

Overall, we found this playbook effective at quickly assessing model quality and cost, enabling us to rapidly adopt the latest models that prove their worth. This flexibility matters now more than ever, with new models arriving almost daily.

---

> 本文由AI自动翻译，原文链接：[How Databricks rolls out frontier models to 12,000 employees on Day 1](https://www.databricks.com/blog/how-databricks-rolls-out-frontier-models-12000-employees-day-1)
> 
> 翻译时间：2026-09-30 08:14
