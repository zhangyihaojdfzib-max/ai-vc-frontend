---
title: Nemotron 3 Nano 4B：高效本地AI的紧凑混合模型
title_original: 'Nemotron 3 Nano 4B: A Compact Hybrid Model for Efficient Local AI'
date: '2026-03-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/nemotron-3-nano-4b
author: ''
summary: 本文介绍了NVIDIA推出的Nemotron 3 Nano 4B模型，这是一个仅40亿参数的紧凑型混合Mamba-Transformer架构模型，专为边缘设备部署优化。该模型通过Nemotron
  Elastic框架从9B模型压缩而来，在指令遵循、游戏智能和VRAM效率等关键维度上达到同类最佳水平，能够在Jetson、RTX GPU等设备上实现低延迟、高隐私的本地AI推理，并具备出色的工具使用能力。
categories:
- AI产品
tags:
- 边缘计算
- 模型压缩
- 混合架构
- 本地AI
- NVIDIA
draft: false
translated_at: '2026-03-18T04:53:50.164564'
---

# Nemotron 3 Nano 4B：面向高效本地AI的紧凑型混合模型

我们很高兴推出**Nemotron 3 Nano 4B**，这是Nemotron 3家族最新、最紧凑的成员。该模型利用混合Mamba-Transformer架构，旨在特定能力集上实现效率与精度的平衡，为轻量级小语言模型树立了新标准。该模型可在任何支持NVIDIA GPU的平台上使用，结合了最先进的指令遵循和卓越的工具使用能力，同时将VRAM占用降至最低。

仅拥有40亿参数的Nemotron 3 Nano 4B非常紧凑，足以在NVIDIA Jetson平台（Jetson Thor/Jetson Orin Nano）、NVIDIA DGX Spark以及NVIDIA RTX GPU等边缘设备上运行。这使得响应时间更快、数据隐私性更强、部署更灵活，同时保持较低的推理成本。

Nemotron 3 Nano 4B是我们首款专门为设备端部署优化的模型，专为驱动GeForce RTX、Jetson和Spark客户用例中的本地对话Agent（智能体）和角色而构建。该模型在边缘生产使用的几个关键维度上实现了最先进的精度和效率：

- 指令遵循（IFBench, IFEval）：在其尺寸类别中达到最先进水平
- 游戏代理/智能（Orak）：在其尺寸类别中达到最先进水平
- VRAM效率（峰值内存使用）：在低和高ISL/OSL设置下，其尺寸类别中VRAM占用最低（*1）
- 延迟：在高ISL设置下，其尺寸类别中TTFT最低（*1）

（*1）效率基准测试在RTX 4070上使用Llama.cpp进行，测试对象为两个模型的Q4_K_M量化版本。

此外，Nemotron 3 Nano 4B提供了出色的工具使用性能，并且在避免幻觉方面极具竞争力。这些能力共同证明了该模型非常适合边缘用例。

Nemotron 3 Nano 4B是从**Nemotron Nano 9B v2**通过**Nemotron Elastic**框架进行剪枝和蒸馏得到的，使其能够作为混合推理模型继承强大的推理能力。随后，它使用源自**Nemotron 3后训练数据**的新配方进行了进一步的后训练，使模型即使没有显式思考也能出色地完成任务。

最后，作为一个开源模型，它赋能生态系统，使其能够针对特定领域用例进行定制、微调和优化。

![accuracy_table_resized](/images/posts/a41a86867d65.png)

对于**Orak**，我们在《超级马里奥》、《暗黑地牢》和《星露谷物语》等战术游戏中评估了模型。

## Nemotron 3 Nano 4B的训练配方

![Screenshot 2026-03-16 at 12.47.17 PM](/images/posts/94edfd0e6fc0.png)

### 使用Nemotron Elastic将9B压缩至4B

Nemotron 3 Nano 4B源自**Nemotron Nano 9B v2**，使用了**Nemotron Elastic**技术。与从头开始训练一个4B模型，或像现有LLM（大语言模型）压缩技术那样执行剪枝、候选搜索和蒸馏等独立阶段不同，Nemotron Elastic使用由路由器引导的结构化剪枝，该路由器与模型联合训练，其辅助损失函数同时考虑了学生模型的尺寸和原始的知识蒸馏损失。这项技术能够以远低于从头预训练或传统压缩的成本，获得最优的学生模型。

### 路由器如何决定剪枝内容

Nemotron Elastic引入了一个端到端训练的路由器，该路由器在知识蒸馏运行的同时，在多个压缩轴上进行神经架构搜索。对于Nano 4B，该框架在单一预算配置下使用——仅针对40亿参数目标——路由器的角色是确定**剪枝哪些轴**以及**剪枝多少**以达到目标预算。

路由器被赋予四个剪枝轴以供选择：

- Mamba头——减少SSM头的数量
- 隐藏维度（嵌入/向量维度）——缩小模型整体的表示宽度
- FFN通道——剪枝MLP层中的中间神经元
- 深度（层数）——从网络中移除整个层

