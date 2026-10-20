---
title: How HP Is Building an AI-Ready CDP with Databricks CustomerLake
title_original: How HP Is Building an AI-Ready CDP with Databricks CustomerLake
date: '2026-10-20'
source: Databricks Blog
source_url: https://www.databricks.com/blog/hp-ai-ready-cdp-databricks-customerlake
author: ''
summary: '[翻译失败，原文如下]


  - HP became audience-ready in 2 hours instead of 2 to 3 months. With Databricks
  CustomerLake, HP configured governed data models and publ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:34.505259'
---

[翻译失败，原文如下]

- HP became audience-ready in 2 hours instead of 2 to 3 months. With Databricks CustomerLake, HP configured governed data models and published attributes directly on its existing Databricks foundation, dramatically accelerating audience creation.
- HP estimates up to 40% lower CDP total cost of ownership. Consolidating CDP capabilities with CustomerLake could reduce HP’s TCO by up to 40% compared with its former composable CDP approach.
- HP expanded its marketing context with 90% net-new signals. HP unified media, brand, intent and technographic data in its Marketing Lakehouse, expanded intent-data ingestion from 75 to approximately 20,000 topics, and reduced comparable governed data-sharing timelines from three months to 48 hours.

At Data + AI Summit 2026,Luis Alonso, Global Head of Data Strategy & Engineering for MarTech & AI Enablement at HP, shared how the company is building an AI-ready go-to-market data foundation on Databricks.

HP has spent extensive time and effort unifying customer data and third-party signals in their Marketing Lakehouse, and now Genie and CustomerLake make that trusted context available to marketers making daily decisions about audiences, channels, and customer journeys.

HP’s early work highlights three ways this approach can reduce costs, expand available customer context, and accelerate activation:

- 40% lower CDP total cost of ownership:HP estimates that consolidating CDP capabilities with CustomerLake could reduce total cost of ownership by up to 40% compared to its former Composable CDP approach.
- 90% net-new marketing signals:HP expanded the data available for marketing with 90% net-new signals across media, brand, intent, and technographic sources.
- Audience-ready in two hours:In the first session of using CustomerLake, HP configured data models, published attributes, and became ready to build audiences — a process that could’ve taken 2-3 months with a traditional CDP.

![HP projects a potential 40% reduction in CDP total cost of ownership with CustomerLake](/images/posts/29ac4505ead2.png)

## Why HP is rethinking the traditional CDP

For HP, a CDP isn't one product or a narrow set of activation features. It's a collection of capabilities built around the needs of the business:

- First- and third-party data strategy
- Account profiling and clustering
- Identity and buying-group intelligence
- Audience segmentation and activation
- Closed-loop measurement
- Always-on automation and self-service

As HP consolidated more governed data and business logic on Databricks, maintaining a separate CDP increasingly meant duplicating pipelines, data and operational overhead. Composable architectures reduced some data movement, but the activation layer still lacked the business definitions, context, and governance already available in the data platform.

