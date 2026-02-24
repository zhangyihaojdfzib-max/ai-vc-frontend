---
title: Zerobus Ingest全面上市：简化架构，将数据直接流式传输至湖仓
title_original: Announcing General Availability of Zerobus Ingest
date: '2026-02-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-general-availability-zerobus-ingest-part-lakeflow-connect
author: ''
summary: 本文宣布了Zerobus Ingest的全面上市，这是一项完全托管、无服务器的服务，旨在解决传统流式架构（如Kafka）的复杂性和高成本问题。它采用单一接收端架构，允许数据生产者直接将事件推送到受治理的Delta表中，从而移除了中间消息总线、模式注册表和连接器等组件。此举大幅简化了架构，降低了成本与运营开销，并支持高性能、大规模的数据摄取，同时通过Unity
  Catalog提供从创建之初的数据治理与血缘追踪。
categories:
- AI基础设施
tags:
- 数据湖仓
- 流式数据
- 数据架构
- 无服务器
- 实时计算
draft: false
translated_at: '2026-02-24T04:38:51.143266'
---

随着企业扩展实时运营智能，传统流式架构已成为成本高昂的瓶颈。管理Kafka等消息总线、处理模式注册表和连接器框架会产生显著的"复杂性税"，使高价值的工程资源从战略性业务计划中分流。同时，重复存储推高了云账单，多跳架构则延迟了关键洞察。此外，传输中的数据通常处于集中治理框架之外，带来了合规风险和血缘盲点。

## 推出Zerobus Ingest：面向湖仓的近实时流式传输

今天，我们很高兴地宣布Zerobus Ingest全面上市，这是Lakeflow Connect的一部分。Zerobus Ingest是一项完全托管、无服务器的服务，可将数据直接流式传输到受治理的Delta表中，通过移除中间层来提供简化、高性能的架构。

通过使数据能够直接从生产者流向湖仓，Zerobus Ingest大幅降低了成本并消除了工具蔓延。它还能在大规模下提供高性能，支持数千个并发连接，并在5秒内实现超过10GB/秒的聚合吞吐量到单个表。

### 单一接收端优势：简化架构，大幅降低成本

像Kafka这样的传统消息总线被设计为多接收端架构：作为通用枢纽将数据路由到数十个独立的消费者。然而，当您的唯一目的地是湖仓时，这种灵活性可能会带来高昂的成本。Zerobus Ingest采用了一种根本不同的方法，采用针对单一任务优化的单一接收端架构：将数据直接推送到湖仓。

这种架构选择消除了复杂性并大幅降低了成本：

- 无需随着数据量增长而扩展代理
- 无需为优化性能而调整分区
- 无需监控和调试消费者组
- 无需规划和执行集群升级
- 您的团队无需具备Kafka等专业知识

使用Zerobus Ingest，只有一个托管的Databricks端点。在Unity Catalog中创建您的表，通过API或SDK开始写入数据，就完成了。仅此而已，无需其他设置。无服务器架构会自动扩展以支持每秒千兆字节的摄取，无需任何配置更改。

![Zerobus Ingest允许数据生产者绕过消息总线，将事件直接推送到湖仓中的托管Delta表。](/images/posts/29619ade120a.gif)

Zerobus Ingest允许数据生产者绕过消息总线，将事件直接推送到湖仓中的托管Delta表。

Zerobus Ingest将传统流式架构从五个托管系统简化为两个组件，消除了多个故障点，减少了运营开销，并消除了对专业知识的需求。

- 传统架构：源系统 → 带有模式注册表的消息总线（Kafka集群） → 连接器 → 湖仓
- Zerobus Ingest架构：源系统 → Zerobus Ingest → 湖仓

通过消除中间消息总线，您移除了两个主要成本中心：总线本身的计算和存储，以及管理它所需的专门工程时间。与运行和维护自管理的Kafka集群相比，Zerobus Ingest以每千兆字节成本的一小部分提供数据摄取。

与运行和维护自管理的Kafka集群相比，Zerobus Ingest以每千兆字节成本的一小部分提供数据摄取。

在此深度探讨的Databricks社区博客或文档中了解更多关于Zerobus如何工作的信息。

### 支持的接口和原生集成

开发人员可以通过gRPC和REST API集成，或使用特定语言的SDK。Zerobus Ingest为特定行业集成提供了一套广泛的基于推送的接口，使其成为一个灵活的、简化数据摄取的单一工具。

