---
title: Recraft V4文生图模型正式登陆AI Gateway
title_original: Recraft V4 on AI Gateway - Vercel
date: '2026-02-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/recraft-v4-on-ai-gateway
author: ''
summary: Recraft V4是一款专为专业设计与营销场景打造的文生图模型，现已集成至Vercel的AI Gateway。V4版本在职业设计师参与下研发，显著提升了照片真实感，改善了肌肤质感与纹理细节，并减少了合成痕迹。模型提供标准版V4与专业版V4
  Pro两个版本，分别针对日常迭代与高分辨率印刷级素材等不同场景。AI Gateway为此提供了统一的API接口，支持成本追踪、故障转移与性能优化，保障了服务稳定性与连续性。
categories:
- AI产品
tags:
- 文生图
- AI Gateway
- Vercel
- 设计工具
- AIGC
draft: false
translated_at: '2026-02-18T04:36:34.378393'
---

Recraft V4 现已登陆 AI Gateway。

作为专为专业设计与营销场景打造的文生图模型，V4 版本在职业设计师的参与下研发而成。该模型在照片真实感方面显著提升，呈现更真实的肌肤质感、自然的纹理细节，并减少合成痕迹。其生成的图像具备干净的光影效果与多样化的构图。在插画领域，该模型能够生成原创角色，并运用更具意外感的色彩组合。

提供两个版本：

- V4：速度更快、成本更优，适合日常工作和迭代
- V4 Pro：生成更高分辨率图像，适用于印刷级素材及大规模应用场景

V4：速度更快、成本更优，适合日常工作和迭代

V4 Pro：生成更高分辨率图像，适用于印刷级素材及大规模应用场景

使用该模型时，请在 AI SDK 中将模型参数设置为 `recraft/recraft-v4-pro` 或 `recraft/recraft-v4`：

```
1import { generateImage } from 'ai';2
3const result = await generateImage({4  model: 'recraft/recraft-v4',5  prompt:6    `Product photo of a ceramic coffee mug on a wooden table,7     morning light, shallow depth of field.`,8});
```

AI Gateway 提供统一 API 接口，支持模型调用、用量与成本追踪，并可配置重试机制、故障转移及性能优化方案，实现高于供应商标准的运行稳定性。平台内置可观测性功能，支持自带密钥（Bring Your Own Key），并通过智能供应商路由与自动重试机制保障服务连续性。

了解更多关于[AI Gateway](https://example.com)的信息，查看[AI Gateway 模型排行榜](https://example.com/leaderboard)或在我们的[模型体验平台](https://example.com/playground)进行试用。

---

> 本文由AI自动翻译，原文链接：[Recraft V4 on AI Gateway - Vercel](https://vercel.com/changelog/recraft-v4-on-ai-gateway)
> 
> 翻译时间：2026-02-18 04:36
