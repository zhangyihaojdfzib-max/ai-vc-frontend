---
title: Waypoint-1：实时交互式视频扩散模型，用键盘鼠标创造世界
title_original: 'Introducing Waypoint-1: Real-time interactive video diffusion from
  Overworld'
date: '2026-01-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/waypoint-1
author: ''
summary: Overworld推出的Waypoint-1是一款创新的实时交互式视频扩散模型，允许用户通过文本、鼠标和键盘输入实时控制和生成视频世界。该模型采用帧因果校正流Transformer架构，在1万小时游戏录像上训练，支持零延迟交互。与依赖预训练模型微调的传统方法不同，Waypoint-1专为交互体验设计，结合扩散强制预训练和自强制后训练技术，减少长序列生成的误差累积。配套的WorldEngine推理库优化性能，在消费级硬件上可实现30-60
  FPS的流畅体验。
categories:
- AI研究
tags:
- 视频生成
- 扩散模型
- 实时交互
- 世界模型
- Transformer
draft: false
translated_at: '2026-01-21T04:38:30.053221'
---

# Waypoint-1：来自 Overworld 的实时交互式视频扩散模型

- 
- 
- 
- 
- 

![](/images/posts/4241b99076dc.jpg)

![](/images/posts/f20fa9eebbef.jpg)

![](/images/posts/cf46f3f2bac8.jpg)

![Louis Castricato 的头像](/images/posts/4241b99076dc.jpg)

![Scott Fox 的头像](/images/posts/438a901d01fb.png)

![waypoint 启动网格](/images/posts/57356a747284.gif)

## Waypoint-1Hub 上的权重试用模型什么是 Waypoint-1？它是如何训练的？推理库：WorldEngine使用 World Engine 构建保持联系Waypoint-1Hub 上的权重

- Waypoint-1Hub 上的权重
- 试用模型
- 什么是 Waypoint-1？
- 它是如何训练的？
- 推理库：WorldEngine
- 使用 World Engine 构建
- 保持联系

- Waypoint-1-Small
- Waypoint-1-Medium（即将推出！）

Overworld Stream：https://overworld.stream

Waypoint-1 是 Overworld 的实时交互式视频扩散模型，可通过文本、鼠标和键盘进行控制和提示。你可以给模型一些帧，运行模型，让它创建一个你可以步入并与之互动的世界。

该模型的核心是一个帧因果校正流 Transformer，在 10,000 小时多样化的电子游戏录像片段上训练而成，这些片段与控制输入和文本描述配对。Waypoint-1 是一个潜在模型，意味着它在压缩帧上进行训练。

现有世界模型的标准做法是采用预训练的视频模型，并用简短简化的控制输入进行微调。相比之下，Waypoint-1 从一开始就专注于交互式体验进行训练。对于其他模型，控制很简单：你可以每隔几帧移动和旋转一次相机，但存在严重的延迟问题。而对于 Waypoint-1，就控制而言，你完全不受限制。你可以用鼠标自由移动相机，输入键盘上的任何按键，所有这些都实现零延迟。每一帧的生成都以你的控制作为上下文。此外，该模型运行速度足够快，即使在消费级硬件上也能提供无缝体验。

Waypoint-1 通过扩散强制进行预训练，这是一种让模型学习在给定过去帧的情况下对未来的帧进行去噪的技术。应用了因果注意力掩码，使得任何给定帧中的 Token 只能关注其自身帧或过去帧中的 Token，而不能关注未来帧。每一帧都被随机添加噪声，因此模型学习分别对每一帧进行去噪。在推理过程中，你可以一次去噪一个新帧，从而生成一个程序化的新帧流。

虽然扩散强制提供了一个强大的基线，但随机对所有帧添加噪声与逐帧自回归展开的方式并不一致。这种推理不匹配会导致误差累积和长序列生成时的噪声问题。为了解决这个问题，我们使用自强制进行后训练，这是一种训练模型在匹配推理行为的机制下产生逼真输出的技术。通过 DMD 进行的自强制还有一个额外的好处，即单次 CFG 和少步去噪。

## 推理库：WorldEngine

WorldEngine 是 Overworld 用于交互式世界模型流的高性能推理库。它为核心工具，用于在纯 Python 中构建推理应用，针对低延迟、高吞吐量、可扩展性和开发者简易性进行了优化。运行时循环专为交互性设计：它接收上下文帧图像、键盘/鼠标输入和文本，并输出用于实时流传输的图像帧。

在 5090 GPU 上运行的 Waypoint-1-Small（2.3B）模型，WorldEngine 可维持约每秒 30,000 次 Token 传递（单次去噪；每帧 256 个 Token），并在 4 步时达到 30 FPS，或在 2 步时达到 60 FPS。

性能来自四项针对性优化：

- AdaLN 特征缓存：只要前向传递之间的提示词条件和时间步保持不变，就通过缓存和重用来避免重复的 AdaLN 条件投影。
- 静态滚动 KV 缓存 + Flex Attention
- 矩阵乘法融合：使用融合的 QKV 投影进行标准推理优化。
- Torch Compile：使用 `torch.compile(fullgraph=True, mode="max-autotune", dynamic=False)`

```
from world_engine import WorldEngine, CtrlInput

# 创建推理引擎
engine = WorldEngine("Overworld/Waypoint-1-Small", device="cuda")

# 指定提示词
engine.set_prompt("A game where you herd goats in a beautiful valley")

# 可选：强制下一帧为特定图像
img = pipeline.append_frame(uint8_img)  # (H, W, 3)

# 根据控制器输入生成 3 个视频帧
for controller_input in [
        CtrlInput(button={48, 42}, mouse=[0.4, 0.3]),
        CtrlInput(mouse=[0.1, 0.2]),
        CtrlInput(button={95, 32, 105}),
]:
    img = engine.gen_frame(ctrl=controller_input)

```

## 使用 World Engine 构建

我们将在 2026 年 1 月 20 日举办一场 `world_engine` 黑客马拉松 - 你可以在此处回复参与。欢迎 2-4 人组队，奖品是一块现场颁发的 5090 GPU。我们很期待看到你能想出什么点子来扩展 `world_engine`，这应该是一个结识志同道合的创始人、工程师、黑客和投资者的绝佳活动。我们希望你能在太平洋时间 1 月 20 日上午 10 点加入我们，进行 8 小时的友好竞赛！

- 网站
- Discord（开发者）
- Discord（模型/玩家）
- X/Twitter

来自我们博客的更多文章

![](/images/posts/7e9901eeab7a.png)

## Transformers v5：为 AI 生态系统提供动力的简单模型定义

- 
- 
- 
- 
- 

![](/images/posts/fb71dc93d9af.jpg)

![](/images/posts/ee041adb72f8.jpg)

![](/images/posts/f80373445ed0.jpg)

![](/images/posts/4402b0abc4cd.jpg)

![](/images/posts/32eca1742f7d.png)

## 为开放未来而构建——我们与 Google Cloud 的新合作伙伴关系

- 
- 
- 

![](/images/posts/95d1650d88ea.jpg)

![](/images/posts/e449c92fe2b3.jpg)

· 注册或登录以发表评论

- 
- 
- 
- 
- 

![](/images/posts/4241b99076dc.jpg)

![](/images/posts/f20fa9eebbef.jpg)

![](/images/posts/cf46f3f2bac8.jpg)

---

> 本文由AI自动翻译，原文链接：[Introducing Waypoint-1: Real-time interactive video diffusion from Overworld](https://huggingface.co/blog/waypoint-1)
> 
> 翻译时间：2026-01-21 04:38
