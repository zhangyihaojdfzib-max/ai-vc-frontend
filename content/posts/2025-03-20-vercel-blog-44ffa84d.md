---
title: xAI Grok模型上线Vercel Marketplace
title_original: xAI joins the Vercel Marketplace  - Vercel
date: '2025-03-20'
source: Vercel Blog
source_url: https://vercel.com/changelog/xai-joins-the-vercel-marketplace
author: ''
summary: xAI的Grok模型现已集成到Vercel Marketplace，开发者可通过免费计划直接在其Vercel项目中调用Grok大语言模型。该集成简化了身份验证和API密钥管理，支持自动配置环境变量，并提供按使用量付费的计费方式。用户可通过AI
  SDK xAI提供程序快速集成，或使用Vercel CLI安装。此外，Vercel还提供了可立即部署的Next.js xAI入门模板，帮助开发者快速上手。
categories:
- AI产品
tags:
- xAI
- Grok模型
- Vercel
- AI集成
- 开发者工具
draft: false
translated_at: '2026-06-01T07:06:30.023459'
---

![](/images/posts/fae720ff8f43.jpg)

![](/images/posts/1b312e6c3dfd.jpg)

xAI 的 Grok 模型现已上线 Vercel Marketplace，让您能够轻松将对话式 AI 集成到 Vercel 项目中。

- 通过 xAI 的免费计划开始使用——无需通过 Marketplace 额外注册
- 直接从您的 Vercel 项目访问 Grok 的大语言模型（LLM）
- 通过自动配置的环境变量简化身份验证和 API 密钥管理
- 通过 Vercel 的集成计费，仅按使用量付费

通过 xAI 的免费计划开始使用——无需通过 Marketplace 额外注册

直接从您的 Vercel 项目访问 Grok 的大语言模型（LLM）

通过自动配置的环境变量简化身份验证和 API 密钥管理

通过 Vercel 的集成计费，仅按使用量付费

要开始使用，您可以在项目中采用 AI SDK xAI 提供程序：

```
1import { xai } from "@ai-sdk/xai";2import { streamtext } from "ai";3
4const result = streamText({5  model: xai("grok-2-1212"),6  prompt: "What is the meaning of life?",7});8
9for await (const textPart of result.textStream) {10  process.stdout.write(textPart); 11}
```

然后，通过 Vercel CLI（或从控制台）安装 xAI Marketplace 集成：

```
vercel install xai
```

一旦您接受条款，即可在项目中使用 Grok 模型，无需额外步骤。

为帮助您快速上手，我们还提供了一个可立即部署的 Next.js xAI 入门模板。要了解更多关于 Vercel 上 xAI 的信息，请阅读我们的公告和文档。

---

> 本文由AI自动翻译，原文链接：[xAI joins the Vercel Marketplace  - Vercel](https://vercel.com/changelog/xai-joins-the-vercel-marketplace)
> 
> 翻译时间：2026-06-01 07:06
