---
title: 英特尔推出AutoRound：面向大模型的先进量化工具
title_original: 'Introducing AutoRound: Intel’s Advanced Quantization for LLMs and
  VLMs'
date: '2025-04-29'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/autoround
author: ''
summary: 英特尔发布AutoRound，一种先进的训练后量化方法，专为大型语言模型和视觉语言模型设计。该方法通过带符号梯度下降联合优化权重舍入和裁剪范围，能在低比特（如INT2-INT8）量化下实现卓越的准确性，尤其在INT2精度下表现远超主流基线。AutoRound兼容广泛的模型架构和设备，支持多种量化配置和导出格式，且量化过程快速高效，在A100
  GPU上量化720亿参数模型仅需37分钟。
categories:
- AI基础设施
tags:
- 模型量化
- 英特尔
- 大语言模型
- 推理优化
- AutoRound
draft: false
translated_at: '2026-04-22T04:57:38.761186'
---

# 什么是 AutoRound？

随着大语言模型（LLM）和视觉语言模型（VLM）的规模和复杂性持续增长，高效部署它们变得日益具有挑战性。量化通过减小模型大小和降低推理延迟提供了一种解决方案。英特尔的 **AutoRound** 应运而生，成为一款在准确性、效率和兼容性之间取得平衡的尖端量化工具。

AutoRound 是英特尔开发的一种仅权重的训练后量化（PTQ）方法。它使用带符号的梯度下降来联合优化权重舍入和裁剪范围，能够在大多数场景下以最小的精度损失实现精确的低比特量化（例如，INT2 - INT8）。例如，在 INT2 精度下，其相对准确性比主流基线方法高出最多 **2.1 倍**。下图概述了 AutoRound 的核心算法。更多细节，请参阅我们的论文。

![algorithm overview<](/images/posts/0d3f95926854.png)

尽管性能强大，AutoRound 却快速且轻量——在 A100 GPU 上使用轻量模式量化一个 720 亿参数的模型仅需 **37 分钟**。它还支持混合比特调优、lm-head 量化、GPTQ/AWQ/GGUF 格式导出以及灵活的调优方案。

# 主要优势

## 低比特宽度下的卓越准确性

AutoRound 提供了非常有前景的结果，尤其是在低比特量化场景中。跨多种任务的评估表明，在 2 比特精度下，其表现远超主流方法（来源）。在 4 比特精度下，正如在低比特开放 LLM 排行榜上所展示的，AutoRound 在大多数情况下仍保持竞争优势。

W2g128 下 10+ 个任务的平均表现

![Average of 10+ tasks at W2g128<](/images/posts/b8e0d05f7f14.png)

W4 下 10+ 个任务的平均表现

![Average of 10+ tasks at W4<](/images/posts/efd7c98cdf32.png)

## 2. 广泛的兼容性

### 模型

**LLM：** AutoRound 支持几乎所有流行的 LLM 架构，包括 Qwen、LLaMA 和 DeepSeek 等知名模型。通过 OPEA、Kaitchup 和 fbaldassarri 等集合，可以在 Hugging Face 上找到开箱即用的量化模型。

**VLM：** AutoRound 支持超过 10 种视觉语言模型（VLM），包括 Mistral-Small-3.1、Gemma3 等。您可以在 README 中找到完整列表，开箱即用的量化模型可在 OPEA Hugging Face 集合中找到。对于尚未支持的模型，您仍然可以使用 `--iters 0` 参数应用我们的 RTN 方法。这不需要调优，但预计会有一些精度损失。

### 设备

- CPU
- 英特尔 GPU
- CUDA

### 量化配置

- 仅权重 Int8
- 仅权重 Int4
- 仅权重 Int3
- 仅权重 Int2
- 仅权重混合比特

### 导出格式

- AutoRound
- GPTQ
- AWQ
- 部分 GGUF

### 3. 灵活/高效的量化

AutoRound 仅需 200 个调优步骤和一个小型校准数据集（少至 128 个样本）即可实现高精度。与其他计算密集度更高的 int2 方法相比，这种效率意味着更快的量化时间和更少的资源消耗。

# 开始使用 AutoRound

