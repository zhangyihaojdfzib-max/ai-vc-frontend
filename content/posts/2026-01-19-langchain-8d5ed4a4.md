---
title: Remote利用LangChain与LangGraph实现AI驱动的规模化客户入驻
title_original: How Remote uses LangChain and LangGraph to onboard thousands of customers
  with AI
date: '2026-01-19'
source: LangChain Blog
source_url: https://www.blog.langchain.com/customers-remote/
author: ''
summary: 本文介绍了Remote公司如何通过构建代码执行智能体，结合LangChain和LangGraph，解决大规模客户数据迁移的挑战。该方案将大语言模型的推理能力与确定性代码执行分离，在沙箱中运行Python代码处理海量数据，避免了上下文窗口限制和幻觉问题，实现了数千家客户的自动化、精准入驻。
categories:
- AI产品
tags:
- LangChain
- LangGraph
- 智能体
- 数据迁移
- 企业AI
draft: false
translated_at: '2026-01-20T04:44:02.288284'
---

![How Remote uses LangChain and LangGraph to onboard thousands of customers with AI](/images/posts/5207977ffeb6.png)


# Remote 如何利用 LangChain 和 LangGraph 通过 AI 为数千家客户完成入驻

特邀撰稿人：José Mussa（Remote 高级软件工程师）

Remote 是一家快速发展的初创公司，致力于帮助企业通过单一平台在全球范围内招聘、管理和支付员工薪酬。Remote 的客户业务遍布多个国家和监管环境，他们信赖 Remote 作为其员工、薪资和合规数据的记录系统。每位新客户都带来一套独特的人力资源和薪资数据，有时包含数千个电子表格或大型 SQL 导出文件。准确、快速地迁移这些数据是客户入驻成败的关键，但手动操作根本无法规模化。

为了应对这一挑战，Remote 在其 AI 服务内部构建了一个代码执行 Agent（智能体），以实现这些迁移流程的自动化。该 Agent（智能体）将大语言模型的推理能力与确定性代码执行的精确性相结合。以下是其工作原理、Remote 选择使用 LangChain 和 LangGraph 来构建它的原因，以及他们在此过程中获得的经验。

## 挑战：上下文窗口与幻觉

LLM（大语言模型）功能强大，但也有其硬性限制。每个模型都有一个上下文窗口：即其一次能处理的 Token 最大数量。即使是像 GPT-5 这样的先进模型，其上限也仅在 40 万 Token 左右，远少于大型薪资电子表格中的数百万字符。模型还需要占用部分窗口来跟踪指令、系统提示词和对话历史。

试图将 50 MB 的 Excel 文件直接输入 LLM（大语言模型）不仅成本高昂，还很可能产生幻觉。正如 Anthropic 工程师所指出的，当 Agent（智能体）直接调用工具时，每个中间结果都会流经模型，这可能导致每次调用增加数万个 Token，甚至超出上下文限制。

对于像 Remote 这样准确性和合规性不容妥协的全球雇佣平台而言，这些限制清楚地表明，需要一种不同的方法来进行大规模数据迁移。

## 解决方案：让模型推理，让代码执行

Remote 的代码执行 Agent（智能体）将“思考”与“执行”分离。它不强迫 LLM（大语言模型）摄取所有数据，而是利用 LangChain 的工具调用接口来决定采取哪些步骤，然后编写并运行真实的 Python 代码来转换数据。

Anthropic 关于代码执行的研究揭示了这种混合设计为何有效：通过让 Agent（智能体）在沙箱中运行代码，工具定义和中间结果都保留在上下文窗口之外。只有指令和摘要会经过模型，这极大地减少了 Token 使用量，并几乎消除了幻觉风险。

以下是 Remote 的 Agent（智能体）在实际工作中的流程：

- **文件摄取**。客户将其原始数据（CSV、Excel 或 SQL 导出文件）上传到 Remote 的安全存储中。
- **Agent（智能体）推理**。利用 LangChain 的工具调用功能，Agent（智能体）接收诸如“将此文件转换为 Remote 的员工入职模式”的任务。它会规划如何将输入列映射到该模式。
- **沙箱执行**。在后台，一个 Python 沙箱（在 WebAssembly 中运行）执行由 LLM（大语言模型）生成的代码。Remote 依赖 Pandas 等库，因为它们在数据分析方面快速且灵活。
- **迭代优化**。Agent（智能体）审查输出，如有需要则编写更多代码，并重复此过程，直到数据符合模式要求。
- **结构化输出**。最终经过验证的 JSON 文件被存储以供后续摄取。大型中间结果从不传回模型，从而保持上下文简洁。

该架构最初是一个概念验证，Remote 将一个包含 5000 行的 Excel 文件输入 Agent（智能体）。Agent（智能体）在沙箱中加载文件，使用 Pandas 将每个条目映射到模式，并且可以通过运行代码（而非生成文本）来回答诸如“员工 X 的年龄是多少？”的查询。Remote 还限制了控制台输出，以防止模型尝试读取整个数据集——这是一种直接从数据科学笔记本中借鉴的简单“显示前 N 行”模式。

## 为何选择 LangChain 和 LangGraph

