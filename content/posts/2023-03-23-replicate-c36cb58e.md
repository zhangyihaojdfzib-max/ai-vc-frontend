---
title: 用Alpaca-LoRA微调类ChatGPT模型指南
title_original: How to use Alpaca-LoRA to fine-tune a model like ChatGPT – Replicate
  blog
date: '2023-03-23'
source: Replicate Blog
source_url: https://replicate.com/blog/fine-tune-alpaca-with-lora
author: ''
summary: 本文介绍了如何使用低秩适配（LoRA）技术微调大语言模型，特别是基于LLaMA的Alpaca-LoRA项目。LoRA相比传统微调方法速度更快、内存占用更少，可在消费级GPU上运行，输出结果小且支持运行时组合多个微调模型。文章详细说明了从克隆仓库、安装Cog工具、获取LLaMA权重到运行微调脚本的完整步骤，并指出在40GB
  A100 GPU上微调约需3.5小时。该方法降低了模型微调的门槛，使个人开发者也能在有限硬件上定制AI模型。
categories:
- AI研究
tags:
- LoRA
- Alpaca-LoRA
- LLaMA微调
- 大语言模型
- 模型微调
draft: false
translated_at: '2026-06-02T06:34:57.851896'
---

- Replicate
- 博客

# 如何使用 Alpaca-LoRA 微调类似 ChatGPT 的模型

- andreasjansson
- daanelson
- zeke

低秩适配（LoRA）是一种用于微调模型的技术，与以往方法相比具有一些优势：

- 速度更快，内存占用更少，这意味着它可以在消费级硬件上运行。
- 输出结果小得多（兆字节，而非千兆字节）。
- 你可以在运行时将多个微调后的模型组合在一起。

上个月，我们发表了一篇关于使用 LoRA 更快地微调 Stable Diffusion 的博客。我们的朋友 Simon Ryu（又名 @cloneofsimo）将 LoRA 技术应用于 Stable Diffusion，使得人们能够仅凭少量训练图像创建自定义训练风格，然后在预测时混合搭配这些风格，生成高度定制化的图像。

快进一个月后，我们看到 LoRA 被应用于其他领域。现在它被用于微调像 LLaMA 这样的大语言模型。本月早些时候，Eric J. Wang 发布了 Alpaca-LoRA，这是一个包含代码的项目，用于使用 PEFT 重现 Stanford Alpaca 的结果。PEFT 是一个库，允许你获取各种基于 Transformer 的语言模型，并使用 LoRA 对其进行微调。其巧妙之处在于，它允许你在中等硬件上以低成本高效地微调模型，并生成更小（或许还可组合）的输出。

在这篇博客文章中，我们将向你展示如何使用 LoRA 结合 Alpaca 训练数据来微调 LLaMA。

## 前提条件

- GPU 机器。得益于 LoRA，你可以在低规格 GPU（如 NVIDIA T4）或消费级 GPU（如 4090）上完成此操作。如果你还没有一台带 GPU 的机器，请查看我们的 GPU 机器获取指南。
- LLaMA 权重。LLaMA 的权重尚未公开发布。要申请访问权限，请填写此 Meta Research 表单。

## 第 1 步：克隆 Alpaca-LoRA 仓库

我们创建了原始 Alpaca-LoRA 仓库的一个分支，增加了对 Cog 的支持。Cog 是一个用于将机器学习模型打包到容器中的工具，我们用它来安装微调和运行模型所需的依赖项。

使用 Git 克隆仓库：

```
git clone https://github.com/daanelson/alpaca-lora
cd alpaca-lora
```

## 第 2 步：安装 Cog

```
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
```

## 第 3 步：获取 LLaMA 权重

将你下载的权重放入名为 unconverted-weights 的文件夹中。文件夹层次结构应如下所示：

```
unconverted-weights
├── 7B
│   ├── checklist.chk
│   ├── consolidated.00.pth
│   └── params.json
├── tokenizer.model
└── tokenizer_checklist.chk
```

使用以下命令将权重从 PyTorch 检查点转换为 transformers 兼容格式：

```
cog run python -m transformers.models.llama.convert_llama_weights_to_hf \
  --input_dir unconverted-weights \
  --model_size 7B \
  --output_dir weights
```

你最终的目录结构应如下所示：

```
weights
├── llama-7b
└── tokenizermdki
```

## 第 4 步：微调模型

微调脚本默认配置为在性能较低的 GPU 上运行，但如果你有内存更大的 GPU，可以在 finetune.py 中将 MICRO_BATCH_SIZE 增加到 32 或 64。

如果你有自己的指令微调数据集，请编辑 finetune.py 中的 DATA_PATH，指向你自己的数据集。确保其格式与 alpaca_data_cleaned.json 相同。

运行微调脚本：

```
cog run python finetune.py
```

在 40GB A100 GPU 上这需要 3.5 小时，对于处理能力较低的 GPU 则需要更长时间。

## 第 5 步：使用 Cog 运行模型

```
$ cog predict -i prompt="Tell me something about alpacas."

Alpacas are domesticated animals from South America. They are closely related to llamas and guanacos and have a long, dense, woolly fleece that is used to make textiles. They are herd animals and live in small groups in the Andes mountains. They have a wide variety of sounds, including whistles, snorts, and barks. They are intelligent and social animals and can be trained to perform certain tasks.
```

## 后续步骤

以下是一些你可以尝试的想法：

- 使用你自己的数据集微调你自己的 LoRA，例如 Cabrita：一个葡萄牙语微调指令 LLaMA，或微调 LLaMA 使其像 Homer Simpson 一样说话。
- 将模型推送到 Replicate 以在云端运行。如果你需要 API 来构建界面，或并行进行大规模评估，这会很方便。你需要将其设为私有，以免权重公开。
- 组合 LoRA。可以将不同的 Stable Diffusion LoRA 组合起来，在同一图像中同时拥有微调风格和微调对象。如果对语言模型也这样做，可能会实现什么？
- 使用 Alpaca 数据集（或其他数据集）微调更大的 LLaMA 模型，并观察其性能。这应该可以通过 PEFT 和 LoRA 实现，尽管需要更大的 GPU。

我们迫不及待地想看到你的成果。

在 Twitter 上关注我们以获取最新动态。我们将发布更多关于开源语言模型调试的指南。

---

> 本文由AI自动翻译，原文链接：[How to use Alpaca-LoRA to fine-tune a model like ChatGPT – Replicate blog](https://replicate.com/blog/fine-tune-alpaca-with-lora)
> 
> 翻译时间：2026-06-02 06:34
