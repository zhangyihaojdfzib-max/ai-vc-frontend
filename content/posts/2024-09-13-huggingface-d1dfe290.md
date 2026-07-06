---
title: Accelerate 1.0.0：迈向大规模训练新纪元
title_original: Accelerate 1.0.0
date: '2024-09-13'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/accelerate-v1
author: ''
summary: Accelerate 1.0.0 候选版发布，标志着该库从简化多GPU/TPU训练的轻量框架，发展为支持六种硬件加速器、大模型推理与PEFT训练的多功能工具。文章回顾了其成为Hugging
  Face生态基础的原因，并展望未来将集成FP8训练、DeepSpeed多模型编排、torch.compile及torchao等新技术，以应对大规模模型训练与推理的挑战。
categories:
- AI基础设施
tags:
- Accelerate
- 分布式训练
- PyTorch
- 大模型推理
- FP8训练
draft: false
translated_at: '2026-07-06T06:50:12.579883'
---

# Accelerate 1.0.0

## 今天的 Accelerate 是什么？

3.5 年前，Accelerate 是一个简单的框架，旨在通过提供低层级抽象来简化原始 PyTorch 训练循环，从而让多 GPU 和 TPU 系统上的训练变得更加容易：

从那时起，Accelerate 已发展成为一个多方面的库，旨在解决在 4050 亿参数（Llama）成为新语言模型规模的时代，大规模训练和大模型面临的许多常见问题。这包括：

- 一个灵活的低层级训练 API，允许在六种不同的硬件加速器（CPU、GPU、TPU、XPU、NPU、MLU）上进行训练，同时保留 99% 的原始训练循环
- 一个易于使用的命令行界面，旨在跨不同硬件配置配置和运行脚本
- 大模型推理或 `device_map="auto"` 的发源地，不仅允许用户在 LLM 上使用多设备进行推理，现在还通过参数高效微调（PEFT）等技术帮助在小型计算资源上训练 LLM

这三个方面使 Accelerate 成为 Hugging Face 几乎所有包的基础，包括 transformers、diffusers、peft、trl 等！

由于该包已稳定近一年，我们很高兴地宣布，从今天起，我们已经发布了 Accelerate 1.0.0 的首个候选版本！

这篇博客将详细介绍：

1. 我们为什么决定发布 1.0？
2. Accelerate 的未来是什么，我们如何看待 PyTorch 的整体发展方向？
3. 发生了哪些重大变更和弃用，以及如何轻松迁移？

## 为什么是 1.0？

发布 1.0.0 的计划已经酝酿了一年多。API 大致已经达到了我们期望的水平，以 Accelerator 为核心，简化了大量配置并使其更具可扩展性。然而，我们知道在能够称 Accelerate 的“基础”为“功能完整”之前，还有一些缺失的部分：

- 集成 MS-AMP 和 TransformersEngine 的 FP8 支持（在此处和此处了解更多）
- 支持使用 DeepSpeed 时的多模型编排（实验性）
- 为大模型推理 API 提供 `torch.compile` 支持（需要 torch>=2.5）
- 集成 `torch.distributed.pipelining` 作为替代的分布式推理机制
- 集成 `torchdata.StatefulDataLoader` 作为替代的数据加载器机制

通过为 1.0 所做的更改，Accelerate 已准备好应对新的技术集成，同时保持面向用户的 API 稳定。

## Accelerate 的未来

既然 1.0 即将完成，我们可以专注于社区中出现的新技术，并寻找集成到 Accelerate 的路径，因为我们预见到 PyTorch 生态系统很快将发生一些根本性变化：

