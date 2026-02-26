---
title: Lakeflow与Agent Bricks：以AI优先重塑数据工程
title_original: An AI-First Approach to Data Engineering with Lakeflow and Agent Bricks
date: '2026-02-24'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ai-first-approach-data-engineering-lakeflow-and-agent-bricks
author: ''
summary: 本文探讨了数据工程师如何利用Databricks Lakeflow平台和Agent Bricks AI函数，将AI深度集成到ETL流程中，以自动化处理结构化和非结构化数据。文章重点介绍了ai_extract、ai_classify、ai_parse_document等AI函数，它们能够大规模提取实体、分类文本、解析文档，并通过无服务器批量推理引擎高效运行。通过Lakeflow
  Jobs，企业可以在统一治理的数据平台上实现AI模型的产品化与规模化编排，从而将原始数据（如通话记录）转化为可操作的业务洞察，提升数据工程效率与价值。
categories:
- AI产品
tags:
- 数据工程
- AI/ML
- Databricks
- ETL自动化
- 非结构化数据处理
draft: false
translated_at: '2026-02-26T04:33:50.739229'
---

数据工程师正日益聚焦于一个核心问题：如何利用AI改进ETL流程，构建可靠的生产级数据管道，同时不引入新的复杂性。他们需要真正能交付价值的AI，在简化工作流程的同时，避免增加割裂的工具或剥离上下文信息。

Databricks Lakeflow 提供了一个统一的数据工程平台，内置安全可靠的AI功能，可自动化整个数据处理过程，挖掘更多洞察，并支持更广泛的业务问题。无论是通过AI生成的管道代码，还是编排AI工作负载，使用Lakeflow的数据工程师都能避免在手工粘合工作上耗费数小时，转而专注于具有战略意义和更高价值的模式，从而为企业带来实际影响。

在本博客中，我们将探讨如何通过将AI模型集成到数据管道中，实现AI模型的产品化和规模化，从而自动解锁业务洞察。

## 轻松实现大规模数据洞察挖掘

数据团队正淹没在非结构化输入中，无论是合同、发票、转录文本还是评论。处理这些数据通常意味着要应付脆弱的NLP模型、僵化的规则或手动清理工作。结果是：输出不可靠、周转缓慢，宝贵的洞察被锁在文档中，而工程师则将时间浪费在重复的解析工作上，而不是构建有影响力的成果。

借助Databricks Lakeflow，您可以通过Databricks Agent Bricks AI Functions，将AI驱动的转换无缝集成到现有工作流中，从而解决这一问题。这些功能让您能够将高质量的AI直接集成到ETL流程中，自动化地大规模提取、转换和分类结构化和非结构化数据。

Agent Bricks 提供多种类型的AI函数供您选择。其中一些无需提示词，且针对特定任务，例如：

- `ai_extract`：根据您提供的标签从输入文本中提取特定实体。例如，人物、地点、组织。
- `ai_classify`：根据您提供的标签对输入文本进行分类。例如，“紧急”与“非紧急”，或主题类别。
- `ai_translate`：将文本翻译到指定的目标语言。

