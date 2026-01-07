---
title: 在Replicate上运行Isaac 0.1：20亿参数视觉语言模型
title_original: Run Isaac 0.1 on Replicate – Replicate blog
date: '2025-11-26'
source: Replicate Blog
source_url: https://replicate.com/blog/isaac-01
author: null
summary: Perceptron AI发布了Isaac 0.1，这是一个拥有20亿参数的开放权重视觉语言模型，专为基于事实的感知任务设计。该模型能够回答图像问题、进行空间关系推理、在复杂环境中读取文本，并能提供答案来源的视觉依据（如边界框）。其特色包括基于事实的视觉推理、强大的真实场景OCR能力、对物理环境的空间感知，以及无需微调即可通过示例学习新任务的能力。尽管参数规模较小，Isaac在OCR、物体识别和视觉推理方面的表现可与更大模型媲美，且效率高，适用于机器人、制造检测、文档处理等实时或边缘计算场景。文章还提供了通过Replicate
  API使用JavaScript快速运行该模型的示例代码。
categories:
- AI产品
tags:
- 视觉语言模型
- Isaac 0.1
- Replicate
- OCR
- 视觉推理
draft: false
translated_at: '2026-01-05T16:35:07.388Z'
---

在 Replicate 上运行 Isaac 0.1
运行 Isaac 0.1
Perceptron AI 发布了 Isaac 0.1，这是一个拥有 20 亿参数、开放权重的视觉语言模型，专为基于事实的感知而构建。Isaac 能够回答关于图像的问题，推理空间关系，在杂乱环境中读取文本，并指出其答案的来源。
尽管体积小巧，Isaac 在 OCR、物体识别和视觉推理方面的能力可与大其数倍的模型相媲美。

Isaac 0.1 的特别之处
基于事实的视觉推理
Isaac 不仅能描述场景，还能解释其答案为何正确，并返回与每个论断相关联的边界框或区域。这有助于您构建需要透明度、可追溯性或分步证据的应用程序。

真实场景下的强大 OCR
该模型能够读取标志、标签、包装和文档上微小或被部分遮挡的文本。它将 OCR 与上下文理解相结合，因此您可以提出诸如“退货地址是什么？”或“比赛还剩多少时间？”之类的问题。

针对物理环境的空间感知
Isaac 理解物体之间如何相互关联：它们的位置、如何互动，以及何时出现异常。这使得它在识别未对齐的组件、发现损坏部件或确定物品应属于哪个箱子或位置等任务中非常有用。

通过示例学习新任务
向 Isaac 展示几个您关心的缺陷、组件或状况的标注示例，它便能立即适应，无需进行微调。

为高效而构建
Isaac 仅有 20 亿参数，速度快到足以满足实时或边缘受限应用的需求。它非常适用于机器人、制造、视觉检测和大规模文档工作流。

开始使用 API
以下是如何使用 JavaScript 和 Replicate API 运行 Isaac 0.1 的方法：
import Replicate from "replicate";
const replicate = new Replicate();
const input = {
image: "https://replicate.delivery/pbxt/O3bB4rzBd1qi3wMWb1GFvjuxduAw9AfASgAkfCLcaT1380ZN/woman-street.webp"
};
const output = await replicate.run("perceptron-ai-inc/isaac-0.1", { input });
console.log(output)
//=> {"text":"No, it is not safe to cross the street at this t...
运行 Isaac 0.1

---

> 本文由AI自动翻译，原文链接：[Run Isaac 0.1 on Replicate – Replicate blog](https://replicate.com/blog/isaac-01)
> 
> 翻译时间：2026-01-05 13:17
