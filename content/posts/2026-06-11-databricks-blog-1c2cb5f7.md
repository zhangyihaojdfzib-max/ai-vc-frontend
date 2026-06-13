---
title: Databricks Spatial SQL正式发布：地理空间分析进入湖仓一体时代
title_original: 'Geospatial Unbounded: Spatial SQL GA with AI/BI Maps, Delta Sharing,
  and Iceberg v3'
date: '2026-06-11'
source: Databricks Blog
source_url: https://www.databricks.com/blog/geospatial-unbounded-spatial-sql-ga-aibi-maps-delta-sharing-and-iceberg-v3
author: ''
summary: Databricks宣布Spatial SQL正式发布，将地理空间分析能力深度集成到开放湖仓一体平台中。新版本支持原生地理空间数据类型、90多个ST_*函数，性能大幅提升，布尔集合运算速度提升2倍。AI/BI仪表盘可直接渲染几何或地理类型地图，无需第三方工具。通过Delta
  Sharing和Iceberg v3实现地理数据开放共享与互操作，Unity Catalog统一治理。文章以飓风风险评估场景为例，展示了从保单查询、风险分析到地图可视化的全流程一体化能力。
categories:
- AI产品
tags:
- Spatial SQL
- 地理空间分析
- 湖仓一体
- Databricks
- 开放数据格式
draft: false
translated_at: '2026-06-13T06:20:57.614432'
---

- Spatial SQL 现已在 Databricks 上正式发布。原生地理空间数据类型、90 多个 ST_* 函数、AI/BI 仪表盘可使用几何或地理类型原生渲染地图。
- 自公开预览版以来性能大幅提升。布尔集合运算（ST_Intersection、ST_Difference、ST_Union）速度提升 2 倍，我们的 SpatialBench 结果显示性能提升 20% 至 15 倍。
- 地理空间加入开放湖仓一体。开放共享协议（Delta Sharing）、开放表格式（Iceberg v3、Delta）和开源引擎（Apache Spark 4.2）均支持地理列。

一场飓风正在佛罗里达湾形成。作为一家保险公司，您需要立即回答业务关键问题：识别预测风暴路径内的保单、面临风险的总保险价值、风险最高的县，以及需要通知哪些再保险合作伙伴。

不久之前，回答这些空间问题意味着要拼接多个系统：用于交叉分析的空间数据库、用于保单数据的数据仓库，以及用于将结果映射并分享给分析师和核保人的可视化工具。您甚至可能需要在外部系统中复制保单数据。每增加一个系统就多一分风险，每复制一次数据就使治理更加碎片化。

如今，空间工作可以在一个平台上完成。Spatial SQL 现已正式发布。Databricks 是一个地理空间湖仓一体。将空间数据库、数据仓库和地图工具拼接在一起的时代已经结束。将数据以 Geometry 类型存储在 Iceberg 或 Delta 中，大规模运行空间查询，调用 90 多个空间函数，通过 Delta Sharing 共享，并在 Genie 中探索，同时由 Unity Catalog 负责治理。

![使用 Genie 在 AI/BI 仪表盘中提问，现已支持使用自定义几何图形的地图。](/images/posts/3bdd4e799381.png)

Databricks 客户喜爱该平台提供的价值：

## Spatial SQL 提供世界级性能

在飓风逼近造成的时间紧迫中，每一秒都至关重要。这就是我们自公开预览版以来持续提升空间连接和 ST_* 函数开箱即用性能的原因。为了衡量最新的改进，我们使用 SpatialBench 运行了全面的基准测试。在 SpatialBench 中，12 个查询中有 8 个自公开预览版以来有所改进，提升幅度从 20% 到 15 倍不等。

![注意：图表仅展示了性能有所提升的 SpatialBench 查询。查询 Q2、Q4、Q10 和 Q12 没有变化。](/images/posts/4e8c5d568a2c.png)

对于布尔集合运算（ST_Intersection、ST_Difference、ST_Union），我们引入了改进的算法。这些函数可以帮助回答诸如“我的地块中哪些部分位于预测的飓风路径内？”以及“我们在这个区域所有手机信号塔的覆盖范围总和是多少？”等问题。与之前的版本相比，Databricks 现在使用这些运算符处理面数据集的速度平均提升了 2 倍。无需更改代码，您现有的查询速度就变得更快了。

这些空间运算为 Databricks 客户（如专注于高端快递和最后一英里配送服务的 Top Chrono）提升了效率。

