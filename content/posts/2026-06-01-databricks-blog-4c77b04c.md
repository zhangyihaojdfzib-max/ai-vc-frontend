---
title: 液态聚类：打破数据布局八大误区
title_original: 'Debunking 8 data layout myths: why Liquid Clustering outperforms
  partitioning'
date: '2026-06-01'
source: Databricks Blog
source_url: https://www.databricks.com/blog/debunking-8-data-layout-myths-why-liquid-clustering-outperforms-partitioning
author: ''
summary: 本文深入探讨了Liquid Clustering（液态聚类）作为现代Lakehouse数据布局方案的优势，指出其性能优于传统Hive风格分区，并成功规避了分区带来的小文件、数据倾斜等问题。文章揭穿了8个常见误区，包括分区更快、低基数列过滤更优等，强调Liquid
  Clustering通过事务日志剪枝、自动低基数优化等机制实现更高效的查询与写入。客户案例显示，在PB级规模下，查询延迟、写入吞吐量和存储效率均有显著提升。
categories:
- 技术趋势
tags:
- Liquid Clustering
- 数据布局
- Lakehouse
- 分区优化
- 开放表格式
draft: false
translated_at: '2026-06-02T06:36:05.244701'
---

- Liquid Clustering（液态聚类）是开放表格式的数据布局方式，其性能优于分区，同时规避了分区的局限性
- 8个常见误区让团队固守分区，而这些误区如今已不再成立
- 使用Liquid Clustering的客户报告称，查询延迟、写入吞吐量、存储效率和数据新鲜度均有显著提升，在PB级规模下收益尤为突出

## 引言

数据布局是计算领域最古老的问题之一。

自Hadoop和Hive问世以来的15多年里，分区一直是物理组织数据以进行处理和分析的标准方式。然而，如今的Lakehouse服务于Agent（智能体）、实时管道以及变化速度远超人工重新分区能力的查询模式。

Liquid Clustering是现代标准，客户正在各种规模下运行它，包括数十个在生产环境中拥有PB级表的客户。在这篇博客中，我们将介绍Liquid Clustering为何在Lakehouse中胜出。同时，我们将**揭穿8个常见的数据布局误区**，分享**3个团队将分区表转换为Liquid Clustering的成功案例**，**预览即将推出的新功能**，并展示**如何开始使用**。

## Liquid Clustering为何在现代Lakehouse中胜出

Hive风格的分区强制用户在创建表时，就确定一种体现在文件结构中的物理数据组织方式。选择一个基数过高的列，你会得到数十亿个小文件。选错列，查询可能会变慢，而非变快。无论哪种情况，你都得重写整个表。出错很常见：根据我们的分析，Hive风格的分区在超过75%的情况下会导致过度分区和小文件问题。

Liquid将聚类键视为引擎用于指导最佳文件组织的输入。键可以随时更改，或通过**自动Liquid Clustering**智能选择。基数不再是约束条件，布局可以随时间演变，无需不必要的重写。

Liquid Clustering的优势均源于上述原则：更好的倾斜处理、**行级并发**、无小文件问题、**多维聚类**以及更低的写入放大。

![分区导致的小文件和数据倾斜；Liquid带来的良好文件大小和聚类](/images/posts/9e09c42918aa.png)

到2026年，布局**应该**成为表的一个实现细节，每个读取或写入的引擎都能从中受益。随着Agent（智能体）进入Lakehouse，生成和消费的数据比以往任何时候都多，这一点变得越来越重要。人类和Agent（智能体）需要宽容的接口，避免Hive风格分区的潜在副作用。

## 揭穿8个常见的数据布局误区

Liquid Clustering于2024年正式发布（Generally Available）。自那时起，我们与大规模运行它的客户不断迭代。在此期间，一些关于Liquid Clustering和分区的常见误区一直存在，今天我们想揭穿它们。

### 误区#1：分区更快，因为它可以剪枝目录而非文件

误区认为：使用分区时，Spark或其他引擎可以剪枝整个目录，而无需打开其中的任何文件。

现实：在Delta和Iceberg等现代开放表格式中，不存在目录剪枝。例如，Delta使用**事务日志**来跟踪每个数据文件及其每列统计信息，剪枝是针对这些统计信息进行的，而非目录结构。引擎从不列出目录来规划查询。它读取事务日志，根据统计信息评估过滤器，并跳过不匹配的文件。Liquid Clustering使用相同的机制。无论你的数据位于`date=x/hour=y/`目录还是聚类文件的扁平目录中，引擎都在文件粒度上进行剪枝。不存在目录级别的捷径可丢失。

### 误区#2：在低基数列上进行过滤时，分区效果更好

