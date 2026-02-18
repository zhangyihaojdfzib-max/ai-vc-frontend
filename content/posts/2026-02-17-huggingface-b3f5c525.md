---
title: NVIDIA发布Nemotron 2 Nano 9B日语模型，助力日本主权AI发展
title_original: 'NVIDIA Nemotron 2 Nano 9B Japanese: 日本のソブリンAIを支える最先端小規模言語モデル'
date: '2026-02-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/nemotron-nano-9b-v2-japanese-ja
author: ''
summary: NVIDIA发布了专为日语优化的Nemotron-Nano-9B-v2-Japanese小规模语言模型，该模型在小于10B参数类别中实现了SOTA性能。它基于经过验证的Nemotron
  2 Nano架构，并利用Nemotron-Personas-Japan合成数据集进行训练，旨在解决日本企业AI在高级日语理解和智能体任务执行能力方面的缺口。该模型支持本地部署，降低基础设施门槛，并能高效定制以加速企业AI应用开发。
categories:
- AI产品
tags:
- NVIDIA
- 小规模语言模型
- 日语AI
- 主权AI
- 智能体
draft: false
translated_at: '2026-02-18T04:35:19.400790'
---

# NVIDIA Nemotron 2 Nano 9B Japanese：支撑日本主权AI的尖端小规模语言模型

NVIDIA Nemotron 不仅提供开源模型，还提供数据集、库、配方和手册，以推动主权AI发展，使开发者能够定制模型，适应多样化的用例和语言。

今天，NVIDIA 发布了 NVIDIA Nemotron-Nano-9B-v2-Japanese，该模型在 Nejumi Leaderboard 4 的参数规模小于10B类别中，实现了最先进的性能（SOTA）。

该模型以易于部署的轻量级尺寸，实现了高级日语理解和强大的 Agent（智能体）功能，是日本企业AI开发的一个重要里程碑。这一成就是建立在两个关键基础之上的：经过验证的 Nemotron-Nano-9B-v2 架构，以及由 Nemotron-Personas-Japan 实现的高质量日语合成数据生成（SDG）。

我们的目标是通过对已发布的 Nemotron 2 Nano 模型进行日语定制，激励社区开发和发布适应多样化用例和语言的定制化尖端模型。Nemotron 团队将把从此次定制中获得的见解应用于未来的 Nemotron 版本，以增强日语推理能力。

## SLM（小规模语言模型）在日本企业中的重要性

日本企业AI的关键缺口：当前日本的企业AI环境面临一个挑战：几乎没有同时具备“高级日语能力”和“作为 Agent（智能体）AI的任务执行能力”的 SLM。这导致了部署障碍，尤其是在以下方面：

本地部署要求：处理机密数据的企业必须在私有网络内运行模型。参数少于100亿（10B）的模型可以在保持实用性能的同时，显著降低基础设施方面的部署门槛。

提高定制效率：从一个已具备验证过的 Agent（智能体）能力的强大日语基础模型开始，可以缩短微调周期。这使得计算资源可以集中在适应特定领域，而非构建基础能力上。

加速 Agent（智能体）开发：该模型的架构和性能使得能够快速原型化多 Agent（智能体）系统和复杂工作流，而无需像大模型那样产生高昂开销。

## 利用经过验证的基础

### Nemotron 2 Nano：卓越的架构

Nemotron-Nano-9B-v2-Japanese 基于 NVIDIA Nemotron-Nano-9B-v2 构建，后者在英语基准测试中展现了卓越的尺寸与性能比。我们在这个高效架构的基础上进行了进一步的定制，以增强日语能力。该架构具有以下特点：

- 实现高级推理能力并优化参数效率
- 为多语言适应提供坚实基础
- 经过验证的 Agent（智能体）任务执行能力

通过将这个经过验证的架构适配到日语，我们在保持基础模型优势的同时，实现了出色的日语能力。

### Nemotron-Personas-Japan：高质量合成数据生成的种子集

本模型的数据策略侧重于将开源（CC BY 4.0）数据集 "Nemotron-Personas-Japan" 作为高质量合成数据生成（SDG）的种子。该数据集由基于日本现实世界人口统计、地理分布和性格特征分布合成的角色组成，捕捉了人口的多样性和丰富性。我们以这些文化上准确的角色为基础，构建了一个高度多样化、可扩展且稳健的训练流程。丰富的种子角色群使我们能够高效地扩展出涵盖多样化场景和细微差别的合成数据集。这种方法确保了扩展数据在保持原始角色严格文化一致性的同时，达到了尖端训练所需的规模。

特别是在 Nemotron-Nano-9B-v2-Japanese 中，我们利用这些角色作为工具调用场景中训练数据的生成基础。这确保了模型获得的能力不仅仅是工具调用功能，而且是文化上恰当的日语对话，并植根于现实世界的用例。

Nemotron-Personas 集合还包括美国、印度、新加坡和巴西的数据集，使得可以在不同地区复制相同的方法。

## 训练流程

Nemotron-Nano-9B-v2-Japanese 是通过结合日语开源语料库和 NVIDIA 的 Nemotron 技术栈，构建了从持续预训练、合成数据生成到后训练的完整流程。

![training_diagram](/images/posts/a45ad9f3f1c2.png)

### 持续预训练

- Japanese OSS Corpus: Wikipedia, fineweb-2 Japanese, aozorabunko, sip3-ja-general-web-corpus
- Nemotron-CC-v2.1
- Nemotron-Pretraining-Specialized-v1

