---
title: When it comes to Governance, Retailers need a control plane for context
title_original: When it comes to Governance, Retailers need a control plane for context
date: '2026-08-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/when-it-comes-governance-retailers-need-control-plane-context
author: ''
summary: '[翻译失败，原文如下]


  *Retail AI is reaching further into the business than ever, into stores, merchandising,
  and daily decision-making, opening up real gains ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:59.648943'
---

[翻译失败，原文如下]

*Retail AI is reaching further into the business than ever, into stores, merchandising, and daily decision-making, opening up real gains in innovation and efficiency, along with a growing footprint retailers now have to govern.*The next bottleneck is trusted context: Retailers hold some of the most sensitive customer data of any industry: purchase history, loyalty behavior, payment activity. That same data is what makes AI genuinely useful for personalization and retention. Retailers need a way to put it to work without losing control of who can access it and how.*Databricks gives retailers one governed layer for AI, so every model, agent, and application draws from the same trusted data and the same cost controls, instead of every team building its own.

Retailers are entering a new phase of AI adoption.

The early conversations around generative AI were often about experimentation. Which model should we try? Which chatbot should we build? Which team should run the first pilot? Could AI improve search, summarize documents, enrich product content, or answer internal questions?

Those were important starting points. Many retailers, grocers, distributors, and consumer-facing companies created real value from those early efforts.

In late 2023, one large distributor we worked with saw an opportunity to combine traditional machine learning and large language models to improve product catalog operations. As new products entered the catalog, machine learning models helped categorize and match items, while large language models generated richer product descriptions.

At the time, that was groundbreaking.

The initiative required a systems integrator, a focused tiger team, and roughly a 100-day sprint to prove the value while the team worked through the mechanics of the architecture, data access, model behavior, and business workflow. It was a highly successful initiative, saving millions of dollars and proving that AI could materially improve a business-critical process.

But it also represented a common first-wave pattern: one team, one use case, one architecture, one focused sprint.

Today, that same kind of AI-enabled workflow is becoming table stakes. The conversation is shifting from “I wonder if AI could solve this problem” to “AI must help solve this problem, and I need the right data quickly so I do not slow down the business.” That shift changes the enterprise challenge.

The next phase of retail AI is not just about having a better model. It is about giving every AI experience the right business context.

## Context is what makes enterprise AI useful

A model without retail context can give a generic answer.

A model with the right context can help a merchant weigh assortment risk, a store leader prioritize the day, or an executive get a trusted answer on sales and margin. For retailers, that context spans everything from inventory and pricing to the permissions and policies that decide who is allowed to see what.

That context is what makes AI useful. But context is also where risk enters the system.

Which data should the AI see? Which business definitions should it trust? Which users are allowed to ask which questions? Which tools can the agent call? Which model should handle the task? How much should that interaction cost? How should the enterprise audit what happened?

That is why retail AI needs a control plane for context, a single layer that governs which data, models, and tools every AI experience can use.

## Governance enables speed

Governance is sometimes framed as the thing that slows teams down. For retailers, the opposite is true.

The purpose of governance is to give more teams more freedom to use AI safely.

If the right controls are in place, every new AI use case does not need to become a one-off security, procurement, and architecture exercise. Teams across the retail enterprise can move faster because model access, permissions, logging, tracking, and cost controls are already built into the platform.

That is the “so what” for AI governance in retail.

It is not governance for governance’s sake. It is governance so employees can use AI more confidently, serve customers better, and make faster decisions with trusted data.

Teams are getting more comfortable with AI embedded in their workflows. They need to be unleashed to explore, build, and deliver results. But unleashing teams does not mean removing controls. It means giving them a governed way to move quickly with the right data, the right models, the right permissions, and the right cost controls already in place.

## The next phase is enterprise-wide AI adoption

In my work with retail technology leaders, I have seen the conversation move through three phases.

