---
title: Claude Fable 5登陆Databricks，通过Unity AI Gateway实现治理
title_original: Claude Fable 5 is now available on Databricks, fully governed through
  Unity AI Gateway
date: '2026-06-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/claude-fable-5-now-available-databricks-fully-governed-through-unity-ai-gateway
author: ''
summary: Anthropic最智能的通用模型Claude Fable 5现已在Databricks上可用，客户可通过Unity AI Gateway访问，获得集中治理、成本控制和可观测性。该模型在企业工作流自动化、Agent搜索、数据推理和多模态文档理解等基准测试中达到最先进水平，支持长期自主性、复杂问题首次正确性及并行子Agent委派。Fable
  5在OfficeQA Pro基准测试中准确率达57.9%，比Claude Opus 4.8提高20%，同时工具调用次数减少12%。
categories:
- AI产品
tags:
- Claude Fable 5
- Databricks
- Unity AI Gateway
- 企业AI
- 多模态
draft: false
translated_at: '2026-06-10T06:27:16.615952'
---

Claude Fable 5，Anthropic 最智能的通用模型，现已在 Databricks 上可用。Claude Fable 5 在我们涵盖企业工作流自动化、Agent（智能体）搜索、数据推理和多模态文档理解的内部基准测试中，均达到了最先进的性能。Databricks 客户可以通过 Unity AI Gateway 访问 Claude Fable 5，并获得集中治理、成本控制和可观测性。

Databricks 和 Anthropic 共享一个信念：最强大的 AI 是能够处理您最棘手的问题、使用您的数据、并在您的治理下运行的 AI。Claude Fable 5——Anthropic 有史以来最智能的模型——现已全面可用，并将在接下来一周内通过 Unity AI Gateway 在 Databricks 上（覆盖 AWS、Azure 和 Google Cloud）推出。

Claude Fable 5 是一款 Mythos 级模型，专为处理那些以前对模型来说过于复杂、耗时过长或过于模糊的问题而设计。现在，Fable 5 可以完成这些任务甚至更多；它可以完成端到端的工作流，而这些工作流原本需要一个人花费数小时、数天甚至数周的时间。

通过在 Databricks 上原生访问 Fable 5，您可以直接针对您的企业数据运行它，将其连接到您现有的工具和工作流，并在此基础上构建特定领域的 Agent（智能体），同时享有您的组织在其他所有方面已经依赖的治理能力。

## 在 Agent（智能体）企业任务中达到最先进水平

Claude Fable 5 专为长期自主性、复杂问题的首次正确性以及跨并行子 Agent（智能体）的可靠委派而构建。Databricks 在三个内部基准测试中对 Claude Fable 5 进行了评估，这些测试涵盖了企业面临的最困难的 Agent（智能体）和文档 AI 任务。结果很明确：Fable 5 是复杂、自主知识工作的质量领导者。

### OfficeQA Pro — 最先进水平

在我们的 OfficeQA Pro 基准测试中——该测试在各自的 Agent（智能体）框架下，对前沿模型进行涉及文件搜索、网络搜索、代码执行和多模态文档理解的困难文档 QA 任务评估——Claude Fable 5 达到了 57.9% 的正确率，树立了新的最先进水平。

![Claude Fable 5 基准测试](/images/posts/f64df6b0659d.png)

与 Claude Opus 4.8 相比，Fable 5 的准确率提高了 +20%，并且使用的工具调用次数减少了 12%——尽管它的速度大约慢了 30%，并且每个问题生成的输出 Token 数量是前者的 2.5 倍。Fable 5 是一个质量优先的模型，而非效率优先的模型。

## Claude Fable 5 为 Databricks 客户带来的新特性

Fable 5 旨在能够独立走得更远：以更高的准确度和更少的人工干预，处理更长、更复杂的工作流。以下是对 Databricks 客户而言，这在实践中的意义。

- **企业工作流的长期自主性：** Fable 5 能够在较长时间内维持高效产出，成功完成持续多天的、目标导向的运行。对于 Databricks 客户而言，这意味着 AI 驱动的工作流可以运行得更久，并且需要更少的人工干预。
- **复杂问题的首次正确性：** 早期测试者报告称，他们能够一次性实现之前需要数天迭代才能完成的系统。对于在 Databricks 上构建数据管道、分析工作流或 AI 应用的客户来说，这直接转化为更快的投产时间。
- **更强的代码审查和调查能力：** 错误查找的召回率明显高于 Opus 4.8。故障排查、仓库历史调查和复杂调试同样得到改进，使 Fable 5 成为 Databricks 上工程团队的强力选择。
- **可靠地委派给并行子 Agent（智能体）：** Fable 5 在调度和维护并行子 Agent（智能体）方面比以前的模型可靠得多，这是在 Databricks Agent Bricks 上构建复杂 Agent（智能体）工作流的关键能力。
- **高质量视觉能力：** Fable 5 在解读密集技术图像、Web 应用和详细截图方面，准确度远高于以前的模型，从而在 Databricks 上实现更丰富的文档 AI 和多模态工作流。