![HP's architecture is evolving toward lakehouse-native CDP capabilities that combine composability with business context.](/images/posts/dd77129cc6be.png)

That context is essential for self-service analytics and AI agents. Without it, an agent may be able to access data but still lack the definitions, relationships, metrics and governance needed to use it correctly.

## From hundreds of data repositories to a governed Marketing Lakehouse foundation

HP's broader data transformation consolidated hundreds of data lakes and repositories into a small number of Databricks lakehouses. The company uses central standards with federated execution, allowing domain experts to retain ownership and stewardship while sharing governed data products across the business.

This gave marketing governed access to previously fragmented sources, including media performance, market-share, technographic and intent data, along with propensity models.

The change has materially changed how HP teams work together.

Alonso described a 2024 request to share data with a sales partner that required three months, roughly 15 email exchanges and three escalations, without a reliable outcome. Today, a comparable request can result in a governed Delta Sharing asset within 48 hours.

That improvement gives marketing faster access to the data it needs for planning, targeting, reporting and measurement, while preserving domain ownership and governance.

![HP built a unified Marketing Lakehouse then federates governed data products across marketing and partner teams.](/images/posts/2afad8a3bd28.png)

## Turning technology readiness into business readiness

Creating a strong technical foundation doesn't automatically make data usable for marketers. The next step is enabling executives, marketing users, media teams and analysts to use that foundation without relying on engineering for every question or task.

HP is using AI/BI Genie and agent-based capabilities to help bridge that gap across three layers of work:

- Decision-making and planning for executives and business teams
- Insight generation and activation for marketers, analysts and data scientists
- Building and scaling for engineering teams

Business context is a core part of that strategy. HP is developing semantic layers that help Genie understand what the company's data means, including domains, metric views, instructions and reusable skills.

![HP centralizes its semantic layer in Genie Ontology and Metric Views](/images/posts/1063a5164a92.png)

For example, HP created a media metric view covering 26 dimensions and 10 measures. This centralizes definitions for media-spend and performance KPIs so dashboards, business users and AI systems can work from the same source of truth.

HP has also expanded its intent-data ingestion from 75 topics to approximately 20,000 topics. Genie Code helps the team plan how to cluster those signals at scale and use them for richer account profiles.

## Bringing identity into the governed data foundation

HP is also rethinking where identity resolution should live. Historically, companies often sent customer data to an external identity provider and kept the resulting identity layer outside their core data environment.

HP plans to bring identity signals back into its Databricks environment. That creates a governed foundation for measurement, audience activation and model improvement. Data can flow through the same identity service on its way to media platforms and on the return path, helping HP build a more complete view of performance and continuously improve its models.

Alonso noted that reaching even 10% of HP's consumer customer base through this consent-preserving approach could create a substantial new opportunity for the commercial business.

## CustomerLake Agentic CDP: Becoming audience-ready in two hours

HP's early experience with CustomerLake illustrates the potential of bringing marketing capabilities directly to the governed data foundation.

Based on the team's prior CDP implementations, Alonso expected a long setup process involving extensive meetings, documentation, data-model configuration, and privacy and security reviews.

The initial experience was dramatically simpler.

“We had our data models in place, we had attributes published, and we were ready to build audiences — work that might have previously required two or three months to complete.”

Because CustomerLake is native to Databricks and Unity Catalog, HP's team could work directly with their schemas, tables, definitions, and governance, instead of recreating context in a separate platform.

![HP configured data models and attributes and became ready to build audiences within two hours.](/images/posts/aa9ade7ee700.png)

The architecture also supports a significant B2C-to-B2B opportunity. HP has hundreds of millions of consumer customers, but a much smaller known population of business contacts. CustomerLake makes it possible for HP to work across both their B2C and B2B data models and systems in one environment through a shared identity layer. HP can also incorporate data from other platforms using Lakehouse Federation.

[翻译失败，原文如下]

![CustomerLake enables HP to combine its B2B and B2C data models with no additional overhead](/images/posts/1ecb44a1ca2f.png)

## HP’s four lessons for building an AI-ready marketing foundation

Across the go-to-market roadmap, HP is evaluating value in three areas:

- Outcomes: Better insights, planning, activation, reporting and measurement
- Productivity: Faster model development, audience creation and data access
- TCO: Lower platform, licensing, integration and operational costs

HP’s work with Genie and CustomerLake suggests potential to address all three areas together. Their journey offers four practical takeaways for other enterprises modernizing their marketing stack:

1. Define the CDP around business needs.Start with the capabilities your stakeholders need rather than a rigid category definition or product checklist.
2. Build a governed Marketing Lakehouse.Data unification, quality, and access need to be in place before self-service and agents can work reliably.
3. Choose CDP capabilities closest to your data and AI.AI agents work best when customer context, business definitions, and activation capabilities operate on the same foundation, giving them the context to act accurately and safely at scale.
4. Measure outcomes, productivity, and TCO together.Faster activation, revenue impact, reduced engineering overhead, and lower platform costs are connected parts of the same transformation.

HP’s journey shows that modernizing marketing activation and applying AI at scale both depend on bringing data, intelligence, and action together on the same foundation. With CustomerLake and Genie on its governed Marketing Lakehouse, HP is giving marketers and agents direct access to trusted context without recreating it across disconnected systems. The early results include becoming audience-ready in two hours instead of months, with the potential to reduce CDP TCO by up to 40%. Together, these gains lay the foundation for faster, more intelligent and more personalized customer engagement at scale.

Watch the full Data + AI Summit session here.

---

> 本文由AI自动翻译，原文链接：[How HP Is Building an AI-Ready CDP with Databricks CustomerLake](https://www.databricks.com/blog/hp-ai-ready-cdp-databricks-customerlake)
> 
> 翻译时间：2026-10-20 07:22
