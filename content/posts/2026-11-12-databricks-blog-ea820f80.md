---
title: 'Lakehouse//RT: Scale real-time analytics, not your bill'
title_original: 'Lakehouse//RT: Scale real-time analytics, not your bill'
date: '2026-11-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/lakehousert-scale-real-time-analytics-not-your-bill
author: ''
summary: '[翻译失败，原文如下]


  - AI agents can multiply real-time query volume almost overnight, and teams want
  to know whether their bill will multiply with it.

  - Lake...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-16T08:50:37.854419'
---

[翻译失败，原文如下]

- AI agents can multiply real-time query volume almost overnight, and teams want to know whether their bill will multiply with it.
- Lakehouse//RT is intentionally built to absorb that demand without a proportional cost increase
- Customers that chose Lakehouse//RT over separate real-time serving layers report 6x to 10x lower infrastructure costs

AI agents are pushing the limits of data warehouses. A human analyst might run a few dozen queries in an afternoon. An agent can run hundreds per second, around the clock. And with growing demand for use cases like customer-facing dashboards that refresh in milliseconds and applications with embedded analytics, real-time workloads are quickly becoming a standard part of how businesses use data.

Most data warehouses were designed for human-scale query volume, not the sustained concurrency agents generate. And even when a warehouse can deliver low latency, the bill grows as fast as demand: 10x the queries could easily mean 10x the cost.

We builtLakehouse//RTnot only to serve real-time workloads directly on thelakehouse, but to do so without growing your costs at the same rate as your queries.

## Why is real-time analytics cost efficient on Lakehouse//RT?

Most data warehouses scale capacity in step with demand: more queries, more compute, more cost. That works well for many analytics workloads, where query volume tracks the number of people asking questions. Real-time workloads are different. When AI agents and thousands of concurrent users all need answers in milliseconds, query volume can grow far faster than headcount, and cost grows with it.

Real-time workloads are also often spiky. The usual way to handle that is to overprovision: add capacity in large blocks and keep it running so latency holds up at peak. You end up paying for idle compute most of the day.

Lakehouse//RT flips the equation. Instead of scaling cost with demand, it scales efficiency. Its engine is architected to serve dramatically more queries on the same resources, so when demand doubles (or increases tenfold), your infrastructure keeps pace without a proportional spike in spend.

