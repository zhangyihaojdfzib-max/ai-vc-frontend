---
title: How Concurrence governs clinical AI at a trillion-token scale with Unity Gateway
title_original: How Concurrence governs clinical AI at a trillion-token scale with
  Unity Gateway
date: '2026-09-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway
author: ''
summary: '[翻译失败，原文如下]


  Healthcare AI has little margin for error. AI agents helping coordinate patient
  care depend on reliable patient context, clear controls o...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-24T07:29:17.399149'
---

[翻译失败，原文如下]

Healthcare AI has little margin for error. AI agents helping coordinate patient care depend on reliable patient context, clear controls over data and model access, and visibility into every interaction, all while maintaining stringent compliance requirements.

Concurrenceis operating these healthcare agentic systems at a significant scale. The company builds clinical AI agents across patient- and provider-facing workflows, from AI clinicians, nurses, and care coordinators to ambient documentation, care-plan summaries, and knowledge retrieval.

Across its production AI environment, Concurrence now processes approximately 100.8 billion input tokens and 11.2 million LLM calls every 30 days, equivalent to an annualized run rate of roughly 1.2 trillion input tokens. Monthly token volume has grown about 5x from its late-2025 baseline to July 2026.

In high-stakes clinical workflows, reliable AI agents start with trustworthy, well-governed data. Supporting that reliability at scale requires strong compliance, rigorous agent testing and governed AI access. Concurrence is consolidating these capabilities on Databricks, withLakebasefor operational agent and conversation state,Unity Catalogfor governing data and AI assets, andUnity Gatewayfor centralized AI access and security across its rapidly growing developer AI workloads.

## Building reliable clinical AI on trusted data

Healthcare data often conflicts across systems. A patient may provide information that differs from an existing record, and the newest value is not always the most reliable.

Concurrence addresses this by recording new information as immutable events rather than overwriting existing records. From that history, Concurrence computes the current patient state while preserving the source and provenance of each piece of information, which it calls its world model. This gives agents a consistent view and history of what is known about a patient, while allowing what they learn from patients and clinicians to feed back into the state for future workflows.

Databricks provides the shared data foundation for this architecture. Events stream throughZerobus Ingestinto governed Delta tables, including 2.7 million world-model events per month and 90,000 per day at peak.Apache Spark™ Declarative Pipelinesderive Concurrence’s world model and clinical data; Unity Catalog governs each customer environment; and Lakebase serves the patient state, agent and conversation state, and knowledge base data needed by operational applications.

Care gap and medication adherence outreach is one example. Concurrence’s agents can call or text patients who are overdue for follow-up care or falling off a medication, use existing patient context to guide the conversation, and record what they learn back into the patient state for future workflows. Concurrence also runs production applications on Databricks Apps, including a care-packet guide, nurse care-plan summary, and clinical-content review surface. Each builds on the same governed patient context and infrastructure. The move to this architecture has also allowed Concurrence to retire its homegrown prompt-log store and reverse-ETL jobs in favor of governed Delta tables and Lakebase Synced Tables.

## Testing clinical AI agents before production

![](/images/posts/2941153bc781.png)

Every agent on Concurrence’s new platform is tested against simulated patients before it reaches a real one. Today, simulation and evaluation traffic is approximately seven times greater than production traffic on the new platform.

Concurrence’s data architecture makes this testing possible. Because the patient state is computed from an immutable event history, teams can replay that state and test different paths without changing the real patient record. This allows Concurrence to evaluate how an agent responds to different scenarios before deploying it to patients.

Agent traces stream through Zerobus Ingest and lands in Delta tables alongside the clinical data that produced them. Scheduled ai_query jobs using Databricks-hosted Claude, then score those interactions for conversation quality and safety, extract memory, and write the results back to Delta. With patient data, traces, outcomes and evaluations on the same governed foundation, teams can investigate whether changes in performance came from the model, the data or the workflow.

## Enforcing AI governance and compliance in healthcare

For Concurrence, HIPAA requirements shape the architecture from the start. Concurrence is HIPAA-, GDPR- and SOC 2-compliant today, with HITRUST and ISO 27001/42001 in progress. Each healthcare organization gets its own schema and service principal, with access controls, lineage and audit trails governed through Unity Catalog.

