---
title: Dispelling LTAP myths
title_original: Dispelling LTAP myths
date: '2026-11-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/dispelling-ltap-myths
author: ''
summary: '[翻译失败，原文如下]


  - Lakebase''s LTAP design makes the lake the database''s storage, not a replica:
  one Delta or Iceberg table, one catalog, with Postgres cac...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:36.171195'
---

[翻译失败，原文如下]

- Lakebase's LTAP design makes the lake the database's storage, not a replica: one Delta or Iceberg table, one catalog, with Postgres caches and pageservers in front for speed.
- Point lookups read Postgres heap pages and scans read Parquet, and every analytical query sees a consistent snapshot, including commits not yet in the lake.
- Logical replication replays every change through a pipeline that must keep up, which makes it a costly way to build the lake copy.

Reynold Xin's post "From monolith to Lakebase to LTAP"explained what LTAP is and how the Lakebase architecture makes it possible: one governed copy of operational data, serving both Postgres and analytics, with no CDC pipeline and no second database.

![A traditional database keeps its WAL and data files on one machine. Lakebase moves them off a single machine and into separate, scalable storage](/images/posts/6e42eea94503.png)

Much of the commentary that followed read that claim through systems people already know. Four readings came up often:

- “LTAP is CDC under another name”
- “A single copy of the data can have only one physical layout, so either point lookups or scans must be slow”
- “Iceberg or Delta tables on object storage are inherently stale”
- “Postgres already provides the extraction path: logical replication”

Each of these myths rests on a wrong assumption about how Lakebase stores data. Let's take them one at a time.

## Myth 1: “LTAP is replication”

The reality:LTAP keeps one durable copy of each table, in the lake. The layers in front of it hold some of the same bytes to make that table durable and fast, but none of them is a second database.

From the outside, LTAP can look like a familiar pipeline. Postgres writes rows, a process tails the log, the changes land in an Iceberg table, and analytics reads Iceberg. That pipeline is CDC. It is also the structure of logical replication, mirroring, and most zero-ETL products. So it is easy to classify LTAP as the same design.

To see why it isn't, it helps to be precise about what counts as a second copy. There are two different ways a system can end up holding the same data in more than one place:

- Replication keeps two databases aligned by shipping changes from one to the other. Each side has its own catalog and its own timeline, and either side can be queried as a source of truth. If shipping stalls, the two copies drift apart, and nothing forces them back together.
- Tiering keeps one database and puts a stack of caches in front of it. The caches hold some of the same bytes so reads are fast. If a read misses the cache, it goes one layer down and costs some latency. It never creates a second catalog, and if a cache is lost, the table is not.

So the test is simple: can this layer be queried, or failed over to, as its own database? If yes, it is a replica. If no, it is a tier.

![Replication keeps two databases in sync. LTAP keeps one database, with the lake as the durable tier and caches in front of it](/images/posts/b5b989bd1820.png)

By that test, Postgres has always been tiered. The WAL, the buffer cache, and the indexes all store bytes that overlap with the heap. Nobody calls an index a replica of the table, because it has no catalog or timeline of its own.

LTAP keeps that same hierarchy. It moves it onto object storage and lets a lakehouse engine read the bottom, durable tier.

Here is what that hierarchy looks like in Lakebase, following a write and then a read:

- A write is durable when its WAL reaches a quorum of safekeepers. The pageserver then applies the log, keeps hot pages in memory and on local disk, and materializes data into object storage.
- A read starts at the compute node, which keeps a buffer cache and a local file cache. Indexes, TOAST, and visibility maps sit on the same hot path. A page that isn't cached there comes from the pageserver.

Object storage itself works the same way. When you PUT an object into S3, it is stored more than once, often across availability zones using erasure coding. The API still names one object, and no sync job runs between the copies. Lakebase stacks the same idea in front of the lake: log, caches, pageserver, object storage. The extra files are how one table is made durable and fast.

CDC does create a second database. It decodes a logical change stream into a foreign schema, usually keyed by primary key, and upserts into a table the source never reads back. That second table can be queried on its own, and it can fall out of step with the source: types can drift, DDL can go missing, a replication slot can drop rows, and tables nobody selected never appear. The result is two catalogs.

