---
title: 利用Databricks文档智能与Lakeflow构建生产级智能文档处理
title_original: Building with Databricks Document Intelligence and Lakeflow
date: '2026-04-16'
source: Databricks Blog
source_url: https://www.databricks.com/blog/building-databricks-document-intelligence-and-lakeflow
author: ''
summary: 本文介绍了企业如何通过Databricks的统一数据平台解决非结构化文档处理难题。传统IDP方案存在割裂、准确率低和治理困难等问题。文章详细阐述了三个步骤：首先使用Lakeflow
  Connect安全高效地摄取散落在各处的文档；其次利用Databricks Document Intelligence的AI函数（如解析、提取、分类）将文档转化为结构化数据；最后将这些工作负载规模化生产化。该方法将文档智能直接融入数据生命周期，实现了治理统一与业务洞察的快速转化。
categories:
- AI产品
tags:
- 智能文档处理
- Databricks
- 数据工程
- 生成式AI
- 数据平台
draft: false
translated_at: '2026-04-17T04:54:47.179112'
---

尽管数十年来结构化数据管道已臻完善，但企业80%的知识资产仍处于功能性的隐形状态，被禁锢在PDF、图像和办公文档中。

传统上，智能文档处理（IDP）一直是个支离破碎的噩梦。在生成式AI时代之前，企业被迫依赖与其核心数据平台割裂的NLP和计算机视觉API。这些孤立的OCR（光学字符识别）供应商提供的准确率有限，且缺乏规范的治理协议，造成了巨大阻力。要实现企业级AI的承诺，我们需要一种将数据智能直接融入数据生命周期的统一方法。

今天，我们将展示数据工程师如何利用Databricks的统一数据工程解决方案**Lakeflow**和**Databricks Document Intelligence**，在Databricks平台中构建生产级自主IDP，从而解锁这些数据并将其转化为具有业务影响力的智能。

![Lakeflow Connect - Document Intelligence - Lakeflow Jobs](/images/posts/7f6e088912a8.png)

## 步骤一：使用Lakeflow Connect实现安全摄取

企业文档散落在孤立的“数据坟墓”中，只能通过脆弱、定制的API集成访问，一旦文件夹重命名，连接就会中断。**Lakeflow Connect**是Databricks用于将数据摄取到湖仓的解决方案，它通过为许多流行的企业应用、数据库和文件源（包括**SharePoint**和**Google Drive**）提供内置连接器，彻底改变了游戏规则。

该解决方案提供零维护的数据摄取，无需管理复杂的OAuth流程或自定义Python脚本。文档直接进入**Unity Catalog Volumes**和表，因此一旦文件进入湖仓，访问控制、血缘关系和审计便立即生效，并且您可以复用已用于结构化数据的相同细粒度、基于属性的策略。

得益于Lakeflow Connect的**强大功能**（包括增量读写），您还可以实现快速高效的大规模数据摄取。结合下游流处理，这避免了在批量回填和近实时文档流中对大型文档库进行完全重新拉取。

## 步骤二：开始使用Databricks Document Intelligence

这些企业文档承载着组织最有价值的洞察，但本质上杂乱、多变且不一致。扫描页面、手写笔记和嵌套表格困住了您最有价值的洞察。要解决这个问题，您需要的不仅仅是另一个文档提取工具；正如Forrester所指出的，您需要“以推理为先的架构演进”。Gartner预测，采用这种方法，生成式AI将把对定制训练文档模型的需求减少70%。

如今，借助**Databricks Document Intelligence**，您可以将最先进的文档理解能力直接引入您的数据。您的数据工程团队可以利用专门构建的AI函数，可靠地**解析**、**结构化**和**丰富**复杂文档，并与现有数据管道无缝集成，所有这些都由Unity Catalog统一治理。

- **ai_parse_document（新功能 - 正式发布）**：此函数使用Variant数据类型将非结构化文件转换为结构化表示。它能原生处理通常困扰传统解析器的输入复杂性，例如扫描图像、手写内容和可变布局，同时保留关键文档结构（例如嵌套表格、章节和标题），而这些是平面文本提取会丢失的。这使您可以随时间演进模式而不会破坏管道。在下游，您可以将VARIANT输出视为灵活的原生/中间表示，并使用SQL或PySpark在**Lakeflow Spark声明式管道**中将其投影到中间/最终层的Delta列中。

在解析结构的基础上，您可以链接额外的**专为研究调优的AI函数**：

