---
title: Holotron-12B发布：高吞吐计算机使用智能体，性能提升2倍
title_original: Holotron-12B - High Throughput Computer Use Agent
date: '2026-03-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/Hcompany/holotron-12b
author: ''
summary: H公司发布了基于NVIDIA Nemotron-Nano-2 VL模型的多模态计算机使用模型Holotron-12B。该模型采用混合状态空间模型和注意力机制架构，针对高吞吐推理优化，在WebVoyager基准测试中吞吐量比前代Holo2-8B高出2倍以上，并发处理能力达8.9k
  tokens/s。模型在专有数据上进行了监督微调，在智能体基准测试中表现优异，WebVoyager性能从35.1%提升至80.5%，适用于数据生成、标注等高吞吐工作负载。
categories:
- AI产品
tags:
- 多模态模型
- 智能体
- 高吞吐推理
- 状态空间模型
- 计算机使用
draft: false
translated_at: '2026-03-18T04:53:27.915727'
---

# Holotron-12B - 高吞吐计算机使用智能体

![Screenshot 2026-03-17 at 13.25.28](/images/posts/a742ecbf61a7.png)

我们很高兴发布 Holotron-12B，这是 H 公司推出的多模态计算机使用模型。该模型基于开源的 NVIDIA Nemotron-Nano-2 VL 模型，在 H 公司的专有数据混合集上进行了后训练。Holotron-12B 是我们研究实验室紧密合作的成果，旨在打造一种新型模型，主要针对生产环境中的规模和性能进行优化。

H 公司是 NVIDIA Inception 计划的成员。

该模型现已在 Hugging Face 上提供。

# 我们为何构建 Holotron-12B

当今大多数多模态模型主要针对静态视觉或指令遵循进行优化。然而，Holotron-12B 与我们的 Holo2 模型一样，有着不同的目标：作为计算机使用智能体的策略模型，这些智能体必须在交互环境中高效地感知、决策和行动。

通过 Holotron-12B，我们希望创建一个能够在生产中高效扩展、同时处理包含多张图像的长上下文，并且在智能体基准测试中仍能表现优异的模型。NVIDIA Nemotron 模型在推理方面提供了坚实的基础，而通过开发 Holotron-12B，我们展示了该模型经过进一步训练后所能实现的更大潜力。

## 采用混合 SSM 架构实现高吞吐推理

Holotron-12B 在推理效率上的显著飞跃，得益于其基础的 Nemotron 架构，该架构采用了混合状态空间模型和注意力机制。与纯基于 Transformer 的模型不同，这种设计针对高吞吐服务进行了优化。状态空间模型通过避免与完整注意力机制相关的二次计算成本，为长上下文推理提供了卓越的可扩展性，尤其有利于涉及多张图像和长交互历史的智能体工作负载。在推理方面，SSM 的主要贡献在于其显著减少了内存占用：标准的注意力机制需要为每个 Token 和每个层存储 K 和 V 激活值（即著名的 KV 缓存），而 SSM 是一种线性循环模型，仅为每个生成的序列的每一层存储一个恒定状态，与序列长度无关。

在 WebVoyager 基准测试中，该模型在使用真实世界多模态智能体工作负载（具有长上下文、多张高分辨率图像以及 100 个基准测试工作者的高请求并发性）时表现出色。在单个 H100 GPU 上运行，并使用具有最新 SSM 优化（v0.14.1）的 vLLM，Holotron-12B 的吞吐量比 Holo2-8B 高出 2 倍以上。这使得 Holotron-12B 成为吞吐量受限工作负载（如数据生成、标注和在线强化学习）的有吸引力的选择。

![](/images/posts/c37baa4d1eef.png)

在受控实验设置中（见图 2），随着并发性的增加，Holotron-12B 继续高效扩展，在最大并发数为 100 时，总 Token 吞吐量稳步上升至 8.9k tokens/s。相比之下，Holo2-8B 的总 Token 吞吐量更快地达到平台期，为 5.1k tokens/s。这种行为凸显了 Nemotron 架构的一个关键优势，即更有效、更高效的 VRAM 利用率和更小的整体内存占用，这使得在相同硬件上可以实现更大的有效批处理大小。即使在大批量处理时，Holotron-12B 也能保持强大的吞吐量。

![](/images/posts/f0ff34c623e4.png)

## Holotron-12B 的训练与评估

Holotron-12B 的训练分为两个阶段。我们从 NVIDIA 发布的多模态基础模型 Nemotron-Nano-12B-v2-VL-BF16 开始。然后，我们在 H 公司的专有定位和导航数据混合集上进行了监督微调，重点关注屏幕理解、基础定位和 UI 级别的交互。

最终检查点在大约 140 亿个 Token 上进行了训练。

## 智能体基准测试

在计算机使用和导航基准测试中，Holotron-12B 相较于 Nemotron 基础模型显示出显著改进，并与成熟的智能体模型相比表现出强劲性能。其 WebVoyager 性能从 35.1% 提升至 80.5%，超过了 Holo2-8B 在该基准测试中的表现，证明了该模型在智能体环境中有效执行任务的能力。

![](/images/posts/fb07e91b1559.png)

## 定位基准测试

在定位和基础定位基准测试（如 OS-World-G、GroundUI 和 WebClick）上，Holotron-12B 相较于基础 Nemotron 模型也有显著提升。

![](/images/posts/469d6e4df2eb.png)

# 结论

Holotron-12B 证明，当配合正确的训练设置和基础设施工作时，NVIDIA Nemotron VL 模型为现实世界的多模态智能体提供了坚实的基础。

该模型提供了强大的智能体性能、显著改进的推理吞吐量，以及清晰的未来改进路径，特别是在更高分辨率的视觉训练方面。

我们期待看到其他人使用 Holotron-12B 构建什么。该模型及其检查点现已在 Hugging Face 上提供，遵循 NVIDIA 开放模型许可。

# 下一步：借助 Nemotron 3 Omni 扩展智能体智能的未来

NVIDIA 今日宣布发布 Nemotron 3 Omni。基于 Holotron-12B 的成功，我们正准备对这一下一代多模态模型进行后训练。通过利用 Nemotron 3 系列增强的混合 SSM-注意力 和 MoE 架构基础，我们旨在借助新发布的 Nemotron 3 Omni，在推理能力和多模态精度上实现更大的飞跃。随着这一演进将 Holotron 从研究推向商业应用，它将为企业提供大规模自主“计算机使用”部署所需的高吞吐、低延迟性能。

---

> 本文由AI自动翻译，原文链接：[Holotron-12B - High Throughput Computer Use Agent](https://huggingface.co/blog/Hcompany/holotron-12b)
> 
> 翻译时间：2026-03-18 04:53