## 使用 Unity AI Gateway 安全访问 Claude Fable 5

Fable 5 可通过 Unity AI Gateway 经由统一 API 和 Messages API 端点访问，这与 Databricks 上的所有其他模型一致。管理员可以通过细粒度权限控制哪些用户、团队和服务主体可以调用它。每个请求和响应都会被记录到 Unity Catalog，从而提供整个组织范围内使用情况的完整、可查询审计追踪。并且，由于接口是标准化的，Fable 5 可以替换为任何其他模型，而无需更改应用程序代码。

![Unity AI Gateway](/images/posts/bd164fc001de.png)

## 扩展护栏以匹配 Agent（智能体）自主性

Fable 5 旨在端到端地完成工作，而不仅仅是响应单个提示词。它可以运行数小时，协调并行子 Agent（智能体），并在最少人工干预下跨工具和系统执行。这种自主性水平使其具有价值，而基础设施中的治理则让团队有信心大规模部署它。Databricks 提供两层控制。

- **对每一次 LLM 调用应用护栏。** Unity AI Gateway 在模型看到提示词之前对每个请求应用护栏，并在每个响应到达用户之前对其应用护栏，阻止 PII、越狱尝试、不安全内容以及您定义的自定义业务特定规则。每个操作都通过推理表记录到 Delta。
- **对每一次工具调用扩展护栏。** Unity AI Gateway 服务策略在每个工具调用执行之前对其进行评估，例如，完全阻止 `delete_file`，将 `drop_table` 限制为仅管理员可用，或在任何写操作之前要求明确同意。无论结果如何，每个操作都会被记录到 Delta 表。

![](/images/posts/14a6d8c82a34.png)

## 大规模跟踪和优化 Fable 5 支出

Fable 5 的长期运行消耗的 Token 数量明显多于典型的模型调用，并且 AI 工作负载可能以传统云预算工具无法检测的方式失败。Unity AI Gateway 中的 AI 支出控制允许平台团队按用户、按用例、按工作区和按账户设置阈值，并在达到限制之前触发警报。成本分析仪表板按模型、提供商、工作区和用户细分支出，以便团队在采用规模扩大时拥有完全的可见性。

## 构建特定领域的长期运行 Agent（智能体）

借助 Agent Bricks，团队可以在 Fable 5 上构建特定于其领域的 Agent（智能体）——这些 Agent（智能体）以其自身数据为基础，连接到其工具，并根据其实际工作流随时间进行评估和改进。这正是 Fable 5 的能力转化为为企业量身定制解决方案的地方。

构建完成后，Agent（智能体）将作为 Databricks Apps 部署：完全托管、无服务器，并具有内置身份验证、访问控制和基于 Lakebase 的内存，以便 Agent（智能体）在会话之间保持上下文。最终结果是，一个运行在现有最强大模型上的、连接到您的数据、受您策略治理、并部署在您的组织已经信任的基础设施上的特定领域 Agent（智能体）。

## 用于安全的数据保留

鉴于模型能力的增强，我们尊重 Anthropic 针对 Fable 5 模型的新数据保留政策，该政策包括仅出于信任和安全目的的 30 天保留期（请参阅 Anthropic 公告博客中的具体数据保留政策）。

## 在 Databricks 上开始使用 Claude Fable 5

Claude Fable 5 现已在 Databricks 上通过 Databricks Marketplace 和 Unity AI Gateway 在 AWS、Azure 和 Google Cloud 上推出。

- **在 AI Playground 中尝试 Fable 5：** 现已在 Databricks Marketplace 中可用
- **配置 Unity AI Gateway：** 在您的 Databricks 工作区中设置治理、成本控制和回退
- **探索 Agent Bricks：** 在 Databricks 上构建由 Fable 5 驱动的长期运行自主 Agent（智能体）
- **联系您的客户团队：** 获取企业访问权限、安全分类器指导或从 Opus 4.8 迁移的支持

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Claude Fable 5 is now available on Databricks, fully governed through Unity AI Gateway](https://www.databricks.com/blog/claude-fable-5-now-available-databricks-fully-governed-through-unity-ai-gateway)
> 
> 翻译时间：2026-06-10 06:27
