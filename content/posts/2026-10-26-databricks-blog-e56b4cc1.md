---
title: The media industry is becoming a prediction economy
title_original: The media industry is becoming a prediction economy
date: '2026-10-26'
source: Databricks Blog
source_url: https://www.databricks.com/blog/media-industry-becoming-prediction-economy
author: ''
summary: '[翻译失败，原文如下]


  • The prediction economy is the shift in media and advertising from counting attention
  to predicting and proving outcomes. Performance be...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-27T07:09:11.207201'
---

[翻译失败，原文如下]

• The prediction economy is the shift in media and advertising from counting attention to predicting and proving outcomes. Performance becomes a leading indicator instead of a lagging one.• Agents and measurement stall on fragmented data. Only 3% of CMOs can tie half their marketing to a business outcome (McKinsey), and the fix is one unified, governed data and AI foundation.• Build it on four Cs: context (Databricks CustomerLake, an agentic CDP; Genie; Lakebase), control, cost, and choice (Unity Gateway). A pet specialty retailer that activated loyalty data with agents saw a 12% lift in transactions.

For two decades, media and advertising ran on attention. Impressions, reach and clicks were the currency because they were quantifiable. Increasingly, though, that currency is losing value. Throughout the industry – and brought to a head at Advertising Week New York – leaders across media, agencies, and adtech/martech are asking the same question: not "who saw it?" but "what did it change?"

Behind every answer is the rise of theprediction economy, where advantage comes from knowing what an audience will want before the money is spent, and being able to show what it was worth. Performance has shifted from a lagging indicator to a leading one.

Hear Databricks Media and Advertising GTM leader Jake LaDuke share his thoughts on the prediction economy - and the future of media, advertising and marketing - then read on to learn more.

## What the industry is asking for

A few themes deserving attention:

Agents are moving from answering to acting.Session after session, conversation after conversation on agentic AI reaches the same conclusion: agents fail without trusted, governed data underneath them. The early wins are as much about effectiveness as efficiency, such as orchestrating measurement across many sources of truth. On the sell side, roles like VP of ad sales transformation barely existed two years ago, as agents take over the spreadsheets, emails and stale rate cards of pitch-to-pay so sellers can focus on relationships and yield.

Measurement has to prove impact.According to a McKinsey study,only 3% of CMOs can tie half their marketing to a business outcome. That mandate is rippling through the ecosystem: agencies are restructuring contracts, adtech is building proof into its products, and publishers are launching their own measurement. The hope economy is giving way to the prediction economy, and the loop only closes if partner data can connect.

Martech and adtech are collapsing into one stack.With 90 to 120 tools in a typical enterprise stack, channel-level reporting no longer cuts it. CMOs need holistic performance across every touchpoint, not just advertising or marketing alone. Meanwhile CMOs and CROs draw on the same audiences from separate stacks, and collapsing the two lets both do better.

CTV and retail media need closed loops.Publishers need one data estate for audience intelligence, monetization and cross-platform measurement. Retail media, a fast-growing channel still held back by measurement, needs clean rooms, first-party activation and closed-loop measurement.

Behind all of it, consumer behavior is shifting faster than the stack. Agentic commerce, AI-generated creative and LLMs acting as the new influencer are changing how people discover brands, and executives want to treat these shifts as opportunities, not threats.

Every one of these points back to the same prerequisite: a unified, governed data and AI foundation. When your data is fragmented, adapting to the prediction economy becomes untenable. Leaders must stop funding these as separate projects and instead build one foundation for every persona to draw on.

## Context is where prediction starts

Every prediction starts with context: how complete a view your agents have of your customers and your business across your data estate. As Databricks CEO Ali Ghodsi has put it, models don’t have an intelligence problem, they have a context problem.

PetSmartshows what happens when that context comes together. Using loyalty data from its 75 million Treats Rewards members, the company moved beyond batch-and-blast campaigns, and AI decisioning agents delivered personalized messaging at scale. The result was a 22% incremental lift in salon bookings and a 13% lift in auto-ship transactions. The gain came from getting the data estate to work together, not from a smarter model.

