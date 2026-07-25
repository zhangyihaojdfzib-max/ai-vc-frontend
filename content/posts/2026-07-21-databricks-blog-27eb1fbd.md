---
title: 'The last mile: why great first-party data still doesn''t make great marketing'
title_original: 'The last mile: why great first-party data still doesn''t make great
  marketing'
date: '2026-07-21'
source: Databricks Blog
source_url: https://www.databricks.com/blog/last-mile-first-party-data-great-marketing
author: ''
summary: '[翻译失败，原文如下]


  *The martech stack is broken by design. Decades of layered, siloed tools have left
  marketing teams unable to activate the customer data s...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-25T05:00:51.529850'
---

[翻译失败，原文如下]

*The martech stack is broken by design. Decades of layered, siloed tools have left marketing teams unable to activate the customer data sitting in their modern data platforms — creating a costly gap between data infrastructure investment and actual campaign outcomes.*The composable canvas closes the gap, but only with the right approach. Databricks provides the unified data foundation and the Agentic CDP that eliminate integration bottlenecks; the last mile requires building the bridge between that foundation and real-time, AI-powered marketing execution.*Brands building on this architecture today are already winning. From automating manual data workflows that consume entire weekends, to deploying AI agents that trigger personalized campaigns from live data signals, the composable marketing future is being built now — not in three to five years.

Last month, a data team and a marketing team sat in the same room and talked past each other for 45 minutes.

The engineers spoke in Delta tables and medallion architecture. The marketers spoke in journeys, segments, and send time optimization. Same customer. Same data. Two completely different languages. Nobody was wrong. They just couldn't hear each other.

That dead space — between where data lives and where it activates — is where millions of dollars in customer value go unrecovered every week, at companies with world-class data infrastructure and world-class marketing ambitions. They have the rocket ship. They forgot the launchpad.

Scott Brinker's research report,The New Martech "Stack" for the AI Age, published in partnership with Databricks, puts the right name on what needs to replace the architecture that created this problem. He calls it the composable canvas. The diagnosis is exactly right, and the direction it points is exactly where this partnership is built to go.

## What the composable canvas actually means for marketers

If you've ever exported a CSV from your data warehouse, emailed it to the campaign team, and waited three days for it to get uploaded into your marketing platform — that's the old stack model failing you.

For two decades, martech was built in rigid vertical layers: data at the bottom, systems of engagement in the middle, campaigns at the top. Each layer was its own box. Getting those boxes to talk to each other required pipelines, connectors, sync jobs, and teams of people whose entire job was moving data from one system to another. As Brinker's report notes, integration remained a top-three challenge for the majority of marketing organizations surveyed — not in 2015, but in late 2025. After thirty years of vendors promising to solve it.

The composable canvas is the architectural alternative: a unified data foundation where every tool, from your customer engagement platforms, to your AI agents, to your analytics, operates on the same shared substrate, without data ever having to move. No middleware. No lag. No Sunday night spreadsheet ritual.

Bryce Peake, former VP of Marketing Decision Sciences at Domino's, puts it plainly:

Modern data platforms like Databricks provide an open, shared foundation that marketers, agents, and apps can all operate on together. And the business case is concrete: "Speed: From months to minutes. Today, adding a new marketing capability means integration projects, data pipelines, and IT tickets. In the composable canvas, new tools and AI agents plug into a shared data foundation instantly."

## The architecture: five rings, one center of gravity

Brinker's framework organizes the composable canvas into five concentric rings, each with a distinct role.

