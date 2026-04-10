---
title: Databricks开放预览Iceberg v3，解锁湖仓一体新能力
title_original: 'The Next Era of the Open Lakehouse: Apache Iceberg™ v3 in Public
  Preview on Databricks'
date: '2026-04-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/next-era-open-lakehouse-apache-icebergtm-v3-public-preview-databricks
author: ''
summary: Databricks宣布对Apache Iceberg v3的支持进入公开预览阶段，标志着开放表格式的重要进展。Iceberg v3引入了行级血缘、删除向量和VARIANT类型等关键特性，能够显著提升增量数据处理的性能（如CDC场景快达10倍），并原生支持半结构化数据分析。这些创新进一步统一了Iceberg与Delta
  Lake的数据层，无需重写数据即可实现互操作。结合Unity Catalog，企业能够在多引擎、多目录的环境中，获得高性能与强治理的湖仓一体平台，为构建AI应用和数据分析管道奠定坚实基础。
categories:
- AI基础设施
tags:
- Apache Iceberg
- 湖仓一体
- Databricks
- 数据治理
- 增量处理
draft: false
translated_at: '2026-04-10T04:53:35.001900'
---

今天，Databricks 对 Iceberg v3 的支持进入公开预览阶段，在开放的湖仓一体平台上原生解锁 Iceberg 社区的最新创新。

Iceberg v3 标志着开放表格式向前迈出了重要一步，解锁了增量数据处理和半结构化数据分析等用例，而这些用例过去需要脆弱的变通方案才能实现。除此之外，Iceberg v3 代表了一项重大的技术创新，它进一步统一了 Iceberg 和 Delta Lake 的数据层，消除了在构建可互操作管道时重写数据的需求。

以下是 Iceberg v3 的新特性、其重要性以及为什么 Databricks 是运行湖仓一体平台的最佳选择。

## Iceberg v3 有哪些新特性？

Unity Catalog 管理的 Iceberg v3 表支持行级血缘、删除向量和 VARIANT 类型，从而解锁了新的用例并带来显著的性能优势。Databricks 还能在外部 Iceberg 表（在其他目录中注册的 Iceberg 表）上与这些特性进行互操作，使客户能够基于其数据构建 Agent（智能体）和 AI 应用，无论数据位于何处。

### 大规模增量处理：行级血缘与删除向量

大多数数据是以变更流（INSERT、UPDATE、MERGE、DELETE）的形式到达，而不是批量到达，这些数据通常来自运营数据库、事件流和第三方 API。历史上，处理这些变更需要解决两个难题：

1.  识别青铜数据集中哪些行发生了变更
2.  高效地将这些变更应用到白银/黄金数据集

团队通常采用全表扫描或外部 CDC 系统来检测变更，并通过昂贵的文件重写来应用变更。这导致管道速度慢、维护成本高，并且容易出现数据漂移和数据孤岛。

现在，**行级血缘**允许团队快速识别哪些行发生了变更。Iceberg v3 表中的每一行都携带一个永久的**行 ID** 和一个反映该行最后修改时间的序列号。

![](/images/posts/369065adcf5c.png)

此外，**删除向量**使得向数据集应用变更的性能比以往任何时候都更高。删除向量允许 Iceberg 跟踪哪些行已被逻辑删除，而无需立即重写底层数据文件。引擎不是通过重写大型 Parquet 文件来物理删除行，而是将轻量级的删除文件与数据一起写入。这使得数据操作性能比传统的写时复制方法**快达 10 倍**。

![](/images/posts/69b335952f24.png)

随着删除向量成为 Iceberg 的原生特性，Geodis 可以在 Databricks 上构建其 Iceberg 湖仓一体平台，而无需在性能或引擎选择上做出妥协。

行级血缘和删除向量共同使 CDC 成为表本身的固有属性。团队可以构建专注于增量处理**仅实际发生变更的数据**的管道，从而降低成本，并为下游的每一位分析师和数据科学家**更快地提供洞察**。

![](/images/posts/566ca957e975.png)

### 通过 VARIANT 类型将半结构化数据视为一等公民

日志、API 响应、点击流和 IoT 负载是非常有价值的半结构化数据源。随着它们的发展，AI 模型可以随之适应，直接从不断变化的现实世界信号中学习。

然而，历史上，数据团队在处理半结构化数据时面临着一个痛苦的权衡。一种标准方法是强制执行严格的模式，但这导致了脆弱的管道，每次上游数据演变时都会中断。另一种常见的变通方法是将数据存储为原始字符串转储，但这使得查询非常复杂和缓慢。这两种方法都不可扩展。

Iceberg v3 的 **VARIANT** 类型解决了这一权衡问题。VARIANT 是一种原生列类型，它将半结构化负载与关系型列一起存储在同一张 Iceberg 表中。这不需要任何扁平化处理、存储在单独系统中或用于规范化的 ETL 管道。相反，数据团队可以按原样摄取原始半结构化数据，并使用标准 SQL 进行查询。

![variant](/images/posts/cc96bedeacf6.png)

Panther 使用 VARIANT 类型来支持跨半结构化安全日志的大规模摄取和分析。

