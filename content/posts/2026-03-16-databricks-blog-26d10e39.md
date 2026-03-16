---
title: 突破微批处理壁垒：Apache Spark实时模式架构解析
title_original: 'Breaking the Microbatch Barrier: The Architecture of Apache Spark
  Real-Time Mode'
date: '2026-03-16'
source: Databricks Blog
source_url: https://www.databricks.com/blog/breaking-microbatch-barrier-architecture-apache-spark-real-time-mode
author: ''
summary: Apache Spark 4.1推出的实时模式（RTM）使Structured Streaming能够实现毫秒级延迟，打破了传统上在高吞吐量ETL与低延迟流处理之间必须二选一的困境。文章深入剖析了RTM的混合执行模型架构，它通过延长epoch持续时间、实现数据连续非阻塞流动、分摊检查点开销，在保留微批处理容错与高吞吐优势的同时，成功将延迟降至毫秒级，从而让Spark能够统一处理从批量ETL到实时特征工程等多种工作负载。
categories:
- AI基础设施
tags:
- Apache Spark
- 流处理
- 实时计算
- 大数据架构
- Structured Streaming
draft: false
translated_at: '2026-03-16T05:12:00.034837'
---

随着Apache Spark 4.1中实时模式（RTM）的发布，Structured Streaming现在能够提供毫秒级的延迟。在最近的一篇博客文章中，我们展示了RTM如何在许多低延迟特征工程工作负载上超越Flink（见下文）。

在这篇博客中，我们将讨论使Structured Streaming能够同时支持高吞吐量ETL工作负载和超低延迟工作负载的架构变化。

Apache Spark RTM在特征工程用例中比Flink更快。

![Apache Spark Real-Time Mode vs. Apache Flink](/images/posts/e7c69032823a.png)

## 吞吐量与延迟的两难困境

直到现在，选择流处理引擎都意味着需要做出权衡：选择像Apache Spark这样的系统用于高吞吐量ETL工作负载，或者选择像Apache Flink这样的系统用于低延迟工作负载。这两个系统具有非常不同的语义和性能特征。随着Structured Streaming中RTM的出现，这种情况发生了变化。RTM的引入使得Apache Spark现在能够同时处理高吞吐量和超低延迟的用例。这意味着现在可以选择一个单一的引擎，无需新的学习曲线，并避免管理两个完全不同的系统。

## 微批处理架构提供高吞吐量

Spark Structured Streaming采用微批处理架构：流处理系统接收输入数据，并根据数据可用性和最大批处理大小配置将其划分为称为"epoch"的离散批次。Spark引擎通过投影、过滤和聚合等转换应用业务逻辑。结果以连续的批次流形式输出。Structured Streaming因其微批处理架构而在高吞吐量处理方面表现出色：由于多个记录被一起处理，固定开销得以分摊，并且向量化执行可以进一步提高吞吐量。这些批次并行执行，同时保持硬件的高利用率。微批处理模式动态地在多个流之间分配任务槽，这进一步有助于提高利用率和吞吐量。Spark基于血统的容错这一基础创新确保了这些流处理具有强"恰好一次"的保证。

与微批处理模式相比，RTM以非阻塞方式处理数据。

![Existing microbatch execution vs. Real-Time Mode (RTM)](/images/posts/5de41d72ac5f.png)

## 实现低延迟的挑战

虽然Structured Streaming非常擅长处理秒级的ETL和摄取工作负载，但许多运营用例需要毫秒级的延迟。金融交易中的欺诈检测、旅游业的实时洞察，或分析联网车辆的遥测数据，都是客户需要在毫秒内得到结果的例子。

### 架构挑战：为什么更小的批次行不通

显而易见的解决方案似乎很简单：只需让批次变得更小。如果我们一次处理一条记录，就应该获得实时性能。不幸的是，事情并非如此简单。

