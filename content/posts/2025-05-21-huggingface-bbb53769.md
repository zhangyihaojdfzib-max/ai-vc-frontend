---
title: 探索Diffusers中的量化后端：让大模型更易用
title_original: Exploring Quantization Backends in Diffusers
date: '2025-05-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/diffusers-quantization
author: ''
summary: 本文探讨了Hugging Face Diffusers库中多种量化后端（如bitsandbytes、GGUF、torchao、Quanto及原生FP8支持）的应用，旨在解决大型扩散模型（如Flux）内存占用高的问题。文章通过对比测试说明，量化技术能在显著减少内存消耗的同时，保持图像生成质量，使强大模型更易于部署和使用。重点分析了不同量化方法在Transformer和文本编码器上的效果与权衡。
categories:
- AI基础设施
tags:
- 模型量化
- Diffusers
- AI模型部署
- 内存优化
- 扩散模型
draft: false
translated_at: '2026-04-16T04:57:56.469299'
---

# 探索 Diffusers 中的量化后端

像 Flux（一种基于流的文生图生成模型）这样的大型扩散模型能够生成令人惊叹的图像，但其庞大的规模可能成为一个障碍，需要大量的内存和计算资源。量化提供了一个强大的解决方案，它能缩小这些模型，使其更易于使用，而不会显著牺牲性能。但核心问题始终是：你真的能看出最终图像的差异吗？

在我们深入探讨 Hugging Face Diffusers 中各种量化后端的技术细节之前，何不先测试一下你自己的感知能力？

## 找出量化模型

我们创建了一个测试环境，你可以提供一个提示词，然后我们会使用原始高精度模型（例如 BF16 精度的 Flux-dev）和几个量化版本（BnB 4-bit、BnB 8-bit）分别生成结果。生成的图像会展示给你，你的挑战就是识别哪些图像来自量化模型。

在此处或下方试试看！

通常，特别是对于 8 位量化，差异非常细微，不仔细检查可能无法察觉。更激进的量化（如 4 位或更低）可能更容易被注意到，但结果仍然可能很好，尤其是考虑到其带来的巨大内存节省。不过，NF4 通常能提供最佳的权衡。

现在，让我们深入探讨。

## Diffusers 中的量化后端

基于我们之前的文章《使用 Quanto 和 Diffusers 实现内存高效的扩散 Transformer》，本文将探讨直接集成到 Hugging Face Diffusers 中的多样化量化后端。我们将研究 bitsandbytes、GGUF、torchao、Quanto 以及原生 FP8 支持如何让大型且强大的模型更易于使用，并以 Flux 为例进行演示。

在深入探讨量化后端之前，我们先介绍一下我们将要量化的 FluxPipeline（使用 `black-forest-labs/FLUX.1-dev` 检查点）及其组件。以 BF16 精度加载完整的 `FLUX.1-dev` 模型大约需要 31.447 GB 内存。主要组件包括：

- **文本编码器（CLIP 和 T5）**：
    - **功能**：处理输入的文本提示词。FLUX-dev 使用 CLIP 进行初步理解，并使用更大的 T5 进行细致入微的理解和更好的文本渲染。
    - **内存占用**：T5 - 9.52 GB；CLIP - 246 MB（BF16 精度）
- **Transformer（主模型 - MMDiT）**：
    - **功能**：核心生成部分（多模态扩散 Transformer）。从文本嵌入在潜在空间中生成图像。
    - **内存占用**：23.8 GB（BF16 精度）
- **变分自编码器（VAE）**：
    - **功能**：在像素空间和潜在空间之间转换图像。将生成的潜在表示解码为基于像素的图像。
    - **内存占用**：168 MB（BF16 精度）
- **量化重点**：示例将主要关注 **transformer** 和 **text_encoder_2（T5）**，以实现最显著的内存节省。

```python
prompts = [
    "Baroque style, a lavish palace interior with ornate gilded ceilings, intricate tapestries, and dramatic lighting over a grand staircase.",
    "Futurist style, a dynamic spaceport with sleek silver starships docked at angular platforms, surrounded by distant planets and glowing energy lines.",
    "Noir style, a shadowy alleyway with flickering street lamps and a solitary trench-coated figure, framed by rain-soaked cobblestones and darkened storefronts.",
]
```

### bitsandbytes（BnB）

