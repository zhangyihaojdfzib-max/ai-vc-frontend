---
title: vLLM Transformer后端实现原生速度
title_original: Native-speed vLLM transformers modeling backend
date: '2026-07-08'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/native-speed-vllm-transformers-backend
author: ''
summary: 文章介绍了vLLM Transformer建模后端的最新进展，使其推理速度与vLLM自定义实现相当甚至更快。通过torch.fx静态分析和ast源代码重写，该后端在运行时自动应用推理层融合，无需模型作者手动移植。在Qwen3系列模型上的基准测试显示，从4B密集模型到235B混合专家模型，性能均显著提升。用户只需添加--model-impl
  transformers标志即可享受超快推理，兼容现有并行配置。
categories:
- AI基础设施
tags:
- vLLM
- Transformer
- 推理优化
- 模型部署
- 开源
draft: false
translated_at: '2026-07-11T05:26:27.004070'
---

# 原生速度 vLLM Transformer 建模后端

TL;DR：对于许多 LLM 架构，Transformer vLLM 后端现在与自定义 vLLM 实现速度相当（甚至更快）。模型作者可以自动利用其 Transformer 实现，免费获得超快 vLLM 推理。

```bash

uv pip install --upgrade vllm --torch-backend auto

```

Transformer 库已成为机器学习的参考建模库。它通过一致的 API 支持 450 多种架构，其设计主要目标是模型实现自包含且易于理解。阅读 Transformer 代码有助于贡献者轻松了解架构的工作原理，然后将其移植到其他框架，如 vLLM、SGLang、MLX、llama.cpp 等。

我们已完全接受这一生态角色，并投入大量精力使其更加便捷。去年将 Transformer 作为 vLLM 中的建模后端集成，是朝着这一方向迈出的一大步。这使得模型作者能够在 vLLM 内部运行 Transformer 模型（包括 LLM 和 VLM），而无需进行任何移植。Transformer 提供建模代码，vLLM 提供高度优化的推理技术，如连续批处理和自定义注意力核。

现在，这一集成变得更好 🚀！

## 展示

我们将 vLLM 的 Transformer 建模后端与 vLLM 手写原生实现，在三种截然不同的 Qwen3 模型上进行了正面比较：

- 单 GPU 上的 4B 密集模型
- 张量并行上的 32B 密集模型
- 同一 8×H100 节点上数据并行 + 专家并行的 235B 参数 FP8 混合专家模型

![PR 前后 Transformer vLLM 后端的基准测试](/images/posts/e1161e17d417.png)

通过 Transformer 建模后端运行任何* Hugging Face 模型只需一个标志——`--model-impl transformers`。它与常规并行选项兼容，因此您的服务设置无需更改：

```bash

vllm serve Qwen/Qwen3-4B --model-impl transformers


vllm serve Qwen/Qwen3-32B --model-impl transformers --tensor-parallel-size 2


vllm serve Qwen/Qwen3-235B-A22B-FP8 --model-impl transformers --data-parallel-size 8 --enable-expert-parallel


```

*使用线性注意力的模型目前暂不支持，但很快会支持！代码位于 Hub 仓库中的自定义模型可能无法运行，因为它们可能未按合规方式编写。

### 我们的测量方式

每个模型在三种条件下进行比较，除代码路径外其他方面完全相同：

1. native——`--model-impl vllm`，vLLM 手写模型（待匹配的基准）
2. after——`--model-impl transformers`，包含该 PR
3. before——`--model-impl transformers`，不包含该 PR

完整且可复现的运行脚本以 gist 形式提供：`benchmark.sh`

## 那么，新功能是什么？

vLLM 的 Transformer 建模后端过去主要关注注意力机制作为推理瓶颈。通过在运行时接入 vLLM 的注意力实现，我们可以使 Transformer 模型在 vLLM 引擎内高效运行。但部署涉及多个维度，只有自定义移植才能针对性地提取最大推理性能。跨 GPU 并行化、编译、融合核等，都有助于利用硬件实现超快推理。

![新模型集成到 Transformer 和 vLLM](/images/posts/c2ef3f15e7f9.png)

当模型作者追求绝对最佳性能时，他们仍需编写自定义 vLLM 实现。

![新模型集成到 Transformer，并立即可用于 vLLM](/images/posts/2bc7b766d4c8.png)

vLLM Transformer 建模后端的最新迭代，在运行时动态应用推理特定的层融合，以匹配自定义代码实现的速度，适用于兼容架构。

## 它是如何工作的？

vLLM 的 Transformer 建模后端现在使用 `torch.fx` 对模型图进行静态分析。此过程搜索可优化的已知模式。识别出任何模式后，使用 `ast`（抽象语法树）操作源代码并就地重写部分操作。

我们可以通过此实现什么？

- 融合操作，多对一映射到（超）优化的 vLLM 核，例如混合专家（MoE）模型中用于专家并行化（EP）的核。
- 其他主要的融合操作是 vLLM 的 `MergedColumnParallelLinear` 和 `QKVParallelLinear`。这些模块使我们能够推断 TP（张量并行）的并行方案。如果解码器块列表易于识别，也可以推断 PP（流水线并行）方案。
- 操作后的模型仍然完全可（torch）编译，通过 `torch.compile` 和 CUDA Graphs，与专用 vLLM 模型实现完全相同。
- 与 vLLM 模型实现不同，Transformer 模型实现可用于训练。因此，您可以使用相同的模型代码进行训练/评估/RL  rollout。

如上所示，这为兼容模型带来了原生 vLLM 推理速度，而无需编写一行代码来优化推理模型。

我们正在撰写一篇详细的博客文章，深入探讨这些优化的推理方法，并详细解释我们如何操作模型以适应这些方法。

## 资源

- Transformer 模型定义
- vLLM 中的 Transformer 建模后端
- 大规模服务
- Torch FX
- 抽象语法树

---

> 本文由AI自动翻译，原文链接：[Native-speed vLLM transformers modeling backend](https://huggingface.co/blog/native-speed-vllm-transformers-backend)
> 
> 翻译时间：2026-07-11 05:26
