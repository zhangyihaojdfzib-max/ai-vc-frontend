---
title: Mellea 0.4.0 与 Granite 库发布：构建结构化AI工作流
title_original: What's New in Mellea 0.4.0 + Granite Libraries Release
date: '2026-03-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-granite/granite-libraries
author: ''
summary: IBM Research 发布了 Mellea 0.4.0 开源 Python 库及三个 Granite 专用模型库（core、rag、guardian）。Mellea
  旨在通过约束解码、结构化修复循环和可组合流水线，使基于大语言模型的程序变得可维护和可预测。新版本提供了与 Granite 库的原生集成，引入了“指令-验证-修复”模式及可观测性钩子。Granite
  库则是一系列针对特定任务（如需求验证、RAG、安全合规）微调的专用模型适配器，旨在以适中的成本提升任务准确性。
categories:
- AI研究
tags:
- Mellea
- Granite模型
- AI工作流
- 约束解码
- 开源AI
draft: false
translated_at: '2026-03-21T04:31:08.578222'
---

# Mellea 0.4.0 与 Granite 库发布的新内容

## 概述

我们发布了 **Mellea 0.4.0** 以及三个 **Granite 库**：`granitelib-rag-r1.0`、`granitelib-core-r1.0`、`granitelib-guardian-r1.0`。这些版本共同使得在 IBM Granite 模型之上构建结构化、可验证且具备安全意识的 AI 工作流变得更加容易。

Mellea 是一个用于编写生成式程序的开源 Python 库——它用结构化、可维护的 AI 工作流取代了概率性的提示词行为。与通用的编排框架不同，Mellea 旨在通过约束解码、结构化修复循环和可组合的流水线，使基于 LLM 的程序变得可维护和可预测。（初次接触 Mellea？请从我们的[介绍性博客](https://generative-computing.github.io/blog/2025/08/14/thinking-about-ai.html)开始，并[认识我们的团队](https://www.youtube.com/watch?v=j2ouL1n0Nxk)）

## Mellea 0.4.0

Mellea 0.4.0 是由 IBM Research 发起并开发的一个开源研究项目的最新版本。在 0.3.0 版本的基础库和工作流原语之上，0.4.0 版本扩展了库的集成面，并引入了用于构建生成式工作流的新架构模式。

包含内容：

*   与 Granite 库的原生集成，提供了一个标准化的 API，该 API 依赖约束解码来保证模式正确性。
*   通过拒绝采样策略实现的“指令-验证-修复”模式。
*   用于监控和跟踪工作流的事件驱动回调的可观测性钩子。

查看 Mellea 0.4.0 的完整功能与更新列表[请点击此处](https://generative-computing.github.io/blog/2025/08/14/thinking-about-ai.html)

## 什么是 Granite 库

简而言之，Granite 库是一系列专用模型适配器的集合，这些适配器设计用于对输入链或对话的特定部分执行定义明确的操作。与依赖通用提示词不同，每个专用模型都针对特定任务进行了微调，例如查询重写、幻觉检测或策略合规性检查。使用专用适配器使我们能够以适中的参数量成本提高每项任务的准确性，同时不破坏基础模型的能力。

今天为 `granite-4.0-micro` 模型发布了三个库，每个库针对一组不同的流水线任务，并由一系列 LoRA 适配器组成：

*   **Granitelib-core-r1.0**：针对 Mellea “指令-验证-修复”循环中的需求验证步骤。
*   **Granitelib-rag-r1.0**：针对 Agent（智能体）RAG（检索增强生成）流水线中的各种任务，涵盖检索前、检索后和生成后阶段。
*   **Granitelib-guardian-r1.0**：专注于安全性、事实性和策略合规性的专用模型。

Mellea 0.4.0 是由 IBM Research 发起并开发的一个开源研究项目的最新版本。在 0.3.0 版本引入的基础库和工作流原语之上，此版本扩展了集成面，并引入了用于构建生成式工作流的新架构模式。

## 开始使用

### Mellea

*   [Mellea GitHub 仓库](https://github.com/IBM/mellea)
*   [PyPI 上的 Mellea](https://pypi.org/project/mellea/)
*   [Mellea 文档](https://mellea.readthedocs.io/)

### Granite 库

*   [Granite 库 Hugging Face 集合](https://huggingface.co/collections/ibm-granite/granite-libraries-674f4e4a5a5c5d5e5f5a5b5c)
*   [用于检索增强生成的 LLM 内在特性库](https://arxiv.org/abs/2406.07594)
*   [生成式语言模型的多层次解释](https://arxiv.org/abs/2406.07595)

### 了解更多

*   https://generative-computing.github.io/blog/2025/08/14/thinking-about-ai.html
*   https://www.youtube.com/watch?v=j2ouL1n0Nxk

---

> 本文由AI自动翻译，原文链接：[What's New in Mellea 0.4.0 + Granite Libraries Release](https://huggingface.co/blog/ibm-granite/granite-libraries)
> 
> 翻译时间：2026-03-21 04:31
