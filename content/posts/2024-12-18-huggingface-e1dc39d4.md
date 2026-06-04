---
title: Bamba-9B：高效混合Mamba2模型突破推理瓶颈
title_original: 'Bamba: Inference-Efficient Hybrid Mamba2 Model'
date: '2024-12-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/bamba
author: ''
summary: IBM联合多所大学推出Bamba-9B混合Mamba2模型，在完全开放数据上训练，推理时相比标准Transformer实现2.5倍吞吐量提升和2倍延迟加速。该模型通过保持KV缓存大小恒定解决内存带宽瓶颈，支持transformers、vLLM等主流框架，并开源了训练、微调及数据加载器代码，旨在推动Mamba架构的社区采用。
categories:
- AI研究
tags:
- Mamba2
- 混合架构
- 推理效率
- 开源模型
- KV缓存优化
draft: false
translated_at: '2026-06-04T06:34:24.937369'
---

# Bamba：推理高效的混合Mamba2模型 🐍

![Bamba](/images/posts/e91479d270b6.jpg)

## 摘要

我们推出Bamba-9B，这是一个由IBM、普林斯顿大学、卡内基梅隆大学和伊利诺伊大学厄巴纳-香槟分校在完全开放数据上训练的推理高效混合Mamba2模型。在推理时，该模型在vLLM中相比标准Transformer实现了2.5倍的吞吐量提升和2倍的延迟加速。为促进社区实验，该模型可立即在transformers、vLLM、TRL和llama.cpp中使用。我们还发布了带有状态数据加载器的微调、训练和扩展预训练方案，并邀请社区进一步改进此模型。让我们一起克服KV缓存瓶颈！

## 成果 📦

1. Hugging Face Bamba合集
2. 包含推理、训练和微调脚本的GitHub仓库
3. 数据加载器
4. 量化
5. 集群监控自动导航

## 动机 🌟

Transformer模型越来越多地应用于实际场景，但在推理过程中面临内存带宽瓶颈，尤其是在较长上下文长度模型的逐Token解码阶段。低精度、层剪枝和压缩等技术可以缓解该问题，但未能解决根本原因——随着上下文长度增加，KV缓存所需内存量不断增长。Mamba、Griffin和DeltaNet等新兴架构通过使KV缓存大小保持恒定来消除这一瓶颈。Mamba架构近期在社区中获得了广泛关注。例如，Jamba和Samba将Mamba层与Transformer层交错排列，探索由此产生的混合Mamba模型。Codestral Mamba作为纯Mamba2模型，在编程任务上展现出最先进（SOTA）成果，而NVIDIA的混合Mamba2模型在长上下文和传统LLM基准测试中均取得有竞争力的表现。Falcon Mamba和Falcon 3 Mamba等近期创新在发布时均登顶Hugging Face排行榜。

我们推出Bamba-9B，这是一个在2.2T Token上训练的混合Mamba2模型，进一步验证了这些新兴架构。IBM、普林斯顿大学、卡内基梅隆大学和伊利诺伊大学厄巴纳-香槟分校的合作提供了完整的训练谱系、模型检查点和预训练代码，以支持可复现性和实验。已发布检查点的训练数据集不包含任何基准对齐的指令数据（FLAN除外），以保留扩展预训练和微调的灵活性。我们的目标是通过在中等规模模型（7B-10B）上展示强劲性能来彰显混合Mamba2架构的潜力，并为社区提供完全可复现且使用开放数据集训练的检查点。

为促进社区实验，我们还发布了分布式无状态洗牌数据加载器，并在transformers、TRL、vLLM和llama.cpp等开源库中启用混合Mamba2架构。我们希望这些努力能推动Mamba架构的采用，缓解KV缓存瓶颈，并缩小与最先进开源模型的差距。

### 在transformers中使用 🤗

要使用transformers调用Bamba，您可以使用熟悉的AutoModel类和generateAPI。更多详情请遵循Bamba GitHub中的说明。

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("ibm-fms/Bamba-9B")
tokenizer = AutoTokenizer.from_pretrained("ibm-fms/Bamba-9B")

