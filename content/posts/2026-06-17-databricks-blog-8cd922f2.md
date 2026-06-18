---
title: Databricks与NVIDIA联手打造智能体时代AI平台
title_original: 'Databricks and NVIDIA: Building for the Agentic Era'
date: '2026-06-17'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-and-nvidia-building-agentic-era
author: ''
summary: Databricks与NVIDIA深化合作，构建端到端AI平台，加速模型训练、推理及智能体开发。新增功能包括AI Runtime多节点训练、Free
  Edition GPU支持、模型服务增强，并集成NVIDIA Agent Toolkit等行业框架。双方还推出专为智能体工作负载设计的NVIDIA Vera CPU，以解决编排和工具调用瓶颈，助力医疗、供应链等领域的AI应用落地。
categories:
- AI基础设施
tags:
- Databricks
- NVIDIA
- 智能体
- GPU加速
- AI基础设施
draft: false
translated_at: '2026-06-18T06:55:26.678725'
---

- Databricks 与 NVIDIA 正在深化合作，共同打造一个端到端的 AI 平台，在受治理的企业数据上加速模型训练、推理以及 Agent（智能体）AI 开发。
- 新增功能包括 AI Runtime 中的多节点训练、Databricks Free Edition 中的 GPU 支持、模型服务增强，以及对 NVIDIA Agent Toolkit 等 NVIDIA 技术的支持。
- 客户可直接在 Databricks 中利用 NVIDIA 的行业特定 AI 框架，加速在医疗、生命科学、供应链、机器人、数字孪生和文档智能等领域的应用落地。

全栈 AI，加速前行

NVIDIA 加速计算为 Databricks 上最严苛的 AI 工作负载提供动力，涵盖从大规模训练、微调、推理到行业特定 AI 解决方案的方方面面。在今天的数据与 AI 峰会上，我们将重点展示 NVIDIA AI 基础设施如何成为 Databricks AI Runtime、模型服务和行业 AI 解决方案等多项新公告的核心，并探讨全新的 NVIDIA Vera CPU 将如何驱动下一代 Agent（智能体）基础设施。

以下是 Databricks 与 NVIDIA 共同构建 AI 平台的方式，从用于训练和推理的 GPU，到专为 Agent（智能体）时代打造的特制 CPU。

## 1. 训练与微调

Databricks AI Runtime（AIR）将 NVIDIA GPU 加速能力直接带给数据和 AI 团队，使他们能够在受治理的企业数据上训练和微调模型，而无需管理独立的 GPU 基础设施。通过 AIR，客户可以直接在其受治理数据所在的 Databricks 环境中获得先进的 NVIDIA 硬件和网络：

- 配备 NVIDIA Quantum InfiniBand 的 NVIDIA Hopper GPU：专为多节点分布式训练而设计。无论您是预训练基础模型，还是进行大规模微调，AIR 都内置了对 NVIDIA 高带宽、低延迟 GPU 互连（支持 RDMA 的网络）的支持，消除了跨节点的通信瓶颈。AIR 也正在为 NVIDIA Blackwell 架构做准备，确保客户始终处于加速计算的最前沿。
- Free Edition 中的 NVIDIA GPU：在 DAIS 上，我们很高兴地宣布 Databricks Free Edition 支持 GPU，助力全球的开发者、学生和初创公司在 GPU 上构建和部署其 AI 工作负载。
- 支持 NVIDIA 容器：不久后，Databricks 将支持 NGC 容器和自定义 NVIDIA CUDA 环境，使其能够在平台内原生运行数据。

![AI Runtime 可在 Databricks 内无缝访问 NVIDIA GPU。](/images/posts/4328ea7121af.gif)

AI Runtime 可在 Databricks 内无缝访问 NVIDIA GPU。

## 2. 推理：Databricks 模型服务中的 NVIDIA 加速

Databricks 模型服务为数千名 Databricks 客户提供生产级推理能力。模型服务的核心是 NVIDIA 硬件和软件，它们为我们的客户提供所需的低延迟、高吞吐量的大规模推理，涵盖 Qwen、GPT-OSS 等前沿模型以及客户构建的自定义神经网络。其他服务能力包括 NVIDIA 硬件和 Triton 推理服务器。模型服务支持领先的推理优化 GPU，并将很快提供 Triton 先进的动态批处理和优化性能。通过模型服务，客户可以直接在受管理的 Databricks 基础设施上，为他们使用 NVIDIA 硬件训练的模型提供服务。

## 3. Agent（智能体）基础设施：探索用于下一个计算瓶颈的 NVIDIA Vera

自主 Agent（智能体）的兴起带来了新的基础设施挑战。虽然 GPU 擅长模型推理，但 Agent（智能体）的编排、工具调用、基于 CPU 的分析以及管理多步推理，所有这些都在 CPU 上运行。如今的 CPU 常常成为瓶颈：工具调用的延迟、Agent（智能体）步骤间的通信开销，以及负载下的性能不一致，都降低了 Agent（智能体）的体验。

NVIDIA Vera 是专为此类工作负载设计的下一代 CPU。Vera 针对三个核心用例——Agent（智能体）工作负载、强化学习和基于 CPU 的数据分析——进行了设计，提供：

