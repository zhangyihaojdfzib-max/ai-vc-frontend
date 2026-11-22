---
title: PostgreSQL 19 is available on Lakebase
title_original: PostgreSQL 19 is available on Lakebase
date: '2026-11-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/postgresql-19-available-lakebase
author: ''
summary: '[翻译失败，原文如下]


  - PostgreSQL 19 is available on Lakebase the same day the community released it.
  To try it, create a new Lakebase project and select Post...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-22T09:09:56.318644'
---

[翻译失败，原文如下]

- PostgreSQL 19 is available on Lakebase the same day the community released it. To try it, create a new Lakebase project and select PostgreSQL 19.
- This PostgreSQL release focuses on operational control. REPACK reclaims space while reads and writes continue, query plan advice lets you stabilize plans that go wrong, and WAIT FOR LSN gives you read-your-writes on replicas. Logical replication also gets several upgrades.
- Several Lakebase engineers are PostgreSQL committers and contributors who worked on this release, from query plan advice to shared memory and release management.

![](/images/posts/84c9e3ad0686.gif)

PostgreSQL 19 reached GA today and it's already available on Lakebase.New major versions often take weeks to reach other managed PostgreSQL services. Instead, we wanted to give access to it to our customers the same day.

Several engineers on the Lakebase team are PostgreSQL committers and contributors, and they worked on this release directly, from query plan advice to shared memory, locale handling, and release management. To try it,create a new Lakebase projectand select PostgreSQL 19 as the version.

## What's new in PostgreSQL 19

PostgreSQL 19 is a practical release. There is no single headline feature that changes what PostgreSQL is. Instead, version 19 goes after operational problems that database teams know well: bloated tables, unstable query plans, replica lag, incomplete statistics, and maintenance work that is hard to run safely in production.

The common thread is control. PostgreSQL 19 gives you more ways to step in when the defaults are not enough, without giving up the project's bias toward reliability and predictable behavior.

The full list of changes is in thePostgreSQL 19 release notes.

### REPACK

PostgreSQL uses multiversion concurrency control, so anUPDATEcreates a new row version and aDELETEleaves a dead tuple behind. Routine vacuuming makes that space reusable, but it doesn't necessarily return space to the operating system or restore a useful physical row order. Over time, heavily updated tables can become bloated and poorly clustered.

The usual fixes have beenVACUUM FULL,CLUSTER, or external tools such aspg_repack. The built-in commands work, but they take anACCESS EXCLUSIVElock for the whole operation, blocking normal access to the table.

PostgreSQL 19 addsREPACK, which reclaims space while normal reads and writes continue during most of the operation. For example, a chat application can rebuild itsmessagestable while clustering rows by conversation and send time using an existing index:

REPACKreclaims space likeVACUUM FULL; withUSING INDEX, it also physically orders rows likeCLUSTER. WithCONCURRENTLY, PostgreSQL rebuilds the table while normal reads and writes continue, capturing ongoing changes through logical decoding. It then takes an ACCESS EXCLUSIVE lock to apply any remaining captured changes and swap the new table and index files into place. This phase is typically brief but can take longer on a busy table.

There are operational constraints. Concurrent repacking creates an additional replication slot for the duration of the operation, so it needs free capacity undermax_repack_replication_slotsand a table with either a non-deferrable primary key or a suitable index-based replica identity. It also needs temporary disk space for a copy of the table and all its indexes, potentially plus a sort file up to the size of the table. Tables with heavy update and delete traffic face an additional limit: the current upstream PostgreSQL 19 implementation fails if more than about 104 million tuples in the target table are updated or deleted whileREPACK (CONCURRENTLY)is running. This counts changes made during the repack, not rows already in the table.

Not every relation type is eligible. Long-running transactions can delay the final lock. Concurrent repacking is also not MVCC-safe: after it commits, transactions using snapshots taken before the repack began can see the table as empty. Physical clustering also degrades as later writes arrive.

REPACK CONCURRENTLYstill needs planning, but it brings into core a job that previously required more downtime or an extension.

### Query plan advice

The PostgreSQL cost-based optimizer uses table statistics and cost estimates to choose an execution plan. Most of the time, that works well.

Statistics describe individual tables well, but real datasets often contain relationships that are harder to capture. Imagine that enterprise customers make up 0.1% of customers but generate 30% of orders. Per-table statistics cannot capture that cross-table correlation.

With an index onorders.customer_id,the planner may estimate that each enterprise customer has only a few orders and choose a nested loop that repeatedly probes the index. If those customers actually account for 30% of orders, each lookup returns far more rows than expected, and a hash join may be more appropriate.

PostgreSQL 19 addspg_plan_adviceandpg_stash_advicefor these situations:

- pg_plan_advicedescribes planner decisions as advice, applies supplied advice, and reports whether it was followed.
- pg_stash_advicestores advice by query ID and applies it automatically when a matching query is planned

