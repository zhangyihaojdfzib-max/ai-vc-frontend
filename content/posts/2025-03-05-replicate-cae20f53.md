---
title: Wan2.1：通过API生成高性能开源AI视频
title_original: 'Wan2.1: generate videos with an API – Replicate blog'
date: '2025-03-05'
source: Replicate Blog
source_url: https://replicate.com/blog/wan-21-generate-videos-with-an-api
author: ''
summary: 本文介绍了最新开源AI视频模型Wan2.1，该模型在真实世界物理模拟、手部细节和物体交互方面表现出色，支持480p和720p分辨率。文章详细说明了如何在Replicate平台上通过API调用该模型进行文本生成视频和图像生成视频，并提供了代码示例。Wan2.1模型具有速度快、开源、可在消费级GPU上运行等优势，适合开发者和研究者用于视频生成实验与应用开发。
categories:
- AI产品
tags:
- AI视频生成
- Wan2.1
- Replicate
- 开源模型
- API调用
draft: false
translated_at: '2026-02-25T04:32:20.879299'
---

- Replicate
- 博客

# Wan2.1：通过API生成视频

- zeke

如果你最近一直在关注AI视频领域，你可能已经注意到它正在爆发式发展。每周都有新的模型发布，它们能生成更好的输出、更高的分辨率和更快的生成速度。

Wan2.1是最新、性能最强的开源视频模型。它于上周发布，并且正在领跑各大排行榜。

您的浏览器不支持视频标签。

Wan2.1有很多值得称道的地方：

*   它在Replicate上速度很快。生成一段5秒的视频，480p分辨率需要39秒，720p分辨率需要150秒。
*   它是**开源**的，包括模型权重和代码。社区已经在构建工具来增强它。
*   它能生成具有真实世界准确性的惊艳视频。
*   它足够小，可以在消费级GPU上运行。

在这篇文章中，我们将介绍这些新模型以及如何通过API运行它们。

## 模型版本

该模型在Replicate上提供了多种不同的版本：

*   Wan 2.1 文本生成视频，480p – wavespeedai/wan-2.1-t2v-480p（140亿参数）
*   Wan 2.1 图像生成视频，480p – wavespeedai/wan-2.1-i2v-480p（140亿参数）
*   Wan 2.1 文本生成视频，720p – wavespeedai/wan-2.1-t2v-720p（140亿参数）
*   Wan 2.1 图像生成视频，720p – wavespeedai/wan-2.1-i2v-720p（140亿参数）
*   Wan 2.1 文本生成视频，480p – wan-video/wan-2.1-1.3b（13亿参数）

480p模型非常适合实验，因为它们运行速度更快。

如果你需要更高的分辨率，请使用720p模型。

13亿参数的模型更小，专为在消费级GPU上运行而设计。

## 真实世界准确性

140亿参数的模型在真实世界物理模拟方面表现出色，你可以用它完成大多数其他模型难以处理的任务：

*   **手部**：该模型能很好地处理手部细节，显示单个手指、皮肤纹理以及戒指等细节。
*   **绘画动画**：它能将静态绘画转换成短视频片段。
*   **物理效果**：当提示生成一段长颈鹿倒挂在树上的视频时，模型描绘了树枝在重压下弯曲的情景。
*   **头发运动**：在有人物的视频中，头发渲染准确，能显示人物转头时发丝的运动。
*   **物体交互**：它能准确渲染同一空间内多个物体的交互。
*   **人群**：在渲染大场景时，每个物体都保持清晰可辨，创造出连贯的场景。

## 通过API运行Wan2.1

Replicate上的每个模型都有一个可扩展的云API，Wan2.1也不例外。

以下是一个使用Replicate JavaScript客户端运行Wan2.1文本生成视频模型的代码片段：

```
import Replicate from "replicate";

const replicate = new Replicate()
const model = "wavespeedai/wan-2.1-i2v-480p"
const input = {
  image: "https://replicate.delivery/pbxt/MZZyui7brAbh1d2AsyPtgPIByUwzSv6Uou8objC7zXEjLySc/1a8nt7yw5drm80cn05r89mjce0.png",
  prompt: "A woman is talking",
}

const output = await replicate.run(model, { input })
console.log(output)
```

**图像生成视频**模型的代码几乎相同。只需在调用模型时省略`image`输入即可：

```
import Replicate from "replicate"

const replicate = new Replicate()
const model = "wavespeedai/wan-2.1-t2v-480p";
const input = {
  prompt: "A woman is talking"
}
const output = await replicate.run(model, { input })

console.log(output.url())
```

## 尝试调整设置

Wavespeed Wan2.1模型还提供了许多不同的设置供你尝试。

可以尝试调整`guide_scale`、`shift`和`steps`。我们发现较低的`guide_scale`和`shift`值（大约为4和2）可以生成非常逼真的视频。

## 社区共同努力

没有众多开源贡献者的工作，这个模型就不可能存在。我们正在使用**WavespeedAI的优化**技术，为你带来世界上最快的生成速度。

特别感谢阿里巴巴开源此模型，也感谢`@chengzeyi`和`@wavespeed_ai`与我们合作，为你带来这样的速度。⚡️

---

> 本文由AI自动翻译，原文链接：[Wan2.1: generate videos with an API – Replicate blog](https://replicate.com/blog/wan-21-generate-videos-with-an-api)
> 
> 翻译时间：2026-02-25 04:32