- **ai_extract（公开预览）**：提取结构化洞察，如合同生效和到期日期、交易对手、发票总额、税款、货币和采购订单号。
- **ai_classify（公开预览）**：按类型（发票、采购订单、工作说明书、保密协议）、紧急程度/风险或所属业务部门对文档进行路由。
- **ai_prep_search（新功能 - Beta版）**：智能地将文档分块，用于高质量的下游嵌入，为检索或搜索用例做好准备。

以下是将ai_parse_document和ai_extract链接在一起的简单示例。**注意**：此示例使用PySpark，但您也可以使用SQL（参见文档）。

由于这些是集成到Databricks平台中的托管AI函数，Document Intelligence可以将它们与您的企业上下文（目录元数据、业务语义、现有表）相结合，以驱动智能体工作流，这些工作流基于您的企业领域上下文，以高准确度对数据进行推理。

## 步骤三：大规模生产化IDP工作负载

一旦您在笔记本中实现了摄取和解析，就需要**将您的IDP生产化**：编排摄取、解析、丰富和服务。但您还需要在CI/CD中监控SLA、故障和重试，以确保管道保持健康。

借助Databricks的原生编排器**Lakeflow Jobs**，您可以使用与ETL、分析和ML相同的编排系统，将IDP工作负载转变为稳健、自动化的管道。它为IDP DAG中的每个任务提供**统一编排**，因此您可以在单个作业中链接笔记本、Python脚本、SQL查询、管道、LLM或智能体调用，并对从文档摄取开始的完整流程进行建模。

Lakeflow Jobs还内置了**高级控制流**（包括if/else条件、for each循环、重试等）和**触发器**（表更新、文件到达、连续触发等）。这使得您可以轻松地：1）仅重新处理失败的分区或特定文档批次；2）管理作业以适应特定计划、基于事件的触发器或用于实时文档流的连续模式。

借助Lakeflow Jobs的**无服务器计算**和原生**可观测性**，您可以在文档量激增时获得自动扩展，同时呈现实时监控、指标和警报，从而准确定位瓶颈并修复故障，而无需重新运行成功的任务。

![DAG displaying productionizing IDP workloads](/images/posts/5aedbf9e042d.png)

## 将AI植根于企业上下文

当IDP得到企业上下文（您独特的模式、业务定义和自定义语义）的支持时，其价值最大。

### Unity Catalog

**Unity Catalog**在任何云上为结构化数据、非结构化文件、ML模型和业务指标提供**统一治理和发现**。对于IDP，这意味着：

- 一个统一的位置来定义原始文档和衍生结构化表的**访问策略、血缘关系和审计**
- 支持**开放格式**（Delta、Apache Iceberg、Hudi、Parquet），因此您不会被专有的文档表示形式锁定
- **业务语义**和目录级元数据，智能体可以利用这些信息来一致地命名和解释诸如“供应商”、“客户”或“合同价值”等实体。

### Document Intelligence

**Document Intelligence**利用此上下文构建**生产级AI智能体**，这些智能体知道针对给定的IDP任务应使用哪些**表、工具和模型**，受到端到端的治理以确保它们永远不会越权访问，并通过**基于LLM的质量评分**、**特定任务基准**和学习循环持续改进。对于开发者，Databricks提供**API和SDK**，因此您可以将这些智能体定义为代码，并将其集成到现有的CI/CD管道中，就像处理任何其他数据或ML资产一样。

## 现代IDP技术栈的最佳实践

要从试点走向平台，请牢记以下最佳实践：

- **数据丰富**：不要仅仅提取“供应商名称”。将其与您的内部主数据或第三方来源（如邓白氏）关联，以提供完整的业务上下文。
- **卓越运营**：为Lakeflow Jobs使用服务主体，以确保管道稳定性。
- **监控**：使用Lakehouse Monitoring跟踪模型漂移和提取准确率随时间的变化。

## 通往现代数据智能之路

借助Databricks，您可以在现代数据平台上掌控智能文档处理的全生命周期。通过结合Lakeflow与AI功能，您可以将非结构化的隐藏数据转化为可信、可查询的数据集，并在核心ETL和ML流程旁无缝运行可观测的文档处理管道。

既然我们已经探讨了自主文档智能的战略价值，现在就该着手构建它。请查阅我们的配套文章《从PDF到洞察》，获取使用Databricks部署此架构的逐步技术指南。

您还可以立即探索《文档智能》和《Lakeflow》相关文档，开始构建您的第一个IDP处理管道！

---

> 本文由AI自动翻译，原文链接：[Building with Databricks Document Intelligence and Lakeflow](https://www.databricks.com/blog/building-databricks-document-intelligence-and-lakeflow)
> 
> 翻译时间：2026-04-17 04:54
