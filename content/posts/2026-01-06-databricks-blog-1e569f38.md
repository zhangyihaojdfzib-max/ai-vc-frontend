---
title: 指令化检索器：解锁搜索智能体的系统级推理能力
title_original: 'Instructed Retriever: Unlocking System-Level Reasoning in Search
  Agents'
date: '2026-01-06'
source: Databricks Blog
source_url: https://www.databricks.com/blog/instructed-retriever-unlocking-system-level-reasoning-search-agents
author: ''
summary: 本文介绍了“指令化检索器”这一新型检索架构，旨在解决传统检索增强生成（RAG）在遵循复杂用户指令和理解异构知识源方面的局限性。文章指出，传统RAG难以将细粒度的用户意图和系统规范转化为精确的结构化查询。指令化检索器通过让系统规范流入检索流程的每个组件，能够更好地处理包含时效性、文档类型等约束的复杂任务，从而赋能更强大的企业级搜索智能体。初步评估显示，其在复杂企业问答任务上的性能显著优于传统RAG方案。
categories:
- AI研究
tags:
- 检索增强生成
- 搜索智能体
- 企业AI
- 信息检索
- 系统架构
draft: false
---

![Instructed Retriever](/images/posts/4cca8fce96da.png)

![Instructed Retriever](/images/posts/4cca8fce96da.png)

![Instructed Retriever](/images/posts/4cca8fce96da.png)

基于检索的智能体是许多关键任务型企业应用场景的核心。企业客户期望它们能够执行需要遵循特定用户指令、并在异构知识源中有效运作的推理任务。然而，传统检索增强生成（RAG）往往无法将细粒度的用户意图和知识源规范转化为精确的搜索查询。大多数现有解决方案实际上忽略了这个问题，直接采用现成的搜索工具。另一些则严重低估了这一挑战，仅依赖用于嵌入和重排的定制模型，而这些模型在表达能力上存在根本性限制。在本博客中，我们介绍**指令化检索器**——一种新颖的检索架构，它解决了RAG的局限性，并重新构想了智能体时代的搜索。接着，我们将阐述这种架构如何赋能更强大的基于检索的智能体，包括像**Agent Bricks: Knowledge Assistant**这样的系统，它们必须对复杂的企业数据进行推理并严格遵守用户指令。

例如，考虑图1中的一个示例，用户询问一个虚构的FooBrand产品的电池寿命预期。此外，系统规范还包括关于时效性、需考虑的文档类型以及响应长度的指令。为了正确遵循系统规范，用户请求必须首先被转化为结构化的搜索查询，这些查询除了关键词外，还需包含适当的**列过滤器**。然后，必须基于用户指令，根据查询结果生成一个简洁的、有依据的响应。这种复杂且需要刻意遵循指令的过程，是仅关注用户查询的简单检索流程无法实现的。

![Figure 1. Example of the instructed retrieval workflow for query [What is the battery life expectancy for FooBrand products]. User instructions are translated into (a) two structured retrieval queries, retrieving both recent reviews, as well as an official product description (b) a short response, grounded in search results.](/images/posts/22dd9113804e.png)

![Figure 1. Example of the instructed retrieval workflow for query [What is the battery life expectancy for FooBrand products]. User instructions are translated into (a) two structured retrieval queries, retrieving both recent reviews, as well as an official product description (b) a short response, grounded in search results.](/images/posts/22dd9113804e.png)

传统的RAG流程仅依赖用户查询进行单步检索，不包含任何额外的系统规范，如特定指令、示例或知识源模式。然而，如图1所示，这些规范对于智能体搜索系统中成功遵循指令至关重要。为了解决这些局限性，并成功完成如图1所述的任务，我们的指令化检索器架构使得系统规范能够流入系统的每个组件。

即使超越RAG，在允许迭代搜索执行的更高级智能体搜索系统中，遵循指令和理解底层知识源模式是关键能力，仅将RAG作为工具执行多步操作是无法解锁这些能力的，如表1所示。因此，当需要低延迟和小模型占用空间时，指令化检索器架构为RAG提供了一个高性能的替代方案，同时为深度研究等场景赋能更有效的搜索智能体。

检索增强生成（RAG）

多步智能体（RAG）

多步智能体（指令化检索器）

搜索步骤数量

遵循指令的能力

知识源理解能力

小模型占用空间

对输出的推理能力

表1. 传统RAG、指令化检索器以及使用任一方法作为工具实现的多步搜索智能体能力总结

为了展示指令化检索器的优势，图2预览了其在一系列企业问答数据集上，与基于RAG的基线相比的性能表现。在这些复杂的基准测试中，与传统RAG相比，指令化检索器将性能提升了70%以上。指令化检索器甚至比基于RAG的多步智能体高出10%。将其作为工具整合到多步智能体中，与RAG相比，在减少执行步骤的同时，带来了额外的性能提升。

