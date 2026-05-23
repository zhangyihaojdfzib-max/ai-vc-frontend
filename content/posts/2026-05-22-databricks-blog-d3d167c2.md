---
title: Databricks：OpenTelemetry追踪数据直入Lakehouse
title_original: 'Observability for any agent, anywhere: Production-ready tracing with
  OpenTelemetry & Unity Catalog on Databricks'
date: '2026-05-22'
source: Databricks Blog
source_url: https://www.databricks.com/blog/observability-any-agent-anywhere-production-ready-tracing-opentelemetry-unity-catalog
author: ''
summary: Databricks推出基于OpenTelemetry的追踪数据接入方案，将AI Agent产生的海量追踪数据直接写入Unity Catalog表，存储于Delta
  Lake中。该方案通过无服务器数据接入层Zerobus Ingest实现实时、高吞吐量的数据写入，无需运维中间件。相比传统SaaS可观测性工具，它降低了留存成本，支持PII数据内部治理，并允许用SQL、MLflow等工具对追踪数据进行分析、评估与监控，加速AI应用从生产到改进的迭代循环。
categories:
- AI基础设施
tags:
- OpenTelemetry
- Databricks
- 可观测性
- AI Agent
- Lakehouse
draft: false
translated_at: '2026-05-23T05:41:24.039752'
---

- 问题：AI Agent（智能体）会产生海量的追踪数据，但传统的可观测性工具使得这些数据留存成本高昂、难以治理，并且在评估和分析工作流中难以使用。
- 解决方案：Databricks 现在支持通过完全托管、无服务器的数据接入路径，将 OpenTelemetry（OTel）追踪数据直接写入 Unity Catalog 表。
- 优势：通过将追踪数据直接存入 Lakehouse，团队可以获得可治理、可供分析的可观测性数据，实现长期留存、统一的评估与监控工作流，且无需运维任何 OTel 基础设施。
- 成果：生产环境中的追踪数据可立即用于分析和评估，从而在实际应用、模型评估与持续改进之间实现更快的迭代循环。

## 为什么 AI 追踪会打破传统可观测性

随着 AI 应用进入生产环境，追踪通过捕获提示词、工具调用、响应、延迟和执行路径，成为理解 Agent（智能体）实际行为最清晰的方式之一。如果没有强大的追踪能力，就很难理解 Agent（智能体）为何会表现出特定行为，从而使调试、评估和治理变得更加困难。

AI 追踪数据很快会变得对分析、评估和监控工作流极具价值，其用途远超传统的调试和可观测性场景。团队希望更长时间地留存这些数据，用 SQL 进行分析，将其与业务数据和模型数据关联，并复用于评估和监控。当追踪数据仅存在于可观测性系统中时，这种灵活性会受到限制，治理变得碎片化，而将数据迁移到分析工作流通常需要额外的管道和数据复制，尤其是在涉及敏感提示词数据时。

## OTel 追踪数据接入

Databricks 现在支持使用 OpenTelemetry（OTel）格式将 OTel 追踪数据直接写入 Unity Catalog。实际上，这意味着追踪数据可以实时接入并存储在 Delta 表中，从而享有与您其他数据相同的可扩展性、治理能力和工具支持。

这改变了团队使用追踪数据的方式：

- 实时接入与实用的留存策略：追踪数据可以在生成时以高吞吐量写入，并长期留存，而无需承受通常与可观测性平台相关的成本压力。
- 使用 Lakehouse 进行分析和治理：一旦追踪数据进入表中，您可以像对待任何其他数据集一样对待它们：使用 SQL 进行查询、构建仪表板、运行 ETL 管道、使用 Genie 等工具，并应用 PII 脱敏等治理控制。
- 使用完整的 MLflow 评估栈：MLflow 使搜索、过滤和深入分析追踪数据以进行调试变得简单。将追踪数据持久化存储在 Unity Catalog 中，消除了典型的实验限制（如追踪上限），从而更容易运行大规模离线评估、监控生产系统，并随着工作负载的增长持续改进质量。

### SaaS 与 Lakehouse 的对比

那么，为什么不完全依赖 SaaS 可观测性工具呢？

1. 留存成本：Agent（智能体）会产生大量的文本负载。将此类数据存储在对象存储上的 Delta Lake 中，通常比基于 SaaS 的留存模式更具成本效益。
2. PII 数据困境：将原始提示词发送到第三方平台可能会引发信息安全方面的摩擦。将追踪数据保留在 Unity Catalog 内部有助于维护数据主权并简化治理。
3. 分析能力，而不仅仅是遥测：虽然 SaaS 工具在延迟等运营指标方面表现出色，但 Lakehouse 提供了一个分析引擎。您可以将追踪数据与业务数据（如收入和转化率）关联，以了解实际影响，而不仅仅是关注系统健康状态。此外，Lakehouse 使您能够将 AI 直接应用于追踪数据，并构建评估框架以持续改进系统质量。

