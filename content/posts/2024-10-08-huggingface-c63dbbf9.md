---
title: 动态推测解码：加速文本生成新方法
title_original: Faster Assisted Generation with Dynamic Speculation
date: '2024-10-08'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/dynamic_speculation_lookahead
author: ''
summary: 本文介绍了由英特尔实验室和Hugging Face开发的动态推测解码技术，该方法通过动态调整草稿模型生成的Token数量，显著提升大语言模型推理速度。相比静态或启发式方法，动态方法基于助手模型的置信度阈值决定何时停止生成并切换至目标模型验证，从而更接近最优推测前瞻值。实验表明，在多种任务和模型组合中，该方法可实现高达2.7倍的加速，并已集成至Transformers
  4.45.0版本作为默认模式。
categories:
- AI研究
tags:
- 推测解码
- 大语言模型
- 推理加速
- 动态调度
- Hugging Face
draft: false
translated_at: '2026-06-23T06:08:25.668509'
---

# 动态推测加速生成

⭐ 在这篇博客文章中，我们将探讨动态推测解码——一种由英特尔实验室和Hugging Face开发的新方法，可根据任务将文本生成速度提升高达2.7倍。从Transformers🤗 4.45.0版本开始，该方法已成为辅助生成的默认运行模式。⭐

## 推测解码

推测解码是一种流行的加速大语言模型推理的技术，同时保持其准确性。如下图所示，推测解码通过将生成过程分为两个阶段来工作。在第一阶段，一个快速但准确性较低的草稿模型（又称助手）自回归生成一系列Token。在第二阶段，一个大型但更准确的目标模型对生成的草稿Token进行并行验证。这个过程允许目标模型在单次前向传播中生成多个Token，从而加速自回归解码。推测解码的成功很大程度上取决于推测前瞻（SL），即每次迭代中草稿模型生成的Token数量。在实践中，SL要么是静态值，要么基于启发式方法，这两种方法都不是在推理过程中榨取最大性能的最优选择。

推测解码迭代。

![](/images/posts/d03f4a6dfd59.png)

## 动态推测解码

Transformers🤗提供了两种不同的方法来确定推理过程中调整草稿（助手）Token数量的调度方案。基于Leviathan等人的简单方法使用静态的推测前瞻值，并在每次推测迭代中生成固定数量的候选Token。另一种基于启发式的方法根据当前迭代的接受率调整下一次迭代的候选Token数量。如果所有推测Token都正确，候选Token数量增加；否则减少。

我们预计，一种用于管理生成的草稿Token数量的增强优化策略可以进一步降低延迟。为了验证这一论点，我们使用了一个预言机来确定每次推测迭代的最优推测前瞻值。该预言机使用草稿模型自回归生成Token，直到草稿模型和目标模型的预测Token之间出现差异。这个过程对每次推测迭代重复进行，最终确定每次迭代被接受的最优（最大）草稿Token数量。草稿/目标Token不匹配通过Leviathan等人提出的拒绝采样算法在零温度下识别。这个预言机通过每一步生成最大数量的有效草稿Token，并最小化对草稿模型和目标模型的调用次数，实现了推测解码的全部潜力。

下图左侧展示了来自MBPP数据集的代码生成示例在推测迭代中的预言机和静态推测前瞻值。观察到预言机推测前瞻值（橙色柱）存在高方差。静态推测前瞻值（蓝色柱）将生成的草稿Token数量固定为5，执行了38次目标前向传播和192次草稿前向传播，而预言机推测前瞻值仅执行了27次目标前向传播和129次草稿前向传播——显著减少。右侧图展示了整个Alpaca数据集上的预言机和静态推测前瞻值。

一个MBPP示例上的预言机和静态推测前瞻（SL）值。

![](/images/posts/e51582377d93.png)

整个Alpaca数据集的平均预言机推测前瞻值。

![](/images/posts/54bffd8a3330.png)

两张图都显示了预言机推测前瞻值的显著变化，表明静态推测前瞻值可能不是最优的。

为了更接近预言机并获得额外加速，我们开发了一种简单的方法来动态调整每次迭代的推测前瞻值。在生成每个草稿Token后，我们确定草稿模型是应该继续生成下一个Token，还是切换到目标模型进行验证。这个决定基于助手模型对其预测的置信度，通过logits的softmax估计。如果助手模型对当前Token预测的置信度低于预定义的阈值（称为assistant_confidence_threshold），即使尚未达到最大推测Token数量num_assistant_tokens，它也会停止该迭代的Token生成过程。一旦停止，当前迭代生成的草稿Token将被发送到目标模型进行验证。

