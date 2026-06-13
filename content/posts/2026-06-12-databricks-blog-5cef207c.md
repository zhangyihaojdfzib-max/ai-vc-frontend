---
title: 无需迁移，用自然语言查询所有数据
title_original: Talk to all your data, wherever it lives
date: '2026-06-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/talk-all-your-data-wherever-it-lives
author: ''
summary: 本文介绍了Databricks的Lakehouse Federation与Genie功能，允许企业直接连接并查询分布在AWS Glue、Snowflake、Oracle等多个系统中的数据，无需进行耗时的数据迁移。通过Unity
  Catalog统一治理层，联邦数据与托管数据共享权限、沿袭和访问控制，同时支持继承源系统的元数据注释。用户可在联邦表上定义业务指标（如ROI），使Genie等AI工具能理解并回答自然语言问题，实现跨源即时洞察。
categories:
- AI产品
tags:
- Lakehouse Federation
- Unity Catalog
- 自然语言查询
- 数据联邦
- Genie
draft: false
translated_at: '2026-06-13T06:20:42.504094'
---

*使用 Lakehouse Federation 将 Genie 连接到数据，避免“大爆炸”式迁移的延迟。*利用 Unity Catalog 作为联邦数据与托管数据的唯一真实来源，确保 AI 工作负载安全且可用于生产环境。*立即开始用自然语言查询数据。通过升级到 Unity Catalog 托管表来优化性能。

Agentic AI 创造了 12 个月前不存在的跨源推理需求。业务用户希望提出自然语言问题，例如“哪些营销活动在上个季度带来了最高的 ROI？”，并从数据中即时获得洞察。

问题在于，企业数据通常分布在多个系统中，例如 AWS Glue、Snowflake、Oracle、BigQuery、Postgres，有时还被锁定在传统的专有格式中，将所有数据迁移到单一系统可能需要数月时间。

如果无需迁移数据，却仍能对整个数据资产进行推理，会怎样？借助 Lakehouse Federation，Databricks 可直接连接到您现有的数据源（无论它们位于何处），并将其纳入 Unity Catalog 的单一治理层。权限、数据沿袭和访问控制在每个连接的系统中保持一致，因此您无需逐个重建数据源即可获得企业级安全性。业务用户随后可以通过 Genie 用纯英文查询这些统一数据，获得跨越所有连接平台的答案，而无需任何管道、复制或迁移步骤。

在本博客中，我们将逐步介绍如何通过连接到外部源、将其元数据同步到 Unity Catalog，并通过 Genie 提问来完成设置——所有这些只需几分钟。

## 工作原理

Lakehouse Federation 允许用户和 AI Agent 安全地连接到外部源，并与您的原生数据一起进行治理。这使得 Genie 能够即时访问您扩展的数据资产，而无需进行迁移。Lakehouse Federation 可连接到超过 20 种最流行的数据平台。作为示例，让我们看看如何轻松地使用 AWS Glue 进行设置。

![跨所有数据的 Genie](/images/posts/692464bea524.png)

### 1. 使用 Lakehouse Federation 连接到外部数据源

首先，我们创建一个到外部 AWS Glue 项目的连接。在此示例中，我们连接到一个包含营销活动数据的 Glue 数据库。

接下来，我们将数据原地同步到 Unity Catalog。这提供了对所有表的访问权限，而无需复制任何数据，确保数据始终是最新的。同时，这也避免了对源系统的任何干扰。

### 2. 利用现有元数据

原始的表名和列名对 AI 模型来说通常毫无意义。AI Agent 不会天生就知道 `status_code 4` 表示“紧急”，或者 `spend_amount` 指的是营销成本。

许多组织已经投入资源在源系统中记录其模式——直接在 Glue 中添加表描述、列注释和业务术语表。Lakehouse Federation 现在会自动引入这些上下文。当您创建外部目录时，源系统中的注释和描述会与表元数据一起被联邦到 Unity Catalog 中。