## 架构：无服务器 OpenTelemetry 数据接入

Databricks 支持使用 OTel 标准将 OpenTelemetry（OTel）追踪数据、日志和指标直接接入 Unity Catalog 表，从而将数据埋点与存储分离。

Databricks 通过提供托管的数据接入层（由 Zerobus Ingest 透明驱动），消除了传统多跳遥测管道的运维复杂性。Zerobus Ingest 作为一个完全托管、无服务器的数据接入引擎，原生支持通过 gRPC 协议为标准 OpenTelemetry 协议（OTLP）提供开源采集器支持，同时其 REST API 能力可实现与 MLflow 等应用框架的无缝集成。应用程序可以轻松地将 Span、日志和指标直接导出到 Unity Catalog 表，数据以 Delta 格式存储。凭借“单接收端”架构，Zerobus Ingest 通过将数据直接流式传输到 Lakehouse 来简化可观测性。现有的 OTLP 兼容采集器可以通过 gRPC 直接指向此端点，完全绕过 Kafka 等中间消息总线。Zerobus Ingest 充当您的高吞吐量遥测管道，以零基础设施开销处理数据接入和持久化。任何兼容 OTel 的客户端都可以将追踪数据导出到此端点，包括多种编程语言中流行的 AI Agent（智能体）框架。

从此，追踪数据、日志和指标成为 Lakehouse 中的一等公民，为即席 SQL 分析、仪表板、下游分析以及 MLflow 评估和监控工作流提供支持。统一您的遥测数据将创建一个持续改进的飞轮效应：生产行为反馈给评估和分析，进而推动更快的迭代和更好的 Agent（智能体）性能。

![Databricks Lakehouse 平台](/images/posts/69a9154bfc02.png)

## 教程：将追踪数据接入 Lakehouse

### 示例 Agent（智能体）：支持经理助手

在这篇博客中，我们将创建一个简单的支持经理助手，用于端到端地演示追踪功能。该 Agent（智能体）可以部署在 Databricks 之外，正如我们在此所做的那样，这突显了追踪数据接入与 Agent（智能体）运行位置是解耦的。

我们构建了一个 LangGraph Agent（智能体），它由一个 Databricks 托管的 Claude Sonnet 4.6 模型驱动，用于推理和响应生成。该 Agent（智能体）调用一个 Genie Space 作为工具，您可以在此处部署该工具。

当用户提出数据驱动的问题时，Agent（智能体）通过 MCP 工具 API 调用 Genie。Genie 将请求转换为 SQL，针对支持数据集执行，并返回结果。然后，Agent（智能体）总结发现，并为支持经理提供可操作的要点。

![支持经理助手](/images/posts/91a149f315c9.png)

### 使用 UC 设置 OTel 追踪

在对 Agent（智能体）进行埋点之前，我们首先在 Unity Catalog（UC）中配置将用于存储 OpenTelemetry 追踪数据的表。在此示例中，我们使用 MLflow 在 Unity Catalog 中创建底层的 OpenTelemetry 表，并将其链接到 MLflow 实验，以便可以从 UI 中搜索、分析和注释追踪数据。首先，确定（或创建）一个 SQL 仓库和一个 MLflow 实验，然后使用 MLflow Python 库配置 Unity Catalog 表并将模式关联到实验。有关完整步骤，请参阅此处的文档。

此设置为 OpenTelemetry Span、日志和指标创建了 Unity Catalog 表。底层数据以符合 OpenTelemetry 规范的表格式存储，MLflow 服务会自动在其旁边创建 Databricks SQL 视图，将 OpenTelemetry 数据转换为 MLflow 友好的格式，以便于查询和分析。这些视图包括：

- `<table_prefix>_otel_spans`：每个请求的详细跨度级执行数据  
- `<table_prefix>_otel_logs`：执行期间捕获的结构化日志/事件数据  
- `<table_prefix>_otel_metrics`：执行期间捕获的数值遥测数据  
- `<table_prefix>_otel_annotations`：MLflow 特定的追踪数据（非标准 OTel 信号），包括元数据、标签、评估/反馈、预期结果和运行链接  
- `<table_prefix>_trace_unified`：将追踪数据整合为每条追踪一条记录的汇总视图，包含原始跨度数据和追踪元数据  
- `<table_prefix>_trace_metadata`：按追踪 ID 分组的 MLflow 标签、元数据和评估；当仅需 MLflow 追踪元数据时，性能优于统一视图  