![Animation of a demand curve. Agent demand grows at a steep angle, with traditional warehouse costs following the same curve. Lakehouse//RT cost is a much flatter curve, with the gap indicating savings. ](/images/posts/678d0feff1fa.gif)

Lakehouse//RT achieves this by taking a different approach in four areas:

1. High concurrency support, so more queries share the same resources
2. Faster execution, so each query uses compute for less time
3. Autoscaling in small increments, so capacity follows demand closely instead of jumping in full-cluster steps
4. One system instead of several, so you stop paying for duplicate infrastructure and the work of keeping the system in sync

Organizations will not be able to outspend the demand curve. The only sustainable path is a system that does more per unit of compute.

### 1. Higher concurrency serves more queries per warehouse

Concurrency is where real-time costs usually grow fastest. Traditional warehouses can only run so many queries at once; the rest wait in line or trigger more capacity. Serving hundreds of agents then means running several clusters just to keep response times steady. That's true even when most of those queries are small lookups that don't need the horsepower.

Lakehouse//RT is designed to run far more queries side by side on each warehouse. In ourlaunch blogwe shared that we can deliver sub-100 millisecond latency at 12,000 queries per second, and we’re only getting better from here.

Each query also finishes quickly, so capacity frees up sooner for the next one. The same peak fits on far less compute, and the agents still get answers in milliseconds.

Customers are experiencing this on real-world workloads. Aurasell moved from several clusters at 200 queries per second to one small Lakehouse//RT warehouse sustaining more than 250 QPS, executing queries 4-5x faster while reducing costs by 10x.

Keep reading for more customer success stories!

### 2. Faster queries use less compute

Say you hire a contractor. One charges $20 an hour and takes 10 hours. Another charges $22 an hour and finishes in five. The first costs $200 and the second costs $110. You pay for the finished job, not the hour.

Compute works the same way: your bill is rate times runtime. Lakehouse//RT is built to finish real-time queries fast, including the steps around execution like planning, routing, and returning results. Each query holds compute for less time. Across millions of agent queries a day, that adds up.

### 3. When you need more capacity, you add only what you need

Every warehouse eventually needs more capacity as traffic grows. What matters is the size of each step.

Traditional warehouses typically scale by spinning up whole copies of themselves. On a Large warehouse, that's another Large warehouse spinning up. While cluster-level scaling works well for steady analytics workloads, real-time demand is spikier. When a burst needs only a fraction of a cluster, adding a whole cluster means paying for capacity you don't use until the burst passes.

Lakehouse//RT can flexibly add capacity, even one node at a time, whatever t-shirt size you select. Real-time demand rarely arrives in cluster-sized blocks. A spike in agent traffic might need 10% more capacity, not 100%, and Lakehouse//RT can add a step that size instead of doubling.

Scaling in small steps without hurting latency is easier said than done. It's what Lakehouse//RT was designed for, and it lets capacity grow in step with demand instead of ahead of it.

![Animation showing growth by clusters vs. growth by executors, with growth by executors resulting in less excess compute and therefore cost](/images/posts/93a4884ca332.gif)

### 4. One system removes duplicate infrastructure

Real-time used to mean bolting a separate serving layer onto your warehouse, such as Apache Druid, Apache Pinot, or a cache. That meant always-on infrastructure, a second copy of your data, sync pipelines, and engineers to keep it all consistent.

Lakehouse//RT queries governed lakehouse data directly, so as volume grows there's no second stack growing alongside it.

### What customers are seeing

#### Aurasell: 10x better cost efficiency, up to 5x faster queries

Aurasell's AI-native go-to-market platform runs agents that prospect, manage pipeline, and coach reps around the clock. Those agentic workflows depend on high query throughput, and Aurasell wanted real-time performance without moving or indexing data into an external system. With Lakehouse//RT, the team serves that workload directly in Databricks from a single small cluster.

#### VisionHeight: 90%+ cost reduction, production in three days

VisionHeight is a pre-attack intelligence platform that maps adversary infrastructure across the public internet in real time. Their previous real-time layer ran on Apache Pinot with always-on EC2 clusters running 24/7. After switching to Lakehouse//RT's serverless model, VisionHeight saw a cost reduction of more than 90%. On their heaviest query, Lakehouse//RT delivered sub-second response times, nearly 3x faster than Pinot. The entire migration took three days.

Read thefull case study here.

#### nOps: 6x lower infrastructure costs, 40TB of duplicated data eliminated

nOps manages more than $5 billion in annual cloud spend for hundreds of customers, powering real-time dashboards where enterprises track exactly where their money goes. Their real-time query layer previously ran on Apache Druid, requiring a separate always-on cluster and 40TB of duplicated data synced from their lakehouse. After migrating to Lakehouse//RT, nOps cut infrastructure costs by more than 6x while eliminating the duplicated data entirely. Because Lakehouse//RT queries data directly where it lives, the migration required no data copying, no new ingestion pipelines, and no new infrastructure.

[翻译失败，原文如下]

### The bottom line

The wave of AI and user demand isn't coming; it's here. Query volumes will grow by orders of magnitude. The question isn't whether you can afford real-time performance. It's whether you can afford not to have a system built for efficiency at scale.

Lakehouse//RT gives you:

- Performance that matches real-time analytics needswith sub-100ms latency and thousands of concurrent QPS on governed lakehouse data
- A bill that grows slower than your query volumebecause each query uses less compute and capacity is added in small steps
- No separate infrastructureto buy, sync, or maintain; customers are seeing 6x to 10x lower total infrastructure costs compared to using a separate serving layer for real-time

### Get started

Lakehouse//RTis available in beta today. Spin up a new Lakehouse//RT warehouse and start testing your most demanding real-time workloads.

- Enable Lakehouse//RT: Learnhow to start using Lakehouse//RT
- Review pricing: Through January 2027, try Lakehouse//RT at a30% discount.
- Talk to your account team: They can help you model the cost impact for your specific workloads.

Data WarehousingandLakehouse

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Lakehouse//RT: Scale real-time analytics, not your bill](https://www.databricks.com/blog/lakehousert-scale-real-time-analytics-not-your-bill)
> 
> 翻译时间：2026-11-16 08:50