These components do not add cross-table statistics or replace the planner. Instead, they let you intervene when an inaccurate estimate produces a poor plan.

Consider a query that counts orders from enterprise customers:

Here,cis the alias for the filtered customers table. The following advice asks PostgreSQL to place those customers on the inner side of a hash join:

When PostgreSQL can apply the advice,EXPLAINreports feedback similar to:

matchedmeans the resulting plan complies with the advice. It does not mean the new plan is necessarily better; you still need to evaluate it against the actual workload.

Unlike inline optimizer hints, plan advice lives outside the application’s query text. You can inspect the current plan, test focused advice, and then stash it by query ID.

pg_stash_adviceis the component that applies stashed advice automatically. Create the extension in each database before using its stash-management functions:

Create a stash and associate the tested advice with the query ID reported byEXPLAIN (VERBOSE). Replace<query_id>with the identifier from your plan:

Configure the database to use the stash for new connections:

Replaceappdbwith the name of your database.

Treat plan advice as a stabilizer once you've diagnosed the problem. Data distributions change, cached prepared statements may keep using an older plan for a while, and the optimizer is still right more often than it is wrong.

When the planner unexpectedly switches a critical query to a worse plan, PostgreSQL 19 gives you a supported way to stabilize it.

### Parallel autovacuum and new statistics views

Autovacuum can now use parallel workers when vacuuming indexes, controlled byautovacuum_max_parallel_workers.  A new scoring system prioritizes eligible tables based on how urgently they need vacuuming or analysis.

New statistics views expose more of what the server is doing:

- pg_stat_lockreports statistics by lock type.
- pg_stat_recoveryshows recovery status.
- pg_stat_autovacuum_scoresshows how autovacuum prioritizes tables.

Query-level diagnostics improve as well.EXPLAIN (ANALYZE, IO)reports asynchronous I/O activity, andauto_explain.log_iocan include the same information in logged plans.

PostgreSQL 19 also reports bytes written for full-page images inpg_stat_wal,EXPLAIN (ANALYZE, WAL), and vacuum and analyze logs.

Together, these make performance investigations less dependent on inference. You can see why maintenance work was prioritized, where asynchronous I/O happened, and how many WAL bytes came from full-page images.

### Logical replication

[翻译失败，原文如下]

Logical replication has become core infrastructure for change data capture, migrations, real-time serving, and ETL pipelines. PostgreSQL 19 closes several long-standing gaps:

- Logical decoding can be activated without a restart whenwal_levelisreplica. Creating the first valid logical replication slot raiseseffective_wal_leveltological, showing the WAL level currently in effect.
- Sequence values can be synchronized from publishers to subscribers.
- Publications can include all sequences withFOR ALL SEQUENCES.
- CREATE PUBLICATION ... FOR ALL TABLES EXCEPT (...)publishes all tables except a named set.
- Subscriptions can reuse connection details from apostgres_fdwserver withCREATE SUBSCRIPTION ... SERVER.
- Theretain_dead_tuplessubscription option preserves enough information todetect update_deletedconflicts, where a replicated update targets a row deleted by another origin. Detection also requirestrack_commit_timestampon the subscriber, andpg_stat_subscription_statscounts these conflicts.

Sequence synchronization removes an awkward migration edge case, especially during major-version upgrades that use logical replication. Copying table rows without advancing their sequences can leave a promoted subscriber generating values that already exist, causing duplicate-key errors.

PostgreSQL copies the initial sequence values when the subscription is created withcopy_data = true, the default. Later sequence changes are not streamed continuously, so refresh them immediately before cutover:

This updates the sequences already known to the subscription to their current values on the publisher. If the publication has gained new sequences, useALTER SUBSCRIPTION ... REFRESHPUBLICATIONto add them and synchronize their values before cutover.

### WAIT FOR LSN

Asynchronous read replicas add read capacity without making primary commits wait for them. The tradeoff is replication lag. An application can commit a write on the primary, immediately read from a replica, and not find the row because the replica has not replayed the relevant WAL yet.

PostgreSQL 19 adds a direct way to coordinate that handoff. An LSN identifies a position in the PostgreSQL WAL, andWAIT FOR LSNblocks the standby until replay reaches at least the requested position:

By default,WAIT FOR LSNwaits indefinitely for the standby to replay the requested LSN. Other modes can wait for WAL to be written or flushed, and you can set a timeout.

The client or connection pooler still has to carry the LSN from the primary to the replica. The database now provides the missing synchronization step, so read-your-writes behavior no longer needs polling or arbitrary sleeps.

### ON CONFLICT DO SELECT

INSERT ... ON CONFLICT DO SELECTgives you a clean get-or-create pattern that returns both existing and newly inserted rows:

It replaces theDO UPDATE SET col = EXCLUDED.colworkaround, which performs an update even though no values change. That creates a new row version and leaves a dead tuple on every conflict.