LTAP has no second table to keep in step. There is no list of tables to opt into. A table that exists in Postgres exists in the lake, and the pages the primary serves are caches of that store.

## Myth 2: “A single copy means slow lookups or slow scans”

The reality: two lossless encodings of the same rows can serve different access paths - heap pages for point lookups, Parquet for scans. Each query reads the layout that's fast for it.

Even if the extra files are a hierarchy, layout remains a separate question. Point lookups are efficient on rows, scans are efficient on columns. If there is only one encoding on disk, one of those access patterns pays in I/O. Calling the table a single logical copy does not change that.

That reasoning is correct, but it rests on one assumption - that one copy implies one encoding. It doesn't, as long as two formats can represent the same rows without loss.

So the question is whether LTAP's two formats are lossless:

- The primary format is Postgres heap pages, which are well suited to point lookups and updates.
- The second format is built for analytical access: Parquet behind Delta or Iceberg. Values are preserved, and the files carry enough physical metadata (heap block, offset, and MVCC versions) that the original pages can be rebuilt. Values that Parquet cannot represent losslessly are not coerced or dropped; they travel in an overflow field in the same table.

Because nothing is lost, the columnar copy can be the durable store in the lake, and the heap pages become a cache of it. Each access path then reads the format that suits it. Lookups hit 8 KB pages on the compute node, on local disk, and on the pageserver. Scans hit Parquet through an OLAP engine. Indexes remain in the hot tier; they are not transcoded into Parquet.Postgres already works this way. It keeps two physical structures over the same rows for different access paths: a heap and a covering index. Nobody treats the index as a CDC replica of customer.SELECT * FROM t WHERE id = 1andSELECT count(*) FROM tare two access paths over one table.

![Point lookups read heap pages and scans read Parquet. The pages can be rebuilt from the Parquet, so both hold the same row](/images/posts/6550bcdd9f1d.png)

A narrower observation is valid. The columnar files from Postgres are heap-ordered: rows sit in page-number order, because the page is the unit rewritten on each compaction. That layout is efficient for reconstructing a page and for rewriting only dirty pages. It is a poor clustering key forWHERE order_date >= …. If a warehouse query needs that clustering, it can be derived the waysilver tablesare already derived from any operational source. What is no longer required is a CDC pipeline whose purpose was to create the lake copy.

## Myth 3: “Open table formats mean eventual consistency”

The reality: every analytical query reads a consistent snapshot. Commits that haven't reached the lake yet are read from the pageservers, so nothing committed before the query is missed.

Iceberg and Delta provide snapshot isolation on object storage, and object storage has high latency. So it is natural to conclude that analytics is always behind, that many small tables cannot stay fresh, and that a join across tables cannot be consistent. That description fits CDC ingestion into a lake.

[翻译失败，原文如下]

It depends on one assumption: that a query can only see what has already landed in object storage. In LTAP, a query can also see pages that are not in object storage yet. That changes the answer, and it is easiest to see by following a query.

When an analytical query starts,

1. It asks Postgres for the current LSN. That is a metadata lookup.
2. It reads nearly all of the data from object storage: everything already materialized up to that LSN. An engine that does not share CPU with the OLTP node does this read.
3. It merges the rest from the pageserver. Pages that got committed after the last materialization come from the pageserver and are merged on top.

Postgres serves none of the bulk read traffic - it returns a number and, at most, those recent pages. The lake does not need to contain the latest commit for that commit to be visible. It needs to contain almost everything, plus a way to fetch pages that got committed after the last materialization. The LSN is the cutoff: it tells the engine how far the merge has to go.

The same LSN also keeps joins consistent. CDC applies table by table, so one relation can sit at a later slot position than another, and a join mixes two points in time. LTAP reads every table at a single LSN, the same kind of cutoff Postgres uses for REPEATABLE READ, rather than at whatever each pipeline last flushed. That LSN is a shared watermark. APIs for reading recent changes since a watermark are being developed both natively for Lakebase and as an extension for upstream Postgres.

![Parquet supplies the bulk of the table, and the pageservers fill in recent commits up to the LSN](/images/posts/6a9a88416608.png)