![OpenTelemetry 的 Unity Catalog 表](/images/posts/a09715f2c3d0.png)

设置实验后，Agent（智能体）的仪表化保持不变。任何兼容 OTel 的仪表化库都可以将追踪导出到配置的端点。您可以按照此处描述进行自动和/或手动追踪。在我们的示例中，我们依赖 `mlflow.langchain.autolog()` 来捕获详细的 LangGraph 执行（模型调用和工具调用）。我们还使用 `@MLflow.trace` 包装入口点，以建立请求级根跨度，使每次调用都能作为一次完整的端到端执行被观测。

### 检查示例追踪

现在 Agent（智能体）已完成仪表化，追踪数据正流入 Unity Catalog，让我们查看一次实际执行。

在此示例中，我们向支持经理助手提问：

“我应该推荐哪位支持工程师晋升？”

Agent（智能体）评估了请求，多次调用 Genie 空间以收集支持数据，并基于绩效指标返回了推荐结果。

![性能分析](/images/posts/57580ea2114a.png)

虽然响应看起来直接明了，但追踪揭示了产生该响应的底层执行路径。在 MLflow 实验中，我们可以看到每次工具调用以及 Claude Sonnet 模型的推理逻辑。可以看到它在整理最终答案之前调用了 Genie 空间工具三次。

![Genie 空间工具](/images/posts/360c5a495903.png)

我们可以点击每个步骤来研究其输入和输出。

![Genie 空间工具](/images/posts/59757003c88e.png)

由于追踪以 Delta 表形式存储，它们可以像任何其他数据集一样被查询。我们可以从 `mlflow_experiment_trace_unified` 视图开始，其中包含一条记录，包括请求、响应、追踪元数据以及跨度数组。

![Genie 空间工具](/images/posts/f527d85bf45d.png)

## 超越调试：追踪数据的分析

现在追踪数据存储在 Unity Catalog 中，它们立即可用于批处理和流式分析。

### Unity Catalog 中的治理

然而，提示词和响应通常包含敏感信息，因此将追踪数据视为受治理数据至关重要。通过将其存储在 Unity Catalog 中，追踪数据继承了细粒度的访问控制，从目录和模式权限到列掩码和行级过滤，从而在保持灵活性的同时实现安全、生产级的分析。

一旦建立了访问权限，团队可以通过 SQL 查询底层表和视图来安全地运行临时分析，正如我们上面所做的那样。我们还可以构建 ETL 管道，以及仪表板和 Genie 空间，以获得可操作的业务洞察。

### 仪表板

MLflow 实验 UI 现在为 Unity Catalog 中的追踪数据提供了原生可观测性仪表板，包括追踪量、错误、延迟、Token 使用量和成本的视图。对于大多数团队来说，这足以监控 Agent（智能体）的日常运行状况。

![仪表板](/images/posts/72b5d761af2f.png)

当您需要超越原生可视化的视图时，追踪表仍然是 Unity Catalog 中的 Delta 表。您可以针对它们构建自定义的 AI/BI 仪表板，并编写标准 SQL（借助 AI 的帮助）来建模团队关心的任何内容。

为了展示自定义仪表板可以在原生视图之上增加什么，我们在追踪表上构建了一个 AI 运营中心。以下是一些值得一提的功能。

自定义成本分析与合同定价

原生成本指标依赖于标准标价，这对于拥有协商费率或运行不同定价的微调模型的团队来说可能不准确。由于我们控制 SQL，因此将定价逻辑直接嵌入到查询中。该仪表板按模型类型（例如，GPT 5.5 与 Claude 4.6 Sonnet）跟踪 Token 使用量，并应用我们的合同费率来生成反映实际支付金额的“每次追踪预估成本”。这使得发现昂贵的异常值变得容易，例如由于检索循环导致单个复杂查询花费 0.50 美元。

![自定义成本分析](/images/posts/f212ec0175eb.png)

组件级性能

原生延迟视图显示追踪级别的 P50/P99。为了更深入一层并查看哪个工具较慢，我们构建了一个“工具性能”小部件，该小部件分解 Agent（智能体）中每个单独工具的延迟（P50、P99）和错误率（例如，`retrieve_docs` 与 `generate_response`）。这告诉我们 LLM、Genie 工具调用还是其他步骤是瓶颈，从而可以精确定位用户体验下降的位置。

