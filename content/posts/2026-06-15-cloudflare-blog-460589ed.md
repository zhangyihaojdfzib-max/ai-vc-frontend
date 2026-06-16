---
title: 吸纳Ensemble AI人才，壮大Cloudflare AI团队
title_original: Growing the Cloudflare AI team with talent from Ensemble AI
date: '2026-06-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/ensemble-ai-talent-joins-cloudflare/
author: ''
summary: Cloudflare宣布吸纳Ensemble AI团队核心成员，以增强其AI基础设施能力。Ensemble AI专注于模型压缩与高效推理技术，其开发的NdLinear等创新方法可降低大语言模型和多模态架构的内存与计算开销。此次整合将助力Cloudflare
  Workers AI平台提升推理效率、降低成本，使开发者能更经济、可靠地在全球范围内规模化运行AI模型。
categories:
- AI基础设施
tags:
- Cloudflare
- Ensemble AI
- 模型压缩
- 推理效率
- AI基础设施
draft: false
translated_at: '2026-06-16T07:23:36.135393'
---

# 吸纳Ensemble AI人才，壮大Cloudflare AI团队

2026年6月15日

- Alex Reneau
- Zach Albertson
- Michelle Chen

![](/images/posts/92fc2c31c137.png)

今天，我们很高兴地宣布，Ensemble AI团队的核心成员将加入Cloudflare，助力我们在AI基础设施领域的工作，让开发者能够更轻松地高效规模化运行强大的AI模型。

Ensemble AI于2023年在旧金山成立，过去几年一直专注于AI领域最重要的挑战之一：在不牺牲质量的前提下，让大型模型的推理更快、更小、更具成本效益。该团队开发了模型压缩和高效推理的新方法，旨在降低大语言模型和多模态架构的内存、计算和部署开销。

随着AI成为开发者构建应用的核心组成部分，推理的经济性比以往任何时候都更加重要。模型越来越大，工作负载越来越动态化。客户也日益期望AI能够无处不在：全球分布、快速、可靠且价格合理。将Ensemble AI团队引入Cloudflare，将增强我们实现这一目标的能力。

### 融入Ensemble的专业技术

Ensemble AI团队专注于在降低现代AI模型运行成本的同时，保留其内部结构。Ensemble没有将模型效率仅仅视为一个量化或硬件问题，而是探索了新的模型构建模块，这些模块可以在架构层面使神经网络更加紧凑和高效。

这项工作的核心是NdLinear，它是Transformer模型中标准线性层的即插即用替代方案，直接对多维激活进行操作，而不是扁平化结构。这使得模型能够保留有意义的轴，例如头、通道、空间维度或其他结构化表示，同时减少参数数量和计算量。Ensemble还开发了NdLinear-LoRA，这是一种高效的适配方法，旨在减少微调大型模型所需的可训练参数。

这些方法补充了其他效率技术，包括量化和向量量化。它们共同指向一个未来：开发者能够以显著更低的内存、计算和成本要求来运行强大的AI模型。

### 让AI推理更高效

Cloudflare Workers AI让开发者能够在Cloudflare全球网络上访问由GPU驱动的无服务器推理。随着开发者构建更多AI原生应用，高效服务模型的能力成为平台的关键组成部分。

推理成本是规模化AI应用的最大障碍之一。模型大小、内存占用、吞吐量和GPU利用率的每一次改进，都能让AI对开发者更可及，对客户更经济。这一点在AI工作负载从简单的文本生成扩展到Agent（智能体）、多模态模型、个性化、微调、检索和强化学习时尤为重要。

我们正在深化对核心机器学习能力的投入，以使Workers AI更快、更灵活、更具成本效益。这建立在我们现有提升模型效率的工作基础之上，包括我们的推理引擎Infire、张量压缩技术如Unweight，以及我们运行超大型语言模型的平台。该团队将专注于改善服务大语言模型及其他先进AI架构的经济性，重点放在模型效率、GPU利用率和可扩展部署上。

### 为下一代AI工作负载而构建

AI基础设施正进入一个新阶段。开发者不再仅仅需要访问模型；他们需要能够可靠、经济地运行模型且靠近用户的基础设施。他们需要能够尝试不同的模型大小、微调方法和部署模式，而不受成本或运营复杂性的阻碍。

Cloudflare在帮助解决这个问题方面具有独特优势。我们的全球网络、开发者平台和无服务器架构为我们提供了将AI更贴近应用运行环境的基础。Workers AI机器学习工程团队将帮助我们改善这一体验背后的效率层。

通过将Cloudflare的全球基础设施与Ensemble在模型压缩和高效架构方面的工作相结合，我们可以继续构建一个平台，让开发者能够以更低的成本、更好的性能和更少的运营开销来部署AI应用。

### 下一步计划

我们将携手继续构建所需的基础设施，让AI对全球开发者更高效、更可及、更有用。我们的目标很简单：帮助开发者在全球范围内规模化运行强大的AI工作负载，同时改善Cloudflare平台上推理的经济性。如果你想加入我们的使命，请查看我们的招聘页面。

---

> 本文由AI自动翻译，原文链接：[Growing the Cloudflare AI team with talent from Ensemble AI](https://blog.cloudflare.com/ensemble-ai-talent-joins-cloudflare/)
> 
> 翻译时间：2026-06-16 07:23
