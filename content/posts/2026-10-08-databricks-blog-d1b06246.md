---
title: Announcing Workday Data Connect federation in Unity Catalog
title_original: Announcing Workday Data Connect federation in Unity Catalog
date: '2026-10-08'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-workday-data-connect-federation-unity-catalog
author: ''
summary: '[翻译失败，原文如下]


  - Zero-copy access to Workday data:The new Workday Data Connect connector (Beta)
  lets Unity Catalog read Workday''s shared Iceberg tables ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-08T08:39:36.660661'
---

[翻译失败，原文如下]

- Zero-copy access to Workday data:The new Workday Data Connect connector (Beta) lets Unity Catalog read Workday's shared Iceberg tables directly from cloud storage without ingestion pipelines or duplicate data.
- Governed and performant:Queries run on Databricks compute with Unity Catalog governance including catalog, schema, table-level permissions and lineage over live Workday HR and finance data.
- Unlock workforce and financial insights with Genie:Use the new Workday Data Connect connector (Beta) to query current people and financial data in place, combine it with customer, market, and operational data already in Databricks, and enable Genie-powered natural-language exploration, real-time financial planning, workforce analytics, and AI on trusted, governed data.

We're excited to announce the publicly available Beta of the Workday Data Connect federation connector for Unity Catalog, built for data platform and analytics teams that need Workday HR and finance data alongside the rest of their enterprise data in Databricks. With Workday Data Connect now generally available, Databricks is bringing this new zero-copy capability to the Databricks Data + AI Platform.

The release builds on our partnership announced atWorkday Rising 2025, where Databricks was named a Workday Data Cloud launch partner. With this release, Databricks is one of the first of Workday Data Cloud's launch Data & AI platform partners to make a native Workday Data Connect federation connector publicly available, extending Workday's zero-copy data access directly into the Databricks Data + AI Platform.

Through Lakehouse Federation, data teams query HR and finance data in Workday Data Cloud directly from the Databricks Data + AI Platform without maintaining duplicate copies of data. Once this data is available through Unity Catalog, teams can use Databricks SQL, AI/BI, notebooks, and Genie to explore current Workday data alongside the rest of their enterprise data. This gives HR and finance teams a governed way to move from trusted data to timely answers and decisions.

## How Workday Data Connect federation works

The connector gives administrators one compact path from Workday sharing to governed Databricks queries:

1. A Workday administrator shares approved HR and finance tables through Workday Data Cloud and grants a Workday Integration System User read access.
2. A Databricks administrator creates one OAuth connection and a foreign catalog in Unity Catalog.
3. Unity Catalog resolves the foreign catalog metadata, and Databricks compute reads the corresponding data from Workday
4. A Databricks administrator governs access to the foreign catalog through Unity Catalog’s robust table-level access controls.
5. Users query the resulting catalog with standard SQL in Databricks or in natural-language with Genie.

This means you can:

- Access data without an ingestion pipeline:Discover and query shared Workday tables from Databricks. Access is read-only, so Workday remains the system of record for HR and finance data.
- Govern access through Unity Catalog:Apply catalog-, schema-, and table-level permissions and use the lineage and auditing available for the foreign catalog alongside other Unity Catalog assets.
- Run analysis in Databricks:Databricks reads the shared data directly from Workday’s managed object storage and executes the query, so teams can use Databricks SQL, AI/BI, notebooks, Genie, and downstream data and AI workloads with Workday data.

## What you can build with governed Workday data

Once Workday's people and money data is federated into Unity Catalog, you can combine it with the rest of your enterprise data without moving any of it:

- Explore Workday data with Genie:With Workday HR and finance data available in Unity Catalog, teams can use Genie to ask natural-language questions about workforce and financial trends.

Real-time financial planning:Unify Workday financial data with market, risk, or sales data in Databricks to power forecasting and scenario planning, and accelerate the close.

- Workforce analytics:Blend Workday workforce and talent data with operational metrics to understand which teams drive the most impact, and model retention and performance.
- AI and agents on trusted data:Feed governed, current Workday data into AI applications, models, and agents on Databricks without stale exports, no brittle custom integrations.

