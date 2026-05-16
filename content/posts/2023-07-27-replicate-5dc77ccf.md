---
title: 用API轻松运行Llama 2模型
title_original: Run Llama 2 with an API – Replicate blog
date: '2023-07-27'
source: Replicate Blog
source_url: https://replicate.com/blog/run-llama-2-with-an-api
author: ''
summary: 本文介绍了如何通过Replicate平台使用API运行Meta AI推出的开源语言模型Llama 2。文章提供了JavaScript、Python和cURL三种语言的代码示例，详细说明了四种模型变体（70B聊天版、70B基础版、13B聊天版和7B聊天版）的适用场景，并提及了示例聊天应用、模型微调及本地运行等扩展功能。
categories:
- AI产品
tags:
- Llama 2
- API
- Replicate
- 开源模型
- 模型部署
draft: false
translated_at: '2026-05-16T05:29:03.516933'
---

- Replicate
- 博客

# 使用 API 运行 Llama 2

- joehoover

Llama 2 是 Meta AI 推出的语言模型。它是首个与 OpenAI 模型水平相当的开源语言模型。

借助 Replicate，您只需一行代码即可在云端运行 Llama 2。

## 目录

- 目录
- 使用 JavaScript 运行 Llama 2
- 使用 Python 运行 Llama 2
- 使用 cURL 运行 Llama 2
- 选择使用哪个模型
- 示例聊天应用
- 微调 Llama 2
- 本地运行 Llama 2
- 保持关注

## 使用 JavaScript 运行 Llama 2

您可以使用我们的官方 JavaScript 客户端运行 Llama 2：

```
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const input = {
  prompt:
    "以玛丽·奥利弗的风格写一首关于开源机器学习的诗。",
};

for await (const event of replicate.stream("meta/llama-2-70b-chat", {
  input,
})) {
  process.stdout.write(event.toString());
}
```

## 使用 Python 运行 Llama 2

您可以使用我们的官方 Python 客户端运行 Llama 2：

```
import replicate
# meta/llama-2-70b-chat 模型可以在运行时流式输出结果。
for event in replicate.stream(
    "meta/llama-2-70b-chat",
    input={
        "prompt": "以玛丽·奥利弗的风格写一首关于开源机器学习的诗。"
    },
):
    print(str(event), end="")
```

## 使用 cURL 运行 Llama 2

您可以使用 cURL 等工具直接调用 HTTP API：

```
curl -s -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait" \
  -d $'{
    "input": {
      "prompt": "写一首诗..."
    }
  }' \
  https://api.replicate.com/v1/models/meta/llama-2-70b-chat/predictions
```

您还可以使用其他 Replicate 客户端库（适用于 Go、Swift 等）运行 Llama。

## 选择使用哪个模型

Replicate 上有四种 Llama 2 模型变体，各有优势：

- meta/llama-2-70b-chat：700 亿参数模型，针对聊天补全进行了微调。如果您想构建准确度最高的聊天机器人，这是最佳选择。
- meta/llama-2-70b：700 亿参数基础模型。如果您想进行其他类型的语言补全（如补全用户的写作），请使用此模型。
- meta/llama-2-13b-chat：130 亿参数模型，针对聊天补全进行了微调。如果您正在构建聊天机器人，并且希望以牺牲准确度为代价获得更快的速度和更低的成本，请使用此模型。
- meta/llama-2-7b-chat：70 亿参数模型，针对聊天补全进行了微调。这是更小、更快的模型。

这些模型有什么区别？在我们的博客文章《比较 7B、13B 和 70B》中了解更多信息。

## 示例聊天应用

如果您需要一个起点，我们构建了一个基于 Next.js 的演示聊天应用，可部署在 Vercel 上：

查看 GitHub README，了解如何自定义和部署它。

## 微调 Llama 2

由于 Llama 2 是开源的，您可以在更多数据上训练它，以学习新知识或掌握特定风格。

Replicate 让这变得简单。请查看我们的微调 Llama 2 指南。

## 本地运行 Llama 2

您也可以在没有网络连接的情况下运行 Llama 2。我们编写了一份全面的指南，介绍如何在 M1/M2 Mac、Windows、Linux 甚至手机上运行 Llama。

## 保持关注

- 在 Twitter/X 上关注我们，获取 Llama 世界的最新动态。
- 加入我们的 Discord，讨论 Llama。

祝编码愉快！🦙

---

> 本文由AI自动翻译，原文链接：[Run Llama 2 with an API – Replicate blog](https://replicate.com/blog/run-llama-2-with-an-api)
> 
> 翻译时间：2026-05-16 05:29
