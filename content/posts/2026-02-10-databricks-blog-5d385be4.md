---
title: 基于Lakeflow与Azure Databricks的现代化数据工程平台
title_original: Modernize your Data Engineering Platform with Lakeflow on Azure Databricks
date: '2026-02-10'
source: Databricks Blog
source_url: https://www.databricks.com/blog/modernize-your-data-engineering-platform-lakeflow-azure-databricks
author: ''
summary: 本文介绍了如何利用Azure Databricks上的Lakeflow平台解决数据工程团队面临的工具割裂、效率低下和治理缺失等挑战。Lakeflow提供端到端的统一解决方案，集成了数据摄取、声明式ETL转换、工作流编排及原生治理功能，通过内置连接器、Spark声明式流水线和数据优先的编排器，帮助团队在单一平台上高效构建可靠的数据流水线，提升开发速度与数据可信度。
categories:
- AI基础设施
tags:
- 数据工程
- Azure Databricks
- Lakeflow
- ETL
- 数据治理
draft: false
translated_at: '2026-02-13T04:34:03.642916'
---

数据工程师对构建生产就绪流水线所需的大量割裂工具和解决方案日益感到沮丧。缺乏集中的数据智能平台或统一治理，团队面临诸多问题，包括：

- 效率低下和启动缓慢
- 割裂的用户界面和频繁的上下文切换
- 缺乏细粒度安全性和控制
- 复杂的CI/CD
- 有限的数据血缘可见性
- 等等

结果如何？团队效率降低，对数据的信任度下降。

借助Azure Databricks上的Lakeflow，您可以通过将所有数据工程工作集中在一个原生的Azure平台上来解决这些问题。

![](/images/posts/df0d72f688f6.png)

## 面向Azure Databricks的统一数据工程解决方案

Lakeflow是一个端到端的现代数据工程解决方案，构建于Azure上的Databricks数据智能平台，集成了所有核心数据工程功能。使用Lakeflow，您将获得：

- 内置的数据摄取、转换和编排，集于一处
- 托管的摄取连接器
- 声明式ETL，实现更快、更简单的开发
- 增量和流处理，以实现更快的SLA和更及时的洞察
- 通过Unity Catalog（Databricks的集成治理解决方案）实现原生治理和血缘
- 内置的数据质量和流水线可靠性可观测性

还有更多！所有这些都通过一个灵活、模块化的界面提供，可以满足所有用户的需求，无论他们喜欢编码还是使用点击式界面。

## 在一处摄取、转换和编排所有工作负载

Lakeflow统一了数据工程体验，让您能够更快、更可靠地推进工作。

### 使用Lakeflow Connect实现简单高效的数据摄取

您可以从使用Lakeflow Connect轻松地将数据摄取到平台开始，通过点击式界面或简单的API即可实现。

您可以将来自广泛支持来源的结构化和非结构化数据摄取到Azure Databricks中，包括流行的SaaS应用程序（例如Salesforce、Workday、ServiceNow）、数据库（例如SQL Server）、云存储、消息总线等。Lakeflow Connect还支持Azure网络模式，例如Private Link以及在VNet中为数据库部署摄取网关。

对于实时摄取，请查看Zerobus Ingest，这是Azure Databricks上Lakeflow中的无服务器直写API。它将事件数据直接推送到数据平台，无需消息总线，从而实现更简单、更低延迟的摄取。

![](/images/posts/05284f0d1c93.png)

### 使用Spark声明式流水线轻松构建可靠的数据流水线

利用Lakeflow Spark声明式流水线（SDP），轻松按照业务需求清理、塑形和转换数据。

SDP让您仅用几行Python（或SQL）代码即可构建可靠的批处理和流式ETL。只需声明您需要的转换，SDP会处理其余一切——包括依赖映射、部署基础设施和数据质量。

SDP最大限度地减少了开发时间和运维开销，同时开箱即用地编码了数据工程最佳实践，使得仅通过几行代码即可轻松实现增量处理或复杂模式（如SCD类型1和2）。这是Spark Structured Streaming的全部能力，变得异常简单。

由于Lakeflow已集成到Azure Databricks中，您可以使用Azure Databricks工具，包括Databricks Asset Bundles（DABs）、Lakehouse Monitoring等，在几分钟内部署生产就绪的、受治理的流水线。

![](/images/posts/4ce8897d20a0.png)

### 使用Lakeflow Jobs实现现代数据优先编排

使用Lakeflow Jobs在Azure Databricks上编排您的数据和AI工作负载。凭借现代化、简化的数据优先方法，Lakeflow Jobs是Databricks最值得信赖的编排器，支持大规模数据和AI处理以及实时分析，可靠性达99.9%。

在Lakeflow Jobs中，您可以通过将SQL工作负载、Python代码、仪表板、流水线和外部系统协调到一个统一的DAG中，来可视化所有依赖关系。工作流执行简单灵活，支持数据感知触发器（如表更新或文件到达）和控制流任务。得益于无代码回填运行和内置可观测性，Lakeflow Jobs让您轻松保持下游数据的新鲜、可访问和准确。

作为Azure Databricks用户，您还可以使用Lakeflow Jobs中的Power BI任务自动更新和刷新Power BI语义模型（在此处阅读更多信息），使Lakeflow Jobs成为Azure工作负载的无缝编排器。

