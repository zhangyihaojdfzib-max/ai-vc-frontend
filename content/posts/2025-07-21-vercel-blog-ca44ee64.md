---
title: Vercel AI Gateway 现已支持 OpenAI 兼容 API 端点
title_original: OpenAI-compatible API endpoints now supported in AI Gateway - Vercel
date: '2025-07-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/openai-compatible-api-endpoints-now-supported-in-ai-gateway
author: ''
summary: Vercel AI Gateway 宣布支持与 OpenAI 兼容的 API 端点，开发者无需重写现有代码，只需更改基础 URL 即可通过其熟悉的
  OpenAI 客户端库和工具连接 AI Gateway。这一功能允许用户继续使用现有工作流，同时借助 AI Gateway 的提供商故障转移、提升的运行时间、每分钟
  Token 处理量、配额和可靠性以及增强的可观测性，轻松访问数百个 AI 模型。文章提供了具体的代码示例，并引导读者查阅相关文档了解更多细节。
categories:
- AI基础设施
tags:
- Vercel
- AI Gateway
- API 兼容性
- 开发者工具
- 模型部署
draft: false
translated_at: '2026-04-13T05:00:23.414420'
---

现在，您只需通过简单的URL更改，即可使用与OpenAI兼容的客户端库和工具连接AI Gateway，从而无需重写代码即可访问数百个模型。

以下是一个使用OpenAI客户端库的Python示例：

```
1from openai import OpenAI2
3client = OpenAI(4    api_key='my-ai-gateway-key',5    base_url='https://ai-gateway.vercel.sh/v1'6)7
8stream = client.chat.completions.create(9    model='anthropic/claude-4-sonnet',10    messages=[11        {12            'role': 'user',13            'content': 'Write a one-sentence bedtime story about a unicorn.'14        }15    ],16    stream=True,17)18
19for chunk in stream:20    content = chunk.choices[0].delta.content if chunk.choices[0].delta.content else None21    if content:22        print(content, end='', flush=True)23print()
```

这使得您可以轻松保留现有的工具和工作流程，同时通过AI Gateway的提供商故障转移功能提升运行时间、每分钟Token处理量、配额和可靠性，并增加可观测性。

请在[AI Gateway文档](https://ai-gateway.vercel.sh/v1)中了解更多信息，并在此处查看[更多示例](https://ai-gateway.vercel.sh/v1)。

---

> 本文由AI自动翻译，原文链接：[OpenAI-compatible API endpoints now supported in AI Gateway - Vercel](https://vercel.com/changelog/openai-compatible-api-endpoints-now-supported-in-ai-gateway)
> 
> 翻译时间：2026-04-13 05:00