![Figure 2. Comparing the response quality for instructed retriever and RAG, in both single-step and multi-step setup. RAG is implemented using Databricks Vector Search, and the multi-step agent is based on Claude Sonnet 4.](/images/posts/9067e2e583d4.png)

![ Comparing the response quality for instructed retriever and RAG,](/images/posts/9067e2e583d4.png)

在博客文章的其余部分，我们将讨论这种新颖的指令化检索器架构的设计与实现。我们将证明，指令化检索器在查询生成阶段实现了精确且稳健的指令遵循，从而显著提高了检索召回率。此外，我们展示了即使在小模型中，也可以通过离线强化学习来解锁这些查询生成能力。最后，我们进一步分解了指令化检索器在单步和多步智能体设置下的端到端性能。我们证明，与传统RAG架构相比，它始终能显著提升响应质量。

## 指令化检索器架构

为了应对智能体检索系统中系统级推理的挑战，我们提出了一种新颖的**指令化检索器**架构，如图3所示。指令化检索器既可以在静态工作流中调用，也可以作为工具暴露给智能体。其关键创新在于，这种新架构提供了一种简化的方式，不仅能处理用户的即时查询，还能将系统规范的**全部内容**传播给检索和生成系统组件。这是对传统RAG流程的根本性转变，在传统流程中，系统规范（最多）可能影响初始查询，但随后便丢失了，迫使检索器和响应生成器在没有这些规范关键上下文的情况下运行。

![Figure 3.The general Instructed Retriever architecture, which propagates both query and system specifications to both retrieval and response generation components, and enables new capabilities in each component.](/images/posts/5359c26f82e5.png)

![Figure 3. The general Instructed Retriever architecture, which propagates both query and system specifications to both retrieval and response generation components, and enables new capabilities in each component.](/images/posts/5359c26f82e5.png)

因此，系统规范是一组指导原则和指令，智能体必须遵循它们才能忠实地满足用户请求，这些规范可能包括：

- **用户指令**：一般偏好或约束，例如“关注过去几年的评论”或“结果中不要显示任何FooBrand产品”。
- **标注示例**：相关/不相关的 `<查询, 文档>` 对的具体样本，有助于为特定任务定义高质量、遵循指令的检索应是什么样子。
- **索引描述**：一种模式，告诉智能体**实际可检索**的元数据是什么（例如，在图1的示例中，`product_brand`、`doc_timestamp`）。

为了在整个流程中实现规范的持久性，我们在检索过程中增加了三个关键能力：

1.  查询分解：将复杂的多部分请求（"帮我找一款FooBrand的产品，但必须是去年的，而且不能是'轻量版'型号"）分解为完整搜索计划的能力，该计划包含多个关键词搜索和筛选指令。
2.  上下文相关性：超越简单的文本相似度，在查询和系统指令的上下文中实现真正的相关性理解。这意味着，例如，重排序器可以利用指令来提升符合用户意图（例如，"时效性"）的文档，即使关键词匹配度较弱。
3.  元数据推理：我们"指令化检索器"架构的关键差异化优势之一，是能够将自然语言指令（"去年的"）转化为精确、可执行的搜索过滤器（"doc_timestamp > TO_TIMESTAMP('2024-11-01')"）。

我们还确保响应生成阶段与检索结果、系统规范以及任何先前的用户历史记录或反馈保持一致（如这篇博客中更详细的描述）。

搜索Agent中的指令遵循具有挑战性，因为用户的信息需求可能复杂、模糊甚至相互矛盾，这些需求通常通过多轮自然语言反馈累积而成。检索器还必须具备模式感知能力——能够将用户语言转化为索引中实际存在的结构化过滤器、字段和元数据。最后，各组件必须无缝协作，以满足这些复杂、有时是多层次的约束，而不遗漏或误解其中任何一项。这种协调需要整体的系统级推理。正如我们在接下来两节中的实验所展示的，指令化检索器架构是在搜索工作流和Agent中解锁此能力的一项重大进展。

## 评估查询生成中的指令遵循能力

大多数现有的检索基准测试忽略了模型如何解释和执行自然语言规范，特别是那些涉及基于索引模式的结构化约束的规范。因此，为了评估我们指令化检索器架构的能力，我们扩展了StaRK（半结构化检索基准）数据集，并设计了一个新的指令遵循检索基准——StaRK-Instruct，使用了其电子商务子集STaRK-Amazon。

对于我们的数据集，我们重点关注三种常见的用户指令类型，这些指令要求模型进行超越纯文本相似度的推理：

