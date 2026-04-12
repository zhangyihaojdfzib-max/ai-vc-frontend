---
title: 利用Vercel v0平台API构建你自己的AI应用生成器
title_original: Build your own AI app builder with the v0 Platform API - Vercel
date: '2025-07-23'
source: Vercel Blog
source_url: https://vercel.com/blog/build-your-own-ai-app-builder-with-the-v0-platform-api
author: ''
summary: 本文介绍了Vercel推出的v0平台API，这是一个处于测试阶段的文本到应用REST接口，允许开发者通过编程方式访问其AI驱动的应用生成流水线。文章详细说明了API的功能，包括根据自然语言提示生成全栈Web应用、集成自有文件上下文、管理项目与部署等。通过提供的TypeScript
  SDK，开发者可以轻松将AI代码生成能力集成到自己的应用程序中，用于构建网站生成器、聊天机器人、开发工具插件等多种创新产品。
categories:
- AI基础设施
tags:
- Vercel
- 低代码/无代码
- AI代码生成
- 开发者工具
- Web开发
draft: false
translated_at: '2026-04-12T04:52:17.761282'
---

了解如何通过编程方式访问 v0 的应用生成流水线，来构建、扩展和自动化 AI 生成的应用。

v0 平台 API 是一个文本到应用的 API，它让开发者能够直接访问驱动 v0.dev 的相同基础设施。

该平台 API 目前处于 **测试阶段**，它向开发者提供了一个可组合的接口，用于自动化构建 Web 应用、将代码生成集成到现有功能中，以及在 LLM（大语言模型）生成的 UI 之上构建新产品。

## v0 平台 API 是什么？

平台 API 是一个 REST 接口，它封装了 v0 完整的代码生成生命周期：提示词 → 项目 → 代码文件 → 部署。通过平台 API 构建的每个应用都对应一个 v0.dev 聊天链接。

它包含了 v0.dev 上几乎所有的功能端点：

*   **自然语言应用生成**：根据自然语言提示生成全栈 Web 应用，并返回解析后的代码文件和一个实时演示 URL。
*   **自带上下文**：使用您自己的文件（来自源代码、git 或 shadcn 注册表）开始聊天，或在单个消息中包含附件。
*   **项目与部署**：创建新的 Vercel 项目，将 Vercel 项目链接到聊天，并触发部署。

## 如何使用 v0 平台 API

v0 SDK 是一个 TypeScript 库，它简化了与 v0 平台 API 的交互。

```
1pnpm install v0-sdk
```

从您的 v0 账户设置中获取 API 密钥，并将其设置为环境变量：

```
1V0_API_KEY=your_api_key_here
```

现在，您可以将 v0 的 AI 驱动代码生成集成到您的应用程序中。在我们的完整快速入门指南中了解更多信息。

```
1import { v0 } from "v0-sdk"2
3export default async function V0Chat() {  4  5  const chat = await v0.chats.create({6    message: "Build a todo app with React and TypeScript"7  })8
9  10  chat.files?.forEach((file) => {11    console.log(`File: ${file.name}`)12    console.log(`Content: ${file.content}`)13  })14
15  16  return (17    <iframe18      src={chat.demo}19      width="100%"20      height="600">21    </iframe>22  )23}24

```

## 您能用平台 API 构建什么？

平台 API 将 v0 转变为一个无头应用构建器。开发者们已经在用它来驱动：

*   **网站构建器**：用户描述一个网站，即可获得可用于生产的代码。
*   **Slack 和 Discord 机器人**：返回已部署的 Web 应用程序。
*   **VSCode 插件和 CLI**：围绕从提示词到应用的工作流进行构建。
*   **分析或 CRM 工具中的嵌入式流程**：根据自然语言生成 UI 组件。
*   **自定义开发环境和智能体**：读取用户意图并返回带有演示链接的实时应用。

## 开始使用

查看 v0 平台 API 模板，这是一个 Next.js 应用程序，演示了 v0 平台 API 及其功能，如项目管理、聊天记录和带实时预览的实时应用生成。

*   Vercel 模板
*   v0 模板
*   GitHub 仓库

---

> 本文由AI自动翻译，原文链接：[Build your own AI app builder with the v0 Platform API - Vercel](https://vercel.com/blog/build-your-own-ai-app-builder-with-the-v0-platform-api)
> 
> 翻译时间：2026-04-12 04:52
