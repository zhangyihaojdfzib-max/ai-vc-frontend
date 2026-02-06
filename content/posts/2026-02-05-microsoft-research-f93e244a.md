---
title: 微软发布Paza语音模型与PazaBench，提升低资源语言AI话语权
title_original: 'Elevating voices in AI: Microsoft Research launches Paza & PazaBench'
date: '2026-02-05'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/paza-introducing-automatic-speech-recognition-benchmarks-and-models-for-low-resource-languages/
author: ''
summary: 微软研究院发布Paza语音模型流程与首个低资源语言自动语音识别排行榜PazaBench，旨在解决AI语音技术在资源匮乏环境中的适用性问题。Paza采用以人为本的设计，与社区合作构建并测试，首发涵盖39种非洲语言，并针对六种肯尼亚语言推出微调模型。PazaBench通过标准化评估指标追踪模型性能，以推动针对服务不足语言的语音技术进步，缩小数字鸿沟。
categories:
- AI研究
tags:
- 语音识别
- 低资源语言
- 人工智能伦理
- 微软研究院
- 非洲语言
draft: false
translated_at: '2026-02-06T04:14:49.926571'
---

## 概览

- 微软研究院发布 PazaBench 和 Paza 自动语音识别模型，推动低资源语言的语音技术进步。
- 以人为本的低资源语言处理流程：Paza 是一个端到端的持续流程，专为社区构建并由社区测试，旨在提升历史上代表性不足的语言地位，并使语音模型能在现实世界、资源匮乏的环境中可用。
- 首个同类 ASR 排行榜，从非洲语言开始：Pazabench 是首个针对低资源语言的自动语音识别排行榜。首发涵盖 39 种非洲语言和 51 个最先进的模型，在领先的公共和社区数据集上追踪三个关键指标。
- 以人为本的 Paza ASR 模型：基于在农民日常移动设备上进行真实世界测试的少量数据微调 ASR 模型，涵盖六种肯尼亚语言：斯瓦希里语、卢奥语、卡伦津语、基库尤语、马赛语和索马里语。

根据《2025年微软人工智能扩散报告》，全球大约每六个人中就有一人使用过生成式 AI 产品。然而，对于数十亿人来说，语音交互的承诺仍未兑现。尽管 AI 正变得越来越支持多语言，但一个关键问题依然存在：这些模型是否真的适用于所有语言以及依赖它们的人们？我们最初通过 **Project Gecko**（微软研究院与 **Digital Green** 的合作项目）直面了这一挑战，该项目在非洲和印度的实地团队专注于为农民构建可用的 AI 工具。

Gecko 项目揭示了语音系统在现实世界、资源匮乏的环境中经常失效的情况——许多语言无法被识别，非西方口音也经常被误解。然而，语音仍然是全球主要的沟通媒介。对于肯尼亚、非洲及其他地区的社区而言，这种不匹配带来了连锁挑战：如果没有代表其语言和文化的基础数据，创新就会停滞，数字和 AI 鸿沟也会扩大。

Paza 通过一个以人为本的语音模型流程来解决这个问题。通过 **PazaBench**，它使用公共和社区来源的数据对低资源语言进行基准测试；通过 **Paza 模型**，它对语音模型进行微调，以在中低资源语言上实现显著提升，并由社区测试人员在真实环境中使用真实设备进行评估。即将发布的实践指南将通过分享关于数据集创建、使用最少数据进行微调的方法以及评估注意事项的实用指导来补充这项工作，引入一个持续的流程，使研究人员和实践者能够构建和评估基于真实人类使用的系统。

## Project Gecko 如何影响 Paza 的设计

除了构建具有成本效益、适应性强的 AI 系统外，Project Gecko 广泛的实地工作还突出了一个重要教训：在资源匮乏的环境中构建可用的语音模型不仅是一个数据问题，也是一个设计和评估问题。要使 AI 系统有用，它们必须支持当地语言，通过语音、文本和视频支持免提交互，并以适合现实环境（即在低带宽移动设备上、在嘈杂环境中、针对不同文化水平）的格式传递信息。

这些见解塑造了 Paza 的设计，其名称源自斯瓦希里语短语 "paza sauti"，意为“投射”或“提高你的声音”。这个名字反映了我们的意图：Paza 不仅仅是简单地向现有系统添加更多语言，而是要与使用这些技术的社区合作，共同创造语音技术。在这一原则指导下，Paza 将人类使用放在首位，从而推动模型改进。

聚焦：微软研究通讯

## 微软研究通讯

与微软的研究社区保持联系。

## PazaBench：首个针对低资源语言的 ASR 排行榜

