---
title: ServiceNow如何利用LangSmith提升客户成功Agent的可观测性
title_original: How ServiceNow uses LangSmith to get visibility into its customer
  success agents
date: '2025-11-17'
source: LangChain Blog
source_url: https://blog.langchain.com/customers-servicenow/
author: LangChain
summary: 本文介绍了ServiceNow如何利用LangSmith和LangGraph构建智能多Agent系统，以优化其销售与客户成功运营。面对Agent碎片化问题，ServiceNow开发了一个覆盖售前售后全流程的多Agent系统，使用LangGraph进行复杂编排，并借助LangSmith的追踪功能实现细粒度调试、性能评估和数据集构建，从而提升工作流自动化效率与决策透明度。
categories:
- AI产品
tags:
- 多智能体系统
- LangSmith
- LangGraph
- 客户成功
- 工作流自动化
draft: false
translated_at: '2026-01-06T01:11:37.753Z'
---

作者：Ganesh Srinivasan（ServiceNow）、Linda Ye（LangChain）、Jake Broekhuizen（LangChain）

ServiceNow 是一家领先的数字工作流平台，帮助企业变革 IT、客户服务及其他部门的服务管理。为了改进其内部销售与客户成功运营，ServiceNow 的 AI 团队正在使用 LangSmith 和 LangGraph 开发一个智能多 Agent（智能体）系统，用以编排从线索识别到售后采用与扩展的整个客户旅程。

**应对 Agent（智能体）碎片化问题**

在 ServiceNow，Agent（智能体）曾部署在平台的多个部分，缺乏单一可信源或统一的编排层。这种碎片化使得协调跨越整个客户生命周期的复杂工作流变得困难。

为了变革销售与客户成功运营，ServiceNow 决定构建一个全面的多 Agent（智能体）系统，能够处理从线索确认、成交交易到售后采用、续约和客户倡导的所有环节。这个雄心勃勃的项目既需要一个强大的编排框架，也需要对 Agent（智能体）行为进行深度可观测性。ServiceNow 需要一个全面的框架来评估工具完成度、准确性和路径优化，同时还需要用于 Agent（智能体）调试的细粒度逐步追踪。

**面向客户成功工作流的多 Agent（智能体）系统**

ServiceNow 正在开发一个覆盖售前和售后工作流的智能 Agent（智能体）系统。在本案例研究中，我们将涵盖售前和售后的旅程，它包括多个关键阶段：
- **线索确认**：识别正确线索并协助准备电子邮件和会议
- **机会发现**：识别交叉销售/向上销售机会
- **经济决策者识别**：识别关键的经济决策者
- **上线与实施**：帮助客户部署 ServiceNow 平台应用
- **采用情况追踪**：监控客户实际使用的授权应用
- **使用与价值实现**：确保客户从平台获取真实价值
- **续约与扩展**：识别合同续约或增加许可证的机会
- **客户满意度与倡导**：追踪客户满意度分数并培养客户拥护者

在每个阶段，专门的 Agent（智能体）会决定客户经理、销售人员或客户成功经理应采取哪些行动来满足客户需求。例如，在采用阶段，Agent（智能体）追踪应用使用情况并主动识别机会。如果客户未能实现预期价值，系统会推动客户成功经理建议可能提高投资回报率的其他应用，自动起草包含相关信息的个性化电子邮件，并安排客户成功经理与客户之间的会议。

该架构使用一个监督 Agent（智能体）进行编排，由多个专门的子 Agent（智能体）处理特定任务。不同的触发器会根据客户信号和生命周期阶段激活相应的 Agent（智能体），从而实现跨客户旅程的智能工作流自动化。

**使用 LangGraph 进行复杂的 Agent（智能体）编排**

LangGraph 提供了 ServiceNow 所需的底层工具和抽象技术，用于实现复杂的多 Agent（智能体）协调。ServiceNow 团队在其系统中广泛使用了结合 Send API 和子图调用的 Map-Reduce 风格图。这些特性支持模块化方法：团队首先使用 LangGraph 的底层技术构建了几个较小的子图，然后组合成更大的图，将原始图作为模块调用。