![组件级性能](/images/posts/bae950937a90.png)

### Genie 空间

业务和技术利益相关者通常希望在不编写 SQL 的情况下探索 Agent（智能体）行为。通过 Genie 公开追踪表，团队可以对其遥测数据进行自然语言分析，允许用户直接询问有关性能、工具使用、延迟和模型行为的问题。在我们的示例中，这可能包括以下问题：

- 哪些类型的请求需要升级处理？
- 工具重试次数是否在增加？
- 哪些查询触发了最复杂的执行路径？

![追踪表](/images/posts/ab87de19703b.png)

### ETL 管道

由于追踪以 Delta 表形式存储，它们可以像任何其他数据集一样馈送到下游 ETL 管道。通过启用变更数据馈送（CDF），团队可以增量处理追踪数据（批处理或流式处理），而无需重复扫描整个表。

这使得可观测性可操作化成为可能。例如，管道可以监控追踪模式，并在延迟超过定义阈值、工具故障激增或 Token 使用量偏离预期基线时触发警报。这些信号随后可以馈送到仪表板、通知系统或自动修复工作流中。

重要的是，这补充了诸如 AI 护栏之类的实时保护。护栏在请求时执行策略，而 ETL 管道则创建反馈循环，帮助团队分析趋势、优化策略并持续改进 Agent（智能体）性能。

## 闭环：从生产追踪到评估

一旦追踪可用，它们就可以驱动完整的 MLflow 评估栈，使团队能够在其 GenAI 应用程序的整个生命周期中衡量、改进和维护质量。评估和监控直接构建在追踪之上，允许使用 LLM 评判器和自定义指标对开发、测试和生产期间捕获的相同遥测数据进行评分。

### 开发期间评估

MLflow 允许我们针对评估数据集运行评估，应用内置或自定义评判器对响应质量进行评分。一种有效的方法是从真实追踪中引导生成此数据集。由于这些提示词源自实际用户交互，与纯粹合成的测试用例相比，它们能更好地代表 Agent（智能体）必须处理的场景。

下面，我们从最近捕获的追踪中创建一个评估数据集。MLflow 使用 SQL 仓库来搜索和物化数据集记录，因此请确保在您的环境中配置了仓库 ID。

有了数据集后，我们就可以定义用于给应用打分的评判器。MLflow 提供了一系列内置评判器，同时也允许我们根据 Agent（智能体）的预期行为来定义自定义评估准则。

现在，我们可以在 MLflow 实验中查看结果。

![M Flow 实验](/images/posts/d1214aec0866.png)

### 生产监控

开发阶段的评估帮助我们在发布前验证行为，但生产监控则展示应用在真实用户环境下的表现。MLflow 能够使用相同的评判器自动评估实时追踪数据，帮助我们快速发现性能退化、数据漂移以及新出现的故障模式。这使得评估从一次性任务转变为伴随应用演进的持续性实践。

## 在 Databricks 上运行 AI 可观测性的客户

Experian

Superhuman (Grammarly)

SmartSheet

The Standard

## 常见问题解答 (FAQ)

问：我能否将此功能用于在 Databricks 之外运行的 Agent（智能体）？
答：可以，Agent（智能体）可以在任何地方运行。事实上，本博客中使用的客服助手示例就是本地部署的。

问：此解决方案的吞吐量和存储限制是多少？
答：数据摄入吞吐量限制起始为 200 QPS。存储没有限制。之前每个实验的追踪数据限制已不再适用。如果您需要更高的吞吐量限制，请联系您的 Databricks 客户团队。

问：如何确保我的搜索查询、MLflow 实验体验以及下游分析保持高性能？
答：通过最新的产品更新，数据表会自动进行 Liquid 聚类以保持数据的最佳组织状态。然而，对于较大的追踪数据量，您应该在派生视图之上创建物化视图，并对其进行增量刷新以维持查询性能。

问：此功能如何处理用户提示词中的个人身份信息 (PII)？
答：此功能不对 PII 进行任何特殊处理。但是，数据存储在 Unity Catalog 中，您可以在其中利用治理功能（如细粒度访问控制、列掩码和行过滤）来管理和限制下游访问。

## 开始使用

要开始使用，请按照文档进行操作。

### 在您的收件箱中获取最新文章

订阅我们的博客，将最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Observability for any agent, anywhere: Production-ready tracing with OpenTelemetry & Unity Catalog on Databricks](https://www.databricks.com/blog/observability-any-agent-anywhere-production-ready-tracing-opentelemetry-unity-catalog)
> 
> 翻译时间：2026-05-23 05:41
