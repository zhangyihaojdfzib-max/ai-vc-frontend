---
title: Falcon-Arabic：70亿参数阿拉伯语大模型，性能超越同类四倍规模模型
title_original: 'Falcon-Arabic: A Breakthrough in Arabic Language Models'
date: '2025-05-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/tiiuae/falcon-arabic
author: ''
summary: 本文介绍了由阿联酋技术创新研究所（TII）推出的Falcon-Arabic大语言模型。该模型基于Falcon 3-7B架构，通过添加3.2万个阿拉伯语专用Token和创新的嵌入初始化策略进行适配，并在100%阿拉伯语原生数据集上进行持续预训练。Falcon-Arabic支持3.2万Token上下文窗口，在通用知识、语法、数学推理及方言理解方面表现卓越，其性能在同类阿拉伯语LLM中领先，甚至优于规模大四倍的模型，为阿拉伯语AI应用提供了高效、先进的解决方案。
categories:
- AI研究
tags:
- 大语言模型
- 阿拉伯语AI
- Falcon
- 多语言模型
- 自然语言处理
draft: false
translated_at: '2026-04-16T04:55:48.952720'
---

# Falcon-Arabic：阿拉伯语大语言模型的突破

![image/png](/images/posts/0c511eb74ca6.png)

查看我们的官方博客文章（英文，阿拉伯文）

我们很高兴推出 **Falcon-Arabic**，这是一个拥有 70 亿参数的大语言模型，为阿拉伯语自然语言处理树立了新的标杆。Falcon-Arabic 基于 Falcon 3 架构构建，是一个支持阿拉伯语、英语及其他多种语言的多语言模型。它在通用知识、阿拉伯语语法、数学推理、复杂问题解决以及理解阿拉伯语方言的丰富多样性方面表现出色。Falcon-Arabic 支持 32,000 个 Token 的上下文窗口，使其能够处理长文档，并支持诸如检索增强生成（RAG）、深度内容创作和知识密集型任务等高级应用。

Falcon-Arabic 重新定义了阿拉伯语大语言模型的可能性边界。在其规模类别中，它显著超越了其他阿拉伯语 LLM，甚至在阿拉伯语原生模型以及从其他语言适配而来的模型中，其性能也优于那些规模大至四倍的模型。这使得 Falcon-Arabic 不仅在性能上是一个最先进的模型，而且对于使用阿拉伯语的开发者和研究人员来说，也是一个独特高效且易于获取的解决方案。

## 🚀 介绍 Falcon-Arabic：为阿拉伯语世界推进 LLM 发展

近年来，大语言模型（LLM）已经改变了人工智能，为翻译、内容创作、虚拟助手等工具提供了动力。然而，这些进展大多集中在英语等高代表性语言上，使得阿拉伯语等语言代表性不足。阿拉伯语带来了独特的挑战：它形态丰富，是双言制语言（涵盖现代标准阿拉伯语和多样化的地区方言），并且被庞大且文化多样的人群使用。开发强大的阿拉伯语 LLM 对于确保阿拉伯语社区充分融入人工智能革命至关重要。

怀着这个目标，我们推出 **Falcon-Arabic**，这是由阿联酋**技术创新研究所（TII）** 开发的 **Falcon 3** 模型系列的一个专门适配版本。Falcon 模型因其多语言能力和开源方法而获得了全球认可。Falcon-Arabic 在此基础上发展，为阿拉伯语带来了先进的语言理解和生成能力。通过训练模型同时处理现代标准阿拉伯语和主要方言，Falcon-Arabic 填补了语言技术中的一个关键空白，使得在海湾地区、中东和北非能够实现更自然、智能和包容的阿拉伯语人工智能。

![image/png](/images/posts/e26f570b0dac.png)

## 🦅 Falcon-Arabic 已问世 - 以下是其训练配方 🧪

构建 Falcon-Arabic 始于一个战略决策：我们选择适配一个强大的多语言基础模型，而不是从头开始训练。在阿拉伯语 LLM 领域，存在三种主要方法：从头开始训练（例如 Jais-native）、适配多语言模型（如 Allam 或 Fanar），或者使用原生支持阿拉伯语及其他语言的模型（如 Qwen 或 LLaMA）。观察**开放阿拉伯语 LLM 排行榜**，可以清楚地看到，适配模型和多语言模型在效率和能力方面始终优于其他模型。为了延续这一势头，我们选择了 **Falcon 3-7B**，这是由**技术创新研究所（TII）** 开发的 Falcon 3 系列中，在性能和资源效率之间取得实际平衡的模型。

核心挑战在于适配 **Falcon 3-7B**，该模型最初在分词器和嵌入层面缺乏阿拉伯语支持。我们通过向分词器词汇表中添加 **32,000 个阿拉伯语专用 Token**，并应用一种基于**文本相似度**的**新颖嵌入初始化策略**来解决这个问题。该技术将新的阿拉伯语 Token 映射到现有词汇表中语义相关的嵌入上，使模型能够继承先验知识并加速学习，特别是在情感、抽象概念和推理模式方面。这为 Falcon-Arabic 在理解和生成高质量阿拉伯语文本方面提供了先发优势。

分词器和嵌入准备就绪后，我们开始在高质量的、**100% 阿拉伯语原生数据集**上进行**持续预训练**，避免使用机器翻译内容，以最小化文化偏见并保持语言真实性。训练遵循**多阶段课程**：早期阶段侧重于**通用知识和富含方言的阿拉伯语内容**，以稳定模型并增强逻辑能力；后期阶段则强调**数学、代码和推理**。最终得到的模型不仅能够流利地使用各种方言进行阿拉伯语交流，还保留了 Falcon 的多语言和推理优势，为阿拉伯语优先的人工智能拓展了边界。