人在回路的特性在开发过程中被证明特别有价值。工程师可以暂停执行以进行测试、批准或回滚 Agent（智能体）操作，并使用不同的输入重新启动特定步骤，而无需等待完整的重新运行。这极大地减少了开发阻力——考虑到测试期间等待模型响应的延迟，这一点尤为重要。

ServiceNow 已将其知识图谱和模型上下文协议与 LangGraph 集成，为其平台上的 Agent（智能体）编排创建了一个全面的技术栈。

**LangSmith 追踪：Agent（智能体）开发的突出特性**

LangSmith 通过提供 Agent（智能体）编排每一步的输入、输出、所用上下文、延迟、Token 计数，提供详细的追踪能力，帮助用户提升 Agent（智能体）性能。将追踪数据直观地结构化为每个节点的输入和输出，使得调试比解析日志要容易得多。

ServiceNow 使用 LangSmith 的追踪能力来：
- **逐步调试 Agent（智能体）行为**：准确理解 Agent（智能体）如何做出决策以及问题出现在哪里
- **观察每个阶段的输入/输出**：查看 Agent（智能体）工作流中每一步的上下文、延迟和 Token 生成情况
- **构建全面的数据集**：从成功的 Agent（智能体）运行中创建黄金数据集以防止回归

**采用定制指标的严格评估策略**

ServiceNow 在 LangSmith 中实施了一个为其多 Agent（智能体）系统量身定制的复杂评估框架。他们不是采用一刀切的指标，而是根据每个 Agent（智能体）的具体任务定义自定义评分器。此外，他们还利用 LLM-as-a-judge 评估器来评判 Agent（智能体）的响应。

例如，一个生成自动化电子邮件的 Agent（智能体）会根据准确性和内容相关性进行评估。特定于 RAG（检索增强生成）的 Agent（智能体）使用块相关性和事实依据性作为主要衡量标准。每个指标都有不同的阈值来评估 Agent（智能体）输出。LangSmith UI 提供输入、输出和 LLM 生成的分数，以及延迟和 Token 计数。该 UI 还帮助 ServiceNow 查看不同实验的分数。

评估工作流包括：
- **自动化黄金数据集创建**：当提示词达到特定 Agent（智能体）任务的分数阈值时，它们会自动添加到黄金数据集中
- **人工反馈集成**：利用 LangSmith 的灵活性收集人工反馈并比较提示词版本
- **回归预防**：使用数据集确保新更新不会降低先前成功场景的性能
- **多种比较模式**：比较不同版本的提示词，以识别并利用最佳的提示策略

**测试与生产路线图**

ServiceNow 目前正处于测试阶段，由 QA 工程师评估 Agent（智能体）性能。他们正在利用这个受控环境作为构建其数据集和评估框架的基础来源。ServiceNow 将持续收集真实用户数据，并继续使用 LangSmith 监控线上 Agent（智能体）性能。当生产运行通过其阈值时，这些提示词将自动成为持续质量保证的黄金数据集的一部分。作为下一步，ServiceNow 将使用 LangSmith 最近推出的新功能——多轮评估，来评估 Agent（智能体）在端到端用户交互中的表现。我们将为评估器使用整个对话线程的上下文，而非单次对话。

**结论**

ServiceNow 正在成功利用 LangChain 平台应对 Agent（智能体）编排和可观测性的挑战。通过利用 LangGraph 进行多 Agent（智能体）协调，并利用 LangSmith 实现对 Agent（智能体）行为的细粒度可见性，ServiceNow 为跨越整个客户旅程的智能客户成功运营奠定了基础。

---

> 本文由AI自动翻译，原文链接：[How ServiceNow uses LangSmith to get visibility into its customer success agents](https://blog.langchain.com/customers-servicenow/)
> 
> 翻译时间：2026-01-06 01:11
