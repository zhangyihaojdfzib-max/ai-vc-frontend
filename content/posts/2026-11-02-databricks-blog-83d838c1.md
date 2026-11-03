---
title: Lakebase Postgres is now generally available on Google Cloud
title_original: Lakebase Postgres is now generally available on Google Cloud
date: '2026-11-02'
source: Databricks Blog
source_url: https://www.databricks.com/blog/lakebase-postgres-now-generally-available-google-cloud
author: ''
summary: '[翻译失败，原文如下]


  - Lakebase Postgres, a fully managed, serverless Postgres database, is now generally
  available on Google Cloud.

  - Autoscaling, scale to z...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-03T09:14:47.179187'
---

[翻译失败，原文如下]

- Lakebase Postgres, a fully managed, serverless Postgres database, is now generally available on Google Cloud.
- Autoscaling, scale to zero, instant branching, and point-in-time recovery help teams build and ship faster without managing database infrastructure.
- Operational and analytical data share the same storage foundation so analytics, apps and agents run on a unified platform with no fragile pipelines to maintain.

We're excited to announce that Lakebase Postgres is generally available on Google Cloud. Teams building on Google Cloud can now run production-grade, serverless Postgres directly on the Databricks Data + AI Platform.

The Lakebase architecture separates compute from storage, which removes the resource conflicts and infrastructure overhead of traditional databases. It also shares the same storage layer as your analytical data which eliminates the need to build and maintain pipelines. The result is a Postgres database that scales with your application, shares one governance model with the rest of your data estate, and reduces your total cost of ownership.

## Lakebase Postgres removes operational barriers, allowing teams to ship faster

For years, transactional databases and analytics platforms have been kept separate. Moving operational data into the lakehouse meant building and maintaining ETL pipelines, duplicating storage and accepting data lag. Now that AI agents act on data in real-time, that operational overhead becomes a bigger liability.

Instead with Lakebase, operational workloads run on the same platform, with the same security and governance as your analytics and AI. There is no siloed database to manage, no separate access controls to maintain and no data movement to keep in sync. Lakebase is a key component of theLake Transactional/Analytical Processing (LTAP) architecturewhich allows organizations to unify their data foundation, decrease operational overhead and lower infrastructure costs.

Lakebase Postgres on Google Clouddelivers the capabilities for teams to ship faster:

- Serverless autoscaling and scale to zero:Compute adjusts to match traffic and shuts off when idle, so you aren't paying for capacity you don't use.
- Instant branching:Create isolated, zero-copy branches of production data in seconds to test changes safely.
- Point-in-time recovery (PITR):Restore your database to a specific moment to recover from bugs or accidental deletions.
- Standard Postgres:Use the tools, drivers, and extensions you already know, including built-in search engine (pgvector-compatible) for AI-driven search.
- Unified governance with Unity Catalog:Apply consistent access control, lineage, and auditing across operational, analytical, and AI data.

## Built on the trust and scale of Google Cloud

In addition to allowing teams to build faster, Lakebase Postgres on Google Cloud delivers the scale, reliability and security production workloads demand:

- Enterprise-grade availability:Multi-zone high-availability endpoints with automatic failover are backed by a 99.99% SLA, and single-zone endpoints by a 99.9% SLA.
- Private connectivity (Beta):Enterprise customers can keep database traffic off the public internet withGoogle Cloud Private Service Connect, connecting applications in their own VPC directly to Lakebase.
- Unified identity and access:Users and service principals authenticate with Databricks OAuth or native Postgres credentials, and access is governed centrally in Unity Catalog.
- Scalable search in Postgres:Combine vector and full-text search directly in Lakebase Postgres for 2x throughput than pgvector at 4x lower cost (no second system, no sync pipelines) withLakebase Search.
- Optimize data ingestion:Direct writesallows you to push enriched lakehouse data into Lakebase Postgres without slowing down your app. Testing shows loading 1TB of data takes less than five minutes.

## Get started with Lakebase Postgres on Google Cloud

Lakebase Postgres on Google Cloud gives you a production-ready foundation for the next generation of apps and AI agents, with no infrastructure to manage and no pipelines to maintain. As of GA, it is available in the following regions:

- asia-southeast1
- europe-west3
- us-central1
- us-east4
- us-west1

Create your first Lakebase project from your Databricks workspace on Google Cloud, connect with your existing Postgres tools, and start building in minutes.

New to Databricks? Get started for freehere.

Announcements

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Lakebase Postgres is now generally available on Google Cloud](https://www.databricks.com/blog/lakebase-postgres-now-generally-available-google-cloud)
> 
> 翻译时间：2026-11-03 09:14
