---
title: SAP语义元数据同步至Databricks，赋能AI就绪数据
title_original: Unlocking SAP Business Context in Databricks with Semantic Metadata
  Delta Sharing
date: '2026-04-30'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing
author: ''
summary: SAP Business Data Cloud与Databricks Unity Catalog实现语义元数据自动同步，包括业务友好的表名、列描述及主外键关系，使SAP数据在Databricks中更易理解和发现。该功能基于Delta
  Sharing，无需手动丰富数据字典，并自动应用个人数据治理标签，支持细粒度访问控制。丰富的语义上下文显著提升AI Agent和数据分析的准确性，助力AI辅助数据工程与自然语言查询。
categories:
- AI基础设施
tags:
- SAP
- Databricks
- 语义元数据
- Delta Sharing
- 数据治理
draft: false
translated_at: '2026-05-01T05:46:17.493621'
---

- SAP Business Data Cloud 现在会自动将语义元数据同步到 Unity Catalog 中——包括描述以及主键/外键关系。
- SAP 数据即刻具备 AI 就绪状态，在 Databricks 中更易于理解和发现，无需手动丰富。
- SAP 个人数据治理标签现在会自动在 Unity Catalog 中可用，支持基于 ABAC 的细粒度访问控制。

## SAP 数据功能强大，但彼此关联可能较为困难

任何处理过 SAP 数据的人都了解这一挑战：像 <VBAK> 这样的表名和像 <KUNNR> 这样的列名在技术上是精确的，但彼此关联可能较为困难。数据工程师花费大量时间将这些标识符映射到业务含义，而这些工作通常存在于电子表格、内部文档或隐性知识中——远离数据本身。

通过 Databricks 与 SAP 的合作，我们着手改变这一现状。

## 自动同步语义元数据

![SAP Business Data Cloud](/images/posts/c3f2e2766436.gif)

我们很高兴地宣布，SAP Business Data Cloud 与 Databricks Unity Catalog 之间的语义元数据同步现已全面可用。对于所有挂载的 SAP BDC Delta Shares，当表被访问时，语义元数据现在会自动在表级别共享到 Unity Catalog 中，使 SAP 数据更易于理解和发现。在 SAP BDC 中所做的任何更改都会反映在 Unity Catalog 中——SAP BDC 仍然是语义元数据的单一事实来源。这意味着，当数据从业者或 AI Agent（智能体）在 Databricks 中遇到 SAP 表时，他们看到的是对业务友好的显示名称、描述和上下文——而不仅仅是原始的 SAP 标识符。无需手动数据字典。无需与 SAP 管理员反复沟通。

这一新功能建立在 SAP Business Data Cloud Connect to Databricks（BDC Connect）之上，该功能允许 SAP 团队通过 Delta Sharing 将受治理的 SAP 数据产品发布到 Databricks 平台。通过将这些数据产品中的语义元数据和治理标签同步到 Unity Catalog 中，Databricks 用户可以更轻松地发现、组合和操作 SAP 数据产品，并将其与其他企业数据源结合用于分析和 AI，而无需在单独系统中重新创建业务上下文或治理。

## 这对 AI 为何重要

其价值超越了人类可读性。随着组织在 SAP 数据之上构建 AI Agent（智能体）和分析应用程序，丰富的语义上下文正是区分有用 Agent（智能体）与混乱 Agent（智能体）的关键。没有 SAP 内置的领域逻辑，AI 输出将缺乏关键的业务上下文——从而降低准确性和相关性。语义元数据恰好解决了这一问题，将 AI 建立在 SAP 数十年来在企业运营中编码的业务含义之上。

这种元数据同步最显著的好处之一是其对 AI 辅助数据工程的影响。通过引入列描述和表关系（如主键和外键），我们为 Databricks AI Assistant 和 AI/BI Genie 的蓬勃发展提供了必要的上下文。

AI 模型不再需要猜测像 VBAK 这样的表如何与 VBAP 关联，Unity Catalog 提供了明确的语义映射。这使得用户可以提出自然语言问题——例如“表 SalesOrder 和 SalesOrderItem 之间是什么关系？”——并立即获得准确的、可直接用于连接的查询，因为 AI 终于“说”了你的 SAP 数据的“语言”。

![Databricks AI Assistant](/images/posts/dfee441d8740.gif)

## 包含治理标签

SAP BDC 还会将 PersonalData 命名空间中的治理标签作为系统治理标签同步到 Unity Catalog 中的表上——自动应用团队在合规性、访问控制和负责任 AI 方面所需的数据分类信号。无需手动标记。

## 了解更多

Delta Sharing Connector for SAP：https://learn.microsoft.com/en-us/azure/databricks/delta-sharing/sap-bdc/semantic-metadatahttps://docs.databricks.com/aws/en/delta-sharing/sap-bdc/semantic-metadatahttps://docs.databricks.com/gcp/en/delta-sharing/sap-bdc/semantic-metadata

SAP Databricks：https://docs.databricks.com/sap/en/share-data#sap-bdc-semantic-metadata

准备好优化您的工作流程了吗？立即在您的 Databricks 环境中试用 SAP 语义元数据。

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Unlocking SAP Business Context in Databricks with Semantic Metadata Delta Sharing](https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing)
> 
> 翻译时间：2026-05-01 05:46
