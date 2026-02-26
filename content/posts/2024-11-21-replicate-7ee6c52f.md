---
title: FLUX.1工具集发布：为文生图模型新增四大控制功能
title_original: FLUX.1 Tools – Control and steerability for FLUX – Replicate blog
date: '2024-11-21'
source: Replicate Blog
source_url: https://replicate.com/blog/flux-tools
author: ''
summary: Black Forest Labs团队推出FLUX.1工具集，为其FLUX文生图模型新增了四项控制与引导功能。该工具集包括：填充（图像修复与外绘）、Canny（基于边缘检测生成结构精确的图像）、深度（利用深度图生成真实透视感图像）以及Redux（为FLUX.1基础模型生成图像变体的适配器）。这些新模型已上线Replicate平台，其中填充功能在文本修复方面表现突出，能精准替换图像中的文字并匹配原风格。工具集进一步增强了用户对AI图像生成过程的控制能力。
categories:
- AI产品
tags:
- 文生图
- AI图像生成
- FLUX模型
- ControlNet
- Replicate
draft: false
translated_at: '2026-02-26T04:32:34.618829'
---

- Replicate
- 博客

# FLUX.1 工具集——为FLUX增添控制与引导能力

- zeke
- fofr

![](/images/posts/3cc298e6ba4c.webp)

![](/images/posts/e840569f0b57.webp)

![](/images/posts/9bb542efcb1d.webp)

Black Forest Labs团队携FLUX.1工具集回归，这是一套为其FLUX文生图模型新增控制与引导能力的新模型系列。

FLUX.1工具集包含四项新功能：

- **填充**：图像修复与外绘，如同精准编辑的AI魔法画笔。
- **Canny**：利用边缘检测生成具有精确结构的图像。
- **深度**：利用深度图生成具有真实透视感的图像。
- **Redux**：适用于FLUX.1基础模型的适配器，可用于创建图像变体。

所有这些新功能均适用于FLUX.1 [dev]和FLUX.1 [pro]模型，其中Redux也适用于FLUX.1 [schnell]模型。所有这些模型现已在Replicate平台上线。

## FLUX填充功能擅长文本修复

最令人兴奋的新功能之一是FLUX填充的文本修复能力。只需遮盖想要更改的文本，并通过提示词输入新文字。FLUX填充将修复该文本，同时匹配原始图像的风格。

在此示例中，我们使用FLUX填充快速将文本“FLUX Dev”更改为“Fill Dev”。我们遮盖了“FLUX”一词，使用的提示词是：

a photo of misty woods with the text “FILL DEV”

效果立竿见影。

![FLUX填充功能示例](/images/posts/456da4906a3b.webp)

## 所有新模型

**FLUX.1 [dev] 模型：**
- FLUX.1 填充 [dev]
- FLUX.1 Canny [dev]
- FLUX.1 深度 [dev]
- FLUX.1 Redux [dev]

**FLUX.1 [pro] 模型：**
- FLUX.1 填充 [pro]
- FLUX.1 Canny [pro]
- FLUX.1 深度 [pro]

**FLUX.1 [schnell] 模型：**
- FLUX.1 Redux [schnell]

## FLUX Redux

您可以使用FLUX Redux生成图像的变体。当您输入一张图像时，它会生成一个具有细微差别的新版本，同时保留原始图像的核心元素。

您还可以通过添加文本提示词来自定义输出，从而对现有图像进行创造性的风格重塑。

Redux作为独立模型适用于FLUX.1 [dev]和FLUX.1 [schnell]，并将很快作为新功能在pro、pro 1.1和pro 1.1 ultra模型上提供。

![FLUX Redux修改“分心男友”表情包的示例](/images/posts/bade4be11721.webp)

## 什么是ControlNet？

ControlNet是一个开源工具，允许您使用“条件图像”来引导图像生成模型。

结合文本提示词，条件图像引导模型产生特定结果，例如复制轮廓的结构或场景的深度，同时仍允许生成细节的创造性发挥。

## 什么是ControlNet Canny？

![ControlNet Canny示例](/images/posts/da2e1ab65cc2.webp)

Canny方法是一种检测图像边缘的技术。它将图片简化为显示物体形状的线条和边界。ControlNet可以将这些边缘用作条件图像，以确保生成的输出与提供的结构或轮廓相匹配。Canny边缘检测非常适合将草图或轮廓转化为丰满、细节丰富的图像。您也可以使用Canny边缘检测来保留现有图像的边缘，同时生成该图像的新变体。

## 什么是ControlNet深度？

![ControlNet深度示例](/images/posts/22ac860b8e22.webp)

深度图是一种视觉表示，其中较暗和较亮的区域显示图像各部分的远近。ControlNet可以使用深度图来引导模型生成具有真实透视感的图像，确保输出中物体的排列和大小正确。

## 延伸阅读

要了解更多信息，请查看我们的ControlNet指南。

---

> 本文由AI自动翻译，原文链接：[FLUX.1 Tools – Control and steerability for FLUX – Replicate blog](https://replicate.com/blog/flux-tools)
> 
> 翻译时间：2026-02-26 04:32
