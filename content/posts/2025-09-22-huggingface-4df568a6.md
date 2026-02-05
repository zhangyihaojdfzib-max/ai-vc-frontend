---
title: SyGra：为LLM/SLM构建数据的一站式框架
title_original: 'SyGra: The One-Stop Framework for Building Data for LLMs and SLMs'
date: '2025-09-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ServiceNow-AI/sygra-data-gen-framework
author: ''
summary: 本文介绍了SyGra，一个旨在简化为大语言模型（LLM）和小语言模型（SLM）创建、转换和对齐数据集的低代码/无代码框架。文章首先列举了在模型训练中常见的数据挑战，如缺失复杂场景、知识库转问答、生成偏好对等。SyGra通过提供统一的Python库和框架，支持多种推理后端，允许用户专注于提示词工程，而无需编写复杂的数据处理管道，从而帮助团队加速模型对齐、节省工程时间并提升模型在特定任务上的鲁棒性。
categories:
- AI基础设施
tags:
- 大语言模型
- 数据工程
- 机器学习框架
- 模型训练
- 低代码
draft: false
translated_at: '2026-02-05T04:14:02.214282'
---

# SyGra：为LLM和SLM构建数据的一站式框架

当我们考虑构建模型时——无论是大语言模型（LLM）还是小语言模型（SLM）——首先需要的就是数据。虽然存在大量开源数据，但它们很少以训练或对齐模型所需的精确格式呈现。
在实践中，我们常常面临原始数据不足的场景。我们需要更结构化、更特定领域、更复杂或与当前任务更匹配的数据。让我们看看一些常见情况：

#### 缺失复杂场景

你从一个简单的数据集开始，但模型在高级推理任务上表现不佳。如何生成更复杂的数据集来提升性能？

#### 知识库转问答

你已经拥有一个知识库，但它不是问答格式。如何将其转化为可用的问答数据集？

#### 从SFT到DPO

你已经准备了监督微调（SFT）数据集。但现在你想使用直接偏好优化（DPO）来对齐你的模型。如何生成偏好对？

#### 问题深度

你有一个问答数据集，但问题很浅显。如何创建深入的、多轮次的或需要大量推理的问题？

#### 特定领域的中期训练

你拥有海量语料库，但需要为特定领域的中期训练筛选和整理数据。

#### PDF和图像转文档

你的数据存在于PDF或图像中，需要将其转换为结构化文档以构建问答系统。

#### 提升推理能力

你已经拥有推理数据集，但希望推动模型产生更好的“思维Token”以进行逐步问题求解。

#### 质量过滤

并非所有数据都是好数据。如何自动过滤掉低质量样本，只保留高价值数据？

#### 从小上下文到大上下文

你的数据集包含小块上下文，但你想构建针对RAG（检索增强生成）管道优化的大上下文数据集。

#### 跨语言转换

你拥有德语数据集，但需要将其翻译、调整并重新用于英语问答系统。
诸如此类的需求还有很多。在处理现代AI模型时，数据构建的需求永无止境。

## 引入SyGra：应对所有数据挑战的统一框架

这正是SyGra的用武之地。SyGra是一个低代码/无代码框架，旨在简化为LLM和SLM创建、转换和对齐数据集的过程。你无需编写复杂的脚本和管道，只需专注于提示词工程，而繁重的工作则由SyGra处理。SyGra的主要特性：

- ✅ Python库 + 框架：通过SyGra库轻松集成到现有ML工作流中。
- ✅ 支持多种推理后端：与vLLM、Hugging Face TGI、Triton、Ollama等无缝协作。
- ✅ 低代码/无代码：无需大量工程工作即可构建复杂数据集。
- ✅ 灵活的数据生成：从问答到DPO，从推理到多语言，SyGra适应你的用例。

## SyGra为何重要

数据是AI的基石。数据的质量、多样性和结构通常比模型架构的调整更重要。通过实现灵活且可扩展的数据集创建，SyGra帮助团队：

- 加速模型对齐（SFT、DPO、RAG管道）。
- 通过即插即用的工作流节省工程时间。
- 提升模型在复杂和特定领域任务上的鲁棒性。
- 减少手动整理数据集的工作量。

注：示例实现可在 https://github.com/ServiceNow/SyGra/blob/main/docs/tutorials/image_to_qna_tutorial.md 找到

## SyGra架构

部分示例任务 https://github.com/ServiceNow/SyGra/tree/main/tasks/examples

## 最后思考

构建和完善数据集的旅程永无止境。每个用例都带来新的挑战——从翻译和知识库转换到推理增强和领域过滤。有了SyGra，你无需每次都重复造轮子。
相反，你获得了一个统一的框架，使你能够为模型生成、过滤和对齐数据——从而让你专注于真正重要的事情：构建更智能的AI系统。

## 参考文献

- 论文链接：https://arxiv.org/abs/2508.15432
- 文档：https://servicenow.github.io/SyGra/
- Git仓库：https://github.com/ServiceNow/SyGra

---

> 本文由AI自动翻译，原文链接：[SyGra: The One-Stop Framework for Building Data for LLMs and SLMs](https://huggingface.co/blog/ServiceNow-AI/sygra-data-gen-framework)
> 
> 翻译时间：2026-02-05 04:14
