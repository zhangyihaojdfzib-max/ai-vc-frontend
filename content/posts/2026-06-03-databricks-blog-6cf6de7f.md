---
title: Spark实时模式革新游戏会话化
title_original: 'Apache Spark Real-Time Mode for Gaming: A Better Way to Do Real-Time
  Sessionization'
date: '2026-06-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/apache-spark-real-time-mode-gaming-better-way-do-real-time-sessionization
author: ''
summary: 本文介绍Apache Spark实时模式如何通过transformWithState算子实现游戏会话的亚秒级实时处理。该方案支持响应式事件处理和主动式定时器驱动心跳输出，替代了Flink等外部引擎或定制内部系统。文章以游戏会话跟踪为例，展示了实时模式在数百万设备场景下的低延迟、高精度和统一架构优势，帮助团队利用熟悉的Spark生态加速开发关键运营应用。
categories:
- AI基础设施
tags:
- Apache Spark
- 实时流处理
- 游戏会话化
- transformWithState
- 低延迟架构
draft: false
translated_at: '2026-06-04T06:36:21.723839'
---

- 探索 Apache Spark™ 实时模式如何实现对数百万活跃设备会话的实时游戏会话化
- 了解 transformWithState 定时器如何驱动主动式、基于定时器的心跳——按计划生成输出，独立于输入数据
- 了解实时模式与 transformWithState 结合如何替代定制内部应用和外部流处理引擎——为输入处理和定时器驱动输出提供亚秒级精度

在游戏行业，每一毫秒都至关重要。为了推动游戏内个性化、支持推荐引擎以及做出动态内容调度决策，平台必须以亚秒级延迟处理全球数百万玩家的会话数据。

如今，满足这些超低延迟需求不再需要采用多引擎的割裂架构。在本博客中，我们探讨了 Apache Spark 实时模式的一个实际实现。通过利用新的 transformWithState 算子处理复杂的有状态逻辑，我们展示了 Spark 如何实现端到端的毫秒级性能。了解您的团队如何利用熟悉的 Structured Streaming 生态系统加速开发，并构建关键任务的运营应用。

## 用例概述

### 从游戏开始到游戏结束——为何会话跟踪至关重要

对于游戏平台而言，了解哪些设备处于活跃状态以及活跃时长不仅仅是基础设施问题——它驱动着业务。实时会话数据为个性化游戏体验提供支持，为推荐引擎提供燃料，为内容调度决策提供信息，并在数百万台主机和 PC 上提供设备健康信号。运营团队利用这些数据实施家长控制并检测异常会话模式。

### 会话事件基础

来自主机和 PC 的会话事件流入 Kafka 主题。每个事件携带一个设备 ID 和一个会话 ID。设备 ID 标识主机或 PC；会话 ID 标识游戏会话。任何时刻每台设备只能有一个活跃会话。

该管道处理四种场景：

- 会话开始（GameStart）：到达一个开始事件。管道存储会话 ID 和开始时间，发出一个 SessionActive 事件，并注册一个 30 秒的处理时间定时器。如果该设备已有另一个活跃会话，则先结束旧会话。
- 会话心跳（Active）：定时器每 30 秒触发一次。管道计算 now - start_time，发出带有当前持续时间的 SessionActive 心跳，并重新注册定时器。
- 会话结束（GameEnd）：到达一个与活跃会话匹配的结束事件。管道发出带有最终持续时间的 SessionEnd 并清除状态。
- 会话超时（GameSessionTimeout）：定时器触发，计算出的持续时间超过可配置的最大值。管道不发出心跳，而是发出带有超时原因的 SessionEnd 并清理状态。

### 为何采用实时模式的 Spark 是游戏规则改变者

采用微批模式的 Spark Structured Streaming 可以处理有状态会话化，但当用例要求输入处理和定时器驱动输出均达到亚秒级精度时，微批模式就力不从心了。过去，这一差距促使团队转向管理额外的专用引擎或构建定制解决方案。

使用 Apache Flink：可以实现状态管理和定时器，但采用 Flink 意味着采用一整套并行生态系统：独立的集群、状态后端、部署模型、监控栈和代码库，所有这些都与 Databricks 平台并存。结果是基础设施碎片化、运营复杂性增加，以及运营和配备第二个流处理引擎的成本。

使用定制内部解决方案：一些团队构建自己的会话化服务——例如，基于 Akka 的 Actor 系统，其中每个设备对应一个 Actor，负责管理会话状态、定时器和心跳发送。这些方案与 Flink 一样带来基础设施和运营开销，且面临额外挑战：它们无法扩展。跨节点分布数百万个有状态 Actor 需要自行设计。这些系统初期可行，但最终会进入维护模式——稳定到足以运行，但不易扩展。