## 基准测试

我们在一系列任务和模型配对中将动态方法与启发式方法进行了基准测试。动态方法在所有测试中均表现出更好的性能。值得注意的是，使用Llama3.2-1B作为Llama3.1-8B的助手采用动态方法时，我们观察到高达1.52倍的加速，而启发式方法在相同设置下没有显示出显著加速。另一个观察结果是，codegen-6B-mono使用启发式方法导致减速，而动态方法则显示出加速。

- 表中的结果反映了贪婪解码（温度=0）。使用采样（温度>0）时观察到类似趋势。
- 所有测试均在RTX 4090上进行。
- 我们的基准测试公开可用，允许所有人评估进一步的改进：https://github.com/gante/huggingface-demos/tree/main/experiments/faster_generation

表中的结果反映了贪婪解码（温度=0）。使用采样（温度>0）时观察到类似趋势。

所有测试均在RTX 4090上进行。

我们的基准测试公开可用，允许所有人评估进一步的改进：https://github.com/gante/huggingface-demos/tree/main/experiments/faster_generation

动态推测已集成到Hugging Face Transformers库的4.45.0版本中，现在作为辅助解码的默认运行模式。要使用带有动态推测的辅助生成，无需更改代码——只需像往常一样执行代码：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

prompt = "Alice and Bob"
checkpoint = "EleutherAI/pythia-1.4b-deduped"
assistant_checkpoint = "EleutherAI/pythia-160m-deduped"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
inputs = tokenizer(prompt, return_tensors="pt").to(device)

model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)
assistant_model = AutoModelForCausalLM.from_pretrained(assistant_checkpoint).to(device)

outputs = model.generate(**inputs, assistant_model=assistant_model)

```

默认的动态推测前瞻参数反映了最优值，但可以通过以下代码进行调整，以改善特定模型配对或数据集的性能：

```python

assistant_model.generation_config.assistant_confidence_threshold=0.4


assistant_model.generation_config.num_assistant_tokens_schedule='constant'



assistant_model.generation_config.num_assistant_tokens=20

```

要恢复到启发式或常量（如Leviathan等人）方法，只需将num_assistant_tokens_schedule设置为'heuristic'或'constant'，并将assistant_confidence_threshold=0和num_assistant_tokens=5设置如下：

```python

assistant_model.generation_config.num_assistant_tokens_schedule='heuristic'
assistant_model.generation_config.assistant_confidence_threshold=0
assistant_model.generation_config.num_assistant_tokens=5

```

## 下一步是什么？

我们引入了一种更快的辅助生成策略，称为**动态推测解码**，其性能优于基于启发式的方法，以及抽取固定数量的候选Token的方法。

在即将发布的博客文章中，我们将展示一种新的辅助生成方法：将任意目标模型与任意辅助模型相结合！这将为加速Hugging Face Hub上众多没有足够小尺寸辅助变体的模型打开大门。例如，**Phi 3**、**Gemma 2**、**CodeLlama**等模型都将适用于推测解码。敬请期待！

## 参考文献

- **Dynamic Speculation Lookahead Accelerates Speculative Decoding of Large Language Models**  
  在本文中，我们提出了DISCO，一种动态推测前瞻优化方法，该方法利用分类器来决定草稿模型是继续生成下一个Token还是暂停，并切换到目标模型进行验证，而不是使用预测概率的简单阈值。

- **Assisted Generation: a new direction toward low-latency text generation**  
- **Fast Inference from Transformers via Speculative Decoding**

## 引用

```bibtex
@article{mamou2024accelerating,
  title={Accelerating Speculative Decoding using Dynamic Speculation Length},
  author={Mamou, Jonathan and Pereg, Oren and Korat, Daniel and Berchansky, Moshe and Timor, Nadav and Wasserblat, Moshe and Schwartz, Roy},
  journal={arXiv preprint arXiv:2405.04304},
  year={2024}
}
```

---

> 本文由AI自动翻译，原文链接：[Faster Assisted Generation with Dynamic Speculation](https://huggingface.co/blog/dynamic_speculation_lookahead)
> 
> 翻译时间：2026-06-23 06:08
