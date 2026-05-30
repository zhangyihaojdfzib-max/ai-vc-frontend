---
title: Databricks在SIGMOD 2026展示增量视图维护引擎Enzyme
title_original: Databricks at SIGMOD 2026
date: '2026-05-29'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-sigmod-2026
author: ''
summary: Databricks将在SIGMOD 2026上展示其Spark Declarative Pipelines (SDP) 工作，并获荣誉提名奖。文章重点介绍了增量视图维护引擎Enzyme的创新，包括支持复杂物化视图模式（如连接、窗口函数、非确定性函数）、多语言支持（SQL和Python）以及多种性能优化技术。Enzyme旨在简化ETL和流处理工作负载，其性能显著优于竞争方案。
categories:
- AI基础设施
tags:
- Databricks
- SIGMOD 2026
- 增量视图维护
- Enzyme
- 数据工程
draft: false
translated_at: '2026-05-30T05:46:56.509705'
---

- 了解 Databricks 如何通过 Spark Declarative Pipelines (SDP) 开创下一代数据工程，简化复杂的 ETL 和流处理工作负载。
- 深入了解我们的增量视图维护引擎 Enzyme，该引擎在 SIGMOD 会议上获得了荣誉提名奖。
- 在会议上与我们的工程师会面，讨论这些行业领先的创新成果。

Databricks 持续引领工程创新，不断突破数据和 AI 领域的可能性边界。我们激动地宣布，我们在 Spark Declarative Pipelines 上的工作将在 SIGMOD 2026 上展示，并获得了会议的荣誉提名奖。作为白金赞助商，我们将于今年 6 月 1 日至 5 日前往 SIGMOD。SIGMOD 将在印度班加罗尔举行，这里也是 Databricks 的一个大型研发中心。

我们即将发表的数据工程论文展示了 Databricks 如何为客户简化增量处理。在 Spark Declarative Pipelines (SDP) 中，有两种编写增量程序的方式，客户可以在一个管道中混合使用它们：

- 数据工程师可以为转换指定物化视图。Enzyme 引擎会在新数据到达时增量维护这些视图。增量处理的所有复杂性对物化视图的创建者完全透明。SIGMOD 2026 论文《Enzyme: Incremental View Maintenance for Data Engineering》讨论了其中一些想法。
- 精通流处理的数据工程师可以使用 SDP 的流处理引擎来增量处理数据。流处理 API 提供了多种构造——从有状态算子到水印，使得表达复杂的业务逻辑（如自定义聚合）变得容易。我们流处理产品的关键思想将出现在 VLDB 2026 论文《A Decade of Apache Spark Structured Streaming: How We Evolved the Architecture To Meet Real-world Needs》中。

以下是 Enzyme 论文以及团队工作内容的预览：

## Enzyme 在 SIGMOD 2026

### 增量视图维护

假设你是一家公司的分析师，想要分析某个地区销售的总订单数。下面的物化视图提供了答案。

CREATE MATERIALIZED VIEW  order_report as

SELECT region, sum(orders)

FROM customer_and_order_table

GROUP by region

随着新订单的添加，你希望物化视图保持最新。这种数据维护本质上就是增量视图维护问题。虽然保持上述简单的物化视图更新看似简单，但想象一下，如果物化视图需要跨多个表进行数据连接，或者包含窗口函数，或者调用 LLM 函数。

### Enzyme 创新

物化视图 (MV) 在查询加速方面很受欢迎——加速数据仓库中数据仪表盘的运行。在创建 Spark Declarative Pipelines 时，我们决定超越查询加速，将物化视图应用于提取-转换-加载 (ETL) 用例。我们的关键观察是，如果物化视图能够高效地增量维护，将显著简化 ETL 工作负载，否则这些工作负载需要编写复杂的自定义代码。

Enzyme 丰富了增量维护物化视图的现有文献，并展示了如何将这些技术扩展到生产工作负载中。团队研究的一些创新包括：

- 支持广泛的物化视图模式：Enzyme 在生产环境中增量维护复杂的物化视图，包括包含连接、窗口函数、聚合及其组合的视图。与其他行业解决方案不同，Enzyme 还支持非确定性函数，例如 current_date() 和 AI 特定函数。
- 多语言支持：虽然大多数行业解决方案只关注 SQL，但 Enzyme 也支持用 Python 指定的物化视图。Python 现在是大多数数据工程和 AI 工作负载的首选语言。Enzyme 解决了多语言支持带来的许多有趣挑战，例如准确检测物化视图定义中的变化。
- 性能优化：Enzyme 具有多种优化措施来减少需要处理的数据量，包括自动确定更新应在分区级别而非行级别应用的技术，从而减少重写开销。它选择性地缓存中间结果以减少 IO 成本。它使用一个成本模型，利用计划信息和先前的执行来确定最高效的增量策略。

![图 1：Enzyme 的性能显著优于另一个竞争行业解决方案（由于许可限制，名称匿名化为 CV-IVM）。](/images/posts/5d3e86e7b055.png)

图 1：Enzyme 的性能显著优于另一个竞争行业解决方案（由于许可限制，名称匿名化为 CV-IVM）。

有兴趣了解更多吗？查看论文，如果你在 SIGMOD 现场，请参加我们的演讲以获取更多细节。

## 在 SIGMOD 与团队会面：

请光临我们的展位，与团队会面并了解更多关于 Databricks 正在进行的创新。此外，不要错过在 SIGMOD 期间直接聆听 Ritwik Yadav 演讲的机会！

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Databricks at SIGMOD 2026](https://www.databricks.com/blog/databricks-sigmod-2026)
> 
> 翻译时间：2026-05-30 05:46
