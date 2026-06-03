---
title: Holo3.1：快速本地化计算机使用Agent
title_original: 'Holo3.1: Fast & Local Computer Use Agents'
date: '2026-06-02'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/Hcompany/holo31
author: ''
summary: Holo3.1是Holo系列的最新版本，专注于提升计算机使用Agent在网页、桌面和移动环境中的鲁棒性，并支持多种Agent框架和部署目标。该版本首次发布量化检查点（FP8、Q4
  GGUF、NVFP4），实现快速本地推理，性能几乎无损。在移动自动化（AndroidWorld）和跨框架性能上均有显著提升，同时推出更小模型尺寸以平衡成本与性能，推动消费级硬件上的本地Agent部署。
categories:
- AI产品
tags:
- Holo3.1
- 计算机使用Agent
- 本地推理
- 量化模型
- 移动自动化
draft: false
translated_at: '2026-06-03T06:50:51.680843'
---

# Holo3.1：快速且本地的计算机使用Agent（智能体）

去年三月，我们发布了Holo3，这是我们最先进的计算机使用模型。该模型迅速获得了采用。开发者、企业和合作伙伴开始在广泛的工作流程中部署Holo3，涵盖从浏览器自动化和商业软件到内部工具和桌面应用程序。随着采用率的增长，我们意识到仅凭性能已不足以满足需求。

用户希望在桌面和移动环境中运行相同的计算机使用能力，并与不同的Agent（智能体）框架实现无缝集成。他们需要部署的灵活性，从云端推理到终端设备上的完全本地执行。

这就是我们发布Holo3.1系列的原因。Holo3.1在生产环境中最重要的三个维度上提升了鲁棒性：环境（网页、桌面、移动）、Agent（智能体）框架和部署目标。我们首次发布了针对本地推理优化的量化检查点，包括FP8、Q4 GGUF和NVFP4。

Holo3.1是我们迈向通用计算机使用Agent（智能体）愿景的重要一步：能够在各种环境中运行、集成到任何Agent（智能体）栈中、并在工作流程所在之处执行。

# 跨GUI环境和Agent（智能体）框架的计算机使用

基于Qwen系列，Holo3.1旨在提升计算机使用Agent（智能体）实际部署环境中的鲁棒性，同时保持最先进的性能。

随着团队将Holo3从评估阶段推进到生产阶段，我们反复观察到同样的挑战：在一种环境中的强劲表现并不一定能迁移到另一种环境。移动设备、替代的Agent（智能体）框架以及不同的执行框架都会引入各自的数据分布偏移。

![Capture d’écran 2026-06-01 à 16.30.52](/images/posts/f283ebea2bb9.png)

## 移动自动化

Holo3.1将Holo3的能力扩展到浏览器和桌面控制之外，在移动环境中取得了重大提升。在AndroidWorld上，我们的35B-A3B模型从67%提升至79.3%，而较小的4B和9B变体则从58%提升至72%。

## 跨框架性能

为了更好地支持在第三方Agent（智能体）栈中部署Holo的团队，Holo3.1除了Holo3已有的结构化JSON输出外，还引入了对函数调用协议的原生支持。

在OSWorld以及涵盖电子商务、商业软件和协作工作流程的内部基准测试套件中，函数调用和原生执行现在实现了近乎相同的性能。在我们的Holotab产品框架内评估时，Holo3.1相比Holo3还实现了超过25%的提升。

## 更小尺寸以实现成本与性能的权衡

为了进一步支持本地和设备端推理，除了用于最先进性能的较大35B-A3B模型外，我们还发布了新的模型尺寸，包括用于经济高效和私有部署的小型模型（0.8B、4B和9B）。

![Capture d’écran 2026-06-01 à 16.21.18](/images/posts/506b3c7e5005.png)

![overall_pareto_light_notitle](/images/posts/8467fb220e83.png)

Holo3.1和Qwen 3.5系列的性能与成本对比。总体性能首先对四个H Corporate基准取平均值（因此每个系列权重相等），然后取OSWorld、AndroidWorld、H Corporate、ScreenSpot-Pro和OSWorld-G的平均值。

# 快速且本地的推理

这是我们首次发布量化权重的版本。我们从35B-A3B检查点开始，提供FP8、Q4 GGUF和NVFP4格式。

对于NVFP4，我们使用了NVIDIA的Model Optimizer，采用W4A16配置。这些检查点使得计算机使用Agent（智能体）能够实现快速本地推理，且模型性能几乎没有下降。FP8和NVFP4在OSWorld上取得了相同的分数，仅比全精度BF16检查点低约两个百分点。

加速效果显著：在DGX Spark上，NVFP4 W4A16的总Token吞吐量是FP8的1.41倍，是BF16的1.74倍。

![quality_throughput_pareto_light (1)](/images/posts/09a4b34ae720.png)

## 迈向消费级硬件上的本地Agent（智能体）

我们还发布了Q4 GGUF检查点，旨在消费级硬件上本地部署计算机使用Agent（智能体）。

Agent（智能体）本身在Windows或Mac机器上本地运行，而模型可以在同一台机器上运行——我们提供了Apple Silicon的参考数据——也可以在同一网络的DGX Spark上运行。在这两种情况下，执行过程完全保持私密和本地化，没有任何数据离开用户的网络。

在Spark上，我们与NVIDIA共同开发的Agent（智能体）框架优化，结合上述NVFP4量化，相比FP8基线实现了约2倍的复合端到端加速，将平均步骤时间从6.8秒缩短至3.3秒。

![agent_request_rate_light](/images/posts/509f369d183c.png)

跨平台和精度的Agent（智能体）请求速率。在DGX Spark上，采用NVFP4的vLLM在默认模式和快速模式下均实现了最高的请求速率，其次是Q4 GGUF和FP8。这些改进及其他优化将在即将推出的桌面Agent（智能体）框架中实现。

# 可用性

Holo3.1系列提供四种尺寸：

我们还发布了针对本地和边缘部署优化的FP8、NVFP4和Q4 GGUF检查点。

# 开始使用

- Holo Models API：https://hcompany.ai/holo-models-api
- Hugging Face：https://huggingface.co/collections/Hcompany/holo31

我们期待看到开发者使用Holo3.1构建的应用。

---

> 本文由AI自动翻译，原文链接：[Holo3.1: Fast & Local Computer Use Agents](https://huggingface.co/blog/Hcompany/holo31)
> 
> 翻译时间：2026-06-03 06:50
