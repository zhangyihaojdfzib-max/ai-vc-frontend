---
title: OpenAI GPT-5.2与Responses API登陆Databricks，赋能可信数据感知智能体
title_original: 'OpenAI GPT-5.2 and Responses API on Databricks: Build Trusted, Data-Aware
  Agentic Systems'
date: '2025-12-11'
source: Databricks Blog
source_url: https://www.databricks.com/blog/openai-gpt-52-and-responses-api-databricks-build-trusted-data-aware-agentic-systems
author: null
summary: OpenAI最新模型GPT-5.2及其Responses API现已在Databricks平台正式上线。该集成通过Agent Bricks框架，使开发者能够安全地将模型连接至受治理的企业数据，调用MCP工具，并评估响应的准确性与可靠性。GPT-5.2在中等至复杂任务中展现出更高的准确性、更强的指令遵循与结构化推理能力。结合Responses
  API提供的统一接口，企业可高效构建具备多模态处理、工具调用能力且可追溯的智能体系统，从而在真实工作流中实现安全、可扩展的AI应用部署。
categories:
- AI产品
tags:
- OpenAI
- Databricks
- AI智能体
- 企业AI
- 大模型集成
draft: false
translated_at: '2026-01-06T01:25:13.336Z'
---

• OpenAI GPT-5.2 和 Responses API 现已登陆 Databricks，为团队提供了一种统一的方式来构建具备推理、多模态和使用工具能力的 Agent（智能体），且集成工作量极小。
• 借助 Agent Bricks，开发者可以安全地将 GPT-5.2 连接到受治理的数据，调用 MCP 工具，并评估每个响应的准确性和可靠性。
• 这些能力共同实现了可信赖的、具备数据感知能力的 Agent（智能体），它们能够安全地行动，交付一致的结果，并在真实的企业工作流中实现扩展。

OpenAI GPT-5.2 现已在 Databricks 上可用，让团队能够在第一天就在 Databricks 数据智能平台内访问 OpenAI 的最新模型。此次发布还新增了对 Responses API 的原生支持，该 API 解锁了 OpenAI 模型的全部能力，使开发者能够更快地构建 Agent（智能体）系统，并大幅减少自定义集成工作。

当与 Databricks Agent Bricks 结合使用时，开发者可以安全地将模型连接到受治理的数据，使用自定义指标评估每个响应，并可靠地大规模部署和监控 Agent（智能体）。这些能力共同为构建能够准确推理并安全地作用于企业数据和流程的 AI Agent（智能体）奠定了基础。

GPT-5.2 在对于企业和 Agent（智能体）工作流至关重要的领域直接改进了 GPT-5.1：在中等到复杂任务上具有更高的准确性和更好的 Token 效率，更强的指令遵循能力且格式更清晰，更具条理的框架式推理，以及更低的冗余度和更聚焦于任务的响应。它还表现出更保守的基于事实的倾向，偏爱更清晰、基于证据的推理，并在输入模糊或未明确指定时减少偏离。

这些改进直接惠及依赖准确性和结构化执行的用例：

为了解这些改进如何转化为真实的企业工作负载，我们在 OfficeQA 上评估了 GPT-5.2。OfficeQA 是 Databricks 设计的基准测试，旨在测试客户日常执行的那些涉及大量文档、多步骤的分析任务。OfficeQA 基于 89,000 页美国财政部公报构建，用于衡量模型跨文档检索信息、解读复杂表格以及基于真实企业数据执行精确计算的能力。

在整个基准测试和最难的子集上，GPT-5.2 都取得了迄今为止 OpenAI 最强的性能表现，在 Agent（智能体）设置和 Oracle 页面基线方面均优于 GPT-5.1。这些提升突显了 GPT-5.2 在处理大量文档工作负载时更强的基于事实的能力、更稳定的推理和更高的可靠性。

"OpenAI GPT-5.2 旨在擅长企业中的 Agent（智能体）任务，在中等到复杂的工作负载上提供更高的准确性和更好的 Token 效率。我们很高兴 GPT-5.2 在第一天就能在 Databricks Agent Bricks 中可用，为客户构建和部署能够在企业用例中准确、安全地进行推理的 AI Agent（智能体）提供了坚实的基础。" — Nikunj Handa，OpenAI API 产品负责人