## 安装

```bash
pip install auto-round

```

## 量化与序列化

目前仅支持离线模式来生成量化模型。

### 命令行用法

```bash
auto-round \
    --model Qwen/Qwen3-0.6B \
    --bits 4 \
    --group_size 128 \
    --format "auto_round,auto_awq,auto_gptq" \
    --output_dir ./tmp_autoround

```

AutoRound 还提供了另外两种方案：`auto-round-best` 和 `auto-round-light`，分别设计用于实现最佳精度和提升速度。

```bash
auto-round-best \
    --model Qwen/Qwen3-0.6B \
    --output_dir ./tmp_autoround

```

对于 2 比特量化，我们推荐使用 `auto-round-best` 或 `auto-round`。关于这三种方案的比较，请参考下表。

W4G128 下 13 个任务（mmlu-pro, if_eval, gsm8k 等）的平均精度和时间成本结果（测试在 Nvidia A100 80G 上使用 PyTorch 2.6.0 版本并启用 torch_compile 进行）：

### AutoRound API 用法

此设置在精度和调优成本之间提供了更好的权衡，推荐在所有场景中使用。

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from auto_round import AutoRound

model_name = "Qwen/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
bits, group_size, sym = 4, 128, True
autoround = AutoRound(
    model,
    tokenizer,
    bits=bits,
    group_size=group_size,
    sym=sym,
    
)

output_dir = "./tmp_autoround"
autoround.quantize_and_save(output_dir, format='auto_round,auto_awq,auto_gptq') 

```

关于 AutoRound API 用法的最佳/轻量设置或混合比特配置，请参考 AutoRound README。

## 推理

AutoRound 会根据已安装的库自动选择最佳可用后端，并在发现更好的后端时提示用户安装额外的库。更多细节，请参考 HF README 或 AutoRound README。

### CPU/英特尔 GPU/CUDA

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "OPEA/Qwen2.5-1.5B-Instruct-int4-sym-inc"
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)
text = "There is a girl who likes adventure,"
inputs = tokenizer(text, return_tensors="pt").to(model.device)
print(tokenizer.decode(model.generate(**inputs, max_new_tokens=50, do_sample=False)[0]))

```

### 将 GPTQ/AWQ 转换为 AutoRound

大多数 GPTQ/AWQ 模型可以转换为 AutoRound 格式，以获得更好的兼容性以及对英特尔设备的支持。请注意，如果模型被序列化，量化配置将会改变。

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoRoundConfig

model_name = "ybelkada/opt-125m-gptq-4bit"
quantization_config = AutoRoundConfig()
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu", torch_dtype="auto",
                                             quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained(model_name)
text = "There is a girl who likes adventure,"
inputs = tokenizer(text, return_tensors="pt").to(model.device)
print(tokenizer.decode(model.generate(**inputs, max_new_tokens=50, do_sample=False)[0]))

```

# 结论

AutoRound 为大语言模型和视觉语言模型的训练后量化迈出了重要的一步。通过将高精度、卓越效率以及对流行模型、设备和导出格式的广泛兼容性相结合，AutoRound 使得低比特量化既实用又强大。无论您是在大规模部署 LLM，还是在 VLM 上进行边缘推理实验，AutoRound 都提供了所需的工具和灵活性，让您能以最小的开销实现最佳性能。我们邀请您尝试使用，并加入不断壮大的社区，共同推动高效 AI 部署的边界。

欢迎并非常感谢对 **AutoRound** 的贡献！无论是修复错误、改进文档、添加新功能还是提出改进建议，您的帮助始终受到重视。

如果您在使用 auto-round 时遇到任何问题，请在 AutoRound 仓库中提交 issue。

# 致谢

我们要感谢包括 AutoGPTQ、AutoAWQ、GPTQModel、Triton、Marlin 和 ExLLaMAV2 在内的开源低精度库，AutoRound 使用了它们的 CUDA 内核。

---

> 本文由AI自动翻译，原文链接：[Introducing AutoRound: Intel’s Advanced Quantization for LLMs and VLMs](https://huggingface.co/blog/autoround)
> 
> 翻译时间：2026-04-22 04:57