借助 VARIANT，您的 AI 模型和分析管道可以直接针对单个受治理表中的实时、不断演变的数据工作。当 API 响应中出现新字段或点击流中出现新事件类型时，无需模式迁移即可立即查询。借助**分片**等性能优化，客户可以在其半结构化数据上获得类似列式存储的性能，从而解锁低延迟的 BI、仪表板和告警管道。

## Unity Catalog 为多引擎、多目录的企业提供互操作性和性能

现代企业依赖多个引擎和目录来支持跨业务部门和遗留系统的多样化用例。Unity Catalog 旨在实现跨目录的互操作性和治理，同时根据查询模式优化数据布局。

### 跨目录和引擎的统一治理

Unity Catalog 的开放 API 允许客户一次写入，随处读取——不再有数据重复或孤立的访问控制。UC 可以联合到其他 Iceberg 目录，实现双向互操作性。Snowflake、AWS Glue、Salesforce 和其他主要目录中的所有 Iceberg 数据都可以被 Unity Catalog 读取，而 UC 中的所有数据也可以通过开放 API 被这些第三方平台访问。

![](/images/posts/05fcc2a94bd9.png)

除此之外，Unity Catalog 是第一个支持**在外部引擎上进行细粒度访问控制**的目录，使团队能够定义一次行过滤器和列掩码，并在数据被访问的任何地方强制执行。在 Unity Catalog 上集中治理，使得安全团队管理和监控其湖仓一体平台变得容易得多，同时也赋予数据团队自主权，可以将任何工具指向其湖仓一体平台。

![](/images/posts/2715348be4c3.png)

### Delta 与 Iceberg 的互操作性

采用 UniForm 的 Delta Lake 解锁了客户 Delta Lake 和 Iceberg 生态系统之间的互操作性：一次写入 Delta Lake，即可从 Snowflake、BigQuery、Redshift、Athena、Trino 或任何其他 Iceberg 引擎以 Iceberg 格式读取。随着 Iceberg v3 原生采用删除向量、行级血缘和 VARIANT 类型，客户不再需要在 Delta Lake 的性能特性和 Iceberg 兼容性之间做出权衡。其结果是，一份数据副本即可服务于技术栈中的每个引擎，无需维护复制管道，也没有数据漂移的风险。一家领先的金融服务提供商用 UniForm 取代了昂贵的全表复制服务，让 Snowflake 可以直接从 Unity Catalog 管理的表中读取数据。

### 自动化性能与优化

除了互操作性之外，Databricks 还将性能、布局优化和治理整合到一个系统中，因此团队无需自己将这些功能拼接在一起。Databricks 将智能维护（预测性优化）、基于查询模式的物理布局优化（自动液态聚类）和跨引擎治理（Unity Catalog）结合在一个层面，无需手动配置。

其他托管的 Iceberg 产品要求团队独立管理表维护、文件布局和访问策略执行。在 Databricks 上，这些功能是统一且自动化的，消除了整个类别的运营开销，同时保留了完整的数据可移植性。

## 在 Databricks 上开始使用 Apache Iceberg v3

Databricks 上的 **Iceberg v3** 今天进入公开预览！团队现在可以利用 Delta 和 Iceberg 的最佳特性，而无需在性能和互操作性之间进行权衡。

Iceberg v3 在启用了 Unity Catalog 的 Databricks Runtime 18.0+ 上可用。

创建一个启用 v3 的 Unity Catalog 管理的 Iceberg 表很简单：

```sql
CREATE TABLE my_catalog.my_schema.my_table (
  id BIGINT,
  data VARIANT
) USING ICEBERG
TBLPROPERTIES ('format-version' = '3');
```

创建一个启用 UniForm 和 v3 的 Unity Catalog 管理的 Delta 表同样简单：

```sql
CREATE TABLE my_catalog.my_schema.my_table (
  id BIGINT,
  data VARIANT
) USING DELTA
TBLPROPERTIES ('delta.enableIcebergCompatV3' = 'true');
```

## 展望未来：Iceberg v4

Iceberg v3 在高效、可互操作的基础上统一了 Delta 与 Iceberg 的数据层——下一个前沿是元数据层。Databricks 工程师正在 Apache 社区积极推动多项 Iceberg v4 核心提案，旨在使元数据更简单、更快速、更具可扩展性。其中包括**自适应元数据树**，它简化了元数据结构，使大多数操作只需写入单个文件而非多个文件。其他提案还包括支持跨环境无缝迁移表的**相对路径支持**，以及可扩展至 VARIANT 和 GEOMETRY 等新型数据类型的**现代化统计模型**。这些进步共同意味着更快的摄入速度、更高效的查询规划以及企业级规模下更简单的表管理。我们期待与社区共同推进 Iceberg 规范的发展。

## 在 Data and AI Summit 了解更多

立即开始使用 Iceberg v3，并加入我们于 2026 年 6 月 15 日至 18 日在旧金山举办的**Data and AI Summit**，深入了解我们的 Iceberg 路线图及跨生态系统工作。

---

> 本文由AI自动翻译，原文链接：[The Next Era of the Open Lakehouse: Apache Iceberg™ v3 in Public Preview on Databricks](https://www.databricks.com/blog/next-era-open-lakehouse-apache-icebergtm-v3-public-preview-databricks)
> 
> 翻译时间：2026-04-10 04:53
