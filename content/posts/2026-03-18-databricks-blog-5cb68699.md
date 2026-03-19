---
title: FabCon 2026：Azure Databricks发布Lakebase、Lakeflow与Genie新功能
title_original: 'What’s New in Azure Databricks at FabCon 2026: Lakebase, Lakeflow,
  and Genie'
date: '2026-03-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/whats-new-azure-databricks-fabcon-2026-lakebase-lakeflow-and-genie
author: ''
summary: 在Microsoft Fabric Community Conference 2026上，Azure Databricks宣布了多项重要更新。Lakeflow
  Connect推出免费层，支持每日免费摄取约1亿条记录，简化企业数据入湖流程。Lakebase全面上市，作为面向AI Agent的运营数据库，将Postgres能力与湖仓存储结合，为智能代理提供状态管理基础。这些更新旨在加速企业在Azure上构建统一的数据与人工智能平台，提升数据工程和AI应用开发效率。
categories:
- AI基础设施
tags:
- Azure Databricks
- 数据湖仓
- AI Agent
- 数据工程
- 微软云
draft: false
translated_at: '2026-03-19T04:58:12.086876'
---

## 加速 Azure 上的数据与人工智能

本周，数千名数据专业人士齐聚亚特兰大，参加 **Microsoft Fabric Community Conference (FabCon) 2026**——这是首次与 **SQLCon** 联合举办——将微软数据和 SQL 社区汇聚一堂，共同探索 Azure 上分析、商业智能和人工智能的未来。

对于 Azure Databricks 而言，FabCon 凸显了我们与微软合作伙伴关系的持续发展势头，以及客户如何利用 Azure Databricks 来统一数据工程、分析、商业智能和人工智能。

自 2017 年以来，Azure Databricks 一直是 Azure 的一级服务，与包括 Power BI、Excel、Microsoft Teams、Data Factory、Azure OpenAI、Microsoft Foundry、Copilot Studio 和 Power Platform 在内的微软服务深度集成。

各行各业的公司都依赖 Azure Databricks，在开放的湖仓一体架构上构建现代数据平台，将开放数据的灵活性与分析和人工智能所需的性能和规模相结合。

在本周的 FabCon 上，我们推出了多项新功能，旨在让在 Azure 上构建智能应用变得更加容易。

## Lakeflow Connect 免费层

可靠的数据摄取是现代分析和人工智能的基础。

今天，我们很高兴推出 **Lakeflow Connect 免费层**，让各组织能够轻松地将其企业数据引入湖仓，以构建分析和人工智能应用。

**Lakeflow Connect** 让您能够将企业 SaaS 应用和数据库中的数据直接镜像到湖仓中。每个工作区每天包含 **100 个免费 DBU**，允许您在 **标准 Lakeflow Connect 定价** 生效前，每天免费将大约 **1 亿条记录** 摄取到每个工作区的湖仓中。此免费层包含 Lakeflow Connect 的所有优势，包括简单的用户界面、高效的摄取以及通过 Unity Catalog 实现的统一治理。

主要功能包括：

*   支持对九种最常用的数据库进行数据库镜像（SQL Server、Oracle、Teradata、PostgreSQL、MySQL、Snowflake、Redshift、Synapse 和 BigQuery）
*   全面支持许多最受欢迎的 SaaS 应用（包括 Dynamics 365、Salesforce、ServiceNow、Workday 和 Google Analytics）

Lakeflow Connect 直接写入 **Azure Data Lake Storage (ADLS)** 上的开放存储，并由 Unity Catalog 治理。您摄取的数据在落地的那一刻起就是安全、可发现且可从任何引擎访问的。

结合 Lakeflow 的编排和转换能力，Azure Databricks 提供了一个用于构建生产数据管道的完整平台——使团队能够以 **高达 25 倍的速度** 构建管道，同时将 ETL 成本降低 **高达 83%**。

详细了解 **Azure Databricks 上的 Lakeflow** 如何在单一治理平台上统一摄取、转换和编排。

## Azure Databricks Lakebase：面向 AI Agent 的数据库，现已全面上市

现代应用越来越需要能与分析和人工智能无缝集成的运营数据库。在 AI Agent 时代，这一点更为关键：Agent 需要一个事务性的记录系统来管理状态、操作和应用工作流。

现已全面上市的 **Azure Databricks Lakebase** 是一项托管的、无服务器的 Postgres 服务，它将生产级的运营能力直接带到您在 Azure 上的湖仓基础之上。**Lakebase 是 Agent 时代的运营数据库**，使 AI Agent 和应用能够直接在湖仓中对运营数据进行读取、写入和推理。

