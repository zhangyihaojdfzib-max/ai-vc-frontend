---
title: Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines
  on Databricks
title_original: Announcing General Availability of Real-Time Mode for Spark Declarative
  Pipelines on Databricks
date: '2026-10-29'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Announcing General Availability of Real-Time Mode (RTM) on Spark Declarative Pipelines
  (SDP), delivering end-to-end processing latencie...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:47:59.519715'
---

[翻译失败，原文如下]

- Announcing General Availability of Real-Time Mode (RTM) on Spark Declarative Pipelines (SDP), delivering end-to-end processing latencies in the millisecond range for operational streaming workloads.
- Real-Time Mode eliminates the need for separate specialized engines such as Apache Flink, unifying batch, ETL, and low-latency streaming under a single framework.
- Real-Time Mode enables real-time computation and instant writes to operational stores via ForEach sinks, powering time-critical use cases like fraud detection and live personalization.

WeintroducedReal-Time Mode (RTM)last year which enabled customers to build low-latency, operational use cases. This was a game changer because it allowed customers to process streaming data in milliseconds, up to 100x faster than traditional micro-batch architecture. Furthermore, they no longer needed to maintain separate, specialized engines like Flink alongside Spark, eliminating duplicate codebases, fragmented governance models, and operational overhead.

Today, we are announcingRTM in Spark Declarative Pipelines (SDP)is now Genearally Available. SDP has become the standard way to build streaming and ETL pipelines on Databricks, automatically handling dependency resolution, incremental processing, orchestration, failure recovery, and data quality enforcement. With RTM, customers can build operational, low-latency pipelines while retaining all of those SDP benefits. Whether for fraud scoring, real-time alerting, or pushing fresh features to operational stores, you can now use SDP across all of these use cases.

## What Is Real-Time Mode (RTM)?

RTM is an evolution of the Spark Structured Streaming engine that achieves end-to-end latencies in the millisecond range. It does this by streaming data continuously, running all query stages simultaneously, and passing data between stages as soon as it is produced. For the full architecture deep dive, read the blog, “Breaking the microbatch barrier: The architecture of Apache Spark Real-Time Mode.”

RTM can support any workload that benefits from turning data into decisions in milliseconds. Some example use cases include fraud detection, live personalization, real-time recommendation systems, and real-time feature computation. We benchmarked RTM against Apache Flink on actual customer workloads performing feature computation, and RTM is up to 92% faster than specialized engines like Flink. Below are the benchmarks. For more information on the datasets and queries referenced, see thisGitHub repository.

![Apache Spark Real-Time Mode vs. Apache Flink](/images/posts/2752c24a41ce.png)

## Why RTM on Spark Declarative Pipelines

Customers are increasingly defaulting to SDP for their ETL workloads. With RTM, SDP now supports all streaming workloads, including operational low-latency streaming, enabling customers to use a single framework across all pipelines. One framework means one observability stack, one billing model, and no fragmentation across different APIs.

SDP serverless takes it further. There is no compute to choose and no cluster to size. You get sub-second latency, without any complex infra tuning, while paying only for the cores your query uses.  RTM flows also get SDP features such as versionless upgrades and low-downtime maintenance, which reduce both the operational work and the disruption of upgrades.

One use case where RTM on SDP has immediate impact is real-time feature computation. ML models for fraud detection or personalization depend on fresh signals, such as a user's total transaction amount over the last 10 minutes, to make accurate predictions. Computing these rolling-window aggregations and landing them in an online store within milliseconds is where RTM on SDP closes the gap. The Databricks Feature Store uses this exact architecture to deliverend-to-end p99 latency of 200ms from Kafka to the online feature store.

## Getting started with RTM on SDP

### Step 1: Configure the pipeline

Real-Time Mode requires the pipeline mode to becontinuousandspark.databricks.streaming.realTimeMode.enabledset totruetakes over.

### Step 2: Define a real-time update flow

Real-time mode requires an update flow. Usedp.create_sink()to define the output target, then use the@dp.update_flowdecorator withpipelines.triggerset to"RealTime"andtargetpointing to the sink.

For supported sources and sinks, see thedocumentation.

## Writing features to any custom sink

Use cases like fraud detection or real-time personalization require not only that features be computed in real time but also that they land in a queryable, low-latency store. A fraud model needs a customer's latest transaction before it clears, and a personalization engine needs to read what a user just browsed.

Today, you can write to any custom sink likeLakebase, Redis, or any other OLTP store from SDP using aForEach sink. Define the writer, register it as aforeach_sink, and wire it to anupdate_flow.

Features land in your operational store within milliseconds of being produced, with no offline-to-online sync in between. Applications and models can query them at ultra-low latency.What’s next for RTM on serverless?

- Running RTM pipelines at lower cost:Bin-pack multiple RTM flows into a single pipeline instead of each query standing up its own resources. The system also auto-tunes source and shuffle partitions based on workload, so users skip manual sizing.
- Expanded sink support:Native Lakebase sinkfor SDP, with built-in batching, automatic retries, and UC-managed authentication.

## Conclusion

RTM extends Spark Declarative Pipelines into a new class of workloads, operational, latency-sensitive applications that demand immediate response to streaming data. By bringing sub-second latency to the SDP APIs your team already uses, it eliminates the need to operate a separate framework or engine for your most time-critical pipelines. Whether you're building fraud detection pipelines, personalization engines, or ML feature computation systems, real-time mode gives you the latency your application demands with the simplicity of SDP.

Real-Time Mode on Spark Declarative Pipelines is now Generally Available.

## Technical Resources

Check out the following resources to get started with RTM on SDP:

- Documentation:Use Real-Time Mode on Lakeflow pipelines
- Documentation:Connect to Lakebase streaming sink
- Documentation:Use a ForEach sink to write each row in pipelines
- Code examples:Real-Time Mode on SDP examples

What is Real-Time Mode (RTM) in Spark Declarative Pipelines?

Real-time mode (RTM) lets Spark Declarative Pipelines (SDP) process streaming data with end-to-end latency in the millisecond range. It streams data continuously, runs all query stages at the same time and passes data between stages as soon as it's produced. Real-time pipelines benefit from SDP's orchestration and automatic failure recovery.

Is Real-Time Mode available in Spark Declarative Pipelines?

Yes. Real-time mode on Spark Declarative Pipelines is now generally available. It brings the real-time mode already available in Spark Structured Streaming to SDP pipelines.

How do I turn on real-time mode in a pipeline?

Set the pipeline tocontinuousmode and setspark.databricks.streaming.realTimeMode.enabledtotrue. Then define an update flow withpipelines.triggerset to"RealTime"and a target that points to a sink.

Can a real-time pipeline write to Lakebase or another OLTP store?

Yes. Define a ForEach sink with a writer that implementsopen,processandclose, then point a real-time flow at it. This works for Lakebase, Redis or any other OLTP store.

What use cases is Real-Time Mode in Spark Declarative Pipelines built for?

[翻译失败，原文如下]

Real-Time Mode is built for operational workloads that turn streaming data into decisions in milliseconds. Examples include fraud detection, live personalization, real-time recommendations and real-time feature computation. The Databricks feature store uses this architecture to reach a p99 latency of 200 ms from Apache Kafka to the online feature store.

Data Streaming,Data EngineeringandAnnouncements

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines on Databricks](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks)
> 
> 翻译时间：2026-10-30 08:47
