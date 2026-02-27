---
title: Transformer混合专家模型（MoEs）：原理、优势与生态支持
title_original: Mixture of Experts (MoEs) in Transformers
date: '2026-02-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/moe-transformers
author: ''
summary: 本文介绍了混合专家模型（MoEs）在Transformer架构中的应用。MoEs通过用一组可学习的专家网络替换部分稠密前馈层，并引入路由器为每个Token动态选择少量专家，实现了模型总参数容量与推理激活参数量的解耦。这种稀疏架构能显著提升计算效率、降低推理延迟，并支持天然的专家并行化。文章还概述了transformers库为支持MoE所做的工程改进，包括权重加载重构、专家后端和并行化等，以应对稀疏模型对传统稠密模型工具链的挑战。
categories:
- AI研究
tags:
- 混合专家模型
- Transformer
- 大语言模型
- 稀疏计算
- 模型推理
draft: false
translated_at: '2026-02-27T04:38:38.505448'
---

# Transformer中的混合专家模型（MoEs）

## 引言

过去几年，扩展稠密语言模型一直是推动LLM（大语言模型）发展的主要动力。从早期的原始ULMFiT（约3000万参数）或GPT-2（15亿参数，当时被认为"过于危险而不宜发布"🧌）等模型，到如今的数千亿参数系统，其方法很简单：

更多数据 + 更多参数 = 更好的性能。

扩展定律强化了这一趋势，但稠密扩展存在实际限制：

- 训练成本越来越高。
- 推理延迟增加。
- 部署需要大量内存和硬件。

这正是混合专家模型（MoEs）发挥作用的地方。

