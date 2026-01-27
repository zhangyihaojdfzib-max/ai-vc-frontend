---
title: Databricks空间连接性能现提升17倍
title_original: Databricks Spatial Joins Now 17x Faster Out-of-the-Box
date: '2025-12-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-spatial-joins-now-17x-faster-out-box
author: ''
summary: 本文介绍了Databricks平台在空间连接（Spatial Joins）性能上的重大突破，实现了高达17倍的性能提升。这一优化是开箱即用的，无需用户进行额外配置，显著提升了地理空间数据分析的效率。作为统一的数据、分析和AI平台，Databricks通过持续的技术创新，为数据工程、数据科学和AI应用提供了更强大的基础设施支持，帮助用户更高效地处理大规模复杂数据，特别是涉及地理位置信息的分析任务。
categories:
- AI基础设施
tags:
- Databricks
- 性能优化
- 空间计算
- 数据平台
- 湖仓一体
draft: false
translated_at: '2026-01-06T18:15:23.226Z'
---

# Databricks空间连接现开箱即用提速17倍

## 原生空间SQL现无需调优或代码更改即可实现更快的空间连接

发布日期：2025年12月18日

作者：Kent Marten 和 Michael Johns

-   Databricks上的空间连接现开箱即用提速高达17倍基准测试使用客户启发的工作负载和Overture Maps数据GEOMETRY类型提供最佳性能

-   Databricks上的空间连接现开箱即用提速高达17倍
-   基准测试使用客户启发的工作负载和Overture Maps数据
-   GEOMETRY类型提供最佳性能

空间数据处理和分析对于Databricks上的地理空间工作负载至关重要。许多团队依赖外部库或Spark扩展（如Apache Sedona、Geopandas、Databricks Lab项目Mosaic）来处理这些工作负载。虽然客户取得了成功，但这些方法增加了运维开销，并且通常需要调优才能达到可接受的性能。

今年早些时候，Databricks发布了**空间SQL**支持，现已包含90个空间函数，并支持将数据存储在**GEOMETRY**或**GEOGRAPHY**列中。与任何替代方案相比，Databricks内置空间SQL是存储和处理矢量数据的最佳方法，因为它解决了使用附加库的所有主要挑战：高度稳定、性能卓越，并且借助Databricks SQL Serverless，无需管理经典集群、库兼容性和运行时版本。

最常见的空间处理任务之一是判断两个几何图形是否重叠、一个几何图形是否包含另一个，或者它们彼此有多接近。这种分析需要使用空间连接，而卓越的开箱即用性能对于加速获得空间洞察至关重要。

## 使用Databricks SQL Serverless，空间连接提速高达17倍

我们很高兴地宣布，与安装了Apache Sedona¹的经典集群相比，**每位使用内置空间SQL进行空间连接的客户，都将看到高达17倍的性能提升**。所有使用**Databricks SQL Serverless**和Databricks Runtime (DBR) 17.3的经典集群的客户均可获得此性能改进。如果您已经在使用Databricks内置的空间谓词，如`ST_Intersects`或`ST_Contains`，则无需更改代码。

运行空间连接面临独特的挑战，其性能受多种因素影响。地理空间数据集通常高度倾斜，例如密集的城市区域和稀疏的农村地区，并且几何复杂度差异很大，例如复杂的挪威海岸线与科罗拉多州简单的边界。即使在高效的文件剪枝之后，剩余的连接候选对象仍然需要计算密集型的几何操作。这正是Databricks的闪光点。

空间连接的改进源于使用R树索引、Photon中优化的空间连接以及智能的范围连接优化，所有这些都自动应用。您只需编写带有空间函数的标准SQL，引擎会处理复杂性。

## 空间连接的商业重要性

空间连接类似于数据库连接，但它不是匹配ID，而是使用**空间谓词**基于位置匹配数据。空间谓词评估相对物理关系（如重叠、包含或邻近度），以连接两个数据集。空间连接是空间聚合的强大工具，可帮助分析师从购物中心、农场到城市乃至整个地球的不同地点发现趋势、模式和基于位置的洞察。

