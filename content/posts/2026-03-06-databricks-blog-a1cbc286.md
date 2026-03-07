---
title: 利用Zerobus Ingest与Lakebase构建近实时应用
title_original: Building a near real-time application with Zerobus Ingest and Lakebase
date: '2026-03-06'
source: Databricks Blog
source_url: https://www.databricks.com/blog/building-near-real-time-application-zerobus-ingest-and-lakebase
author: ''
summary: 本文介绍了Databricks推出的Zerobus Ingest和Lakebase两款工具如何简化数据架构，实现近实时数据处理。Zerobus Ingest通过API将事件数据直接摄入湖仓，无需中间消息总线，支持大规模低延迟写入。Lakebase则是内置的托管Postgres数据库，可自动同步湖仓数据，为运营应用提供低延迟访问。两者结合使企业能够轻松构建实时监控等应用，并以外卖公司“Data
  Diners”的司机订单跟踪为例，说明了实时应用在提升运营感知和问题缓解方面的价值。
categories:
- AI基础设施
tags:
- 实时数据处理
- 数据湖仓
- Databricks
- 数据摄取
- 运营分析
draft: false
translated_at: '2026-03-07T04:34:56.282688'
---

来自物联网、点击流和应用遥测的事件数据，与Databricks数据智能平台结合后，能够驱动关键实时分析与人工智能应用。传统上，摄取这类数据需要在数据源和数据湖仓之间进行多次数据跳转（消息总线、Spark作业）。这不仅增加了运维开销和数据冗余，还需要专业知识，并且当湖仓是这些数据的唯一目的地时，这种做法通常效率低下。

一旦这些数据进入湖仓，它们会被转换和整理以供下游分析用例使用。然而，团队需要为运营用例提供这些分析数据，而构建这些定制应用程序可能是一个费力的过程。他们需要配置和维护关键的基础设施组件，例如专用的OLTP数据库实例（包括网络、监控、备份等）。此外，他们还需要管理将分析数据反向ETL到数据库的流程，以便在实时应用程序中重新呈现这些数据。客户还经常构建额外的管道，将数据从湖仓推送到这些外部运营数据库中。这些管道增加了开发人员需要设置和维护的基础设施，从而分散了他们对主要目标的注意力：为业务构建应用程序。

那么，Databricks如何简化将数据摄取到湖仓以及提供黄金数据以支持运营工作负载这两个过程呢？

答案是Zerobus Ingest和Lakebase。

## 关于Zerobus Ingest

Zerobus Ingest是Lakeflow Connect的一部分，是一组API，提供了一种将事件数据直接推送到湖仓的简化方式。Zerobus Ingest完全消除了单一接收端的消息总线层，减少了基础设施，简化了操作，并实现了大规模近实时摄取。因此，Zerobus Ingest让解锁数据价值变得前所未有的简单。

数据生产应用程序必须指定一个目标表来写入数据，确保消息正确映射到表的模式，然后启动一个流将数据发送到Databricks。在Databricks端，API会验证消息和表的模式，将数据写入目标表，并向客户端发送数据已持久化的确认。

### Zerobus Ingest的主要优势：

- **简化架构**：无需复杂的工作流和数据复制。
- **大规模性能**：支持近实时摄取（最长5秒），允许数千个客户端写入同一表（每个客户端吞吐量高达100MB/秒）。
- **与数据智能平台集成**：通过使团队能够直接在其数据上应用分析和AI工具（例如用于欺诈检测的MLflow），加速价值实现时间。

Zerobus Ingest能力

规格

摄取延迟

近实时（≤5秒）

每个客户端最大吞吐量

高达100 MB/秒

并发客户端

每表数千个

连续同步延迟（Delta → Lakebase）

10–15秒

实时foreach写入器延迟

200–300毫秒

## 关于Lakebase

Lakebase是内置于Databricks平台中的一款完全托管、无服务器、可扩展的Postgres数据库，专为低延迟运营和事务工作负载设计，这些工作负载直接运行在为分析和AI用例提供动力的同一数据上。

