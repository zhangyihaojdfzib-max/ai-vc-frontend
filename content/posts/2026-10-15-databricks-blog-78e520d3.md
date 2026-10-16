---
title: Geospatial queries are up to 38X faster with Lakehouse//RT
title_original: Geospatial queries are up to 38X faster with Lakehouse//RT
date: '2026-10-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert
author: ''
summary: '[翻译失败，原文如下]


  - Spatial SQL and spatial joins are now supported on Lakehouse//RT, delivering ultra
  low latency and high concurrency directly on your go...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:41:08.819290'
---

[翻译失败，原文如下]

- Spatial SQL and spatial joins are now supported on Lakehouse//RT, delivering ultra low latency and high concurrency directly on your governed lakehouse data.
- Benchmarks show Lakehouse//RT delivers 38X faster spatial query performance than a traditional data warehouse with 50 concurrent users.
- No separate geospatial serving layer required. Spatial SQL on Lakehouse//RT combines real-time performance with open formats, Unity Catalog governance, and the full 100+ spatial function library.

Spatial SQL and spatial joins now run on Lakehouse//RT and they'reup to 38X fasterthan traditional cloud data warehouses.

Earlier this year, we broughtSpatial SQL to General Availabilityon Databricks: this included support for the GEOMETRY data type, 100+ spatial functions, high-performance spatial joins, AI/BI maps, Delta Sharing. The GEOMETRY and GEOGRAPHY data types are part of the open lakehouse, available in Apache Spark, and supported in the same underlying parquet files used by Delta and Iceberg v3. Customers across insurance, agriculture, energy, telecom, retail, logistics and more have adopted it to consolidate geospatial workloads onto a single governed platform.

Organizations with both spatial OLAP workloads and real-time location-based applications want great performance and high concurrency. Many of these organizations still rely on traditional data warehouses and build out specialized architectures for spatial applications, sometimes managing a separate stack centered on PostGIS for every use case just to meet latency requirements. Separate stacks lead to more copies of data, more synchronization pipelines, and more governance overhead.

Databricks now supports 4-pillars for geospatial workloads:Lakehousefor long-running spatial OLAP workloads,Lakebasefor spatial OLTP, apps, and agents,Databricks Appsfor purpose-built experiences, and now theLakehouse//RT warehousefor real-time analytics.

This blog covers what Lakehouse//RT delivers for spatial workloads, driving up to 38X performance improvement under high concurrency.

## OCT 2026 Geospatial performance on Lakehouse//RT

We benchmarked Lakehouse//RT against a traditional cloud data warehouse across a suite of spatial queries usingSpatialBench. By comparison, Lakehouse//RT delivers3X faster on average, and up to 20X fasteracross the tested queries.

![Bar chart showing Lakehouse//RT spatial query speedup versus a traditional data warehouse, up to 20x faster](/images/posts/6ead4709f1c0.png)

Under heavy load, the performance differences are even more significant. At 50 concurrent users, Lakehouse//RT deliversup to 38Xon the queries where the traditional warehouse could keep up.

![Bar chart showing Lakehouse//RT spatial query speedup versus a traditional data warehouse, up to 38x faster with 50 concurrent users.](/images/posts/9defa62e245e.png)

Try it for yourself: Follow the SpatialBench documentation to generate the synthetic data used in the benchmark queries from thispage.

Take a look at query #8. To follow best practices, it is recommended to remove the ST_GeomFromWKB call that converts data stored as well-known binary and instead use the native GEOMETRY data types. Using the native data types allows query optimizations and file-skipping to provide the best performance.

Three takeaways:

1. Lakehouse//RT is up to 38X faster, maintaining performance with high-concurrency.Even removing the most significant query improvement; the average speed-up is over 3.5X.
2. Lakehouse//RT is up to 20X faster with single-query concurrency.Every spatial benchmark query is faster on Lakehouse//RT.
3. No query changes or new licenses required.Spatial workloads are portable on Databricks; the same spatial queries you run on SQL Serverless today can run on Lakehouse//RT with no code changes.

## Spatial SQL use cases that benefit from Lakehouse//RT

![GIF showing examples of spatial use cases in oil and telecom](/images/posts/398681e89bcf.gif)

Spatial SQL on Databricks already serves a wide range of industries. With Lakehouse//RT, workloads can run with the real-time speed applications demand. Here are a few examples:

- Telecom and retail:Evaluate subscriber signal health in coverage areas and assess trade-area overlap for new store sites.
- Energy and natural resources:Intersect well locations against land leases, pipeline routes against suitability corridors, and renewable sites against terrain and infrastructure.
- Insurance and risk:Match policies to projected storm paths and calculate insured value at risk, provide real-time forecast updates to reinsurance partners.
- Logistics and delivery:Assign orders to the nearest service area instantly.
- Security and observability:Correlate threat signals with geographic boundaries and serve point-in-polygon lookups to dashboards and agents at high concurrency.

## Get started with Spatial SQL on a real-time data warehouse

Spatial SQL on Lakehouse//RT is available now in Beta. To get started:

1. Create aLakehouse//RT real-time warehousefrom the SQL Warehouses page
2. Run your existing spatial queries; no code changes needed
3. Explore theSpatial SQL documentationfor the full function reference

## Frequently asked questions

### What is Lakehouse//RT?

At Data + AI Summit 2026, weintroduced Lakehouse//RT, Databricks' newreal-time data warehousebuilt to deliver millisecond query performance at massive concurrency directly on yourlakehouse data. Lakehouse//RT was designed to solve a specific problem: as organizations expand data access across users, applications, dashboards, and AI agents, they need real-time responsiveness without copying data into a separate serving layer. Preview customers have seen significantly better performance overall with Lakehouse//RT vs. real-time serving layers, with latency as low as 10ms and concurrency as high as 12,000 queries per second.

### Can I run spatial SQL in real time on a lakehouse?

Yes. Spatial SQL and spatial joins now run on the Lakehouse//RT, so you can serve geospatial queries with low latency and high concurrency directly on your governed Delta and Iceberg tables. There is no need to copy data into a separate geospatial system or real-time analytics serving layer.

### Do I need to change my queries?

No. The same spatial functions and spatial joins you run on Databricks SQL Serverless today run on Lakehouse//RT with no code changes. You get the speedup by creating a Lakehouse//RT warehouse and pointing your existing queries at it.

### How much faster is Lakehouse//RT for spatial queries?

In head-to-head benchmarks against a traditional data warehouse, Lakehouse//RT runs spatial queries up to 38X faster under heavy load. On average, benchmark queries are 3.5X faster even when you exclude the largest increase.

### Is Spatial SQL on Lakehouse//RT available now?

Spatial SQL and spatial joins are available on Lakehouse//RT in Beta. To get started, create a Lakehouse//RT warehouse from the SQL Warehouses page and run your existing spatial queries with no code changes.

### If I have modeled my data using the H3 grid system, can I use the H3 functions on Lakehouse//RT as well as Spatial SQL functions?

Yes. All H3 expressions supported by Databricks Lakehouse are supported today with Lakehouse//RT. Read more about H3here.

### Does AI/BI support maps with Geometry and Geography data types?

Yes. You can create maps that use native geometry and geography data types in AI/BI dashboards. Read morehere.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Geospatial queries are up to 38X faster with Lakehouse//RT](https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert)
> 
> 翻译时间：2026-10-16 06:41