误区认为：对于不同值数量较少的列，分区能提供完美的数据分离和良好的文件大小。

现实：Liquid Clustering会自动检测何时应用低基数优化。例如，如果你按`(date, user_id)`聚类，且`date`基数较低，系统会力求每个文件只包含单个日期的行。基数较高的列（如`user_id`）随后会自动用于在每个日期的文件内进行更细粒度的排序，而无需依赖Z-Ordering等其他排序技术。

![低基数Liquid Clustering优化](/images/posts/f31ff37ed4cf.png)

我们在一个真实世界的数据仓库基准测试中对这种Liquid优化进行基准测试时，看到了以下改进：**聚类时间降低35%，查询速度提升22%**。

此外，Liquid Clustering在高基数列上进行聚类时，设计上优于分区，因为它始终尝试创建大小合适的文件。

### 误区#3：Liquid Clustering不支持仅元数据操作

误区认为：仅元数据操作是分区独有的特性。与分区边界对齐的DELETE仅更新表的元数据，而基于分区列的聚合可以在不扫描文件的情况下计算。Liquid Clustering无法做到同样的事情。

现实：Liquid Clustering也支持仅元数据操作，包括DELETE、COUNT、DISTINCT和GROUP BY查询。引擎使用与数据跳过相同的每文件最小/最大统计信息，来确定查询的答案是否仅从元数据即可计算。在我们的基准测试中，Liquid Clustered表上的仅元数据DELETE比完全重写DELETE**快约90%**。其他仅元数据聚合查询的速度提升高达**27倍**。

### 误区#4：Liquid Clustering在PB级规模下效果不佳

误区认为：在PB级表上运行OPTIMIZE可能需要数小时，维护成本太高。

现实：我们对OPTIMIZE进行了大量重大改进，现在有数十个客户在生产环境中拥有PB级的Liquid Clustered表。两年前，在某些情况下，OPTIMIZE的第一阶段（规划）在10 PB的Liquid表上可能需要长达12小时。此后，我们已将规划时间缩短至**23分钟**。OPTIMIZE的第二阶段（执行）在Medium DBSQL集群上**快了5倍**。

![OPTIMIZE规划与执行时间](/images/posts/aaa431f745f1.png)

### 误区#5：Liquid Clustering仅使部分读取器受益

误区认为：Liquid Clustering仅对Databricks读取器读取UC管理的Delta表有益。

现实：Liquid Clustering是一种写入端优化。它是引擎组织文件以实现高效数据跳过的方式。输出是带有最小/最大统计信息的标准Parquet文件，写入Delta/Iceberg等开放表格式。任何兼容的读取器（例如开源Apache Spark、DuckDB等）都可以使用这些统计信息来跳过文件。Liquid Clustering在外部/托管表以及Delta/Iceberg表上均可用，且无论读取器如何，其益处都适用。

### 误区#6：分区对于并发ETL是必要的

误区认为：并发ETL需要写入边界。没有分区，两个写入器更新同一个表可能会发生冲突，而Delta/Iceberg的并发控制会强制其中一个重试或失败。进行分区，给每个写入器分配表的一个切片，这样两个管道就永远不会触及相同的文件。

现实：在分区粒度上操作是旧并发模型的一种变通方法。与仅提供文件级并发的分区不同，Liquid提供**行级并发**。更新不同行的两个写入器不再冲突，即使这些行位于同一个文件中。这消除了团队进行分区的主要原因之一：维护写入边界以避免序列化。使用Liquid Clustering，ETL可以轻松地针对同一个表并发操作。

### 误区#7：Z-Ordering可以弥补分区的不足

传说认为：分区处理分区列的过滤条件，而 Z-Ordering 处理其余部分。通过运行 OPTIMIZE ZORDER BY，引擎会对数据进行排序，以便在与分区方案不匹配的过滤条件下实现最佳跳过效果。

现实：Z-Ordering 并不能替代分区。事实上，它自身也存在结构性问题。

- 首先是**聚类质量差**。Z-Order 无法在表内维持真正的排序。同一列的值可能分散在多个文件中，因此每个文件的最小/最大值范围更宽，查询时跳过的文件比使用 Liquid 时更少。
- 其次是**不必要的重写**。随着新数据不断写入，Z-Order 需要定期重新运行，而每次重新运行都会重写大量旧数据（可能已被聚类），以恢复聚类质量。在持续数据摄入的情况下，使用 Z-Order 保持数据良好聚类的成本会随着表的大小而增长。

Liquid 采用增量聚类，包括在写入时进行，因此布局始终保持最优，无需不必要的重写。

### 误区 #8：分区是实现选择性数据覆盖的必要条件

传说认为：只有通过动态分区覆盖才能实现选择性数据覆盖。