Nowhere does context matter more than in the customer 360. Marketers increasingly want to run marketing where they run the business, rather than copying golden profiles into a separate CDP. That is the idea behindCustomerLake, Databricks’ agentic CDP. Marketing and data teams can build trusted Customer 360 profiles, activate audiences and personalize engagement directly on their governed data.Paired with measurement orchestration, those same customer signals connect directly to ROI.

Geniethen brings that context to the people making decisions. It acts as an AI coworker connected to your governed enterprise data, so planners, marketers and sellers can ask questions in plain language and get answers built on their own definitions. Under the hood,Genie Ontologygives the AI an understanding of your business: its unique definitions, relationships, business rules, authoritative sources and permissions. At answer or decision time, it ranks that context by authority and relevance, applies permissions, and delivers the most useful pieces.

![ontology architecture](/images/posts/6031ab5aa7ce.png)

Acting intelligently in the moment also takes operational context: what the customer just did, what they were offered, and what the agent decided and why.Lakebase, Databricks’ serverless Postgres database, keeps that live state next to your analytical data, so agent memory, decision history and fresh features are available at production speed without brittle pipelines in between.

Getting there starts with a simple discipline: define identity, audiences and metrics once, and govern them centrally.

## Control, cost and choice: from token maxing to value maxing

Context gets you to a prediction. The other three C's decide whether you can afford to act on it at scale, and whether you should.

Control.This is about governing not only who has access from a people perspective, but also from your agents' perspective. Agents will touch audience data, bids and brand-sensitive placements, so governance has to be the front door.Unity Gatewayruns every model and agent request through one control plane, with authentication, auditing and PII guardrails, so the enterprise sets the guardrails and the platform enforces them.

Cost.AI for AI's sake is no longer tolerated by CFOs, and the shift is from token maxing to value maxing. Every agent loop burns tokens, and always-on campaigns multiply that. Unity Gateway attributes spend by team, model and application, enforces budgets and rate limits, and routes simple requests to cheaper models, so AI cost tracks business value.

Choice.Having the right model for the right job matters because frontier models leapfrog each other regularly. If switching means rewriting applications, you are always a generation behind. Unity Gateway offers models from multiple providers through one API, so you can swap by configuration instead of re-engineering. Built on open formats, the foundation keeps your data portable, andOpenSharingandDatabricks Clean Roomslet you collaborate with partners without copying data

Leaders should treat governance, cost visibility and portability as design requirements from day one, not retrofits.

## Think big, aim small

[翻译失败，原文如下]

Looking ahead, advertising itself will change. With ad avoidance rising and intent still largely untapped, it must shift from feeling like a break in what people want to do to a more intelligent, integrated 1:1 experience driven by that viewer’s intent. Getting there will take new operating systems and operating models across brands, agencies, adtech and publishers, all in service of outcomes.

Moving forward, leaders need to think big about how AI can be a growth lever for the business, then aim small on the use cases you unlock first, whether that's audience planning, activation or measurement orchestration. Start with the why: a new revenue stream, lower costs or simpler operations. Not every problem needs an agent.

Pick one meaningful decision, such as reactivating lapsed customers, packaging an audience for a buyer or closing the loop on a retail media campaign. Assemble the context, set the guardrails, agree up front on how you will measure impact, and expand from there. Those who go furthest fastest will be business people growing more technical and technical people growing more business-centric, building on trusted context, real control, the freedom to choose, and costs that scale with value.

Ready to get started?Watch the video with Beet.TV,listen to the podcast with Advertising Week, and learn more atDatabricks for Media, Advertising, & Entertainment.

Media & Entertainment

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[The media industry is becoming a prediction economy](https://www.databricks.com/blog/media-industry-becoming-prediction-economy)
> 
> 翻译时间：2026-10-27 07:09
