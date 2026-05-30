---
title: KVPress：高效压缩KV缓存，解锁LLM长上下文
title_original: Mastering Long Contexts in LLMs with KVPress
date: '2025-01-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/kvpress
author: ''
summary: 本文介绍了大语言模型（LLM）中KV缓存随上下文窗口线性增长导致的内存瓶颈问题，并重点阐述了NVIDIA开发的KVPress工具包。KVPress通过集成多种先进的KV缓存压缩技术（如KnormPress、SnapKVPress），利用前向钩子剪枝重要性低的键值对，显著降低内存占用。文章还以Llama
  3-70B为例，展示了KV缓存可占70%总内存的严峻挑战，并指出KVPress可与量化方法结合，为研究人员和开发者提供了灵活高效的解决方案。
categories:
- AI基础设施
tags:
- KV缓存
- 长上下文
- 内存压缩
- NVIDIA
- LLM推理
draft: false
translated_at: '2026-05-30T05:45:46.707332'
---

# 使用KVPress掌握LLM中的长上下文

TL;DR：KVPress集成了最新的KV缓存压缩技术，实现了内存高效的长上下文LLM。🚀

大语言模型（LLM）的关键特性之一是其**上下文窗口**——即单次请求中可处理的最大Token数量。随着LLM的发展，其上下文窗口正变得越来越大。

更大的上下文窗口带来了令人难以置信的可能性：

- **上下文内检索**：在单个查询中无缝引用大量文本。
- **上下文内学习**：在同一会话中根据特定示例调整行为。
- **扩展推理**：处理极长的思维链而不会中断上下文。

然而，这些扩展的窗口是有代价的——KV缓存中长上下文占用的内存变得难以管理。例如，使用float16精度的Llama 3-70B处理100万Token需要**330GB**的KV缓存，这使得许多应用无法实现。

在这篇博客文章中，我们将探讨这一问题的解决方案：**压缩KV缓存**以实现更高效的生成。为此，我们将了解：

- 什么是KV缓存及其重要性。
- KVPress，NVIDIA开发的一款用于高效压缩KV缓存的强大工具包。
- KVPress的内部工作原理及其实现压缩的方式。

在开始之前，在此空间中探索KVPress（如有需要，文末可找到示例）：

## 什么是KV缓存及其重要性？

图1：注意力模块内的键值缓存（来源：NVIDIA）

![KV缓存](/images/posts/acbfea1a7574.png)

在自回归模型中，文本生成是**逐Token**进行的，每个预测都依赖所有前面的Token作为上下文。例如：

- 要生成第1000个Token，模型必须考虑第1到第999个Token的表示。
- 要生成第1001个Token，必须再次处理相同的信息（第1到第999个Token），以及第1000个Token。

随着序列增长，这种重复计算变得低效，尤其是对于大型模型。KV缓存通过存储注意力层的中间结果——键（K）和值（V）来优化这一过程，使模型可以重复使用这些结果用于后续Token，而无需重新计算。

## 问题：KV缓存及其线性扩展的负担

尽管KV缓存功能强大，但它有一个主要缺点——它随上下文窗口的大小线性扩展。虽然这乍听起来并不令人担忧，但让我们详细分析一下，看看为什么这成为一个严重的瓶颈。

### KV缓存的大小

KV缓存中存储的值来自模型使用的所有注意力块。因此，其大小取决于模型架构，而模型架构决定了注意力头的数量。更具体地说，KV缓存消耗的内存由以下公式决定：

Size(KV)=2×precision×n_layers×n_heads×d×n_tokens

这些因素中的每一个都导致了内存使用的爆炸性增长。为了更直观地理解，让我们考虑一个具体示例——以**bfloat16**精度（模型作者推荐）运行Llama 3-70B，上下文大小为100万Token：

Size(KV)=2×2×80×8×128×1M=327.6GB

由于bfloat16每个参数使用2字节，仅模型权重就需要140 GB（70B x 2字节）。这意味着，以100万Token的上下文大小运行该模型大约需要470 GB内存，其中仅KV缓存就占了总内存的惊人的70%。

## KVPress：KV缓存压缩工具包

正如我们所看到的，KV缓存既是部署具有长上下文窗口的大语言模型（LLM）的关键推动因素，也是一个重大瓶颈。解决线性扩展的内存问题需要创新的压缩技术，而这正是**KVPress**发挥作用的地方。

KVPress由NVIDIA开发，是一个Python工具包，旨在通过提供一套**最先进的压缩技术**来解决大型KV缓存的内存挑战。它还可以与其他方法集成，例如**KV缓存量化**，这是一种内置于transformers库中的减少内存使用的方法（上述公式中的精度项），进一步扩展了其实用性（详情请见此处）。