![](/images/posts/0a7e895da71d.png)

## 内置安全性和统一治理

通过Unity Catalog，Lakeflow继承了跨摄取、转换和编排的集中身份、安全和治理控制。连接安全地存储凭据，访问策略在所有工作负载中一致执行，细粒度权限确保只有正确的用户和系统可以读取或写入数据。

Unity Catalog还提供了从摄取到Lakeflow Jobs再到下游分析和Power BI的端到端血缘，便于追踪依赖关系和确保合规性。系统表提供了跨作业、用户和数据使用的操作和安全可见性，帮助团队监控质量并实施最佳实践，而无需拼接外部日志。

Lakeflow和Unity Catalog共同为Azure Databricks用户提供了默认受治理的流水线，从而构建出安全、可审计、生产就绪的数据交付团队可以信赖。

![](/images/posts/643df7edfd11.jpg)

阅读我们的博客，了解Unity Catalog如何支持OneLake。

## 为所有人提供灵活的用户体验和创作方式

除了所有这些功能外，Lakeflow还极其灵活且易于使用，非常适合您组织中的任何人，尤其是开发人员。

代码优先用户喜爱Lakeflow，因为它拥有强大的执行引擎和先进的以开发人员为中心的工具。借助Lakeflow Pipeline Editor，开发人员可以利用IDE并使用强大的开发工具来构建他们的流水线。Lakeflow Jobs还提供代码优先创作和开发工具，包括DB Python SDK和DABs，用于可重复的CI/CD模式。

![](/images/posts/8f08d2f64922.jpg)

Lakeflow Pipelines Editor帮助您在一处编写和测试数据流水线。

对于新手和业务用户，Lakeflow非常直观且易于使用，具有简单的点击式界面和用于通过Lakeflow Connect进行数据摄取的API。

## 减少猜测，通过原生可观测性实现更准确的故障排除

监控解决方案通常与您的数据平台隔离，使得可观测性更难操作化，您的流水线更容易中断。

Azure Databricks上的Lakeflow Jobs为数据工程师提供了他们所需的深度、端到端可见性，以快速理解和解决流水线中的问题。借助Lakeflow的可观测性功能，您可以在统一的运行列表中，通过单一UI立即发现性能问题、依赖瓶颈和失败的任务。

Lakeflow系统表和Unity Catalog的内置数据血缘还提供了跨数据集、工作区、查询和下游影响的完整上下文，使根本原因分析更快。借助Jobs中新推出的GA系统表，您可以跨所有作业构建自定义仪表板，并集中监控作业的运行状况。

![](/images/posts/b0de5fc8a16a.png)

使用Lakeflow中的系统表查看哪些作业最常失败、总体错误趋势和常见错误消息。

当问题出现时，Databricks Assistant随时为您提供帮助。

Databricks Assistant是一个嵌入在Azure Databricks中的上下文感知AI助手，通过让您使用自然语言快速构建和排除笔记本、SQL查询、作业和仪表板的故障，帮助您更快地从故障中恢复。

但这款助手的功能远不止调试。它还能生成基于Unity Catalog特性的PySpark/SQL代码并加以解释，从而理解您的上下文。它还可用于运行建议、呈现模式、执行数据探索与EDA，成为满足您所有数据工程需求的得力助手。

## 精准掌控成本与消耗

数据管道规模越大，合理配置资源用量和控制成本就越困难。

借助Lakeflow的无服务器数据处理能力，Databricks会自动持续优化计算资源，最大限度减少闲置浪费和资源消耗。数据工程师可根据需求灵活选择运行模式：对关键任务负载采用性能优先的"性能模式"，对成本更敏感的场景则选用"标准模式"。

Lakeflow Jobs还支持集群复用，允许工作流中的多个任务在同一个作业集群上运行，既消除了冷启动延迟，又实现了细粒度控制——每个任务均可选择使用可复用的作业集群或专属集群。结合无服务器计算，集群复用最大程度减少了资源启动次数，帮助数据工程师降低运维开销，增强数据成本管控力。

## Microsoft Azure + Databricks Lakeflow —— 久经考验的黄金组合

Databricks Lakeflow助力数据团队在保障治理、可扩展性与性能的前提下，实现更快速可靠的运营。通过将数据工程无缝集成至Azure Databricks，团队可借助统一的端到端平台，规模化满足所有数据与AI需求。

已集成Lakeflow的Azure客户取得了显著成效，包括：

- **加速管道开发**：团队构建部署生产级数据管道的速度提升高达25倍，创建时间缩短70%
- **提升性能与可靠性**：部分客户实现90倍性能提升，处理时间从数小时缩短至分钟级
- **提高效率与成本节约**：自动化与优化处理大幅降低运维开销。客户反馈年节约成本达数千万美元，ETL成本最高降低83%

欢迎访问Databricks博客阅读Azure与Lakeflow客户成功案例。对Lakeflow感兴趣？立即免费试用Databricks，亲身体验数据工程平台的强大功能。

## 下一步计划？

---

> 本文由AI自动翻译，原文链接：[Modernize your Data Engineering Platform with Lakeflow on Azure Databricks](https://www.databricks.com/blog/modernize-your-data-engineering-platform-lakeflow-azure-databricks)
> 
> 翻译时间：2026-02-13 04:34