For batch AI workloads, Concurrence runsai_queryjobs on Databricks-hosted Claude under a BAA. Its endpoint resolver only permits models within the BAA-covered namespace, preventing PHI from being routed to an uncovered model. The same covered path runs Concurrence’s safety classification for self-harm, suicidal ideation, and medical emergencies. Some of its highest-stakes AI workloads are therefore protected by the same architectural constraint. This also shapes Concurrence’s approach to model routing: routing is compliance-gated before it is cost-gated. Models must first meet the compliance requirements of a workload before Concurrence considers quality, performance or cost.

Real-time patient and clinician inference remains on Concurrence’s existing provider infrastructure today. Concurrence has already built and feature-flagged its Unity Gateway integration for real-time inference, with a synthetic canary continuously testing it end-to-end. Production traffic can move to Unity Gateway as the required compliance coverage becomes available.

![](/images/posts/c90146182693.png)

## Governing coding agents with Unity Gateway

Concurrence applies the same approach to developer AI. Coding agents are used across engineering, operations, and research, including by forward-deployed engineers working within customer environments that handle sensitive healthcare data.

Concurrence routes all coding-agent model and tool traffic throughUnity Gateway’s coding CLI, ug. Developers get a single governed path to approved models and MCP tools, while each request remains associated with the identity of the person who made it. MCP access is centrally managed through the same environment, with permissions assigned by engineer group and each user authenticating individually when agents access tools such as Databricks, Datadog, and Linear.

The scale is already substantial. In July, 14 individual users generated 35.85 billion input tokens through Unity Gateway, of which 95.37% were cache reads. Since ug rolled out on July 10, Concurrence’s coding agents have generated approximately 360,000 requests and 61 billion cumulative input tokens.

Centralizing coding-agent traffic gives Concurrence visibility into how developer AI is used and how much it costs. Every request is attributed to the engineer who made it, allowing individuals to monitor their own usage throughug usage. At the organization level, Concurrence uses Databricks usage data fromsystem.ai_gateway.usageto track models in use, token consumption, cache rates, and spend by person and team.

![](/images/posts/e15470cbb107.png)

## Centralizing AI access with Unity Gateway

Concurrence’s goal is to bring production, batch and developer AI under a common inference control point with Unity Gateway. Developer AI already runs through Unity Gateway, while batch inference runs on Databricks-hosted models through BAA-covered paths. Today, Claude Opus 4.8 and GPT-5.6 Sol account for most coding-agent model usage, with Opus 5 usage growing. Real-time patient and clinician inference remains on Concurrence’s existing provider infrastructure until the required compliance coverage is available.

[翻译失败，原文如下]

That multi-model approach is especially important for Concurrence’s clinical workloads. The company currently has 14 models serving production inference and a governed catalog of 46 models. Most production volume runs on smaller, faster models, with frontier models reserved for more complex reasoning. Concurrence is developing clinical reasoning benchmarks to determine which models perform best across different healthcare tasks.

Concurrence is also excited about the pace of innovation with Unity Gateway. Most recently they have begun testingUnity Gateway Smart Routingagainst healthcare-specific routing approaches it is developing and publishing the results. Because model eligibility in healthcare starts with compliance, those evaluations will assess how intelligent routing can optimize model choice within the boundaries established for each workload. On the developer side, Concurrence is also exploringOmnigentas a meta-harness across its coding-agent environment.

![](/images/posts/95a610fbc429.png)

## A unified foundation for healthcare AI

As Concurrence moves more workflows onto Databricks, the foundation becomes more valuable with every agent interaction. Each agent’s work can enrich the patient state the next agent starts from, allowing new workflows to reuse existing context rather than rebuild it, reducing the incremental cost and effort of adding new AI workflows.

At an annualized rate of roughly 1.2 trillion production-input tokens, that compounding foundation matters. By bringing patient context, operational state, traces, evaluations, governance and AI access together on Databricks, Concurrence can scale high-stakes clinical AI while maintaining the reliability and controls healthcare demands.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How Concurrence governs clinical AI at a trillion-token scale with Unity Gateway](https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway)
> 
> 翻译时间：2026-09-24 07:29