Lakebase 将熟悉的 Postgres 与开放湖仓存储的可扩展性和经济性相结合。随着各组织采用由 **Genie** 和 **Agent Bricks** 等工具驱动的 Agent 工作流，**Lakebase 提供了 Agent 所依赖的运营数据库层**，用于管理状态和应用工作流。这一基础也借助 **Genie Code** 等工具，催生了新一轮的 Agent 数据工程和 Agent 数据科学。

*   **开放的 Postgres 基础**，支持社区扩展，如 pgvector 和 PostGIS
*   **分离的计算与存储**，实现高吞吐量和高效扩展
*   **亚秒级启动，支持自动扩缩容和缩容至零定价**
*   **分支和即时恢复**，用于开发工作流
*   **跨可用区的高可用性与自动故障转移**

随着此次发布，Lakebase 现已在 **全球 14 个 Azure 区域** 上市，使各组织能够直接在 Databricks 平台上运行运营工作负载。

常见用例包括：

*   运营应用和工作流系统
*   AI Agent 状态管理
*   客户个性化和特征服务
*   运营数据的事务性分析

## 将 Azure Databricks 扩展至 Microsoft 365

许多业务决策仍然发生在 **Excel 和 Teams** 等熟悉的工具中。本周发布的一个关键重点是将 Azure Databricks 扩展至 Microsoft 365，以便在用户已经工作的环境中提供受治理的数据和人工智能洞察。

这建立在之前宣布的 Azure Databricks 与 Microsoft 365 集成的基础上，包括对 **支持 Genie 的 Copilot Studio Agent** 的支持——允许员工直接在 Teams 或 M365 Copilot 中从 Genie 获取可信洞察——以及即将推出的计划，例如 Teams 中的 Databricks 应用，可直接访问 Genie。

![](/images/posts/86c202082b84.gif)

**Azure Databricks Excel 加载项（公开预览版）**

**Azure Databricks Excel 加载项** 将 Excel 直接连接到受治理的湖仓数据。

用户可以：

*   直接从 Excel **浏览 Unity Catalog 表和指标视图**
*   使用 **指标视图和受治理的语义定义** 构建数据透视表
*   无需编写 SQL 即可筛选和分析数据

该加载项适用于 **Windows、macOS 和网页版 Excel**，帮助组织用直接访问可信湖仓数据的方式取代脆弱的导出操作。

要了解更多信息，请查阅 **文档**。

![](/images/posts/f22de14fba7a.gif)

## Genie：了解您业务的 AI

Azure Databricks 上基于人工智能的分析采用率快速增长，98% 的 Databricks SQL 仓库客户使用 AI/商业智能，Genie 月活跃用户同比增长超过 300%。

这一体验的核心是 **Genie**，它使用户能够就其数据提出问题，并以表格、图表或自然语言解释的形式获得答案。

**Genie** 是 Databricks 中面向数据的对话式人工智能体验，而 **Genie Code** 将这些能力扩展到构建管道、机器学习模型、商业智能仪表板和应用的程序员。

**Genie Agent 模式**

对于复杂的分析问题，**Genie Agent 模式** 引入了一种面向业务分析的 Agent 方法。

Agent 模式使用 **多步推理和假设检验** 来调查复杂问题，并从企业数据中发掘更深层次的洞察。Genie 不是返回单一的查询结果，而是可以迭代地探索问题，并根据中间结果学习来优化其方法。Genie Agent 模式使用户能够超越基本的“发生了什么”问题，去理解“为什么”和“接下来会怎样”。

借助 Genie Agent 模式，用户可以：

*   自动生成并执行跨多个查询的研究计划
*   检验假设并根据中间发现优化分析
*   将结构化数据探索与叙述性解释和可视化相结合
*   提供由表格、图表和证据支持的全面答案

这将 Genie 从一个简单的对话式查询界面转变为一个 **能够调查复杂业务问题的 AI 分析师**。

**Genie Code**

对于数据从业者，**Genie Code** 支持直接在 Databricks 工作区中进行 Agent 数据工程、数据科学和分析工作流。

Genie Code 是专为数据团队构建的 AI Agent。它通过 **Unity Catalog** 理解企业数据上下文，使其能够在直接在笔记本、SQL 编辑器和 Lakeflow 管道中工作时，对数据集、血缘、治理策略和业务语义进行推理。