### 预训练模型平均性能

![image/png](/images/posts/f8cb231a562d.png)

## 📊 Falcon-Arabic：提升阿拉伯语 LLM 的标准

我们在 **OALL v2**（阿拉伯语大语言模型的主要基准测试）上评估了 Falcon-Arabic。它包括六项选择题任务，如阿拉伯语 MMLU（原生和翻译）、阿拉伯语考试、Alghafa、MadinahQA、Aratrust，以及一项生成式基准测试 Alrage。**Falcon-Arabic 在其规模范围内超越了所有现有的阿拉伯语 LLM，甚至超过了规模大至 4 倍的模型**。它在阿拉伯语 MMLU、考试、MadinahQA 和 Aratrust 等关键基准测试中领先，为阿拉伯语优先的大语言模型树立了新标准。

![image/png](/images/posts/894931436478.png)

### 预训练模型对比表

![image/png](/images/posts/f3b7ba9cd415.png)

**Falcon-Arabic-7B-Base** 的评估详情（对数概率、预测和 LLM 作为评判指标）可在 https://huggingface.co/datasets/tiiuae/Falcon-Arabic-7B-Base-details 获取。

## 🗣️ 从预训练到指令调优：对齐 Falcon-Arabic 以进行对话

在完成基础模型训练后，我们进行了**训练后对齐**阶段，以根据人类偏好微调 Falcon-Arabic 的响应。此阶段始于**监督微调（SFT）**，使用了高质量公共数据集和内部收集的**阿拉伯语原生指令数据**的组合，涵盖了一系列任务和对话场景。

为了进一步增强对齐效果，我们应用了**直接偏好优化（DPO）**，这是一种基于强化学习的方法，用于调整模型，使其偏好人类评价为更有帮助、更安全和更相关的输出。这个两步过程确保了 Falcon-Arabic Instruct 不仅能够很好地理解阿拉伯语，而且能够以符合真实用户期望的方式做出回应。

### 指令模型平均性能

![image/png](/images/posts/9c517604d742.png)

如结果图所示，**Falcon-Arabic Instruct 处于领先地位**，在其规模类别中超越了所有其他经过指令对齐的阿拉伯语 LLM，甚至在多个基准测试中超越了规模显著更大的模型。该模型在遵循指令和开放式对话方面都表现出强大的性能，为阿拉伯语对话式人工智能树立了新标准。

### 指令模型按基准测试的性能

![image/png](/images/posts/f77ca7628eae.png)

### 对话模型对比表

![image/png](/images/posts/49d1a5d9b593.png)

**Falcon-Arabic-7B-Instruct** 的评估详情（对数概率、预测和 LLM 作为评判指标）可在 https://huggingface.co/datasets/tiiuae/Falcon-Arabic-7B-Instruct-details 获取。

## 🔓 释放阿拉伯语人工智能的潜力

Falcon-Arabic 为阿拉伯语大语言模型树立了新的标杆。凭借仅 70 亿参数，它提供了最先进的性能，在阿拉伯语 MMLU、MadinahQA 和 Aratrust 等关键基准测试中超越了相似规模的模型，甚至超越了规模大数倍的模型。它结合了对现代标准阿拉伯语的流利掌握、对地区方言的深刻理解以及强大的推理和多语言能力，使其成为广泛应用的理想选择：从阿拉伯语优先的聊天机器人和教育工具，到内容生成、代码辅助和文档理解。

为了让您亲身体验Falcon-Arabic的能力，我们构建了一个简单的演示，展示其在**机器翻译**方面的能力——尽管该模型并未专门针对此任务进行微调。该工具完全基于**Falcon-7B-Arabic-Instruct**运行，结果在各种翻译方向上表现出惊人的强大。您可以通过下方链接的演示亲自尝试。事实上，我们使用相同的设置将这篇博客文章翻译成了阿拉伯语，以服务于我们的阿拉伯语受众。请点击**此处**查看🚀。如果您想探索更多，我们还提供了一个实时**演示平台**，您可以在其中与Falcon-Arabic Instruct互动，体验其在不同任务上的表现✨。

## ⚠️ 局限性

与所有大语言模型一样，Falcon-Arabic也继承了一些常见的局限性。这些包括偶尔出现的**幻觉**（产生看似合理但不正确的输出）、**对提示词表述方式的敏感性**，以及在处理非常长的上下文时性能表现不一。虽然Falcon-Arabic旨在减少这些问题，特别是针对阿拉伯语任务，但用户在解读结果时仍应运用批判性思维，尤其是在高风险或对事实敏感的用例中。

## 引用

如果您发现这项工作对您的研究或项目有帮助，请考虑引用它。

```latex
@misc{falcon-arabic,
    title = {Falcon-Arabic: A Breakthrough in Arabic Language Models},
    author = {Falcon-LLM Team},
    month = {May},
    url = {https://falcon-lm.github.io/blog/falcon-arabic},
    year = {2025}
}
```

---

> 本文由AI自动翻译，原文链接：[Falcon-Arabic: A Breakthrough in Arabic Language Models](https://huggingface.co/blog/tiiuae/falcon-arabic)
> 
> 翻译时间：2026-04-16 04:55