计算与存储的完全分离实现了快速配置和弹性自动扩展。Lakebase与Databricks平台的集成是其与传统数据库的主要区别，因为Lakebase使湖仓数据无需复杂的自定义数据管道即可直接供实时应用程序和AI使用。它旨在满足企业应用程序和智能体工作负载对数据库创建、查询延迟和并发性的要求。最后，它允许开发人员像管理代码一样轻松地对数据库进行版本控制和分支。

### Lakebase的主要优势：

- **自动数据同步**：能够轻松地将数据从湖仓（分析层）按快照、计划或连续方式同步到Lakebase，无需复杂的外部管道。
- **与Databricks平台集成**：Lakebase与Unity Catalog、Lakeflow Connect、Spark声明式管道、Databricks Apps等集成。
- **集成的权限和治理**：运营数据和分析数据具有一致的角色和权限管理。原生Postgres权限仍可通过Postgres协议维护。

这些工具共同使客户能够将来自多个系统的数据直接摄取到Delta表中，并大规模实施反向ETL用例。接下来，我们将探讨如何使用这些技术来构建一个近实时应用程序！

## 如何构建近实时应用程序

作为一个实际例子，让我们帮助一家名为“Data Diners”的外卖公司，为其管理人员赋能，构建一个应用程序来实时监控司机活动和订单配送。目前，他们缺乏这种可见性，这限制了他们在配送过程中出现问题时缓解问题的能力。

为什么实时应用程序有价值？

- **运营感知**：管理人员可以即时查看每个司机的位置以及他们当前配送的进度。这意味着在订单延迟或司机需要帮助时，盲点更少。
- **问题缓解**：实时位置和状态数据使调度员能够在发生延误时重新规划司机路线、调整优先级或主动联系客户，从而减少配送失败或延迟。

让我们看看如何在数据智能平台上使用Zerobus Ingest、Lakebase和Databricks Apps来构建这个应用！

#### 应用程序架构概述

![应用程序架构：数据生产者，Zerobus Ingest，Delta，Lakebase，Databricks Apps](/images/posts/868f10b0c47a.png)

这个端到端架构遵循四个阶段：(1) 数据生产者使用Zerobus SDK将事件直接写入Databricks Unity Catalog中的Delta表。(2) 一个连续同步管道将更新后的记录从Delta表推送到Lakebase Postgres实例。(3) 一个FastAPI后端通过WebSockets连接到Lakebase以流式传输实时更新。(4) 一个基于Databricks Apps构建的前端应用程序为最终用户可视化实时数据。

从我们的数据生产者开始，司机手机上的Data Diner应用程序将在配送订单途中发出关于司机位置（经纬度坐标）的GPS遥测数据。这些数据将被发送到一个API网关，最终由网关将数据发送到摄取架构中的下一个服务。

使用Zerobus SDK，我们可以快速编写一个客户端，将事件从API网关转发到我们的目标表。随着目标表以近实时方式更新，我们可以创建一个连续同步管道来更新我们的lakebase表。最后，通过利用Databricks Apps，我们可以部署一个使用WebSockets从Postgres流式传输实时更新的FastAPI后端，以及一个可视化实时数据流的前端应用程序。

在引入Zerobus SDK之前，流式架构在数据落地到目标表之前会包含多次跳转。我们的API网关需要将数据卸载到像Kafka这样的暂存区，并且我们需要Spark Structured Streaming将事务写入目标表。所有这些都增加了不必要的复杂性，特别是当湖仓是唯一目的地时。上面的架构展示了Databricks数据智能平台如何简化端到端企业应用程序开发——从数据摄取到实时分析以及交互式应用程序的实现。

## 开始使用

先决条件：您需要什么

- **Lakebase**：已在AWS和Azure上正式可用。
- **Zerobus Ingest**：已在AWS和Azure上正式可用。
- **Databricks Apps**：请确认您拥有创建Databricks Apps的权限。

### 步骤 1：在 Databricks Unity Catalog 中创建目标表

客户端应用程序产生的事件数据将存储在 Delta 表中。使用以下代码在您期望的目录和模式中创建该目标表。

### 步骤 2：使用 OAUTH 进行身份验证