- 以 Nemotron-Personas-Japan 为种子集的工具调用数据集
- Nemotron-Post-Training-v3

### 用于 Nemotron-Nano-9B-v2-Japanese 的软件

- Megatron-LM：用于持续预训练和 SFT
- NeMo Curator：用于数据预处理和过滤

为了最大化模型的日语能力，我们进行了持续预训练。在此过程中，我们最大限度地利用了日本代表性开源 LLM 社区 LLM-jp 的资产。同时，我们利用了 Nemotron 预训练数据集，以保持模型的 Agent（智能体）功能。

用于 SFT 的、以 Nemotron-Personas-Japan 为种子的工具调用数据集非常强大。性能提升不仅限于工具调用，还广泛涵盖了日语知识、问答、指令遵循等方面。此外，由于这个种子集是基于 600 万个角色构建的，我们能够有效地扩展 SDG。这使我们能够以最小的重复，成功覆盖现实世界中的多样化场景。Nemotron-Personas 集合正在扩大目标国家范围，不仅日本，其他地区的开发者也可以采用类似的方法。

模型的训练继承了在 Nemotron Nano 2 中确立的训练配方。这使得我们能够在不引入训练不稳定的情况下提高吞吐量。

这种方法实现了作为强大日语语言模型的性能，同时保持了稳健的工具调用功能和推理能力。

## 基准测试性能

![leaderboard](/images/posts/42a64cfc8953.png)

Nemotron-Nano-9B-v2-Japanese 在日本最全面的 LLM 评估平台 "Nejumi Leaderboard 4" 中，在小于10B的模型类别中获得了第一名。Nejumi Leaderboard 通过涵盖以下领域的约 40 个基准测试，对模型进行多维度评估：

- 基础语言能力：日语理解和生成
- Agent（智能体）能力：代码生成、数学推理、工具使用等
- 对齐：指令遵循能力、偏见、毒性、真实性、稳健性等

通过这些多维度的评估，Nejumi Leaderboard 成为在日本环境下为定制或实际应用选择基础模型的开发者们值得信赖的参考。

![benchmark_summary](/images/posts/4529c3971b94.png)

基准测试结果证实，Nemotron-Nano-9B-v2-Japanese 成功地将强大的日语能力整合到了其基础模型 Nemotron-Nano-9B-v2 中。这些改进不仅限于日语知识或问答能力，还涵盖了工具调用、编码、对齐等广泛任务。值得注意的是，它超越了同等规模的 Qwen3-8B，实现了卓越的尺寸与性能比。

## 技术优势

![throughput](/images/posts/124aa5e22bb0.png)

- 推理效率：继承了 Nemotron 2 Nano（Transformer-Mamba）的架构，使其可以部署在边缘 GPU 上，同时与开源替代模型相比，实现了高达 6 倍的吞吐量提升。上图展示了 Nemotron 2 Nano 论文中测量的结果。
- 上下文处理：针对多轮对话和工具操作进行了优化。
- 工具调用可靠性：具备强大的结构化数据生成能力，用于 API 调用或函数执行。
- 微调效率：其参数规模使得即使在适中的计算基础设施上也能进行全量微调。

## 部署选项

#### 直接部署

对于需要高级日语理解和 Agent（智能体）技能的应用，可以直接部署并利用该模型。其已具备的能力支持即时集成到 Agent（智能体）工作流中。Nemotron 2 Nano 支持的推理引擎可以无缝迁移。

#### 针对特定领域的定制

可以将 Nemotron-Nano-9B-v2-Japanese 用作针对特定领域进行微调的基础。其在基准测试中证明的日语和 Agent（智能体）任务的良好性能，为专业应用开发提供了坚实的起点。您可以使用 NeMo Framework（NeMo Megatron-Bridge, NeMo AutoModel, and NeMo-RL）进行定制。

## 立即开始使用

日本的AI应用开发者现在就可以开始使用 Nemotron-Nano-9B-v2-Japanese。无论是用于客户服务 Agent（智能体）、内部自动化工具，还是领域专用助手，该模型都能提供实际部署所需的卓越尺寸与性能比。

经过验证的 Nemotron 2 Nano 架构与作为高质量数据集种子的 Nemotron-Personas-Japan 的结合，将成为日本主权AI开发的一个高效起点。

我们欢迎社区利用 Nemotron 模型、数据集、配方和库，并为更多语言和用例定制 Nemotron 模型。我们期待看到您构建的作品！

通过订阅 [NVIDIA 新闻](https://www.nvidia.com/en-us/news/) 并在 [LinkedIn](https://www.linkedin.com/company/nvidia/)、[X](https://twitter.com/NVIDIAAI)、[YouTube](https://www.youtube.com/c/NVIDIA) 和 [Discord](https://discord.com/invite/nvidia) 上的 [Nemotron 频道](https://discord.com/channels/1234567890/1234567890) 上关注 NVIDIA AI，随时了解 NVIDIA Nemotron 的最新动态。

在 [Hugging Face](https://huggingface.co/NVIDIA) 上访问开源的 Nemotron 模型，并在 [build.nvidia.com](https://build.nvidia.com) 上查看一系列 NIM 微服务和开发者示例。

---

> 本文由AI自动翻译，原文链接：[NVIDIA Nemotron 2 Nano 9B Japanese: 日本のソブリンAIを支える最先端小規模言語モデル](https://huggingface.co/blog/nvidia/nemotron-nano-9b-v2-japanese-ja)
> 
> 翻译时间：2026-02-18 04:35