- 作为多模型 DeepSpeed 支持的一部分，我们发现虽然当前 DeepSpeed 的通用工作方式可能可行，但随着我们努力支持简单的包装来为任何多模型训练场景准备模型，最终可能需要对整体 API 进行一些重大更改。
- 随着 torchao 和 torchtitan 的兴起，它们暗示了 PyTorch 整体的未来。旨在提供对 FP8 训练更原生的支持、新的分布式分片 API 以及对新版本 FSDP（FSDPv2）的支持，我们预测 Accelerate 的许多内部机制和通用使用 API 将需要更改（希望不会太剧烈）以满足这些需求，因为这些框架逐渐变得更加稳定。
- 依托 torchao/FP8，许多新框架带来了不同的想法和实现，以解决如何使 FP8 训练工作并保持稳定（仅举几例：transformer_engine、torchao、MS-AMP、nanotron）。我们在 Accelerate 中的目标是将这些实现集中在一个地方，并提供简单的配置，让用户随意探索和测试每一种，旨在找出最终最稳定和最灵活的那些。这是一个快速加速（无意双关）的研究领域，尤其是随着 NVIDIA 的 FP4 训练支持即将到来，我们希望确保不仅能够支持这些方法中的每一种，还能为每一种提供可靠的基准测试，以展示它们与原生 BF16 训练相比的开箱即用表现（只需最少的调整）。

我们对 PyTorch 生态系统中分布式训练的未来感到无比兴奋，我们希望确保 Accelerate 始终伴随每一步，为这些新技术提供更低的入门门槛。通过这样做，我们希望社区能够继续共同实验和学习，因为我们正在寻找在更复杂的计算系统上训练和扩展更大模型的最佳方法。

## 如何试用

要试用 Accelerate 的首个候选版本，请使用以下方法之一：

- pip：

```bash
pip install --pre accelerate

```

- Docker：

```bash
docker pull huggingface/accelerate:gpu-release-1.0.0rc1

```

有效的发布标签有：

- gpu-release-1.0.0rc1
- cpu-release-1.0.0rc1
- gpu-fp8-transformerengine-release-1.0.0rc1
- gpu-deepspeed-release-1.0.0rc1

## 迁移帮助

以下是此版本中实施的所有弃用的完整详细信息：

- 向 `Accelerator()` 传递 `dispatch_batches`、`split_batches`、`even_batches` 和 `use_seedable_sampler` 现在应通过创建 `accelerate.utils.DataLoaderConfiguration()` 并将其传递给 `Accelerator()` 来处理（`Accelerator(dataloader_config=DataLoaderConfiguration(...))`）
- `Accelerator().use_fp16` 和 `AcceleratorState().use_fp16` 已被移除；应替换为检查 `accelerator.mixed_precision == "fp16"`
- `Accelerator().autocast()` 不再接受 `cache_enabled` 参数。相反，应使用 `AutocastKwargs()` 实例来处理此标志（以及其他标志），并将其传递给 `Accelerator`（`Accelerator(kwargs_handlers=[AutocastKwargs(cache_enabled=True)])`）
- `accelerate.utils.is_tpu_available` 应替换为 `accelerate.utils.is_torch_xla_available`
- `accelerate.utils.modeling.shard_checkpoint` 应替换为来自 `huggingface_hub` 库的 `split_torch_state_dict_into_shards`
- `accelerate.tqdm.tqdm()` 不再接受 `True/False` 作为第一个参数，而应将 `main_process_only` 作为命名参数传递
- `ACCELERATE_DISABLE_RICH` 不再是有效的环境变量，而应通过设置 `ACCELERATE_ENABLE_RICH=1` 手动启用 rich traceback
- FSDP 设置 `fsdp_backward_prefetch_policy` 已替换为 `fsdp_backward_prefetch`

## 结语

非常感谢您使用 Accelerate；看着一个小想法在过去几年中变成超过 1 亿次下载和近 30 万次日下载，这真是太棒了。

通过这个候选版本，我们希望给社区一个机会，在正式发布之前试用并迁移到 1.0。

请持续关注 github 和社交媒体以获取更多信息！

---

> 本文由AI自动翻译，原文链接：[Accelerate 1.0.0](https://huggingface.co/blog/accelerate-v1)
> 
> 翻译时间：2026-07-06 06:50
