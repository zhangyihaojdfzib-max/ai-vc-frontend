---
title: LoRA：五分钟微调Stable Diffusion的轻量方案
title_original: 'Introducing LoRA: A faster way to fine-tune Stable Diffusion – Replicate
  blog'
date: '2023-02-07'
source: Replicate Blog
source_url: https://replicate.com/blog/lora-faster-fine-tuning-of-stable-diffusion
author: ''
summary: 本文介绍了LoRA（低秩适应）技术在Stable Diffusion微调中的应用。相比DreamBooth，LoRA训练时间从20分钟缩短至8分钟，模型大小从数GB降至约5MB，且支持多概念组合与即时推理。文章详细说明了LoRA的独特优势（更快训练、更小输出、更好风格表现）以及从收集图像到生成新图像的四步操作流程，为开发者提供了一种高效、低成本的模型定制方案。
categories:
- AI研究
tags:
- LoRA
- Stable Diffusion
- 模型微调
- 低秩适应
- DreamBooth对比
draft: false
translated_at: '2026-06-03T06:52:24.103766'
---

- Replicate
- 博客

# 介绍 LoRA：一种更快的微调 Stable Diffusion 的方法

- cloneofsimo
- andreasjansson
- anotherjesse
- zeke

去年，DreamBooth 发布了。这是一种针对你自己的物体或风格训练 Stable Diffusion 的方法。

短短几个月后，Simo Ryu 创建了一种新的图像生成模型，将一种名为 LoRA 的技术应用于 Stable Diffusion。与 DreamBooth 类似，LoRA 让你只需使用少量图像就能训练 Stable Diffusion，并生成包含这些物体或风格的新输出图像。与 DreamBooth 不同的是，LoRA 速度很快：DreamBooth 运行大约需要二十分钟，生成的模型有数 GB 大小，而 LoRA 训练只需短短八分钟，生成的模型大约只有 5MB。

LoRA 代表低秩适应（Low-Rank Adaptation），这是一种减少训练参数数量的数学技术。你可以将其视为创建模型的差异文件，而不是保存整个模型。LoRA 由微软的研究人员开发，Simo 将其应用到了 Stable Diffusion 上。查看 GitHub 上 Simo 的推理模型 README 以及 arXiv 上的论文，以了解更多关于其工作原理的信息。

我们一直在与 Simo 合作，将 LoRA 部署到 Replicate 上。现在，你可以通过一次 API 调用在云端训练 LoRA 模型。与 DreamBooth 不同，后者需要等待模型推送并启动，而 LoRA 预测可以即时运行，无需冷启动。

![来自 LoRA 训练的示例图像](/images/posts/19d5d47ac539.webp)

## LoRA 有何独特之处？

LoRA 与 DreamBooth 有一些不同之处，使其作为替代方案特别有吸引力：

- **更快的训练**：使用 LoRA 训练一个新概念只需几分钟。
- **更小的输出**：训练后的 LoRA 输出比 DreamBooth 输出小得多。这使得它们更容易共享、存储和重复使用。
- **多概念组合**：你可以在单个图像中组合多个训练好的概念。（此功能仍处于实验阶段，但我们正在努力改进。🧪）
- **更快的图像生成**：当你在 Replicate 上训练自己的 DreamBooth 模型时，该模型仅在你主动使用时保持热状态。使用 LoRA，你不需要运行自己的模型，而是运行 `cloneofsimo/lora` 模型，该模型始终在线并准备好提供服务预测。
- **风格表现更好，人脸表现较差**。根据我们的实验，LoRA 在风格方面似乎比 DreamBooth 做得更好，但人脸效果不佳。它们停留在恐怖谷效应中，而不是看起来精确像本人。不过，你的结果可能会比我们的更好，所以请告诉我们你的进展。

## 如何使用 LoRA

🐴 要了解其可能性，请查看 LoRA 示例页面，你可以在那里试用我们一些预训练的概念，比如 Bob Ross、宝可梦、南方公园、卡拉瓦乔等等。

要训练你自己可重复使用的 LoRA 概念，请执行以下步骤：

1.  将训练图像收集到一个 zip 文件中。
2.  将你的训练图像上传到一个可公开访问的 URL。
3.  使用 LoRA 的训练模型之一来训练你的概念。
4.  保存你训练输出的 URL。
5.  使用 LoRA 的预测模型，用你训练好的概念生成新图像。

