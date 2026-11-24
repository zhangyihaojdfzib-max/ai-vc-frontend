---
title: What Kind of Factory Will You Build?
title_original: What Kind of Factory Will You Build?
date: '2026-11-22'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/what-kind-of-factory-will-you-build/
author: ''
summary: '[翻译失败，原文如下]


  In short :A software factory has four components: a shared context, skills & specs,
  an execution trace, & a curator loop that rewrites th...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-24T12:12:07.723352'
---

[翻译失败，原文如下]

In short :A software factory has four components: a shared context, skills & specs, an execution trace, & a curator loop that rewrites the system from the trace. Notion's A New Shape for Work & LangChain's knowledge factory describe the same loop for company knowledge. The architecture generalizes to marketing & sales factories, so the open question is what kind of factory to build.

Before AI, we wrote software line by line. After AI, the best engineering teams stopped writing code & started building software factories : systems that write, test, & ship the code for them.

So why don’t other teams build factories?

They are. On November 21, Notion published “A New Shape for Work”1& LangChain published “How to Build a Knowledge Factory”2. One is a manifesto, the other a build guide. Both describe the exact same four-step loop applied to company knowledge : context, agent, trace, curator.

This is the plan for shipping a factory.3

![Every AI factory runs the same four-step loop : context, agent, trace & curator](/images/posts/829b55dfd8a8.jpg)

Notion puts it bluntly :

“This structure is among the most valuable IP any modern organization can have, because it defines the limit of what is possible for agents to do within that company.”

LangChain frames the same loop from the other side :

“The goal isn’t to document everything before agents can start working. It’s to build a system where doing the work reveals what knowledge is missing, & resolving those gaps makes future work better.”

A software factory has four components. A shared context : the specs, docs & history an agent reads before it starts. An agent that runs the skills & specs to do the work. An execution trace that flags what shipped, what broke, & what it cost. A curator loop that reads the trace & rewrites the skills & specs for the next run.

The last two steps compound. A prompt with a document attached is a one-off. The trace turns the work into data. The curator turns the data into a better system. That is the difference between a factory that improves every week & a workflow that stays flat.

The loop is not a vendor’s idea. It is what the work looks like once an agent does most of it. A knowledge factory has the same four parts as a code factory. The context is the docs. The agent is the answer. The trace is the wrong answer. The curator is the fix.

Once you see the loop, it generalizes everywhere. A marketing factory turns campaign performance into better copy. An online ads factory turns ROAS4traces into new creative. A sales pitch factory turns call transcripts into sharper decks.

Satya Nadella described the same shift at Microsoft Ignite5:

“The new company looks like there’s a founder. The founder has a token budget. Then the founder hires somebody. That person also comes in, & then they have a token budget, & they figure out how to add the tokens & the wages & then keep building.”

Factories are still rare because a factory is an operations project, not a model purchase. Someone has to own the context, write the specs, read the traces & run the curator on a cadence. This is the reinvention of work : defining & operating the factory for each team.

Different departments, identical architecture. The question is no longer whether AI can do the work : it is what kind of factory you will build.

1. A New Shape for Work, Notion, Nov 21, 2026.↩︎
2. How to build a knowledge factory, LangChain, Nov 21, 2026.↩︎
3. Neither post includes a benchmark, a customer result, or independently verified outcome. Both are vendor arguments about architecture.↩︎
4. Return on ad spendmeasures revenue generated for each dollar spent on advertising.↩︎
5. Satya Nadella, Microsoft Ignite roundtable, Nov 17, 2026.↩︎

A New Shape for Work, Notion, Nov 21, 2026.↩︎

How to build a knowledge factory, LangChain, Nov 21, 2026.↩︎

Neither post includes a benchmark, a customer result, or independently verified outcome. Both are vendor arguments about architecture.↩︎

Return on ad spendmeasures revenue generated for each dollar spent on advertising.↩︎

Satya Nadella, Microsoft Ignite roundtable, Nov 17, 2026.↩︎

---

> 本文由AI自动翻译，原文链接：[What Kind of Factory Will You Build?](https://tomtunguz.com/what-kind-of-factory-will-you-build/)
> 
> 翻译时间：2026-11-24 12:12
