---
title: FilBench：评估大语言模型对菲律宾语的理解与生成能力
title_original: 🇵🇭 FilBench - Can LLMs Understand and Generate Filipino?
date: '2025-08-12'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/filbench
author: ''
summary: 本文介绍了FilBench评估套件，用于系统性评估大语言模型在塔加洛语、菲律宾语和宿务语上的表现。该套件涵盖文化知识、经典NLP、阅读理解和生成四大类别共12项任务，通过对20多个先进模型的测试发现，尽管东南亚特定区域模型在参数效率上表现优异，但仍落后于GPT-4等闭源模型。研究强调了为菲律宾语言构建系统性评估工具的重要性，并提供了开源实现。
categories:
- AI研究
tags:
- 大语言模型
- 多语言评估
- 菲律宾语
- AI研究
- 自然语言处理
draft: false
translated_at: '2026-02-20T04:35:01.796304'
---

# 🇵🇭 FilBench - LLM 能理解和生成菲律宾语吗？

随着大语言模型（LLM）日益融入我们的生活，评估它们是否能反映特定语言社群的细微差别和能力变得至关重要。
例如，菲律宾人是全球最活跃的 ChatGPT 用户群体之一，其 ChatGPT 流量排名第四（仅次于美国、印度和巴西 [1] [2]），但尽管使用率很高，我们仍不清楚 LLM 在塔加洛语和宿务语等菲律宾语言上的表现如何。
现有的大部分证据都是轶事性的，例如用 ChatGPT 以菲律宾语回复的截图来证明其流利程度。
我们真正需要的，是对 LLM 在菲律宾语言上的能力进行系统性评估。

为此，我们开发了 FilBench：一个全面的评估套件，用于评估 LLM 在塔加洛语、菲律宾语（塔加洛语的标准化形式）和宿务语上的流利度、语言与翻译能力，以及特定的文化知识。

我们使用它对 20 多个最先进的 LLM 进行了评估，全面评估了它们在菲律宾语言上的表现：

- 📄 论文：https://arxiv.org/abs/2508.03523
- 🖥️ GitHub：https://github.com/filbench/filbench-eval

## FilBench

FilBench 评估套件包含四大类别——文化知识、经典 NLP、阅读理解和生成——共分为 12 项任务。
例如，经典 NLP 类别包含情感分析等任务，而生成任务则涵盖翻译的不同方面。
为确保这些类别能反映 NLP 研究和使用的重点与趋势，我们基于对 2006 年至 2024 年初菲律宾语言 NLP 研究的历史调查进行了整理。
（这些类别中的大部分内容专门包含非翻译内容，以确保忠实于菲律宾语言的自然使用。）

![](/images/posts/23ce571335ca.png)

- **文化知识**：此类别测试语言模型回忆事实性和特定文化信息的能力。对于文化知识，我们整理了一系列示例，用于测试 LLM 的区域和事实知识（Global-MMLU）、以菲律宾为中心的价值观念（KALAHI）以及词义消歧能力（StingrayBench）。
- **经典 NLP**：此类别涵盖各种信息提取和语言任务，例如命名实体识别、情感分析和文本分类，这些任务传统上由专门的、经过训练的模型执行。在此类别中，我们包含了来自 CebuaNER、TLUnified-NER 和 Universal NER 的命名实体识别实例，以及来自 SIB-200 和 BalitaNLP 的文本分类和情感分析子集。
- **阅读理解**：此类别评估语言模型理解和解释菲律宾语文本的能力，重点关注可读性、理解和自然语言推理等任务。在此类别中，我们包含了来自宿务语可读性语料库、Belebele 和 NewsPH NLI 的实例。
- **生成**：我们将 FilBench 的很大一部分用于测试 LLM 忠实翻译文本的能力，无论是从英语到菲律宾语，还是从宿务语到英语。我们包含了一组多样化的测试示例，范围涵盖文档（NTREX-128）、志愿者提供的现实文本（Tatoeba）和特定领域文本（TICO-19）。

每个类别都提供一个聚合指标。
为了创建一个单一的代表性分数，我们根据每个类别中的示例数量计算加权平均值，我们称之为 FilBench 分数。

为了简化使用和设置，我们在 Lighteval 之上构建了 FilBench，这是一个用于 LLM 评估的一体化框架。
对于特定语言的评估，我们首先为评估中常用的术语定义了从英语到塔加洛语（或宿务语）的翻译对，例如 "yes"（oo）、"no"（hindi）和 "true"（totoo）等。
然后，我们使用提供的模板为我们关心的能力实现了自定义任务。

