---
title: Announcing General Availability of native Lakebase Postgres sink for Spark
  Structured Streaming
title_original: Announcing General Availability of native Lakebase Postgres sink for
  Spark Structured Streaming
date: '2026-11-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-general-availability-native-lakebase-postgres-sink-spark-structured-streaming
author: ''
summary: '[翻译失败，原文如下]


  - Announcing General Availability of the native Lakebase sink for Apache Spark™
  Structured Streaming: stream computed results directly in...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-24T12:13:03.106783'
---

[翻译失败，原文如下]

- Announcing General Availability of the native Lakebase sink for Apache Spark™ Structured Streaming: stream computed results directly into Lakebase with a single writeStream call, replacing custom foreach writers.
- Learn how Real-Time Mode and the native Lakebase sink together enable real-time feature computation and ingestion into Lakebase in one streaming pipeline.
- See it in action on a real-time feature pipeline, upserting ~20K EPS for 5 million users into Lakebase at p99 under 500 ms, end-to-end.

Low-latency use cases like fraud detection, live personalization, and real-time feature computation need computed results in a serving-ready OLTP store.Lakebase Postgresis Databricks' fully managed, serverless PostgreSQL database offering, with autoscaling, branching, native Unity Catalog integration, and sub 10ms reads. But writing to it from a streaming pipeline has meant building a customforeachwriter and handling batching, retries, and upserts yourself, which is complex to get right and hard to keep performant under load.

Today, we are announcing the general availability of thenative Lakebase sinkfor Apache Spark™ Structured Streaming, a connector that writes computed results directly toLakebaseand handles all of that for you. The same connector works in both micro-batch andReal-Time Mode. We show it on a feature pipeline that ingests watch and like events from a video streaming platform, computes each user's recent activity, and upserts one feature row per user into Lakebase in hundreds of milliseconds. You get that performance without building or maintaining the connector yourself.

## Why the native Lakebase sink matters

### The problem it solves

Aforeachwriter has to do a lot at once: batch writes for throughput, a bounded queue for backpressure, pool connections and refresh OAuth tokens, retry transient failures with backoff, deduplicate within a batch. It also has to implement upsert semantics correctly, including keeping the greatest timestamp or updating a column only when an incoming event has a newer ordering value.

Even for an experienced developer, writing and tuning all of this is weeks of work, and it does not end there. The connector turns into something you maintain, fixing throughput regressions, credential refresh, and keeping the code current with the latest versions. For a sense of what that looks like in practice, see thisreference implementation.

### What it handles for you

The native sink takes care of it. You wire up a Lakebase write in minutes with a singlewriteStreamcall, and spend no time on performance, tuning, or maintaining the connector. You get:

- Ease of use:no custom sink code; batching, connection reuse, and error handling are built in.
- Upserts:declare anupsertkeyand the sink maintains one row per key.
- Merge strategies for upserts:declarative custom merge logic for how non-key columns update on conflict. Seesupported merge strategies.
- Reliable delivery:transient JDBC errors (connection failures, deadlocks, rate limiting) are retried automatically with exponential backoff.
- A familiar API:the samewriteStreamand.toTable()used for Unity Catalog tables.
- Tunable batching:optional caps onbatch size and intervalwhen the defaults don't fit your SLA.
- UC-managed authentication:the connector authenticates to Lakebase automatically as the running user or service principal.

## Example: A real-time feature pipeline for recommendation systems

### Use case

A video streaming provider wants to recommend videos to its viewers. A recommendation model needs what users watched most recently. So for each user we compute the last 6 videos they watched and the last 3 they liked. We store that as one row per user in Lakebase. At inference time, the recommendation model looks up that row byuser_idto rank what to show next.

### The pipeline

A feature is an input the model uses to make a prediction. Here, the features are each user's recent activity, computed from a stream of events. Each event has auser_idand avideo_idand an event type (WATCH/LIKE). For each user we keep their recent watches and likes as one row, keyed byuser_id. Every new event for auser_idupdates that row in place.

The pipeline is three stages:

- Stream:read engagement events from Kafka.
- Transform:group byuser_idand maintain each user's last-6 watched and last-3 liked withtransformWithState, emitting one feature row per user.
- Write:upsert that row into Lakebase with the native sink.

### Writing to Lakebase

Writing to Lakebase is a singlewriteStreamcall. How you point it at Lakebase depends on whether the target table is registered in Unity Catalog.

If the Lakebase table isregistered in Unity Catalog, write with.toTable()using the fully qualifiedcatalog.schema.table. The connector manages credentials as the running user or service principal, and creates the table if it doesn't exist:

If the Lakebase table isn't registered in Unity Catalog, write to the Lakebase endpoint directly withformat("postgresql")(seeLakebase tables not registered with Unity Catalog). The sameformat("postgresql")path also supports writing to external PostgreSQL databases (e.g. Amazon RDS or self-hosted) via aUnity Catalog connection(DBR 19+, Public Preview).

### Serving the features

The sink writes the features into Lakebase within 100-200 milliseconds of being produced, with no offline-to-online sync in between. Applications and models can query them in single-digit milliseconds. This supports two patterns:

- An application fetching a user's features byuser_id, a low-latency single-row lookup.
- A model reads those same features for real-time inference, so its predictions reflect what the users just did.

For a deeper look at the implementation, see thecompanion repo, a self-serve example you can run end-to-end.

## How the sink performs at scale

We ran the pipeline at a sustained input rate of ~20K events/sec against 5 million active users, each accumulating watch and like history. The cluster used was a 40-core classic compute (DBR 18 LTS) writing to an 8-CU Lakebase project with 5-minute RTM checkpoint intervals.

Every event is an upsert that overwrites that user's existing feature row in Lakebase. As state builds up, the sink is continuously upserting against a table with millions of existing rows, finding and replacing the row for eachuser_idon every event. This is the workload pattern that breaks customforeachwriters at scale.

End-to-end latency is measured from the Kafka input timestamp to the row landing in Lakebase.

Metric

Value

Input throughput

20k Events per sec (1 hour sustained)

Active user (state cardinality)

5,000,000

P50 (end-to-end latency)

183 ms

P99 (end-to-end latency)

354 ms

Note: This illustrative example uses synthetic data replayed into Kafka. The test ran for 60 minutes, achieving ~20K EPS and 63.5 million upserts.

These latencies are specific to this setup. Your numbers will differ with input rate, the amount of state you keep, RTM cluster size, and Lakebase size. Size both the cluster and Lakebase to sustain the throughput you need. The sink also lets you tune how it batches writes usingbatchintervalandbatchsize. Seeperformance tuning.

### Lakebase server-side throughput

At this throughput on an 8-CU project,pg_stat_statementsshows 63.5 million upserts averaging ~0.015 milliseconds per statement. Lakebase had headroom to spare. For a deeper look at how Lakebase achieves this, see the blog,How Lakebase Architecture Delivers 5x Faster Postgres Writes.

## Conclusion

With Real-Time Mode computing features as events arrive and the native Lakebase sink enabling writes directly to a serving-ready OLTP database, together they unblock real-time feature computation and ingestion in one streaming pipeline.

[翻译失败，原文如下]

The native sink gives you a first-class experience when writing to Lakebase, using the samewriteStreamAPI you already know. We showed it on a recommendation feature pipeline, but the same pattern works wherever a streaming pipeline needs to write computed results to a database for immediate serving.

The native Lakebase sink for Spark Structured Streaming is now Generally Available.

### Try it yourself

- Companion repo:run the full feature pipeline end-to-end in your workspace.
- Write to Lakebase from Structured Streaming:sink configuration, supported triggers, output modes, and tuning options.
- Lakebase Postgres:instance setup, UC integration, and serving.

What is the native Lakebase sink for Spark Structured Streaming?

It’s a Structured Streaming connector that writes computed results directly to Lakebase. It handles batching, retries, connection pooling, deduplication, upserts, and workspace-managed authentication, so you don’t build a customforeachwriter. The same connector works in both micro-batch and Real-Time Mode.

Is the native Lakebase sink generally available?

Yes. The native Lakebase sink for Spark Structured Streaming is now generally available on Databricks Runtime 18 LTS and above. The RealTime and ProcessingTime triggers run on classic compute; on serverless, useTrigger.AvailableNow. It isn’t supported in Lakeflow Declarative Pipelines.

How do I write to Lakebase with the sink?

For a Lakebase table registered in Unity Catalog, use.toTable()with the fully qualifiedcatalog.schema.table; the connector manages credentials and creates the table if it doesn’t exist. For an unregistered table, useformat("postgresql")with the Lakebaseendpointanddbtable.

Does the sink support upserts and custom merge logic?

Yes. Declare anupsertkeyand the sink maintains one row per key. Merge strategies (DBR 19+) control how non-key columns update on conflict, such as keeping the latest non-null value or the value from the newest event, with no hand-writtenON CONFLICTSQL.

What use cases is the native Lakebase sink built for?

The native Lakebase sink is built for operational dashboards, app databases, and low-latency feature stores.. Examples include real-time feature computation for recommendations and personalization, and fraud detection.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Announcing General Availability of native Lakebase Postgres sink for Spark Structured Streaming](https://www.databricks.com/blog/announcing-general-availability-native-lakebase-postgres-sink-spark-structured-streaming)
> 
> 翻译时间：2026-11-24 12:13