1.  包含指令——选择必须包含特定属性的文档（例如，"找一款FooBrand的夹克，要最适合寒冷天气且评分最高的"）。
2.  排除指令——过滤掉不应出现在结果中的项目（例如，"推荐一款省油的SUV，但我对FooBrand有过负面体验，所以避开他们生产的任何产品"）。
3.  时效性提升——当存在与时间相关的元数据时，优先选择较新的项目（例如，"哪些FooBrand笔记本电脑经久耐用？优先考虑过去2-3年的评论——由于操作系统变化，较早的评论重要性较低"）。

为了构建StaRK-Instruct，同时能够复用StaRK-Amazon现有的相关性判断，我们遵循信息检索中指令遵循的先前工作，通过加入额外的约束来缩小现有相关性定义，从而将现有查询合成为更具体的查询。然后通过程序化方式过滤相关文档集，以确保与改写后的查询保持一致。通过此过程，我们将StaRK-Amazon的81个查询（每个查询平均19.5个相关文档）合成为StaRK-Instruct中的198个查询（每个查询平均11.7个相关文档，涵盖三种指令类型）。

为了使用StaRK-Instruct评估指令化检索器的查询生成能力，我们评估了以下方法（在单步检索设置中）：

-   原始查询——作为基线，我们使用原始用户查询进行检索，没有任何额外的查询生成阶段。这类似于传统的RAG方法。
-   GPT5-nano, GPT5.2, Claude4.5-Sonnet——我们使用各自的模型生成检索查询，输入包括原始用户查询、包含用户指令的系统规范以及索引模式。
-   InstructedRetriever-4B——虽然像GPT5.2和Claude4.5-Sonnet这样的前沿模型非常有效，但对于查询和过滤器生成等任务，尤其是在大规模部署中，它们可能成本过高。因此，我们应用了测试时自适应优化机制，该机制利用测试时计算和离线强化学习，基于过去的输入示例教会模型更好地执行任务。具体来说，我们使用StaRK-Amazon中的"合成"查询子集，并利用这些合成查询生成额外的指令遵循查询。我们直接使用召回率作为奖励信号，通过采样候选工具调用并强化那些获得更高召回率分数的调用来微调一个40亿参数的小模型。

StaRK-Instruct的结果如图4(a)所示。与原始查询基线相比，指令化查询生成在StaRK-Instruct基准测试上实现了高出35-50%的召回率。这种增益在不同模型规模上保持一致，证实了即使在严格的计算预算下，有效的指令解析和结构化查询制定也能带来可衡量的改进。更大的模型通常表现出进一步的增益，表明该方法具有随模型容量扩展的可扩展性。然而，我们微调后的InstructedRetriever-4B模型几乎与更大的前沿模型性能相当，并且优于GPT5-nano模型，这表明对齐可以显著增强Agent检索系统中指令遵循的有效性，即使使用较小的模型也是如此。

为了进一步评估我们方法的泛化能力，我们还测量了在原始评估集StaRK-Amazon上的性能，该集合中的查询没有明确的元数据相关指令。如图4(b)所示，所有指令化查询生成方法在StaRK-Amazon上的召回率都比原始查询高出约10%，证实了指令遵循在无约束查询生成场景中同样有益。我们还观察到InstructedRetriever-4B的性能相比未微调的模型没有下降，这证实了针对结构化查询生成的专业化不会损害其通用查询生成能力。

![StaRK-Instruct](/images/posts/f11076396f58.png)

![图4. 在(a) StaRK-Instruct和(b) StaRK-Amazon的三类查询上的平均检索性能。指令化查询生成模型提供了显著的性能改进。离线RL使得能够以一小部分成本微调一个高效的InstructedRetriever-4B模型，使其性能与GPT-5和Claude-4.5模型相当。](/images/posts/addde67a165a.png)

![StaRK-Amazon](/images/posts/addde67a165a.png)

## 在Agent Bricks中部署指令化检索器

在上一节中，我们展示了使用指令遵循查询生成可以实现的检索质量显著提升。在本节中，我们进一步探讨指令化检索器作为生产级Agent检索系统一部分的实用性。具体来说，指令化检索器被部署在Agent Bricks知识助手中，这是一个问答聊天机器人，您可以向其提问，并基于提供的领域专业知识获得可靠的答案。

我们将两种DIY RAG解决方案作为基线：

-   RAG：我们将高性能向量搜索的顶部检索结果输入到一个前沿大语言模型中进行生成。
-   RAG + 重排序：我们在检索阶段之后增加一个重排序阶段，早期测试表明这平均能将检索准确率提升15个百分点。重排序后的结果被输入到一个前沿大语言模型中进行生成。

