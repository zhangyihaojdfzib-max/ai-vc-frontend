---
title: Llama 4 Maverick & Scout 登陆 Hugging Face
title_original: Welcome Llama 4 Maverick & Scout on Hugging Face
date: '2025-04-05'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/llama4-release
author: ''
summary: Meta 的下一代大语言模型 Llama 4 Maverick（约400B参数）和 Scout（约109B参数）正式登陆 Hugging Face
  Hub。两者均为混合专家（MoE）模型，拥有17B活跃参数，支持原生多模态（文本+图像）。文章介绍了模型架构、上下文窗口（最高10M）、无 RoPE 层等创新，并详细说明了
  Hugging Face 的集成支持，包括 transformers、TGI、量化及 Xet 存储后端，旨在方便社区快速部署和微调。
categories:
- AI产品
tags:
- Llama 4
- 混合专家模型
- Hugging Face
- 多模态
- Meta
draft: false
translated_at: '2026-04-29T05:26:09.209231'
---

# 欢迎 Llama 4 Maverick & Scout 登陆 Hugging Face

我们无比激动地欢迎 Meta 的下一代大语言模型登陆 Hugging Face Hub：Llama 4 Maverick（约400B）和 Llama 4 Scout（约109B）！🤗 两者均为混合专家（MoE）模型，拥有17B活跃参数。

今天发布的这些强大的原生多模态模型代表着一次重大飞跃。我们与 Meta 紧密合作，确保从第一天起就与 Hugging Face 生态系统无缝集成，包括 transformers 和 TGI。

这只是我们与 Llama 4 合作的开始。未来几天，我们将继续与社区合作，利用 Maverick 和 Scout 构建出色的模型、数据集和应用！🔥

## 什么是 Llama 4？

Llama 4 由 Meta 开发，引入了新的自回归混合专家（MoE）架构。这一代包括两个模型：

- 高性能的 **Llama 4 Maverick**，总参数约400B，拥有17B活跃参数，配备128个专家。
- 高效的 **Llama 4 Scout**，总参数约109B，同样拥有17B活跃参数，仅使用16个专家。

两个模型均采用早期融合实现原生多模态能力，能够处理文本和图像输入。Maverick 和 Scout 均使用多达40万亿 Token 的数据进行训练，涵盖200种语言（并针对包括阿拉伯语、西班牙语、德语和印地语在内的12种语言提供特定微调支持）。

在部署方面，Llama 4 Scout 设计为易于访问，通过即时4位或8位量化可适配单张服务器级 GPU，而 Maverick 提供 BF16 和 FP8 格式。这些模型根据自定义的 Llama 4 社区许可协议发布，该协议可在模型仓库中获取。

## Hugging Face 上的功能与集成

为帮助社区立即利用这些最先进的模型，我们激动地宣布以下集成：

- **Hub 上的模型检查点**：Llama 4 Maverick 和 Llama 4 Scout 的模型权重可直接在 Hugging Face Hub 上的 `meta-llama` 组织下获取。这包括基础版本和指令微调版本，便于访问、探索和下载。您需要在模型卡片上接受许可条款后才能访问权重。
- **Hugging Face transformers 集成**：立即开始构建！Llama 4 模型已完全集成到 `transformers`（版本 v4.51.0）中。这允许使用熟悉的 API 轻松加载、推理和微调，包括支持其原生多模态能力以及 TRL 等下游库。
- transformers 中张量并行和自动设备映射的自动支持。
- **文本生成推理（TGI）支持**：为优化和可扩展的部署，两个模型均受 TGI 支持。这实现了高吞吐量的文本生成，使 Llama 4 更易于集成到生产应用中。
- **量化支持**：为 Scout 提供了即时 int4 量化的代码，在最小化性能下降的同时，支持在更小的硬件上部署。Maverick 包含 FP8 量化权重，可在兼容硬件上高效部署。
- **Xet 存储**：为改善上传下载体验，并支持社区微调模型的更快速迭代，我们使用 **Xet 存储后端** 发布了所有 Llama 4 模型。该存储系统专为更快的上传和下载而设计，在 Llama 4 上实现了约25%的去重。所有衍生模型（微调、量化等）应具有更高的去重率（约40%），为社区节省更多时间和带宽。

## 上下文窗口长度与架构选择

Llama 4 模型以256K的上下文窗口长度进行预训练。指令模型经过微调以支持更大的上下文窗口长度：大型128专家版本（Maverick）支持1M，而16专家版本（Scout）支持10M（！）。

这些大上下文窗口长度伴随着一些非常有趣的架构选择。在官方技术报告发布之前，以下是我们目前所知的信息。

- **无 RoPE（NoPE）层**

NoPE（可爱的名字，魅力值+1），早在2022年就被探索过，它摒弃了传统的位置编码方案（如 RoPE），而 RoPE 在大多数情况下应用于 Transformer 模型。在 Llama 4 中，每4层使用一个 NoPE 层。这些层对于长上下文至关重要，因为它们在整个上下文上使用完整的因果掩码。

对于 RoPE 层（每4层中的3层），使用 **分块注意力**。

Meta 将 NoPE 层的交错使用与温度缩放（如下所述）称为 **iRoPE** 架构。

如果您想了解更多关于位置编码的信息，我们推荐 Chris 最近的文章。

- **分块注意力**（在 RoPE 层中）

为减少内存需求，Llama 4 在使用传统 RoPE 位置编码的层（每4个解码器层中的3层）中使用分块注意力。可视化分块注意力工作原理的最佳方式是通过从 `transformers` 源代码中提取的以下 ASCII 表示：

