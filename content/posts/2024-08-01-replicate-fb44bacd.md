---
title: 通过API在Replicate上运行FLUX.1图像生成模型
title_original: Run FLUX with an API – Replicate blog
date: '2024-08-01'
source: Replicate Blog
source_url: https://replicate.com/blog/flux-state-of-the-art-image-generation
author: ''
summary: 本文介绍了如何在Replicate平台上通过API调用Black Forest Labs开发的开源图像生成模型FLUX.1。文章提供了JavaScript代码示例，并详细阐述了FLUX.1在文本处理、复杂构图和手部生成等方面的先进特性。同时，文章还介绍了FLUX.1的三种模型变体（pro、dev、schnell）及其定价，为开发者提供了快速上手指南。FLUX.1以其卓越的提示词遵循能力和图像质量，成为当前领先的开源文生图模型之一。
categories:
- AI产品
tags:
- 图像生成
- FLUX.1
- Replicate
- API
- Stable Diffusion
draft: false
translated_at: '2026-03-19T04:55:41.017157'
---

- Replicate
- 博客

# 通过API运行FLUX

- zeke
- zsxkib

FLUX.1是由Stable Diffusion的创造者Black Forest Labs开发的一款新型开源图像生成模型。它现已登陆Replicate平台，您只需一行代码即可在云端运行它。

以下是如何使用JavaScript在Replicate上运行FLUX.1的示例：

```
import Replicate from "replicate";
const replicate = new Replicate();

const model = "black-forest-labs/flux-dev";
const prompt = "Purple striped narwhal devouring a fluffy high-resolution everything bagel";
const output = await replicate.run(model, {input: { prompt }});
console.log(output);
```

您可以直接在浏览器中试用FLUX.1，或者使用您选择的语言以编程方式运行它。

## FLUX.1有何特别之处？

FLUX.1模型在提示词遵循、视觉质量、图像细节和输出多样性方面拥有最先进的性能。以下是一些令我们印象深刻的方面：

**文本处理！** 与那些经常搞混相似字母的旧模型不同，Flux能够处理带有重复字母的棘手词汇。这使得它在需要文本准确的设计场景中表现出色。看看这个Black Forest Flux Schnell蛋糕：

![带有文字的蛋糕](/images/posts/1c6240dea25e.webp)

**复杂构图。** Flux在遵循关于图像中物体位置的复杂指令方面表现惊人。例如，给定提示词“三位魔法师站在一张黄色桌子上，每人手持一个标牌。左边，一位身穿黑色长袍的魔法师手持写有‘AI’的标牌；中间，一位身穿红色长袍的女巫手持写有‘is’的标牌；右边，一位身穿蓝色长袍的魔法师手持写有‘cool’的标牌”，Flux完美地创建了这个场景：

![复杂场景](/images/posts/3e765af91730.webp)

**（基本）正确的手部。** 手部对AI来说是个难题，但Flux做得相当不错。您通常能得到位置正确、数量合适的手指。虽然并非完美，但这是一个巨大的进步——它始终优于我们尝试过的任何其他开源文生图模型：

![酷炫的手](/images/posts/dca55907f9a4.webp)

## 模型变体

- **FLUX.1 [pro]**：FLUX.1的精华，拥有顶级性能的最先进图像生成模型。
- **FLUX.1 [dev]**：一个用于非商业应用的开源权重、经过指导蒸馏的模型。它直接蒸馏自FLUX.1 [pro]，具有相似的图像质量和提示词遵循能力，同时比同尺寸的标准模型更高效。
- **FLUX.1 [schnell]**：最快的模型，专为本地开发和个人使用而设计。根据Apache 2.0许可证开源提供。

## 定价

FLUX.1按图像计费：

- FLUX.1 [pro] 每张图像0.055美元。
- FLUX.1 [dev] 每张图像0.030美元。
- FLUX.1 [schnell] 每张图像0.003美元。

## 后续步骤

FLUX.1是一款出色的模型，请务必尝试一下。请持续关注——既然模型已经发布，我们正着手开发诸如FLUX.1微调等功能，敬请期待。

---

> 本文由AI自动翻译，原文链接：[Run FLUX with an API – Replicate blog](https://replicate.com/blog/flux-state-of-the-art-image-generation)
> 
> 翻译时间：2026-03-19 04:55
