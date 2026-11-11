---
title: 'Read, don''t copy: replacing file and API feeds with OpenSharing - Part 1
  (The Why)'
title_original: 'Read, don''t copy: replacing file and API feeds with OpenSharing
  - Part 1 (The Why)'
date: '2026-11-06'
source: Databricks Blog
source_url: https://www.databricks.com/blog/read-dont-copy-replacing-file-and-api-feeds-opensharing-part-1-why
author: ''
summary: '[翻译失败，原文如下]


  - Traditional customer feeds get expensive as you scale: Every SFTP drop or API
  pull means another pipeline to monitor, fragile increment...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-11T09:04:28.221349'
---

[翻译失败，原文如下]

- Traditional customer feeds get expensive as you scale: Every SFTP drop or API pull means another pipeline to monitor, fragile incremental loads, backfills that depend on your customer, and a duplicate copy of their data to store.
- Read the customer's table in place instead of copying it: With OpenSharing, you can follow changes on the tables your customers share through streaming or change data feed, without tracking what's been processed yourself.
- Sharing gets easier for your customers: Adding you as a recipient is just a grant on a table they already maintain, and audit logs record every time you access their shared data.

If you ingest data from your customers over SFTP or APIs, you have probably asked yourself at least one of these questions.

- Can I pull only what changed, instead of reprocessing whole files?
- Can I get new data as soon as my customer writes it, instead of waiting for the next file drop?
- Can I backfill months of data without asking my customer to re-export it?
- Can I show my customers exactly when their data is being accessed?

The answer is yes, but not with the patterns most teams still rely on.

Data engineering has come a long way, but customer ingestion has barely changed. Most teams still use SFTP file dumps, API pulls, or managed connectors. Each of these patterns works, but each also carries hidden costs that quietly add up as you take on more customers.

Ideally, you should be able to use a table's own version history to incrementally pull just the new data, and simply read the table your customer already maintains, with no SFTP to stand up and no per-customer connector to babysit. You would also get the freshest data, because as soon as your customer writes to the table, it becomes immediately available to you and every other recipient.

OpenSharing does exactly that. It is an open protocol for reading a table in place, built on open table formats such as Delta Lake and Iceberg. Because the protocol is open, you don't even need to be on Databricks to read what your customer shares.

## How we got here

None of this happened overnight. It began with file-based feeds, as they were a simple ingestion pattern: your customer simply drops a file via SFTP or into a bucket, and your job picks it up. Following that, APIs arrived when customers demanded something fresher than a nightly file. Instead, you could pull changes on your own schedule while the customer maintained an API endpoint. Then came managed connectors. This was the natural next step once custom-coding each feed connected to an API or SFTP stopped scaling, leading to new customer onboarding becoming configuration rather than code.

While each has its place, the real problem is what they quietly cost you once you start maintaining these pipelines.

## The hidden costs

Most hidden costs stem from managing every pipeline, since each customer has their own quirks that can introduce failures. SFTP file dumps need to handle cases where your customer uploads something other than the agreed-upon files into the SFTP server. On the other hand, APIs hide their own set of failures.

Let's use an endpoint that returns data as an example. Calling the endpoint often demands passing a time parameter, where, in turn, it returns data. It is this parameter that can cause pain, as failing to keep track of the last timestamp can cause your copy of the data to drift. For managed connectors, that connection can still fail, and you lose a ton of flexibility.

In backfill scenarios, you feel the most pain. Let's say you find a bug and need to reprocess months of data. If you aren’t currently storing the raw data you ingest, you end up needing to work with your clients. For files, you may need to ask a customer to re-export months of data. In the case of APIs, you end up having to re-poll them for data in chunks, likely hitting rate limits or other blockers.

In all of this, you are keeping track of the last data you processed for each customer. However, if your bookkeeping drifts, you end up either duplicating rows or missing a potential batch, and can potentially create a silent failure where you end up spending countless hours debugging.

The pain is felt not only by you, the consumer, but also by your own customers. Providing this data means building and babysitting an export, with its own schedule, format, and failure mode. The customer also loses all visibility into whether you've even accessed it, and has to trust, with no way to verify, that no one else has queried it. Lastly, both parties incur storage costs because they maintain a duplicate of this data.

## What OpenSharing changes

OpenSharing addresses several of these problems because you are no longer taking a copy of your customers' data. Instead, you read the customer's table directly in place through the open protocol.

Shared tables can also expose a change data feed. This means that whenever your pipeline runs, it can read the feed to know which records have been created, deleted, or even updated. So now the table you used to maintain to track what has already been processed becomes a checkpoint your pipeline manages for you.

In addition, if a customer shares the entire historical table with you, you can resolve backfill situations smoothly. In these cases, you can simply query the data you need to backfill. OpenSharing provides direct access to the table; you do not need to pay for storage to duplicate this data, and you access the freshest data whenever you query it.

Your customer gets the better end of this, too. Instead of building and babysitting an export just to feed you, they share a table they already keep, and adding a recipient is just a grant. On top of that, reading their tables does not slow down their systems, because you read straight from cloud storage with your own compute rather than querying their database. Lastly, with Databricks system tables, they can see when a recipient queries a shared table, replacing the trust they previously extended on faith with an audit trail they can actually read.

## Let's see this in action

We set out to tackle the problems that come with traditional customer ingestion. By utilizing OpenSharing, you can read a table in place, allowing you to pull only what changed, see new data the moment your customer writes it, turn backfills into a query instead of a favor you ask for, and give your customer an audit trail of every access.

See Part 2, for setting up OpenSharing with a customer end to end, from creating the share to reading changes incrementally in your own pipeline.

Insights

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Read, don't copy: replacing file and API feeds with OpenSharing - Part 1 (The Why)](https://www.databricks.com/blog/read-dont-copy-replacing-file-and-api-feeds-opensharing-part-1-why)
> 
> 翻译时间：2026-11-11 09:04