- 高性能的 NVIDIA 设计、兼容 Arm 的内核，SQL 查询速度提升高达 3 倍，Agent（智能体）性能提升高达 80%，针对工具调用和 Agent（智能体）编排等延迟敏感、突发性的计算模式进行了优化
- 巨大的内存带宽，用于 Agent（智能体）在模型调用之间执行的数据密集型操作
- 快速的内核间通信，有助于在 Agent（智能体）复杂性增加时提供可预测的性能

愿景是在 Databricks 上构建一个端到端的 NVIDIA 加速堆栈：模型在 NVIDIA GPU 上运行以进行推理，而 Agent（智能体）编排和工具调用可以在 Vera CPU 上运行，每个工作负载都运行在为其特性量身定制的芯片上。开发人员使用专有数据在 Databricks 上自定义模型，通过模型服务进行部署，而周围的 Agent（智能体）基础设施则运行在从一开始就为该模式设计的计算之上。

## 4. 开发者体验：让加速 AI 更易于构建

### NVIDIA Agent Toolkit：在 Databricks 上部署

基于 Databricks Apps，团队可以直接在其 Databricks 环境中托管和运行 NVIDIA Agent Toolkit——NVIDIA 用于构建、自定义和部署 Agent（智能体）AI 工作流的开源开发平台。这意味着您可以获得：

- NVIDIA Agent Toolkit 功能：护栏、工具使用、检索增强生成和多步推理，运行在 Databricks 托管的应用程序中。
- Databricks Apps 作为托管层：部署任何代码库，包括使用 NVIDIA Agent Toolkit 构建的 Agent（智能体）或服务，作为托管应用程序，并通过 Unity Catalog 提供内置的身份验证、网络和治理功能。
- 与 Databricks 的数据、模型和服务基础设施无缝集成。您的 Agent（智能体）可以访问受治理的数据，通过 FMAPI 调用模型，并在不离开环境的情况下利用整个平台。

### 使用 Genie Code 处理 GPU 工作负载

GPU 功能强大，但要实现高利用率、诊断性能问题以及调试工作负载，传统上需要深厚的系统专业知识。我们正在通过一种以 Agent（智能体）为先的方法来改变这一现状：

Genie Code 支持围绕 NVIDIA 硬件和软件设计的技能。开发者可以：

- 对话式调试 GPU 工作负载：描述问题，获取可操作的指导
- 性能优化：识别利用率瓶颈、内存问题和通信开销
- 利用 NVIDIA 特定知识：理解 CUDA、cuDNN、NCCL 和 NVIDIA 性能分析工具的技能

Genie Code 和 NVIDIA 调试工具也与各种 Databricks 产品界面完全集成，包括：

- 笔记本：在笔记本环境中提供一流的 GPU 监控、性能分析和调试
- MLflow：跟踪 GPU 指标和利用率以及实验
- 模型服务：诊断端点健康和 GPU 性能，识别优化端点机制（如自动缩放）的机会

![image2.gif](/images/posts/d58ab72ea693.gif)

## 5. 行业 AI：受治理的 Databricks 数据上的 NVIDIA 软件

每个行业都面临着由其生成的数据和构建的模型所塑造的独特计算挑战。这些挑战涵盖从分析基因组和加速药物发现，到优化供应链、解读医学图像，以及模拟工厂、机器人和数字孪生等方方面面。

为了帮助解决这些问题，NVIDIA 在领域特定的加速计算库和框架上投入了大量资源。我们很高兴将这些能力直接引入 Databricks 平台。

客户可以在端到端的 Databricks 体验中利用 NVIDIA 的加速计算堆栈——从数据工程和实验，到模型开发和生产工作流；现在，特定领域的研发团队无需离开 Databricks 平台，即可使用 NVIDIA 的加速能力。

该合作伙伴关系涵盖NVIDIA的加速计算库和领域框架，客户可将其与Databricks结合使用，以处理特定行业的人工智能工作负载：

## 展望未来：为Agent（智能体）时代而构建

NVIDIA AI基础设施支持Databricks上人工智能的关键层级：驱动训练和推理的GPU、为Agent（智能体）编排和数据分析提供动力的Vera CPU、支持Agent（智能体）应用的NVIDIA Agent Toolkit，以及帮助您充分利用每个计算周期的开发者工具。

无论您是初创公司在Free Edition中首次尝试GPU工作负载，还是制药公司运行BioNeMo进行药物发现，亦或是大规模部署前沿模型的企业，Databricks和NVIDIA共同为您提供所需的性能、简洁性和治理能力。

立即开始：在Databricks Free Edition中试用NVIDIA GPU，在Databricks Apps上部署NVIDIA Agent Toolkit，或探索由NVIDIA加速计算驱动的基础模型API。

### 将最新文章发送至您的收件箱

订阅我们的博客，即可将最新文章直接发送至您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Databricks and NVIDIA: Building for the Agentic Era](https://www.databricks.com/blog/databricks-and-nvidia-building-agentic-era)
> 
> 翻译时间：2026-06-18 06:55
