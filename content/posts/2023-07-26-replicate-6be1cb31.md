---
title: 通过API运行SDXL：Replicate平台指南
title_original: Run SDXL with an API – Replicate blog
date: '2023-07-26'
source: Replicate Blog
source_url: https://replicate.com/blog/run-sdxl-with-an-api
author: ''
summary: 本文介绍了如何在Replicate平台上通过API运行Stability AI推出的SDXL 1.0文生图模型。SDXL相比之前的版本能生成更高质量、更大尺寸且面部更逼真的图像，并支持添加清晰文字。Replicate提供了官方Python、Node.js等客户端库，用户只需注册并获取API
  Token即可一行代码运行模型。文章详细展示了图生图、蒙版重绘、精炼器使用等高级功能，并比较了两种精炼器模式（专家集成与基础图像精炼器）的差异。该服务按秒计费，比自建GPU基础设施更经济。
categories:
- AI产品
tags:
- SDXL
- Replicate
- API
- 文生图
- Stable Diffusion
draft: false
translated_at: '2026-05-16T05:29:19.575960'
---

- Replicate
- 博客

# 通过API运行SDXL

- fofr

SDXL 1.0 是 Stability AI 推出的全新文生图模型。Stable Diffusion XL 让您能够创建更优质、尺寸更大且面部更逼真的图像。只需简短的提示词，您就可以为图像添加清晰可读的文字，并创作出精美的艺术作品。

与 Stable Diffusion 1.5 和 2.1 一样，SDXL 是开源的。您可以对其进行修改、基于它构建应用，并将其用于商业用途。

Replicate 让您能够从自己的代码中运行 SDXL 等生成式 AI 模型，而无需搭建任何基础设施。

![一位宇航员骑着一只独角兽](/images/posts/c7153cebc6ab.png)

## 您可以做什么

您可以在 Replicate 上使用 SDXL 模型来：

- 根据提示词生成图像
- 根据另一张图像生成图像（图生图）
- 使用蒙版进行局部重绘
- 使用精炼器为图像添加精细细节

查看示例

## 使用 Replicate 的客户端库

我们为 Replicate 维护了官方的 Python、Node.js、Swift 和 Go 客户端。社区也贡献了更多客户端。

您需要注册 Replicate，然后在您的账户页面找到 API Token。

然后，您只需一行代码即可运行 SDXL：

```
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const output = await replicate.run(
  "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
  {
    input: {
      prompt: "一位宇航员骑着一只彩虹独角兽"
    }
  }
);
```

您可以免费使用 API 一段时间，但最终我们会要求您输入信用卡信息。我们仅根据请求运行的时间按秒计费，因此这比运行自己的 GPU 要便宜得多。

## 精炼器

您可以使用精炼器为图像添加精细细节。

精炼器是随 SDXL 发布的全新模型，其训练方式不同，尤其擅长为图像添加细节。它与基础模型协同工作，修正差异并提升图像的整体质量。

您可以通过两种方式使用精炼器：

1. 作为“专家集成”
2. 作为基础模型完成后的额外步骤

在此示例中，使用“专家集成”模式时，SDXL 基础模型将处理生成过程的前 80%（0.8），然后将任务交给精炼器，由其为最后 20% 添加精细细节：

```
const output = await replicate.run(
  "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
  {
    input: {
      prompt: '一只猫的工作室肖像照',
      negative_prompt: '丑陋、柔和、模糊、失焦、低质量、花哨、扭曲、畸形',
      width: 1024,
      height: 1024,
      num_inference_steps: 50,
      scheduler: 'DDIM',
      guidance_scale: 7.5,
      refine: 'expert_ensemble_refiner',
      high_noise_frac: '0.8'
    }
  }
);
```

或者，您也可以使用“基础图像精炼器”模式，在基础模型之后运行精炼器模型。

在此示例中，基础模型将运行 50 步并生成输出。该输出将传递给精炼器，精炼器再额外运行 20 步：

```
const output = await replicate.run(
  "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
  {
    input: {
      prompt: '一只猫的工作室肖像照',
      negative_prompt: '丑陋、柔和、模糊、失焦、低质量、花哨、扭曲、畸形',
      width: 1024,
      height: 1024,
      num_inference_steps: 50,
      scheduler: 'DDIM',
      guidance_scale: 7.5,
      refine: 'base_image_refiner',
      refine_steps: '20'
    }
  }
);
```

对比效果：

- 左：未使用精炼器的基础模型
- 中：基础模型加精炼器
- 右：专家集成精炼器

![使用 SDXL 精炼器的猫图像对比](/images/posts/1894dd287d69.webp)

## 图生图

您可以向模型传递一张图像，基于该图像创建新图像。更改 `prompt_strength` 可以控制保留原始图像的程度。`0.6` 到 `0.8` 是一个不错的起始范围。

查看图生图示例

```
const output = await replicate.run(
  "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
  {
    input: {
      prompt: '一只彩虹色的老虎',
      negative_prompt: '丑陋、柔和、模糊、失焦、低质量、花哨、扭曲、畸形',
      image: 'https://replicate.delivery/pbxt/JF3foGR90vm9BXSEXNaYkaeVKHYbJPinmpbMFvRtlDpH4MMk/out-0-1.png',
      prompt_strength: 0.8,
      width: 1024,
      height: 1024,
      num_inference_steps: 50,
      scheduler: 'DDIM',
      guidance_scale: 7.5,
      refine: 'base_image_refiner',
      refine_steps: '20'
    }
  }
);
```

![一只彩虹色的老虎](/images/posts/5d7b89030ee8.png)

## 局部重绘

您可以在提示词和图像中包含一个 `mask`，以控制输入图像中哪些部分将被更新。使用黑白蒙版，其中黑色像素将被保留，白色像素将被更新。

查看局部重绘示例

```
const output = await replicate.run(
  "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
  {
    input: {
      prompt: '一只彩虹色的熊',
      negative_prompt: '丑陋、柔和、模糊、失焦、低质量、花哨、扭曲、畸形',
      image: 'https://replicate.delivery/pbxt/JF3foGR90vm9BXSEXNaYkaeVKHYbJPinmpbMFvRtlDpH4MMk/out-0-1.png',
      mask: 'https://replicate.delivery/pbxt/JFIZFfJsSnWgxbTmEYLqhHIGdZo9o2BX3p47wSdn55HWtMON/mask1.png',
      prompt_strength: 0.95,
      width: 1024,
      height: 1024,
      num_inference_steps: 50,
      scheduler: 'DDIM',
      guidance_scale: 7.5,
      refine: 'base_image_refiner',
      refine_steps: '20'
    }
  }
);
```

![一只彩虹色的熊](/images/posts/755a0e8c7bd0.png)

## 保持联系

关注我们的 Twitter 以获取更多 SDXL 更新。

加入我们的 Discord，向我们展示您的作品，或寻求帮助。

祝您编程愉快！✨

---

> 本文由AI自动翻译，原文链接：[Run SDXL with an API – Replicate blog](https://replicate.com/blog/run-sdxl-with-an-api)
> 
> 翻译时间：2026-05-16 05:29