bitsandbytes 是一个流行且用户友好的库，用于 8 位和 4 位量化，广泛用于 LLM 和 QLoRA 微调。我们也可以将其用于基于 Transformer 的扩散和流模型。

所有基准测试均在 1x NVIDIA H100 80GB GPU 上进行

```python
import torch
from diffusers import FluxPipeline
from diffusers import BitsAndBytesConfig as DiffusersBitsAndBytesConfig
from diffusers.quantizers import PipelineQuantizationConfig
from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig

model_id = "black-forest-labs/FLUX.1-dev"

pipeline_quant_config = PipelineQuantizationConfig(
    quant_mapping={
        "transformer": DiffusersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
        "text_encoder_2": TransformersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
    }
)

pipe = FluxPipeline.from_pretrained(
    model_id,
    quantization_config=pipeline_quant_config,
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

prompt = "Baroque style, a lavish palace interior with ornate gilded ceilings, intricate tapestries, and dramatic lighting over a grand staircase."
pipe_kwargs = {
    "prompt": prompt,
    "height": 1024,
    "width": 1024,
    "guidance_scale": 3.5,
    "num_inference_steps": 50,
    "max_sequence_length": 512,
}


print(f"Pipeline memory usage: {torch.cuda.max_memory_reserved() / 1024**3:.3f} GB")

image = pipe(
    **pipe_kwargs, generator=torch.manual_seed(0),
).images[0]

print(f"Pipeline memory usage: {torch.cuda.max_memory_reserved() / 1024**3:.3f} GB")

image.save("flux-dev_bnb_4bit.png")
```