Structured Streaming中的每个微批次都带有固定成本，当处理少量数据时，这些成本会主导执行时间。系统在每个微批次执行前后都会将日志文件写入持久化对象存储。此外，每个有状态查询的状态更新也需要在微批次结束时上传到对象存储。这些是保证一致性语义的关键步骤，但可能会增加数百毫秒甚至数秒的执行时间。即使我们隐藏了其中一些延迟，规划每个批次的延迟、逻辑和物理规划开销、任务序列化和调度都难以减少。正如您可以想象的，缩小批次大小很快就会遇到瓶颈。下图显示，当微批次变得太小（最左侧的柱状图）时，固定的微批次处理成本主导了执行并增加了端到端延迟。

超过某个阈值后，由于固定开销，更低的批次大小反而会增加延迟

![](/images/posts/a405488bc63c.png)

这给我们带来了一个架构挑战：我们希望保留微批处理架构的成本和容错优势，同时实现人们期望的一次处理一条记录的模型（如Apache Storm和Apache Flink）所具有的低延迟。我们的关键见解是，我们可以改进微批处理架构以支持实时工作负载。我们继续使用了许多核心微批处理架构特性，例如用于容错的检查点。然而，我们消除了那些导致数据等待并产生高延迟的步骤。我们将在下面讨论这些变化。

### 我们的解决方案：混合执行模型

以下是我们如何改进Structured Streaming延迟的方法：

#### 1. 具有连续数据流的更长持续时间epoch

微批处理模式处理称为epoch的数据批次。epoch边界是预先使用起始和结束偏移量决定的。实时模式则处理持续时间更长的epoch，但改变了数据在每个epoch内的流动方式。数据现在连续地流经不同的阶段和算子，而不会阻塞。由于epoch持续时间更长，检查点和屏障的开销得以分摊。在epoch边界，我们仍然使用屏障进行恢复记账和任务重新调度——保留了使微批处理架构具有弹性和高效性的优点。我们本质上将Structured Streaming中的微批处理演进成了一个检查点间隔。

#### 2. 并发处理阶段

在Structured Streaming架构中，处理阶段是顺序执行的——Reducer等待Mapper完成，造成了不必要的延迟。我们在实时模式中使这些阶段并发执行。现在，Spark驱动程序请求源偏移量并调度Mapper，但Reducer可以在shuffle文件一可用时就开始处理，而不是等待所有Mapper完成。这一改变极大地减少了端到端延迟。下面的RTM图显示两个阶段并发运行，阶段2在阶段1处理完行后立即开始处理。

实时模式使用并发阶段来降低延迟

![Concurrent stages in Real-Time Mode decreases overall latency](/images/posts/d08ed50a4c21.png)

#### 3. 非阻塞算子

我们重构了像shuffle这样的关键算子，这些算子原本是为具有大量缓冲的批处理执行而设计的。在批处理模式下，分组聚合会缓冲所有记录，执行预聚合，并仅在结束时发出结果。对于实时处理，我们修改了这些算子，以最小化缓冲并持续产生结果，允许数据在管道中流动而无需不必要的等待。

## 总结

通过采用具有连续数据流的更长持续时间epoch、并发处理阶段和非阻塞算子，我们扩展了Apache Spark Structured Streaming引擎，使其能够同时处理高吞吐量和超低延迟的流处理用例。这种混合方法现在消除了在流处理引擎之间进行选择的需要。用户只需要学习Apache Spark，无需再学习另一个专门用于超低延迟流处理的框架。

实时模式已在Databricks投入生产，并被从尖端金融公司到旅游网站的多个客户使用。我们的客户能够为其用例实现毫秒级延迟。

虽然这是Spark能力的一个重要飞跃，但我们仍在继续添加新的流处理功能。如果您的组织正在寻找实时工作负载的解决方案，不妨试试Apache Spark Structured Streaming！

## 探索技术资源

要深入了解RTM背后的工程细节，请观看由我们的主题专家主持的这场点播会议。他们将详细介绍实时模式的设计和实现。

或查阅《实时模式技术指南》了解如何开始使用。您将找到为流处理工作负载启用实时处理所需的一切信息。

---

> 本文由AI自动翻译，原文链接：[Breaking the Microbatch Barrier: The Architecture of Apache Spark Real-Time Mode](https://www.databricks.com/blog/breaking-microbatch-barrier-architecture-apache-spark-real-time-mode)
> 
> 翻译时间：2026-03-16 05:12