现实：Liquid 表原生支持选择性覆盖。Databricks 提供了 `REPLACE USING` 和 `REPLACE ON` 两种 SQL 语法，可在任何数据布局（Liquid 聚类表、分区表或普通未聚类表）上实现选择性数据覆盖。与需要 Spark 配置的动态分区覆盖不同，`REPLACE USING` 和 `REPLACE ON` 可在任何计算环境（经典集群、SQL 仓库和 Serverless）中使用。该操作是原子性的，并且可以匹配你选择的任何列。

## 成功案例：从分区迁移到 Liquid 聚类

### Arctic Wolf 3.8 PB 安全遥测表查询速度提升 7.7 倍

Arctic Wolf 运行着一个超过 3.8 PB 的安全遥测表，每天摄入超过 1 万亿个事件，威胁猎手依赖最新数据来检测活跃攻击。

在从分区迁移到 Unity Catalog 托管表（启用预测优化）的 Liquid 聚类后，Arctic Wolf 取得了以下成果：

- 90 天查询时间从 51 秒降至 6.6 秒
- 文件数量从 400 万降至 200 万
- 数据新鲜度从小时级提升至分钟级

### Bolt 关键 CDC 表的读写性能提升

Bolt 最近尝试了 Liquid 转换（目前处于私有预览阶段），该功能使用 `ALTER TABLE .. REPLACE PARTITIONED BY WITH CLUSTER BY` 将分区表原地转换为 Liquid 表。在将一个 TB 级的 CDC 表转换为 Liquid 聚类后，他们观察到了以下读写性能提升：

- 写入吞吐量（行/秒）提升了 138%
- 读取时间最多减少了 63%，在 9 个代表性查询中平均减少了 21%

### 内部 PB 级工作负载查询时间提升 5.9 倍

我们在内部运行着一个 1.1 PB 的表，每天被查询数千次，主要由工程师用于生产调查和可观测性仪表板。最初，该表按 `date` 和 `hour` 分区，假设时间范围扫描将占主导地位。然而，这个假设并不完整。虽然时间范围扫描很常见，但该表也经常按 `source` 和 `id` 进行查询，这迫使引擎扫描相关日期和小时分区中的每个文件，以找到少量行。

将 `source` 和 `id` 添加为分区并不可行，因为存在太多不同的值，这会产生数十亿个小文件。Liquid 聚类消除了这种权衡，允许同时对时间和其他标识符列进行聚类，同时保持良好的文件大小。

基准测试显示，在 16 个代表性生产查询中，性能得到了巨大提升：

表本身也变得更小了。总大小从 1.1 PB 降至 0.8 PB，减少了 27%，而底层数据没有变化。聚类更好的文件压缩效率更高，并且过度分区带来的小文件开销也消失了。

## Liquid 聚类的未来规划

### 优化 Liquid 到 Liquid 的连接：速度提升高达 51%，Shuffle 减少 87%

目前，即使数据已经按聚类列组织，连接 Liquid 表时仍可能需要完全的数据 Shuffle。协同聚类连接（目前处于私有预览阶段）会自动消除这种 Shuffle。在一个真实的数据仓库基准测试中，与未优化的相同查询相比，Liquid 到 Liquid 的连接运行速度**快了约 51%**（从 28 分钟降至 14 分钟），并且**Shuffle 的数据量减少了 87%**（从 1.2 TiB 降至 150 GiB）。

### 分区表的轻松 Liquid 转换

以前，将分区表转换为 Liquid 聚类需要完全重写表，并通过 `REPLACE TABLE` 或使用双写和计划停机进行切换，从而带来下游破坏性变更。我们正在引入一个新的命令（目前处于私有预览阶段），使这种转换更加容易，最大限度地减少停机时间和重写。

## Liquid 聚类入门

使用 Liquid 聚类创建表：

或者，如果你使用启用了预测优化的 UC 托管表，请使用自动 Liquid 聚类，根据你的工作负载和查询模式智能选择聚类键：

Liquid 聚类是现代 Lakehouse 的布局。在你的下一个表上试试吧，或者立即联系你的客户团队，尝试分区到 Liquid 转换和协同聚类连接的私有预览版！

别忘了在 DAIS 上找我们！

- 使用智能存储和 Liquid 聚类优化 Lakehouse 成本和性能

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章直接发送到你的收件箱。

---

> 本文由AI自动翻译，原文链接：[Debunking 8 data layout myths: why Liquid Clustering outperforms partitioning](https://www.databricks.com/blog/debunking-8-data-layout-myths-why-liquid-clustering-outperforms-partitioning)
> 
> 翻译时间：2026-06-02 06:36