Because the data never leaves its source of truth and Unity Catalog governs every read, you get fresh, trusted data with the controls your HR and finance teams require. This helps organizations build enterprise AI on open, governed data while maintaining consistent access controls across analytics and AI workloads.

## Three ways to bring Workday data into Databricks

Different teams need Workday data in different shapes: a durable copy for historical reporting, an on-demand lookup, or a governed live view for analytics. Databricks now offers three complementary paths, so you can pick the right one per use case instead of forcing everything through a single pipeline.

All three are native to the platform: governed by Unity Catalog, and ready for Databricks SQL, AI/BI, Genie and downstream AI applications and agents. With this release, Databricks introduces catalog federation as the newest way to access Workday Data Cloud data in place.

## Getting started

Enabling Workday Data Connect federation is a short collaboration between your Workday administrator and your Databricks administrator:

1. In Workday: Enable Workday Data Connect for your tenant and share the tables you want to query through its Iceberg REST catalog.
2. Register an API client with a JWT Bearer Grant, upload the public key, and register an Integration System User (ISU) as a principal with a role that grants read access to the shared tables. See Get Started with Workday Data Lake and Register API Client for Data Lake (JWT Bearer Grant).
3. In Databricks: Create a connection and a foreign catalog, then grant access and query. Databricks performs the OAuth token exchange with Workday's Iceberg REST catalog for you — you never manage a Workday token endpoint.

![image2.gif](/images/posts/67eefdd96710.gif)

Requirements: A Unity Catalog enabled workspace and Databricks compute on Databricks Runtime 19 or above. With the connector in Beta, a workspace admin is required to enable it from the Previews page. Note that this connector does not ingest or copy data into Databricks, and is separate from the Lakeflow Connect ingestion connectors for Workday.

## Frequently Asked Questions

### What is Workday Data Connect federation in Databricks?

Workday Data Connect federation is a Lakehouse Federation connector for Unity Catalog, now in Beta. It lets Databricks query Workday HR and finance data in place, reading Workday's shared Iceberg tables directly from cloud storage. There are no ingestion pipelines and no duplicate copies of data.

### How does catalog federation differ from query federation?

Query federation sends SQL to an external database and runs it on that system's compute. Catalog federation, which Workday Data Connect uses, gets table metadata from Workday's Iceberg REST catalog. Databricks compute then reads the data straight from Workday's managed object storage and runs the query itself. Either way, Unity Catalog governs access.

### Does the Workday connector copy data into Databricks?

No. Access is zero-copy and read-only, so Workday Data Cloud stays the system of record for HR and finance data. If you need a durable copy with history tracking (SCD2), use Lakeflow Connect for Workday Reports and Workday HCM instead.

### How is Workday data governed in Databricks?

Unity Catalog governs every query of federated Workday data. Administrators set catalog-, schema- and table-level permissions. Lineage and auditing work the same way as for other Unity Catalog assets.

### What are the ways to bring Workday data into Databricks?

[翻译失败，原文如下]

There are three, all governed by Unity Catalog:

- Lakeflow Connect: managed, incremental ingestion into Delta tables, for durable copies and scheduled pipelines.
- Workday Data Connect federation (Beta): zero-copy analytics on Workday's shared Iceberg tables, joined with your other enterprise data.
- Live Data Query through a JDBC connection: on-demand, real-time lookups that store nothing.

### How can I use Workday data with Genie?

Once Workday Data Cloud data is available through a Unity Catalog foreign catalog and the appropriate permissions are granted, teams can use it alongside other governed Databricks data in Genie. Example questions include:

- Which cost centers had the fastest headcount growth this quarter?
- How does attrition vary by region and job family?
- How do workforce changes compare with bookings or operating expenses?

Ready to bring Workday data into your Databricks Data + AI Platform?

- Read the docs:Workday Data Connect catalog federation, theJDBC connection example for Workday Live Data Query, andLakeflow Connect for Workday Reports,Workday HCM, andWorkday Activity Logging
- Learn more aboutWorkday Data Cloudand the Databricks partnership.
- To join the Beta, contact your Databricks account team.

---

> 本文由AI自动翻译，原文链接：[Announcing Workday Data Connect federation in Unity Catalog](https://www.databricks.com/blog/announcing-workday-data-connect-federation-unity-catalog)
> 
> 翻译时间：2026-10-08 08:39
