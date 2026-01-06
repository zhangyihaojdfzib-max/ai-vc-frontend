---
title: Polly发布：集成于LangSmith的AI智能体调试助手
title_original: 'Introducing Polly: Your AI Agent Engineer'
date: '2025-12-10'
source: LangChain Blog
source_url: https://blog.langchain.com/introducing-polly-your-ai-agent-engineer/
author: LangChain Accounts
summary: 本文介绍了新推出的AI助手Polly，它直接集成在LangSmith平台中，旨在帮助开发者调试、分析和改进AI智能体（Agent）。文章指出，由于智能体具有提示词长、执行轨迹复杂、交互轮次多等特点，传统调试方法面临巨大挑战。Polly能够深入分析单个执行轨迹、理解长时间跨度的完整对话，并能以自然语言交互的方式协助设计更优的系统提示词。其能力基于LangSmith全面的追踪数据，现以测试版形式开放，旨在提升智能体的开发效率与质量。
categories:
- AI产品
tags:
- AI智能体
- LangSmith
- 调试工具
- 提示工程
- AI开发
draft: false
---

今天，我们正式推出Polly：一款直接集成在LangSmith中的AI助手，它能帮助你调试、分析和改进你的Agent（智能体）。

是的，我们看到了其中的反讽意味：我们正在为一个用于构建Agent的产品添加一个Agent。

我们投入了大量时间，与数千名开发者合作，在LangSmith上构建生产级Agent。我们见证了Agent真正擅长的领域（分析复杂的执行轨迹，在数百个步骤中发现模式），也看到了它们的局限（无法替代深思熟虑的工程决策）。我们希望把这件事做好。

成果就是Polly：一位理解Agent架构、识别故障模式、并能真正帮助你更快交付更优Agent的AI Agent工程师。Polly现已开放测试版。

**为什么Agent需要一个AI调试伙伴**

通过与数千个在LangSmith上构建Agent的团队合作，我们看到相同的调试挑战反复出现。Agent从根本上不同于简单的LLM（大语言模型）调用，原因在于：

*   **更长的提示词**：系统提示词常常长达数百或数千行。当行为出现偏差时，几乎不可能找出是哪条指令导致的。
*   **更长的轨迹**：Agent可以运行数百个步骤，在单次轨迹中生成数千个数据点——这远远超出了人类能有效解析的范围。
*   **多轮交互**：Agent涉及持续数小时或数天的多轮对话。要理解发生了什么，需要查看整个交互历史。

当出现问题时，你无法轻易定位是哪个决策、提示词指令或工具调用导致了它。这正是AI Agent工程师擅长解决的问题——也是我们构建Polly的原因。

**Polly帮助调试轨迹、分析对话并设计更好的提示词**

你无需再手动浏览无尽的轨迹或猜测哪个提示词修改能解决问题，只需用自然语言向Polly提问即可。这就像你的团队里有一位专家级的Agent工程师。以下是Polly目前能做的事情：

**调试单个轨迹**
在轨迹视图中，Polly会分析单次Agent执行过程，帮助你理解发生了什么。这是Polly真正大放异彩的地方——深度Agent的轨迹可能包含数百个步骤，故障模式往往很微妙，分散在许多步骤中，或隐藏在长时执行的中间环节。

你可以向Polly提问，例如：
*   "Agent有没有做什么可以更高效的事情？"
*   "Agent犯了什么错误吗？"
*   "为什么Agent选择了这种方法而不是那种？"
*   "问题到底出在哪里？"

Polly不仅仅是呈现信息。它理解Agent的行为模式，并能识别出即使经过仔细人工检查也可能遗漏的问题。

**分析完整对话**
在会话视图中，Polly可以访问整个对话的信息，这些对话有时持续数小时、数天或包含数十次来回交互。这是人类大脑无法完全记住的上下文。

你可以要求Polly：
*   总结多次交互中发生了什么
*   识别Agent行为随时间变化的模式
*   解释Agent的策略在轮次间为何改变
*   发现Agent何时丢失了重要的上下文

这对于调试那些令人沮丧的"Agent本来运行良好，然后突然就不行了"的问题尤其有效。Polly能精确定位变化发生的位置和原因。

**设计更好的提示词**
这是Polly真正强大的地方。系统提示词是任何深度Agent最重要的部分，而Polly是一位专家级的提示词工程师。

只需用自然语言描述你想要的行为，Polly就会相应地更新你的提示词。你再也不需要手动调整数百行指令、试图找出正确的措辞，或者在修复一个问题时担心是否破坏了其他东西。

Polly还可以帮助你：
*   定义结构化输出模式
*   配置工具定义
*   添加或优化少样本示例
*   在不丢失关键指令的情况下优化提示词长度

**Polly如何与LangSmith追踪协同工作**

Polly的智能源于LangSmith全面的追踪基础设施。LangSmith捕获你的Agent所做的一切：
*   **运行**：单个步骤，如LLM调用和工具执行
*   **轨迹**：你的Agent的一次执行，由一系列运行构成的树状结构
*   **会话**：一次完整的对话，包含多个轨迹

在LangSmith中设置追踪只需几分钟——请按照[此指南](https://docs.langchain.com/langsmith/setup)开始。一旦你的数据流入LangSmith，Polly就能立即开始帮助你分析Agent行为、识别问题和改进提示词。

**开始使用Polly**

Polly已经能够分析轨迹、调试对话和设计提示词。但随着时间的推移，我们将教会它如何分析实验、优化提示词等等。

准备好开始使用Polly了吗？
*   在几分钟内[设置追踪](https://docs.langchain.com/langsmith/setup)
*   开始使用LangSmith[构建和调试你的Agent](https://smith.langchain.com/)
*   与Polly对话，体验Agent工程的未来

你可以观看[此视频演示](https://youtu.be/7QvzBwYVb8o)以获取关于如何开始使用Polly的更多详细信息。

LangChain是数千个交付生产级Agent的团队信赖的Agent工程平台。现在，有了Polly，你将拥有一位AI专家，在你前进的每一步提供帮助。

---

> 本文由AI自动翻译，原文链接：[Introducing Polly: Your AI Agent Engineer](https://blog.langchain.com/introducing-polly-your-ai-agent-engineer/)
> 
> 翻译时间：2026-01-06 01:09
