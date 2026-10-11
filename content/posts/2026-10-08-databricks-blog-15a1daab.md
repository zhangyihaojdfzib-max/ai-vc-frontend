---
title: Load terabytes of data in minutes into Lakebase Postgres
title_original: Load terabytes of data in minutes into Lakebase Postgres
date: '2026-10-08'
source: Databricks Blog
source_url: https://www.databricks.com/blog/load-terabytes-data-minutes-lakebase-postgres
author: ''
summary: '[翻译失败，原文如下]


  - The LTAP (Lake Transactional/Analytical Processing) architecture offloads heavy
  bulk operations from the primary compute of Lakebase Po...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-11T08:06:34.522563'
---

[翻译失败，原文如下]

- The LTAP (Lake Transactional/Analytical Processing) architecture offloads heavy bulk operations from the primary compute of Lakebase Postgres to distributed engines like Spark.
- By allowing Spark to build valid Postgres pages and indexes in parallel and write directly to storage, Lakebase Postgres achieves data loads up to 147x faster without consuming live application resources.
- The primary node of Lakebase Postgres publishes the final manifest via a compact WAL record, ensuring that live OLTP queries remain unaffected and high performance is maintained.

Operational databases like Postgres are built to reliably execute highly concurrent, low-latency queries across subsets of data. What often impacts this reliability are bulk operations, like loading terabytes of data or running analytical queries that scan an entire table. These operations compete for the same resources as your application workloads, risking performance degradation or downtime.

Our goal is to make Lakebase Postgres the safest, most reliable place for your operational workloads. We achieve this by offloading heavy batch operations from the primary compute to distributed engines like Spark, which are purpose-built for these tasks. This is made possible by theLTAP(Lake Transactional/Analytical Processing) architecture, which allows both transactional and analytical engines to work on the exact same data in the lake.

Without this isolation, teams are frequently forced to be extremely careful with bulk operations. They sacrifice data freshness, run loads infrequently at off-hours, and manually manage complex backfills and checkpointing. Today, by leveraging the LTAP architecture, they offload ingestion pipelines entirely to Spark, ensuring apps get fresh data without compromising the performance of the live system.

### Show me the numbers

During our beta, a customer was using Synced Tables to load about 1 billion rows into Lakebase every day. By leveraging the LTAP architecture, we accelerated those loads drastically while keeping their operational workloads completely unaffected.

Previously, their bulk load took over 8 hours and completely saturated their CPU and memory. Even with Lakebase's autoscaling, they were forced to heavily overprovision their OLTP resources just to survive the sync. This happens because traditional Postgres architectures make the primary the sole gatekeeper of durable state. Bulk loads are forced through this single bottleneck, meaning every imported row generates heap pages, updates indexes, and writes WAL records on the exact same instance serving your live application traffic.

The LTAP architecture entirely relieved the pressure on their primary instance, protecting their live application traffic. You get the full power of a distributed engine, scaling load throughput almost linearly as your data grows. Our internal benchmarks show that loading 1 TB now takes less than 5 minutes.

Note: This benchmark measures data load time (building heap pages). We are actively working on parallelizing index builds for this loaded data as well.

In the rest of this post, we deep dive into the challenges of bulk-loading data into an OLTP database like Postgres, and explore how we leverage the LTAP architecture to solve them.

## The problem with bulk loads at scale into Postgres

The native PostgresCOPYcommand is efficient for standard, smaller ingests.

But as customers bring their operational and analytical estates closer together, the scale changes. An increasingly common workload involves serving massive, gold-tier Lakehouse tables to applications with operational query patterns. Pushing data at that extreme volume into a production database exposes two fundamental limits:

1. The load is inherently slow because every imported row must funnel through a single primary writer.
2. That same compute that is used for the load is also serving your application queries. Bulk loads demand heavy CPU, I/O, connections, and WAL bandwidth, competing with your OLTP traffic.

That remains true even if you start the load as a distributed Spark job. Spark can read source partitions in parallel, but each row still has to pass through one Postgres writer:

1. Workers send rows to Postgres throughCOPY
2. The primary turns those rows into heap and index pages
3. The primary records the changes in the Write-Ahead Log (WAL)
4. The WAL has to be flushed to durable storage before committing the load

Traditional bulk loads are bottlenecked by a single writer

The source side can scale horizontally, but the destination side cannot. Adding Spark executors speeds up the scan, but it does not remove the single-writer bottleneck. Additionally, this same Postgres primary is serving your online application transactions.A large import competes with them for CPU, memory, I/O, connections, and WAL bandwidth. Latency rises, teams schedule loads into quiet windows, and they often provision the primary for the largest import rather than for day-to-day traffic.

## What LTAP changes

