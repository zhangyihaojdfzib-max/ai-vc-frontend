---
title: The Cost Curve of Intelligence
title_original: The Cost Curve of Intelligence
date: '2026-11-20'
source: Unusual Ventures
source_url: https://www.unusual.vc/the-cost-curve-of-intelligence/?utm_source=rss&utm_medium=rss&utm_campaign=the-cost-curve-of-intelligence
author: ''
summary: '[翻译失败，原文如下]


  ###### November 19, 2026


  # The Cost Curve of Intelligence


  ![The Cost Curve of Intelligence](/images/posts/b7bc3bb48676.png)


  Model pric...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:30:09.838538'
---

[翻译失败，原文如下]

###### November 19, 2026

# The Cost Curve of Intelligence

![The Cost Curve of Intelligence](/images/posts/b7bc3bb48676.png)

Model prices fell about 13x last year. The savings still to come are in the system that serves the model and the sandbox environment the agent works in, and that’s where Unusual is looking for the next infrastructure winners.

PERSPECTIVES · INFRASTRUCTURE · TEAM UNUSUAL · OCTOBER 2026 · 8 MIN READ

## The price of a good answer fell 725x in eighteen months

Organizations have spent three years choosing AI models by quality, and for most of that time that was right. Model capability has not saturated. The horizon over which a model can work autonomously, from a single answer to a multi-hour task, keeps lengthening, and we expect it to keep lengthening. What has changed is what happens underneath that frontier: the price of a fixed level of capability now falls for years after the capability itself stops being news.

Epoch AI’s September 2026 study,The plunging price of thought, puts a number on it. Since 2023 the cost of a fixed level of AI performance has fallen about 47 percent per quarter, roughly 13x per year, four times faster than DNA sequencing and eighteen times faster than lithium batteries. In January 2025 OpenAI’s o3, then the leading and largest model, scored 75 percent on GPQA Diamond at an estimated 30 cents per question; under eighteen months later GPT-5.6 Luna, a smaller and cheaper model, matched it for $0.0004 per question, a 725-fold drop.

That example measures the model alone, and the model is now only part of the price. The cost of intelligence is set by the system that serves a model at least as much as by the model itself. Models are called inside agent loops thousands of times per task, and the time a user waits for finished work depends on the queue, the cold start, the sandbox and the test suite as much as on the weights. The metrics providers advertise, price per million tokens and aggregate throughput, measure a single call, and a task is a loop.

Two Unusual portfolio companies,FalandLithos, have built their businesses on the serving system and the environment, and their published numbers are the clearest evidence we have of how much slack is left in each.

## What is the cost curve of intelligence?

The cost curve of intelligence is the price of a finished unit of AI work over time, at a fixed level of quality. Most people use the phrase to mean the price of a token, but a unit of work costs more than its tokens. Its price is set by three layers, and the last two now matter more:

- The modelsets the price of a given quality level. Epoch measures it and the public price indexes track it.
- The serving systemsets the latency and cost of delivering that quality to one user under real load. A new category of infrastructure company has formed around it in two years.
- The environmentsets the cost of everything an agent does between model calls: starting a sandbox, running tests, saving progress, recovering from a failed attempt. It’s where the next big drop will come from.

## The model

The price of a fixed quality keeps falling after the quality stops being news, and open weights now cap what any provider can charge for it.

Epoch separates two rates: a level’s cost falls about 66 percent per quarter when it first becomes state of the art, and about 32 percent per quarter two years later, once the launch premium has competed away. The market indexes agree:Silicon Data’s indexof realized prices fell 43 percent in the ten weeks to early August 2026, driven by a price war and by low-cost open-weight models from Chinese labs.

