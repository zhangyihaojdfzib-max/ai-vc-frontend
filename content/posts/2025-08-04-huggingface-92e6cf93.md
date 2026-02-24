---
title: 开源Llama Nemotron模型在DeepResearch Bench评测中表现卓越
title_original: Measuring Open-Source Llama Nemotron Models on DeepResearch Bench
date: '2025-08-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/ai-q-top-ranking-open-portable-deep-research-agent
author: ''
summary: 英伟达AI-Q智能体融合Llama 3.3-70B Instruct与Llama-3.3-Nemotron-Super-49B-v1.5模型，在Hugging
  Face DeepResearch Bench“带搜索的LLM”排行榜中位居榜首。该开源堆栈通过多阶段后训练、透明推理轨迹和高效架构，实现了媲美闭源方案的深度研究能力，支持长上下文检索、多步推理与工具调用，证明了开源AI在复杂智能体任务中的领先地位。
categories:
- AI研究
tags:
- 开源大模型
- 智能体评测
- Llama Nemotron
- DeepResearch Bench
- AI-Q
draft: false
translated_at: '2026-02-24T04:34:43.087366'
---

# 在DeepResearch Bench上评测开源Llama Nemotron模型

贡献者：David Austin、Raja Biswas、Gilberto Titericz Junior，英伟达

英伟达的AI-Q Blueprint——领先的便携式开源深度研究智能体——最近登顶了Hugging Face DeepResearch Bench的“带搜索的LLM”排行榜。这是开源AI堆栈向前迈出的重要一步，证明了开发者可访问的模型能够驱动媲美甚至超越闭源方案的先进智能体工作流。

AI-Q有何独特之处？它融合了两个高性能开源LLM——Llama 3.3-70B Instruct和Llama-3.3-Nemotron-Super-49B-v1.5——来协调长上下文检索、智能体推理和稳健的综合分析。

## 核心堆栈：模型选择与技术革新

- **Llama 3.3-70B Instruct**：流畅、结构化报告生成的基础，源自Meta的Llama系列，采用开放许可，可无限制部署。
- **Llama-3.3-Nemotron-Super-49B-v1.5**：一个经过优化、专注于推理的变体。通过神经架构搜索（NAS）、知识蒸馏以及多轮监督学习和强化学习构建，擅长多步推理、查询规划、工具使用和反思——同时具有更小的内存占用，可在标准GPU上高效部署。

AI-Q参考示例还包括：

- **NVIDIA NeMo Retriever**：用于可扩展的多模态搜索（内部+外部）。
- **NVIDIA NeMo Agent工具包**：用于编排复杂的多步智能体工作流。

该架构支持对本地和网络数据进行并行、低延迟搜索，非常适合那些需要隐私、合规性或本地部署以降低延迟的用例。

## 使用Llama Nemotron进行深度推理

英伟达Llama Nemotron Super不仅仅是一个经过微调的指令模型——它经过了针对显式智能体推理的后训练，并支持通过系统提示词切换推理的开启/关闭。您可以在标准聊天LLM模式下使用它，也可以切换到深度思维链推理模式以用于智能体流水线——从而实现动态、上下文感知的工作流。

关键亮点：

- **多阶段后训练**：结合了指令遵循、数学/编程推理和工具调用技能。
- **透明的模型谱系**：可直接追溯到开放的Meta权重，并在合成数据和调优数据集方面具有额外的开放性。
- **高效性**：490亿参数，上下文窗口高达128K Token，可在单块H100 GPU或更小的设备上运行，保持推理成本可预测且快速。

## 评估：指标中的透明度与稳健性

AI-Q的核心优势之一是透明度——不仅体现在输出上，还体现在推理轨迹和中间步骤上。在开发过程中，英伟达团队利用了标准和新的指标，例如：

- **幻觉检测**：每个事实性主张在生成时即被检查。
- **多源综合**：从不同证据中综合出新见解。
- **引用可信度**：对主张-证据链接进行自动评估。
- **RAGAS指标**：对检索增强生成准确性的自动评分。

该架构非常适合进行细粒度、逐步的评估和调试——这是智能体流水线开发中最大的痛点之一。

## 基准测试结果：DeepResearch Bench

DeepResearch Bench使用一套包含100多个长上下文、真实世界研究任务（涵盖科学、金融、艺术、历史、软件等领域）来评估智能体堆栈。与传统问答不同，这些任务需要报告长度的综合分析和复杂的多跳推理：

- 截至2025年8月，AI-Q在“带搜索的LLM”类别中获得了40.52的总分，目前在完全开放许可的堆栈中位居榜首。
- 最强的指标：全面性（报告深度）、洞察力（分析质量）和引用质量。

## 致Hugging Face开发者社区

- **Llama-3.3-Nemotron-Super-49B-v1.5**和**Llama 3.3-70B Instruct**均可在Hugging Face上直接使用/下载。您可以用几行Python代码在您自己的流水线中尝试它们，或者使用vLLM进行部署以获得快速推理和工具调用支持（代码/服务示例请参见模型卡片）。
- 开放的后训练数据、透明的评估方法和宽松的许可，使得实验和可复现性成为可能。

## 要点总结

开源生态系统正在迅速缩小差距，并在某些重要的真实世界智能体任务领域处于领先地位。基于Llama Nemotron构建的AI-Q证明，您无需在透明度或控制力上妥协，也能实现最先进的结果。

请从Hugging Face或build.nvidia.com尝试该堆栈，或将其适配到您自己的研究智能体项目中。

---

> 本文由AI自动翻译，原文链接：[Measuring Open-Source Llama Nemotron Models on DeepResearch Bench](https://huggingface.co/blog/nvidia/ai-q-top-ranking-open-portable-deep-research-agent)
> 
> 翻译时间：2026-02-24 04:34
