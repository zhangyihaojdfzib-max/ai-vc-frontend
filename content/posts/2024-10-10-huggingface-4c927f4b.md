---
title: AMD第五代EPYC CPU发布：性能翻倍
title_original: Introducing the AMD 5th Gen EPYC™ CPU
date: '2024-10-10'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/huggingface-amd-turin
author: ''
summary: AMD发布了基于Zen5架构的第五代EPYC CPU（代号Turin），最高支持192核384线程。文章展示了Turin与上一代Genoa在AI推理任务上的性能对比，使用PyTorch
  ZenDNN插件和bfloat16数据类型，在Meta LLaMA 3.1 8B模型上实现了约2倍的吞吐量提升。文章还介绍了与Hugging Face生态系统的合作，以及通过zentorch插件利用torch.compile加速工作负载的方法。
categories:
- AI基础设施
tags:
- AMD
- EPYC
- Zen5
- AI推理
- PyTorch
draft: false
translated_at: '2026-06-19T07:07:19.651104'
---

# 介绍 AMD 第五代 EPYC™ CPU

AMD 刚刚发布了基于 Zen5 架构的第五代服务器级 EPYC CPU——也被称为 Turin。它在性能上带来了显著提升，核心数最高可达 192 个和 384 个线程。

从大语言模型到 RAG（检索增强生成）场景，Hugging Face 用户可以利用这一代新服务器来增强其性能表现：

1. 降低部署的目标延迟。
2. 提高最大吞吐量。
3. 降低运营成本。

在过去几周里，我们一直与 AMD 合作，验证 Hugging Face 生态系统在这代新 CPU 上得到全面支持，并在不同任务中提供预期的性能。

此外，我们还在开发一些令人兴奋的新方法，通过使用 AMD ZenDNN PyTorch 插件（zentorch）在 AMD CPU 上利用 `torch.compile`，以进一步加速我们将在后面讨论的工作负载。

虽然我们能够提前获得这项工作来测试 Hugging Face 模型和库，并与您分享性能表现，但我们预计 AMD 很快就会将其提供给社区——敬请期待！

## AMD Turin 与 AMD Genoa 性能对比——2 倍加速

在本节中，我们展示了两款 AMD EPYC CPU：Turin（128 核）和 Genoa（96 核）的基准测试结果。在这些基准测试中，我们使用了 PyTorch 的 ZenDNN 插件（zentorch），该插件为 AMD EPYC CPU 上的深度学习工作负载提供了针对性的推理优化。该插件与 `torch.compile` 图编译流程无缝集成，能够在 `torch.fx` 图上执行多轮图级优化，从而实现进一步的性能加速。

为确保最佳性能，我们使用了 `bfloat16` 数据类型和 ZenDNN 5.0。我们配置了多实例设置，使多个 Meta LLaMA 3.1 8B 模型实例能够跨所有核心并行执行。每个模型实例在每个插槽上分配 32 个物理核心，使我们能够充分利用服务器的全部处理能力，实现高效的数据处理和计算速度。

我们使用两种不同的批次大小——16 和 32——在五个不同的用例中运行了基准测试：

- 摘要（1024 个输入 Token / 128 个输出 Token）
- 聊天机器人（128 个输入 Token / 128 个输出 Token）
- 翻译（1024 个输入 Token / 1024 个输出 Token）
- 论文写作（128 个输入 Token / 1024 个输出 Token）
- 实时字幕（16 个输入 Token / 16 个输出 Token）

这些配置不仅有助于全面分析每台服务器在不同工作负载下的表现，还能模拟大语言模型的实际应用场景。具体来说，我们绘制了每个用例的解码吞吐量（排除第一个 Token），以展示性能差异。

### Llama 3.1 8B Instruct 的结果

![Turin 与 Genoa 对比](/images/posts/16ae1b0d8e4c.png)

Meta Llama 3.1 8B 的吞吐量结果，对比 AMD Turin 与 AMD Genoa。AMD Turin 始终优于 AMD Genoa CPU，在大多数配置下实现了约 2 倍的吞吐量提升。

## 结论

如上所示，与上一代 AMD Genoa 相比，AMD EPYC Turin CPU 在 AI 用例中提供了显著的性能提升。为提高可复现性并简化基准测试流程，我们使用了 `optimum-benchmark`，它提供了一个统一的框架，可在各种设置下进行高效基准测试。这使我们能够通过使用 `zentorch` 后端进行 `torch.compile` 来有效进行基准测试。

此外，我们还开发了一个优化的 Dockerfile，该文件将与基准测试代码一起很快发布。这将有助于轻松部署和复现我们的结果，确保其他人能够有效利用我们的发现。

您可以在 AMD Zen 深度神经网络（ZenDNN）中找到更多信息。

## 实用资源

- ZenTF：https://github.com/amd/ZenDNN-tensorflow-plugin
- ZenTorch：https://github.com/amd/ZenDNN-pytorch-plugin
- ZenDNN ONNXRuntime：https://github.com/amd/ZenDNN-onnxruntime

---

> 本文由AI自动翻译，原文链接：[Introducing the AMD 5th Gen EPYC™ CPU](https://huggingface.co/blog/huggingface-amd-turin)
> 
> 翻译时间：2026-06-19 07:07