## 步骤 1：收集训练图像

要训练一个新的 LoRA 概念，创建一个包含几张相同人脸、物体或风格图像的 zip 文件。5-10 张图像就足够了，但对于风格，如果你有 20-100 个示例，可能会得到更好的结果。许多针对训练 DreamBooth 的建议也适用于 LoRA。训练图像可以是 JPG 或 PNG 格式。

💡 给你的 zip 文件起一个有意义的名称，因为它将作为训练输出文件名的一部分。这将有助于以后更容易地识别和区分不同的训练输出。

## 步骤 2：上传训练图像

LoRA 的训练模型期望你的图像能通过 HTTP 在公共 URL 上访问。你可以使用像 Google Drive、Amazon S3 或 GitHub Pages 这样的服务来托管你的 zip 文件。

## 步骤 3：训练你的概念

Replicate 上有两个 LoRA 训练模型：

- `replicate/lora-training` 为面部/物体/风格提供了预设选项，我们发现这些选项对这些用例是最优的。
- `replicate/lora-advanced-training` 允许你自行设置选项，以便完全控制模型。

首先使用 `lora-training` 模型来训练你的概念。以下是一个示例 Python 脚本，它使用训练模型来训练一个新概念：

```
import replicate

# 包含输入图像的 zip 文件，托管在互联网上的某个位置
zip_url = "https://my-storage/my-input.zip"

# 训练模型
lora_url = replicate.run(
    "replicate/lora-training:b2a308762e36ac48d16bfadc03a65493fe6e799f429f7941639a6acec5b276cc",
    input={"instance_data": zip_url, "task": "style"}
)
```

## 步骤 4：保存你训练输出的 URL

每次训练运行的输出是一个单独的 `.safetensors` 文件，位于我们无限期托管的 HTTPS URL 上。

例如，`https://replicate.delivery/pbxt/S8wVSt0vXr5mEFDjP5XkmMPjLPCaDmv1Rw6AzRMDEhoFqqGE/tmp_fs4evyhbob-ross.safetensors`

从你的预测响应中复制该训练概念文件的 URL，以便将其用作 LoRA 预测模型的输入。

## 步骤 5：生成图像

现在你已经有了一个训练好的概念，是时候生成一些新图像了！你可以基于单个训练概念生成图像，也可以将多个训练概念组合在一起使用。

预测模型 `replicate/lora` 需要两个输入：

- `prompt`：一个包含字符串 `<1>` 的提示词，用于指示训练概念应出现的位置，例如 `an astronaut riding a horse in the style of <1>`。如果你要向 `lora_urls` 输入传递多个 URL，请使用 `<2>`、`<3>`。
- `lora_urls`：你在上一步中复制的一个或多个训练好的 LoRA 概念的 URL。你可以传递单个 URL，或用管道符 `|` 分隔的 URL 列表。传递多个 URL 允许你将多个概念组合到单个图像中。

你可以从浏览器运行 LoRA 的预测模型：

你也可以使用 Replicate 运行 LoRA 的预测模型。以下是一个示例 Python 脚本，它使用 API 生成新图像：

```
import replicate

lora_url = "https://replicate.delivery/pbxt/S8wVSt0vXr5mEFDjP5XkmMPjLPCaDmv1Rw6AzRMDEhoFqqGE/tmp_fs4evyhbob-ross.safetensors"

output_url = replicate.run(
    "replicate/lora:97ec1b97e5e6a6476e45ba7211d368509bbf39c30a927e39637f3cb98b36ac91",
    input={
        "prompt": "a painting of dinosaur in the style of <1>",
        "lora_urls": lora_url,
    },
)
```

## 后续步骤

在接下来的几周内，我们将增加对在 Stable Diffusion 2.1、图像修复以及其他酷炫功能上训练 LoRA 的支持。请告诉我们你的想法！

如果你想与社区分享你的 LoRA 模型，或者看看其他人的成果，请加入我们 Discord 中的 #lora 频道。

---

> 本文由AI自动翻译，原文链接：[Introducing LoRA: A faster way to fine-tune Stable Diffusion – Replicate blog](https://replicate.com/blog/lora-faster-fine-tuning-of-stable-diffusion)
> 
> 翻译时间：2026-06-03 06:52
