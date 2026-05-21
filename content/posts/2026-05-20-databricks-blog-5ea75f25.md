---
title: Lakebase：实现低成本、无缝营销活动的新一代数据库
title_original: Unlock seamless and cost-effective marketing campaigns with Lakebase
date: '2026-05-20'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unlock-seamless-and-cost-effective-marketing-campaigns-lakebase
author: ''
summary: 本文介绍了Databricks推出的Lakebase Postgres无服务器OLTP数据库，它通过存储与计算分离、自动缩放到零等特性，解决了营销活动中数据库资源利用率低、数据同步负担重的问题。文章以与SAP
  Engagement Cloud集成为例，展示了如何利用Lakebase创建弹性、低成本的营销活动后端，实现从Lakehouse到营销平台的无缝数据同步，显著降低运营成本并提升个性化营销效率。
categories:
- AI基础设施
tags:
- Lakebase
- 无服务器数据库
- 营销自动化
- SAP Engagement Cloud
- 成本优化
draft: false
translated_at: '2026-05-21T06:23:21.181288'
---

- Lakebase Postgres 是一款无服务器 OLTP 数据库，可在营销活动高峰期间自动缩减至零，从而消除个性化工作负载中常见的数据库资源利用率不足所带来的成本。
- 原生同步表消除了构建和维护 Lakehouse 到 OLTP 管道的负担，让营销团队只需点击几下即可将新的客户细分群体推送至 SAP Engagement Cloud 等平台。
- 由于 Lakebase 将存储与计算分离，客户属性的广度和深度可以在不线性扩展计算的情况下增长，从而在保持成本平稳的同时实现更丰富的个性化。

最近，Deichmann 发布了一篇客户案例，描述了 Lakebase 如何实现无缝的全渠道营销。本篇博客将介绍该案例的技术层面。

每家零售公司都需要利用数据来交付个性化、高性能的营销活动。然而，我们在整个行业中发现了一些低效之处：

- 公司为利用率不足的数据库资源付费：用于个性化活动的客户细分群体通常存储在 OLTP 数据库中，营销工具从中读取数据。当营销活动启动时，数据库请求会出现峰值，但在其他时间，数据库利用率很低。
- 营销团队不断变化的需求给数据团队增加了运营负担：数据从业者在 Lakehouse 中创建新的客户细分群体，而营销部门的每个新请求都会导致需要创建、维护和监控一系列 Lakehouse 到 OLTP 的同步管道。

Lakebase 是一种全新的开放架构，它结合了事务性数据库的最佳特性以及数据湖的灵活性和经济性。Databricks Lakebase Postgres 是我们对 Lakebase 架构的实现，它解决了这些问题：

- 通过将存储与计算分离，数据可以廉价地存储在对象存储中，而无需线性扩展计算。这意味着客户属性的数量和多样性可以显著增加，而无需额外的计算资源。随着数据增长而数据库流量不增长，Lakebase 的成本仍低于传统 OLTP 数据库。
- 借助弹性、无服务器的 Postgres 计算能力，Lakebase 可根据需求即时扩展，并在空闲时于一秒内缩减。成本与使用量直接挂钩，使其成为计划性营销活动等突发性工作负载的理想选择。Lakebase 客户只需为他们所需的资源付费，从而降低成本，并无需预先规划和配置计算资源。
- 通过与 Lakehouse 无缝集成，Lakebase 与 Lakehouse 之间的同步是完全托管、可靠且高效的，减轻了数据从业者创建和维护管道的负担。

![Lakebase 与 Lakehouse 之间的同步](/images/posts/3a41e43e0512.png)

## 将 Lakebase 与 SAP Engagement Cloud 集成

为了说明使用 Lakebase 作为营销活动平台后端数据库的优势，我们将展示如何将 Lakebase 与全渠道营销平台 SAP Engagement Cloud 集成，并基于之前在 Lakehouse 中创建的客户细分群体启动个性化营销活动。

### 步骤 1：创建并配置新的 Lakebase 项目

我们通过创建一个新的 Lakebase 自动扩缩项目来设置我们的 Postgres 实例。项目是数据库资源的顶级容器。新创建的项目包含一个生产数据库，该数据库将是 SAP Engagement Cloud 连接的 PostgreSQL 实例。

营销活动依赖于基于时间的触发器。当活动被触发时，SAP Engagement Cloud 会查询数据库以检索符合指定条件的潜在客户。这种机制会在较长的低峰期内引发周期性的峰值。因此，对于计算资源，我们在长时间的低峰期内将其缩减至零，以消除这些时段内的计算成本，并将中等容量设置为 16 CU（约 32 GB 内存）作为峰值时的最大值。即使选择的内存范围相对较大，Lakebase 的自动扩缩速度和响应能力也能消除资源利用率不足的风险，从而降低总拥有成本，并减少对数据库进行容量规划和预配置的需求。

![将 Lakebase 与 SAP Engagement Cloud 集成](/images/posts/401b970415aa.gif)

一旦 Lakebase 计算资源设置完毕，我们需要为 SAP Engagement Cloud 创建必要的角色。Lakebase 支持 Databricks 身份的 OAuth 角色和原生 Postgres 密码角色。由于 Engagement Cloud 无法处理 OAuth 角色每小时一次的令牌轮换，我们将使用原生 Postgres 角色。可以通过多种方式创建 Postgres 角色；我们将使用 Lakebase UI 生成一个高熵密码。请立即获取密码并将其存储在密钥管理器中。我们建议通过定期生成新密码来轮换密码。

