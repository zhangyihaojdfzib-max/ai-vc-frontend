---
title: Lakebase CDF：消除操作数据库管道蔓延
title_original: Announcing Lakebase Change Data Feed (CDF)
date: '2026-05-27'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-lakebase-change-data-feed-cdf
author: ''
summary: Databricks 宣布 Lakebase 变更数据馈送（CDF）进入公开预览版，该功能通过 Unity Catalog 托管表统一暴露所有表的变更，无需数据库连接器或单独提取作业。原生
  CDC 实现端到端治理，下游消费者可订阅同一隔离馈送而不影响主工作负载。操作数据库作为奖章架构中的原生 Bronze 层运行，与 Lakehouse 形成闭环，提供全面治理和血缘追踪。
categories:
- AI基础设施
tags:
- Lakebase
- 变更数据馈送
- CDC
- Unity Catalog
- 数据治理
draft: false
translated_at: '2026-05-28T06:11:54.301575'
---

- Lakebase 变更数据馈送（公开预览版）消除了来自操作数据库的管道蔓延。在每个 Lakebase 项目中启用一次 CDF，即可通过 Unity Catalog 托管表暴露所有表的变更，供任何引擎、模型或 Agent（智能体）直接读取访问。
- 原生 CDC 在无需边车基础设施的情况下实现端到端治理：无需数据库连接器、复制状态监控或单独的提取作业；下游消费者（如 SDP 流式管道、DBSQL 物化视图和 Agent Bricks 嵌入/向量）均可订阅同一隔离馈送，而不会影响主工作负载。
- 操作数据现在作为奖章架构中的原生 Bronze 层运行。Lakebase 同步表已为应用程序提供 Gold 数据；Lakebase CDF 通过 Unity Catalog 在整个数据生命周期内实现全面治理和血缘追踪，形成闭环。

传统上，将数据从操作数据库迁移意味着需要为每个源到每个目标设置并监控管道。对大多数团队而言，这是一种脆弱、缺乏治理且需要 O(n) 人力投入的工作。

今天，我们正在改变这一方法。Lakebase 现已在公开预览版中提供变更数据馈送（CDF），该馈送存储并治理于 Unity Catalog 托管表中。只需启用一次馈送，即可让所有引擎、模型和 Agent（智能体）直接从中读取。

![只需几次点击即可设置 Lakebase CDF。](/images/posts/a98051100ea6.gif)

## 为什么将操作数据落地到数据湖仍然如此困难？

虽然 Lakeflow Connect 已使数据摄入 Lakehouse 变得简单，但从 OLTP 数据库中提取数据仍然是一个手动且高摩擦的过程。提取变更数据捕获（CDC）迫使团队配置数据库连接器、监控复制状态、缓解性能影响，并通过脱节的工具跟踪错误。这种模式在依赖快速数据分支的 Agent（智能体）优先开发中会崩溃。为每个新分支到每个目标维护复杂且缺乏治理的提取管道是不可持续的。

### 我们在 Lakehouse 中解决了这个问题。现在我们将其引入 Lakebase。

Lakehouse 通过以开放格式（Apache Iceberg™、Delta Lake）一次性存储数据，消除了用于分析目的的提取管道。它确立了变更数据馈送（CDF）作为下游复制的标准，为 ETL、流式工作负载和审计日志提供支持。

![Lakebase CDF 同步行级变更](/images/posts/8686ac82dc08.png)

您现在可以在 Lakebase 上原生设置该 CDF。启用它只需不到一分钟，并适用于项目内的所有表。通过这一单一馈送，您可以使用 SDP 构建流式管道，使用 DBSQL 生成物化视图，或使用 Agent Bricks 计算和存储嵌入/向量。每个下游消费者都订阅完全相同的馈送，与您的主操作工作负载完全隔离。

## 操作数据库属于奖章架构

借助 Lakebase，您的操作数据不再与 Lakehouse 隔离。Lakebase 已提供同步表，确立了直接向应用程序提供 Gold 数据集的模式。Lakebase CDF 完善了该架构。您的操作数据库现在成为原生 Bronze 层，无需单独的管道或提取作业即可将数据落地到 Lakehouse。相反，您可以通过 Unity Catalog 在整个数据生命周期内获得全面的治理和血缘追踪。

这仅仅是个开始。我们正在将您喜爱的 Lakehouse 开放性直接引入 Lakebase。敬请关注 Data and AI Summit，并参加我们关于此架构的分组会议。

### 在您的收件箱中获取最新文章

订阅我们的博客，让最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Announcing Lakebase Change Data Feed (CDF)](https://www.databricks.com/blog/announcing-lakebase-change-data-feed-cdf)
> 
> 翻译时间：2026-05-28 06:11
