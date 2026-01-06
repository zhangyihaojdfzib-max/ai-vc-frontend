---
title: Databricks空间连接性能提升17倍，开箱即用
title_original: Databricks Spatial Joins Now 17x Faster Out-of-the-Box
date: '2025-12-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-spatial-joins-now-17x-faster-out-box
author: null
summary: Databricks宣布其内置空间SQL功能现提供高达17倍的空间连接性能提升，相比之前依赖外部库（如Apache Sedona）的方案。这一改进源于R树索引、Photon优化引擎和智能范围连接等技术的自动应用，用户无需更改代码即可在Databricks
  SQL无服务器或DBR 17.3+集群上体验。新功能支持90多个空间函数，能高效处理大规模地理空间数据，帮助零售、农业、物流等行业解答基于位置的关键业务问题。
categories:
- AI基础设施
tags:
- Databricks
- 空间计算
- 性能优化
- 地理空间分析
- SQL
draft: false
---

空间数据处理与分析对于Databricks上的地理空间工作负载至关重要。许多团队依赖外部库或Spark扩展（如Apache Sedona、Geopandas、Databricks Lab项目Mosaic）来处理这些工作负载。尽管客户已取得成功，但这些方法增加了运维开销，且通常需要调优才能达到可接受的性能。

今年早些时候，Databricks发布了空间SQL支持，现已包含90个空间函数，并支持将数据存储在GEOMETRY或GEOGRAPHY列中。与任何替代方案相比，Databricks内置空间SQL是存储和处理矢量数据的最佳方法，因为它解决了使用附加库的所有主要挑战：高度稳定、性能卓越，并且借助Databricks SQL无服务器，无需管理传统集群、库兼容性和运行时版本。

最常见的空间处理任务之一是判断两个几何图形是否重叠、一个几何图形是否包含另一个，或它们彼此之间的距离。这类分析需要使用空间连接，其开箱即用的卓越性能对于加速空间洞察至关重要。

我们很高兴地宣布，与安装了Apache Sedona的经典集群相比，每位使用内置空间SQL进行空间连接的客户都将体验到高达17倍的性能提升。该性能改进适用于所有使用Databricks SQL无服务器以及Databricks Runtime（DBR）17.3经典集群的客户。如果您已在使用的Databricks内置空间谓词（如ST_Intersects或ST_Contains），则无需更改代码。

运行空间连接面临独特的挑战，其性能受多种因素影响。地理空间数据集通常高度偏斜（如密集的城市区域与稀疏的农村地区），且几何复杂度差异巨大（如错综复杂的挪威海岸线与科罗拉多州简洁的边界）。即使在高效的文件剪枝后，剩余的连接候选仍需要计算密集的几何操作。这正是Databricks的卓越之处。

空间连接的改进源于R树索引的使用、Photon中优化的空间连接以及智能范围连接优化，所有这些都自动应用。您只需使用空间函数编写标准SQL，引擎将处理复杂性。

空间连接类似于数据库连接，但它不是匹配ID，而是使用空间谓词基于位置匹配数据。空间谓词通过评估相对物理关系（如重叠、包含或邻近）来连接两个数据集。空间连接是空间聚合的强大工具，可帮助分析师从购物中心、农场到城市乃至整个地球，揭示不同地点的趋势、模式和基于位置的洞察。

空间连接可解答各行业的关键业务问题。例如：
- **零售**：哪些商店位于竞争对手的5英里范围内？
- **农业**：哪些农田位于易受洪水影响的河流100米范围内？
- **物流**：哪些配送路线穿过施工区域？
- **城市规划**：哪些建筑位于工业区？

对于数据，我们选择了Overture Maps Foundation的四个全球大规模数据集：地址、建筑、土地利用和道路。您可以使用下文描述的方法自行测试查询。

我们使用了Overture Maps数据集，这些数据集最初以GeoParquet格式下载。下方展示了为Sedona基准测试准备地址数据的示例。所有数据集均遵循相同模式。

```python
# 代码块保持原样
```

我们还将数据处理为Lakehouse表，将parquet WKB转换为原生GEOMETRY数据类型，用于Databricks基准测试。

上图使用同一组三个查询，针对每种计算资源进行测试。

**查询 #1 - ST_Contains(建筑, 地址)**
此查询评估包含4.5亿地址点的25亿建筑多边形（点面连接）。结果产生超过2亿匹配项。对于Sedona，我们将其反转为ST_Within(a.geom, b.geom)以支持默认的左构建侧优化。在Databricks上，使用ST_Contains或ST_Within没有实质性差异。

**查询 #2 - ST_Covers(土地利用, 建筑)**
此查询评估覆盖25亿建筑多边形的130万全球“工业”土地利用多边形。结果产生超过2500万匹配项。

**查询 #3 - ST_Intersects(道路, 土地利用)**
此查询评估与1000万全球“住宅”土地利用多边形相交的3亿条道路。结果产生超过1亿匹配项。对于Sedona，我们将其反转为ST_Intersects(l.geom, trans.geom)以支持默认的左构建侧优化。

Databricks持续根据客户需求添加新的空间表达式。以下是自公开预览以来新增的空间函数列表：ST_AsEWKB、ST_Dump、ST_ExteriorRing、ST_InteriorRingN、ST_NumInteriorRings。现已在DBR 18.0 Beta中提供：ST_Azimuth、ST_Boundary、ST_ClosestPoint、支持摄取EWKT（包括两个新表达式ST_GeogFromEWKT和ST_GeomFromEWKT），以及ST_IsValid、ST_MakeLine和ST_MakePolygon的性能和稳健性改进。

如果您希望分享对其他ST表达式或地理空间功能的请求，请填写此简短调查。

GEOMETRY和GEOGRAPHY数据类型对Apache Spark™的贡献已取得重大进展，并计划于2026年提交至Spark 4.2。

立即在Databricks SQL上运行您的下一个空间查询——体验空间连接的速度飞跃。要了解更多关于空间SQL函数的信息，请参阅SQL和Pyspark文档。有关Databricks SQL的更多信息，请查看网站、产品导览和Databricks免费版。如果您希望将现有数据仓库迁移到具有卓越用户体验和更低总成本的高性能无服务器数据仓库，那么Databricks SQL是您的解决方案——免费试用。

产品
2024年11月21日 / 3分钟阅读

---

> 本文由AI自动翻译，原文链接：[Databricks Spatial Joins Now 17x Faster Out-of-the-Box](https://www.databricks.com/blog/databricks-spatial-joins-now-17x-faster-out-box)
> 
> 翻译时间：2026-01-06 01:23