1. First, teams asked where to start with generative AI.
2. Then they built focused use cases like product matching, catalog enrichment, search, summarization, internal knowledge assistants, and content generation.
3. Now the conversation is shifting again: how do we scale AI across stores, headquarters teams, and digital channels without creating fragmented governance, uncontrolled model spend, or inconsistent access to enterprise data?

This matters because retail is not a single-user, single-workflow industry.

Most of these employees are not sitting at a desk choosing an AI tool. Their AI experience is embedded, in a store app, a dashboard, a workflow they already use, and it needs to answer a different question for every role. Each function needs different data. Each function has different permissions. Each function may need a different model. Each function has a different cost profile and risk profile.

That is why retail AI cannot be solved by one model.

Retailers need a governed way to deliver many AI experiences across the business while controlling which users can access which data, which models they can use, how much they spend, and how those interactions are monitored.

## The hard part is scaling without losing control

As AI spreads across the enterprise, retailers risk creating a fragmented operating model.

One team uses Claude directly. Another builds a RAG app. Another uses Copilot. Developers reach for Cursor. Business users experiment with Claude Cowork. Data teams stand up their own agentic workflows.

Each tool may have its own model access, data access, logs, permissions, costs, and governance process.

That can work during experimentation. It does not work as the operating model for enterprise AI.

Without a control plane, retailers can quickly end up with:

- Separate model-provider contracts
- Separate AI tools and agent frameworks
- Separate prompt and response logs
- Separate cost centers
- Separate permission models
- Separate places where business logic lives
- Separate answers to the same business question

Retailers spent years trying to reduce fragmentation in data and analytics. AI should not reintroduce the same problem in a new form.

## Retailers need open AI harnesses, not closed AI dead ends

As AI adoption scales, another question is emerging: where should theAI harnesslive?

![definition of AI Agent harness](/images/posts/8166564e657a.png)

Some harnesses are closed. The user gets a packaged AI experience, a default model, and limited control over how data, tools, prompts, costs, and model selection are governed. That may be useful for individual productivity, but it becomes limiting when the enterprise wants to control which models are used, how data is accessed, how costs are managed, and how AI interactions are audited.

Other harnesses are more open. They allow the enterprise to choose the right model for the job, connect to governed data and tools, route model calls through a central gateway, and preserve flexibility as the model landscape changes.

![databricks ai gateway llm endpoints](/images/posts/35aebfbf82c9.png)

That distinction matters.

[翻译失败，原文如下]

In a recent dinner conversation, the CIO of a discount retailer shared that CIO peer groups are actively discussing whether they should procure GPUs to take advantage of lower-cost open-source models. At the same time, teams are already experimenting with different AI surfaces: developers using Cursor and coding assistants, business teams exploring Claude Cowork, enterprise teams evaluating Copilot-style experiences, and data teams building custom agents and applications.

This is the reality for most retailers. AI adoption will not standardize neatly around one model, one assistant, or one vendor.

And when we ask CIOs which model they believe will win, the answer is almost always some version of: “I don’t know.” That is a rational answer. The model landscape is changing too quickly for any CIO to bet the enterprise AI strategy on today’s default model inside today’s preferred tool.

Retailers need model flexibility without model chaos.

They need to support frontier models where quality and reasoning matter. They need access to open-source models where cost, control, or specialization matter. They need to support coding assistants, business agents, associate apps, and custom applications. But they also need a common way to govern access, monitor usage, control spend, log interactions, and ensure AI is grounded in trusted enterprise context.

That is the role of an AI control plane.

## Benchmark the model while maintaining optionality

The model landscape is moving too quickly for retailers to make long-term architecture decisions around a single model provider or a single default assistant.

Databricks researchis finding open-source models handle increasingly complex tasks that would have required premium frontier models not long ago. That matters for retailers, especially grocers and discount retailers, where margins are tight and high-volume AI usage can become expensive quickly.

But the answer is not to assume open-source models are always good enough. The answer is to benchmark.

