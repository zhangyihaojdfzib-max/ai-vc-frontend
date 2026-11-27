---
title: Rethinking read replicas for the lakebase architecture
title_original: Rethinking read replicas for the lakebase architecture
date: '2026-11-26'
source: Databricks Blog
source_url: https://www.databricks.com/blog/rethinking-read-replicas-lakebase-architecture
author: ''
summary: '[翻译失败，原文如下]


  - In a traditional Postgres deployment, every read replica is a full clone of the
  primary, with its own instance and storage. That makes ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-27T10:43:08.295945'
---

[翻译失败，原文如下]

- In a traditional Postgres deployment, every read replica is a full clone of the primary, with its own instance and storage. That makes replicas slow to create, expensive to keep, and hard to use for scaling reads.
- On the lakebase architecture, a read replica is just another compute on the storage the primary already uses. It's ready in seconds, adds no storage, autoscales with read load, and scales to zero when idle.
- That turns replicas into a tool you can use per workload: for launches, dashboards, background jobs, read-only access for AI agents, and agents that add read capacity for their own tasks.

![](/images/posts/6b4b108b4b10.gif)

The idea behind read replicas makes sense: when your app gets busy, you add a couple of read-only replicas, route the heavy reads to them, and let the primary focus on writes.

In practice, that rarely works well. In traditional managed Postgres, a replica is a physical clone of the primary: its own instance, its own storage volume, and its own copy of every page. That makes replicas impractical for scaling reads on the go. They take minutes to hours to create, each one adds a full copy of the data to your bill, and they keep running long after the traffic spike is gone. What was supposed to be a nimble way to scale reads turns into one more instance to manage.

![A monolith replica copies the whole machine, disk included. A lakebase replica adds compute only, on top of one shared copy of the data](/images/posts/b987e4121748.gif)

Like other DX problems with OLTP databases,this is an architecture problem that comes from running things as a monolith. In Lakebase Postgres, a read replica doesn't copy anything - it's one more compute attached to the storage the primary already uses. It's ready in seconds, adds no storage, and scales to zero when nobody is reading from it.

## The traditional replica

