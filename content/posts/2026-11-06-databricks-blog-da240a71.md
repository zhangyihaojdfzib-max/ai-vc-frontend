---
title: 'Read, don''t copy: replacing file feeds with OpenSharing - Part 2 (How to
  Implement)'
title_original: 'Read, don''t copy: replacing file feeds with OpenSharing - Part 2
  (How to Implement)'
date: '2026-11-06'
source: Databricks Blog
source_url: https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement
author: ''
summary: '[翻译失败，原文如下]


  - OpenSharing exposes a Delta table via an open protocol, so recipients can read
  it live rather than ingesting from scheduled file or API...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-11T09:04:29.105938'
---

[翻译失败，原文如下]

- OpenSharing exposes a Delta table via an open protocol, so recipients can read it live rather than ingesting from scheduled file or API exports.
- It removes the per-recipient export jobs, file tracking, and reconciliation that are required by file and API feeds.
- Recipients read the shared table as a checkpointed incremental stream, with row-level inserts, updates, and deletes received through Change Data Feed.

Many data-sharing architectures begin with a familiar pattern:

- A provider exports a file on a schedule.
- The file lands in a bucket or is transferred through an SFTP endpoint.
- The recipient detects the new file, loads it, deduplicates it, and tracks what has already been processed.
- Updates and deletes require additional conventions or reconciliation jobs.

Part 1 of this blog described why a shared table can be a better alternative to a recurring file or API feed. Now let's look at what the recipient actually does with that table.

This walkthrough focuses on Databricks-to-Databricks (D2D) sharing. The recipient has aUnity Catalogenabled Databricks workspace and accesses the shared table through a shared catalog. The provider shares the table with its history, enabling the recipient to use it as aStructured Streamingsource. We'll come back to Databricks-to-Open (D2O) sharing later in the post.

## How OpenSharing replaces the feed

A Delta table keeps anordered historyof every change made to it. OpenSharing exposes that table over an open protocol without copying it. The data stays in the provider's storage, and the recipient reads it live.

On the recipient side, you point aStructured Streamingreader at the shared table. Spark records how far it has read in a checkpoint, so each run picks up only the changes made since the last one. Tracking "what's new since I last looked" becomes the engine's job, running over governed data with lineage and access control intact.

## Set up the share (both sides)

Let’s take an example: a retailer maintains a live orders table and shares it with an external recipient running Databricks. Instead of receiving a nightly CSV, the recipient can query the shared orders table directly. If the recipient needs a local copy for analytics or downstream workloads, it can incrementally materialize the data into a Delta table. The setup happens once and is split between the provider and recipient.

### Provider

Create the source table with Change Data Feed on, then publish it in a share WITH HISTORY. History is what makes the table an incremental source. Without it, the recipient only gets a static snapshot. Enabling Change Data Feed (delta.enableChangeDataFeed) is optional for the main incremental read below. Turn it on only if you plan to use the upserts and deletes path later. If you're on Databricks Runtime 19 or above, you can skip the property and rely onautomatic Change Data Feed, which computes row-level changes at query time for tables with row tracking enabled and works with Databricks-to-Databricks OpenSharing.

Register the recipient by their sharing identifier, then grant the share:

Do note that CREATE SHARE and CREATE RECIPIENT require metastore-level privilege, not just workspace admin.

### Recipient

The share now shows up as a provider in your metastore. Mount it as a catalog, and you can read it like any other table.

## Reading the stream

With the share mounted as shared_in, reading is handled by Structured Streaming.

Trigger.AvailableNow processes all currently available, unprocessed data using one or more micro-batches and then terminates. This makes it a good fit for scheduled incremental jobs. Instead of a fixed schedule, you can also configure the job with atable update triggeron the shared table, so the job runs only when the provider commits new data. It is recommended to store the checkpoint in durable cloud storage such asUC Volumes.

Note: This example reads a shared table through Delta Sharing, so it uses ignoreChanges. If you stream directly from a regular Delta table, newer Databricks runtimes use skipChangeCommits for append-only processing.

To prove it's actually incremental, run the stream once against an initial set of rows. Run it again after you have new rows on the provider. The target table's commit history will show two streaming writes:

Version

Operation

Operation Metrics

STREAMING UPDATE

numRemovedFiles: 0, numOutputRows: 200, numOutputBytes: 2307, numAddedFiles: 1

numRemovedFiles: 0, numOutputRows: 1000, numOutputBytes: 4958, numAddedFiles: 1

CREATE TABLE

The second run wrote 200 rows, not 1200. The checkpoint tracked the last version read, so the run pulled only the new ones.

ignoreChanges is suitable for this incremental landing pattern, but it may re-emit rows and does not propagate deletes. If downstream consumers need inserts, updates, and deletes, read the shared table’s Change Data Feed instead:

## What changes operationally

When a new customer is added, the provider does not need to create a new SFTP endpoint or implement a new export job. The provider grants the recipient access to the share. The recipient uses the same general pattern while keeping its own target tables and downstream business logic separate. The operational difference is significant:

- The provider manages a single governed source table instead of a separate export.
- Access is managed through the share: D2D recipients use permissions on the shared Unity Catalog, while D2O recipients use the applicable OpenSharing credential flow.
- The recipient retrieves data from table history rather than keeping track via custom files or timestamps.
- Backfills can use historical table versions rather than requiring the provider to recreate the old files.
- Change Data Feed gives the recipient explicit insert, update, and delete events when that behavior is required.
- Both parties have a clearer boundary: the provider owns the shared data product, and the recipient owns its downstream processing.

## Recipients that aren't on Databricks (D2O)

Everything above works because the recipient runs Spark on Databricks, which is what unlocks checkpointed streaming and CDF. Other recipients (pandas, BI tools, Snowflake) connect through OpenSharing with a credentials file instead of a metastore sharing ID.

If they run OSS Spark, the read is the same spark.readStream code through the delta-sharing connector. Without Spark, there's no continuous stream, so they pull changes by version range:

## Start ingesting data with OpenSharing

A useful first project does not need to solve every sharing scenario. Start with one regular Delta table and one recipient.

Before implementing the stream, answer these questions:

- Is the recipient D2D or D2O?
- Does the recipient need a snapshot, incremental reads, or row-level CDC?
- Does the share include history?
- Is CDF enabled if updates and deletes must be propagated?
- Which Databricks Runtime or OpenSharing connector version will the recipient use?
- How will the recipient handle retries, duplicates, deletes, and schema changes?
- Who owns monitoring and support after the share is in production?

Once those answers are clear, validate the smallest possible end-to-end flow: create the share, read an initial snapshot, write a new row, update a row, delete a row, and confirm that the recipient sees the expected results.

That is the practical shift OpenSharing makes possible. Instead of building a new transport and ingestion workflow for every customer, you can establish a governed data-sharing contract and let each recipient consume the data through the path that fits its platform.

### References

- Read data shared using Databricks-to-Databricks OpenSharing
- Read OpenSharing shared tables using Apache Spark DataFrames
- What is OpenSharing?
- Create shares for OpenSharing
- Use change data feed on Databricks
- Delta Lake table streaming reads and writes

[翻译失败，原文如下]

New to OpenSharing? Start withWhat is OpenSharing?andCreate shares for OpenSharing, then stand up the minimal end-to-end flow above against one table and one recipient.

Tutorials

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Read, don't copy: replacing file feeds with OpenSharing - Part 2 (How to Implement)](https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement)
> 
> 翻译时间：2026-11-11 09:04