### 步骤 3：创建 Zerobus 客户端并将数据摄取到目标表

以下代码使用 Zerobus API 将遥测事件数据推送到 Databricks 中。

#### 变更数据捕获（CDF）的限制与解决方案

截至目前，Zerobus Ingest 不支持 CDF。CDF 允许 Databricks 记录写入 Delta 表的新数据的变更事件。这些变更事件可能是插入、删除或更新。然后，这些变更事件可用于更新 Lakebase 中的同步表。为了将数据同步到 Lakebase 并继续我们的项目，我们将把目标表中的数据写入一个新表，并在该表上启用 CDF。

### 步骤 4：配置 Lakebase 并将数据同步到数据库实例

为了驱动应用程序，我们将从这个启用了 CDF 的新表中将数据同步到一个 Lakebase 实例。我们将持续同步此表，以支持我们的近实时仪表板。

![将同步表创建到 Lakebase 实例](/images/posts/e5c646056270.png)

在用户界面中，我们选择：

- 同步模式：连续（用于低延迟更新）
- 主键：table_primary_key

这确保了应用程序能以最小延迟反映最新数据。

注意：您也可以使用 Databricks SDK 以编程方式创建同步管道。

#### 通过 foreach writer 实现实时模式

从 Delta 到 Lakebase 的连续同步存在 10-15 秒的延迟，因此如果您需要更低的延迟，请考虑通过 ForeachWriter 使用实时模式，将数据直接从 DataFrame 同步到 Lakebase 表。这将在毫秒级内同步数据。

请参考 Github 上的 [Lakebase ForeachWriter 代码](https://github.com/databricks/apps/tree/main/examples/python/lakebase-foreachwriter)。

### 步骤 5：使用 FastAPI 或其他选定的框架构建应用程序

在您的数据同步到 Lakebase 后，您现在可以部署代码来构建您的应用程序。在本示例中，应用程序从 Lakebase 获取事件数据，并用其更新一个近实时应用程序，以跟踪司机在送餐途中的活动。阅读 [Get Started with Databricks Apps](https://docs.databricks.com/en/apps/index.html) 文档，了解更多关于在 Databricks 上构建应用程序的信息。

## 其他资源

查看更多教程、演示和解决方案加速器，以根据您的特定需求构建自己的应用程序。

- 构建端到端应用程序：一个实时帆船模拟器，使用 Python SDK 和 REST API，结合 Databricks Apps 和 Databricks Asset Bundles，跟踪一支帆船船队。[阅读博客](https://www.databricks.com/blog/2023/11/07/building-real-time-sailing-simulator-databricks-apps.html)。
- 构建数字孪生解决方案：了解如何利用 Databricks Apps 和 Lakebase 最大化运营效率、加速实时洞察和预测性维护。[阅读博客](https://www.databricks.com/blog/2023/10/31/building-digital-twins-databricks-apps-lakebase.html)。

在技术文档中了解更多关于 [Zerobus Ingest](https://docs.databricks.com/en/ingestion/zerobus-ingest/index.html)、[Lakebase](https://docs.databricks.com/en/lakebase/index.html) 和 [Databricks Apps](https://docs.databricks.com/en/apps/index.html) 的信息。您也可以查看 [Databricks Apps Cookbook](https://docs.databricks.com/en/apps/cookbook/index.html) 和 [Cookbook Resource Collection](https://docs.databricks.com/en/apps/cookbook/resources.html)。

## 结论

物联网、点击流、遥测和类似应用程序每天产生数十亿个数据点，这些数据点被用于驱动多个行业的关键实时应用程序。因此，简化从这些系统的数据摄取至关重要。Zerobus Ingest 提供了一种简化的方式，可以直接从这些系统将事件数据推送到湖仓一体平台，同时确保高性能。它与 Lakebase 良好配合，简化了端到端的企业应用程序开发。

---

> 本文由AI自动翻译，原文链接：[Building a near real-time application with Zerobus Ingest and Lakebase](https://www.databricks.com/blog/building-near-real-time-application-zerobus-ingest-and-lakebase)
> 
> 翻译时间：2026-03-07 04:34
