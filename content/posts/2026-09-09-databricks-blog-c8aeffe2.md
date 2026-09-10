---
title: Five AI Questions We're Hearing from Financial Services Leaders
title_original: Five AI Questions We're Hearing from Financial Services Leaders
date: '2026-09-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/five-ai-questions-were-hearing-financial-services-leaders
author: ''
summary: '[翻译失败，原文如下]


  - Explore five questions shaping the move from financial-services AI pilots to governed
  production deployments.

  - See how Databricks brin...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-10T07:13:52.571208'
---

[翻译失败，原文如下]

- Explore five questions shaping the move from financial-services AI pilots to governed production deployments.
- See how Databricks brings data, AI and governance together for financial crime, finance, banking, and wealth-management workflows.
- Meet with Databricks financial-services leaders and experts at Sibos 2026 in Miami.

Last year at Sibos Frankfurt, the question was whether AI works. This year:can your AI earn your trust?

The data backs up that shift. In Grant Thornton's 2026 Banking Insights AI Impact Survey, half of banking executives said governance and compliance were already limiting AI performance, yet only 18% said they were confident they could pass an independent audit of their AI controls. Our own research with Economist Enterprise, the 2026 reportMaking AI Deliver, found a similar gap for agentic AI specifically: fewer than half of organizations formally mandate a governance framework for autonomous systems.

These are the five questions we hear most from chief financial officers (CFOs), compliance officers, treasury leads and relationship managers. They're worth asking whether or not you're headed to Sibos this year.

## 1. Can finance teams move from reporting to action?

"What's our real liquidity position right now, across every entity and currency?" That's the question a treasury officer asks every day. It's the one AI should finally answer without a three-day spreadsheet sprint.

Getting a model to summarize a report is straightforward. The harder part is putting governed data and AI into the decisions finance teams make every day across the balance sheet, liquidity, spend, and operations. The goal is to help teams spot changes, investigate what is driving them, and do more than automate the reporting cycle.

