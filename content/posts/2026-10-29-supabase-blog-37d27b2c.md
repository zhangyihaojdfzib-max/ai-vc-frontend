---
title: 'Multigres private alpha: automatic failover for Supabase Postgres'
title_original: 'Multigres private alpha: automatic failover for Supabase Postgres'
date: '2026-10-29'
source: Supabase Blog
source_url: https://supabase.com/blog/multigres-private-alpha
author: ''
summary: '[翻译失败，原文如下]


  Multigres brings high availability to Supabase projects, and it''s now in private
  alpha. Organizations on a paid plan canrequest accessand...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:48:02.996953'
---

[翻译失败，原文如下]

Multigres brings high availability to Supabase projects, and it's now in private alpha. Organizations on a paid plan canrequest accessand create projects that run Postgres on three nodes across availability zones, with automatic failover and connection pooling included.

Today, every Supabase project writes to a single Postgres primary. This works well for most applications, and it will stay the default. The downside is what happens when the primary fails. If the underlying hardware has a fault or its availability zone has an outage, your database is unavailable until it is recovered.

Teams that can't accept that downtime usually build high availability themselves. They run replicas, add a failover manager, put a pooler in front, and write runbooks for the cases the tooling doesn't handle. The hardest part is making sure no committed writes are lost when a replica is promoted. With Multigres, Supabase takes care of all of this for you.

## What is Multigres?#

Multigres is an open source operating system for Postgres, built by the team behindVitess. Vitess was created at YouTube to scale MySQL. In 2025, weannounced Multigresto build the same kind of system for Postgres. We releasedMultigres v0.1as open source in June under the Apache 2.0 license, and this private alpha is the first time it runs on the Supabase platform. We first showed Multigres atSupabase Selecton October 2.

Multigres is not a fork of Postgres. Your data lives in standard Postgres, and Multigres manages the cluster around it: routing connections, pooling, replication, failover, and backups.

## What's included in the alpha#

When you create a project with Multigres enabled, you get:

- A three-node Postgres clusterspread across availability zones in one region, so losing a single zone doesn't take your database down.
- Automatic failover.If the primary fails, Multigres promotes a replica within seconds.
- Built-in connection pooling.There is no separate pooler to configure or run.
- One standard Postgres connection string.You don't need to change your application code to move to Multigres.
- Most of Supabase.Auth, the REST Data API, Storage, Edge Functions, and all client libraries work with Multigres projects.

## How failover works#

Most Postgres high availability tools treat failover as a monitoring problem. They detect that the primary is gone, pick a replica, and promote it. The difficult part is choosing a replica that is safe to promote. If the old primary acknowledged a commit that never reached the replica you promote, that write is lost, even though your application was already told it succeeded.

Multigres treats failover as a consensus problem instead. It uses a generalized consensus protocol built on top of Postgres synchronous replication. Your application only receives an acknowledgement for a write once it has been replicated to enough nodes to survive a failure. That guarantees every acknowledged write exists on at least one surviving node. When the primary fails, the remaining nodes agree on the full set of committed writes and make sure the replica being promoted has every one of them before it accepts new writes. This is how acknowledged commits survive a failover.

During a failover, the Multigres gateway can hold incoming requests until the new primary is ready, instead of returning connection errors to your application.

## Connection pooling without choosing a mode#

With PgBouncer, you pick a pooling mode up front. Transaction mode lets many clients share a small number of connections, but it restricts session-level features. Session mode supports those features, but each client holds a connection for as long as it is connected.

Multigres parses each request and tracks the session state it creates, so it decides how to handle every query on its own. You don't pick a mode. Each database user also gets its own pool, and a fair-share algorithm divides the connection budget across users so one busy role can't starve the others. Prepared statements are deduplicated, which means Postgres parses and caches a statement once instead of once per client. For full details on how this works, readPooling without choosing a modeon the Multigres blog.

## Getting started#

1. Request access.Fill out theearly access form. We are adding organizations to the alpha gradually, so the option won't appear in your Dashboard until your organization has been invited.
2. Create a project with high availability.OpenCreate a new projectin the Dashboard. Turn on theHigh availabilitytoggle.
3. Finish setup and connect.Set the database password, region, and compute size, then clickCreate new project. Connect to it the same way you connect to any other Supabase project.

Multigres is free during the alpha for up to two projects per organization. It isn't available on the Free plan, and pricing may change once it leaves alpha.

## Things to know during the private alpha#

- Not for production.Multigres projects aren't covered by the uptime SLA during the alpha.
- Chosen at project creation.You can't enable Multigres on an existing project, and there is currently no managed path back to a standard Postgres project.
- No Realtime.Multigres doesn't yet support logical replication, which Realtime depends on.
- No Point-in-Time Recovery.Standard daily backups are available.
- Single region.You can only create projects in East US (North Virginia). Cross-region read replicas aren't supported yet.
- Fixed size.Compute size, disk, and the number of replicas can't be changed after the project is created. If you need more read throughput or more client connections, contact us and our team can help.
- Multigres or OrioleDB.A project can use one or the other, not both.

---

> 本文由AI自动翻译，原文链接：[Multigres private alpha: automatic failover for Supabase Postgres](https://supabase.com/blog/multigres-private-alpha)
> 
> 翻译时间：2026-10-30 08:48
