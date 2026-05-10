---
title: Aya Vision：多语言多模态AI新突破
title_original: 'A Deepdive into Aya Vision: Advancing the Frontier of Multilingual
  Multimodality'
date: '2025-03-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/aya-vision
author: ''
summary: Cohere For AI发布Aya Vision系列视觉语言模型（8B和32B参数），旨在解决多语言多模态AI的挑战。该模型基于Aya Expanse，通过合成标注、数据扩展和多模态融合等技术，在23种语言的图像描述、视觉问答等任务上表现优异。32B模型在多个基准上超越参数规模两倍以上的竞品，8B模型在其参数类别中实现最佳性能。模型以开源权重发布，加速多语言多模态研究。
categories:
- AI研究
tags:
- 多模态模型
- 多语言AI
- 视觉语言模型
- 开源模型
- Cohere
draft: false
translated_at: '2026-05-10T05:37:06.494526'
---

# 深入解读 Aya Vision：推动多语言多模态前沿发展

随着 Aya Vision 系列（我们全新的 8B 和 32B 参数视觉语言模型）的发布，我们正在解决 AI 领域最大的挑战之一：将多语言能力引入多模态模型。

Aya Vision 是 Cohere For AI 最新的开源权重多语言多模态模型系列，旨在为 23 种语言的视觉与语言理解提供强大基础。该系列建立在 Aya Expanse（最先进的多语言语言模型）的成功基础之上，并通过结合多种先进技术进行扩展。这些技术包括合成标注、通过翻译和改写扩展多语言数据，以及多模态模型融合——这些关键方法在多语言环境下同时提升了语言和视觉理解能力。

因此，我们的模型在多种任务中表现出色，包括图像描述、视觉问答、文本生成，以及将图像和文本翻译成清晰的自然语言文本。我们在多个数据集上评估了 Aya Vision 模型，包括我们全新的开放式视觉语言基准 AyaVisionBench 以及翻译成 23 种语言的多语言版 Wild Vision Bench（mWildVision），这两个数据集均已发布供研究使用。

在成对比较中，Aya Vision 32B 在 AyaVisionBench 上以 50% 至 64% 的胜率，在 23 种语言的 mWildVision 平均胜率上以 52% 至 72% 的胜率，超越了其参数规模两倍以上的模型，如 Llama-3.2 90B Vision、Molmo 72B 和 Qwen2.5-VL 72B。

![aya vision 胜率](/images/posts/64281576c11a.png)

我们紧凑且更高效的模型 Aya Vision 8B 在其参数类别中实现了最佳的多语言多模态性能，在 AyaVisionBench 上以高达 79% 的胜率，在 mWildBench 上以 81% 的胜率，超越了 Qwen2.5-VL 7B、Pixtral 12B、Gemini Flash 1.5 8B、Llama-3.2 11B Vision、Molmo-D 7B 和 Pangea 7B 等领先模型。

![效率与性能权衡](/images/posts/7c90dfcb4510.png)

我们以开源权重形式发布了 8B 和 32B 两个模型，供研究社区使用，以进一步加速多语言多模态领域的发展。在本篇博客中，我们将分享 Aya Vision 模型背后的关键技术细节。

## Aya Vision 架构与训练

![aya vision 架构](/images/posts/d6db98c7a449.png)

对于高性能视觉语言模型而言，处理任意分辨率的图像（尤其是高分辨率图像）至关重要。为了实现这一能力，Aya Vision 采用动态调整大小和分割方法，将任何高分辨率图像拆分为多个图块，从而从图像编码器中生成丰富的图像特征。在 Aya Vision 模型中，我们使用最近发布的 SigLIP2-patch14-384 模型作为视觉编码器的初始化。

虽然动态调整大小能够处理高分辨率图像，但也会导致通过视觉语言连接器和 LLM 解码器的图像 Token 数量增加。为了改善延迟和吞吐量，我们采用了一种名为 Pixel Shuffle 的下采样方法，将图像 Token 数量压缩 4 倍。下采样后，图像 Token 通过视觉语言连接器与语言模型输入嵌入对齐，并传递至 LLM 解码器。

