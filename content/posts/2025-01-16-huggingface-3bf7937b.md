---
title: TGI引入多后端支持，统一LLM推理部署
title_original: Introducing multi-backends (TRT-LLM, vLLM) support for Text Generation
  Inference
date: '2025-01-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/tgi-multi-backend
author: ''
summary: Hugging Face为文本生成推理（TGI）引入多后端架构，支持集成TensorRT-LLM、vLLM、llama.cpp等推理引擎。通过统一的Rust前端层，用户可根据模型、硬件和性能需求灵活切换后端，简化生产部署。文章介绍了底层机制（Backend
  trait接口）及2025年路线图，包括与NVIDIA、AWS、Google等合作优化GPU、CPU、TPU等硬件支持，旨在降低LLM部署复杂度并提升性能。
categories:
- AI基础设施
tags:
- TGI
- 多后端
- LLM部署
- 推理引擎
- Hugging Face
draft: false
translated_at: '2026-06-01T06:52:55.960399'
---

# 为文本生成推理引入多后端（TRT-LLM、vLLM）支持

## 引言

自2022年首次发布以来，文本生成推理（TGI）为Hugging Face和AI社区提供了一个以性能为核心的解决方案，用于轻松部署大语言模型（LLMs）。TGI最初提供了一种几乎无需编码的解决方案，可以从Hugging Face Hub加载模型并在NVIDIA GPU上投入生产部署。随着时间的推移，支持范围已扩展到包括AMD Instinct GPU、Intel GPU、AWS Trainium/Inferentia、Google TPU和Intel Gaudi。多年来，多种推理解决方案相继出现，包括vLLM、SGLang、llama.cpp、TensorRT-LLM等，使得整个生态系统趋于分散。不同的模型、硬件和使用场景可能需要特定的后端来实现最佳性能。然而，对于用户来说，正确配置每个后端、管理许可证并将其集成到现有基础设施中可能颇具挑战。

为了解决这一问题，我们很高兴推出TGI后端的概念。这种新架构提供了灵活性，可以通过TGI作为统一的单一前端层与上述任何解决方案集成。这一变化使社区能够更轻松地为其生产工作负载获得最佳性能，根据其模型、硬件和性能需求切换后端。

Hugging Face团队很高兴能够与构建vLLM、llama.cpp、TensorRT-LLM的团队以及AWS、Google、NVIDIA、AMD和Intel的团队合作并做出贡献，为TGI用户提供稳健且一致的体验，无论他们使用哪种后端和硬件。

![TGI多后端架构图](/images/posts/cd0e2239c70f.png)

## TGI后端：底层机制

TGI由多个组件构成，主要使用Rust和Python编写。Rust驱动HTTP和调度层，而Python仍然是建模的首选语言。

简而言之：Rust使我们能够通过静态分析和基于编译器的内存安全增强来提高服务层的整体稳健性：它能够在保持相同安全保证的前提下，更轻松地扩展到多核。利用Rust强大的类型系统来处理HTTP层和调度器，可以在最大化并发的同时避免内存问题，绕过基于Python环境中的全局解释器锁（GIL）。

说到Rust……惊喜的是，这正是TGI集成新后端的起点 - 🤗

今年早些时候，TGI团队致力于暴露基础控制点，以解耦实际HTTP服务器和调度器之间的耦合方式。这项工作引入了新的Rust `trait Backend`接口，用于连接当前的推理引擎以及未来的推理引擎。

拥有这个新的`Backend`接口（用Rust术语来说就是trait）为模块化铺平了道路，并使得将传入请求路由到不同的建模和执行引擎成为可能。

## 展望未来：2025年

TGI全新的多后端能力开辟了许多具有影响力的路线图机会。展望2025年，我们很高兴分享一些最令我们期待的TGI开发成果：

- **NVIDIA TensorRT-LLM后端**：我们正在与NVIDIA TensorRT-LLM团队合作，将优化的NVIDIA GPU + TensorRT性能带给社区。这项工作将在即将发布的博客文章中进行更详细的介绍。它与我们的使命密切相关，即通过开源提供`optimum-nvidia`（量化/构建/评估TensorRT兼容工件）以及TGI+TRT-LLM，使AI构建者能够轻松地在NVIDIA GPU上部署、执行和扩展部署。
- **Llama.cpp后端**：我们正在与llama.cpp团队合作，扩展对服务器生产用例的支持。TGI的llama.cpp后端将为任何希望在Intel、AMD或ARM CPU服务器上部署的用户提供强大的基于CPU的选项。
- **vLLM后端**：我们正在为vLLM项目做出贡献，并计划在2025年第一季度将vLLM作为TGI后端集成。
- **AWS Neuron后端**：我们正在与AWS的Neuron团队合作，在TGI中原生支持Inferentia 2和Trainium 2。
- **Google TPU后端**：我们正在与Google Jetstream和TPU团队合作，通过TGI提供最佳性能。

我们相信TGI后端将有助于简化LLMs的部署，为所有TGI用户带来多功能性和高性能。您很快就能在推理端点中直接使用TGI后端。客户将能够轻松地在各种硬件上使用TGI后端部署模型，开箱即用地获得顶级性能和可靠性。

敬请期待下一篇博客文章，我们将深入探讨即将推出的后端的技术细节和性能基准测试！

---

> 本文由AI自动翻译，原文链接：[Introducing multi-backends (TRT-LLM, vLLM) support for Text Generation Inference](https://huggingface.co/blog/tgi-multi-backend)
> 
> 翻译时间：2026-06-01 06:52