![Scott Brinker's 5 rings ](/images/posts/d770721587ce.png)

- Data Core:the unified foundation of customer, company, content, code, and control data; the gravitational center of everything
- Semantic Layer:shared definitions that make data consistent and meaningful across every system that touches it
- CaaS (Context-as-a-Service):platforms like CDPs that package relevant data and context for the apps and agents that need it
- Decisioning:where AI engines optimize next-best actions and resolve contention when multiple agents want to reach the same customer simultaneously
- Apps & Agents:the outermost ring, where customer experiences actually get delivered

The payoff of this structure is a dramatic reduction in integration complexity. In the old point-to-point model, ten systems could require up to 45 integrations. In the composable model, each new capability joins a coherent shared ecosystem rather than a web of brittle pipelines. As Rick Schultz, CMO of Databricks, puts it:

The composable canvas is how all three become achievable simultaneously.

Elizabeth Dobbs, AVP of Marketing Technology at Databricks, describes the impact from firsthand experience:

## The last mile: the gap between your first-party data platform and a live campaign

Brinker is explicit that this report is a North Star, not a step-by-step implementation guide,  and that's exactly what makes it valuable. What it intentionally opens up is the practitioner question: how does a unified data foundation actually become a triggered campaign? How does a decisioning layer get built for a marketing team that doesn't speak data engineering? How do the five rings move from an architecture diagram to a customer experience that fires at the right moment?

These questions are where the real work of implementation lives — what Stitch calls the last mile.

Here's what the gap between the starting point and the finish line of the last mile actually looks like in practice:

- The autonomous agents with nowhere to go.A marketing leader at a major brand recently described a maddening situation: her engineering team had just deployed an autonomous agent system on Databricks that could reason across their entire customer data set in real time. But it had no idea how to trigger a campaign. Meanwhile, her marketing team's lifecycle journeys were still being fed by a batch file updated once a day. Two talented teams building the future, with no visibility into each other's work.
- The propensity score nobody acted on.A gaming brand's data science team built a sophisticated churn model. The propensity score fired correctly, flagging customers at risk. It went into a dashboard nobody was checking. The customer felt nothing from the brand at the moment they needed to feel something… and left. Because the last mile never got built.
- The Sunday night spreadsheet.A national grocery retailer had a Databricks environment full of offer eligibility data and a customer engagement platform built for exactly this kind of personalization. The gap between them? Four hours, every Sunday night, and a CSV. Campaign prep time: hours. The data was there. The activation capability was there. Nobody had built the bridge. Once connected, with offer eligibility flows automatically into customer profiles and campaigns, triggering in real time. Those four hours became minutes, every week, permanently.

As Brinker notes,

Architecturally, that's true. Operationally, for most brands today, the data and the campaign still live in completely different worlds.

## What closing the last mile requires

The brands making the composable canvas real aren't doing it by buying better tools. They're doing it by building the bridge — and that requires deep fluency in both the data platform and the marketing execution layer simultaneously.

Marketing data architecture built for activation.There is a meaningful difference between a data foundation built for analysts and one built for marketers. The former is optimized for queries, insights, and governance. The latter is optimized to trigger a campaign at the right moment, enrich a customer profile in real time, and provide an AI agent with the context it needs to make a decision. Getting there requires understanding both what Databricks can do and what the engagement layer actually needs from it.

[翻译失败，原文如下]

Self-service analytics for marketing teams.Brinker describes natural language interfaces as a core feature of the composable model — and for good reason. This is achievable, but most marketing teams are still submitting tickets to get basic campaign performance data.

The opportunity: build analytics environments scoped to real marketing use cases, so non-technical teams can answer their own questions without SQL, without a queue, and without waiting on data engineering. It's one of the highest-leverage implementations available right now.

AI agents that run natively on the data layer.The most powerful agentic marketing workflows aren't agents bolted on top of the existing stack. They're agents that live inside the data foundation and execute through the engagement layer — pulling segments, validating data quality, triggering campaigns, and measuring results without the CSV, without the manual handoff, without the lag. Kumar Ram, VP and Global Head of Marketing Data Sciences at HP, frames the strategic principle precisely:

Migrations that build toward composability, not away from it.For brands still running on rigid legacy marketing platforms, the move to a composable architecture is not simply a platform swap; it's an architectural decision. Done right, it positions Databricks as the data layer beneath an engagement stack that can flex and evolve as AI capabilities change. Elizabeth Dobbs captures the goal:

## Three ways to start building toward the composable canvas today

Brinker is clear that this is a 3-5 year architectural journey, not a rip-and-replace project. The good news: every step delivers value on its own terms. Here are three starting points that consistently unlock the most immediate impact.

### 1. Get your marketing data into Databricks — actually into it.

The most common version of "we have Databricks" is: the data engineering team has Databricks, and marketing has a dashboard that occasionally reflects it. That's not a unified data foundation. That's a reporting layer.

The first move is consolidation: getting campaign performance data, customer behavioral signals, loyalty data, and engagement history flowing into the same lakehouse where your transactional and operational data already lives. This is plumbing work — connectors, pipelines, data quality checks — but it's the foundation everything else depends on.

The immediate payoff is unified reporting: one version of truth that marketing, sales, and finance are all looking at. As Brinker's report puts it:

That alone is worth the investment. But it also ends the data tax that slows every campaign down — the tickets, the exports, the waiting.

Where to start: Map where your marketing data currently lives versus where it needs to be. Identify the two or three data sources that would most change what marketing can do if they were unified — typically transaction history, behavioral events, and offer or loyalty data — and build toward those first.

### 2. Build one self-service analytics use case for your marketing team

Most marketing teams are sitting one question away from an insight that would change how they run their campaigns. The problem isn't the data. It's the friction between the marketer and the answer.

Brinker's composable canvas puts self-service analytics — specifically, natural language interfaces that let non-technical users query data directly — at the center of the model. Tools like Databricks AI/BI Genie make this achievable today: a marketer types a question in plain English and gets an answer in seconds, without SQL, without a ticket, without a three-day wait.

The key is building for a specific use case rather than trying to give marketing access to everything at once. Start with the question your team asks most often and takes the longest to answer: campaign conversion by segment, offer redemption by store, churn signals by customer cohort. Build the Genie space around that decision. Let the team use it. Watch what happens when friction disappears.

One brand's campaign manager went from a four-day turnaround on a basic performance question to an answer in seconds — and then asked 12 more questions over the next 20 minutes, surfacing an insight about push notification timing that had been hiding in the data for a quarter. The friction was gone, and so was the ceiling on what she could find.

Where to start: Identify the single most common data question your marketing team escalates to the data team. Build a governed, use-case-focused analytics environment around that question first. Expand from there.

### 3. Pick one AI agent use case and ship it

The biggest mistake marketing teams make with AI is treating it as a strategy rather than a practice. The composable canvas makes AI agents genuinely operational — but only if you start building them on real data, in real workflows, against real outcomes.

The most effective first agent use cases are narrow, high-frequency, and connected directly to a campaign outcome. A QA agent that validates every email before it sends. A personalization agent that pulls real-time inventory or loyalty signals and generates copy on the fly. A churn agent that monitors behavioral signals in Databricks and triggers a campaign the moment a customer crosses a risk threshold — not three days later when a batch file runs.

What makes these use cases work is the architecture: agents that live in the data layer and execute through the engagement layer: no CSV exports, no manual handoffs, no lag. The campaign is only as intelligent as the data feeding it — which is exactly why the data foundation comes first.

As Brinker notes in the report,

The composable canvas is what gives them that context. The agent is just the thing that acts on it.

Where to start: Identify one high-frequency, high-cost manual process in your campaign operations — QA, segmentation, content generation, performance reporting — and scope a single agent to automate it. Measure the time saved and the change in outcome. Use that proof point to build the case for the next one.

## Why the window to build this is now

The timeline on Brinker's three-to-five-year vision is compressing faster than most marketing leaders expected.

Databricks just launchedCustomerLake, an Agentic CDP natively embedded within the Lakehouse. Core CDP capabilities including Customer 360, identity resolution, audience building, campaign automation, activation, and personalization can happen where customer data, AI models, and governance already reside — no middleware required.

Customer engagement platforms like Braze are connecting directly to Databricks through native Cloud Data Ingestion and OpenSharing. New platform capabilities like Lakebase mean full-stack marketing applications — front end, transactional logic, and campaign execution — can run on a single platform with a single governance model, eliminating the need to stitch together four separate systems.

The pattern Brinker identifies is already playing out: the platforms on each end are getting smarter and more directly connected. The integration layer in the middle is getting thinner every quarter.

The brands doing this work today see where the market is going. They're building the data architecture now so they're not scrambling to catch up when everyone else figures it out.

The composable canvas describes the destination. The last mile is the work between here and there.

Download Scott Brinker’s research report:The New Martech “Stack” for the AI Age

Databricks and Stitch are partnering to help marketing organizations close the gap between modern data infrastructure and real customer outcomes. If your organization is sitting on a Databricks investment that it hasn't fully activated for marketing,talk to Stitch→

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[The last mile: why great first-party data still doesn't make great marketing](https://www.databricks.com/blog/last-mile-first-party-data-great-marketing)
> 
> 翻译时间：2026-07-25 05:00