Small tables are a metadata cost, not a freshness limitation. Iceberg's overhead is files and snapshots. For a relation of a handful of rows, that bookkeeping costs more than it saves, and layout does not matter for scan performance. Those tables stay in the page cache, participate in the LSN-consistent read, and skip the Iceberg commit.

This leaves two claims that sound alike but aren't:

- "A long query doesn't see new commits" - true, and correct. A query that started at LSN X will not see commits after X. That is snapshot isolation, the same contract as REPEATABLE READ, not replica lag.
- "A query misses committed data" - this would be an incorrect result: a query that started at X and missed a commit that was already durable at X, because it was still sitting in a CDC buffer. Merging recent pages as of that LSN is how LTAP avoids this case.

The materialized columnar snapshot can lag behind the primary by the most recent compaction interval, but the query itself does not. The fact that Parquet files may be several minutes behind does not mean a reader is unable to see committed data.

## Myth 4: “Postgres replication is all we need”

The reality: logical replication is a costly way to keep the lake in sync with the database. It replays every change, row by row, and needs a pipeline that has to keep up. Decoding the WAL in parallel doesn't get around this, because log records can't be processed independently.

A standard way to get analytics on fresh Postgres is to enable logical replication. Debezium, PeerDB, pgoutput, and similar tools start from the observation that the database already emits a change stream, and ask what storage format is needed in addition.

The question is whether a change stream is a good way to build a table in the lake. Two properties of the stream say it isn't: how much it has to read, and how much state it has to carry.

Logical replication reads every change

The WAL is a physical log of page edits, written so Postgres can crash and recover. Logical decoding turns it into row events in commit order. That conversion cannot collapse many updates to the same page into the current image of the page; every change has to pass through. On a hot page, Postgres may log the same 8 KB a hundred times between checkpoints. Logical decoding emits a hundred events, then a downstream job upserts them into Parquet by primary key. In contrast, a page-tiering path reads the page once. In the write-intensive workloads we have measured, CDC reads at least the WAL volume, while dirty-page compaction may read a fraction of it.

Logical replication carries state

A replication slot is a cursor into WAL that the consumer must keep advancing. If the consumer falls behind, WAL remains on disk until the slot is dropped or the disk fills. Logical decoding does not emit DDL, so ALTER TABLE, type changes, and renames either make events inconsistent with the current catalog or invalidate the slot. Tables without a primary key need REPLICA IDENTITY FULL. Because the pipeline is expensive, it is typically applied to a subset of tables. That is the opposite of every Postgres table appearing in the lake because it exists.

A related claim: logical decoding can be skipped and the WAL decoded in parallel

Pageservers already consume WAL, so a parallel log-to-Parquet path can look like a small additional step. It is possible in principle. It has not been built as a production extractor, and it is not the path LTAP uses. WAL records are ordered because later ones assume earlier ones. Visibility lives in pg_xact, the proc array, and the catalog at that LSN, not in the tuple. Independent workers cannot each decode a disjoint byte range and emit correct current rows.

What LTAP parallelizes is pages, not log records. The system asks which pages changed since the last snapshot (WAL summaries on Postgres 17+, or the pageserver's log-structured merge trees), and each dirty page is independent work. That set is partitioned, the pages are transcoded, and one Iceberg snapshot is committed. The log is how writes were made durable, and one way to discover which pages changed. The snapshot is the current pages, not a replay of every record that dirtied them.

None of this makes replication the wrong tool for its intended jobs: migrations, major version upgrades, and cutovers to a second Postgres. But using logical replication as storage produces a second source of truth.

## Closing

All four myths come from the same misunderstanding: treating every materialization of the data as a second database.

LTAP keeps one logical table, and the lake is its durable copy. Heap pages, indexes, and caches are how Postgres serves that table at OLTP latency, much as a covering index serves queries over a heap. An OLAP engine scans the Parquet directly and merges in transactionally consistent changes since the last materialization.

None of these layers adds a second catalog or a second source of truth that can drift.

For a deep dive on how Lakebase's storage architecture leads to LTAP,see this post.

Lakebase

---

> 本文由AI自动翻译，原文链接：[Dispelling LTAP myths](https://www.databricks.com/blog/dispelling-ltap-myths)
> 
> 翻译时间：2026-11-13 09:19