然后，我们通过在 Lakebase SQL 控制台中运行以下命令，为新创建的 SAP Engagement Cloud Postgres 角色授予对我们用于同步客户细分群体的模式所需的权限。

### 步骤 2：将 SAP Engagement Cloud 连接到 Lakebase

SAP Engagement Cloud 需要 CA 证书才能连接到 PostgreSQL 实例。Lakebase 使用由 Let's Encrypt 颁发的证书，因此所需的根证书是 ISRG Root X1。

我们可以通过以下方式获取根证书：

我们可以检查导出的证书以确认其正确性：

在 SAP Engagement Cloud 中配置新的 PostgreSQL 连接时，当提示输入 CA 证书时，我们将粘贴此文件的内容。

### 步骤 3：将客户细分群体与 Lakebase 同步

创建好连接和角色后，我们可以将客户细分群体从 Lakehouse 同步到 Lakebase。为此，我们需要从要同步的表中创建一个同步表。Databricks 同步表会在 Lakebase 中创建 Unity Catalog 数据的托管副本，使其可供需要 OLTP 风格、低延迟查询的应用程序使用。

有几种同步模式可用：快照模式、触发模式和连续模式。在我们的案例中，并且通常情况下，客户细分群体每晚以批处理方式重新计算，会替换数据集中的很大一部分。当超过 10% 的数据被更新时，我们建议使用快照模式，其性能比触发模式高出 10 倍。然后，会创建一个托管管道，数据随之同步。现在，只需点击几下即可将新的客户细分群体提供给 Engagement Cloud，从而加快上市速度并降低运营负担。

![将客户细分群体与 Lakebase 同步](/images/posts/049f30133205.gif)

此外，由于 Lakebase 实现了计算与存储的分离，可供 Engagement Cloud 使用的数据的大小和多样性可以增长，而无需像传统数据库那样扩展计算资源，从而保持低成本。然而，需要记住的是，Databricks Lakebase 针对高并发点查询和短 OLTP 查询进行了优化，而非大规模扫描或传统 OLAP。

### 将运营数据同步到 Lakehouse

除了生成的客户细分群体之外，营销活动还可以整合来自其他应用程序的数据。例如，客户可能会注册以接收关于特定类别或品牌的产品补货或新品到货的通知。应用程序可以将 Lakebase 用作标准 Postgres 数据库来存储这些通知数据，使其可供 Engagement Cloud 用于活动定向。写入 Lakebase 的任何数据随后都可以通过 Lakehouse Sync（一种从 Lakebase Postgres 到 Unity Catalog Delta 表的原生、基于 CDC 的连续管道）同步到 Lakehouse 进行分析，从而使运营数据可用于更丰富的分析和 AI。

### 性能优化

Lakebase 就是 Postgres，我们可以像优化传统 Postgres 数据库一样优化其性能。

构建索引是最简单、影响最大且最常见的优化手段之一。当营销活动被触发时，SAP Engagement Cloud 会执行查询，通过 WHERE 子句筛选条件来检索客户 ID。

基于此筛选条件创建索引。可以在 Lakebase 中通过 Lakebase SQL 控制台编写语句来创建索引：

对于 SAP Engagement Cloud 而言，索引应已能提供所需的性能。如果需要进一步优化，我们应首先使用 `pg_stat_statements` 或 Databricks Lakebase UI（该界面提供查询性能及一组用于监控数据库的指标）来识别耗时最长且最频繁的查询。

![监控](/images/posts/d5934c35e0eb.gif)

耗时最长且问题最严重的查询可通过以下方式分析：

`PREFETCH` 和 `FILECACHE` 是 Lakebase 特有的指标，分别显示预取请求的发出/命中/浪费次数，以及本地文件缓存（LFC）的命中/未命中情况。Databricks Lakebase UI 还提供了便捷的界面来运行这些分析。

![SQL 编辑器](/images/posts/247aeca6ae1e.png)

在此基础上，我们可以探索其他优化选项，例如：

- 更改 `work_mem` 的配置——对于较大的计算资源，将其提升至 256 MB 可能有益。
- 在高变更率的表上调低 `autovacuum_vacuum_scale_factor`，并通过 `pg_stat_user_tables` 监控膨胀情况。

## 结论

Lakebase 凭借其独特的技术以及与 Lakehouse 的紧密集成，能够为分析和 AI 工作负载创建的客户细分群体提供低延迟服务。

Lakebase 通过积极自动扩缩容并在资源闲置时缩容至零，大幅降低了总拥有成本（TCO），消除了闲置资源的成本。

Lakebase 与 Lakehouse 的集成消除了维护同步管道的运营负担，缩短了新客户细分群体的上市时间，并支持更个性化的营销活动，从而在更短时间内提升用户参与度。

准备好升级你的营销技术栈了吗？立即试用 Databricks Lakebase Postgres，了解无服务器 OLTP 与 Lakehouse 的结合如何降低 TCO 并加速活动交付。请访问 Databricks Lakebase 产品页面，阅读 Deichmann 客户案例，或联系你的 Databricks 客户团队，为你的营销活动工作负载定制概念验证方案。

---

> 本文由AI自动翻译，原文链接：[Unlock seamless and cost-effective marketing campaigns with Lakebase](https://www.databricks.com/blog/unlock-seamless-and-cost-effective-marketing-campaigns-lakebase)
> 
> 翻译时间：2026-05-21 06:23
