---
title: Azure Databricks Lakebase正式发布：统一运营与分析数据
title_original: Azure Databricks Lakebase is Generally Available
date: '2026-03-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/azure-databricks-lakebase-generally-available
author: ''
summary: 微软正式发布Azure Databricks Lakebase，这是一种专为Azure优化的托管无服务器PostgreSQL服务。它通过计算与存储分离的架构，将运营数据直接写入湖仓存储，打破了事务系统与分析系统之间的壁垒。Lakebase提供无服务器自动扩缩、即时数据分支克隆、标准PostgreSQL兼容性，并通过Unity
  Catalog实现统一治理。该服务旨在简化数据架构，消除复杂ETL管道，降低数据重复和延迟，为开发AI智能体、实时特征服务等下一代应用提供统一的数据基础。
categories:
- AI基础设施
tags:
- Azure
- Databricks
- 数据库
- 数据湖仓
- PostgreSQL
draft: false
translated_at: '2026-03-04T04:47:19.249417'
---

多年来，一道数据高墙将应用开发领域与分析领域分隔开来。开发人员被迫构建脆弱的ETL管道来弥合这一鸿沟，仅仅是为了将数据从运营中的PostgreSQL实例迁移到数据湖。这种割裂不仅拖慢了交付速度，更造成了存储重复的"数据税"，并导致现实状况与数据洞察之间存在持续滞后。

今天，我们正通过发布Azure Databricks Lakebase的正式版（GA）来推倒这堵高墙，这也是微软宣布的一个重要里程碑。

Lakebase是专为Azure上的Databricks平台优化的托管式无服务器PostgreSQL。它引入了一种全新的数据库架构类别，将计算与存储分离，使您能够将运营数据直接写入湖仓存储。通过融合事务系统与分析系统之间的隔阂，Azure Databricks Lakebase为统一数据架构提供了最后一块拼图。Lakebase是微软生态系统中的第一方服务，旨在补充您现有的Azure投资，同时显著提升开发人员的工作效率。借助即时分支和零拷贝克隆等功能，团队现在可以基于生产级数据进行迭代，而无需受制于传统上阻碍创新的基础设施延迟。

## 为什么选择Lakebase？面向现代应用的数据库

传统云数据库如同孤岛，而Lakebase则原生集成于Azure生态系统。由于Lakebase与湖仓共享相同的存储层，您无需再担心构建和维护复杂的数据管道，也无需担心数据作业不同步。您还可以在不影响运营工作负载性能的情况下，从运营数据库系统中获取洞察。

### 具备自动扩缩容和缩容至零能力的无服务器效率

Lakebase以无服务器模式的效率，提供企业级的PostgreSQL体验。该平台可自动扩展以处理繁重的应用流量，并在空闲时缩容至零，确保您的计算资源与实际需求相匹配。这种基于使用量的定价模式确保了最低的总拥有成本（TCO），因为您只需为实际使用的计算付费，而Azure则负责管理底层基础设施和可用性。

### 通过分支和恢复实现开发敏捷性

现代开发需要智能体的速度与安全性。Lakebase支持即时克隆和数据分支，允许团队在几秒钟内创建生产数据的零拷贝分支。这使您可以在安全、隔离的环境中测试模式迁移或调试查询，而不会影响实时用户。为了增强弹性，Lakebase包含即时时间点恢复（PITR），允许您立即将数据库恢复到精确的时间点，以便从错误或事件中恢复。

### 标准PostgreSQL与开放生态系统

Lakebase基于标准PostgreSQL构建，确保与您已使用的工具和库完全兼容。它支持数十种流行的扩展，包括用于AI驱动搜索的pgvector和用于高级地理空间分析的PostGIS。通过支持标准PostgreSQL生态系统，Lakebase确保开发人员能够利用最新的开源创新，而Azure则负责处理安全、身份和网络需求。

### 通过Unity Catalog实现统一治理

安全不应在不同的数据库引擎间割裂。使用Lakebase，您的运营数据将与分析和AI工作负载同处于Unity Catalog的统一管理之下。这为整个Azure Databricks数据资产提供了一个单一的治理模型，实现一致的访问控制、自动化的数据血缘和企业级审计。

## 赋能AI智能体

通过统一数据库和湖仓，Lakebase为构建下一代智能软件的开发人员解锁了新的场景：

-   **AI智能体记忆与状态**：在高性能、受治理的环境中存储智能体对话历史和工具日志。智能体可以像访问生产数据库一样可靠地获取实时运营上下文。
-   **基于pgvector的向量驱动上下文**：由于完全支持pgvector，开发人员可以构建RAG（检索增强生成）工作流，直接利用来自运营源的最新数据。
-   **低延迟特征服务**：将Lakebase用作特征存储的高性能在线存储。这确保了机器学习模型能够立即访问最新特征以进行实时推理，而无需管理单独的服务基础设施的复杂性。
-   **使用同步表的运营分析**：通过使用同步表，此架构确保您的模型训练和BI仪表板更新所使用的数据，与应用程序实时生成的数据完全一致。这消除了手动管道连接的需要，减少了数据重复，并使您的运营上下文和历史上下文保持完美同步。

## 基于Azure的企业级信任构建

Azure Databricks Lakebase让开发人员可以继续使用熟悉的工具和库，如pgAdmin、DBeaver和PostgREST API，而Azure则负责处理安全、身份、网络和合规性。通过与Microsoft Entra ID和Azure网络保护集成，Lakebase加速了应用程序交付，同时简化了底层的DevOps负担。

## 立即开始使用

Azure Databricks Lakebase的正式发布为现代数据系统的速度和复杂性提供了新的基础。对于Azure客户而言，这是在湖仓基础上直接构建智能、实时应用程序的最简单途径。

准备好构建了吗？Azure Databricks Lakebase已集成到Azure Databricks体验中，可以直接在您的工作区中进行配置。立即创建您的第一个项目，看看推倒应用与分析之间的高墙如何能加速您的创新。

免费开始使用Azure Databricks →

## 下一步是什么？

---

> 本文由AI自动翻译，原文链接：[Azure Databricks Lakebase is Generally Available](https://www.databricks.com/blog/azure-databricks-lakebase-generally-available)
> 
> 翻译时间：2026-03-04 04:47