### JSON output for COPY TO

COPY TOcan now emit JSON directly. By default, it writes one object per line, whileFORCE_ARRAYwraps the output in a single JSON array:

The new JSON format is export-only, soCOPY FROMdoes not accept it.

### Smaller SQL and performance changes

Lastly, a few compact changes with a quality-of-life payoff:

- JSON path expressions gain familiar string methods such asbtrim(),lower(),replace(), andsplit_part().
- Therandom(min, max)family now supportsdate,timestamp, andtimestamptz, which helps with tests and synthetic datasets.
- Five window functions acceptIGNORE NULLSandRESPECT NULLS.
- Whenio_method = worker, I/O workers scale automatically betweenio_min_workersandio_max_workers. Foreign-key checks are faster, and the planner and executor get another round of targeted optimizations.

## We also lost a few features

Several major features landed during PostgreSQL 19 development but were removed before release. Reviewers found correctness or design problems that were too risky to resolve late in the cycle, so the community held the features for a later release.

Some of the features that finally won't ship in 19:

- SQL/PGQproperty graph queries.CREATE PROPERTY GRAPHandGRAPH_TABLEbrought graph pattern matching over regular tables into SQL.Reverted on September 7, 2026.
- UPDATE and DELETE ... FOR PORTION OF.Temporal updates and deletes that split rows to preserve history outside the targeted time range.Reverted on September 15, 2026.
- ALTER TABLE ... MERGE PARTITIONSandSPLIT PARTITION. Built-in commands for combining or dividing partitions.Reverted on August 27, 2026.
- GROUP BY ALL. Shorthand for grouping by every non-aggregate expression in the select list..Reverted on July 17, 2026.
- Non-text output formats forpg_dumpall.Reverted on June 18, 2026.
- DDL extraction functions.pg_get_role_ddl(),pg_get_tablespace_ddl(), andpg_get_database_ddl()wereReverted on September 13, 2026.

## Thanks to the PostgreSQL contributors

PostgreSQL is made by its contributors: thank you to the hundreds of community contributors credited in therelease notes. Special thanks to the engineers on the Lakebase team who worked on this version of PostgreSQL:

- Robert Haaswrote pg_plan_advice and pg_stash_advice (the latter with Lukas Fittl)
- Heikki Linnakangasworked on a new mechanism for registering shared memory, a rework of how subsystems allocate it, multixact fixes, and the new default of 128 for max_locks_per_transaction
- Jeff Daviswrote the change that lets CREATE SUBSCRIPTION reuse a postgres_fdw server's connection details, and did a long run of locale and character-handling work
- Jonathan Katzworked on the PostgreSQL 19 press release and handled release shepherding
- Matthias van de Meentworked on multiple commits including the change to static index access method routines
- Alexander Lakhinfound and reported multiple bugs

## Upgrading to PostgreSQL 19

As with any new major version of PostgreSQL, we recommend a measured approach to adopting it. Before moving production workloads to 19.0, we suggest you:

- Test your own workloads, queries, and extensions on PostgreSQL 19 in a development or staging environment first
- Compare performance and behavior against your current version, since major releases can change query plans and defaults
- Check that the extensions you rely on are available on PostgreSQL 19 (see below).
- Keep production on your current version until you're comfortable with the results

PostgreSQL19 also changes several defaults and compatibility behaviors. Check these before you upgrade:

- JIT compilation is off by default
- TOAST compression defaults to LZ4 instead of pglz
- MD5 password authentication emits stronger deprecation warnings
- RADIUS authentication support is removed
- standard_conforming_strings is always on
- pg_upgrade rejects clusters with affected btree_gist indexes on inet or cidr
- Database, role, and tablespace names can no longer contain carriage returns or line feeds

### A note on extensions

We've covered most of the extensions supported in our PostgreSQL 18 release, but not all of them are available on PostgreSQL 19 yet. We're adding more as they become available from the extension providers. If your workload depends on a specific extension,confirm it's available on PostgreSQL 19 before you plan a migration.

The community typically ships its first minor release a few months after a major version, as real-world usage surfaces fixes and refinements. PostgreSQL 19.1 is anticipated in February, and many teams plan production upgrades around that release. That's a common and sensible pattern for any .0 release, and it's just as true here.

Whatever your timeline, we're here to help. If you'd like to talk through upgrade planning or testing, reach out to your account team or Databricks support.

## Try it

[翻译失败，原文如下]

PostgreSQL 19 is available on Lakebase today.Create a PostgreSQL 19 projectin your workspace to try it, orget started with Lakebaseif you're new to it.

Lakebase

---

> 本文由AI自动翻译，原文链接：[PostgreSQL 19 is available on Lakebase](https://www.databricks.com/blog/postgresql-19-available-lakebase)
> 
> 翻译时间：2026-11-22 09:09
