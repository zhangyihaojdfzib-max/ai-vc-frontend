---
title: Transformers库：迈向模型定义标准化与跨框架互操作
title_original: 'The Transformers Library: standardizing model definitions'
date: '2025-05-15'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/transformers-model-definition
author: ''
summary: 本文介绍了Hugging Face Transformers库的发展愿景，即成为机器学习生态系统中模型定义的标准化枢纽。文章指出，Transformers已支持300多种模型架构，并与主流训练框架（如Axolotl、DeepSpeed）和推理引擎（如vLLM、TGI）深度集成，实现了“一次贡献，多处可用”的互操作性目标。未来，团队将致力于简化模型贡献流程、统一API设计，并淘汰冗余组件，以降低社区贡献门槛，减少生态碎片化，推动整个领域的高效协作与发展。
categories:
- AI基础设施
tags:
- Transformers库
- 模型标准化
- 机器学习框架
- 模型部署
- 开源生态
draft: false
translated_at: '2026-04-18T04:36:29.160971'
---

# Transformers库：标准化模型定义

TLDR：展望未来，我们的目标是让Transformers成为跨框架的枢纽：如果一个模型架构被Transformers支持，你可以预期它在生态系统的其他部分也能得到支持。

Transformers创建于2019年，紧随BERT Transformer模型的发布。自那时起，我们持续致力于添加最先进的架构，最初专注于NLP，随后扩展到音频和计算机视觉领域。如今，Transformers已成为Python生态系统中LLM和VLM的默认库。

Transformers目前支持300多种模型架构，平均每周新增约3个新架构。我们一直致力于及时发布这些架构；对于最受追捧的架构（如Llamas、Qwens、GLMs等），我们实现了发布当日（day-0）支持。

## 一个模型定义库

随着时间的推移，Transformers已成为机器学习生态系统的核心组件，在模型多样性方面成为最完整的工具包之一；它已集成到所有流行的训练框架中，如Axolotl、Unsloth、DeepSpeed、FSDP、PyTorch-Lightning、TRL、Nanotron等。

最近，我们一直与最流行的推理引擎（vLLM、SGLang、TGI等）紧密合作，让它们使用Transformers作为后端。其带来的价值是显著的：一旦一个模型被添加到Transformers，它就会在这些推理引擎中可用，同时还能利用每个引擎提供的优势：推理优化、专用内核、动态批处理等。

例如，以下是如何在vLLM中使用Transformers后端：

```python
from vllm import LLM

llm = LLM(model="new-transformers-model", model_impl="transformers")

```

只需如此，新模型就能享受vLLM提供的超快速、生产级服务！

更多信息请参阅vLLM文档。

我们也一直与llama.cpp和MLX非常紧密地合作，以确保Transformers与这些建模库之间的实现具有良好的互操作性。例如，得益于社区的巨大努力，现在可以非常轻松地将GGUF文件加载到Transformers中进行进一步的微调。反之，Transformers模型也可以轻松转换为GGUF文件，以便与llama.cpp一起使用。

MLX也是如此，Transformers的safetensors文件与MLX的模型直接兼容。

我们非常自豪地看到Transformers格式正被社区采纳，带来了我们都能受益的互操作性。用Unsloth训练模型，用SGLang部署它，然后导出到llama.cpp在本地运行！我们旨在继续支持社区向前发展。

## 致力于更简单的模型贡献

为了让社区更容易地将Transformers用作模型定义的参考，我们致力于显著降低模型贡献的门槛。我们为此努力了几年，但在接下来的几周内将显著加速：

- 每个模型的建模代码将进一步简化；为最重要的组件（KV缓存、不同的注意力函数、内核优化）提供清晰、简洁的API。
- 我们将弃用冗余组件，转而采用简单、单一的方式来使用我们的API：通过弃用慢速分词器来鼓励高效分词，并类似地使用快速的向量化视觉处理器。
- 我们将继续加强围绕模块化模型定义的工作，目标是使新模型所需的代码更改量绝对最小化。6000行的贡献、为新模型更改20个文件的时代已经过去。

## 这对您有何影响？

### 对于作为模型用户的您意味着什么

作为模型用户，未来您应该在您使用的工具中看到更多的互操作性。

这并不意味着我们打算在您的实验中锁定您使用Transformers；相反，这意味着得益于这种建模标准化，您可以期望您用于训练、推理和生产的工具能够高效地协同工作。

### 对于作为模型创建者的您意味着什么

作为模型创建者，这意味着一次贡献就能让您的模型在所有集成了该建模实现的下游库中可用。多年来我们已经多次看到这种情况：发布一个模型压力很大，并且集成到所有重要的库中通常非常耗时。

通过以社区驱动的方式标准化模型实现，我们希望降低跨库对该领域贡献的门槛。

我们坚信，这个新的方向将有助于标准化一个常常面临碎片化风险的生态系统。我们很乐意听取您对团队决定采取的方向的反馈，以及我们可以做哪些改变来实现这一目标。请到Hub上的Transformers社区支持标签页来找我们！

---

> 本文由AI自动翻译，原文链接：[The Transformers Library: standardizing model definitions](https://huggingface.co/blog/transformers-model-definition)
> 
> 翻译时间：2026-04-18 04:36
