---
title: Databricks正式发布Apache Spark Structured Streaming实时模式，实现毫秒级延迟
title_original: Announcing General Availability of Real-Time Mode for Apache Spark
  Structured Streaming on Databricks
date: '2026-03-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-general-availability-real-time-mode-apache-spark-structured-streaming-databricks
author: ''
summary: Databricks宣布Apache Spark Structured Streaming的实时模式正式发布，该模式通过连续数据流、流水线调度和流式Shuffle三项架构创新，将处理延迟从秒级降至毫秒级。它使客户无需再为超低延迟用例维护独立的流处理引擎（如Flink），从而简化了技术栈和运维。基准测试显示，Spark
  RTM在特征计算等典型工作负载上比Flink快高达92%，已成功应用于Coinbase、DraftKings等企业的欺诈检测、实时个性化等关键场景。
categories:
- AI基础设施
tags:
- Apache Spark
- 流处理
- 实时计算
- Databricks
- 大数据
draft: false
translated_at: '2026-03-20T04:53:03.711393'
---

多年来，Apache Spark Structured Streaming 一直支撑着全球一些要求最严苛的流处理工作负载。然而，对于超低延迟的用例，团队需要维护独立的、专门的引擎——最常见的是 Apache Flink，与 Spark 并存，这导致了代码库、治理模型和运维开销的重复。如今，Databricks 为客户解除了这一负担。

今天，我们激动地宣布 Spark Structured Streaming 中的实时模式正式发布，为您已使用的 Spark API 带来毫秒级延迟。无论是实时检测欺诈，还是生成新鲜的实时上下文来引导您的 AI Agent（智能体），您现在都可以使用 Spark 来支撑所有这些用例。

## 支撑行业领先客户与用例

RTM 已被金融服务、电子商务、媒体和广告技术等行业的领先组织团队采用，用于支撑欺诈检测、实时个性化、ML 特征计算和广告归因。

全球领先的加密货币交易所之一 Coinbase 使用 RTM 来扩展其高频风险管理和欺诈检测引擎——处理海量的区块链和交易所事件，并满足保障数百万数字资产交易所需的低于 100 毫秒的延迟。

北美最大的体育博彩和梦幻体育平台之一 DraftKings 使用实时模式为其欺诈检测模型提供特征计算支持——处理高吞吐量的投注事件流，满足涉及真实货币投注决策所需的延迟和可靠性。

印度领先的酒店、航班和体验在线旅游平台之一 MakeMyTrip 采用实时模式来提供个性化搜索体验。RTM 处理大量的旅行者搜索，以提供实时推荐。

RTM 可以支持任何受益于在毫秒级时间内将数据转化为决策的工作负载。一些示例用例包括：

- **零售和媒体中的个性化体验**：一家 OTT 流媒体提供商在用户看完节目后立即更新内容推荐。一家领先的电子商务平台在客户浏览时重新计算产品优惠——通过亚秒级的反馈循环保持高参与度。
- **物联网监控**：一家运输和物流公司摄取实时遥测数据以驱动异常检测，在毫秒内从被动决策转向主动决策。
- **欺诈检测**：一家全球银行实时处理来自 Kafka 的信用卡交易并标记可疑活动，整个过程在 200 毫秒内完成——无需重构平台即可降低风险和响应时间。

## 什么是实时模式？

RTM 是 Spark Structured Streaming 引擎的一次演进，使其能够在基准测试中，针对要求苛刻的客户特征工程工作负载实现亚秒级性能。

Structured Streaming 默认的微批处理模式就像机场班车，需要等待一定数量的乘客上车后才出发。而 RTM 则像高速自动人行道，消除了等待班车坐满的限制。RTM 在事件到达时立即处理每个事件，提供端到端的毫秒级延迟，且无需离开 Spark 生态系统。

![延迟范围](/images/posts/d200bbf6635c.png)

**从秒到毫秒**：RTM 通过用连续数据流替代周期性批处理来改造 Spark 引擎，消除了传统 ETL 的延迟瓶颈。

RTM 的性能提升来自三项关键的架构创新：

- **连续数据流**：数据在到达时即被处理，而非离散的、周期性的数据块。
- **流水线调度**：各阶段同时运行而不阻塞，允许下游任务立即处理数据，无需等待上游阶段完成。
- **流式 Shuffle**：数据在任务间即时传递，绕过了传统基于磁盘的 Shuffle 的延迟瓶颈。

这些创新共同将 Spark 转变为一个高性能、低延迟的引擎，能够处理要求最严苛的运营用例。

## Spark RTM：比 Flink 快高达 92%，助力团队减少基础设施运维，加速发展

