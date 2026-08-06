---
title: Variant正式发布：半结构化数据读取提速30倍
title_original: Ingest semi-structured data faster and more efficiently with Variant
  - Now Generally Available
date: '2026-08-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ingest-semi-structured-data-faster-and-more-efficiently-variant-now-generally-available
author: ''
summary: Databricks宣布Variant数据类型正式发布，该技术解决了半结构化数据摄取中灵活性与性能的取舍问题。Variant支持无缝处理Schema变更，无需更新管道即可摄取JSON、XML等数据。结合Variant
  Shredding和Predictive Optimization，读取速度比未分片快近4倍，比存储为字符串快30倍。已有超5000个团队使用，每月处理160TB数据，执行5亿次查询，并广泛集成于Auto
  Loader、Agent Bricks等平台组件。
categories:
- AI基础设施
tags:
- Variant
- 半结构化数据
- Databricks
- 数据摄取
- 性能优化
draft: false
translated_at: '2026-08-06T05:11:55.315444'
---

- 现已正式发布，Variant 使团队能够在半结构化数据上实现结构化数据的性能，读取速度最高提升 30 倍
- Variant 无缝处理不可预测的 Schema 变更，团队无需更新管道即可摄取半结构化数据
- Variant 已广泛集成到 Databricks 平台中——涵盖数据（Auto Loader、Spark Declarative Pipelines）和 AI 工作负载（Agent Bricks、AI Functions）

多年来，摄取 JSON、XML 或 CSV 等半结构化数据一直意味着艰难的取舍。数据团队可以构建 ETL 管道将数据 Schema 化以获得快速查询，但牺牲灵活性；或者将数据存储为字符串以保持灵活性，但承受查询性能缓慢的代价。为了解决这一取舍问题，我们与 Delta 和 Spark 社区合作，引入了 Variant 数据类型，并将其推广到 Parquet 和 Iceberg 社区，将湖仓一体统一为半结构化数据的单一开放标准。

我们很高兴地宣布，Variant 现已在 Databricks 中正式发布。此次发布还包括同样正式发布的 Variant Shredding，这是一项性能优化功能，利用 Predictive Optimization 自动提升 Variant 数据的查询性能。借助 Variant，团队可以灵活摄取半结构化数据，同时不影响下游查询性能。

## 大规模灵活摄取

超过 5,000 个团队正在使用 Databricks 写入 Variant。这些团队最常使用 Variant 摄取来自 Kinesis 或 Event Hub 等流式源的事件、来自 API 的 JSON 负载，以及来自 PostgreSQL 和 MongoDB 等数据库的无 Schema 数据。

Variant 在处理摄取源的 Schema 变更时尤为有用。例如，上游应用可能会更改其 API 类型。这会导致下游团队忙于更新相关管道、对现有数据进行回填，并处理切换。更糟糕的是，大多数企业拥有独立的数据平台和应用团队，使得这些 Schema 变更难以预测。借助 Variant，用户可以灵活地将所有半结构化数据摄取到表中。

![image3.png](/images/posts/f48508ed5ef9.png)

Variant 消除了处理半结构化数据的初始成本。构建管道将数据 Schema 化需要时间，数据工程师需要证明其时间投入的合理性。Variant 颠覆了这一范式——团队可以轻松地先落地数据，然后再确定其对业务其他部分的价值。

## 借助 Predictive Optimization 实现更快、更智能的查询

Databricks 用户每月在超过 160 TB 的 Variant 数据上执行 5 亿多次 Variant 查询。Databricks 使读取 Variant 的速度与读取托管表上的 Schema 化数据一样快。通过使用 Shredding，Variant 将常见字段作为列存储在底层 Parquet 文件中。Predictive Optimization 会根据用户独特的工作负载和查询模式进行训练，利用机器学习识别最关键的分片字段，并收集这些字段的统计信息以改善文件跳过。因此，Databricks 只扫描查询所需的文件和列，避免不必要的工作并提升性能。

Variant Shredding 的读取速度比未分片的 Variant 快近 4 倍——比将 JSON 存储为字符串快 30 倍：

![image2.png](/images/posts/2244566ac1e7.png)

借助 Variant，Databricks 正在大规模释放极速性能：

我们需要查询安全日志，这些日志不仅仅是简单的扁平记录，而是难以高效搜索的复杂 JSON 结构。Databricks 的 Variant 支持结合 Shredding，能够实现对深层嵌套属性的高性能查询——即使在 PB 级规模下也是如此

![Panther](/images/posts/05517be1163f.png)

—— Russell Leighton，首席架构师

## 在 Databricks 中使用 Variant

借助 Databricks，您可以在整个数据技术栈中使用 Variant。

我们的用户通常使用两种工具将半结构化数据摄取为 Variant：

1. Auto Loader，一种从对象存储增量处理半结构化文件的源

1. Zerobus，一种完全托管的摄取服务，无需使用消息总线即可直接写入表

两种摄取方式都将数据写入 Delta 或 Iceberg，使任何客户端都能与湖仓一体中的数据进行互操作。为简化设置，可使用 Lakeflow Pipelines 编辑器中的 Genie Code，通过自然语言轻松生成 Auto Loader 摄取管道。

![Delta or Iceberg](/images/posts/eaf06ed90a37.png)

团队随后可以在 Lakehouse 中直接消费 Variant 数据。由于数据在摄取过程中已被智能分片，仪表板和报表可以直接查询数据，速度与结构化数据一样快。

在不久的将来，我们计划进一步扩展 Variant 支持，包括按 Variant 字段进行 Liquid Clustering、扩展 SQL 函数以及更多功能集成。

## 立即开始使用 Variant

借助 Variant，您在使用半结构化数据时不再需要在灵活性和性能之间做出取舍。Databricks 使用 Predictive Optimization 跟踪工作负载和查询模式，自动以最佳性能写入 Variant 数据，从而在各产品中实现最优表现。

开始使用 Variant 非常简单——点击此处试用。

---

> 本文由AI自动翻译，原文链接：[Ingest semi-structured data faster and more efficiently with Variant - Now Generally Available](https://www.databricks.com/blog/ingest-semi-structured-data-faster-and-more-efficiently-variant-now-generally-available)
> 
> 翻译时间：2026-08-06 05:11
