---
title: 'Unity Catalog Metric Views, now in Power BI: one unified, governed semantic
  layer for all your reporting and AI'
title_original: 'Unity Catalog Metric Views, now in Power BI: one unified, governed
  semantic layer for all your reporting and AI'
date: '2026-11-10'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting
author: ''
summary: '[翻译失败，原文如下]


  - Make Databricks the home of your semantics: Keep metric views, relationships,
  Pages, and other modeling metadata in one governed place ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-11T09:04:29.600983'
---

[翻译失败，原文如下]

- Make Databricks the home of your semantics: Keep metric views, relationships, Pages, and other modeling metadata in one governed place with Unity Catalog Semantics, not scattered across different tools.
- Model once, consume across AI and BI: Define metrics and data models once in Unity Catalog metric views and publish them directly to Power BI semantic models from Catalog Explorer or a Power BI task. Receive consistent results across Power BI, AI/BI dashboards, and Genie.
- Stay governed and in sync: Unity Catalog access controls stay in place with DirectQuery, and Power BI task orchestration keeps Power BI models up-to-date as your UC metric views change.

Organizations want a single, trusted definition of their business semantics. Revenue, margin, and active customers should mean the same thing in every report, notebook, and AI application. When they don't, business users and AI agents read the same data differently and reach different answers. Finance and sales show different revenue numbers, teams lose trust in their reports, and decisions get made on the wrong numbers.Unity Catalog metric views, part of Unity Catalog semantics, solve this by enabling customers to define business KPIs once in Databricks, in an open, governed semantic layer that sits on top of the lakehouse.

At the same time, many of these organizations rely on Power BI as the front end for their business users. Often, organizations have thousands of PowerBI workspaces each with its own Semantic Models, creating a governance and unification nightmare. Furthermore, when each team builds its own metrics and relationships in Power BI, the same logic lives in many places. Reports drift apart, and every definition change means updating each copy.

Customers have told us they want both: Databricks as their unified, open semantic layer, and Power BI as their front end. WithPublish to Power BI, they can now have both. Every Power BI report uses the same governed UC metric views as AI/BI dashboards and Genie, so teams work from consistent numbers. Business users can build self-serve reports and explore metrics across any dimension without waiting on a data team to model data or write DAX. Data teams maintain one definition in Databricks instead of many copies across systems. Publish on demand from Catalog Explorer, or add a Power BI task to aLakeflow Jobto keep metric views and semantic models in sync in production.

## Model once in Databricks, use it in Power BI

With Publish to Power BI or a Power BI task, you can connect Unity Catalog metric views to a Power BI semantic model. Each metric view becomes a table in the model. The metric view’s dimensions (aka Fields) become columns and its measures become DAX measures.

Power BI queries the metric view itself (as if it was a table). The metric view stays the source of truth, and joins defined in the metric view run in Databricks. Joined dimensions, such as campaign channel or region, show up in Power BI as ordinary columns, so you don't have to rebuild table relationships in Power BI.

For example, a marketing team needs to track campaign performance and decide where to shift budget. They define a campaign_performance metric view in Unity Catalog with dimensions such as channel and region and measures such as total spend, total revenue, and return on ad spend (ROAS). When the team publishes the metric view, those dimensions and measures arrive in Power BI like this:

Category

Metric view expression

Power BI measure (DAX)

Dimension

channel

(from the joined campaigns table)

‘campaign_performance'[channel]

region (from the joined regions table)

'campaign_performance'[region]

Measure

total_spend = SUM(spend)

total_spend = SUM('campaign_performance'[spend])

total_revenue = SUM(revenue)

total_revenue = SUM('campaign_performance'[revenue])

roas = MEASURE(total_revenue) / MEASURE(total_spend)

roas = DIVIDE([total_revenue], [total_spend])

A marketing analyst can then build a Power BI report that compares ROAS by channel and region, and see the same numbers the team gets in AI/BI dashboards and Genie. If the team later changes what counts as total_revenue they update the metric view once, a Power BI task in their pipeline republishes it, and every Power BI report picks up the new definition.

![](/images/posts/ec8667c74ac6.gif)

## Fast by design

Because Power BI queries the metric view, it will soon be able to benefit from metric view materialization too. Metric view materialization is a performance optimization that pre-computes results without changing how metrics are calculated. When Power BI sends a query, Databricks will serve it from a matching materialization for faster results. If no materialization matches, the query runs against the metric view as usual. Either way, the metric definitions, DAX measures, and results are identical.

Additionally, with Lakehouse//RT + DirectQuery, Power BI reports get real-time performance, directly on your governed lakehouse data. Lakehouse//RT runs on your managed Delta tables, so there's no separate serving system to copy data into or manage. It also enforces the same Unity Catalog row filters, column masks, and ABAC policies, so reports get faster without giving up governance.

## Governed and always in sync

With DirectQuery, every query honors Unity Catalog access controls and security policies, and lineage stays connected to the metrics your teams already use inAI/BI dashboards,Genie, andDatabricks Lakehouse.