对于专门从事压缩的**研究人员**，KVPress提供了一个灵活且模块化的框架，使其易于理解并扩展新方法。对于**开发者**，KVPress简化了部署这些尖端技术的过程，实现了快速高效地集成到实际应用中。

## KVPress的实际应用

KVPress的核心利用**presses**，这些是专门设计用于减少KV缓存内存占用的高级压缩算法。

许多这些presses依赖于一个分数，该分数在每个头中用于剪枝重要性最低的KV对。例如，KnormPress剪枝键值范数最低的KV对（论文），SnapKVPress剪枝与最新查询的注意力权重较低的KV对（论文）。

这些presses通过前向钩子无缝集成到模型的注意力层中。

图2：KV压缩可视化（来源：NVIDIA）

![KVPress实际应用](/images/posts/5c9f6096fcfe.png)

在文本生成过程中，它们动态压缩KV缓存，减少内存使用而不影响模型生成连贯准确输出的能力。每个press都有一个**compression_ratio**属性，该属性决定了应用于KV缓存的压缩程度。

这些presses与自定义的transformers管道无缝集成，便于应用和实验。

以下是如何使用KVPress中的众多presses之一——ExpectedAttentionPress。该press剪枝与未来查询的预期注意力权重最低的KV对。

```py
from transformers import pipeline
from kvpress import ExpectedAttentionPress

pipe = pipeline(
"kv-press-text-generation",
model="meta-llama/Llama-3.1-8B-Instruct",
device="cuda",
model_kwargs={"attn_implementation": "sdpa"}
)

context = "一段你想要一次性压缩的非常长的文本"
question = "\n一个关于压缩后文本的问题"  

press = ExpectedAttentionPress(compression_ratio=0.5)
answer = pipe(context, question=question, press=press)["answer"]

```

尝试直接在此Hugging Face空间或此Google Colab笔记本中使用它！

通过针对**预填充**阶段，KVPress确保在缓存最大时进行压缩——有助于减少处理数万甚至数百万Token序列时的内存开销。

下图展示了随着提示长度增加，使用KVPress压缩所实现的GPU内存节省。对于较短的提示，大部分内存分配给模型权重——Llama 3.1 8B在bfloat16精度下约为15GB。然而，随着提示长度增长，KV缓存成为内存消耗的主要贡献者。对于128k上下文长度，应用压缩比为50%的KVPress可将峰值内存使用从45GB降至37GB。这种更小的KV缓存还提高了解码速度，在A100 GPU上从每秒11个Token提升到每秒17个Token（来源）。

图3：内存使用与上下文长度的关系（来源：NVIDIA）

![内存使用](/images/posts/ac98bbbac528.png)

# 基准测试

研究社区一直在积极开发各种KV缓存压缩技术。KVPress鼓励研究人员贡献他们的方法，并且已经提供了十多种presses。

为了评估这些压缩方法的表现，KVPress 提供了一个简单的命令行工具，用于在标准长上下文数据集（如 RULER、InfiniteBench 和 Loogle）上对其进行基准测试。下图展示了在 RULER 数据集上，使用 4k 上下文长度和不同压缩比时，9 种不同压缩方法的基准测试结果。在该数据集上表现最佳的压缩方法是 AdaKVPress（论文）与 ExpectedAttentionPress 的组合，后者是 KVPress 作者提出的一种尚未发表的新型剪枝技术（更多信息请点击此处）。

图 4：平均得分与压缩比（来源：NVIDIA）

![基准测试](/images/posts/17288b8e9499.png)

# 结论

LLM（大语言模型）不断增长的上下文窗口带来了新的可能性，但也因线性扩展的 KV 缓存而带来了显著的内存挑战。KVPress 通过在关键的预填充阶段压缩缓存来解决这一问题。

虽然 KVPress 提升了内存效率，但如基准测试图所示，更高的压缩比可能会影响模型精度。未来需要进一步研究，以开发更有效的压缩算法，从而尽量减少这种权衡。

凭借与 transformers 库的无缝集成以及模块化设计，KVPress 使研究人员和开发者能够高效处理长上下文 LLM（大语言模型），并设计新的压缩技术。它是一个实用的解决方案，可在不耗尽内存资源的情况下扩展 LLM（大语言模型），确保随着模型规模的增大，创新依然触手可及。

---

> 本文由AI自动翻译，原文链接：[Mastering Long Contexts in LLMs with KVPress](https://huggingface.co/blog/nvidia/kvpress)
> 
> 翻译时间：2026-05-30 05:45