如果您已经熟悉MoEs并想直接了解transformers中完成的工程工作，可以直接跳转到[Transformers与MoEs](#transformers-and-moes)部分。

## 从稠密到稀疏：什么是MoEs？

混合专家模型保留了Transformer主干结构，但用一组**专家**替换了某些稠密前馈层。"专家"并非主题专用模块（例如"数学专家"、"代码专家"），它只是一个可学习的子网络。对于每个Token，**路由器**会选择一小部分专家来处理它。

![MoE路由示意图](/images/posts/fadb5b3bc3ec.png)

不同的Token会根据其隐藏表示激活不同的专家。

模型容量取决于总参数数量，但推理速度取决于激活参数数量。

这是核心思想。

例如，以`gpt-oss-20b`为例。它总共有210亿参数，但每个Token只使用4个激活专家（总共32个专家）。考虑到共享组件加上激活专家，该模型每个Token使用约36亿激活参数。在内存带宽约为800 GB的M3 Ultra Mac上运行此模型，我们可以估算生成速度约为`800 / (3.6 * 2)`（使用bfloat16，每个参数占2字节）。这得出约**每秒111个Token**。我们实际获得的性能数据约为**115 tok/s**，与粗略估算非常接近。

这种超快速度证实了该模型的工作方式近似于一个36亿参数的模型，但它具有与210亿参数模型相同的容量（或质量）。

（注：如果我们使用模型原生mxfp4量化的内核，速度会更快）。

MoEs因以下原因具有吸引力：

1. **更好的计算效率**  
   在固定的训练FLOP预算下，MoEs通常优于稠密模型。  
   ![MoE与稠密训练对比图](/images/posts/581d3e0f58d9.png)  
   这意味着更快的迭代和更好的扩展效率。

2. **天然的并行化维度**  
   专家在计算图中提供了结构边界。由于不同Token涉及不同专家，我们可以跨专家并行化（稍后在**专家并行**部分讨论）。

3. **行业采用**  
   过去几周发布的主要开源MoE模型包括Qwen 3.5、MiniMax M2、GLM-5或Kimi K2.5。  
   这一趋势在2025年1月DeepSeek R1取得成功后加速，建立在DeepSeek V2等早期系统之上。另一个早期MoE是2023年12月发布的Mixtral-8x7B。  
   ![transformers包中MoE模型添加的2年时间线](/images/posts/11858ed58cdb.png)  
   闭源实验室也使用MoEs。ChatGPT长期以来一直传闻使用稀疏架构，而开源`gpt-oss`模型确实如此。

如果您想更全面地了解MoEs，我们强烈建议阅读[这篇博客](this blog)并观看我们最近关于路由的[YouTube视频](YouTube video on routing)。

## Transformers与MoEs

生态系统中的大多数工具，包括模型加载、设备放置、量化和后端执行，最初都是为**稠密**模型设计的。MoEs对这些假设提出了挑战。

使MoEs成为`transformers`中的**一等公民**意味着重新设计加载流水线、执行模型和分布式抽象的部分内容，而不仅仅是添加新的模型类。我们将重点介绍`transformers`库如何演进以支持稀疏架构，涵盖：

- 权重加载重构
- 专家后端
- 专家并行
- 使用transformers训练MoEs

## 权重加载重构

`AutoModelForCausalLM.from_pretrained("model_id")`会下载模型权重并加载到PyTorch模型中。对于稠密模型，加载相对简单，检查点中的每个张量与运行时模块中的参数一一对应。

对于MoEs，情况更复杂。在大多数MoE检查点中，每个专家都是独立序列化的。如果您查看DeepSeek-V3检查点索引内部，会看到类似这样的键：

```bash
model.layers.3.mlp.experts.0.gate_proj.weight
...
model.layers.3.mlp.experts.255.gate_proj.weight
```

每个专家都有自己的一组权重矩阵，本质上是256个（以DeepSeek-V3为例，总共0到255）小型前馈网络并排保存。然而在运行时，GPU执行的是优化内核。现代MoE内核（如分组GEMM和融合MoE实现）旨在**在单个操作中处理所有专家**，而不是逐个循环处理。

为了高效实现这一点，它们要求专家权重被打包成**单个连续张量**。

因此我们存在不匹配：

- 检查点：**256个独立张量**
- 运行时：**1个打包张量**

系统性地弥合这一差距正是**权重加载重构**所实现的。

通过引入**通用WeightConverter**，思维模式从：

> 检查点已经匹配我的运行时布局；加载主要是逐个键的复制。

转变为：

> 检查点只是张量的序列化来源。加载是一个**转换流水线**，将它们转换为我们想要的运行时布局。

### 使用WeightConverter进行动态权重加载

此次重构引入的核心抽象是通过`WeightConverter`实现的**动态权重加载**。

`WeightConverter`让我们可以定义：

```
源键模式 → 目标键 + 操作
```

基本操作（分块、连接等）是可组合的。其中两个对MoEs特别有用：

- `MergeModulelist`将张量列表合并为单个张量。例如，您可以将`MergeModulelist`与`Concatenate`组合，以堆叠MoE中的专家并将它们打包成一个张量。
  ```python
  WeightConverter(
      ["block_sparse_moe.experts.*.w1.weight","block_sparse_moe.experts.*.w3.weight",],
      "mlp.experts.gate_up_proj",
      operations=[
          MergeModulelist(dim=0),
          Concatenate(dim=1),
      ],
  )
  ```
- `SplitModulelist`将张量分割回张量列表。例如，您可以将专家堆叠分割回单个专家。
  ```python
  WeightConverter("mlp.experts.down_proj","block_sparse_moe.experts.*.w2.weight",
      operations=[SplitModulelist(dim=0)],
  )
  ```

```python
WeightConverter(
    ["block_sparse_moe.experts.*.w1.weight", "block_sparse_moe.experts.*.w3.weight",],
    "mlp.experts.gate_up_proj",
    operations=[
        MergeModulelist(dim=0),
        Concatenate(dim=1),
    ],
)

```

SplitModulelist 将一个张量分割回一个张量列表。例如，您可以将一组专家分割回独立的专家。

```python
WeightConverter(
    "mlp.experts.down_proj",
    "block_sparse_moe.experts.*.w2.weight",
    operations=[SplitModulelist(dim=0)],
)

```

### 张量的惰性物化

这次重构不仅改进了*存在哪些*转换，还改进了它们*如何*被调度。

加载器扫描一次检查点键，将它们与转换器模式匹配，并按转换器对张量进行分组。一旦某个键被识别为需要，它就会被注册为一个*未来*并通过线程池进行物化。转换操作仅在其依赖项准备就绪后才运行。例如，`MergeModulelist` 会等待直到某一层的所有专家都被加载。

这避免了重复扫描并减少了内存峰值。

### 基准测试：权重加载管道的改进

为了评估新权重加载管道带来的改进，我们对 `transformers` 的 v4 与 v5 版本进行了基准测试。重点是大型 MoE 模型的加载速度，这通常是训练和推理中的瓶颈。

我们使用以下分支对 v4 和 v5 进行了基准测试：

- v4 分支：https://github.com/ariG23498/transformers/tree/bench-v4
- v5 分支：https://github.com/ariG23498/transformers/tree/bench-v5

示例：

```python
from transformers import AutoModelForCausalLM

model_id = "Qwen/Qwen1.5-110B-Chat"
model = AutoModelForCausalLM.from_pretrained(model_id)

```

两个相关的环境变量：

- `HF_ENABLE_PARALLEL_LOADING`：通过线程启用并行分片加载。
- `HF_DEACTIVATE_ASYNC_LOAD`：禁用新的异步管道（v5 的逃生舱口）。

`HF_ENABLE_PARALLEL_LOADING`：通过线程启用并行分片加载。

`HF_DEACTIVATE_ASYNC_LOAD`：禁用新的异步管道（v5 的逃生舱口）。

### 结果

模型：`Qwen/Qwen1.5-110B-Chat` GPU：1× A100 (80GB)

![加载基准测试](/images/posts/313117072c13.png)

速度提升不仅仅是“更多线程”。

它是*单次路由*、*异步物化*和*转换感知调度*的结合，共同避免了不必要的物化和内存峰值，同时支持在加载时进行专家打包和投影融合。

### 量化如何融入

通过这次重构，我们现在可以先创建运行时模块结构，然后将权重转换到该结构中。我们现在可以选择性地在转换管道中附加量化，使量化成为权重加载管道本身的一部分。这至关重要，因为只有在专家以可预测的打包布局存在后，“按专家”量化才有意义。

这种端到端的管道以前是不可能的，现在它作为一个公开的 API 提供给用户。

## 专家后端

一旦专家被打包到单个运行时张量中，另一个问题就出现了：

如何实际高效地通过它们进行路由？

在专家混合模型中，每个 Token 被路由到不同的专家。这意味着运行时必须将 Token 分派到它们选定的专家权重，高效地执行投影，应用路由权重，然后收集并重新排序结果。

这正是*专家后端系统*（在 PR #42697 中引入）所要解决的问题。专家后端引入了一个*可插拔的执行架构*，将专家计算与模型实现解耦。系统允许专家层在运行时动态选择后端，而不是在每个 MoE 模型内部硬编码一种分派策略。

这是通过装饰器模式实现的：

```python
@use_experts_implementation

```

该装饰器包装专家类，并自动将计算分派到选定的后端。

目前提供了三个后端：

1.  `eager`：循环遍历选定的专家并对每个专家应用投影。这用于正确性参考和调试。
2.  `batched_mm`：使用 `torch.bmm` API。这会为每个 Token 复制选定的专家权重，并执行一次批处理 GEMM。该后端非常适合内存充足、小批量、GPU 密集型的工作负载。
3.  `grouped_mm`：使用 `torch._grouped_mm` API。在这里，我们按专家 ID 对 Token 进行排序、分组，然后执行一次分组 GEMM。该后端在处理大批量或内存受限的设置时表现出色。

`eager`：循环遍历选定的专家并对每个专家应用投影。这用于正确性参考和调试。

`batched_mm`：使用 `torch.bmm` API。这会为每个 Token 复制选定的专家权重，并执行一次批处理 GEMM。该后端非常适合内存充足、小批量、GPU 密集型的工作负载。

`grouped_mm`：使用 `torch._grouped_mm` API。在这里，我们按专家 ID 对 Token 进行排序、分组，然后执行一次分组 GEMM。该后端在处理大批量或内存受限的设置时表现出色。

![](/images/posts/a4661c2e1e68.png)

## 专家并行

专家混合模型可能拥有数千亿参数（远超单个 GPU 的容量）。专家并行通过将专家分布在多个设备上来解决这个问题。每个设备仅加载分配给它的专家子集，为这些专家进行计算，然后参与结果聚合。这种方法可以将模型扩展到更大的参数数量，而不会增加计算成本，因为每个 Token 只激活少数几个专家。

通过 `enable_expert_parallel` 启用专家并行：

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.distributed.configuration_utils import DistributedConfig

distributed_config = DistributedConfig(enable_expert_parallel=True)

model = AutoModelForCausalLM.from_pretrained(
    "openai/gpt-oss-120b",
    dtype="auto",
    distributed_config=distributed_config,
)

```

使用以下命令启动：

```bash
torchrun --nproc-per-node N script.py

```

其中 `N` 能整除专家总数，并且可能匹配您节点中的 GPU 数量。

当 `enable_expert_parallel=True` 时，模型从标准张量并行计划切换到具有专门分片策略的专家并行计划。

EP 的核心组件在于：

1.  `GroupedGemmParallel`：这沿着专家维度（dim=0）分割专家权重。这里每个设备只加载 `num_experts / num_devices`。
2.  `RouterParallel`：这将全局专家索引重新映射到本地索引，屏蔽掉未分配给当前等级的专家，确保每个设备仅使用其本地专家进行计算，并使用 all-reduce 来跨设备组合部分输出。

`GroupedGemmParallel`：这沿着专家维度（dim=0）分割专家权重。这里每个设备只加载 `num_experts / num_devices`。

`RouterParallel`：这将全局专家索引重新映射到本地索引，屏蔽掉未分配给当前等级的专家，确保每个设备仅使用其本地专家进行计算，并使用 all-reduce 来跨设备组合部分输出。

## 使用 Transformers 训练 MoE

MoE 非常适合扩展推理，但训练它们要复杂得多。

MoE 拥有*海量*的参数数量，分布式专家通信复杂，存在需要处理的路由不稳定性。为了解决这个问题，我们与 *Unsloth* 合作，以实现显著更快的专家混合训练：

- MoE 训练速度提升约 12 倍
- VRAM 减少超过 35%
- 上下文长度延长约 6 倍
- 与 v4 相比，整体速度提升 12–30 倍

我们利用专家后端抽象，围绕 PyTorch 的 `torch._grouped_mm` API 进行标准化，并使用自定义的 Triton 分组 GEMM + LoRA 内核。Unsloth 建立在 Transformers（和 TRL）优化的基础上，以进一步提升性能。

有关完整详情，我们建议阅读：*Unsloth 官方指南*

## 结论

随着稀疏架构的持续演进，我们希望transformers库能与之共同发展。如果您正在基于MoE进行构建，或尝试新的稀疏架构思路，我们非常期待您的反馈。请告诉我们您希望接下来在transformers中看到哪些抽象层、内核或工作流程。

---

> 本文由AI自动翻译，原文链接：[Mixture of Experts (MoEs) in Transformers](https://huggingface.co/blog/moe-transformers)
> 
> 翻译时间：2026-02-27 04:38
