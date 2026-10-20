---
title: What makes a catalog open? Unity Catalog Advances the Open Lakehouse
title_original: What makes a catalog open? Unity Catalog Advances the Open Lakehouse
date: '2026-10-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse
author: ''
summary: '[翻译失败，原文如下]


  - Customer-owned storage: Unlike other platforms with native tables in managed storage,
  Unity Catalog managed tables in customer-owned st...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:34.241659'
---

[翻译失败，原文如下]

- Customer-owned storage: Unlike other platforms with native tables in managed storage, Unity Catalog managed tables in customer-owned storage allow portability without data copy.
- Unity Catalog is the most open catalog: As the first catalog to support the Apache Iceberg REST catalog spec for REGISTER and UNREGISTER, Unity Catalog allows you to move tables between catalogs without data duplication.
- Best features available on tables you own: Open catalogs like Unity Catalog deliver all advanced table features on tables in your storage, not only on tables a provider stores for you.

While almost every platform now supports open formats, what makes a catalog truly open? An open catalog keeps your data in storageyou own, gives you thebest featuresthere, and supportsdata portability: the ability tomoveyour tablesto another catalogwhile keeping thedata in place. Portability is a core tenet of an open lakehouse, and it’s where most catalogs fall short.

As the first catalog to support both REGISTER and UNREGISTER from the Apache Iceberg™ REST catalog spec,Unity Catalogin Databricks' Open Lakehouse expands what an open catalog means: your tables can move existing Iceberg tables in or out without any data movement. Databricks contributed UNREGISTER to the Iceberg REST catalog spec, making this an open standard. ReadUnlocking Data Portability.

This post walks through the three requirements of an open catalog, how Unity Catalog meets each one, and compares what happens to the same Iceberg table on different platforms.

### Beyond open formats: The three requirements of an open catalog

How open a lakehouse is comes down to the catalog. Many providers still use a proprietary format for the primary table type in their catalog, so formats are important to pay attention to. Beyond this however, anopen catalogmust also meet three requirements:

![image2.png](/images/posts/7e6237825015.png)

Teams move tables into provider-controlled storage to get

features the customer-owned option lacks. From then on, the provider's roadmap decides what you can do with your data.

Changing catalogs means exporting and rewriting every

table, to move it out of provider-controlled storage.

## [1] Customer-owned storage for Unity Catalog managed tables and every table type

Most data platforms support open table formats like Apache Iceberg. However, when those tables live in buckets that belong to the provider, your tables are no longer open. That makes the format open in name only: you can't see the files in your own cloud account, storage is billed through the provider, and leaving means copying every table out first.

Unity Catalog takes the opposite approach. In Databricks, "managed" describes who maintains a table, not who owns its storage. The catalog handles optimization, maintenance, and upgrades, while the files stay in a cloud storage account you own, not in the proprietary storage other platforms often call "managed storage." In Databricks, 99% of UC managed tables are in customer-owned storage. On platforms built around provider-controlled storage, it’s the opposite: nearly all of their tables live in storage that the provider controls and are locked in a proprietary format by default. The difference shows up the day you decide to leave a catalog.

## [2] The best features should work on the tables you own

Owning your storage only matters if the catalog treats those tables as first-class. Some platforms offer a customer-owned storage option, but reserve their best capabilities for tables in managed storage they control, creating an illusion of openness. The open path exists, but it comes with fewer features, so most tables would end up in provider managed storage anyway.

With Unity Catalog managed tables, the best features are supported for customer-owned storage (“bring your own storage”) path, whereas other platforms have limitations:

- Fail-safe data protection.Snowflakeand other platforms reserve fail-safe recovery for tables in their own storage. By contrast, Unity Catalog managed tables in customer-owned storage support data recovery: you can query earlier versions or restore dropped tables for up to 30 days.
- Automatic optimizations.InSnowflake, data compaction is costlier in provider-controlled storage. For other platforms, table maintenance and V-order apply to tables stored in customer-owned storage, rather than data reached through shortcuts. Databricks’Predictive OptimizationRuns on Unity Catalog managed tables in both Delta and Iceberg formats in customer-owned storage.
- Storage costs.Snowflakedoesn't delete orphaned files from Iceberg tables in your own bucket, such as files left behind by failed writes, which means you keep paying for files no table uses. On Unity Catalog managed tables on the other hand, Predictive Optimization removes unreferenced files from your bucket automatically, saving you money.