## AI/BI 仪表盘现已支持使用 Geometry 和 Geography 的地图

对于空间问题，分享结果的最佳方式通常是地图。作为 Spatial SQL 正式版的一部分，AI/BI 现在可以使用 Geometry 或 Geography 列渲染地图。无需再使用自定义应用程序或第三方地图工具来可视化您的地理数据。

当核保人打开飓风风险仪表盘时，面临风险的保单、飓风路径和历史轨迹都可以成为可视化的一部分。您可以按县筛选，比较不同的预测路径，或根据需要对数据进行切片。

![在 AI/BI 仪表盘中通过多个筛选器对地图数据进行切片。](/images/posts/594b9ae577a7.gif)

而且核保人无需编写 SQL 即可实现。Genie Code 只需一个提示词就能生成正确的仪表盘。

Genie 处理地理空间列的方式与处理任何其他列相同。您可以输入“向我展示飓风预测中佛罗里达州的保单，总保险价值超过 100 万美元”，Genie 就会生成空间查询，遵守 Unity Catalog 行筛选器，并根据需要生成包含地图的仪表盘。

## 开放湖仓一体：用于地理数据的 Delta Sharing 和 Iceberg v3 互操作性

风险和风险敞口数据需要能够共享。再保险合作伙伴需要保单级别的分保文件。应急管理机构需要在内部和外部共享数据。每一次数据交换都可能是一个自定义的数据提取管道。

现在，随着 Spatial SQL 正式版发布，包含地理列的表已获得 Delta Sharing 支持。保险公司发布一个包含保单边界的单一 Delta Share，核保人的再保险合作伙伴直接从中读取，无需数据提取或模式转换。访问由 Unity Catalog 策略管理，并且血缘关系可追踪。

Databricks 在地理数据方面的开放性现已扩展到底层表格式。使用 Spatial SQL，您现在可以读写托管 Iceberg 表，并读取外部写入的 Iceberg 表。Databricks 上的 Iceberg v3 支持已正式发布，现已扩展以支持地理空间数据类型。开放湖仓一体意味着标准优先于孤岛。

## 今日正式发布内容

Databricks 上的 Spatial SQL 包括：

- GEOMETRY 数据类型——将您的矢量地理空间数据存储在原生的列类型中。Geometry 数据类型将提供最佳的空间查询性能。

注意：Geography 将保持公开预览状态，直到其在常用空间函数中得到全面支持。

- 90 多个 ST_* 函数——符合 OGC 标准的空间函数，支持常见格式（WKT、WKB、GeoJSON、EWKT、EWKB）的导入和导出、测量、构建、谓词、转换等。
- 高性能空间连接和运算——Databricks Spatial SQL 提供世界级性能，自公开预览版以来，大多数 SpatialBench 查询的性能提升了 20% 到 15 倍。

Databricks 平台现在支持在以下方面使用地理空间数据类型：

- AI/BI 地图
- Delta Sharing
- Iceberg v3 表（Databricks Runtime 18.2+）

这篇博客描述了一个保险公司的场景，但地理空间上下文在所有领域都很重要：

- 营销团队通过结合人口统计、商圈分析和客户位置模式来构建营销活动
- 电信运营商通过分析用户密度、覆盖测量和未覆盖区域来规划基站布局和维护
- 零售商通过分析新店址与现有位置的商圈重叠、人口覆盖区域和竞争对手距离来评估新店选址
- 现代农业公司通过分析土壤传感器、田块区域和天气预报来制定变量施肥和灌溉方案
- 能源和公用事业公司通过结合地形、天气模式和基础设施需求来评估可再生能源场址潜力

## 地理空间的下一步

开放湖仓一体的故事不止于 Databricks 平台。Databricks 正在向 Apache Spark 4.2（计划于 2026 年夏季发布）贡献 GEOMETRY 和 GEOGRAPHY 类型。您今天在 Databricks 上查询的几何和地理类型，将成为每个 Spark 社区用户都可使用的同一流类型。

### 向产品团队提供您的反馈
如果您想分享您对额外地图可视化需求、ST 表达式或任何地理空间功能的请求，请填写此简短反馈调查。

### 在您的收件箱中获取最新文章
订阅我们的博客，将最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Geospatial Unbounded: Spatial SQL GA with AI/BI Maps, Delta Sharing, and Iceberg v3](https://www.databricks.com/blog/geospatial-unbounded-spatial-sql-ga-aibi-maps-delta-sharing-and-iceberg-v3)
> 
> 翻译时间：2026-06-13 06:20
