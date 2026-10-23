---
title: The AI Bill is coming
title_original: The AI Bill is coming
date: '2026-10-22'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ai-bill-coming
author: ''
summary: '[翻译失败，原文如下]


  - The cost curve is structural. AI tools are consumption-priced, so usage grows
  exponentially while revenue doesn’t. Unlimited tokens and...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-23T07:13:52.781053'
---

[翻译失败，原文如下]

- The cost curve is structural. AI tools are consumption-priced, so usage grows exponentially while revenue doesn’t. Unlimited tokens and hard spend caps both fail, and Databricks has moved to visibility plus progressive friction instead.
- Four levers cut unit costs by as much as 90%. Shift defaults to more efficient models, route each task to the cheapest model that can handle it, give developers visibility into their spend, and cut token overhead. Token price alone is a poor predictor of what a model actually costs.
- Every engineering org needs a control layer. An AI gateway sits between developers and models to handle access, routing, budgets, and tracing, making AI spend observable, steerable, and predictable.

In this conversation, Catherine Brown talks with Patrick about what happened when Databricks went all in on AI coding agents: how costs initially spiraled with growing usage , what actually brought unit costs down by as much as 90%, and why every engineering organization needs a control layer between its developers and its models. That control layer started as an internal fix for Databricks' own AI bill, and it became the inspiration forUnity Gateway.

## Engineering output is the bottleneck

Catherine:You run Databricks' AI products, and you've also been the internal champion for AI adoption. Why has this become such a personal priority for you?

Patrick:Because engineering output is the main bottleneck in our business. Every company needs its engineering team to move faster, and if you can give them something that meaningfully improves their productivity, that's worth a lot. The early chat products were somewhat useful. But the ROI really changed maybe a year ago, when the first really good coding models showed up.

Catherine:How do you know whether you are getting productivity wins from AI tools?

Patrick:We track a bunch of output metrics: pull requests, features shipped and lines of code. None of them is perfect on its own. I think of R&D as a big machine. You put resources in, you get features and code out, and you can measure how much more is coming out. In aggregate, we're close to doubling output with the same team. The teams that rebuilt their processes around AI are going a lot faster than that.

## From Tokenmaxxing to ValueMaxxing

Catherine:When Databricks first rolled out AI coding tools, what did you get wrong?

Patrick:It's kind of funny because at the start, we had the opposite problem. Nobody wanted to try the new stuff. I was going around bugging people. So we did what everyone did, which was remove every barrier: the most expensive model, as many tokens as you want. I think that came from a good place. You're trying to get people over the hump.

Then people actually started using it, and we saw this exponential cost curve. These tools are all consumption-priced now, not per seat, so a single user can, in principle, spend an unbounded amount of money. They can run a little loop on the most expensive model and go to lunch. Maybe that loop is doing something really valuable, but maybe it’s just burning tokens. If your costs grow exponentially and your revenue doesn't, at some point, you have a problem. We got to the point where the costs were threatening to reverse the efficiency gains, which were the whole reason we did this.

That's when I got very involved personally. I compared notes with leaders at other technology companies who I knew were adopting AI at scale (Coinbase, Uber, Stripe, and others). Collectively, many of us were pursuing similar techniques. Today, at Databricks, our token spend per head is roughly flat now, even as total usage and value keep going up.

## Stop putting hard caps on your best developers

Catherine:Most companies' first instinct is a hard spend cap. You tried that. What happened?

Patrick:It's the obvious first move, and you do want the mechanism. But a hard stop is a bad experience. You cut someone off mid-task, and they lose their flow, maybe hours of work. And the people hitting the cap are often your best users. Cut them off, and some of them just go use a personal account, and now you can't see anything.

So we moved to friction that ramps up, and Unity Gateway handles all of it. First, a warning, then an approval, then we downshift you to a cheaper model so you can keep working. Actually cutting someone off is a last resort. We also send everyone a regular breakdown of their own spending with suggestions on where to save. That alone is worth about 10%. One company I know of puts the model and the cost right in every pull request. So it's basically public shaming if you use an expensive model for a small thing. I love it.

## The best cost optimization is one developers never notice

Catherine:You'vewritten aboutfour levers for bringing these costs down. Which one has had the biggest impact?

Patrick:Our favorite one is kind of boring: better, cheaper models keep coming out, and you move traffic to them. There are probably five models released every week between the proprietary and open source vendors. Not every one is a step forward on cost, but maybe one every week or two is. It's a rising tide. You get the same output for less money, and nobody has to change anything. No fancy routing, nothing.