Replicas in Postgres are asked to do two jobs: standbys for high availability, and read replicas for scaling reads. This post is about the second one. (High availability replicas are also fascinating, and we'll cover how we approach HA in the lakebase architecture in a future post.)

### The case for read replicas

Picture a typical Postgres deployment on a managed service like Amazon RDS. Postgres runs on a single instance, with its data on a storage volume attached to that instance. Backups and snapshots go to S3. Every query the app sends, reads and writes, lands on that one machine.

Traffic keeps growing. Most of it is reads, and at some point the instance runs out of CPU and memory to serve them. On a monolithic service like RDS, you have two ways to scale: move to a bigger instance, or add a read replica and send some of the reads there.

### Deploying a replica is deploying a new instance

On RDS, adding a read replica pretty much means building a second machine:

1. RDS takes a snapshot of the primary instance
2. It provisions a new instance from that snapshot, with its own compute and its own storage volume, and the volume has to be filled with the snapshot's data
3. The primary keeps taking writes the whole time, so once the new instance is up, it uses Postgres streaming replication to catch up with every change made since the snapshot, and to keep up from then on
4. Only then can you start routing reads to it

The work scales with the database. A bigger database means a bigger snapshot and a bigger volume to fill. A busier one means more WAL to replay before the replica catches up. On a small database, that can take minutes. On a large one, it can take hours.

And "available" doesn't mean done. On RDS, the new replica's volume keeps loading data blocks from S3 in the background after the replica comes online,and AWS notes that performance might not be at its fullest until that finishes. The process isn't free for the primary either: creating the snapshot briefly pauses its I/O unless it runs Multi-AZ, and a long-running transaction on it slows the whole thing down.

### The problems you are left with

Put all of that together, and you get a set of problems that share one root cause: in a monolith, the replica is a physical clone of the machine.

1. Every replica duplicates the data:each replica you add copies the entire dataset, and you are billed for that storage. If the goal is read capacity, paying for a second copy of the data is pure overhead
2. Replicas take time to be ready:since creating one takes minutes to hours, you cannot create a replica in response to a traffic spike. You have to guess the spike in advance and provision for it
3. Replicas are always on:pausing and resuming a replica is a manual process, and a resumed replica has to catch up on all the WAL it missed while paused. So most teams don't bother: the replica runs 24/7, and you pay for its compute and storage 24/7
4. Replicas don't scale on their own:RDS, for example, does not autoscale read replicas. It won't add replicas when demand increases or remove them when it drops, and resizing a replica means resizing an instance

The result is the opposite of what replicas promised. Instead of an elastic way to scale reads, you get one more static, overprovisioned piece of infrastructure to maintain. So many teams do the rational thing: they oversize the primary for the peak and skip replicas altogether, or they keep one replica running full time, just in case.

## Rethinking read replicas in the lakebase

The principle behind read replicas is sound. It's the monolithic implementation that broke them in practice.

The lakebase architecture sets the stage for building replicas differently, making them much more usable:

- Replicas share the data:a replica is a compute attached to the same storage as the primary. Adding one copies nothing, so you pay for the compute it uses and nothing extra for storage
- Replicas are ready in seconds:there is no snapshot to take and no volume to fill, so creating a replica takes a few seconds however large the database is
- Replicas scale to zero:when nobody is reading from a replica, it suspends on its own and starts again on the next query, up to date with the primary almost immediately
- Replicas autoscale:each replica grows and shrinks its compute with read load, within the limits you set, so you size it for the traffic you have, not for the peak

### It all starts with compute and storage being separate

Services like RDS run Postgres as a monolith: a single machine that owns both execution and durable state. Lakebase Postgressplits those responsibilities apart:

- The compute layer runs Postgres.It runs SQL, plans and executes queries, enforces MVCC, and generates WAL. It has RAM for shared buffers and local NVMe for the compute cache, and it owns no durable state
- The storage layer owns durability and history.Safekeepers receive the WAL from compute and replicate it with a Paxos-based protocol; a transaction is committed once a quorum acknowledges it. Pageservers turn that WAL into the pages Postgres reads, and they can reconstruct any page as of any LSN (GetPage@LSN). Object storage keeps the long-term, immutable history

## Breaking the monolith

The four problems of traditional replicas come down to two:

1. They are heavy to deploy and manage.A replica is a new machine with a full copy of the data, so it takes minutes to hours to build, and once it exists, nobody wants to pause, resize, or remove it
2. They are expensive.That machine runs around the clock whether anyone is reading from it or not, and each one adds a full copy of the data to your storage bill

Separating compute from storage fixes both. Since compute owns nothing durable, nothing stops more than one compute from attaching to the same storage. That is the whole trick behind replicas in the lakebase.

## Making replicas lightweight to deploy and manage

### A lakebase replica is just another compute

[翻译失败，原文如下]

Aread replica in Lakebase Postgresis an independent, read-only compute that reads from the same storage as the primary. Creating one looks like this:

1. The control plane starts a new compute on the branch, marked as read-only
2. The replica is initialized from a slim base backup served by the pageserver, exactly like a primary is
3. It connects to the safekeepers to stream the WAL
4. It connects to the same pageservers as the primary to read pages

That is it. Nothing in that list depends on the size of the database, which is why creating a replica takes seconds on a small database and on a large one alike. It also adds no replication work to the primary: the primary keeps streaming WAL to the safekeepers as usual, and the replica reads from the safekeepers, not from the primary.

![In Lakebase Postgres, a read replica is a second Postgres compute on the same storage as the primary. It has its own shared buffers and cache, and no copy of the data](/images/posts/630f2582d013.gif)

### Lakebase replicas don't duplicate storage

In a traditional setup, N replicas means N + 1 copies of the database: one on the primary's volume and one on each replica's volume, each provisioned, filled, and billed separately. In Lakebase Postgres, N replicas still means one copy. The data lives once in the storage layer, and every compute on the branch, the primary and all of its replicas, reads from it.

A replica does keep a local cache, in shared buffers and on its local NVMe, but a cache is not a copy. It starts empty, fills from the pageserver with the pages the replica actually uses, and holds nothing durable.

For deploying and running replicas, that means:

- There is no volume to size or fill.You don't pick, provision, or grow a disk for a replica, and there is nothing to load before it can serve reads
- The primary's WAL is processed once.The pageserver turns WAL into pages once for every compute on the branch. A replica only applies WAL to the pages it has cached, and reads everything else from the pageserver as of its own position in the WAL

### Lakebase replicas autoscale and scale to zero

Since a replica is just a compute, it gets everything a Lakebase compute gets, configured independently of the primary:

- Each replica has its own autoscaling range.The same algorithm that resizes the primarytracks the replica's CPU, memory, and working set, and resizes it in place as read load moves. Resizing never means provisioning a new instance
- Replicas scale to zero.By default, a replica suspends after 5 minutes of inactivity and starts automatically with the next query. There is no WAL backlog to replay on wake: storage kept ingesting WAL while the replica was suspended, so it reads current pages and is up to date with the primary almost immediately

![In Lakebase Postgres, the primary and the replica autoscale independently with traffic. The replica scales to zero when it's not needed, and both read from the same shared storage](/images/posts/b526f1c28aa9.gif)

## Making replicas cheaper

Being lighter to deploy is half of the story. The other half is that Lakebase replicas cost much less to run, for two reasons:

### You pay for compute only while it's working

A traditional replica is an instance, and an instance bills by the hour, whether it serves one query or a million. You size it for the peak, and you pay for the peak around the clock.

A Lakebase replica bills for the compute it actually uses:

- Scale to zeromeans a replica that nobody is reading from costs no compute. A replica for a nightly export that runs for 30 minutes is billed for those 30 minutes (plus the few minutes before it suspends), not for 24 hours
- Autoscalingmeans a replica that is active runs at the size the load needs right now. During the quiet hours it runs small, and it only grows during the spike

### You don't pay for a second copy of the data

On RDS, every replica comes with its own storage volume, sized for the full dataset and billed like the primary's. Three replicas on a 1 TB database means paying for 4 TB of storage.

In Lakebase Postgres, the same setup still means paying for 1 TB.Storage is billed for the data in the storage layer, and replicas add nothing to it. Replicas add compute, never storage.

Put together, the cost of a replica follows the reads it serves, not the size of the database or the number of hours in a day. That is what turns a replica from something you budget for in advance into something you can create for a single job and delete afterwards.

## Read replicas suddenly get useful: 7 use cases for lakebase replicas

When a replica is ready in seconds, adds no storage, and costs nothing while it's idle, patterns that never made sense with traditional replicas start to make sense. You can create one replica per workload instead of sharing one replica across everything. When you're done, you can delete it, or let it scale to zero.

Just a few examples on how Lakebase customers use them:

- Scaling application reads
- Absorbing a launch or a traffic spike
- Analytics, BI, and reporting
- Ad-hoc queries and production investigations
- Read-only access for agents, partners, and tools
- Isolating background jobs
- Agents scaling reads for their own jobs

### Splitting reads and writes

If your app is heavy on reads, or you want the primary to spend its resources on writes, you can send reads like feeds, product pages and search to one or more replicas. Writes, and any read that needs to see a write it just made, stay on the primary.

- Why it's better on the lakebase:a lakebase replica is just more compute on the same data - nothing gets copied or moved. Reads run on the replica's own compute, so they don't slow down the primary, and each side scales on its own: the replica with read traffic, the primary with writes.

### Absorbing temporary traffic spikes

Every time there’s a launch or you’re experiencing a traffic spike, you can immediately add a read replica and let it scale to zero as traffic settles.

- Why it's better on the lakebase:a replica takes seconds to create, independently on how large your primary compute is or how many TBs you have in storage. You or your agent can add replicas ad-hoc as you need them, and let them autoscale and scale to zero, without worrying about sizing them or pausing them manually.

### Offload analytics, BI, and reporting

You can also give dashboards, BI tools, and reports their own compute, so heavy scans don't compete with your app for CPU and cache.

- Why it's better on the lakebase:the replica wakes up when a tool connects and scales to zero when it's done, so you only pay while dashboards are in use. It also has its own memory, so a big scan can't push your app's hot data out of the primary's cache. And because a replica can't write, nobody running a report can change production data by accident.

### Production investigations

the primary, like how many orders are stuck in pending right now or which customers hit a checkout error in the last hour.

- Why it's better on the lakebase:you can spin up a replica just for the investigation and delete it when you're done. It reads the same live data as the primary, and nothing you run on it can slow the primary down.

### Read-only access for agents, partners, and tools

You can of course set up read-only roles in Postgres, but when an agent, a partner, an auditor, or a third-party tool needs to look at live data, it's often quicker to give them a read replica. They get current data, and there's no way for them to change it.

- Why it's better on the lakebase:a replica rejects every write, with the guarantee coming from the compute itself - also, their queries run on the replica’s compute, without affecting the primary.

### Isolating background jobs

[翻译失败，原文如下]

Plenty of background work mostly reads - nightly CSV exports, a search index rebuild, a newsletter going out to your whole list. When you run them on the primary, these jobs compete with your users for CPU and cache, and the app slows down whenever they kick in. If you point them at a replica instead, your users will never notice (and you’ll gain peace of mind).

- Why it's better on the lakebase: the replica wakes up when the job starts, scales up for the heavy part, and scales back to zero when the job finishes. Between runs it costs nothing in compute.

## The lakebase is the right architecture for replicas

The idea behind read replicas was always right. They keep heavy, non-critical read jobs from slowing down production, and they're a way to add compute capacity temporarily. But when Postgres ran as a monolith, that was hard to do in practice: every replica was an expensive physical clone with its own upkeep.

The lakebase architecture lets you use read replicas the way they were meant to be used. A read replica is just a compute attached to storage that already exists, so it's ready in seconds, adds no storage, and only costs compute while it's running. Read replicas in the lakebase are finally what they were supposed to be: a lightweight, short-lived way to scale reads without touching the primary.

Lakebase

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Rethinking read replicas for the lakebase architecture](https://www.databricks.com/blog/rethinking-read-replicas-lakebase-architecture)
> 
> 翻译时间：2026-11-27 10:43