The slack here sits in open weights. In July 2026 Moonshot AI released Kimi K3 at $3 per million input tokens and $15 per million output, against $5 and $25 for Opus 4.8 and $5 and $30 for GPT-5.6 Sol, while placing first or second on five of six coding benchmarks in Moonshot’s own reporting. AsLithos’s analysis of the launchnotes, for a closed model the API price is the least a customer will pay; for an open-weight model it’s the most, since many providers compete to host the weights. Once the weights are open, the remaining cost advantage belongs to whoever serves them most efficiently, which moves the slack to the serving system.

Buyers have already adjusted. Nobody picks a single model anymore; teams deploy different models for different points on the Pareto frontier of quality, price and latency: a frontier closed model for the hardest step, an open-weight model for the bulk of the loop, a small fast model for routing. The frontier keeps moving outward, but at any moment it is a curve, not a point.

## The serving system

The largest remaining gains are in the system between the weights and the user, and they’re being delivered on commodity GPUs.

The serving system is everything between a set of trained weights and a user who’s waiting: kernels, scheduler, weight caches, autoscaler and queue. For three years it was treated as plumbing, because the model was the slow part. In 2026 it’s where a new category of infrastructure company has formed, and the market prices it accordingly. The table draws onContrary Research’s September 2026 review, updated for the rounds announced since.

Sources: Contrary Research, September 2026; company announcements and press reports through November 2026. Private-company figures are reported, with no audited financials behind them.

Valuations track revenue closely, and the companies are specializing by workload.Lithos, which serves open-weight language models for agent loops and hasn’t announced financing, belongs with the language-and-agents group.

The gains come from a handful of techniques that spread across the industry within weeks of publication: speculative decoding (DSpark, open-sourced in June 2026, was in production at Fal and Lithos within weeks), megakernels that run a whole forward pass as one dispatch (Lithos’s open-source implementation for Apple siliconserves a 27-billion-parameter model at more than 200 tokens per second on an M5 Max), weight streaming (Fal’s FlashPack), new number formats on Blackwell (Fal’s MXFP8 quantizer) and multi-node serving with smart routing.

The physics differ by workload, which is why the specialists have diverged and why we expect them to stay diverged. A video frame from a diffusion transformer is bound by compute per sampling step; a token from a mixture-of-experts language model is bound by memory bandwidth, since the active weights are read once per token. Those are different engineering problems with different winning techniques, and diffusion transformers will continue to need a separate serving stack from MoE LLMs. A platform that treats them as one workload gives up the gains that move the curve.

The two companies we know best sit on either side of that divide.Fal cut Ideogram V4’s generation timefrom 2.75 seconds to 0.44 seconds with no visible quality loss, and its H3 Max video modelgenerates a five-second clip in under three seconds, the first to run faster than playback at frontier quality.Lithos serves Kimi K2.7 Code, a one-trillion-parameter model, at more than 1,000 peak tokens per second per user on a standard eight-GPU B200 node, against the 80 to 200 typical GPU serving delivers, and it does so at native precision.

One line runs through both: the gains are delivered on commodity GPUs. OpenAI’s launch of GPT-5.6 Sol highlighted serving it on Cerebras at up to 750 tokens per second; Lithos clears that on a standard NVIDIA node. The deeper point is where the advantage lives. The fastest inference companies in the world will circumvent CUDA, writing their own kernels and schedulers against the hardware rather than through the vendor’s libraries, which is what lets the team that saturates a B200 ship a megakernel for Apple silicon months later. An advantage in software compounds with every hardware generation instead of being tied to one vendor’s roadmap.

[翻译失败，原文如下]

Both companies treat quality as a fixed constraint: Fal ships an optimization only when the model keeps its rank in its quality evaluations, and Lithos serves the weights the model shipped with. They’ve also proposed the measurements. Fal separatesinference latency from end-to-end latency at scale, which adds queueing and cold starts (in Fal’s published example, loading weights was 496 seconds of a 524-second start), and Lithos proposestime to useful work, driven by tokens per second per user, since a cluster can produce enormous aggregate throughput while each agent crawls.

## The environment

Once the model call is fast, the time between model calls is the loop, and the first big cut has already been made there.

