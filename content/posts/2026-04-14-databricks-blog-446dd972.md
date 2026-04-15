---
title: Agent Bricks：受治理的企业级智能体平台
title_original: 'Agent Bricks: The Governed Enterprise Agent Platform'
date: '2026-04-14'
source: Databricks Blog
source_url: https://www.databricks.com/blog/agent-bricks-governed-enterprise-agent-platform
author: ''
summary: 本文介绍了Databricks推出的企业级智能体平台Agent Bricks。该平台旨在解决企业在生产环境中部署智能体时面临的挑战，如与业务数据深度集成、遵循权限治理及确保业务影响。其核心特性包括开放的多AI模型支持、通过Unity
  Catalog实现的统一治理体系，以及利用业务上下文提升智能体准确性。平台还推出了Document Intelligence、Custom Agents等新功能，帮助企业在安全、可观测的环境中大规模构建和运行智能体应用。
categories:
- AI产品
tags:
- 企业智能体
- AI平台
- 数据治理
- Agent Bricks
- Databricks
draft: false
translated_at: '2026-04-15T04:49:47.886306'
---

如今，基础智能体模式已为人所熟知：一个连接工具、进行推理并执行行动的模型。但构建这个循环并非难点。真正的挑战在于让企业级智能体能够在真实的业务数据上运行，遵循真实的权限设置，并产生真实的业务影响。

最有价值的智能体，取决于其与您业务连接的深度：客户记录、运营系统、内部政策和机构知识。一个金融服务智能体，若能够审核贷款申请并应用公司承保政策，其价值在于它在业务场景中运作，而不仅仅是因为模型或框架本身。正是这种业务场景使得智能体有用，也使得它们在生产环境中难以运行。智能体需要理解数据的含义，在正确的身份和权限下操作，并且能够跨模型工作，而不会将团队锁定在单一供应商。

这正是大多数团队陷入困境的地方。大多数智能体产品只提供零散的组件，而非一个完整的平台。

这就是我们构建 Agent Bricks 的原因。Agent Bricks 是 Databricks 的企业级智能体平台，用于端到端地构建、部署和管理在您业务数据上运行的智能体。它统一了模型访问、执行、治理和上下文，使团队能够在生产环境中可靠地运行智能体。

![Agent Bricks: The Governed Enterprise Agent Platform ](/images/posts/cda180341759.png)

金融服务、零售、医疗保健和技术领域的数千家组织已在 Agent Bricks 上大规模部署了生产级智能体，包括 Workday、Virgin Atlantic、Zapier、EchoStar 和 AstraZeneca。团队正在构建的智能体能够为数百名分析师提供持续的市场分析，跨供应链、采购和研发系统编排工作流，自动解决员工对复杂服务任务的请求，并在广告费用浪费之前检测并解决营销活动中的异常情况。

今天，我们宣布 Document Intelligence 和 Custom Agents 正式全面上市，同时推出平台范围内的新功能，包括 AI Gateway，以帮助您基于数据中的丰富上下文构建、治理和保护企业级智能体。

## Agent Bricks 平台

在生产环境中运行智能体，需要的不仅仅是一个模型和工具。它需要一个平台。Agent Bricks 平台由三个核心要素定义：

**开放与多AI。** 要构建有用的智能体和智能体应用，团队需要跨多个模型提供商和框架工作，以选择合适的模型、使用正确的工具，并管理访问、成本和可靠性。Agent Bricks 通过单一 API 原生支持前沿模型和流行的编码智能体（如 Cursor、Codex 和 Claude Code），并内置路由、回退和成本优化功能。它还支持使用 LangGraph 和 OpenAI Agents SDK 等主流框架构建和部署智能体。这使得团队可以切换模型或集成外部智能体，而无需重建系统。如今，63% 的客户会在两个或更多模型系列之间路由任务，确保智能体随着模型发展保持灵活性和韧性。

**统一治理。** 大多数平台治理智能体本身、它可以调用的工具及其拥有的权限。Agent Bricks 在一个系统中治理智能体及其交互的一切。通过 Unity Catalog 和 AI Gateway，对数据、模型和外部 MCP 的访问在一个地方进行管理和监控，并强制执行端到端的身份验证。智能体通过代表令牌传递继承用户身份，因此只能访问用户被授权使用的内容。无论是查询您的数据湖仓还是调用外部 API，相同的权限、审计和路由规则适用于每一次交互。这确保了每一次智能体交互都是安全、可观测且一致的。

