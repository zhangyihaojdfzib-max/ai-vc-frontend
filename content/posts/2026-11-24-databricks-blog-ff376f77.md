---
title: Sharing catalog metadata across data platforms, engines, and agents
title_original: Sharing catalog metadata across data platforms, engines, and agents
date: '2026-11-24'
source: Databricks Blog
source_url: https://www.databricks.com/blog/sharing-catalog-metadata-across-data-platforms-engines-and-agents
author: ''
summary: '[翻译失败，原文如下]


  - Catalog labels provide a standard way to share table- and column-level context
  through the Apache Iceberg REST Catalog API.

  - Unity Cat...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-24T12:13:02.683416'
---

[翻译失败，原文如下]

- Catalog labels provide a standard way to share table- and column-level context through the Apache Iceberg REST Catalog API.
- Unity Catalog is implementing the standard to make its tags consumable by any tool and platform.
- Databricks, Google Cloud, Salesforce, ClickHouse, Atlan, Collibra, DataHub, Immuta, Trust3 AI, PhoenixAI, and Datastrato are aligned with the vision of catalog metadata exchange across the data and AI ecosystem.

We’re excited to announce support for catalog labels – a new capability in the Apache Iceberg™ REST Catalog API that enables platforms, engines, and agents to access context such as business purpose, ownership and data classifications maintained in Iceberg REST-compatible catalogs. This shared context supports discovery, governance, and agentic workflows across the data and AI ecosystem.

We believe that catalog metadata should be as open and portable as the data it describes. As enterprises bring more tools into their open lakehouse architectures, they need a common way to share the context that makes their data understandable, useful, and secure for all teams, regardless of what tools they use.

Today, that context often remains siloed in the source catalog. Data and AI teams must recreate classifications across platforms, maintain custom metadata synchronization pipelines, or work with agents that lack complete context.

Databricks is joined by Google Cloud, Salesforce, ClickHouse, Atlan, Collibra, DataHub, Immuta, Trust3 AI, PhoenixAI, and Datastrato in advancing this shared vision of metadata interoperability. Catalog labels offer a path toward that vision, making catalog context portable while allowing each platform to retain its own capabilities and controls.

![Sharing catalog metadata across data platforms, engines, and agents](/images/posts/754d4feb6b0f.png)

## An open standard for catalog context

Databricks worked with the Apache Iceberg community to add an optionallabels fieldto the Iceberg REST LoadTable response. This gives catalogs a standard way to expose table- and column-level context to other platforms, tools, and agents.

Labels are string key-value pairs that can describe business ownership, intended use, sensitivity or other catalog-maintained context. The standard defines a common format for sharing this metadata without prescribing its vocabulary or interpretation, giving each platform the flexibility to build on it in its own way.

## How labels provide context

Consider a table named support_cases

An authorized data steward assigns domain=customer_support and the Databricks system tag system.certification_status=certified to the table, and content_type=support_case_summary to the issue_summary column.

A catalog exposing these tags could include the following in its Iceberg REST LoadTable response:

This example shows only the labels portion of the response.

A downstream platform can then use these labels to make the table more useful:

- Improve discovery.A catalog can surface the business domain and intended purpose in search results, helping users identify relevant data without asking stewards to recreate that context.
- Give agents better context.An agent investigating support issues could use domain=customer_support and system.certification_status=certified to identify a relevant dataset, then use the column label to locate case summaries.
- Connect classifications to policies.A governance platform could map a sensitivity label to a locally defined masking rule, with the receiving platform responsible for configuring and enforcing that rule.

For example, PyIceberg hasadded support for accessing catalog labels in Python. In the next 0.13 release, applications will be able to inspect the table- and column-level labels from the same support_cases table:

This produces:

These labels make the catalog’s metadata available directly to Python applications, including data-discovery tools and agents.

## Tag Exchange advances open metadata exchange

Unity Catalog exposes its table- and column-level tags through catalog labels with Tag Exchange. Tag Exchange is a step toward our broader vision of open governance: context maintained in one system should be usable across every platform, engine, and AI agent working with the data.

By exposing Unity Catalog’s table- and column-level tags, Tag Exchange lets enterprises reuse classifications and business context for discovery, agent workflows, and access policies. Each tool has the freedom to decide how to interpret and use that context.

## Building an open ecosystem

Databricks is excited to join our partners in advancing catalog labels to make catalog metadata open and accessible.

Together, we’re in support of an open interface that gives AI agents and data platforms shared context for discovering data, understanding it, and keeping it governed.

Tag Exchangeis available in Beta today, exposing Unity Catalog’s table- and column-level tags through catalog labels. To get started, enable “Tag Exchange via Iceberg REST Catalog” in the Databricks Previews portal.

### What are catalog labels?

Catalog labels are string key-value pairs that share table- and column-level context through the Apache Iceberg REST Catalog API. They can describe business ownership, intended use, sensitivity, and other metadata, helping platforms, tools, and agents understand the data they access.

### How does Databricks support catalog labels?

Databricks supports catalog labels through Tag Exchange, which exposes Unity Catalog’s table- and column-level tags through the Apache Iceberg REST Catalog API. External platforms, tools, and agents can use this context for discovery, classification, and locally defined access policies.

Unity CatalogandOpen Source

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Sharing catalog metadata across data platforms, engines, and agents](https://www.databricks.com/blog/sharing-catalog-metadata-across-data-platforms-engines-and-agents)
> 
> 翻译时间：2026-11-24 12:13