Once inference runs at 1,000 tokens per second per user, an agent’s loop is dominated by what happens between model calls: starting a sandbox, running tests, saving progress, recovering from a failed attempt. The sandbox providers that grew up alongside coding agents treated those operations as fixed overhead measured in seconds, which was fine while inference took longer and the loops around it were simple, with few tool calls between model turns. It isn’t fine anymore, and the first evidence comes from an inference company: in October 2026 Lithos releasedLithosBox, explaining that as inference gets faster, managing the environment becomes a larger share of the time to finish a task.

LithosBox gives an agent Git-like control over a running environment: snapshot the live state of a sandbox, including running processes, branch that checkpoint to try alternatives in parallel, and restore it when an approach fails. Source control has offered those operations for code for decades; what LithosBox changes is their cost for a live environment.

Source: Lithos, October 2026. Only LithosBox restores running processes; the others restore files. Vendor numbers against competitors the vendor chose.

The interesting number is the snapshot. At 95 milliseconds a checkpoint is cheap enough to take routinely, so an agent can try several patches in parallel branches, run the tests in each and roll back whatever failed. At four to seven seconds the same operation is something an agent is designed to avoid. The environment has the same structure the serving system had two years earlier: an operation everyone treated as fixed overhead turns out to be mostly waste, and removing it changes what agents are built to do. Tokens per task will rise again, and the Jevons paradox repeats a third time.

## What this means for founders

Model prices, serving systems and agent environments have all followed the same sequence. We call it the overhead cycle: an operation the market treats as fixed turns out to be ten times slower than it needs to be, a small team with deep systems expertise fixes it, and demand expands into the space that opens up. The cycle points to a few conclusions.

- Plan for demand to outrun the price decline.The Jevons paradox has held at every turn of the cycle, and compute stays scarce through 2027. Usage-based pricing captures the volume; per-seat pricing is priced against a floor that keeps dropping.
- Measure the loop your users wait through.Instrument end-to-end latency per user and time to useful work from day one. If you can’t see where a user’s time goes, you can’t sell them the improvement.
- Let software compound on commodity hardware.Custom silicon buys a fixed advantage tied to one roadmap. Kernels and schedulers written below the vendor’s libraries ride every hardware generation.
- Look for the next operation everyone treats as fixed.Inference in 2024, cold starts and queueing in 2025, the sandbox in 2026. Next: tool execution, retrieval, memory and evaluation.
- Watch for thresholds.Real-time media became a category when generation crossed playback speed; long-horizon agents will become one when a task fits between two human check-ins.

One observation about the people who find this slack: in both cases we know best, the insight came from technical depth in the system itself. Fal’s founders first set out to build compute infrastructure for Python and pivoted to generative media after noticing that their customers’ image models were slow; Lithos’s founders aresystems researchersin GPUs, operating systems and hardware-software co-design. We expect the next winners to look like them.

## Why Unusual, and how to reach us

The cost of intelligence will keep falling, and the useful question is where the next drop comes from.Unusual Venturesbacks infrastructure founders at the earliest stage, when the thesis is a measurement nobody else has taken yet and the product is a few people who know how to act on it. Fal and Lithos are both in our portfolio because we saw that profile before the market priced it, and working alongside them is how we developed this view. We’ve spent years in the systems layer underneath AI, and we think the next infrastructure winners will come from it: companies that make the serving system and the environment as cheap as the model has become.

If you’re building in any of these layers, or removing slack that everyone else treats as fixed,we’d like to hear from youearly, before the round, when a conversation can still shape the company. Reach the Unusual investment team atunusual.vc/contact-us.

---

> 本文由AI自动翻译，原文链接：[The Cost Curve of Intelligence](https://www.unusual.vc/the-cost-curve-of-intelligence/?utm_source=rss&utm_medium=rss&utm_campaign=the-cost-curve-of-intelligence)
> 
> 翻译时间：2026-11-20 09:30