**PazaBench** 是首个专为低资源语言设立的自动语音识别排行榜。首发涵盖 39 种非洲语言，并对 52 个最先进的 ASR 和语言模型（包括新发布的针对六种肯尼亚语言的 Paza ASR 模型）进行基准测试。该平台将领先的公共和社区数据集（涵盖对话、脚本朗读、非脚本、广播新闻和特定领域数据等多种语音风格）聚合到每个语言易于探索的平台中。这使得研究人员、开发人员和产品团队能够更容易地评估哪些模型在服务不足的语言和多样化地区表现最佳，理解速度与准确性之间的权衡，同时识别哪些地方仍存在差距。

PazaBench 追踪三个核心指标：

1.  **字符错误率**：对于具有丰富词形变化的语言很重要，这些语言通过组合词的部分来构建意义，因此字符级别的错误会显著影响含义。
2.  **词错误率**：用于衡量词级转录的准确性。
3.  **RTFx**：衡量转录速度相对于实时音频时长的快慢。

PazaBench 不仅仅是提供分数，它还标准化了评估，以优先考虑数据集的差距，识别表现不佳的语言，并突出显示本地化模型在何处优于覆盖范围更广的 ASR 模型——为以非洲为中心的创新的价值提供了早期证据。

要为基准测试做出贡献，请在排行榜上请求对更多语言进行评估。

## Paza ASR 模型：与肯尼亚语言共同构建，为其服务

Paza ASR 模型包含三个基于最先进模型架构微调的 ASR 模型。每个模型针对**斯瓦希里语**（一种中资源语言）和五种低资源肯尼亚语言：**卢奥语、卡伦津语、基库尤语、马赛语和索马里语**。这些模型在公共和精选的专有数据集上进行了微调。

对这三个模型进行微调使我们能够探索实现共同目标的支持性方法：构建适用于当地环境的语音识别系统（从六种肯尼亚语言开始），并通过 **MMCT 智能体** 弥合多语言和多模态视频问答的差距。

基库尤语和斯瓦希里语的两个模型早期版本已在移动设备上部署，并在真实环境中直接与农民进行测试，使团队能够观察模型在日常使用中的表现。农民就准确性、可用性和相关性提供了即时反馈，指出了转录失败的地方、哪些错误最具破坏性以及哪些改进能使模型在实践中更有帮助。这个反馈循环直接指导了后续的微调，确保模型的改进不仅由基准分数驱动，更由其旨在服务的社区的需求和期望驱动。

以下是 Paza 模型与当今**三种**最先进 ASR 模型的比较：

![图1：包括 Paza 模型在内的几种最先进 ASR 模型在肯尼亚语言上的字符错误率比较。CER 越低表示转录性能越好。](/images/posts/d3eac32e53c0.png)

![图2：包括 Paza 模型在内的几种最先进 ASR 模型在肯尼亚语言上的词错误率比较。WER 越低表示转录性能越好。](/images/posts/44123ac95d42.png)

**1) Paza-Phi-4-Multimodal-Instruct**

微软的 **Phi-4 multimodal-instruct** 是一个为跨音频、文本和视觉进行推理而构建的下一代小型语言模型。通过 Paza，我们扩展了其音频能力，将强大的多模态架构适配成一个适用于低资源非洲语言的高质量自动语音识别系统。

该模型在统一的多语言语音数据集上进行了微调，专门针对六种语言的转录进行了优化。模型保留了其底层的 Transformer 架构和多模态能力，同时仅选择性地微调音频特定组件，从而实现了强大的跨语言泛化能力。

如下文结果所示，该模型在所有六种语言中均实现了转录质量的一致提升。

![图3：基础模型与微调后的Paza模型在六种语言上的字符错误率（CER）对比。CER越低表示转录性能越好。](/images/posts/f8205aa63d20.png)

![图4：基础模型与微调后的Paza模型在六种语言上的词错误率（WER）对比。WER越低表示转录性能越好。](/images/posts/d0fe48e3c9d6.png)

2) Paza‑MMS‑1B‑All

该模型基于Meta的mms-1b-all模型进行微调。mms-1b-all模型采用大规模Wav2Vec2.0风格的编码器，并配备轻量级的语言特定适配器，以实现高效的多语言专业化。在此次发布中，六个语言适配器均在精选的低资源数据集上独立进行了微调，从而实现有针对性的适配，同时保持共享编码器基本冻结。

如下图所示，该模型在保持强大跨语言泛化能力的同时，提升了转录准确性。

![图5：基础模型与微调后的Paza模型在六种语言上的字符错误率（CER）对比。CER越低表示转录性能越好。](/images/posts/f69e56d8c52f.png)

![图6：基础模型与微调后的Paza模型在六种语言上的词错误率（WER）对比。WER越低表示转录性能越好。](/images/posts/a231c334a2d6.png)