Remote 选择 LangChain 是因为其生态系统为提示词处理和工具调用提供了成熟的抽象层。其模块化设计使团队能够集成多个模型提供商，并基于标准接口进行构建，而无需自行开发。Remote AI Agent Toolkit（Remote 为合作伙伴发布的开源包）已经使用 LangChain 将人力资源任务作为结构化工具公开，因此保持内部工作流的一致性是一个自然的选择。LangChain 为 Remote 奠定了基础，使其能够专注于对他们最重要的事情：安全性、可扩展性和开发者体验。

其节点和边模型让 Remote 能够将复杂的工作流（摄取、映射、执行、验证）表示为有向图。每个步骤成为一个节点，并具有明确的状态转换（成功、失败或重试）。这使得 Agent（智能体）的状态透明且可恢复，类似于分布式系统工程师对管道的思考方式。LangGraph 专注于长期运行、有状态的 Agent（智能体），这与我们多步骤的迁移流程完美契合。

通过将 LLM（大语言模型）推理与确定性代码执行相结合，Remote 已将手动流程转变为自动化工作流。他们的入驻团队不再需要为每个客户编写定制脚本——他们只需将数据输入代码执行 Agent（智能体）。该 Agent（智能体）能在数小时而非数天内，将各种格式的数据转换为一致的 JSON 模式。

除了速度之外，该系统还使一切变得更加可靠。由于转换逻辑作为代码在沙箱中运行，因此它是可重复且可审计的，这对于处理跨司法管辖区敏感雇佣和薪资数据的平台至关重要。LLM（大语言模型）指导整个过程，但实际的数据操作由可信的 Python 库完成，完全绕过了幻觉问题。

构建这个 AI Agent（智能体）让 Remote 学到了几个经验，这些经验现在指导着其团队在全公司范围内构建 AI 系统的方式：

- **LLM（大语言模型）是规划者，而非处理器**。利用它们来推理任务和选择工具，但将繁重的数据处理卸载给代码。
- **结构化优于即兴发挥**。将工作流编排为图，使其更易于调试和扩展。
- **上下文 Token 非常宝贵**。大型中间结果应保留在它们所属的执行环境中。
- **Python 仍是分析的主力**。像 Pandas 这样的库提供了快速、灵活的数据操作能力，难以被超越。

代码执行 Agent（智能体）是 Remote 更广泛 AI 平台中的一个构建模块。每当他们在不同团队中发现重复的模式，例如将文档转换为结构化记录或从半结构化表单中提取数据，他们就会将其抽象成一个可复用的 Agent（智能体）。最近的一个例子是 Agentic OCR-to-JSON Schema 原型，它将文档解析与 Agent（智能体）工作流相结合，性能远超基础 OCR。

随着 Remote 不断完善这些工具，团队计划将通用的改进贡献回 LangChain 的开源生态系统，并采纳社区出现的新创新。

在全球雇佣平台上为数千家客户完成入驻，迁移人力资源数据是最棘手的部分之一。通过将 LangChain 的工具框架、LangGraph 的编排能力以及 Python 代码执行层相结合，Remote 构建了一个能够可靠且大规模处理复杂转换的系统。这种利用 LLM（大语言模型）进行推理、利用代码进行执行的混合方法，反映了 Remote 如何将 AI 作为基础设施进行投资：消除摩擦，同时使团队能够专注于更高层次的问题，帮助客户在任何地方雇佣和支付任何人。

来自 LangChain 团队和社区的更新

正在处理您的申请...

成功！请检查您的收件箱并点击链接确认订阅。

抱歉，出错了。请重试。

![Fastweb + Vodafone: Transforming Customer Experience with AI Agents using LangGraph and LangSmith](/images/posts/7d701cbfd763.png)

## Fastweb + Vodafone：使用 LangGraph 和 LangSmith 通过 AI Agent（智能体）变革客户体验

![How Jimdo empower solopreneurs with AI-powered business assistance](/images/posts/7e6643c5bf29.png)

## Jimdo 如何通过 AI 驱动的业务助手赋能个体创业者

![How ServiceNow uses LangSmith to get visibility into its customer success agents](/images/posts/8fd47451bedf.png)

## ServiceNow 如何使用 LangSmith 获取其客户成功 Agent（智能体）的可观测性

![Monte Carlo: Building Data + AI Observability Agents with LangGraph and LangSmith](/images/posts/cc9b83b0771d.png)

## Monte Carlo：使用 LangGraph 和 LangSmith 构建数据与 AI 可观测性 Agent（智能体）

![How Bertelsmann Built a Multi-Agent System to Empower Creatives](/images/posts/64b86b3206b1.png)

## 贝塔斯曼如何构建多 Agent（智能体）系统赋能创意工作者

![How Exa built a Web Research Multi-Agent System with LangGraph and LangSmith](/images/posts/a29355ef524b.png)

## Exa 如何利用 LangGraph 和 LangSmith 构建网络研究多 Agent（智能体）系统


> 本文由AI自动翻译，原文链接：[How Remote uses LangChain and LangGraph to onboard thousands of customers with AI](https://www.blog.langchain.com/customers-remote/)
> 
> 翻译时间：2026-01-20 04:44