对于文本解码器，我们使用多语言语言模型。对于 Aya Vision 8B，我们使用从 Cohere Command R 7B 初始化的 LLM，以提升指令遵循能力和世界知识，并采用 Aya Expanse 方案（包括多样化多语言数据、模型融合和偏好训练）进行进一步后训练。对于 Aya Vision 32B，我们基于 Aya Expanse 32B 初始化语言模型，因其具有最先进的多语言性能。

### 训练过程

我们分两个阶段训练 Aya Vision 模型：视觉语言对齐和监督微调（SFT）。在视觉语言对齐阶段，仅训练视觉语言连接器，而视觉编码器和语言模型权重保持冻结。这通过将图像编码器特征映射到语言模型嵌入空间，实现基础的视觉语言理解。在 SFT 阶段，我们在 23 种语言的多样化多模态任务上同时训练连接器和语言模型。

![逐步改进](/images/posts/2721ee266a94.png)

## 多模态数据增强与语言覆盖扩展

![多语言合成标注](/images/posts/b7518d3dd986.png)

开发多语言视觉语言模型的最大挑战之一，是确保在代表性不足的语言上也能表现出色。为解决这一问题，我们首先使用多样化的高质量英文数据集收集合成标注，这为我们的多语言多模态标注奠定了基础。在英文数据集的合成标注之后，我们将大量数据翻译成 23 种语言。为避免翻译痕迹并保持流畅的文本特征及高精度答案，我们随后将翻译后的提示词/生成对与原始高质量合成样本进行匹配改写，从而在真实世界数据集稀缺的语言上扩展覆盖范围。这既提升了语言流畅性，也增强了视觉与文本之间的对齐，使 Aya Vision 在多种语言中展现出卓越的图像理解能力。

我们的 8B 模型仅使用原始学术数据集进行监督微调时，在 AyaVisionBench 上对 Pangea 7B（一个多语言 VLM）的 23 种语言平均胜率为 40.9%，而采用合成标注并扩展多语言数据后，胜率提升至 58.1%，提高了 17.2%。这一显著改进展示了在多语言数据覆盖方面大量投入所带来的影响。

## 多模态模型融合

![多模态融合](/images/posts/0afaf4e80308.png)

最先进的视觉语言模型不仅应在图像理解方面表现出色，还应具备对话上下文能力，即模型需对图像和文本输入生成高质量响应。为解决这一问题，受我们先前关于模型融合（一种结合多个训练模型的技术）研究的启发，我们将基础语言模型与微调后的视觉语言模型进行融合。

模型融合增强了最终模型的生成能力，使得在 AyaVisionBench 上对 Pangea 7B 的 23 种语言平均胜率达到 70%，与融合前相比，多模态胜率提升了 11.9%。

多模态模型融合还使我们的 Aya Vision 模型在纯文本任务中表现出色，这一点在 mArenaHard 数据集上与其他领先视觉语言模型的比较中得到了验证。

![阶段](/images/posts/b9c39b4bfac4.png)

## 扩展至 32B

最后，我们将方案从 8B 扩展至 32B，从而打造出最先进的开源权重多语言视觉语言模型——Aya Vision 32B。由于文本骨干网络的初始化更强，该模型在胜率上展现出显著提升，在 AyaVisionBench 上以 49% 至 63% 的胜率，在 23 种语言的 mWildVision 平均胜率上以 52% 至 72% 的胜率，超越了其参数规模两倍以上的模型，如 Llama-3.2 90B Vision、Molmo 72B 和 Qwen2.5-VL 72B。

![aya vision 基准](/images/posts/8559d5257e5a.png)

## Aya Vision 基准——多语言评估数据集

与 Aya Vision 模型一同发布的，还有一个名为 AyaVisionBench 的高质量多语言视觉语言基准。该基准基于实际应用场景构建，涵盖 23 种语言和 9 个不同的任务类别，每种语言包含 135 个图像-问题对。

