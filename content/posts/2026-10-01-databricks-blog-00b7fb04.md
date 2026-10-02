---
title: Lakebase Postgres branch-based restores for fast recovery at scale
title_original: Lakebase Postgres branch-based restores for fast recovery at scale
date: '2026-10-01'
source: Databricks Blog
source_url: https://www.databricks.com/blog/lakebase-postgres-branch-based-restores-fast-recovery-scale
author: ''
summary: '[翻译失败，原文如下]


  - Traditional database recovery is painfully slow and scales poorly with size, often
  causing hours of downtime while provisioning new com...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:48.534580'
---

[翻译失败，原文如下]

- Traditional database recovery is painfully slow and scales poorly with size, often causing hours of downtime while provisioning new compute, downloading large snapshots and replaying log files.
- Lakebase Postgres introduces branch-based restores, a metadata operation that instantly recovers a database by pointing to immutable history in decoupled storage rather than copying data.
- Restoring a 100 TB database takes seconds, making recovery virtually instant and enabling AI agents to seamlessly handle branching and undo workflows.

In managed OLTP, restores have always been painfully slow and they get slower at scale. This often means that large production databases, where downtime costs the most, are left waiting the longest to recover.

The usual workarounds are difficult, expensive and risky. They involve extra replicas, extra environments and even a DBA on the restore which doesn’t fully guarantee you will be protected. Failover to a healthy replica helps when a machine dies, but it does not help when the bad write is already on the standby. That still means a restore, and a restore can mean hours of downtime.

This pain is caused by the architecture of traditional managed OLTP systems. Compute and storage ship as one machine, a restore starts with provisioning a new instance (you’re already waiting); snapshots live in object storage while Postgres runs on that volume, so the snapshot still has to be pulled onto disk (more waiting); WAL replay then has to close the gap from snapshot time to the exact recovery timestamp (even more waiting). As the database grows, this gets slower and more expensive.

The Lakebase Postgres architecture breaks the monolith and changes the restore mechanics. In Lakebase, compute and storage are decoupled, and database history is already kept in object storage in a way that’s instantly referenceable. In this architecture, a restore does not copy data into a new disk. Instead, it simply creates a branch at a timestamp which is a simple metadata operation, not a multi-hour copy-and-replay job.

In practical terms, time to restore drops to seconds, even if the database is 100 TB. And, it’s so simple that an agent can do it.

![image6.png](/images/posts/7c3866a8f5d8.png)

## The traditional OLTP restore path (and where it breaks)

Traditional Postgres point-in-time recovery (PITR) is built from two ingredients: a base backup of the files and archived WAL for everything after that backup. In a managed Postgres environment, such as Amazon RDS, that backup is usually a snapshot sitting in object storage.

“Restoring from backup” to a particular moment in time T is actually a process that involves three parts:

1. Deploy a new instance
2. Restore the latest usable snapshot before T
3. Replay WAL from that snapshot up to T

### 1. Deploy a new instance

This involves shipping compute and storage volumes (coupled) of at least the same as the primary. A small instance can come up in minutes, but a large instance with large EBS volumes usually takes longer causing you to wait before even starting the restore process.

### 2. Restore from the snapshot

RDS snapshots live in S3, so “restoring” means getting that snapshot out of object storage and onto Postgres’s disk.

That process is slow at large size, so RDS does not wait for it to be completed before making the restored instanceavailable. For large volumes, this happens while most table and index pages are still in S3. But available does not mean the working set is on the Postgres volume. If a query touches a block that is not local yet, the volume fetches it from S3 on the spot while the rest keeps hydrating in the background.

These types of queries come with a latency that’s fine for an internal checkup, but not for production. The restore is only done when the data you actually need lives on the volume, and that is not quick for a large database. The larger the database, the more time (in hours) this will take.

### 3. Replay WAL to T

The snapshot is only consistent as of snapshot time. To reach T, Postgres still has to replay the transaction logs archived after that snapshot. How long replay takes depends on how much happened between the snapshot and T. A snapshot from an hour ago will be much faster than a snapshot from last night. Plus if you had a heavy write day, that’ll be a lot of WAL to replay. Once again, this means a long wait (on top of the instance still hydrating from S3).

### Significant downtime windows

Unless the database is small, PITR is almost always a multi-hour operation. You have to provision the monolith, pull a snapshot out of S3, replay WAL and wait until enough of the volume is local to take traffic.

For that whole window, you may be suffering downtime. A healthy, high available (HA) replica can save you if the primary died and the replica still has good data. However, it may not save you from PITR so dropped tables and bad writes might already be on the standby.

## Slow database restores are painful

In a survey,50 developers running 1TB+ production Postgreswere asked about their experience with restores:

- 59% had a critical production failure in the past 12 months
- 30% were down for 3+ hours, some went past half a day
- only 21% recovered in under 60 minutes

This created potential adverse business impact:

- 40% reported significant business interruption
- 52% saw negative customer feedback from the incident
- 72% felt only “somewhat confident” they could recover quickly if a failure happened again

## Branch-based restores introduce a new path

![image4.png](/images/posts/78f08680be33.png)

In Lakebase Postgres, a modern architecture enables a different path for restores.

### Compute and storage are separate

Compute and durable storage are split apart and connected by the WAL. Compute runs Postgres meaning it runs SQL, plans queries, applies MVCC, manages locks, and generates WAL (all the regular Postgres tasks). What it doesnotdo is own the durable copy of your data.

Storage is what owns durability and history, and the job is divided in three parts executed by three distinct components:

- Safekeepersreceive WAL from compute. A transaction is durable once a quorum of safekeepers has acknowledged its WAL record
- Thepageserverturns WAL into the pages Postgres reads. It can reconstruct any page for a given key at a given LSN.
- Object storagekeeps the immutable, long-term history. Compute never reads it directly; the pageserver sits in between.

![image3.png](/images/posts/1c919425baf3.png)

When awrite comes in:

1. Postgres changes rows in memory and generates WAL
2. Compute streams that WAL to the safekeepers
3. A quorum acknowledges it, and the transaction is now durable
4. The pageserver later turns that WAL into page versions
5. Those versions land in object storage as immutable history

### History is stored as an addressable timeline

In this design, the write path takes an interesting shape. The architecture above separates committing a transaction from materializing pages, which in simpler terms means: old page versions are never overwritten. Your database's history piles up as a timeline you can point at, not a single copy you mutate.

### A restore in Lakebase is a branch at a point in time

In the traditional path, a restore mostly means rebuilding that past state into a separate instance. But with Lakebase, there’s an immutable storage history to reference, so that step is unnecessary and is replaced by a different primitive:a branch.

Where traditional restores provision a new instance and copy data into it, a restore in Lakebase isa branch at a point in history. This new branch has its own independent compute, its own connection string and it can be queried completely independently of production. It is not a replica of the original instance, but it feels just like it.

Here’s how to use this primitive for a restore:

[翻译失败，原文如下]

- When something fails in the main branch you pick a timestamp in the past (you can actually inspect that timestamp before committing to a restore, e.g. by running queries)
- Once you've validated it, the control plane maps that timestamp to the exact point in the storage's history (the right LSN), creates that branch and attaches compute
- The "restored database" is that new branch, which is available pretty much as soon as you press "deploy", independent of how much data is stored in the underlying database

Since this is the concept that matters, let's reiterate:

### The branch doesn't copy the database

This restore method completely eliminates data copies. The restored branch doesn’t need to copy data; it simply points at the image and delta layers that already exist up to that point in time.

- In a copy-and-replay system, a restore is a data-movement job. The database isn't “there” until the copy and the WAL replay are done
- In Lakebase, the “database” is already there. A restore is metadata: a pointer to a point in history. All that's left is to expose that point as a branch, with its own compute

### The result: restoring 100 TB is as fast as restoring 10 GB

The benefit is that scaling is not operationally scary anymore. If a restore is metadata work, how long it takes does not grow with the size of your data, and the mechanism stays the same.

![image1.png](/images/posts/8d5f90d3e7db.png)

Independent of how large your database is:

- Reaching an addressable past state is near-instant
- Validating that state takes only as long as the checks and the data you choose to read

A human or an agent can always reach a queryable past state right away after an incident, even on a huge Postgres database.

### Agents can build on restores

![image2.png](/images/posts/24416ab78596.png)

Restores in Lakebase are a simple operation: create a branch at a timestamp. The loop is short enough that agents can treat it as an ordinary tool call, not only to resolve incidents.

That is the piece agent platforms like Replit or v0 actually productize to build versioning or undo features. A typical loop looks like this:

1. The agent changes the app, which changes the database
2. The platform saves a checkpoint as asnapshotof main. It stores the checkpoint ID next to the code version
3. The user hits undo, or picks an older version in the UI
4. The platform looks up that checkpoint and restores it onto the live branch
5. Schema and data are instantly back to the database version that matches the “old code”

Traditional PITR is too slow and too heavy to support live workflows, but a branch at a timestamp is fast and cheap enough to be part of the product.

## Lakebase’s architecture changes what recovery looks like

Traditional restores get slower and heavier as the database grows. Branch-based restores do not. History already lives outside compute, so a past point is something you can open as a branch, not something you rebuild. Regardless if you have 10 GB or 100 TB, restores look the same. Pick a timestamp, create the branch and attach compute. Failures at scale are no longer as scary.

Experience it for yourself:create a Lakebase Postgres database, load a good chunk of data, run a restore and wonder how you’ve been living without this for so long.

---

> 本文由AI自动翻译，原文链接：[Lakebase Postgres branch-based restores for fast recovery at scale](https://www.databricks.com/blog/lakebase-postgres-branch-based-restores-fast-recovery-scale)
> 
> 翻译时间：2026-10-02 08:10