At the Databricks booth (#DISL25) at Sibos Miami, we'll present a talk,Trapped Capital, Released by AI: Reconciliation Your Regulator Can Audit. It finds the GL-to-Risk data breaks that silently inflate risk-weighted assets, investigates them with cited evidence, and releases trapped regulatory capital, with a human maker-checker in control and an audit trail an examiner can actually follow.

We'll also dig into what comes after the money moves. Tokenized settlement rails solve part of the problem, but reconciliation, financial-crime controls, and intraday liquidity management still have to happen off-chain. Our lightning talk,Tokenization Moved the Money. It Didn't Move the Hard Part, walks through the operating model for keeping token positions, deposit sub-ledgers, and funding accounts continuously aligned. Plus you will get a live look at a tokenized-deposit reconciliation control plane.

## 2. Can financial-crime teams use AI without losing control?

"Is this alert real risk, or noise?" That's the question an AML analyst asks dozens of times a day, and it's the one that separates AI that actually helps from AI that just adds another system nobody trusts.

AI can investigate cases, connect context and support analyst decisions. But every recommendation needs a traceable source: what data fed it, what it recommended, whether a person reviewed the output and whether the institution can reconstruct the investigation for an audit or regulatory review. Governance can't live only in a policy document. It has to be built into the data, access controls and workflow itself.

We'll have a live version of this at our booth: an agent working real AML alerts on the bank's own lakehouse, seeing only what the analyst is cleared to see. It drafts the Suspicious Activity Report (SAR) and leaves the filing to a human, with every step logged against the know-your-customer (KYC)/AML evidence and the model that ran. It's the same question that we'll cover in our Discover Stage session,How financial institutions are governing AI in financial crime operations, on Thursday, October 1, 11:00 AM, proving what the AI did, not just what it can do.

## 3. How can AI help bankers, advisors and investment teams?

"What does this client actually need from us right now?" Every relationship manager asks some version of that before a call, and the honest answer usually depends on data scattered across three systems and a research folder they didn't have time to read.RBC Brewin Dolphinuses generative AI to automate preparation for client-review meeting packs, saving an estimated 4,700 hours annually. Other firms are taking this further. At one global asset manager, multi-agent workflows generate investment commentary across hundreds of funds, extending advisor coverage while compliance stays in the loop. At another, agents blend proprietary fund scoring with internal documents to produce audit-ready portfolio analyses in seconds, surfacing opportunities a team wouldn't have had time to find on their own.

The goal isn't removing people from high-value decisions. It's reducing the work around those decisions so more time goes to judgment and the relationship itself.

## 4. How do you use real-time data without adding complexity?

"Why did we just decline a good transaction?" That's what a head of transaction banking asks when risk decisions run on data that's minutes, not milliseconds, old.

Most institutions already have the data. It's just spread across systems, delayed by batch processes or hard to use in a governed way.Coinbaseruns real-time fraud detection on Databricks with sub-100ms P99 latency, a useful benchmark for what "real-time" actually needs to mean.

## 5. What does AI cost once usage expands?

AI economics look manageable in a pilot and very different in production. On a recent Bloomberg CFO Briefing, one CFO called AI token expense a "trivial number" for the first half of 2026, while noting that not every task needs the most expensive model. That won't stay trivial for long, at that bank or anywhere else. Cost discipline needs to start before spend becomes hard to track, not after.

For a closer look at how engineering teams are already solving this problem, see Databricks' blog post,Managing AI Coding Costs at Scale, which breaks down the levers, from model routing to spend visibility, that keep AI costs from outrunning the value they create.

If these are the conversations your team is already having, we'd rather have them in person. Databricks will be in Miami for Sibos 2026, September 28–October 1. Emailsibos@databricks.comor visit ourevent pageto see the full agenda and to schedule a meeting.

- When is Sibos 2026?Sibos 2026 takes place September 28–October 1, 2026, in Miami, Florida.
- Where is Sibos 2026 held?Sibos 2026 is held at the Miami Beach Convention Center.
- Is Databricks exhibiting at Sibos 2026?Yes. Databricks will be on-site throughout Sibos 2026, running live demos and hosting executive meetings for financial services leaders. For the full agenda, visit ourevent page.
- What is the theme of Sibos 2026?"Digital finance for AI-driven economies."
- What topics can I discuss with Databricks at Sibos?Executive and SME meetings on AI agents for financial services, AI governance, Databricks platform strategy, intelligent document processing, and real-time data architecture. Meetings with Databricks Financial Services leadership are available by request. Book a meeting, emailsibos@databricks.comor stop by our booth #DISL25.
- What partners are part of the Databricks financial services ecosystem?Cloud providers, advisory and transformation firms, financial data providers, and specialized technology partners.Featured partner session:Governed AI in Financial Services: Microsoft & Databricks, Wednesday, September 30, 10:30 am, Microsoft Booth #H068.
- When is the Databricks Sibos session?"How financial institutions are governing AI in financial crime operations," at the Discover Stage, Thursday, October 1, 2026, at 11:00 AM.

- Sibos 2026 takes place September 28–October 1, 2026, in Miami, Florida.

- Sibos 2026 is held at the Miami Beach Convention Center.

[翻译失败，原文如下]

- Yes. Databricks will be on-site throughout Sibos 2026, running live demos and hosting executive meetings for financial services leaders. For the full agenda, visit ourevent page.

- "Digital finance for AI-driven economies."

- Executive and SME meetings on AI agents for financial services, AI governance, Databricks platform strategy, intelligent document processing, and real-time data architecture. Meetings with Databricks Financial Services leadership are available by request. Book a meeting, emailsibos@databricks.comor stop by our booth #DISL25.

- Cloud providers, advisory and transformation firms, financial data providers, and specialized technology partners.
- Featured partner session:Governed AI in Financial Services: Microsoft & Databricks, Wednesday, September 30, 10:30 am, Microsoft Booth #H068.

- "How financial institutions are governing AI in financial crime operations," at the Discover Stage, Thursday, October 1, 2026, at 11:00 AM.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Five AI Questions We're Hearing from Financial Services Leaders](https://www.databricks.com/blog/five-ai-questions-were-hearing-financial-services-leaders)
> 
> 翻译时间：2026-09-10 07:13