我们特别兴奋地介绍最近推出的AI函数 `ai_parse_document`，它可用于将任何非结构化数据转换为所需的结构化格式。利用多模态基础模型，`ai_parse_doc` 允许您解析文本、提取表格、对图表进行推理，并将图像转换为AI生成的描述。此函数为处理先前几乎无法分析的数据开辟了新的可能性。[了解更多](https://www.databricks.com/blog/announcing-ai-functions-agent-bricks)

![ai_parse_document](/images/posts/7f575d6453c2.gif)

我们还提供了一个更通用的函数 `ai_query()`，它由我们的无服务器批量推理平台提供支持。此函数使您能够使用任意选择的LLM，一次性对大型数据集运行AI驱动的转换。

为了在数百万行数据上实现最佳性能，我们的无服务器批量推理引擎会自动调配和扩展计算资源，并并行执行工作负载。这消除了每次请求的开销，显著加快了处理速度，将运行时间从数小时缩短到数分钟，同时提高了高容量AI工作负载的成本效益。

借助Lakeflow，您可以使用 Lakeflow Jobs 轻松地将AI模型产品化，并在数据工程解决方案中原生编排它们。利用AI函数，您可以为编排工作带来更高效率，并解锁更多用例，例如：

- **生成新数据**。使用AI撰写客户洞察摘要，以加速报告或预测未来收入。
- **将数据组织和构建**成具有特定业务意义的类别。对数百万条多语言评论进行情感分析，或使用自然语言提示大规模自动化客户细分。
- **改进数据质量**。使用模糊匹配和实体解析大规模修复重复项和不一致之处。

结合Lakeflow和Agent Bricks，您可以在一个统一且受治理的数据平台上运行AI模型，确保您的AI及其提取的洞察具有正确的业务和企业上下文。

## AI函数与Lakeflow的实际用例

- 示例1：将原始通话记录转化为业务洞察

### 示例1：将原始通话记录转化为业务洞察

想象一下，您的销售团队需要一种可靠的方法，将冗长、非结构化的通话记录转化为清晰、可操作的摘要。每天有数百通电话——许多长达45到60分钟——人工审阅很快变得不切实际。

借助Databricks，您可以利用内置的AI函数轻松快速地分析所有这些记录，提取关键洞察，并生成后续建议。

您无需构建单独的AI服务或管理自定义Agent，只需编写一个查询，并通过Lakeflow Jobs将其作为编排器的一部分运行。然后，您的AI模型将直接在一个受治理的统一数据工程平台中实现，您将获得可扩展的批处理能力，该能力与您现有的销售管道工作流保持完全集成，同时保持在正确的业务和企业上下文中。

让我们看看这在实践中是如何运作的。将通话记录摄取到管道后，您可以应用AI函数将非结构化文本转换为可用的信号：

- `ai_analyze_sentiment`：揭示通话的整体情绪（积极、消极、中性）
- `ai_extract`：从通话中提取关键信息，包括客户姓名、公司名称、职位、电话号码等。
- `ai_classify`：对通话类型进行分类（紧急程度、主题等）

这为下游分析和自动化奠定了结构化基础。

接下来，使用 `ai_query` 和您选择的AI模型（在我们的示例中，我们使用“databricks-meta-llama-3-3-70b-instruct” LLM）来总结每次通话：

```sql
SELECT
  ai_query(
    'databricks-meta-llama-3-3-70b-instruct',
    CONCAT(
      'Summarize the following call transcript in three bullet points: ',
      call_transcript
    )
  ) AS call_summary
FROM call_transcripts
```

此查询可生成一致、高质量的摘要，销售和客户团队可以一目了然地审阅。

然后，您可以在同一工作流中生成个性化的后续跟进：

```sql
SELECT
  ai_query(
    'databricks-meta-llama-3-3-70b-instruct',
    CONCAT(
      'Based on the following call summary, generate a personalized follow-up email: ',
      call_summary
    )
  ) AS follow_up_email
FROM call_summaries
```

这些记录随后可以大规模直接推送到您的CRM或销售工具中，这样您的团队在通话结束后不久就能确切知道应采取的正确行动。您还可以将这些记录分享给您的BI团队，以发现差距并帮助改善整体客户服务体验。

- 示例2：简化保险理赔处理

### 示例2：简化保险理赔处理

假设您正在为一家需要更快、更一致审批的保险公司构建理赔处理管道。目前，理赔通常通过电子邮件发送，并带有非结构化附件，如扫描文档、照片和PDF，这使得大规模摄取和处理变得困难。

借助Agent Bricks和Lakeflow，数据工程师可以在其ETL管道中使用 `ai_parse_document` 和 `ai_query`，自动从收到的电子邮件中提取、规范化和整合数据。这实现了可靠的端到端自动化，减少了人工审核，加速了决策，并无缝集成到现有的数据工作流中。

具体操作如下：

使用Lakeflow和Agent Bricks，您可以将电子邮件文件摄取到数据湖屋中，然后使用以下函数提取所需数据：

- `ai_query`：读取邮件正文并提取关键信息（例如：姓名、出生日期、地址、社会安全号码）
- `ai_query`：使用一个能专门读取传入图像类型的模型。此AI函数将生成描述附件图像的文本并提取其元数据。以下是该函数的SQL查询示例：

```sql
SELECT
  ai_query(
    'your-chosen-vision-model',
    CONCAT(
      'Describe the image and extract any visible text: ',
      image_file
    )
  ) AS image_description
FROM email_attachments
WHERE attachment_type = 'image'
```

- 以及 `ai_parse_document`：读取电子邮件附带的任何PDF（jpg或png）文件

数据提取完成后，您可以再次使用 `ai_query` 将所有信息整合到一个文件中，根据您的用例，该文件可以在另一个工作流中重复使用，或直接共享给下游团队（BI分析师、AI/ML团队等）。

以下是该工作流在 Lakeflow Jobs 中的 DAG 示例：

![](/images/posts/40edcc06ae98.png)

结合 Lakeflow 与 Agent Bricks 还能实现更多功能——[观看此视频](https://example.com)了解如何将杂乱的销售数据转化为 AI 驱动的营销活动。

## AI 在 Databricks 中的实际应用

许多 Databricks 客户和数据工程师已成功运用 AI 和 Lakeflow 解决各类业务问题——定价、客户成功与营销——从而释放数据洞察并提升生产力。

纽约金融科技公司 Kard 运用 **Agent Bricks AI 功能**构建了**可扩展且精准的交易分类系统**，取代了传统手工操作与不一致的旧方法。这种现代方案使 Kard 能高效处理数十亿笔交易，提供个性化奖励，并产出推动用户忠诚度与商业价值的深度洞察。

拉丁美洲最大银行之一 Banco Bradesco 的数据工程团队曾因冗长的编码、调试和文档流程面临生产力瓶颈。通过采用 **Databricks Assistant**，他们**将编码时间缩短了 50%**，并赋能技术与非技术人员使用自然语言生成和调试代码——实现了数据访问民主化，降低了成本，并加速了数据驱动决策。

全球全渠道广告平台 Locala 曾使用 **Lakeflow Jobs 编排复杂的 LLM 训练流程**，这是其原有调度器 Airflow 无法胜任的。通过优化 ETL、模型训练与实验以及计算资源选择，**Lakeflow Jobs 消除了管理复杂工作流的运维负担**，使得仅需一名数据科学家就能构建成为该广告科技公司核心销售功能的 GenAI 助手。

借助 Lakeflow，您可以轻松将 AI 能力集成到数据工程平台中并编排 AI 工作流，使数据处理流程更高效、更洞察驱动、更易于使用。我们还有更多功能即将推出！很快，您将能使用 Databricks Genie 赋能数据工程平台，通过自然语言处理进行流水线开发与调试。

- 开始使用 [Databricks 免费版](https://example.com)
- 查看 [Databricks AI 功能](https://example.com)产品文档
- 了解更多关于 [Databricks Genie](https://example.com) 的信息

---

> 本文由AI自动翻译，原文链接：[An AI-First Approach to Data Engineering with Lakeflow and Agent Bricks](https://www.databricks.com/blog/ai-first-approach-data-engineering-lakeflow-and-agent-bricks)
> 
> 翻译时间：2026-02-26 04:33
