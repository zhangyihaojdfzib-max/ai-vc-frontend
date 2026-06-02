---
title: JetBrains发布120亿参数混合专家模型Mellum2
title_original: 'Introducing Mellum2: A 12B Mixture-of-Experts Model by JetBrains'
date: '2026-06-01'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/JetBrains/mellum2-launch
author: ''
summary: JetBrains推出Mellum2，一个120亿参数的混合专家模型，专为低延迟文本和代码工作负载优化。该模型每个Token仅激活25亿参数，推理速度提升超2倍，适用于路由、RAG、摘要、子Agent及私有部署等场景。基于Apache
  2.0开源，在代码生成、推理等基准测试中与同类模型竞争，同时保持高效推理。文章强调范围明确的模型在非单一化AI系统中的重要性。
categories:
- AI产品
tags:
- Mellum2
- 混合专家模型
- JetBrains
- 低延迟推理
- 开源模型
draft: false
translated_at: '2026-06-02T06:34:00.621985'
---

# 介绍 Mellum2：JetBrains 推出的 120 亿参数混合专家模型

- Mellum2 是一个 120 亿参数的混合专家模型，基于自然语言和代码从零开始训练。
- 该模型每个 Token 仅激活 25 亿参数，使其适用于高吞吐量、低延迟推理。
Mellum2 可用于路由、RAG（检索增强生成）、摘要、子 Agent（智能体）、高吞吐量编码功能以及私有部署。
- 它基于 Apache 2.0 许可证发布。
- 与类似规模的模型相比，Mellum2 在基准测试中具有竞争力，同时推理速度提升超过 2 倍。
- 在 Hugging Face 上下载模型：https://huggingface.co/collections/JetBrains/mellum-2
- 有关架构细节、训练设置、基准测试和评估方法，请阅读完整技术报告：https://arxiv.org/pdf/2605.31268

今天，我们发布 Mellum2，这是一个针对低延迟文本和代码工作负载优化的开源混合专家模型。
Mellum 最初是一个代码补全模型。通过 Mellum2，我们将这一基础扩展到更广泛的自然语言和软件工程任务，同时保持模型专注于高效推理和可部署性。
现代 AI 系统越来越依赖多次模型调用：路由、检索、摘要、规划、验证和工具使用。其中许多操作对延迟敏感，且不需要使用最大的可用模型。
Mellum2 正是针对这些工作负载而设计。

## 基准测试亮点

![Mellum 2 评估](/images/posts/f68702874ae7.jpg)

在我们的技术报告中，我们评估了 Mellum2 在代码生成、推理、科学和数学基准测试中的表现。
Mellum2 与类似规模的开源模型相比具有竞争力，同时推理速度提升超过 2 倍，使其适用于高吞吐量的生产工作负载。
模型架构
Mellum2 是一个混合专家模型：

MoE 架构在保持总模型容量较高的同时，每个 Token 仅激活部分参数。这使得推理更加高效，并有助于降低实时工作负载的服务成本。
Mellum2 有意专注于文本和代码，而非多模态任务。这种专业化使模型保持紧凑高效，适用于软件工程工作负载。

## 关键用例

### 路由与编排

Mellum2 在多模型系统中作为轻量级路由和编排模型表现出色，包括提示词分类、工具选择和中间控制流步骤。

### RAG（检索增强生成）管道

该模型非常适合对延迟敏感的检索管道，包括上下文压缩、摘要和检索后处理。

### 子 Agent（智能体）

Mellum2 可用于 Agent（智能体）子任务，如规划、验证、转换和上下文准备，从而减少在中间操作中调用更大模型的需求。

### 私有部署

由于 Mellum2 是开源的且服务效率高，它可以部署在涉及专有代码或内部数据的自托管环境中。

## 为什么范围明确的模型很重要

随着 AI 系统的成熟，最有效的架构正变得越来越非单一化。
一个前沿模型可能很强大，但生产系统通常需要多个专业化组件协同工作：检索器、路由器、代码感知模型、验证器、工具调用者和更大的推理模型。
我们将 Mellum2 视为一个“焦点”模型：一个快速、范围明确的模型，针对更大 AI 系统中的高频任务进行了优化。
目标不是取代堆栈中的每个模型。目标是让堆栈更快、更便宜、更易于控制。

## 开始使用 Mellum2

如果你正在为软件工程构建 AI 系统——无论是在 IDE 内部、在 RAG（检索增强生成）管道中、作为 Agent（智能体）工作流的一部分，还是在私有基础设施上——Mellum2 都值得一试。

---

> 本文由AI自动翻译，原文链接：[Introducing Mellum2: A 12B Mixture-of-Experts Model by JetBrains](https://huggingface.co/blog/JetBrains/mellum2-launch)
> 
> 翻译时间：2026-06-02 06:34