A product content workflow may perform well on a lower-cost or open-source model. A complex merchandising analysis may require a stronger reasoning model. A store associate assistant may need low latency, tight permissions, and predictable cost. A coding assistant or multi-step planning agent may benefit from a frontier model. The right model depends on the task, the data, the accuracy requirement, the latency requirement, and the cost profile.

This is why retailers need model flexibility without model chaos. The question should not be, “Which model will win?” The better question is, “Which model is best for this job, with this context, at this cost, and with this governance requirement?”

Closed AI harnesses often hide or limit that choice. An open control plane lets retailers benchmark, switch, and optimize models as the market changes.

## A control plane for retail AI context

This is what a control plane looks like in practice. Four Databricks capabilities work together to deliver it: Unity Catalog, Unity AI Gateway, Foundation Model APIs, and Genie.

- Unity Catalog governs the business context: data, permissions, lineage, models, and trusted definitions.
- Unity AI Gateway governs model access: routing, usage visibility, logging, budgets, and rate limits.
- Foundation Model APIs provide centralized access to commercial, open-source, and custom models.
- Genie lets business users ask natural-language questions against governed data, so answers stay grounded in trusted context.

Together, these capabilities help retailers move from isolated AI wins to enterprise-wide AI adoption.

The point is not to force every user into one AI application. It is to give the enterprise one governance and model access strategy that holds no matter which application, agent, or interface an employee is using.

The goal is not to stop teams from using the AI tools they like. The goal is to let teams move faster while giving the enterprise control over the model, the data, the context, the cost, and the risk.

## What this looks like across retail teams

A CIO at a discount retailer recently shared a telling example. Their CEO wanted AI to be grounded in broader company data so it could become genuinely useful for executive decision-making.

That request captures the enterprise AI challenge perfectly. The CEO was not asking for a smarter model. She was asking for one she could trust with the business. The instinct is right. AI becomes more valuable when it understands the business. CEOs want an answer grounded in their own numbers, not generic ones.

The answer is not simply to give every AI tool unrestricted access to every raw dataset. The answer is to give each user the right AI experience, grounded in the right data, with the right permissions, lineage, definitions, and auditability.

![multiple functions that need governed ai](/images/posts/4822f1d99e0b.png)

## Avoiding another disconnected AI layer

Many retailers are already investing heavily in data governance, lakehouse modernization, and trusted analytics. As AI adoption accelerates, the risk is creating a separate AI layer running outside of that governed data estate.

That can introduce real problems.

- Business logic can get duplicated outside the data platform.
- Permissions may need to be recreated in multiple systems.
- AI agents may access data without consistent lineage.
- Model usage can spread across separate providers and contracts.
- Cost visibility can become fragmented by team or application.
- Prompt and response logs can become disconnected from governance workflows.

Retailers should avoid recreating the same fragmentation that many spent years trying to eliminate in data and analytics.

The future of agentic retail mandates that AI come to the governed data, not move business logic, permissions, and trusted context into another disconnected layer.

![image of a core gateway with boxes off to the side](/images/posts/6c30bd447ce3.png)

For retailers already investing in Unity Catalog, the next step is to govern the AI systems built on top of it. Do that, and every new AI use case inherits the same permissions, audit trail, and cost controls already in place, instead of starting from zero.

## The business outcome: more freedom with more control

With a governed AI control plane, retailers can let teams move faster with freedom while maintaining enterprise control. Every function gets AI built for how it actually works, from the store floor to the finance team, without waiting on a one-off security or procurement review to get there.

At the same time, IT leaders can maintain visibility into who is using which models, what data is being accessed, how much each workflow costs, and how AI interactions are governed.

That is the balance retailers need. Not one chatbot. Not one model. Not another disconnected AI platform.

A control plane for context.

---

> 本文由AI自动翻译，原文链接：[When it comes to Governance, Retailers need a control plane for context](https://www.databricks.com/blog/when-it-comes-governance-retailers-need-control-plane-context)
> 
> 翻译时间：2026-08-19 03:07