### [3] Open catalogs provides data portability: Unity Catalog does it without data copy

The most important test for whether a catalog is open is portability: whether you can leave the catalog easily at any time by moving tables between catalogs without having to copy out data.

Until recently, the ecosystem didn’t have a standard way to release a table from a catalog's management. Therefore, Databricks contributedUNREGISTERto the Apache Iceberg REST catalog specification which gives customers the freedom to leave without having to copy, move or rewrite any data files.

In Unity Catalog, REGISTER and UNREGISTER work as a pair:

- UNREGISTERremoves a table from Unity Catalog and returns the table's latest metadata location, the exact pointer the next catalog needs to take over commits.
- REGISTERattaches that metadata location to a new catalog, which writes a single record linking the table name to its metadata.

This is made possible because Unity Catalog managed tables reside in storage that you own. Unregistering isn’t possible with provider controlled storage since the exit API can’t hand you a pointer to files that you can't take with you.

Unity Catalog managed tables are fully portable and open with no lock-in: you retain control of your own data.

## Getting started

To get started in Databricks, reach out to your account team to get access to REGISTER and UNREGISTER (in Private Preview). With REGISTER and UNREGISTER, your Iceberg tables move to Unity Catalog with zero data copy into Databricks, stay fully open in your own storage, and gain all the benefits of Unity Catalog and Predictive Optimization:

To learn more, readUnlocking Data Portability. SeeUnity Catalog managed tables documentationfor more details on how to use Unity Catalog managed tables, which exist in customer-owned storage.

## What's next on the roadmap

In the future, we plan to support converting foreign tables or external tables to Databricks to managed tables using SET MANAGED IN PLACE. This would allow you to keep the same customer-defined storage path as before and does not require any data movement.

## Frequently asked questions (FAQ)

### Is Unity Catalog open?

Yes. Unity Catalog is open source and meets three requirements of an open catalog. Its managed tables, in Apache Iceberg or Delta Lake, live in a cloud storage account you own, get the full feature set there, and can move to another catalog without copying data through REGISTER and UNREGISTER. Most importantly, Unity Catalog managed tables are in customer-owned storage, so UNREGISTER in Databricks provides catalog portability without data movement on the Unity Catalog side. Read and write access to manage tables is also supported, using Unity Catalog and Iceberg REST Catalog Open APIs.

### Does using Apache Iceberg prevent vendor lock-in?

[翻译失败，原文如下]

Not on its own. An Iceberg table in provider-controlled storage can be as hard to move as a proprietary table, and an Iceberg table in your own storage may get fewer features. Avoiding lock-in also requires storage you own, full features on those tables, and a catalog that supports a clean, no-copy handoff.

### What's the difference between Unity Catalog managed tables and managed storage?

In Unity Catalog, "managed" describes who maintains a table, not who owns its storage. Unity Catalog managed tables are optimized and maintained by the catalog, and their files live in a cloud storage account you own. On some other platforms, "managed storage" means storage the provider owns and controls, not just optimizes.

### Can I move tables out of Unity Catalog without copying data?

Yes. With UNREGISTER, you can remove a table from Unity Catalog and register it in another Iceberg REST catalog, without copying data files.

In Unity Catalog, "managed" describes who maintains a table, not who owns its storage. Unity Catalog managed tables are optimized and maintained by the catalog, but their files live in a cloud storage account you own. On some other platforms, "managed storage" means storage the provider owns and often keeps in proprietary table formats.

### Can Databricks write to foreign Iceberg tables?

Foreign Iceberg tables are read-only in Databricks because another catalog owns their commits, which prevents two catalogs from writing to the same table. To have Unity Catalog manage the table in customer-owned storage, register it in Unity Catalog with REGISTER. You can also convert foreign tables to Unity Catalog managed tables in customer-owned storage using SET MANAGED.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[What makes a catalog open? Unity Catalog Advances the Open Lakehouse](https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse)
> 
> 翻译时间：2026-10-20 07:22