To give you a sense of how fast this moves: one of the recent cheap models roughly matches what a frontier model could do about nine months ago, at around 1% of the cost per task. That's a 100x drop in under a year. That's still preliminary, but it's the direction.

The catch is you have to actually move. If a new model comes out and nobody in your company is using it, it's a tree falling in the woods. So we got good at evaluating new models fast and shifting workloads over when one is good enough. Because everything goes through Unity Gateway, we can make that switch in one place, and developers don't have to change anything. That's been the most impactful thing we've done, 50% or more on its own. Add routing, spend visibility, and cutting token overhead, and in some cases, our unit costs are down as much as 90%.

## A model's token price is a bad predictor of what it costs

Catherine:Your teambenchmarks coding agents against Databricks' own multi-million-line codebase. Why not just trust the public benchmarks?

Patrick:Public benchmarks don't tell you much about your own code. The tasks leak into training data, and they don't look like a big enterprise codebase. So we built our own from real pull requests in our repo, and we grade by actually running the tests. We don't use an LLM as the judge, because that tends to reward sounding right over being right.

Some of the results surprised people. An open source model, GLM 5.2, tied Opus 4.8 on quality at about a third less per task. One model that was 1.7x cheaper per token cost more per task, because it burned through more tokens. And the harness, the coding tool around the model, mattered about as much as the model. Same model, different harness, more than 2x difference in cost. Just tuning our harness and caching settings saved us close to 50%.

## Frontier models are for frontier problems

Catherine:The gap between the cheapest and most expensive models can be 100x. How should engineering leaders think about that range?

Patrick:Think of it like cars. There's the Lamborghini, the Honda, and the bicycle. You don't need the Lamborghini for every trip, and most coding work doesn't need the biggest model.

Astra was a good example. We rolled it out to every engineer, around 3,500 people, and as far as we know, we're the first company toshare a rollout like that publicly. It was clearly better on the hard stuff, like system design. But spend went up about 60%, and it wasn't obviously helping on everyday tasks, which the existing models already handle fine. A lot of that was waste, people using Astra for things they should've used another model for. So we gave it its own budget in Unity Gateway. Use it for the hard problems.

[翻译失败，原文如下]

Long term, I don't know which way this goes. Cheap models keep taking over more of the routine work, but people are also throwing harder and harder problems at AI. That's kind of the point. You want to be able to steer either way.

## Model routing is the new AI battleground

Catherine:You've argued that AI cost is an infrastructure problem, not a procurement problem. Why can't budgets and policy solve it?

Patrick:Budgets help, but a budget can't decide which model should handle a given request. That's routing. Renaming a component goes to a cheap model; a hard, open-ended problem goes to a capable one. OurSmart Routercuts average task cost by more than 30% at roughly the quality of the most expensive model. It's also allowing us to stop asking users to decide when to use the more expensive models… that just happens.

To do any of this you need a layer between your developers and the models. We built ours because we had to. All our coding tool traffic goes through one gateway, whether it's Claude Code, Codex, Cursor, orOmnigent, our meta-harness. That's what let us actually see where the money was going. Then we realized every customer had the same problem, so we productized it as Unity Gateway. Thousands of customers use it now.

Catherine:Will routing end up as competitive as the models themselves?

Patrick:That's our view. As margins on the models get thinner, figuring out which model to use for what is a pretty interesting place to be. The routing models have to be tiny and fast. It's also just hard to do well. There are a lot of open research problems in the practical side of using these models, and I think there's real IP in getting it right.

## You can't optimize what you can't see

Catherine:If you could give one piece of advice to a CTO staring at a growing AI bill, what would it be?

Patrick:Figure out where it's going. Most companies can't tell you what they're spending on AI by team or by model, let alone whether it's paying off. Put a gateway in front of your models so all the traffic goes through one place, and you can see it. Everything else gets easier after that. And don't slow down. The productivity gains are real. But this stuff compounds, and if you wait, the bill is going to be a lot bigger than you think.

## The AI bill is coming, but it doesn't have to win

Patrick's message to engineering leaders is that you don't have to choose between AI productivity and cost control. The companies getting this right keep broad access to the best models, test new models on their own code, move to cheaper ones as soon as they're good enough, and give developers visibility instead of walls. Underneath all of it is one control layer, a gateway, that makes AI spend something you can see and steer. At Databricks, that layer became Unity Gateway.

To learn more about how Databricks manages its own AI coding spend, read Patrick's blog "Managing AI Coding Costs at Scale," and tryDatabricks Unity Gateway.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[The AI Bill is coming](https://www.databricks.com/blog/ai-bill-coming)
> 
> 翻译时间：2026-10-23 07:13