FilBench 现已作为一组社区任务在官方的 Lighteval 代码库中提供！

## 我们从 FilBench 中学到了什么？

通过在 FilBench 上评估多个 LLM，我们揭示了关于它们在菲律宾语上表现的几个见解。

### 发现 #1：尽管特定区域的 LLM 仍落后于 GPT-4，但收集数据来训练这些模型仍然是一个有前景的方向

过去几年，我们看到针对东南亚语言的特定区域 LLM（SEA-specific）有所增加，例如 SEA-LION 和 SeaLLM。
这些是开放权重的 LLM，您可以从 HuggingFace 免费下载。
我们发现，对于我们的语言，SEA-specific LLM 通常是参数效率最高的，与其规模相当的其他模型相比，获得了最高的 FilBench 分数。
然而，最好的 SEA-specific 模型仍然被 GPT-4o 等闭源 LLM 超越。

![](/images/posts/ebed1e15fd01.png)

构建特定区域的 LLM 仍然有意义，因为我们观察到，当使用 SEA-specific 的指令微调数据持续微调一个基础 LLM 时，性能提升了 2-3%。
这表明，为微调整理菲律宾语/SEA-specific 训练数据的努力仍然具有相关性，因为它们可以带来 FilBench 上更好的性能。

### 发现 #2：菲律宾语翻译对 LLM 来说仍然是一项困难的任务

我们还观察到，在 FilBench 的四个类别中，大多数模型在生成能力方面都表现不佳。
在检查生成中的失败模式时，我们发现这些情况包括：模型未能遵循翻译指令、生成过于冗长的文本，或者产生幻觉（生成了塔加洛语或宿务语之外的其他语言）。

![](/images/posts/eceda076c595.png)

### 发现 #3：对于菲律宾语任务，开源 LLM 仍然是性价比高的选择

菲律宾的互联网基础设施往往有限，平均收入较低 [3]，因此需要成本效益和计算效率高的、易于获取的 LLM。
通过 FilBench，我们能够识别出处于效率帕累托前沿的 LLM。

总的来说，我们发现开放权重的 LLM（即可以从 HuggingFace 免费下载的模型）比商业模型便宜得多，且性能不逊色。
如果您想为您的菲律宾语任务寻找 GPT-4o 的替代品，那么试试 Llama 4 Maverick 吧！

![](/images/posts/95b03af34bcc.png)

我们也在 FilBench 排行榜的 HuggingFace 空间中提供了这些信息。

## 您的 LLM 在菲律宾语言上表现如何？在 FilBench 上试试吧！

我们希望 FilBench 能为 LLM 在菲律宾语言上的能力提供更深入的见解，并作为推动菲律宾 NLP 研究和发展的催化剂。
FilBench 评估套件建立在 Hugging Face 的 lighteval 之上，允许 LLM 开发者轻松地在我们的基准测试中评估他们的模型。
更多信息，请访问以下链接：

- 📄 论文：https://arxiv.org/abs/2508.03523
- 🖥️ GitHub：https://github.com/filbench/filbench-eval

## 致谢

作者感谢 Cohere Labs 通过 Cohere 研究资助提供积分以运行 Aya 模型系列，并感谢 Together AI 为运行多个开源模型提供的额外计算积分。
我们也感谢 Hugging Face 团队，特别是 OpenEvals 团队（Clémentine Fourrier 和 Nathan Habib）以及 Daniel van Strien，感谢他们对发布这篇博客文章的支持。

## 引用

如果您正在使用 FilBench 进行评估，请引用我们的工作：

```bibtex
@article{filbench,
  title={Fil{B}ench: {C}an {LLM}s {U}nderstand and {G}enerate {F}ilipino?},
  author={Miranda, Lester James V and Aco, Elyanah and Manuel, Conner and Cruz, Jan Christian Blaise and Imperial, Joseph Marvin},
  journal={arXiv preprint arXiv:2508.03523},
  year={2025}
}
```

---

> 本文由AI自动翻译，原文链接：[🇵🇭 FilBench - Can LLMs Understand and Generate Filipino?](https://huggingface.co/blog/filbench)
> 
> 翻译时间：2026-02-20 04:35