这意味着：

- 现有的列描述（例如，“spend_amount — 以美元计的总营销支出”）无需手动重新输入即可继承
- 记录业务上下文的表级注释得以保留
- 像 Genie 这样的 AI 工具可以立即利用这些元数据来理解您的模式

目前，我们支持 Glue 和 BigQuery 上的外部表注释。在预览版中，我们已扩展支持 PostgreSQL、Redshift、MySQL、Snowflake，并计划每月增加更多数据源（注册预览版）。

### 3. 在联邦数据之上定义可复用的语义

继承的注释告诉 Genie 您的数据是什么，但它们无法捕捉您的业务如何衡量事物。列注释可以解释 `spend_amount` 是以美元计的营销成本，但只有指标定义才能编码出 ROI 是展示次数除以支出。这是业务逻辑，历史上它分散在仪表板公式、临时 SQL 和隐性知识中，并且不同团队的定义往往存在细微差异。

Unity Catalog Semantics 允许您将该业务逻辑定义一次，作为一个受治理的对象，这样每个查询它的工具都能获得相同的可信计算。由于联邦表是 Unity Catalog 中的一等公民，这适用于从未离开其源系统的数据。您可以直接在任何联邦源上定义像 ROI 这样的指标，无需迁移。

使用 Unity Catalog 指标，您可以直接在联邦表上定义一次。指标视图定义了两件事：用户可以分组和筛选的字段（如 `campaign_id` 和 `quarter`），以及一个度量 `roi`，它编码了业务公式本身。

定义 ROI 一次，Genie、AI/BI 仪表板和笔记本都将以相同的方式计算它。当定义发生变化时，您只需在一个地方更新，所有消费者都会继承该更改。

### 4. 询问 Genie

数据连接并上下文化后，您的营销分析师现在可以打开一个 Genie 房间，并问出我们开头的问题：“哪些营销活动在上个季度带来了最高的 ROI？”

Genie 无需从头重建 ROI 公式——它会解析指标视图中经过认证的 `roi` 度量，并自动针对联邦数据生成正确的 SQL。

![](/images/posts/d99dac5351c7.gif)

结果如何？一个基于 Glue 中实时数据得出的即时、准确的答案。

由 Lakehouse Federation 驱动的 Genie，只是 Unity Catalog 如何在整个数据资产中实现 AI 洞察的一个例子。无论查询来自 Genie 房间的业务分析师，还是由 Agent 驱动的工作流，Unity Catalog 都提供了受治理、上下文化的坚实基础，使其得以运作。

## 下一步计划

我们将继续投资，使 Lakehouse Federation 成为接入 Databricks 平台的最快途径：

- **更丰富的联邦表业务语义**：除了导入现有注释，我们正在构建新的方法，通过 AI 驱动的描述和业务上下文来增强您的联邦元数据——使 Genie 开箱即用更加智能。
- **通过升级到托管表提升性能**：使用 `SET MANAGED` 功能将外部表转换为 Databricks 中的 Unity Catalog 托管表，可享受 **50% 以上的成本节省和 20 倍的查询速度提升**。
- **支持更多目录和平台的联邦**：我们持续添加新的联邦数据源，为您提供对更多数据资产的受治理访问。

## 开始使用

- 阅读 Lakehouse Federation 文档了解更多（[AWS](https://docs.databricks.com/en/data-sharing/lakehouse-federation/index.html)、[Azure](https://learn.microsoft.com/en-us/azure/databricks/data-sharing/lakehouse-federation/)、[GCP](https://docs.gcp.databricks.com/en/data-sharing/lakehouse-federation/index.html)）
- 开始免费试用 Databricks

---

> 本文由AI自动翻译，原文链接：[Talk to all your data, wherever it lives](https://www.databricks.com/blog/talk-all-your-data-wherever-it-lives)
> 
> 翻译时间：2026-06-13 06:20