3) Paza‑Whisper‑Large‑v3‑Turbo

该模型基于OpenAI的whisper-large-v3-turbo基础模型进行微调。Whisper是一种基于Transformer的编码器-解码器模型，具备强大的自动语音识别（ASR）能力。该模型在整个统一的多语言ASR数据集上，针对前述六种语言进行了微调，以促进跨语言泛化。此外，还应用了额外的后处理步骤来解决已知的Whisper幻觉失效模式，从而提高了转录可靠性。

如下所示，此次发布在保持Whisper鲁棒性的同时，实现了转录准确性的提升。

![图7：基础模型与微调后的Paza模型在六种语言上的字符错误率（CER）对比。CER越低表示转录性能越好。](/images/posts/03c25152615a.png)

![图8：基础模型与微调后的Paza模型在六种语言上的词错误率（WER）对比。WER越低表示转录性能越好。](/images/posts/9a9cf01aaf6c.png)

## 未来方向

人工智能正在重塑世界的沟通方式。与人共同设计，而不仅仅是为他们设计，意味着要关注那些尚未得到充分服务的语言。我们计划将PazaBench扩展到非洲语言之外，并在全球范围内评估更多低资源语言上的最先进ASR模型。Paza ASR模型只是第一步；要真正支持小众和代表性不足的语言，需要专门的数据集、强大的本地合作伙伴关系和严格的评估。有意义的进展取决于与使用这些语言的社区持续合作，而负责任地扩展意味着优先考虑深度和质量，而非追求广泛但浅层的覆盖。

随着这项工作的继续，我们正在将我们的方法提炼成一份即将发布的指南，以帮助更广泛的生态系统管理数据集、负责任地进行微调，并在真实条件下评估模型。我们不会止步于语音——后续的指南将为在多语言、多文化背景下构建AI工具和应用的团队提供指导，并为他们提供在不同社区部署的实用建议。

这些指南立足于技术进步和社区驱动的设计，汇集了我们的经验教训，旨在帮助研究人员、工程师和设计师构建更加以人为本的AI系统。

## 致谢

以下研究人员在这项工作中发挥了不可或缺的作用：Najeeb Abdulhamid, Felermino Ali, Liz Ankrah, Kevin Chege, Ogbemi Ekwejunor-Etchie, Ignatius Ezeani, Tanuja Ganu, Antonis Krasakis, Mercy Kwambai, Samuel Maina, Muchai Mercy, Danlami Mohammed, Nick Mumero, Martin Mwiti, Stephanie Nyairo, Millicent Ochieng 和 Jacki O’Neill。

我们要感谢Digital Green(在新标签页中打开)团队——Rikin Gandhi, Alex Mwaura, Jacqueline Wang’ombe, Kevin Mugambi, Lorraine Nyambura, Juan Pablo, Nereah Okanga, Ramaskanda R.S, Vineet Singh, Nafhtari Wanjiku, Kista Ogot, Samuel Owinya 以及肯尼亚涅里和南迪的社区评估员——对此项工作的宝贵贡献。

我们向African Next Voices Kenya(在新标签页中打开)、African Next Voices South Africa(在新标签页中打开)、ALFFA(在新标签页中打开)、Digigreen(在新标签页中打开)、Google FLEURS(在新标签页中打开)、Mozilla Common Voice(在新标签页中打开)和Naija Voices(在新标签页中打开)的创建者、社区贡献者和维护者致以谢意，他们在推进非洲语言语音数据方面的工作至关重要。

### Mercy Muchai

二级研究工程师

![Kevin Chege的肖像](/images/posts/b5853d8bedff.jpg)

### Kevin Chege

机器学习工程师

![Nick Mumero的肖像](/images/posts/56044bc88b32.jpg)

### Nick Mumero

### Stephanie Nyairo

高级产品设计师

![研究聚焦 2024年4月15日](/images/posts/186e77d90e63.png)

### 研究聚焦：2024年4月15日当周

![微软研究播客 | 观点 | Kalika Bali](/images/posts/6fa28320a713.png)

### 观点：与Kalika Bali探讨面向所有人的语言技术

![研究聚焦 2024年4月1日](/images/posts/e37c5eccaec8.png)

### 研究聚焦：2024年4月1日当周

![渐变背景上的抽象波浪线](/images/posts/4dfd322b1234.png)

### Orca-Math：通过模型专业化展示SLM的潜力

---

> 本文由AI自动翻译，原文链接：[Elevating voices in AI: Microsoft Research launches Paza & PazaBench](https://www.microsoft.com/en-us/research/blog/paza-introducing-automatic-speech-recognition-benchmarks-and-models-for-low-resource-languages/)
> 
> 翻译时间：2026-02-06 04:14