为评估自建RAG解决方案与知识助手的有效性，我们在图1所示的同一企业问答基准测试套件中进行了答案质量评估。此外，我们实现了两个多步骤智能体，分别以RAG或知识助手作为搜索工具。各数据集的详细性能表现见图5（以相对于RAG基线的百分比提升表示）。

总体而言，我们可以看到所有系统在所有数据集上均持续优于简单的RAG基线，这反映了RAG在解释和一致执行多部分规范方面的不足。增加重排序阶段能改善结果，证明了事后相关性建模的益处。采用指令检索器架构实现的知识助手带来了进一步的提升，这表明在检索和生成的每个阶段持续贯彻系统规范——包括约束、排除项、时间偏好和元数据过滤器——至关重要。

多步骤搜索智能体的效果持续优于单步骤检索工作流。此外，工具的选择也很重要——以知识助手作为工具比以RAG作为工具性能高出30%以上，且在所有数据集上均有一致的改进。有趣的是，它不仅提升了质量，在大多数数据集上还实现了更短的任务完成时间，平均减少了8%（图6）。

![图5. 在五个基准数据集上比较自建RAG+重排序、Agent Bricks知识助手以及使用这两者作为工具的多步骤搜索智能体的响应质量（相对于RAG基线的提升百分比）。RAG+重排序使用Databricks向量搜索实现，多步骤智能体基于Claude Sonnet 4。](/images/posts/7b3a041c6e22.png)

![在五个基准数据集上比较响应质量](/images/posts/7b3a041c6e22.png)

![图6. 分别比较基于RAG或知识助手作为工具的多步骤智能体在五个基准数据集上的任务完成时间（秒）。](/images/posts/93375629f4db.png)

![在五个基准数据集上比较任务完成时间（秒）](/images/posts/93375629f4db.png)

构建可靠的企业智能体需要具备全面的指令遵循能力和系统级推理能力，以便从异构知识源中检索信息。为此，我们在本篇博客中提出了**指令检索器**架构，其核心创新在于将完整的系统规范——从指令到示例和索引模式——贯穿于搜索流程的每个阶段。

我们还推出了新的**StaRK-Instruct**数据集，用于评估检索智能体处理现实世界指令（如包含、排除和时效性）的能力。在此基准测试中，指令检索器架构在检索召回率上实现了**35-50%** 的大幅提升，实证证明了系统级指令感知对查询生成的好处。我们还展示了可以通过优化小型高效模型，使其达到与大型专有模型相当的指令遵循性能，这使得指令检索器成为一种适用于现实世界企业部署的高性价比智能体架构。

当与Agent Bricks知识助手集成时，指令检索器架构能直接转化为面向最终用户的更高质量、更准确的响应。在我们全面的高难度基准测试套件中，与简单的RAG解决方案相比，它提供了超过**70%** 的提升；与包含重排序的更复杂的自建解决方案相比，质量提升了超过**15%**。此外，当作为多步骤搜索智能体的工具集成时，与作为工具的RAG相比，指令检索器不仅能将性能提升超过**30%**，还能将任务完成时间减少**8%**。

指令检索器，以及许多先前已发布的创新技术，如**提示词优化**、**ALHF**、**TAO**、**RLVR**，现已集成于Agent Bricks产品中。Agent Bricks的核心原则是帮助企业开发能够在其专有数据上进行准确推理、持续从反馈中学习，并在特定领域任务上实现最先进质量和成本效益的智能体。我们鼓励客户尝试**知识助手**和其他Agent Bricks产品，以构建适用于其自身企业用例的可控且高效的智能体。

作者：Cindy Wang, Andrew Drozdov, Michael Bendersky, Wen Sun, Owen Oertell, Jonathan Chang, Jonathan Frankle, Xing Chen, Matei Zaharia, Elise Gonzales, Xiangrui Meng

1我们的测试套件包含五个专有和学术基准的混合，测试以下能力：指令遵循、特定领域搜索、报告生成、列表生成以及对具有复杂布局的PDF进行搜索。每个基准都根据响应类型关联一个自定义的质量评估器。2索引描述可以包含在用户指定的指令中，或者通过常用于**文本到SQL**等系统中的模式链接方法自动构建，例如值检索。

#### 介绍OfficeQA：一个端到端基于事实推理的基准

#### 使用自定义评估器从试点到生产

#### 通过自动化提示词优化以90倍低成本构建最先进的企业智能体

---

> 本文由AI自动翻译，原文链接：[Instructed Retriever: Unlocking System-Level Reasoning in Search Agents](https://www.databricks.com/blog/instructed-retriever-unlocking-system-level-reasoning-search-agents)
> 
> 翻译时间：2026-01-07 02:48
