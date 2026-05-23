---
title: Nemotron扩散模型：迈向光速文本生成
title_original: Towards Speed-of-Light Text Generation with Nemotron-Labs Diffusion
  Language Models
date: '2026-05-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/nemotron-labs-diffusion
author: ''
summary: Nemotron-Labs Diffusion系列模型打破了传统自回归语言模型逐Token生成的瓶颈，通过扩散语言模型实现并行生成与迭代优化。该模型支持自回归、扩散和自推测三种模式，在保持准确率的同时，推理速度提升至自回归模型的2.6至6.4倍。基于持续预训练和逐块注意力机制，它兼容KV缓存，为延迟敏感型应用提供了高效、灵活的文本生成方案。
categories:
- AI研究
tags:
- 扩散语言模型
- Nemotron
- 文本生成
- 推理加速
- 自推测解码
draft: false
translated_at: '2026-05-23T05:39:20.597902'
---

# 迈向光速文本生成：Nemotron-Labs扩散语言模型

![1-headline-final](/images/posts/f3bbe3fa69a1.gif)

大语言模型（LLM）已成为代码生成、数学问题求解、摘要、文档理解以及许多其他开发者工作流的默认接口。然而在底层，许多LLM仍然以相同的方式生成文本：一次生成一个Token，且每个Token依赖于它之前出现的Token。因此，这些模型被称为自回归模型，因为它们会消耗自身的输出。

这种自回归（AR）方法取得了显著成功。它训练稳定、部署简单，并且是现代语言建模取得大部分进展的原因。但它也带来了一个硬性限制：每个新Token都需要一次完整的模型前向传播，并且在计算开始之前，每个权重都必须从内存中加载。对于构建延迟敏感型应用、运行较小批次大小或试图更好利用现代GPU的开发者来说，逐Token生成可能会让性能无法充分发挥，因为GPU的大部分时间都花在内存操作上，而非计算上。

此外，一旦自回归模型生成了一个Token，它就是最终结果，模型本身不具备修改先前Token的能力。因此，错误可能会在生成过程中传播。

Nemotron-Labs Diffusion开辟了一条新路径：扩散语言模型（DLM），其工作原理是并行生成多个Token，然后在多个步骤中迭代优化已生成的Token。这些模型不仅能更好地利用现代GPU的计算模型，提供显著的运行时性能优势，还能修改已生成的Token，使其更适合修改现有文本和处理中间填充目标。这种生成与优化的特性还提供了一种内置方式来控制推理预算。通过减少优化步骤的数量，可以降低这些模型在运行时的计算需求。

## 模型、训练方案和技术报告的快速链接

Nemotron-Labs Diffusion系列包括3B、8B和14B规模的文本模型，均采用商业友好的NVIDIA Nemotron开放模型许可证发布，以及一个8B规模的视觉语言模型（VLM），采用NVIDIA源代码许可证发布，赋予广泛的研究灵活性。在整个产品线中，NVIDIA同时发布了基础模型和经过指令调优的对话变体。NVIDIA还通过NVIDIA Megatron Bridge框架发布了训练这些模型的代码。

- HuggingFace上的NVIDIA Nemotron-Labs Diffusion模型集合
- GitHub上的训练方案和代码
- 技术报告

## 一个模型中的三种生成模式

![2-tri-mode-final](/images/posts/023b6e11abe0.gif)

Nemotron-Labs Diffusion围绕一个简单理念设计：自回归生成和扩散生成不应是独立的模型家族，而应是同一模型的能力。该模型支持三种生成模式：

**自回归模式**像标准的从左到右LLM一样运行。这保持了与开发者已经熟悉的生成工作流的兼容性。

**扩散模式**逐块生成，在多个步骤中逐步生成Token。

**自推测模式**使用扩散来草拟多个候选Token，然后使用自回归解码来验证它们。这结合了扩散式草拟的速度潜力与AR验证的可靠性。

这种灵活设计是面向开发者的关键特性，在速度和准确性都至关重要的场景中尤其有价值，即使是在批次大小不可预测的工作负载或单查询（批次大小=1）场景下也是如此。选择所需的推理模式几乎不需要在应用层面进行任何更改，因为这是一个部署时的设置。因此，开发者可以无缝切换他们当前使用的模型，或使用不同推理模式的Nemotron-Labs Diffusion来实现超快生成速度。

## 性能亮点

![Screenshot from 2026-05-22 15-49-43](/images/posts/1090cb6f03de.png)

与Qwen3 8B相比，Nemotron-Labs Diffusion 8B的平均准确率提升了1.2%。比较以每次前向传播生成的Token数（简称TPF，一种衡量Token解码效率的硬件无关指标）衡量的推理速度，扩散模式达到的TPF是AR模型的2.6倍，而自推测模式进一步将其提升至线性自推测的6倍和二次自推测的6.4倍，同时在评估任务上保持了相当的准确率。

## 我们如何训练Nemotron-Labs Diffusion

扩散语言模型多年来一直前景广阔，但历史上存在实际障碍：准确率低于强大的AR模型、训练更困难，以及与KV缓存的兼容性有限。

最近的研究改变了这一方向。Efficient-DLMs表明，通过持续预训练并将注意力机制改为逐块方式，可以将预训练的AR模型转换为扩散语言模型。这种设计有助于保留AR模型的能力，同时实现支持KV缓存的并行解码。

Nemotron-Labs Diffusion基于相同的实践洞察：为现有AR模型添加扩散能力。该模型使用联合AR和扩散目标进行训练，使其能够保留在初始AR训练中学到的知识，同时扩散增加了并行草拟能力。该模型在来自NVIDIA Nemotron预训练数据集的1.3T Token上进行了预训练，并使用来自NVIDIA Nemotron后训练数据集的45B Token进行了额外的监督微调阶段。

## 通过SGLang进行部署和推理

Nemotron-Labs Diffusion模型的部署将很快在SGLang的主分支中得到支持。在撰写本文时，推理支持可通过GitHub上的此问题跟踪请求获得。

巧妙之处在于，该集成允许你以三种不同方式提供同一检查点的服务，只需在算法配置中设置一行代码即可选择：

- **纯自回归模式** - 设置`ar_mode=true`，模型的行为与任何其他因果LM相同。可用作正确性参考，或者如果你只想对纯AR输出进行合理性检查。
- **扩散模式（FastDiffuser）** - 原始吞吐量的主打功能。模型通过迭代去噪一次填充一个32-Token块，置信度阈值决定哪些Token在每个步骤中"足够好"可以提交。
- **自推测模式（LinearSpec）** - 这是我们最喜欢的模式。同一模型双向草拟一个块，然后因果验证它；任何匹配的前缀都会被提交。在温度为0时，输出与AR相比无损，但在B200上的speedbench数据集上，我们达到了约865 tok/s——大约是同一硬件上自回归基线的4倍。

## 立即开始使用

Nemotron-Labs Diffusion将扩散式生成转化为开发者可以实际使用的形式：开放模型、熟悉的AR兼容性、扩散解码以及自推测加速，全部集成在一个系列中。借助Nemotron-Labs Diffusion，开发者获得了一种草拟、优化、验证和加速文本生成的新方式，而无需修改他们的应用。

要开始使用，请探索 Nemotron-Labs 扩散模型系列、阅读技术报告，并尝试可用的训练方案。

---

> 本文由AI自动翻译，原文链接：[Towards Speed-of-Light Text Generation with Nemotron-Labs Diffusion Language Models](https://huggingface.co/blog/nvidia/nemotron-labs-diffusion)
> 
> 翻译时间：2026-05-23 05:39
