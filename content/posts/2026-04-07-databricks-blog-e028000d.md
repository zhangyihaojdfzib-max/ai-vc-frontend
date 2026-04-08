---
title: MakeMyTrip如何借助Databricks实现毫秒级大规模个性化
title_original: How MakeMyTrip Achieved Millisecond Personalization at Scale with
  Databricks
date: '2026-04-07'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-makemytrip-achieved-millisecond-personalization-scale-databricks
author: ''
summary: 本文介绍了印度最大在线旅行社MakeMyTrip如何通过采用Databricks的实时模式（RTM），在Apache Spark上实现毫秒级延迟的实时个性化推荐。面对原有微批处理模式无法满足亚秒级延迟的挑战，团队避免了引入Apache
  Flink导致架构碎片化的方案，转而利用RTM的连续数据流、流水线调度和流式Shuffle等创新技术，在单一Spark技术栈上统一了实时处理流水线，显著降低了工程复杂度和运营成本，成功提升了用户体验。
categories:
- AI基础设施
tags:
- 实时计算
- Apache Spark
- 个性化推荐
- 流处理
- Databricks
draft: false
translated_at: '2026-04-08T04:40:16.475344'
---

## 大规模实现实时个性化

当旅行者搜索酒店、航班或体验时，每一毫秒都至关重要。作为印度最大的在线旅行社，MakeMyTrip 在实时速度和相关性上展开竞争。其最重要的功能之一是"最近搜索"酒店：当用户点击搜索栏时，他们期望基于与系统的交互，获得一个实时、个性化的近期兴趣列表。

在 MakeMyTrip 的规模下，要在服务于每日数百万用户（涵盖消费者和企业差旅业务线）的生产流水线上提供这种体验，需要亚秒级的延迟。通过实施 Databricks 的实时模式——Apache Spark™ Structured Streaming 中的下一代执行引擎，MakeMyTrip 成功实现了毫秒级延迟，同时保持了高性价比的基础设施并降低了工程复杂度。

## 挑战：在避免架构碎片化的前提下实现超低延迟

MakeMyTrip 的数据团队需要为所有业务线的"最近搜索"酒店工作流实现亚秒级延迟。在其规模下，即使是几百毫秒的延迟也会在用户旅程中造成摩擦，直接影响点击率。

Apache Spark 的微批处理模式引入了固有的延迟限制，尽管团队进行了大量调优，但仍无法突破——始终产生一到两秒的延迟，远低于他们的要求。

接下来，他们评估了 Apache Flink 在大约 10 个流处理流水线上的应用，这解决了他们的延迟要求。然而，采用 Apache Flink 作为第二个引擎会带来重大的长期挑战：

- **架构碎片化**：为实时和批处理维护独立的引擎
- **业务逻辑重复**：业务规则需要在两个代码库中分别实现和维护
- **更高的运营开销**：跨多个流水线的监控、调试和治理工作量加倍
- **一致性风险**：批处理和实时处理的结果存在差异风险
- **基础设施成本**：运行和调优两个引擎增加了计算支出和维护负担

## 为何选择实时模式：在单一 Spark 技术栈上实现毫秒级延迟

由于 MakeMyTrip 绝不希望采用双引擎架构，Apache Flink 并非可行的长期选择。团队做出了深思熟虑的架构决策：等待 Apache Spark 变得更快，而不是分裂技术栈。因此，当 Apache Spark Structured Streaming 引入 RTM 时，MakeMyTrip 成为了首个采用它的客户。RTM 使他们能够在 Apache Spark 上实现毫秒级延迟——满足实时需求，而无需引入另一个引擎或拆分平台。

RTM 通过三项关键技术创新实现了连续、低延迟的处理，这些创新共同消除了微批处理执行中固有的延迟来源：

- **连续数据流**：数据在到达时即被处理，而不是被离散化为周期性数据块。
- **流水线调度**：各阶段同时运行而不阻塞，允许下游任务立即处理数据，无需等待上游阶段完成。
- **流式 Shuffle**：数据在任务间立即传递，绕过了传统基于磁盘的 Shuffle 的延迟瓶颈。

这些创新共同使 Apache Spark 能够实现以前只有专用引擎才能实现的毫秒级流水线。要了解更多关于 RTM 技术基础的信息，请阅读这篇博客：《打破微批处理壁垒：Apache Spark 实时模式的架构》。

## 架构：统一的实时流水线