message = ["Mamba是一种具有以下特性的蛇  "]
inputs = tokenizer(message, return_tensors='pt', return_token_type_ids=False)
response = model.generate(**inputs, max_new_tokens=64)
print(tokenizer.batch_decode(response, skip_special_tokens=True)[0])

```

## 评估 📊

我们将评估分为三部分：

1. 与最先进Transformer模型的比较
2. 与相似Token预算的Transformer模型的比较
3. 与其他Mamba变体的比较。

评估设置 ⚙️ 🖥️：除NVIDIA Mamba2 Hybrid模型外，我们按照此处的设置和脚本对所有模型重新运行所有基准测试。由于NVIDIA Mamba2 Hybrid模型的权重并非Hugging Face transformers兼容格式，我们无法对其进行基准测试。因此，我们报告原始论文中的数值。对于v2排行榜结果，我们进行归一化处理并报告归一化结果。在所有评估中，数值越高越好，另有标注除外。

### 摘要评估

Bamba-9B展示了混合Mamba模型与Transformer模型相比的竞争力。虽然在数学基准测试和MMLU分数（MMLU、GSM8K、MMLU-PRO、MATH Lvl 5）上存在差距，但排除这些基准测试后，其平均性能几乎与Meta Llama 3.1 8B持平（Llama为44.68，Bamba为45.53），而后者是在7倍数据量上训练的。这些差距可以通过以下方式解决：(a) 使用更多Token扩展预训练（训练期间MMLU分数稳步提升），以及(b) 在预训练/退火阶段纳入高质量数学数据。未来计划包括使用更新的数据集（如Olmo2混合集）以及使用基准对齐的混合集（如Dolmino混合集）进行退火。

Bamba-9B的结果也缓解了对NVIDIA混合Mamba2模型在排行榜基准测试中得分相对较低的担忧。NVIDIA研究的目标是在相同条件下比较架构。与他们的发现一致，Bamba-9B再次证实混合Mamba2架构在提供高达5倍推理效率的同时，性能与Transformer模型相当。

### 与最先进Transformer模型的比较

我们将Bamba-9B与相似规模的最先进Transformer模型（Meta Llama 3.1 8B、IBM Granite v3 8B、Olmo2 7B和Gemma 2 9B）进行比较。我们观察到，虽然存在明显的基准差距，但尚不清楚这些差距是否指向基于Mamba/Mamba2模型的缺陷。事实上，仔细分析表明，差距主要源于模型训练所用的数据量以及在退火阶段是否包含基准对齐的指令数据集。例如，我们进行了一次小规模运行，添加了metamath，将GSM8K分数从36.77提升至60.0。我们将在即将发表的论文中发布详细分析和发现。

HF LLM-V1+ OpenbookQA和PIQA：

HF LLM-V2**：

安全基准测试对于确保AI模型生成符合伦理、包容且无害的内容至关重要。我们在Toxigen（5-shot，logits）（专注于检测有害语言）、BBQ（5-shot，生成）、PopQA（5-shot，生成）和CrowS-Pairs（5-shot，logits）（衡量偏见和公平性）等知名安全基准测试上评估我们的模型。我们计划通过全面的SFT和DPO方法来解决这些安全方面的差距。

*数值越低越好

## 与相似Token预算的Transformer模型的比较

我们选取了几个知名模型：使用相同数据训练的Olmo 7B（2024年）、Meta Llama 2 7B（2023年）和IBM Granite 7B（2023年），这些模型均训练了约2T Token。在这些Transformer模型中，Olmo 7B在8个关键基准测试中的平均得分最高。Bamba-9B在相同Token数量和数据集上训练，表现优于Olmo 7B。由于Bamba-9B模型拥有9B参数，直接比较仍存在难度，但主要结论是混合Mamba2模型与使用相似Token预算训练的Transformer模型具有竞争力。

### 与基于Mamba/Mamba2架构的语言模型的比较

过去6个月中，多种基于Mamba/Mamba2架构的模型开始涌现（例如NVIDIA混合Mamba2、Codestral Mamba、Falcon Mamba和Zamba 7B v1），进一步提升了这些架构的性能，展示了其卓越的推理性能，并缩小了与Transformer模型在基准测试结果上的差距。我们在Bamba-9B、NVIDIA混合Mamba2、Zamba和Falcon Mamba之间比较了8个关键基准测试。

Falcon Mamba 是一个纯 Mamba 模型，Zamba 每 6 个 Mamba 层设有一个共享注意力层，而 Bamba-9B 和 NVIDIA 都是混合模型，在全注意力层中穿插了 Mamba2 层。Falcon Mamba 在 5.5T Token 上进行了训练，整体表现最佳，但关于它在长上下文任务中的表现仍存在开放性问题，而基于 Mamba 的架构正是在这类任务中展现出其推理性能的真正优势。Zamba 在更少的 Token（1T）上进行了训练，但采用了不同的混合架构，并使用了对齐基准的指令数据集，包括由更强大的语言模型生成的数据。Bamba-9B 和 NVIDIA 混合 Mamba2 彼此非常相似（架构差异的细节在模型架构部分进行了总结），但 Bamba-9B 在 2.2T Token 上训练，而 NVIDIA Hybrid Mamba 在 3.5T Token 上训练。

注意：截至撰写本文时，Falcon3 Mamba 7B 已发布，结果甚至优于 Falcon Mamba。我们计划利用从 Falcon3 Mamba 中获得的任何经验，改进我们的下一个 Bamba 版本。

* 结果取自 NVIDIA 论文。

💡 注意：训练数据集以及训练过程中所见 Token 数量的差异使得直接比较这些模型变得困难。此表的关键结论是，混合 Mamba2 架构能够提供具有竞争力的结果，同时训练效率几乎与 Transformer 模型相当。此外，尽管在全注意力层中穿插了 Mamba2 层，它们仍能在推理效率上实现显著提升（理论上可达 5 倍）。我们正在使用最新数据集继续预训练 Bamba-9B 模型，并计划随着模型改进发布未来的检查点。

## 推理效率 ⚡🏎️

KV 缓存瓶颈是大语言模型面临的主要挑战，这促使了诸如量化、剪枝以及 Mamba2、线性 Transformer 和 RetNet 等新型架构的解决方案。即使在标准 Transformer 中，要实现大规模的推理效率，通常也需要自定义内核。Bamba-9B 建立在社区内核可用性的势头之上，并通过与 vLLM 模型服务框架的集成进行了进一步改进。

我们在 vLLM 集成方面的进展，通过此 PR 进行跟踪，在 NVIDIA H100 80GB GPU 上将 Bamba-9B 与 Meta Llama 3.1 8B 进行了基准测试。使用 1K Token 的输入大小和 2K 到 64K 的输出大小，跨越不同批次大小，我们测量了吞吐量（Token/秒）和延迟。结果表明，随着批次大小和序列长度的增加，与 Transformer 模型相比，Bamba-9B 实现了高达 2-2.5 倍的吞吐量和延迟改善。这些改进增强了实时应用和 GPU 利用率，其中更高的吞吐量比率（>1）和更低的延迟比率（<1）是有益的。

![图 1](/images/posts/83d43bb2695d.png)

![图 2](/images/posts/87bbc38fc504.png)

我们的分析表明，在 H100 NVIDIA GPU 上，当推理转向内存瓶颈时（这通常发生在生产环境中），我们预计会有 5 倍的加速——请参见关于算术强度的附录。然而，由于三个主要原因，我们尚未在 vLLM 中实现这种加速：

1. Bamba 和任何基于 Mamba2 的架构不支持分块预填充
2. 内存分配假设了标准的 Transformer KV 缓存
3. Mamba2 内核未针对 H100 GPU 进行优化

这些问题正在此处跟踪。

## 模型架构

我们的模型架构基于 NVIDIA 混合 Mamba2，并进行了以下更改。

我们在 Mamba2 层中总共有 8B 参数，在全注意力层中有 800M 参数，在嵌入层中有 1B 参数。隐藏状态为 4K，全注意力的 GQA 有 8 个 KV 头和 32 个头，Mamba2 层头维度为 64，卷积滤波器大小为 4。两个模型之间最显著的变化是将全注意力层从 NVIDIA 混合 Mamba2 模型中的 4 层减少到 Bamba-9B 中的 3 层，并引入了 RoPE 嵌入。

自 The Pile 数据集问世以来，开源数据已经取得了长足的进步。当我们开始训练这个模型时，最好的开源数据是 Dolma v1.7，通过 Olmo 模型和 Hugging Face 数据团队的消融实验证明其性能相当不错。此后，又发布了几个更高质量的开源数据集，例如 DCLM、FineWeb-2 和 Olmo2 mix。

我们在训练的第一阶段使用 Dolma v1.7，所选的数据混合如下所示。在训练的第二阶段，我们使用 Fineweb-edu 和 Cosmopedia。这些数据集以原始形式下载，我们使用在内部大规模 Red Hat Open Shift 集群上运行的 Ray 框架对其进行 Token 化。我们计划很快发布 Token 化并格式化的 Parquet 数据，以实现可重复性。

![数据混合](/images/posts/0a5d424acd7a.png)

预训练第一阶段的数据混合

## 预训练

Bamba 的预训练是分阶段进行的，我们在 1.8B 模型大小和 100B Token 上进行了多次消融实验，以确定合适的学习率。基于这项研究的有希望的结果，我们训练了一个更大规模的模型——使用 Dolma 混合数据在 3B 模型上训练到 2T Token。我们还按照 Meta Llama 架构训练了一个 3B Transformer 模型，使用相同的数据混合，观察到 Bamba 模型具有相似或更好的性能，这与同时进行的 NVIDIA 研究得出的结论一致。最后，我们设计了一个 9B 模型架构，并在相同的混合数据上重新训练。我们使用 PyTorch FSDP 来训练所有模型。

训练细节：
我们使用了余弦学习率调度，峰值学习率为 3e−4，在 2000 步上进行二次预热，衰减因子为 0.033，在 2T Token 上的结束学习率为 1e−5。我们使用了 AdamW 优化器，β1 为 0.9，β2 为 0.95。我们使用了 0.1 的权重衰减，序列长度为 4096，全局批次大小为 1.5M Token/批次。我们使用了来自 IBM Cloud Vela 生产集群的 192 个 A100 GPU 来训练这个模型，历时 2 个月。该集群由 Red Hat OpenShift 管理。我们遇到了 3 次作业中断，原因是作业部署不正确和硬件故障。与硬件相关的作业故障使用 autopilot 自动检测。

我们还使用来自 Hugging Face FineWeb-edu 和 Cosmopedia 的高质量数据进行了第二阶段训练，额外训练了 200B Token。我们使用了 2e−5 的学习率和余弦调度来退火模型，这有助于提高我们的分数。我们目前正在尝试更多高质量数据，并将作为我们开源承诺的一部分发布未来的检查点。

## 数据加载器

训练高质量语言模型涉及多个方面，数据加载器是其中之一。在过去 18 个月中，我们一直在开发一个能够满足大规模分布式训练需求的数据加载器。我们开源了这个数据加载器，以便其他人可以将其与他们选择的框架一起使用。我们已在 Bamba 模型训练中使用了它，并将其与 Torch Titan 集成。迄今为止，我们相信这是唯一提供丰富功能的开源数据加载器。

该数据加载器提供以下关键功能：

1. 有状态且可检查点，以确保在 epoch 中间无缝恢复
2. 自动重新缩放以适应变化的工作负载和 GPU 分配
3. 数据流式处理，零开销进行洗牌
4. 异步分布式操作，无需点对点通信
5. 允许动态数据混合和即时 Token 化
6. PyTorch 原生、模块化且可扩展

我们已经在数百次训练作业中对该数据加载器进行了实战测试，并在数月的持续运行中对其进行了优化。主要代码库位于我们的仓库此处，我们还与 Torch Titan 团队合作使其在此处可用。我们正在与 Meta PyTorch 团队合作，将此数据加载器贡献到 PyTorch 核心。

## 量化

我们最近开源了一个模型量化框架。通过该框架，我们利用llm-compressor将Bamba检查点量化为fp8格式。在OpenLLM排行榜的所有基准测试中，我们观察到精度损失极小。具体而言，对于Bamba 9B模型，V1平均得分仅出现0.1的微小差异（从62.31降至61.5），V2平均得分下降0.9（从10.91降至10.04）。这些量化检查点与bf16版本的检查点一同发布。这也验证了Bamba模型与当前最先进的Transformer模型一样适合进行量化。

我们正在vLLM中为该模型启用fp8推理功能，这需要更新相关内核。线性层和全注意力机制的处理相对容易，但Mamba2层需要更新Triton/CUDA内核以支持fp8格式。

## 上下文长度扩展

我们目前正在探索多种长上下文长度扩展方法，首先从对全注意力层应用LongRoPE开始。以PhoneBook检索任务为测试的初步结果表明，LongRoPE可应用于该模型。我们将Bamba-9B的上下文长度扩展了4倍和8倍，并与Meta Llama的三个变体（训练上下文长度分别为4K、8K和128K的LLama2、Llama3、LLama3.1）进行对比。结果如下图所示。

![数据混合](/images/posts/76b6e2f5be21.png)

我们观察到，上下文扩展后的Bamba-9B模型在无需任何调优的情况下，在16K上下文长度内表现极为出色，大幅优于原始Bamba-9B模型、Llama2-7B和Llama3-8B，性能与Llama3.1-8B相当。在序列长度达到32K时，LLama3.1取得了最佳性能。我们计划在准备就绪后发布长上下文长度扩展模型。

## 总结 🎯

由IBM、普林斯顿大学、卡内基梅隆大学和伊利诺伊大学厄巴纳-香槟分校合作开发的Bamba-9B，是一款性能强劲的混合Mamba2模型。该模型完全基于开放数据集训练，我们正在发布中间检查点和最终检查点。为促进社区实验，该模型现已可在transformers、vLLM、TRL和llama.cpp中直接使用。我们还发布了包含状态化数据加载器的调优、训练和扩展预训练方案，并邀请社区进一步改进该模型。

关键要点：

- 推理效率：Bamba-9B在吞吐量和延迟方面实现了显著提升，增强了实时应用性能。使用vLLM与Llama 3.1 8B进行基准测试显示，吞吐量提升2.5倍，延迟改善2倍，更多优化即将推出！
- 竞争性基准：Bamba-9B在与Meta Llama 3.1 8B等最先进Transformer模型的竞争中表现优异。排除数学和MMLU任务后，其平均基准性能与这些模型相当，且通过扩展训练和数学专项数据集有望缩小差距。
- 开放协作：该模型的开发使用了开放数据，促进了AI社区的透明度和可复现性。

推理效率：Bamba-9B在吞吐量和延迟方面实现了显著提升，增强了实时应用性能。使用vLLM与Llama 3.1 8B进行基准测试显示，吞吐量提升2.5倍，延迟改善2倍，更多优化即将推出！

竞争性基准：Bamba-9B在与Meta Llama 3.1 8B等最先进Transformer模型的竞争中表现优异。排除数学和MMLU任务后，其平均基准性能与这些模型相当，且通过扩展训练和数学专项数据集有望缩小差距。

开放协作：该模型的开发使用了开放数据，促进了AI社区的透明度和可复现性。

更多详情及模型与相关资源的获取，请访问Bamba GitHub仓库。

### 未来工作

我们计划在以下几个方向进行探索，并进一步优化推理高效的Mamba2混合架构：

1. 通过持续在更多数据上进行预训练来改进模型；欢迎社区提供任何反馈，以便我们共同打造一款卓越的Mamba2混合模型。
2. 使用Tuluv3、agent instruct和Anteater等SFT数据集对基础模型进行监督微调，并将结果模型与其他最先进的指令调优模型进行对比。
3. 与社区合作在vLLM中启用该模型。分块预填充和该架构的内存分配管理将是关键问题。
4. 启用fp8内核以进一步加速推理。
5. 训练时间优化，应用torch.compile以及fp8训练——我们的团队已在Transformer架构上（与Meta合作）证明了这些方法的有效性。
6. 将上下文长度扩展至100万以上。

## 贡献者

- 数据收集与整理：感谢AllenAI团队提供高质量开源数据集Dolma，以及Hugging Face数据团队提供FineWeb-edu和Cosmopedia数据集。这些巨大贡献使我们能够创建该模型。
- 数据预处理：感谢IBM内部数据预处理团队，特别是Tuan Hoang Trong、Syed Zawad、Jay Gala和Ryan Gordon，他们帮助实现了大规模数据的分词处理。分词代码可在此处获取。
- 模型架构：模型架构设计由普林斯顿大学、卡内基梅隆大学、IBM和伊利诺伊大学厄巴纳-香槟分校共同完成，参与人员包括：Tri Dao（普林斯顿大学）、Albert Gu（卡内基梅隆大学）、Linsong Chu（IBM）、Davis Wertheimer（IBM）、Minjia Zhang（伊利诺伊大学厄巴纳-香槟分校）、Mudhakar Srivatsa（IBM）和Raghu Ganti（IBM）。
- 模型训练：模型训练主要由IBM团队使用Tri Dao和Albert Gu开发的Mamba2内核和层实现完成。IBM主要参与人员包括：Linsong Chu、Divya Kumari、Davis Wertheimer、Raghu Ganti和Dakshi Agrawal。
- 模型调优：IBM团队在TRL中实现并验证了模型调优，参与人员包括Sukriti Sharma和Anh Uong。
- 模型推理：transformers、vLLM和llama.cpp中的模型推理基于普林斯顿大学和卡内基梅隆大学编写的内核。IBM团队正与社区合作，在多个生态系统中启用该功能。团队成员包括：Fabian Lim、Antoni viros i Martin、Adnan Hoque、Jamie Yang、Nelson Nimura Gonzalez、Joshua Rosenkranz、Nick Hill和Gabe Goodhart。
- 量化：量化工作由IBM团队主导——Naigang Wang和Charlie Liu。
- 评估：评估工作由IBM团队主导，长上下文评估由伊利诺伊大学厄巴纳-香槟分校完成，参与人员包括：Yotam Perlitz、Ofir Arviv、Michal Shmueli-Scheuer（IBM）、Haoechen Shen和Minjia Zhang（伊利诺伊大学厄巴纳-香槟分校）。

最后，我们要感谢领导层对本项目的支持——Priya Nagpurkar、David Cox、Sriram Raghavan、Aya Soffer、Ruchir Puri和Mukesh Khare。

同时感谢社区，特别是来自Hugging Face的Pablo Montalvo-Leroux、Aritra Roy Gosthipaty和Vaibhav Srivastav，以及来自Contextual AI的Stas Bekman，他们为本博客和transformers的PR提供了宝贵反馈。此外，感谢来自Neural Magic的Tyler Michael Smith，他正在推动与vLLM的集成。

特别感谢Meta PyTorch、AllenAI和Hugging Face团队对开源倡议的贡献——PyTorch FSDP使我们能够顺利训练该模型，而Dolma、Fineweb/Cosmopedia的数据成就了今天的模型！

## 附录：算术强度

使用以下符号：$b$：批量大小$s$：序列长度$h$：隐藏状态大小（4096）$d$：头维度（128）$l$：总层数（32）$l_{attn}$：注意力层数（3）$l_{ssd}$：SSD层数（29）

注意力模型和Bamba模型均配置了4:1的GQA（分组查询注意力，在注意力层中），MLP扩展比为3.5，并在MLP模块中使用GLU。Bamba中的SSD层配置为状态维度$d$，头维度$d/2$，头数 = $4h/d$。排除嵌入层后的模型规模为：

在预填充阶段，模型带来的计算和内存（读取+写入）需求为：

在解码阶段，模型带来的计算和内存（读取+写入）需求为：

Bamba与LLaMa模型在预填充阶段的计算FLOPs以及解码阶段的内存（读取+写入）大小对比如下。请注意，比值小于1表示更优。由于推理吞吐量主要受解码阶段瓶颈限制，对于长序列长度（> 16K），Bamba（相对于LLaMa）的潜在加速比为5倍。当前测量结果（基于vLLM）约为2.5倍，我们预计近期将进一步提升。

![ArithmeticIntensity](/images/posts/a4528e46ff36.png)

---

> 本文由AI自动翻译，原文链接：[Bamba: Inference-Efficient Hybrid Mamba2 Model](https://huggingface.co/blog/bamba)
> 
> 翻译时间：2026-06-04 06:34
