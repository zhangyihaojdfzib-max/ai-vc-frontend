---
title: 'Apache Spark vs Apache Flink: which should you use?'
title_original: 'Apache Spark vs Apache Flink: which should you use?'
date: '2026-11-14'
source: Databricks Blog
source_url: https://www.databricks.com/blog/spark-vs-flink
author: ''
summary: '[翻译失败，原文如下]


  - Apache Spark is the default choice for most teams: one engine runs batch, SQL,
  machine learning and streaming, now down to millisecond ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-14T08:49:36.229147'
---

[翻译失败，原文如下]

- Apache Spark is the default choice for most teams: one engine runs batch, SQL, machine learning and streaming, now down to millisecond latency with Real-Time Mode.
- In a Databricks benchmark, Spark Real-Time Mode matched or beat Apache Flink on p99 latency for stateless, aggregation and join workloads.
- Flink remains a fit for specialized cases such as very large keyed state or complex event processing on an existing Flink platform.

For most teams, Apache Spark™ is the better choice. Spark runs batch ETL, SQL analytics, machine learning and streaming on one engine, andReal-Time Modenow brings Spark streaming to millisecond, end-to-end latency. Apache Flink is a stream-native engine that fits specialized event-processing workloads, but choosing it usually means running a second engine next to Spark.

The latency gap used to be the main reason teams added Flink. With Real-Time Mode, that reason has largely gone away, and the real question becomes how many engines you want to build, operate and govern.

## What is the difference between Apache Spark and Apache Flink?

Spark is a unified engine for batch, streaming, SQL and AI, and Flink is a specialized stream processor. Both are open source Apache Software Foundation projects with exactly-once processing, stateful operators and SQL APIs. The difference is scope.

Spark started as a batch engine and addedStructured Streaming, which treats a stream as a table that keeps growing. The same DataFrame and SQL code runs as a scheduled batch job, a micro-batch stream or a Real-Time Mode stream. Flink was designed for streaming first and treats batch as a bounded stream.

## How do Spark and Flink compare feature by feature?

This table compares the two engines on the dimensions that usually decide the choice.

Table 1. Apache Spark and Apache Flink compared. Sources:Apache Spark Real-Time Mode docs,Apache Flink 2.0 releaseandFlink CEP docs.

## Is Spark faster than Flink for streaming?

In Databricks' published benchmark, Spark Real-Time Mode matched Flink on stateless work and had lower p99 latency on stateful aggregation and stream-static joins. Thebenchmark codeis public, uses customer-derived feature-computation workloads and runs at 10,000 records per second for 30 minutes, measuring Kafka input-to-output latency. Databricks summarized the results asup to 92% faster than Flink.

![Figure 2. p99 end-to-end latency at 10,000 records per second. Spark Real-Time Mode shows its worst run and Flink shows its best run.](/images/posts/4829017eb708.png)

How to read these numbers:Databricks ran the benchmark. Spark ran on Databricks and Flink ran on AWS Managed Service for Apache Flink 1.18. The results compare Spark's worst run with Flink's best run. Treat them as evidence for these workload patterns, and test your own pipeline before deciding.

Production results tell the same story.MakeMyTripconsidered Flink, chose Spark Real-Time Mode to avoid a second engine and cut P50 latency to 44 ms and P99 from more than a minute to about 500 ms. Coinbase and DraftKings also run Real-Time Mode in production. For how the engine achieves this, readBreaking the microbatch barrier.

## How do I get Flink-like latency in Spark?

You change the trigger. Real-Time Mode is a trigger on an existing Structured Streaming query, so the same code moves between latency tiers without a rewrite.

Real-Time Mode needs update output mode and reads from and writes to Kafka or a row-level foreach sink. Stateful operators arrive in open source with Apache Spark 4.3 and are generally available on Databricks today. On Databricks, it runs onclassic computeor inLakeflow Spark Declarative Pipelines. See theReal-Time Mode referencefor the full support matrix.

### The agentic AI playbook for the enterprise

![ai](/images/posts/739dac6fa259.png)

## When should I choose Apache Flink over Spark?

Flink can be the better fit for a small set of specialized streaming workloads. Consider it when most of these are true:

- Very large keyed state.Flink 2.x disaggregated state is built for state far larger than local disk.
- Complex event processing.You need pattern matching across event sequences with Flink CEP or SQL MATCH_RECOGNIZE.
- Event-time timers on the low-latency path.Your logic depends heavily on event-time timers, which Spark Real-Time Mode does not yet support in transformWithState.
- An existing Flink platform.You already run Flink in production and the stream doesn't feed batch, SQL or ML.

If the stream also feeds analytics, ML features or lakehouse tables, Spark avoids duplicating logic, operations and governance across two engines.

![Figure 3. A decision guide for choosing between Apache Spark and Apache Flink.](/images/posts/e78cf0347bfe.png)

## Why does running one engine matter?

Every second engine adds a second codebase, a second skill set and a second set of governance rules. Teams that pair Spark for batch with Flink for streaming often rewrite the same business logic twice and debug drift between them.

- One codebase.The same DataFrame and SQL logic runs as batch, micro-batch or Real-Time Mode.
- One team.Python and SQL developers build real-time pipelines without learning a new runtime.
- One governance model.Streaming tables and batch tables share lineage and access control in Unity Catalog.
- One path to AI.The same pipelines build ML features for training and online inference, as DraftKings does with transformWithState.

Pipelines can also be declared instead of hand-wired.Spark Declarative Pipelinesmanage dependencies and incremental refresh for streaming tables.

## Running Spark streaming on Databricks

Databricks was founded by the original creators of Apache Spark and runs Real-Time Mode as a generally available feature, including stateful operators andtransformWithState. It adds Lakeflow Spark Declarative Pipelines, Unity Catalog governance and serverless pipelines. Code written for open source Spark runs on Databricks unchanged. To get started, follow theApache Spark tutorial: Real-Time Mode.

### Is Apache Spark faster than Apache Flink?

In Databricks' published benchmark, Spark Real-Time Mode matched Flink on stateless workloads and had lower p99 latency on stateful aggregation and stream-static joins. Results depend on the workload, so benchmark your own pipeline.

### Is Spark streaming still micro-batch?

Not only. Spark Structured Streaming defaults to micro-batch, and Real-Time Mode processes records continuously with millisecond latency. You choose per query by setting the trigger.

### Do I need Flink if I already use Spark?

For most workloads, no. Real-Time Mode gives Spark millisecond latency on the same engine you use for batch, SQL and ML, so you run one system instead of two.

### When is Flink the better choice?

Flink can fit specialized workloads such as very large keyed state, complex event processing or teams that already run a Flink platform for standalone streams.

### Can I migrate a Flink job to Spark?

Yes. Most Flink SQL and DataStream logic maps to Spark SQL and DataFrames in Structured Streaming, and Real-Time Mode covers the low-latency path. Start with stateless and aggregation jobs, then move stateful logic to transformWithState.

Get started with Real-Time Mode on Databricks

---

> 本文由AI自动翻译，原文链接：[Apache Spark vs Apache Flink: which should you use?](https://www.databricks.com/blog/spark-vs-flink)
> 
> 翻译时间：2026-11-14 08:49