TheLTAP architectureopens a path around this, because the primary is no longer the only way to create a durable Postgres state. Transactional compute is stateless in the lakebase: durable state lives in a distributed storage layer, not on the primary’s local disk. In a way,Postgres is a client of storage- it serves queries and transactions, but it does not have to be the process that materializes every new page.

For bulk load, that means Spark can build Postgres state and write it into storage, while the primary only publishes the result.

The operational consequences are:

- Bulk loads do not compete with OLTP on the primary. This runs outside the live compute endpoint. Application workloads keep the CPU, I/O, connections, and WAL bandwidth they need.
- Large loads into the same destination can run concurrently. Each import finishes by writing a single WAL record on the primary, so loads no longer queue behind one another’sCOPYstreams.
- The primary does not need to scale with load size. A 1 CU primary can keep serving traffic while Spark loads billions of rows on separate compute, and the Spark compute terminates as soon as the load finishes.

## Building valid Postgres pages, safely and in parallel

There are different optimizations for building Postgres files and constructing the primary-key index.

### Building the heap in parallel

The pages Spark produces must be valid for the destination database, just as if its primary had built them.

Each Spark executor launches a sandboxed Postgres instance in binary-upgrade mode, the same mechanismpg_upgradeuses to preserve catalog OIDs across major-version upgrades. We use it to transplant the destination’s catalog OIDs into each sandbox, ensuring that the OIDs embedded in the generated pages match those in the destination. The driver also assigns non-overlapping OID ranges to the sandboxes so that objects created concurrently cannot collide.

Inside each sandbox, a binaryCOPYwithFREEZEbuilds that executor’s slice of the heap. Freezing marks the imported tuples as already committed, so Postgres can treat them as visible without consulting transaction history from the sandbox.

Each worker then computes checksums for every generated page. Lakebase’s pageservers validate those checksums when they ingest the files, detecting corruption before the imported pages become authoritative.

Together, binary-upgrade mode, frozen tuples, coordinated OIDs, and checksum validation ensure that Spark produces pages the destination can read as ordinary Postgres pages. We implement this through Postgres extensions and a table access method, without modifying Postgres core.

The disposable sandboxes also allow performance optimizations such asUNLOGGEDhelper tables. These are optimizations, not safety mechanisms: they avoid unnecessary WAL and lock contention because no application traffic shares the sandbox.

### Building the index without scanning the heap

[翻译失败，原文如下]

A B-tree is one ordered structure over the entire keyspace, and its leaf entries contain key and tuple ID pairs that point back into the heap.

Normally, Postgres obtains those pairs by scanning the heap. Here, however, the heap is distributed across uploaded slices, and downloading all of it to an index-building worker would undo much of the benefit of building it in parallel.

The index builder does not actually need the heap contents. It needs the stream of(key, ctid)pairs that a heap scan would produce. Each heap worker from the previous step therefore exports its key columns and tuple IDs to a separate object-storage file while building its slice.

We feed those records into a helper table holding just the exported key columns and tuple ID rather than the original rows. DuringCREATE INDEX, a custom table access method scans the helper table identical toheapam, but writes thectidinto each index entry instead of the helper row’s own physical tuple ID. As records are loaded, each slice-localctidis shifted by the cumulative size of the preceding heap slices, making it point to the tuple’s final location in the concatenated heap. In short, Postgres’s standard B-tree builder can scan this helper table unchanged and produce an index over a heap it never downloaded. This replaces movement of the entire heap with movement of the much smaller key-and-tuple-ID representation.

### Handing the result to Postgres

Once the heap and index slices are in object storage, the Spark driver writes a manifest and invokes one SQL function on the destination. The primary records the import as a compact WAL record. A conventionalCOPYwould send the full data volume through the safekeeper quorum. We only send the import description.

The pageservers claim the uploaded files as authoritative pages and validate their checksums. They also prewarm the pages onto local SSD so initial reads do not incur cold object-storage fetches. Finally, the primary atomically swaps the staged data into the user-visible synced table.

Until that transaction commits, the imported table remains isolated. Afterward, the primary sees ordinary heap and B-tree pages produced through standard Postgres formats and interfaces.

## Get started today.

We use the LTAP architecture to power Synced Tables, enabling much faster syncs when serving gold datasets from your Lakehouse. If you are running manual ReverseETL jobs from the Lakehouse, with Lakebase, you should consider using Lakebase.

We’re excited to generalize this protocol to handle large operations and maintenance, like building indexes or even migrations. Lakebase with the LTAP architecture is the best place to run OLTP workloads.

If you haven’t tried Lakebase and Synced Tables already,get started today.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Load terabytes of data in minutes into Lakebase Postgres](https://www.databricks.com/blog/load-terabytes-data-minutes-lakebase-postgres)
> 
> 翻译时间：2026-10-11 08:06
