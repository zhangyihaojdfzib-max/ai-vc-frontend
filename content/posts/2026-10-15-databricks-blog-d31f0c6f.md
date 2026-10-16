---
title: 'Reducing the noise: How Atlassian built an OCSF security lakehouse on Databricks'
title_original: 'Reducing the noise: How Atlassian built an OCSF security lakehouse
  on Databricks'
date: '2026-10-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks
author: ''
summary: '[翻译失败，原文如下]


  - 80% reduction in ingestion cost after standardizing security telemetry on OCSF

  - 500+ production threat-detection signals running on a ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:41:08.906286'
---

[翻译失败，原文如下]

- 80% reduction in ingestion cost after standardizing security telemetry on OCSF
- 500+ production threat-detection signals running on a single, unified schema
- 60% increase in analyst productivity — one repeatable process across every tool
- Up to 95% faster queries (from ~45 seconds to 2–3 seconds) using OCSF structure
- 44 billion events per day normalized into a common schema
- Winner of the Databricks 2026 Transformation Award

## The challenge: Two decades of logging noise at global scale

Atlassian is a global SaaS provider serving 350,000 customers — the product of 20 years of growth and a long list of acquisitions, each of which arrived with its own logging formats. The result was a security data pipeline absorbing44 billion events per daywith no common language across various log sources.

"You've got varied timestamps, you've got proprietary schemas, you've got operational drain for anyone trying to organize and structure this information," explained Zachary Schmerber, Senior Security Logging Engineer at Atlassian and a maintainer of the OCSF schema. Analysts were burning time normalizing dataafterit landed, cross-platform correlation was limited because data lived in different places and shapes, and SIEM pipelines were not keeping pace.

The team needed a way to coalesce fragmented telemetry into one place and make sense of it, while maintaining flexibility and avoiding vendor lock-in.

## The solution: Open schema on the security lakehouse

Atlassian's answer was to standardize everything on theOpen Cybersecurity Schema Framework (OCSF)and build the lakehouse on Databricks.

OCSF won because it was the only option the team consideredwholly open. Compared to alternatives like ECS or UDM, it offered a strongly typed schema with robust validation that minimized ambiguity after transformation, good compression efficiency, extensibility, and an open-source community (with Linux Foundation backing and a path toward international standardization). Its roughly 40,000 fields looked daunting at first — but that verbosity turned out to be the platform's greatest asset, because the semantic context stays with the data.

"Investigations where a single query could hit many different data sources — because the data is structured," said Schmerber. "Maybe you've got five vulnerability scanners in your system. Now you have one data set instead of five."

Databricks was the natural platform.Native ACID transactions made it far easier to migrate across schema versions without breaking downstream consumers; auto-scaling Spark clusters handled shared, high-volume workloads; and the platform was built to manage the infrastructure overhead of a large, multi-team organization. Atlassian deliberately choseETL over ELT— transforming data in flight — to enable real-time detection, preserve vendor independence, and compress data as it moved through the pipeline.

Table optimization delivered dramatic performance gains. With structured OCSF data, partitioning and Z-ORDER took a representative query from ~45 seconds to 2–3 seconds — a95% improvement, with similar gains on larger queries. EnablingGraviton clusters with Photoncut query cost and runtime by roughly two-thirds.

## Type safety: Embedding the schema into the code

A defining engineering decision was embedding the entire OCSF schema into Go structs — what the team calls "TypeGo." Because the schema lives in the type system, correctness is guaranteed at compile time.

"Every time you produce a new OCSF log, it's pre-validated — because it can't be anything but OCSF," said Schmerber. Nested objects are native, deployments can run anywhere, and everything is unit tested. Crucially, this type safety also tamed AI: when the team automated transformation with an agentic workflow, the rigid schema sharply reduced hallucinations and cut token usage, because the agent couldn't produce invalid mappings and cycle through bad iterations.

## From "mapping as a service" to a self-service platform

The biggest transformation was operational. Atlassian's security data-engineering team started with a six-phase manual procedure to collect logs, transform them into TypeGo, route, test, configure, and ship them via PR. Over time they automated nearly all of it — and eventually handed it back to the customer as a self-service platform.

Now an analyst identifies the logs they want and provides a canonical dataset. After a gated confirmation, the workflow scans the framework inside the Go structs, generates the mappings and the DAG, tests them locally, deploys a canary configuration via PR, validates at scale in a canary environment, and — after a soak — gets promoted to production and notifies the user of any errors. Regression testing gates everything before production.

The tool chain includes a schema-mapping IDE and an open-source Go OCSF library with validation performance enhancements, automatic handling of unmapped fields, schema helpers (IP path, normalization), and intelligent routing. The payoff is low onboarding overhead: "I can now have a SOC analyst do principal data engineer work in a production environment," said Schmerber — with every change still reviewed.

The acceleration is stark: "It took me a year to map about one-third of the data we have mapped today," Schmerber noted, "and two months to map the other two-thirds."

## Better detections: From one-to-one alerts to signals

For the detection and response team, standardization changed how alerts get written. "Adopting the OCSF schema has enabled us to transform our threat detection pipeline by moving from one-to-one alerts to a signal- and risk-based detection methodology, where multiple signal findings are clustered together in a single alert," said Jordan of Atlassian's Detection and Response team.

Using a custom tool calledAlert Explorer, findings cluster around standardized OCSF values — for example, a singleactor.uservalue that is identical whether it appears in an authentication event or a network event. That consistency lets the team standardize clustering, enrichment, and triage plays: instead of per-detection enrichment, they call an enrichment API on a standardized username value every time.

"OCSF has made it much easier to write detections and provide more meaningful, actionable alerts," said Jordan, "which analysts can dive deep into regardless of where the data came from."

## The impact

Beyond the headline cost and performance numbers, standardization unlocked capabilities that were previously impractical: multi-domain correlation with strong entity resolution, efficient user-behavior analytics, and cross-application pattern analysis. With everything speaking one language, the team could write simple queries to spot anomalous behavior across five different routers — or five vulnerability scanners — at once. Dashboards were simplified dramatically because OCSF classes share objects, and storage was optimized because the team knew what data to keep and what to drop.

## What's next: Talking to your data

Schmerber is most excited about what the semantically rich schema unlocks for AI. "How do you talk to your data unless your agent has context? It'll hallucinate and give you the wrong answer," he said. Because OCSF carries its definitions inside the schema, agentic assistance becomes far more accurate.

The roadmap includes skills training that feeds an analyst's real field usage into reusable agent skills, an orchestration of agents that can run threat hunts with the right context, contextual SQL that can answer questions like "where's my DNS C2 traffic in this schema?", and context graphs built on OCSF. The longer-term ambition is semantic: making OCSF the canonical starting point that everything emits — rather than a model coalesced from data after the fact. The team will also continue with improving query performance by looking at a move to Liquid Clustering for data partitioning across environments like corporate devices and cloud.

[翻译失败，原文如下]

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Reducing the noise: How Atlassian built an OCSF security lakehouse on Databricks](https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks)
> 
> 翻译时间：2026-10-16 06:41