**因理解业务上下文而精准。** 智能体的准确性不仅仅取决于模型质量。Agent Bricks 利用 Unity Catalog 元数据（包括模式、业务定义、血缘关系、权限和数据质量信号）来改进智能体的推理和行动方式。这种上下文直接嵌入到检索和规划中，相比标准 RAG 实现了 70% 的准确率提升，并在多步骤工作流中提高了 30%。对于结构化数据，Genie Spaces 利用语义层，使智能体基于业务定义而非原始列名进行推理。这意味着智能体返回的答案与您业务的实际运作方式保持一致，而不仅仅是数据本身。这正是将模型转变为理解您业务的系统的关键。

## 新功能

今天的发布扩展了团队在 Agent Bricks 上基于多AI、治理和企业上下文所能构建的能力：

**多AI与智能体编排**

- **Apps 上的自定义智能体（GA）。** 使用任何模型或框架构建和部署智能体应用，提供全生命周期支持和无服务器计算。与 Lakebase 的原生集成可为长时间运行的工作流提供记忆、对话历史和状态管理。
- **监督者智能体（GA）。** 将多个智能体和工具编排到单一工作流中。定义任务并连接您的系统，监督者将协调跨模型和工具的执行。
- **基础模型 API 中的网络搜索。** 利用原生提供商的搜索能力，使用来自网络的实时信息为智能体响应提供依据。

**跨工具、模型和数据的受治理访问**

- **AI Gateway。** 一个统一的管理层，用于管理和治理对模型、编码智能体以及现在 MCP 连接工具的访问。它在每次交互中强制执行身份验证、权限和可观测性，使智能体能够在您的模型、工具和 API 之间安全运行。现在新增护栏功能，可检测和缓解如 PII 泄露、不安全内容、提示词注入、数据外泄和幻觉等风险，并提供可定制选项以满足各种安全需求。
- **托管的 OAuth MCP 连接器。** 安全地将 GitHub、Atlassian 和 Glean 等外部服务作为受治理的工具进行连接。凭证集中管理，使智能体能够访问系统而无需暴露密钥。

**使智能体精准的企业上下文**

- **文档智能（GA）。** 从合同、发票和报告等非结构化文档中提取和结构化数据，将 PDF 转换为可查询的知识，无需定制化流程。
- **知识助手（GA）。** 自动摄取企业文档，并使任何智能体都能访问它们，检索过程融合了系统上下文、元数据和用户约束。
- **Genie Spaces 中的智能体模式。** 从单轮问答转向对数据的多步骤推理和分析，使智能体能够规划、探索并回答复杂的业务问题。
- **用于智能体质量的 CLEARS 框架（集成 MLflow）。** 通过 MLflow 中的标准化框架，从正确性、延迟、执行、遵循度、相关性和安全性等方面评估智能体，确保生产质量。

## 立即在 Agent Bricks 上构建

如今的挑战不再是构建智能体循环，而是构建围绕它的一切：无法绕过的身份验证、不会泄露的凭证、避免锁定的模型路由、使结果正确的业务上下文，以及能展示每个智能体做了什么及其原因的可观测性。

大多数平台只关注这个系统的某些部分。Agent Bricks 将它们整合在一起。

这是一个面向企业数据操作的多AI、受治理的智能体平台，设计之初就旨在生产环境中可靠运行。我们正在通过不断增长的集成合作伙伴生态系统持续扩展该系统，包括 Accenture、Atlan、Arize、Capgemini、Celebal、Collibra、Daitaiku、Deloitte、EY、Glean、Infosys、LlamaIndex、Lovelytics、LTIMindtree、Monte Carlo、Omni Analytics、Qlik、Retool、Sigma Computing、Slalom、Tiger Analytics、Tredence 和 Wipro，将 Agent Bricks 扩展到企业日常依赖的工具和服务中。

- 查看文档开始使用 →
- 开始 Databricks 试用 →

---

> 本文由AI自动翻译，原文链接：[Agent Bricks: The Governed Enterprise Agent Platform](https://www.databricks.com/blog/agent-bricks-governed-enterprise-agent-platform)
> 
> 翻译时间：2026-04-15 04:49