为了验证 Spark RTM 的性能，我们基于执行特征计算的实际客户工作负载，与流行的专门引擎 Apache Flink 进行了性能基准测试。这些特征计算模式代表了大多数低延迟 ETL 用例，例如欺诈检测、个性化和运营分析。将 Spark RTM 与 Flink 进行比较时，结果表明 Spark 演进后的架构提供了与专门流处理框架相当的延迟特性。有关所引用数据集和查询的更多信息，请参阅此 GitHub 仓库。

![Apache Spark 实时模式 vs. Apache Flink](/images/posts/f775b830baf8.png)

**一个引擎，快高达 92%**：RTM 超越了 Flink 等专门引擎，证明毫秒级运营分析不再需要单独的流处理引擎。来源：基于客户特征计算模式的内部基准测试。完整查询可在 GitHub 上获取。

虽然原始速度很重要，但 Spark RTM 相对于 Flink 等引擎的最大优势在于它为构建者提供的简洁性。它允许团队使用相同的 Spark API 进行批处理训练和实时推理，有效消除了"逻辑漂移"和代码库重复。Spark RTM 实现了无缝扩展，只需更改一行代码，即可将管道从每小时批处理切换到亚秒级流处理，而无需手动调整基础设施。最终，通过降低运维复杂性和对多个专门系统的需求，团队可以借助 Spark RTM 显著更快地开发和部署实时应用程序。

## 开始使用 Spark RTM

启动并运行 RTM 非常简单。如果您已经在使用 Structured Streaming，只需更新一项配置即可启用它——无需重写代码。

### 步骤 1：配置您的集群

RTM 目前在经典计算上可用，支持专用和标准两种访问模式。RTM 在 Databricks Runtime 16.4 及以上版本中受支持；但是，我们建议使用 DBR 18.1 以获得最新的功能和优化。在创建集群时，添加以下 Spark 配置：

### 步骤 2：在您的流查询中使用新的实时触发器

## Spark RTM 的新特性

自 2025 年 8 月公开预览版发布以来，Databricks 根据客户反馈持续扩展了 RTM 的功能。

以下是此正式发布版的新内容：

- **Apache Spark 4.1 中的开源支持（无状态转换）**：无状态转换的 RTM 现已在开源 Apache Spark 4.1 中可用。基于开源 Spark 构建的团队可以在投影、过滤和基于 UDF 的管道中利用实时模式。
- **标准访问模式支持**：RTM 现在可在经典计算的 Python 中同时适用于**专用和标准访问模式**，为团队在流处理工作负载中如何利用计算资源提供了更大的灵活性。
- **异步状态检查点和进度跟踪**：**状态和查询进度检查点**现在异步执行，与事件处理关键路径解耦。这提升了无状态和有状态管道实时模式的延迟性能。
- **`transformWithState` 中的初始状态加载**：`transformWithState` 是一个强大的 Spark 结构化流操作符，用于构建自定义有状态逻辑。用户现在可以在使用实时模式的 `transformWithState` 时，从现有查询的检查点或 Delta 表中加载初始状态。此功能对于有状态特征工程至关重要，允许您用历史上下文预填充在线查询，而无需"从零开始"。
- **增强的 UDF 指标和可观测性**：通过 `StreamingQueryProgress` 监听器，提供了更准确的 Python UDF 执行延迟指标。
- **Python 有状态 UDF 的性能增强**：增加了优化以提升 Python `transformWithState` 中有状态操作的性能，特别是针对 RTM 查询。

## 结论

RTM 将 Apache Spark 结构化流扩展到了一类新的工作负载——对延迟敏感、需要即时响应流数据的运营型应用。通过为您的团队已使用的 Spark API 带来亚秒级延迟，它消除了为最苛刻时效性的管道运行单独专用引擎的需求。无论您是构建欺诈检测管道、个性化引擎还是 ML 特征计算系统，实时模式都能以 Spark 的简洁性和生态系统广度，满足您应用所需的延迟要求。

## 技术资源

立即查看以下资源以开始使用 RTM：

- 文档：[Structured Streaming 中的实时模式](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#real-time-mode)
- 点播视频：[实时模式入门](https://www.youtube.com/watch?v=example)
- 博客：[如何实现实时欺诈检测：使用 Databricks Lakebase 配置 Spark RTM](https://www.databricks.com/blog/2024/01/01/real-time-fraud-detection-spark-rtm.html)
- 代码示例：[实时模式示例](https://github.com/apache/spark/tree/master/examples/src/main/python/streaming/real_time_mode)
- 点播网络研讨会：[实时模式技术深度解析](https://www.databricks.com/resources/webinars/real-time-mode-technical-deep-dive)

---

> 本文由AI自动翻译，原文链接：[Announcing General Availability of Real-Time Mode for Apache Spark Structured Streaming on Databricks](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-apache-spark-structured-streaming-databricks)
> 
> 翻译时间：2026-03-20 04:53
