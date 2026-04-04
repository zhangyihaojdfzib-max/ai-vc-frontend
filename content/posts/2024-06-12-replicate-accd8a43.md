---
title: 通过Replicate API运行Stable Diffusion 3教程
title_original: Run Stable Diffusion 3 with an API – Replicate blog
date: '2024-06-12'
source: Replicate Blog
source_url: https://replicate.com/blog/run-stable-diffusion-3-with-an-api
author: ''
summary: 本文介绍了如何通过Replicate平台提供的API运行Stable Diffusion 3文生图模型。文章首先推荐使用API游乐场快速体验模型能力，随后详细讲解了使用JavaScript、Python和cURL三种方式调用SD3
  API的具体步骤，包括安装客户端库、设置API令牌和运行示例代码。Replicate使得用户无需复杂部署即可便捷使用最新AI图像生成模型。
categories:
- AI产品
tags:
- Stable Diffusion 3
- Replicate
- API调用
- 文生图
- AI开发
draft: false
translated_at: '2026-04-04T04:28:43.323392'
---

-   Replicate
-   博客

# 通过 API 运行 Stable Diffusion 3

-   cbh123

Stable Diffusion 3 是 Stability AI 发布的最新文生图模型。它在图像质量、文字排版、复杂提示词理解以及资源效率方面均有显著提升。

通过 Replicate，您只需一行代码即可运行 Stable Diffusion 3。

## 在我们的 API 游乐场中尝试 Stable Diffusion 3

在深入使用之前，您可以在我们的 API 游乐场中先体验一下 Stable Diffusion 3。

尝试调整提示词，观察 Stable Diffusion 3 如何响应。Replicate 上的大多数模型都提供类似的交互式 API 游乐场，您可以在模型页面找到它：https://replicate.com/stability-ai/stable-diffusion-3

API 游乐场是了解模型能力的绝佳方式，并提供多种语言的可复制代码片段，帮助您快速上手。

## 使用 JavaScript 运行 Stable Diffusion 3

您可以使用我们的官方 JavaScript 客户端运行 Stable Diffusion 3：

安装 Replicate 的 Node.js 客户端库

```
npm install replicate
```

设置 `REPLICATE_API_TOKEN` 环境变量

```
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

（您可以在账户中生成 API 令牌。请妥善保管。）

导入并设置客户端

```
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});
```

使用 Replicate 的 API 运行 stability-ai/stable-diffusion-3。请查阅模型架构以了解输入和输出的概览。

```
const input = {
  prompt: "a photo of vibrant artistic graffiti on a wall saying 'SD3 medium'"
};

const output = await replicate.run("stability-ai/stable-diffusion-3", { input });
console.log(output);
```

要了解更多信息，请查看 Node.js 入门指南。

## 使用 Python 运行 Stable Diffusion 3

您可以使用我们的官方 Python 客户端运行 Stable Diffusion 3：

安装 Replicate 的 Python 客户端库

```
pip install replicate
```

```
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

导入客户端

```
import replicate
```

```
output = replicate.run(
    "stability-ai/stable-diffusion-3",
    input={
        "prompt": "a photo of vibrant artistic graffiti on a wall saying 'SD3 medium'"
    }
)
print(output)
```

要了解更多信息，请查看 Python 入门指南。

## 使用 cURL 运行 Stable Diffusion 3

您也可以直接使用 cURL 等工具调用 HTTP API：

```
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

```
curl -s -X POST\
  -H "Authorization: Bearer $REPLICATE_API_TOKEN"\
  -H "Content-Type: application/json"\
  -H "Prefer: wait"\
  -d $'{
    "input": {
      "prompt": "a photo of vibrant artistic graffiti on a wall saying \'SD3 medium\'"
    }
  }'\
  https://api.replicate.com/v1/models/stability-ai/stable-diffusion-3/predictions
```

要了解更多信息，请查看 Replicate 的 HTTP API 参考文档。

您也可以使用 Replicate 为 Go、Swift 等语言提供的其他客户端库来运行 Stable Diffusion 3。

## 保持关注

-   在 Twitter/X 上关注我们。
-   加入我们的 Discord 讨论 SD3。

祝您探索愉快！🦙

---

> 本文由AI自动翻译，原文链接：[Run Stable Diffusion 3 with an API – Replicate blog](https://replicate.com/blog/run-stable-diffusion-3-with-an-api)
> 
> 翻译时间：2026-04-04 04:28
