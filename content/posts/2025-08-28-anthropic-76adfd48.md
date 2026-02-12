---
title: Claude 3.5 Sonnet发布：智能、速度与成本的新标杆
title_original: Introducing Claude 3.5 Sonnet
date: '2025-08-28'
source: Anthropic
source_url: https://www.anthropic.com/news/claude-3-5-sonnet
author: ''
summary: Anthropic正式推出Claude 3.5模型家族的首个版本Claude 3.5 Sonnet。该模型在研究生水平推理、本科生知识及编码能力上创下行业新基准，运行速度是Claude
  3 Opus的两倍，同时保持中端模型的成本效益。它具备先进的视觉能力，能准确解读图表和转录图像文本。此外，Claude.ai新增Artifacts功能，将对话式AI扩展为协作工作空间，支持实时编辑与集成。模型定价为每百万输入Token
  3美元，输出15美元，上下文窗口20万Token，并承诺保持ASL-2安全级别。
categories:
- AI产品
tags:
- Claude 3.5
- 大语言模型
- AI助手
- Anthropic
- 多模态AI
draft: false
translated_at: '2026-02-12T04:20:52.352933'
---

# Claude 3.5 Sonnet

![Claude head illustration](/images/posts/f00412305cb7.jpg)

- 更新消费者条款和隐私政策 2025年8月28日

消费者条款和隐私政策

2025年8月28日

今天，我们正式推出Claude 3.5 Sonnet——这是即将到来的Claude 3.5模型家族中的首个版本。Claude 3.5 Sonnet在智能水平上树立了新的行业标杆，在广泛的评估中超越了竞争对手模型以及Claude 3 Opus，同时保持了与我们中端模型Claude 3 Sonnet相当的速度和成本。

Claude 3.5 Sonnet现已可在Claude.ai网站和Claude iOS应用中免费使用，而Claude Pro和Team计划订阅用户则可以享受显著更高的使用速率限制。该模型也可通过Anthropic API、Amazon Bedrock和Google Cloud的Vertex AI获取。模型定价为每百万输入Token 3美元，每百万输出Token 15美元，并拥有20万Token的上下文窗口。

![Claude model family](/images/posts/40386b9c6b72.jpg)

## 以两倍速度实现前沿智能

Claude 3.5 Sonnet在研究生水平推理（GPQA）、本科生水平知识（MMLU）和编码能力（HumanEval）方面创造了新的行业基准。它在理解细微差别、幽默和复杂指令方面表现出显著提升，并且尤其擅长以自然、亲切的语气撰写高质量内容。

Claude 3.5 Sonnet的运行速度是Claude 3 Opus的两倍。这种性能提升，结合具有成本效益的定价，使得Claude 3.5 Sonnet成为处理复杂任务（如上下文相关的客户支持和编排多步骤工作流）的理想选择。

在一项内部Agent（智能体）编码评估中，Claude 3.5 Sonnet解决了64%的问题，优于解决了38%问题的Claude 3 Opus。我们的评估测试了模型在给定自然语言描述的期望改进后，修复开源代码库中的错误或添加功能的能力。当获得指令并提供相关工具时，Claude 3.5 Sonnet能够凭借复杂的推理和故障排除能力，独立地编写、编辑和执行代码。它能轻松处理代码翻译，使其在更新遗留应用程序和迁移代码库方面特别有效。

![Claude 3.5 Sonnet benchmarks](/images/posts/fae452b490fe.jpg)

## 最先进的视觉能力

Claude 3.5 Sonnet是我们迄今为止最强的视觉模型，在标准视觉基准测试中超越了Claude 3 Opus。这些跨越式的改进在需要视觉推理的任务（如解读图表）上最为明显。Claude 3.5 Sonnet还能从不完美的图像中准确转录文本——这是零售、物流和金融服务的核心能力，在这些领域，AI可能从图像、图形或插图中获得比单纯文本更多的洞察。

![Claude 3.5 Sonnet vision evals](/images/posts/881db8ad7b29.jpg)

## Artifacts——使用Claude的新方式

今天，我们还在Claude.ai上推出了Artifacts功能，这是一项扩展用户与Claude交互方式的新特性。当用户要求Claude生成诸如代码片段、文本文档或网站设计等内容时，这些Artifacts会出现在对话旁边的一个专用窗口中。这创造了一个动态的工作空间，用户可以实时查看、编辑并基于Claude的创作进行构建，将AI生成的内容无缝集成到他们的项目和工作流中。

这项预览功能标志着Claude从对话式AI向协作工作环境的演变。这只是我们对Claude.ai更广阔愿景的开端，该平台将很快扩展以支持团队协作。在不久的将来，团队——最终是整个组织——将能够在一个共享空间中安全地集中他们的知识、文档和正在进行的工作，而Claude将充当一个按需协作的队友。

## 对安全和隐私的承诺

我们的模型经过严格测试，并经过训练以减少误用。尽管Claude 3.5 Sonnet在智能上实现了飞跃，但我们的红队评估得出结论，Claude 3.5 Sonnet仍保持在ASL-2级别。更多细节可在模型卡片附录中找到。

作为我们对安全和透明度承诺的一部分，我们已邀请外部专家来测试和完善这个最新模型中的安全机制。我们最近向英国人工智能安全研究所提供了Claude 3.5 Sonnet进行部署前安全评估。UK AISI完成了对3.5 Sonnet的测试，并根据一份谅解备忘录与美国AI安全研究所分享了他们的结果，这份备忘录的达成得益于今年早些时候宣布的美英AISI之间的合作伙伴关系。

我们整合了外部领域专家的政策反馈，以确保我们的评估是稳健的，并考虑到滥用行为的新趋势。这种合作帮助我们的团队提升了评估3.5 Sonnet抵御各种类型误用的能力。例如，我们利用来自Thorn的儿童安全专家的反馈来更新我们的分类器并微调我们的模型。

指导我们AI模型开发的核心宪法原则之一是隐私。我们不会在用户提交的数据上训练我们的生成模型，除非用户明确授予我们这样做的权限。

## 即将推出

我们的目标是在未来几个月内，显著改善智能、速度和成本之间的权衡曲线。为了完善Claude 3.5模型家族，我们将在今年晚些时候发布Claude 3.5 Haiku和Claude 3.5 Opus。

除了开发下一代模型家族外，我们还在开发新的模态和功能，以支持企业的更多用例，包括与企业应用程序的集成。我们的团队也在探索诸如“记忆”之类的功能，这将使Claude能够根据指定记住用户的偏好和交互历史，从而使用户体验更加个性化和高效。

我们一直在努力改进Claude，并乐于听取用户的反馈。您可以直接在产品内提交关于Claude 3.5 Sonnet的反馈，为我们的开发路线图提供信息，并帮助我们的团队改善您的体验。一如既往，我们期待看到您使用Claude构建、创造和发现的一切。

---

> 本文由AI自动翻译，原文链接：[Introducing Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet)
> 
> 翻译时间：2026-02-12 04:20
