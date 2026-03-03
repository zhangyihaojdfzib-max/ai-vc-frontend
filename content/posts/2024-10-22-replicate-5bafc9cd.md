---
title: Ideogram v2：一款出色的新型图像修复模型现已登陆Replicate
title_original: Ideogram v2 is an outstanding new inpainting model – Replicate blog
date: '2024-10-22'
source: Replicate Blog
source_url: https://replicate.com/blog/ideogram-v2-inpainting
author: ''
summary: 本文介绍了Ideogram v2图像修复模型的发布及其在Replicate平台上的集成。该模型提供标准版和Turbo版两个版本，不仅擅长图像修复，还能生成包含文本在内的各类图像。文章提供了使用Replicate
  API调用模型的代码示例，并分享了获得最佳修复效果的技巧，如描述整个场景或仅聚焦修复区域。此外，还提及了相关的开源演示应用和潜在用例。
categories:
- AI产品
tags:
- 图像生成
- 图像修复
- Ideogram
- Replicate
- AI模型
draft: false
translated_at: '2026-03-03T04:46:37.378724'
---

- Replicate
- 博客

# Ideogram v2 是一款出色的新型图像修复模型

- andreasjansson

2025年5月更新：Ideogram 已发布其 v3 系列模型，包括 Turbo、Balanced 和 Quality 变体。在此处阅读更多关于 Ideogram v3 的信息。

![](/images/posts/9422e5ee3fad.png)

今天，Ideogram 正在为其 Ideogram v2 模型推出新的图像修复功能。我们非常高兴能与 Ideogram 合作，将 Ideogram v2 引入 Replicate 的 API。这款模型的质量令我们惊叹不已。它真的非常出色。

Ideogram v2 提供两种版本：

- ideogram-ai/ideogram-v2 - 提供最佳的图像质量。
- ideogram-ai/ideogram-v2-turbo - 质量依然很高，但速度更快。

例如，这里有一群恐龙正在《田园绿山》上吃草：

![](/images/posts/98c0c23582b2.png)

Ideogram v2 不仅限于图像修复：你可以用它来生成任何类型的图像。在我们的测试中，我们发现它特别擅长生成文本。

## 在 Replicate 上通过 API 运行 Ideogram v2

要使用 Replicate Python 客户端进行图像修复，请运行：

```
import replicate
from pathlib import Path

output = replicate.run(
    "ideogram-ai/ideogram-v2",
    input={
        "prompt": "Dinosaurs grazing on a hill",
        "image": Path("desktop.png"),
        "mask": Path("desktop-mask.png")
    }
)
print(output.url)
```

或者在 JavaScript 中：

```
import Replicate from "replicate";
import fs from "node:fs";
import path from "node:path";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const image = fs.readFileSync(path.resolve(__dirname, "desktop.png"));
const mask = fs.readFileSync(path.resolve(__dirname, "desktop-mask.png"));

const output = await replicate.run("ideogram-ai/ideogram-v2", {
  input: {
    prompt: "Dinosaurs grazing on a hill",
    image,
    mask,
  },
});

console.log(output.url());
```

## 实时演示

我们更新了开源的 inpainter.app 演示，以使用 Ideogram v2。

你可以在浏览器中实时试用这个图像修复工具。输入提示词开始，然后用鼠标绘制来遮盖图像的部分区域。接着输入新的提示词并点击提交。

## 获得最佳图像修复效果

以下是一些技巧和窍门。效果可能因人而异！

- 根据经验，当“魔法提示词”功能关闭时，你应该尝试描述整个场景，而不仅仅是修复区域。
- 当“魔法提示词”功能开启时，模型会根据原始提示词和图像尝试重写你的提示词，因此你不一定需要描述整个图像。
- 如果你只描述修复区域，模型会更侧重于你的提示词，这可能会产生更好的效果。

## 后续步骤

图像修复有很多有趣的应用。你可以复制字体、在房间中放置物体、为游戏生成精灵图等等。

查看这些示例项目：

- Inpainter - 用于图像修复的开源 Next.js 应用。
- Outpainter - 用于将图像扩展到原始画布之外的开源 Nuxt.js 应用。

请在 X 或 Discord 上告诉我们你构建了什么。

---

> 本文由AI自动翻译，原文链接：[Ideogram v2 is an outstanding new inpainting model – Replicate blog](https://replicate.com/blog/ideogram-v2-inpainting)
> 
> 翻译时间：2026-03-03 04:46