Responses API 现已在 Databricks 上可用，为开发者提供了一个统一的接口，用于构建能够使用工具、处理文件、跨文档检索和生成结构化输出的 Agent（智能体）。它使模型能够在单个请求中调用 MCP 工具、执行计算机使用操作或生成图像，从而无需手动编排层。响应以类型化和有序的项目形式返回，这使得集成、验证和调试比处理自由格式的消息可靠得多。由于该 API 在一个一致的流程中处理文本、图像和工具调用，多模态和工具驱动的工作负载的实现变得显著更容易。很快，Responses API 将作为 Databricks 上所有基础模型的统一接口提供，使多模态和工具驱动的工作负载的构建和扩展变得更加容易。

现在，GPT-5.2 和 Responses API 已在 Databricks 上可用并与 Agent Bricks 集成，团队可以构建受治理的、具备数据感知能力的 Agent（智能体），这些 Agent（智能体）能够采取实际行动并具备完全的可追溯性。GPT-5.2 和 Responses API 建立在 Databricks 与 OpenAI 的合作伙伴关系之上，该合作已经在加速客户开发和部署 AI 的方式。

"Databricks 和 OpenAI 的合作对我们来说非常出色。我们正在使用 OpenAI SDK 和 API，以及所有 Databricks 组件。我们可以在几天内，有时甚至在研讨会期间，在 Databricks 中创建和部署应用程序，以构建 MVP 和 POC，帮助团队了解他们如何利用我们现有的工具来获取洞察、采取行动，并重新思考应用程序和解决方案。" — Richard Masters，维珍航空数据与人工智能副总裁

Agent（智能体）需要访问内部数据和服务，但以受控和可审计的方式实现这一点很困难。Responses API 允许 GPT-5.2 在其推理过程中直接调用 MCP 工具，使 Agent（智能体）能够查询 Delta 表、获取特征或触发内部 API，而无需离开平台。Agent Bricks 通过 MCP Catalog 定义 Agent（智能体）允许使用的工具，MLflow 记录追踪和评估信息，以便开发者可以检查每个工具的调用方式。这为使用专有数据做出明智决策的 Agent（智能体）创建了一条受治理且可观察的路径。

多模态工作流通常需要多个端点、自定义路由和脆弱的预处理。Responses API 通过将文本、图像和 PDF 等文件视为单个推理步骤中的原生输入，消除了这种复杂性。GPT-5.2 可以总结文档、从图表中提取信息、分析扫描页面或生成新的视觉内容，而无需切换界面。由于一切都在 Databricks 上运行，数据保持受治理状态，并且血统得以保留。

一旦 AI Agent（智能体）连接到数据和工具，下一步就是确保其在真实工作负载中行为可靠。Agent Bricks 使用 MLflow 捕获每次运行的详细追踪，启用评估以发现回归问题，并在您优化逻辑时跟踪版本。这为测试变更、比较输出以及将高性能的 Agent（智能体）版本推广到生产环境提供了一个可重复的、企业级的工作流。

从 Databricks AI Playground 开始，使用 GPT-5.2，并在几秒钟内尝试提示词、工具调用和多模态输入。熟悉之后，使用 Agent Bricks 注册一个连接到您 Lakehouse 的 MCP 工具，构建一个小型的具备数据感知能力的 Agent（智能体），并通过追踪和评估进行迭代，直到 Agent（智能体）行为可靠。当它在您的数据上表现一致时，将其推广到生产环境。

产品
2024年11月21日 / 3分钟阅读

---

> 本文由AI自动翻译，原文链接：[OpenAI GPT-5.2 and Responses API on Databricks: Build Trusted, Data-Aware Agentic Systems](https://www.databricks.com/blog/openai-gpt-52-and-responses-api-databricks-build-trusted-data-aware-agentic-systems)
> 
> 翻译时间：2026-01-06 01:25
