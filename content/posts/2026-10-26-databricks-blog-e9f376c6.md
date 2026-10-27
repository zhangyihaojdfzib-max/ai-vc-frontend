---
title: 'Building live intelligence: Databricks AI Search supports Streaming Tables,
  Materialized Views, and Managed tables using Iceberg'
title_original: 'Building live intelligence: Databricks AI Search supports Streaming
  Tables, Materialized Views, and Managed tables using Iceberg'
date: '2026-10-26'
source: Databricks Blog
source_url: https://www.databricks.com/blog/building-live-intelligence-databricks-ai-search-supports-streaming-tables-materialized-views
author: ''
summary: '[翻译失败，原文如下]


  - AI Search natively supports three new table sources in addition to Delta tables:
  Streaming Tables, Materialized Views, and Managed tabl...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-27T07:09:09.108341'
---

[翻译失败，原文如下]

- AI Search natively supports three new table sources in addition to Delta tables: Streaming Tables, Materialized Views, and Managed tables using Iceberg v3+.
- Use AI search to support real-time intelligence, personalized experiences, and cross-engine AI applications.
- Use the same AI Search workflow across data sources, from the UI or API, without building separate synchronization pipelines.

AI Search now natively supportsStreaming Tables, Materialized Views, and Managed tables using Iceberg v3+in addition to Delta tables. You can bring live events, continuously maintained personalized state, and open-format data directly into your AI Search applications — reducing the overhead of building and managing separate pipelines to convert and synchronize these data sources.

## Three table formats, a wider world of search applications

Streaming Tables, Materialized Views, and Managed Iceberg each represent a different way of working with data, and each opens up new possibilities for AI applications.

### Streaming Tables: powering real-time intelligence

Continuously changing data such as new listings, inventory, availability, and user activity can flow into an append-only Streaming Table, with AI Search indexing new records as they arrive and keeping the search index up to date. This freshness enables applications where the latest data can directly shape the search experience: helping users discover newly available restaurants through a search bar, or generating real-time recommendations based on recent trends.

### Materialized Views: enriching search with personalized context

Materialized Views can aggregate events, filter records, and join data from multiple sources to create customized state. As the underlying data changes, the view is incrementally maintained and AI Search propagates those changes to the index, enabling personalized search experiences such as session-aware recommendations, product and content discovery based on recent activity, or tailor results to a user's evolving interests and preferences.

### Managed tables using Iceberg: bring open-format data into search applications

Managed Iceberg tables can serve as AI Search sources directly, without conversion or migration to another table format, making open-format data available to search indexes and other AI applications. The open-format enables AI applications that work across existing data environments: search across product catalogs managed by different systems, unify business or customer data stored across Managed Iceberg tables, or build search experiences over large, distributed datasets without moving the underlying data.

## Making Search Native to Your Data: Connect Your Data Directly to AI Search

Before native support, customers had to create a separate Delta representation of Streaming Tables, Materialized Views, or Managed Iceberg tables and build pipelines to keep it synchronized with the source. This added an extra data layer, custom update logic, and ongoing operational overhead.

Now, AI Search connects directly to these sources. Create an index from your source and sync it when needed — AI Search propagates them directly to the index, eliminating the intermediate Delta table and custom synchronization pipeline. Your data stays connected to search as it evolves, with the platform handling the plumbing behind the scenes.

![](/images/posts/a0d30a9f1caf.png)

## Start building today: one workflow, across more data sources

Whether you use the UI or API, building an AI Search index follows the same workflow used for existing Delta table sources: create a Delta Sync index and point it at your source table. The same workflow now extends to Streaming Tables, Materialized Views, and Iceberg tables — no new workflow to learn.

![](/images/posts/50bcda172379.png)

Ready to build AI applications on your data? Get started by creating an AI Search index directly from your Streaming Tables, Materialized Views, or Managed Iceberg tables — no additional data pipelines required.Explore the AI Search documentation.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Building live intelligence: Databricks AI Search supports Streaming Tables, Materialized Views, and Managed tables using Iceberg](https://www.databricks.com/blog/building-live-intelligence-databricks-ai-search-supports-streaming-tables-materialized-views)
> 
> 翻译时间：2026-10-27 07:09