我们将此评估集提供给研究社区，以推动多语言多模态评估的发展。该数据集旨在评估模型执行多种视觉-语言任务的能力，包括图像描述、图表与图形理解、两幅图像差异识别、通用视觉问答、OCR、文档理解、文本转录、涉及逻辑与数学的推理，以及将截图转换为代码。通过整合多种语言和任务类型，该数据集为评估跨语言和多模态理解提供了一个广泛且具有挑战性的评估框架。

为创建此数据集，我们首先从Cauldron保留测试集中选取了图像，该测试集源自50个高质量数据集，确保这些图像在训练过程中未被使用。随后，我们为每张图像生成了一个明确需要视觉上下文才能回答的对应问题。这些问题通过合成方式生成，并经过两阶段验证流程进行优化。首先，人工标注员对每个问题进行了审查和验证，确保其清晰、相关且确实依赖于图像。这一严格的筛选和验证流程确保了该数据集可作为评估多语言及真实场景下视觉-语言模型的稳健基准。

## 专为真实应用设计

沟通以多种形式和语言进行。凭借我们领先的研发成果，我们发布了一款模型，能够以23种不同语言促进文本或视觉层面的连接。

Aya Vision具有广泛的实际应用场景，其中一个显著例子是其在WhatsApp上的可用性——这是全球使用最广泛的通信平台之一。这使得使用多种语言的广大全球受众能够在一个他们日常沟通的平台上利用Aya Vision的能力。

## 开始使用Aya

开始使用：

从Hugging Face上的Aya Vision集合中下载权重和数据集。通过我们的Hugging Face空间试用Aya Vision，或在WhatsApp上发送消息。使用我们的Colab示例基于Aya进行开发。

了解更多关于我们在多语言方面的持续努力。

## 致谢

此项工作离不开核心Aya Vision技术团队的支持：

Saurabh Dash、Oliver Nan、John Dang、Arash Ahmadian Dehkordi、Shivalika Singh、Alejandro Salamanca、Bharat Venkitesh、Vlad Shmyhlo、Walter Beller-Morales、Jeremy Pekmez、Jason Ozuzu、Madeline Smith、Marzieh Fadaee、Manoj Govindassamy、Sudip Roy、Matthias Gallé、Beyza Ermis、Ahmet Üstün、Sara Hooker。

同时，此项工作也离不开以多种方式提供支持的更广泛的Cohere For AI和Cohere团队。特别感谢Sungjin Hong、Michael Kozakov、Pierre Richemond、Brittawnya Prince、Jim Payne、Kyle Lastovica、Jeff Colen、Jenna Cook、Viraat Aryabumi、Trent Fowler、Linus Chui、Meor Amer、Lucas Fayoux、Kyle Lastovica、Billy Trend、Acyr Locatelli、Morgan Norman、Florian Strub、Jon Ander Campos、Nick Frosst、Phil Blunsom、Aidan Gomez、Ivan Zhang。

特别感谢Hugging Face协助促成此事：Yoni Gozlan、Arthur Zucker、Pedro Cuenca、Aritra Roy Gosthipaty、Merve Noyan、Vaibhav Srivastav。

## 参考文献

[1]Aya Expanse: Combining Research Breakthroughs for a New Multilingual Frontier  
[2]Pangea: A Fully Open Multilingual Multimodal LLM for 39 Languages  
[3]WildVision: Evaluating Vision-Language Models in the Wild with Human Preferences  
[4]SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features  
[5]What matters when building vision-language models?  
[6]Molmo and PixMo: Open Weights and Open Data for State-of-the-Art Vision-Language Models  
[7]How Far Are We to GPT-4V? Closing the Gap to Commercial Multimodal Models with Open-Source Suites

---

> 本文由AI自动翻译，原文链接：[A Deepdive into Aya Vision: Advancing the Frontier of Multilingual Multimodality](https://huggingface.co/blog/aya-vision)
> 
> 翻译时间：2026-05-10 05:37