空间连接为各行各业解答着至关重要的商业问题。例如：

- 沿海管理机构监控港口或航海边界内的船舶交通
- 现代农业公司通过结合天气、田地和种子数据进行作物产量分析与预测
- 公共安全机构和保险公司定位哪些房屋面临洪水或火灾风险
- 能源和公用事业运营团队基于对能源来源、住宅与商业用地以及现有资产的分析，制定服务和基础设施规划

## 空间连接基准测试准备

对于数据，我们选择了来自 Overture Maps 基金会的四个全球大规模数据集：地址、建筑物、土地利用和道路。您可以使用下文描述的方法自行测试这些查询。

我们使用了 Overture Maps 数据集，这些数据集最初以 GeoParquet 格式下载。下方展示了为 Sedona 基准测试准备地址数据的一个示例。所有数据集都遵循相同的模式。

我们还将数据处理成湖仓表，将 Parquet 格式的 WKB 转换为原生的 `GEOMETRY` 数据类型，用于 Databricks 基准测试。

上图使用了同一组三个查询，针对每种计算资源进行了测试。

**查询 #1 - `ST_Contains(buildings, addresses)`**

此查询评估包含 4.5 亿个地址点（点面连接）的 25 亿个建筑物多边形。结果是超过 2 亿个匹配项。对于 Sedona，我们将其反转为 `ST_Within(a.geom, b.geom)` 以支持默认的左构建端优化。在 Databricks 上，使用 `ST_Contains` 或 `ST_Within` 没有实质性差异。

**查询 #2 - `ST_Covers(landuse, buildings)`**

此查询评估覆盖 25 亿个建筑物多边形的 130 万个全球 `industrial`（工业）土地利用多边形。结果是超过 2500 万个匹配项。

**查询 #3 - `ST_Intersects(roads, landuse)`**

此查询评估与 1000 万个全球 `residential`（住宅）土地利用多边形相交的 3 亿条道路。结果是超过 1 亿个匹配项。对于 Sedona，我们将其反转为 `ST_Intersects(l.geom, trans.geom)` 以支持默认的左构建端优化。

## 空间 SQL 和原生类型的未来展望

Databricks 持续根据客户需求添加新的空间表达式。以下是自公开预览以来新增的空间函数列表：`ST_AsEWKB`、`ST_Dump`、`ST_ExteriorRing`、`ST_InteriorRingN`、`ST_NumInteriorRings`。现已在 DBR 18.0 Beta 中提供：`ST_Azimuth`、`ST_Boundary`、`ST_ClosestPoint`，支持摄取 EWKT，包括两个新表达式 `ST_GeogFromEWKT` 和 `ST_GeomFromEWKT`，以及对 `ST_IsValid`、`ST_MakeLine` 和 `ST_MakePolygon` 的性能和稳健性改进。

### 向产品团队提供反馈

如果您想分享对额外 ST 表达式或地理空间功能的请求，请填写此简短的调查问卷。

### 更新：在 Apache Spark™ 中开源地理类型

将 `GEOMETRY` 和 `GEOGRAPHY` 数据类型贡献给 Apache Spark™ 的工作已取得重大进展，并计划于 2026 年提交到 Spark 4.2。

## 免费试用空间 SQL

立即在 Databricks SQL 上运行您的下一个空间查询——看看您的空间连接能有多快。要了解更多关于空间 SQL 函数的信息，请参阅 SQL 和 Pyspark 文档。有关 Databricks SQL 的更多信息，请查看网站、产品导览和 Databricks 免费版。如果您想将现有数据仓库迁移到具有卓越用户体验和更低总成本的高性能、无服务器数据仓库，那么 Databricks SQL 就是解决方案——免费试用。

##

> 本文由AI自动翻译，原文链接：[Databricks Spatial Joins Now 17x Faster Out-of-the-Box](https://www.databricks.com/blog/databricks-spatial-joins-now-17x-faster-out-box)
> 
> 翻译时间：2026-01-06 18:00