如今，实时模式为客户弥补了这一差距——使用团队已经熟悉的相同 Spark API，在单一统一引擎中提供亚秒级精度。

## 实时模式与 transformWithState

transformWithState 是 Spark Structured Streaming 中的下一代算子，使复杂的有状态处理变得灵活且可扩展。关键特性包括面向对象的状态管理、复合数据类型、定时器驱动逻辑、自动 TTL 支持和模式演化。结合实时模式，它为输入处理和定时器驱动输出提供亚秒级精度。

游戏会话化用例需要两件事：

- 响应式处理：处理到达的会话开始和结束。
- 主动式输出：按计划为每个活跃会话生成心跳，独立于输入数据。

transformWithState 通过一个包含两个专用方法的单一 StatefulProcessor 类同时实现这两点。handleInputRows() 响应传入的 Kafka 事件——处理会话开始和结束，在事件到达时维护会话化状态。

handleExpiredTimer() 处理两者之间的一切——触发以生成心跳和超时等主动式输出，无论是否有新数据到达。

## 工作原理：构建实时游戏会话化管道

### 管道架构概览

![管道架构概览](/images/posts/c048fc1e6b5b.png)

- 事件摄取：来自主机和 PC 的会话事件（开始和结束）到达 Kafka 主题。每个事件被解析，并从设备特定标识符中提取 deviceId。
- 有状态分组：流按 deviceId 分组——确保给定设备的所有事件路由到同一个有状态处理器实例。
- 处理：transformWithState 应用 Sessionization 处理器，该处理器使用以会话 ID 为键的 MapState 来跟踪每台设备的活跃会话。当会话开始到达时，handleInputRows() 存储会话状态，发出 SessionActive 事件，并注册第一个 30 秒定时器。此后，handleExpiredTimer() 接管——每 30 秒发出心跳并检查超时。当会话结束事件到达时，handleInputRows() 重新接手——发出带有最终持续时间的 SessionEnd，清除状态，并停止定时器循环。
- 输出：处理后的会话事件——开始、心跳、结束和超时——以 JSON 格式写入输出 Kafka 主题，供下游消费。

### 实现深度解析

有关架构、代码实现和生产考虑的详细说明，请参阅此配套博客——我们将在其中逐步讲解 StatefulProcessor 代码、定时器生命周期、状态管理模式以及使用 StreamingQueryListener 进行监控。以下结果展示了管道的吞吐量和延迟特性，突出了微批模式（MBM）和实时模式（RTM）之间的显著延迟差异：

#### 吞吐量

为了在实际负载下验证管道，我们使用以下持续吞吐量进行了测试：

指标（每分钟）

数值

输入事件（会话开始 + 结束）

~500K

活跃会话数

发出的心跳记录数

输入到输出的放大倍数

绝大多数输出并非由输入数据触发——而是完全由 handleExpiredTimer() 生成，按计划主动发出心跳。

#### 延迟

延迟是端到端测量的——从 Kafka 输入主题时间戳到输出主题时间戳。采用实时模式，管道实现了 432ms 的 p99 延迟——比微批模式快 20 倍。

![延迟对比：实时模式（RTM）与微批模式（MBM）](/images/posts/80903a5d6e1a.png)

## 结论

像游戏会话化这样的用例，需要能够超越简单处理传入事件的管道——主动按计划发送心跳信号、追踪数百万并发会话并高效管理状态。这种模式并不仅限于游戏领域。任何需要定时驱动输出的工作负载——物联网心跳信号、会话追踪、实时告警、设备监控——都可以用同样的方式构建。

transformWithState中的定时器让这成为可能。一个单一的StatefulProcessor类即可处理完整的会话生命周期——响应式输入处理与主动式定时驱动输出。结合实时模式，输入记录的处理和定时器的触发都能达到亚秒级精度——无需等待下一个批处理间隔，而是即刻执行。这一切都在Databricks内部完成，无需第二个引擎。

如果你已经在以微批模式运行Structured Streaming管道，并且为了降低延迟而准备引入第二个引擎，请先尝试实时模式。切换只需更改一个触发器参数——无需重写代码，无需更换平台：

亲自尝试：

- 配套笔记本（含数据生成器）：运行完整的游戏会话化管道，自行比较微批模式与实时模式的延迟差异。
- transformWithState API指南：状态变量、定时器、TTL及模式演化
- 实时模式参考：支持的算子、执行模式、数据源、数据接收端及语言支持

实时模式现已正式发布（GA）。

---

> 本文由AI自动翻译，原文链接：[Apache Spark Real-Time Mode for Gaming: A Better Way to Do Real-Time Sessionization](https://www.databricks.com/blog/apache-spark-real-time-mode-gaming-better-way-do-real-time-sessionization)
> 
> 翻译时间：2026-06-04 06:36
