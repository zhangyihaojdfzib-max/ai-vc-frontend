---
title: 'Building for the AI Era: Lakebase, Streaming, and Lakehouse Innovations at
  VLDB 2026'
title_original: 'Building for the AI Era: Lakebase, Streaming, and Lakehouse Innovations
  at VLDB 2026'
date: '2026-08-27'
source: Databricks Blog
source_url: https://www.databricks.com/blog/building-ai-era-lakebase-streaming-and-lakehouse-innovations-vldb-2026
author: ''
summary: '[翻译失败，原文如下]


  - Discover the Databricks innovations around Lakebase, Structured Streaming, and
  Lakehouse optimizations

  - Understand how Lakebase, a thi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-30T07:44:58.429611'
---

[翻译失败，原文如下]

- Discover the Databricks innovations around Lakebase, Structured Streaming, and Lakehouse optimizations
- Understand how Lakebase, a third generation cloud database that decouples transactional compute from storage, is well suited for agentic workflows
- Meet our Engineering and Recruiting teams at VLDB

We are headed toVLDB 2026to share multiple innovations that power the Databricks platform.  Databricks Co-founder and Chief Architect, Reynold Xin, will kick-off the conference with the opening keynote. Databricks has four accepted papers related to Lakebase, Spark Structured Streaming, and automatic Lakehouse optimizations. The demo paper on the Enzyme engine will showcase how we incrementally maintain materialized views. Below is a preview of these presentations.

Keynote: The Three Golden Ages of Database Engineering

Databricks Co-Founder Reynold Xin will discuss how AI agents are ushering in the "third golden age" of database engineering. Some of you may remember his early 2012 work at Berkeley on the scalable analytical system calledShark. Reynold will reflect on how his own perspective on database technology has evolved over the years from his Berkeley days, through the rise of Lakehouse architecture, and now the changing demands on transactional and analytics engines. He will introduce two new paradigms that will help meet the needs of AI agents: (1)  Lakebase, which applies storage and compute separation to OLTP database, and (2)  LTAP (Lake Transactional Analytical Processing) which unifies transactional and analytical processing.

Lakebase: Serverless Postgres over Open Lake Storage

AI agent workloads are creating unique usage patterns such as millions of short-lived, deeply branched databases. Traditional OLTP engines are monolithic and cannot meet these challenging requirements. Stas Kelvich will present the Lakebase architecture, which is a third-generation cloud database architecture. Lakebase meets the requirements of agentic workflows by decoupling serverless PostgreSQL compute from storage, persisting data and write-ahead logs directly in cloud object storage using open formats. Lakebase not only provides sub-second cold starts but also efficient Git-like database workflows using copy-on-write branching. Furthermore, with its compute-storage separation, it enables low-latency analytics on live transactional data. Figure 1 shows how Lakebase is ushering in the third generation of cloud databases.

![](/images/posts/d48b2237bd5c.png)

Figure 1: Lakebase Postgres is well suited for the agentic era and is built on top of the open data lake.

A Decade of Apache Spark Structured Streaming: How We Evolved the Architecture to Meet Real-World Needs

Structured Streaming powers millions of weekly jobs at Databricks. It uses a unique micro-batch processing architecture which has advantages of scalability, fault tolerance, and exactly-once semantics compared to other designs. However, Structured Streaming required many new innovations to meet the demands of real-world customers and reach today’s scale. Siying Dong will present how the streaming architecture has evolved over the years— microbatch pipelining improved throughput by up to 3x, new stateful APIs makes it easy to express complex business logic, and the system now supports fine grained access control.

AutoLiquid: Autonomic Data Layout Optimization for the Databricks Lakehouse

Clustering tables by keys can significantly improve query performance. However, selecting optimal clustering keys manually across millions of lakehouse tables does not scale. Yunjia Zhang will describe how AutoLiquid automates this lifecycle via a simple CLUSTER BY AUTO primitive. AutoLiquid uses a combination of heuristics for key selection and efficient shadow verification to cluster millions of tables. Using these techniques, AutoLiquid is able to outperform customer-selected keys on over 95% of evaluated workloads.

Ultron: History-Based Query Optimization at Databricks

The latency of Lakehouse queries can be significantly improved if only the optimizer had near perfect knowledge about the data. Ultron is a history based query optimization framework that leverages the repetitive nature of analytical workloads to improve optimizer choices, such as selecting the type of join operator. Eric Liang will describe the architecture of Ultron including how it efficiently stores the history and manages the logs of executed queries. Ultron has significantly improved performance of production workloads including improving the median join latency by 25%.

In addition to these four papers, join us to watch Yuhong Chen demonstrate Enzyme, our incremental view maintenance engine for data engineering workloads.

Agent-Native Data Infrastructure: LakehouseRT, Lakebase, and LTAP (Sponsor talk)Databricks is a Gold Sponsor of VLDB 2026. Ippokratis Pandis will give the Databricks sponsor talk where he will describe how Databricks is evolving its system architecture to accommodate the autonomous, agentic loops. With this in mind, we will present LakehouseRT. LakehouseRT is powered by the new Reyden engine and is designed for real-time low-latency analytics directly over open lake storage. The combination of Lakebase and LakehouseRT provides the foundation to deliver the first true Lake Transactional Analytical Processing (LTAP) system.

Meet the Team at VLDB 2026

Stop by the Databricks booth to connect with our engineering and research teams, discuss our papers, and speak to our recruiters.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Building for the AI Era: Lakebase, Streaming, and Lakehouse Innovations at VLDB 2026](https://www.databricks.com/blog/building-ai-era-lakebase-streaming-and-lakehouse-innovations-vldb-2026)
> 
> 翻译时间：2026-08-30 07:44