```
'What'      :  0 ■ ⬚ ⬚ ⬚ ⬚ ⬚ 
'▁is'       :  1 ■ ■ ⬚ ⬚ ⬚ ⬚ 
'▁ch'       :  2 ■ ■ ■ ⬚ ⬚ ⬚ 
'unked'     :  3 ⬚ ⬚ ⬚ ■ ⬚ ⬚ 
'▁attention':  4 ⬚ ⬚ ⬚ ■ ■ ⬚ 
'?'         :  5 ⬚ ⬚ ⬚ ■ ■ ■ 
```

此图显示了如果分块注意力长度为3时将使用的注意力掩码。在 Llama 4 中，分块注意力长度为 **8192**。这意味着 RoPE 层只能跟踪8K块内的上下文，而 NoPE 层可以访问完整上下文。您可以将其视为滑动窗口注意力的更节省内存和计算效率的版本。

- **注意力温度调节**

应用于长上下文的注意力块存在一个问题：随着序列长度增加，注意力概率分数会逐渐趋近于零。这是将 softmax 函数应用于非常长序列的已知后果。为解决此问题，Llama 4 使用缩放后的 softmax，模型称之为温度调节。这应用于 NoPE 层，但不应用于 RoPE 层，因为后者关注的是较短的子序列。

这种方法是一种改善任意上下文长度泛化能力的方式，并且可能是实现 Llama 4 Scout 10M 上下文窗口长度的关键因素之一。

- **QK 归一化**

Llama Scout（16专家版本）在应用 RoPE 嵌入后，在 RoPE 层中对查询和键状态使用额外的无学习参数的 RMS 归一化。

- **MoE 交错**

Llama Scout 是一个完整的 MoE 模型，包含16个专家。Llama Maverick 使用128个专家，但 MoE 层和密集层交替出现。因此，专家应用于一半的层中。

- **共蒸馏**

Llama Maverick 是从更大的模型 Llama Behemoth 通过共蒸馏得到的，使用了一种新颖的损失函数，该函数动态加权学生和教师的 logit。

- **MetaP**

这些模型利用 MetaP，一种可能受 MuP 启发的方法，以在不同维度（包括训练预算和模型大小）上优化调整超参数。

## 如何使用 Transformers

使用 `transformers` 开始使用 Llama 4 非常简单。请确保您已安装 `transformers v4.51.0` 或更高版本（`pip install -U transformers huggingface_hub[hf_xet]`）。以下是一个使用指令微调 Maverick 模型响应两张图像的快速示例，使用张量并行以获得最大速度。您需要在具有8个 GPU 的实例上运行此脚本，使用如下命令：`torchrun –nproc-per-instance=8 script.py`

```py
from transformers import AutoProcessor, Llama4ForConditionalGeneration
import torch

model_id = "meta-llama/Llama-4-Maverick-17B-128E-Instruct"

processor = AutoProcessor.from_pretrained(model_id)
model = Llama4ForConditionalGeneration.from_pretrained(
    model_id,
    attn_implementation="flex_attention",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
```

url1 = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/0052a70beed5bf71b92610a43a52df6d286cd5f3/diffusers/rabbit.jpg"
url2 = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/datasets/cat_style_layout.png"
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": url1},
            {"type": "image", "url": url2},
            {"type": "text", "text": "你能描述这两张图片的相似之处和不同之处吗？"},
        ]
    },
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

outputs = model.generate(
    **inputs,
    max_new_tokens=256,
)

response = processor.batch_decode(outputs[:, inputs["input_ids"].shape[-1]:])[0]
print(response)
print(outputs[0])

```

请务必查看仓库中的模型卡片（Llama 4 Maverick（约400B）和 Llama 4 Scout（约109B）），以获取详细的使用说明，包括多模态示例、特定的提示词格式（如系统提示词）、量化细节以及高级配置选项！

## 评估分数

评估结果证实了这些模型的强大性能，展现出最先进的水平，显著超越了 Llama 3.1 405B 等前代模型。例如，在推理和知识任务上，经过指令微调的 Maverick 在 MMLU Pro 上达到 80.5%，在 GPQA Diamond 上达到 69.8%，而 Scout 分别得分 74.3% 和 57.2%。

### 预训练模型

### 指令微调模型

## 致谢

发布像 Llama 4 这样的巨型模型需要跨团队、跨地区以及大量虚拟机的巨大努力。我们特别感谢 Transformers 团队的 Arthur、Lysandre、Cyril、Pablo、Marc、Mohammed。我们感谢整个 vLLM 团队，在这次充满挑战的紧密集成过程中，他们进行了丰富的讨论、提供了深刻的见解、共享了测试和调试工作。面对更大的优化需求，我们要感谢 Mohit 在 TGI 中独立为 Llama 4 添加了支持。这些庞大的模型在存储层面需要非常严谨的工程工作。这离不开 Ajit、Rajat、Jared、Di、Yucheng 以及 Xet 团队其他成员的巨大努力。

许多人为这项工作付出了心血，非常感谢 Hugging Face、vLLM 和 Meta Llama 团队的其他成员，感谢你们出色的协同合作！

## 参考文献

- 了解更多关于 Xet Storage 的信息：博客文章 和 Hub 文档。
- 查看 Meta 的发布博客文章

---

> 本文由AI自动翻译，原文链接：[Welcome Llama 4 Maverick & Scout on Hugging Face](https://huggingface.co/blog/llama4-release)
> 
> 翻译时间：2026-04-29 05:26