- gRPC API：推荐用于需要最低延迟和最高吞吐量的高性能应用。
- REST API（测试版）：适用于Webhook、无服务器函数以及gRPC支持可能有限的语言。
- SDK：适用于Python、Java、Rust、Go和TypeScript的生产就绪库，利用gRPC简化了身份验证和批处理逻辑。
- Open Telemetry（测试版）：只需更改配置，即可将您的运营日志、指标和追踪数据带入湖仓进行长期历史分析。在此处了解更多关于Open Telemetry生态系统的信息。

了解更多关于REST和gRPC之间的区别。

此外，由于每次写入都受Unity Catalog治理，您从数据创建的那一刻起就获得了自动的血缘追踪和细粒度的访问控制——确保您的流式数据与湖仓的其他部分具有统一的治理。

## 推动客户突破：大规模指数级加速洞察

### 丰田汽车公司的实时制造监控

丰田寻求一种统一的解决方案，能够即时处理来自数千个工厂设备的遥测数据，而无需传统物联网架构的延迟和复杂性。

丰田没有将多个云服务拼接在一起，而是使用Zerobus Ingest，并与Soracom的全球物联网连接集成，以降低实时运营的高昂维护成本，转变其制造运营，并支持其可持续发展目标。

物联网数据管道架构：从边缘到分析平台，使用Zerobus Ingest和Soracom Beam

Izumi还解释说，他们能够加速运营效率，"当与我们由Databricks驱动的统一数据和AI平台'vista'结合时，我们不仅仅是更快地收集数据；我们正在优化我们的数据操作。"

### Joby Aviation：将飞行性能分析从数天加速到数分钟

作为Zerobus Ingest的早期采用者，Joby Aviation每分钟将千兆字节的飞机遥测数据直接流式传输到湖仓，使其工程团队能够近乎实时地分析飞行性能。阅读Joby Aviation案例研究。

## 赋能行业用例

传统基础设施拖慢了实时运营。通过消除中间消息总线的复杂性，Zerobus Ingest为各行各业创建了一条直接的、低于5秒的价值实现路径。

通过将来自任何行业任何来源的数据直接推送到您的湖仓，加速您的数字化转型。

制造业：最大化工厂车间效率。使用Zerobus Ingest SDK构建自定义转发代理，将海量传感器数据流式传输到湖仓。这通过消除沉重的网络基础设施开销来优化机器性能。

电信和物联网：大规模监控全球网络。部署在边缘的Zerobus Ingest将遥测数据从您的网络传输到湖仓，以近乎实时地跟踪网络负载。我们与Soracom的合作通过蜂窝、卫星和LPWAN网络扩展了与安全可靠的全球物联网数据摄取的集成。

IT和网络安全：无需ETL延迟识别威胁。通过将日志和行为事件直接流式传输到湖仓来绕过复杂的管道。这使得能够在几秒钟内进行威胁检测、自适应模型重新训练和更快的事件响应。

商业和点击流：近乎实时地个性化体验。以最小的基础设施开销从应用和设备捕获高容量的点击流数据。这使得数据能够即时可用，为个性化引擎、A/B测试和转化优化提供动力。

## 可用性

Zerobus Ingest现已在AWS上全面上市，Microsoft Azure和Google Cloud平台支持即将推出。定价基于数据量，属于Lakeflow Jobs Serverless SKU。

作为全面上市发布的一部分，我们推出了为期6个月的促销定价期。在Lakeflow Connect定价页面了解更多信息。

## 开始使用Zerobus Ingest

准备好消除流式基础设施的复杂性了吗？只需几行代码，您就可以开始将数据直接流式传输到由 Unity Catalog 管理的表中，确保数据在到达时即可使用，以帮助提供洞察。

立即查看以下 Zerobus Ingest 资源，开始您的旅程：

- **立即试用 Zerobus Ingest**：访问文档和快速入门指南。
- **产品导览**：浏览 Zerobus Ingest，了解如何开始数据摄取。
- **构建端到端应用程序**：一个实时帆船模拟器，使用 Python SDK 和 REST API，结合 Databricks Apps 和 Databricks Asset Bundles，跟踪一支帆船舰队。阅读博客。
- **构建数字孪生解决方案**：了解如何利用 Databricks Apps 和 Lakebase 最大化运营效率、加速实时洞察和预测性维护。阅读博客。

---

> 本文由AI自动翻译，原文链接：[Announcing General Availability of Zerobus Ingest](https://www.databricks.com/blog/announcing-general-availability-zerobus-ingest-part-lakeflow-connect)
> 
> 翻译时间：2026-02-24 04:38