MakeMyTrip 的流水线遵循一条高性能路径：

- **统一摄入**：B2C 和 B2B 点击流主题合并为单一流。所有个性化逻辑——丰富化、有状态查询和事件处理——在两个用户细分群体中保持一致应用。
- **RTM 处理**：Apache Spark 引擎使用并发调度和流式 Shuffle 在毫秒内处理事件。
- **有状态丰富化**：流水线在 Aerospike 中执行低延迟查询，以检索每个用户的"最近 N 个"酒店。
- **即时服务**：结果被推送到 UI 缓存（Redis），使应用能够在 50 毫秒内提供个性化结果。

## 配置 RTM：单行代码更改

在流查询中使用 RTM 不需要重写业务逻辑或重构流水线。唯一需要的代码更改是将触发器类型设置为 RealTimeTrigger，如下面的代码片段所示：

```scala
// 示例代码片段
val query = streamingDF
  .writeStream
  .trigger(Trigger.RealTime) // 关键更改：设置为实时触发器
  .format("console")
  .start()
```

唯一的基础设施考虑是：集群任务槽位必须大于或等于源阶段和 Shuffle 阶段中活动任务的总数。MakeMyTrip 的团队在生产上线前分析了他们的 Kafka 分区、Shuffle 分区和流水线复杂性，以确保足够的并发性。

## 为生产环境共同开发 RTM

作为 RTM 的首个采用者，MakeMyTrip 直接与 Databricks 工程团队合作，使流水线达到生产就绪状态。有几项功能需要两个团队积极协作来构建、调优和验证。

1.  **流合并：将 B2C 和 B2B 合并到单一流水线**
    MakeMyTrip 需要将两个独立的 Kafka 主题流——B2C 消费者点击流和 B2B 企业差旅——统一到一个 RTM 流水线中，以便相同的个性化逻辑可以一致地应用于两个用户细分群体。在与 Databricks 工程团队密切合作一个月后，该功能得以构建并交付。结果是一个单一流水线，所有业务逻辑都集中在一处，用户细分群体之间没有差异风险。

2.  **任务复用：更多分区，更少核心**
    RTM 的默认模型为每个 Kafka 分区分配一个槽位/核心。在 MakeMyTrip 的生产设置中，有 64 个分区，这意味着需要 64 个槽位/核心——在其规模下成本过高。为了解决这个问题，Databricks 团队为 Kafka 引入了 MaxPartitions 选项，该选项允许单个核心处理多个分区。这为 MakeMyTrip 提供了在不影响吞吐量的情况下降低基础设施成本所需的杠杆。

3.  **流水线加固：检查点、背压和容错**
    团队解决了一系列特定于高吞吐量、低延迟工作负载的运营挑战：调优检查点频率和保留期、处理超时，以及在点击流流量激增时管理背压。通过扩展到 64 个 Kafka 分区、启用背压并将 MaxRatePerPartition 上限设置为 500 个事件，团队优化了吞吐量和稳定性。通过对批处理配置、分区和重试行为的迭代调优，他们最终获得了一个稳定、生产级的流水线，每天为数百万用户提供服务。

## 成果

RTM 实现了即时个性化，提高了响应速度，通过点击率衡量的用户参与度更高，并且单一统一引擎带来了运营简化。关键指标如下所示。

| 指标 | RTM 实施前 | RTM 实施后 |
| :--- | :--- | :--- |
| P50 延迟 | ~1.23 秒 | 44 毫秒 |
| P99 延迟 | >1 分钟 | ~500 毫秒 |
| CTR 提升 | 基线 | **+X%** |

## Apache Spark 作为实时引擎

MakeMyTrip 的部署证明，Spark 上的 RTM 能够提供实时应用所需的极低延迟。由于 RTM 构建在同样熟悉的 Spark API 之上，您可以在批处理和实时流水线中使用相同的业务逻辑。您不再需要为实时处理维护第二个平台或独立代码库的开销，只需一行代码即可在 Spark 上启用 RTM。

## 开始使用实时模式

要了解更多关于实时模式的信息，请观看此关于如何入门的点播视频，或查阅文档。

---

> 本文由AI自动翻译，原文链接：[How MakeMyTrip Achieved Millisecond Personalization at Scale with Databricks](https://www.databricks.com/blog/how-makemytrip-achieved-millisecond-personalization-scale-databricks)
> 
> 翻译时间：2026-04-08 04:40