**注意**：当使用 `PipelineQuantizationConfig` 配合 `bitsandbytes` 时，你需要分别从 `diffusers` 导入 `DiffusersBitsAndBytesConfig` 和从 `transformers` 导入 `TransformersBitsAndBytesConfig`。这是因为这些组件源自不同的库。如果你希望设置更简单，无需管理这些不同的导入，可以使用另一种方法进行流水线级量化，这种方法的一个示例在 [Diffusers 文档关于流水线级量化的部分](https://huggingface.co/docs/diffusers/main/en/quantization/pipeline_quantization)。

更多信息请查看 [bitsandbytes 文档](https://huggingface.co/docs/bitsandbytes/en/index)。

### torchao

`torchao` 是一个 PyTorch 原生库，用于架构优化，提供量化、稀疏性和自定义数据类型，旨在与 `torch.compile` 和 FSDP 兼容。Diffusers 支持广泛的 `torchao` 特殊数据类型，从而实现对模型优化的精细控制。

```diff
@@
- from diffusers import BitsAndBytesConfig as DiffusersBitsAndBytesConfig
+ from diffusers import TorchAoConfig as DiffusersTorchAoConfig

- from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig
+ from transformers import TorchAoConfig as TransformersTorchAoConfig
@@
pipeline_quant_config = PipelineQuantizationConfig(
    quant_mapping={
-         "transformer": DiffusersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
-         "text_encoder_2": TransformersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
+         "transformer": DiffusersTorchAoConfig("int8_weight_only"),
+         "text_encoder_2": TransformersTorchAoConfig("int8_weight_only"),
    }
)
```

```diff
@@
- from diffusers import BitsAndBytesConfig as DiffusersBitsAndBytesConfig
+ from diffusers import TorchAoConfig as DiffusersTorchAoConfig

- from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig
+ from transformers import TorchAoConfig as TransformersTorchAoConfig
@@
pipeline_quant_config = PipelineQuantizationConfig(
    quant_mapping={
-         "transformer": DiffusersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
-         "text_encoder_2": TransformersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
+         "transformer": DiffusersTorchAoConfig("int4_weight_only"),
+         "text_encoder_2": TransformersTorchAoConfig("int4_weight_only"),
    }
)
```

pipe = FluxPipeline.from_pretrained(
    model_id,
    quantization_config=pipeline_quant_config,
    torch_dtype=torch.bfloat16,
+    device_map="balanced"
)
- pipe.to("cuda")

```

更多信息请查阅torchao文档。

### Quanto

Quanto是一个通过optimum库与Hugging Face生态系统集成的量化库。

```diff
@@
- from diffusers import BitsAndBytesConfig as DiffusersBitsAndBytesConfig
+ from diffusers import QuantoConfig as DiffusersQuantoConfig

- from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig
+ from transformers import QuantoConfig as TransformersQuantoConfig
@@
pipeline_quant_config = PipelineQuantizationConfig(
    quant_mapping={
-         "transformer": DiffusersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
-         "text_encoder_2": TransformersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
+         "transformer": DiffusersQuantoConfig(weights_dtype="int8"),
+         "text_encoder_2": TransformersQuantoConfig(weights_dtype="int8"),
    }
)

```

注意：在撰写本文时，要使用Quanto的float8支持，你需要安装`optimum-quanto<0.2.5`并直接使用quanto。我们将致力于修复此问题。

```python
import torch
from diffusers import AutoModel, FluxPipeline
from transformers import T5EncoderModel
from optimum.quanto import freeze, qfloat8, quantize

model_id = "black-forest-labs/FLUX.1-dev"

text_encoder_2 = T5EncoderModel.from_pretrained(
    model_id,
    subfolder="text_encoder_2",
    torch_dtype=torch.bfloat16,
)

quantize(text_encoder_2, weights=qfloat8)
freeze(text_encoder_2)

transformer = AutoModel.from_pretrained(
      model_id,
      subfolder="transformer",
      torch_dtype=torch.bfloat16,
)

quantize(transformer, weights=qfloat8)
freeze(transformer)

pipe = FluxPipeline.from_pretrained(
    model_id,
    transformer=transformer,
    text_encoder_2=text_encoder_2,
    torch_dtype=torch.bfloat16
).to("cuda")

```

更多信息请查阅Quanto文档。

GGUF是llama.cpp社区中流行的用于存储量化模型的文件格式。

```python
import torch
from diffusers import FluxPipeline, FluxTransformer2DModel, GGUFQuantizationConfig

model_id = "black-forest-labs/FLUX.1-dev"


ckpt_path = "https://huggingface.co/city96/FLUX.1-dev-gguf/resolve/main/flux1-dev-Q4_1.gguf"

transformer = FluxTransformer2DModel.from_single_file(
    ckpt_path,
    quantization_config=GGUFQuantizationConfig(compute_dtype=torch.bfloat16),
    torch_dtype=torch.bfloat16,
)

pipe = FluxPipeline.from_pretrained(
    model_id,
    transformer=transformer,
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")

```

更多信息请查阅GGUF文档。

### FP8逐层转换 (enable_layerwise_casting)

FP8逐层转换是一种内存优化技术。其工作原理是将模型权重以紧凑的FP8（8位浮点数）格式存储，这大约只使用标准FP16或BF16精度一半的内存。
就在某一层执行计算之前，其权重会动态转换为更高的计算精度（如FP16/BF16）。计算完成后，权重立即转换回FP8以进行高效存储。这种方法之所以有效，是因为核心计算保留了高精度，并且通常跳过对量化特别敏感的层（如归一化层）。此技术也可以与分组卸载结合使用以进一步节省内存。

```python
import torch
from diffusers import AutoModel, FluxPipeline

model_id = "black-forest-labs/FLUX.1-dev"

transformer = AutoModel.from_pretrained(
    model_id,
    subfolder="transformer",
    torch_dtype=torch.bfloat16
)
transformer.enable_layerwise_casting(storage_dtype=torch.float8_e4m3fn, compute_dtype=torch.bfloat16)

pipe = FluxPipeline.from_pretrained(model_id, transformer=transformer, torch_dtype=torch.bfloat16)
pipe.to("cuda")

```

更多信息请查阅逐层转换文档。

## 结合更多内存优化技术与torch.compile

大多数这些量化后端都可以与Diffusers提供的内存优化技术结合使用。让我们探讨一下CPU卸载、分组卸载和`torch.compile`。你可以在Diffusers文档中了解更多关于这些技术的信息。

注意：在撰写本文时，如果从源码安装bnb并使用pytorch nightly版本或设置`fullgraph=False`，bnb + `torch.compile`也可以工作。

```diff
import torch
from diffusers import FluxPipeline
from diffusers import BitsAndBytesConfig as DiffusersBitsAndBytesConfig
from diffusers.quantizers import PipelineQuantizationConfig
from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig

model_id = "black-forest-labs/FLUX.1-dev"

pipeline_quant_config = PipelineQuantizationConfig(
    quant_mapping={
        "transformer": DiffusersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
        "text_encoder_2": TransformersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16),
    }
)

pipe = FluxPipeline.from_pretrained(
    model_id,
    quantization_config=pipeline_quant_config,
    torch_dtype=torch.bfloat16
)
- pipe.to("cuda")
+ pipe.enable_model_cpu_offload()

```

模型CPU卸载 (enable_model_cpu_offload)：此方法在推理流程中，在CPU和GPU之间移动整个模型组件（如UNet、文本编码器或VAE）。它能显著节省VRAM，并且通常比更细粒度的卸载更快，因为它涉及更少、更大的数据传输。

bnb + enable_model_cpu_offload：

```diff
import torch
from diffusers import FluxPipeline, AutoModel

model_id = "black-forest-labs/FLUX.1-dev"

transformer = AutoModel.from_pretrained(
    model_id,
    subfolder="transformer",
    torch_dtype=torch.bfloat16,
    # device_map="cuda"
)
transformer.enable_layerwise_casting(storage_dtype=torch.float8_e4m3fn, compute_dtype=torch.bfloat16)
+ transformer.enable_group_offload(onload_device=torch.device("cuda"), offload_device=torch.device("cpu"), offload_type="leaf_level", use_stream=True)

pipe = FluxPipeline.from_pretrained(model_id, transformer=transformer, torch_dtype=torch.bfloat16)
- pipe.to("cuda")

```

分组卸载 (对于diffusers组件使用`enable_group_offload`，对于通用的`torch.nn.Module`使用`apply_group_offloading`)：它将模型内部层的组（如`torch.nn.ModuleList`或`torch.nn.Sequential`实例）移动到CPU。这种方法通常比完整模型卸载更节省内存，并且比顺序卸载更快。

FP8逐层转换 + 分组卸载：

```diff
import torch
from diffusers import FluxPipeline
from diffusers import TorchAoConfig as DiffusersTorchAoConfig
from diffusers.quantizers import PipelineQuantizationConfig
from transformers import TorchAoConfig as TransformersTorchAoConfig

from torchao.quantization import Float8WeightOnlyConfig

model_id = "black-forest-labs/FLUX.1-dev"
dtype = torch.bfloat16

pipeline_quant_config = PipelineQuantizationConfig(
    quant_mapping={
        "transformer":DiffusersTorchAoConfig("int4_weight_only"),
        "text_encoder_2": TransformersTorchAoConfig("int4_weight_only"),
    }
)

pipe = FluxPipeline.from_pretrained(
    model_id,
    quantization_config=pipeline_quant_config,
    torch_dtype=torch.bfloat16,
    device_map="balanced"
)

+ pipe.transformer = torch.compile(pipe.transformer, mode="max-autotune", fullgraph=True)

```

注意：`torch.compile`可能会引入细微的数值差异，导致图像输出发生变化。

torch.compile：另一种补充方法是通过 PyTorch 2.x 的 torch.compile() 功能加速模型执行。编译模型不会直接降低内存占用，但能显著提升推理速度。PyTorch 2.0 的编译功能（Torch Dynamo）通过提前追踪和优化模型图来实现。

torchao + torch.compile：

在此处查看一些基准测试结果：

## 开箱即用的量化模型检查点

您可以在我们的 Hugging Face 合集（[链接](link to collection)）中找到这篇博客文章中提到的 bitsandbytes 和 torchao 量化模型。

## 结论

以下是选择量化后端的快速指南：

- **追求最简便的内存节省（NVIDIA）**：从 bitsandbytes 4/8 位量化开始。这也可以与 torch.compile() 结合使用以获得更快的推理速度。
- **优先考虑推理速度**：torchao、GGUF 和 bitsandbytes 都可以与 torch.compile() 结合使用，以潜在地提升推理速度。
- **追求硬件灵活性（CPU/MPS）和 FP8 精度**：Quanto 是一个不错的选择。
- **追求简便性（Hopper/Ada 架构）**：探索 FP8 逐层转换（enable_layerwise_casting）。
- **需要使用现有的 GGUF 模型**：使用 GGUF 加载方式（from_single_file）。
- **对量化训练感兴趣？** 请关注后续关于该主题的博客文章！更新（2025年6月19日）：文章已发布[此处](here)！

量化显著降低了使用大型扩散模型的门槛。尝试这些后端，为您的需求找到内存、速度和质量的最佳平衡点。

致谢：感谢 Chunte 为本文提供缩略图。

---

> 本文由AI自动翻译，原文链接：[Exploring Quantization Backends in Diffusers](https://huggingface.co/blog/diffusers-quantization)
> 
> 翻译时间：2026-04-16 04:57