When a metric view changes, we make it easy to keep Power BI up to date. UsingPower BI tasksin Lakeflow Jobs, you can publish your metric views to the target semantic model as a step in your data pipeline, on a schedule or right after upstream tables refresh. Updated measures, new measures, and new dimensions flow into Power BI automatically, so reports stay aligned with the metrics layer without manual rework.

## What’s supported

Publish to Power BI covers the metric definitions most teams use day to day:

- Data modeling:Define your data model directly in metric views, including joins and relationships, dimensions, measures, and other semantic metadata, and let Databricks handle the computation automatically without manually duplicating logic in Power BI.
- Measures:Standard aggregations (SUM, COUNT, AVG, MIN, MAX, MEDIAN, STDDEV, VARIANCE), distinct counts, ratios, filtered measures, and measures composed from other measures.
- Window measures:Current, offset, and trailing window measures.
- Metadata:Descriptions and display formats including currency, decimal and percentage settings carry over to Power BI field properties.
- Storage modes:DirectQuery (the default) for live queries against Lakehouse/RT or Databricks SQL, and Import mode for loading data into Power BI.
- Publishing mechanisms:Use Publish to Power BI in Catalog Explorer to publish metric views on demand in a few clicks. UsePower BI tasksin Lakeflow Jobs to automate publishing as part of your data pipeline, so metric views and semantic models stay in sync in production.

## Get started

Publish to Power BI is available in Private Preview (documentation). Work with your account team to test out the preview.

Once enabled, you can publish in three easy steps:

1. Prepare the metric view(s):Add any measure inputs as dimensions and make sure every field is named.
2. Publish:In Catalog Explorer, clickPublish > Publish to Power BI, sign in withyour Power BI credentials, and choose a target workspace. When you're ready for production, add a Power BI task to a Lakeflow Job to automate publishing, ensuring your Power BI semantic model stays in sync with your metric view.
3. Validate in Power BI:Open the semantic model and confirm that the metric view appears as a table, dimensions appear as columns, and measures appear as DAX measures.

[翻译失败，原文如下]

Together, these capabilities make Databricks the home of your semantics. Define your metrics once in Databricks, keep Power BI models in sync using Power BI tasks, and use the same governed definitions everywhere, including the Power BI reports business users already rely on. Every team and use case works from one open, governed platform.

What is a governed semantic layer, and why do BI and AI agents need one?A governed semantic layer is one place where business metrics and shared dimensions like revenue, country, and active customers are defined. Every BI tool, notebook, and AI agent then uses those definitions the same way. Unity Catalog Semantics is that layer in Databricks. It brings together metric views, relationships, and other modeling metadata in Unity Catalog. It's open, you can query it with SQL, and it inherits Unity Catalog access controls and lineage. That's why a Power BI report, an AI/BI dashboard, and a Genie One agent all return the same ROAS number.

How do you give AI agents and BI users the same business definitions?Build business definitions once in a shared semantic layer that is accessible by all of your tools. Don't encode it separately in each BI tool or agent prompt. With Unity Catalog metric views, Genie One and Agent Bricks agents read the same governed definitions that Power BI reads through Publish to Power BI. When a definition changes, every consumer gets the update.

Should metrics live in Power BI semantic models or in Unity Catalog?Keep the metric definitions in Unity Catalog. A Power BI semantic model primarily serves Power BI. It is hard to access from external BI tools or AI agents, requiring the same metric to be rebuilt in every tool. Publishing metric views to Power BI turns each measure into DAX automatically, so Power BI users keep their reports, while maintaining a single governed definition for AI and other use-cases.

Does Power BI query the metric view or the underlying tables?The metric view. Only the measure expressions are translated to DAX, and they reference the metric view's dimensions. The metric view stays the source of truth, and joins and calculations run in Databricks.

What does the published semantic model look like?Each metric view becomes one table. Its dimensions become columns and its measures become DAX measures. Because joins are defined once in the metric view, joined dimensions show up as ordinary columns and no Power BI relationships are needed. For example, SUM(amount) becomes SUM('sales_metrics'[amount]), and MEASURE(a) / MEASURE(b) becomes DIVIDE([a], [b]).

What happens when a metric view changes?To keep models in sync automatically, add aPower BI taskto a Lakeflow Job so publishing updates runs on a schedule or after upstream tables refresh.

Is access still governed by Unity Catalog?Yes, with DirectQuery. Every query honors Unity Catalog access controls and security policies. In Import mode, data is loaded into Power BI, so access to that copy follows Power BI permissions.

Do changes made in Power BI sync back to Unity Catalog?No. To ensure unified and governed semantics, publishing only goes one way, from Unity Catalog to Power BI. If you edit a published measure in Power BI, that edit isn't written back to the metric view. To change a governed metric, update the metric view in Databricks and republish, or create a Lakeflow Job with a Power BI task to update the Power BI semantic model on a schedule.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Unity Catalog Metric Views, now in Power BI: one unified, governed semantic layer for all your reporting and AI](https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting)
> 
> 翻译时间：2026-11-11 09:04