Genie Code 为构建和运营数据管道、分析与人工智能应用提供统一的智能体开发体验。

借助 Genie Code，团队能够：

- 通过自然语言提示词构建并扩展数据管道、仪表板和机器学习工作流
- 跨 Lakeflow 管道与模型调试故障并调查异常情况
- 基于企业数据上下文生成笔记本、SQL 查询和可视化图表
- 自动化管道监控与故障排除等日常运维工作

通过深度融合平台集成与多步推理能力，Genie Code 使数据团队能够超越辅助编码，将复杂数据任务委托给 AI 协作伙伴。

![](/images/posts/0e9fb1ef1171.jpg)

**Databricks One 中的 Genie**

Databricks One 现已集成由 Genie 驱动的统一多智能体对话体验，让业务用户能够以简单方式跨整个数据资产提出问题。用户可无缝访问并整合来自多个 Genie 空间的数据洞察，无需了解数据存储位置或选择哪个空间。当问题超出既有 Genie 空间范围时，Databricks One 可调用额外智能体探索数据并生成新答案。这使得用户能在单一体验中处理明确定义的问题与即时生成的问题。

除对话功能外，用户还可在专为普及数据与 AI 而设计的流线型界面中搜索数据、探索 AI/BI 仪表板并与 Databricks 应用交互。

**Databricks One 移动端**

Databricks One 移动端将全新的 Genie 多智能体对话体验延伸至 iOS 与 Android 平台，使业务用户能够随时随地安全访问并交互处理数据。

通过 Databricks One 移动端，用户可在手机上向 Genie 提问、探索 AI/BI 仪表板并访问 Databricks 应用。这为业务用户提供了一种在移动中分析数据并制定决策的便捷方式。

![](/images/posts/4388cbb82018.gif)

## 为何 Azure Databricks 是 Azure 上最佳的数据与 AI 平台

这些新功能的发布基于 Azure Databricks 的核心优势，使其成为 Azure 上数据与 AI 领域的首选平台。

**统一治理**

Unity Catalog 集中管理表、文件、模型、仪表板及 AI 资产的治理策略。

**深度微软集成**

Azure Databricks 原生集成 Power BI、Excel、Teams、Azure OpenAI 及其他微软服务。

**湖仓一体原生分析**

Databricks SQL 直接在开放的湖仓存储上提供高性能分析能力。

**AI 开发**

Genie 与 Agent Bricks 为构建和部署 AI 应用提供统一平台。

**降低总体拥有成本**

无服务器计算、Lakebase 零弹性伸缩与简化数据摄入功能降低了基础设施复杂度与成本。

## 在 FabCon 亲睹创新成果

若您将参加亚特兰大举办的 **FabCon 2026**，欢迎莅临现场体验这些创新技术。Databricks 团队将在整周展会期间演示各组织如何运用 Azure Databricks 构建现代数据与 AI 应用。您也可**加入我们的专题会议**（3月19日周四上午8:00–9:00，C302会议室）了解这些功能如何协同提升性能、简化架构并最大化 Azure 平台价值。

- 在 FabCon，您可以：观看 Azure Databricks Lakebase、Lakeflow Connect、Genie、AI/BI 等功能的现场演示
- 与 Databricks 专家探讨如何在 Azure 上统一数据工程、BI 与 AI
- 了解客户如何集成 Azure Databricks、Power BI 与 Azure OpenAI

会议期间，我们还将与微软生态系统的合作伙伴共同举办社区活动。欢迎参加3月18日周三与 Slalom 联合举办的 FabCon 交流酒会，与微软及 Databricks 社区的数据领导者与实践者建立联系：

FabCon 与 Slalom 交流酒会 → https://go.slalom.com/MSFT-FabCon26

同时请标记您的日历：**Databricks 数据 + AI 峰会**将于2026年6月15–18日在旧金山举行——这场全球规模最大的数据、分析与 AI 专题会议将汇聚 **25,000+** 参会者，举办 **800+** 场专题会议及 Databricks 平台实操培训。

Azure 上数据与 AI 的未来已来——而这仅仅是个开始！

免费开始使用 Azure Databricks →

---

> 本文由AI自动翻译，原文链接：[What’s New in Azure Databricks at FabCon 2026: Lakebase, Lakeflow, and Genie](https://www.databricks.com/blog/whats-new-azure-databricks-fabcon-2026-lakebase-lakeflow-and-genie)
> 
> 翻译时间：2026-03-19 04:58