对于每个宽度轴，通过根据基于激活的重要性分数对通道、头和神经元进行排序，向路由器提供了关于组件重要性的先验知识。对于深度，使用了基于归一化MSE的层重要性排序：迭代地移除每一层，并测量其对完整模型输出logits的影响，从而得出哪些层最重要的原则性排序。更多细节可在**Nemotron Elastic论文**中找到。
给定40亿参数的目标预算，路由器收敛于以下剪枝决策：

### 用于精度恢复的两阶段蒸馏

在路由器确定剪枝架构后，使用来自冻结的9B父模型的知识蒸馏，并利用Nano v2的预训练和后训练数据，对压缩后的模型进行重新训练。这个精度恢复过程分两个阶段进行：

1. 阶段1——短上下文蒸馏（8K序列长度）：使用由约70%后训练数据和30%来自父模型Nano v2配方的预训练数据组成的数据混合，在8K上下文窗口下，使用630亿Token对4B模型进行训练。此阶段对于压缩后模型精度的初步恢复至关重要。
2. 阶段2——长上下文扩展（49K序列长度）：为了恢复在需要扩展推理链的更具挑战性任务上的性能，将上下文扩展到49K Token。在此阶段，模型使用1500亿Token进行训练。

### 监督微调

我们使用**Megatron-LM**，从**Nemotron-Post-Training-v3**集合的相关子集中进行了两个阶段的SFT（监督微调）。第一个SFT阶段使用涵盖数学、编程、科学、聊天、指令遵循和Agent（智能体）任务等多个领域的推理和非推理数据混合来训练模型。第二阶段是规模较小、重点突出的训练，旨在强化安全行为。

### 多环境强化学习

一旦模型通过SFT完成引导，我们便转向使用**NeMo-RL**的三阶段RL（强化学习）流程，以针对我们的重点领域：指令遵循和工具调用/Agent（智能体）行为。在第一阶段，我们使用单轮指令遵循数据。在第二阶段，我们使用**NeMo-Gym**环境进行**单轮**和**多轮**指令遵循以及**结构化输出**（JSON, XML）的训练。最后，在第三阶段，我们使用**Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1**的初步版本进行多轮对话式工具调用训练。在三个RLVR阶段中，均使用了推理与非推理数据各占50%的平衡比例，且KL惩罚在每个阶段逐步增加。

## 通过量化提升效率

对于边缘设备，通过量化进一步减小模型尺寸以提高效率并减少VRAM使用至关重要。Nemotron 3 Nano 4B以FP8和Q4_K_M GGUF格式发布，以便在边缘设备上高效运行。

对于FP8模型，我们使用**ModelOpt**库应用了训练后量化（PTQ）。对于PTQ校准数据集，我们使用了后训练SFT数据集中的1K样本小子集来估计激活统计量，以最小化与量化相关的精度损失。为了在提高效率的同时保持精度，我们还应用了选择性量化策略，而不是量化整个网络。比较一组量化配置后发现，将自注意力层（42层中的4层）以及位于自注意力层之前的4个Mamba层保持为BF16，为精度恢复和效率增益的权衡提供了一个最佳平衡点。模型权重、激活和KV-Cache被量化为FP8。所有Mamba层内的Conv1D保持为BF16。与BF16模型相比，FP8模型在目标基准测试中实现了100%的中值精度恢复。在DGX Spark和Jetson Thor上，FP8量化版本与原始BF16版本相比，延迟和吞吐量提升了高达1.8倍。

为支持Llama.cpp，我们采用了广泛使用的GGUF量化方法Q4_K_M，这是一种4位量化方案，在效率与精度之间实现了出色的平衡。与BF16模型相比，Q4_K_M GGUF版本在目标基准测试中实现了100%的中位精度恢复。

此GGUF版本同样非常适合Jetson部署。在为小型嵌入式设备设计的Jetson Orin Nano 8GB上，通过Llama.cpp运行的Q4_K_M检查点可达到18 Token/秒的推理速度，吞吐量最高可达Nemotron Nano 9B v2的2倍，这凸显了Nemotron 3 Nano 4B在嵌入式AI和机器人应用场景中进行边缘推理的高效性。

## 立即体验！

Nemotron 3 Nano 4B现已支持多种推理引擎，包括Transformers、vLLM、TRT-LLM和Llama.cpp，能够适应广泛的边缘部署场景。您可以通过访问下方的Hugging Face仓库下载模型检查点开始使用。模型卡片中提供了Hugging Face Transformers、vLLM、TRT-LLM和Llama.cpp的使用示例。

- https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-FP8
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF

针对Jetson平台，Jetson AI Lab模型页面提供了分步指南和开箱即用的运行命令。

同时，欢迎查看NVIDIA游戏内推理（NVIGI）SDK，该工具可在运行模型的同时处理高强度图形工作负载时显著提升推理性能。

---

> 本文由AI自动翻译，原文链接：[Nemotron 3 Nano 4B: A Compact Hybrid Model for Efficient Local AI](https://huggingface.co/blog/nvidia/nemotron-3-nano-4b)
> 
> 翻译时间：2026-03-18 04:53
