---
title: 'Multigres v0.1 Alpha: an operating system for Postgres'
title_original: 'Multigres v0.1 Alpha: an operating system for Postgres'
date: '2026-06-04'
source: Supabase Blog
source_url: https://supabase.com/blog/multigres-v0-1-alpha
author: ''
summary: '[翻译失败，原文如下]


  Today we''re releasingMultigres v0.1 alphato the open source community, the first
  public milestone of our mission to bring Vitess-grade ho...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:33.152468'
---

[翻译失败，原文如下]

Today we're releasingMultigres v0.1 alphato the open source community, the first public milestone of our mission to bring Vitess-grade horizontal scaling, high availability, and operational simplicity to Postgres. It's early, it's alpha, and we're excited to get it into your hands.

This is an open-source-only release. Multigres for Supabase is coming soon.

## What is Multigres?#

Multigres is a scalable operating system for Postgres: it holistically manages your Postgres instances and gives you sharding, connection pooling, automatic failover, and backup orchestration.

Postgres at scale is operationally complex: You need to manageread replicas, failovers, connection limits, backups, and more. Multigres handles these chores as a single cohesive system. And when the time comes to scale, Multigres will help you shard your database and scale it horizontally.

The v0.1 alpha introduces advanced connection pooling, automatic failovers, and a Kubernetes operator for deployment.

## The Multigres Operator#

The Kubernetes Multigres Operator allows you to deploy and manage Multigres clusters on Kubernetes. Toget started, you need a Kubernetes cluster along with a location for backups configured. The backups can be a shared file system or a cloud storage bucket like AWS S3. It is also possible to run Multigres on a local Kind cluster.

All the necessary images for running Multigres are publicly available.

## High Availability#

Multigres treats HA as a consensus problem, and is capable of resolving split-brain scenarios without losing commits that have succeeded. The protocol implemented by Multigres is based on generalized consensus, a model that gives you flexibilities that do not exist in traditional consensus-based systems:

- Built on top of Postgres replication: The protocol uses unmodified Postgres replication, and yet satisfies all the strict consistency requirements of a consensus-based system.
- User-defined durability policies: You can define arbitrarily complex durability policies. This flexibility allows you to specify the failures you are willing to tolerate without being constrained by restrictive rules like a majority quorum. For example, if you'd like your data to survive the failure of a single AZ, you can set your durability policy to be cross-zone, but still have standbys deployed in more than three zones.
- Add or remove replicas without affecting performance: You can safely scale replicas up and down while the cluster is running. Multigres will continue to honor the durability policy you've configured without affecting performance, while also maintaining correctness.

For more information on HA, you may read the following posts:

- High availability from first principles
- Handling edge cases using consensus

## Connection Pooling#

Multigres ships its own connection pooling solution using a two-service architecture. It consists of amultigatewaythat accepts client connections and routes queries, and amultipoolerthat manages backend connections. This architecture provides some distinct advantages over a single-process pooler.

- Traffic routing: The integration with the HA system allows multigateway to transparently route connections to the current primary. During a failover, multigateway can hold requests until a new primary is promoted, thereby minimizing errors. Additionally, you can balance read load across multiple replicas. In the future, multigateway will handle routing of traffic to different shards.
- Context-aware pooling: Multigres does not require you tochoose a pooling modelike transaction, session, etc. This is because it has a built-in parser and understands the effects of each request. This allows it to track connection state and reuse them wherever applicable. If a request requires a stateful connection, like a transaction, the connection gets pinned to that client until the stateful requirement is satisfied.
- Per-user pools: Multigres maintains a separateconnection pool per userwith no shared pool and noSET ROLEimpersonation. A fair-share algorithm splits a fixed connection budget across users, and pool routing is kept fast.
- Prepared statement consolidation: Multigres deduplicates prepared statements across gateways. Postgres parses, plans, and caches a given statement once, no matter how many gateways are forwarding it.

For more information on connection pooling, you may readTwo jobs, two processes: why Multigres has its own connection pooler.

## Backups#

Multigres uses pgBackRest for backups. Backups are taken from replicas to avoid overloading the primary.

- Three backup types: full backups copy the entire data directory at a checkpoint; incremental backups copy only files changed since the previous backup; differential backups copy changes since the last full backup. A typical schedule runs full backups periodically with more frequent incrementals or differentials in between.
- On-demand and scheduled: the CLI lets you list backups, trigger a manual backup, and initiate a restore. We'll soon add support for scheduled backups through the cluster spec.
- Bootstrap: During bootstrap, Multigres automatically identifies a primary, performs a backup, and uses it to initialize the other replicas. This workflow brings up a ready-to-run cluster without any manual intervention.

To learn more about how a cluster bootstraps, you may readHow a Multigres Cluster Bootstraps.

## What alpha means#

v0.1 is stable enough to experiment with and give feedback on. It is not yet ready for production workloads. Specific caveats:

- We haveknown issuesthat still need to be addressed.
- Sharding (the eventual flagship feature) is not in this release. v0.1 is a single-shard cluster with HA and pooling.
- Future releases are not guaranteed to be backward compatible.
- The CR API is not yet stable. Fields may change before v1.0.
- Performance benchmarks are in progress. We'll publish numbers in a follow-up post.

## Try Multigres#

1. Deploy your first cluster: a minimal CR that stands up a 3-node HA cluster.
2. Join the community: file issues and request features atgithub.com/multigres/multigres. Post your thoughts ingithub.com/multigres/multigres/discussionsto discuss features and get help.

---

> 本文由AI自动翻译，原文链接：[Multigres v0.1 Alpha: an operating system for Postgres](https://supabase.com/blog/multigres-v0-1-alpha)
> 
> 翻译时间：2026-10-21 06:58
