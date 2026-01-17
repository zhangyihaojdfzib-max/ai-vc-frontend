---
title: Vercel AI Gateway 现已支持 OpenAI 的 OpenResponses API
title_original: OpenResponses API now supported on Vercel AI Gateway - Vercel
date: '2026-01-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/openresponses-api-now-supported-on-vercel-ai-gateway
author: ''
summary: Vercel AI Gateway 宣布成为 OpenAI 开源规范 OpenResponses API 的首发合作伙伴。该 API 为多供应商
  AI 交互提供了统一接口，支持文本生成、流式传输、工具调用、图像输入、推理和供应商回退等功能。开发者可通过 Vercel AI Gateway 使用单一密钥和端点，灵活调用不同供应商的模型，并通过简单的模型字符串切换来实现复杂场景，如工具调用。这简化了多模型集成的开发流程，提升了应用的可靠性和灵活性。
categories:
- AI基础设施
tags:
- Vercel
- OpenAI
- AI Gateway
- API
- 多模型集成
draft: false
translated_at: '2026-01-17T04:16:26.174488'
---

Vercel AI Gateway 是 OpenResponses API 的首发合作伙伴，该 API 是 OpenAI 推出的用于多供应商 AI 交互的开源规范。

OpenResponses 为文本生成、流式传输、工具调用、图像输入和跨供应商的推理提供了一个统一的接口。

AI Gateway 支持 OpenResponses 的以下功能：

- **文本生成**：发送消息并从任何支持的模型接收响应。
- **流式传输**：通过服务器发送事件，在 Token 生成时实时接收。
- **工具调用**：定义可由模型通过结构化参数调用的函数。
- **图像输入**：向具备视觉能力的模型发送图像和文本。
- **推理**：通过可配置的思考强度，启用扩展思考。
- **供应商回退**：配置跨模型和供应商的自动回退链。

**文本生成**：发送消息并从任何支持的模型接收响应。

**流式传输**：通过服务器发送事件，在 Token 生成时实时接收。

**工具调用**：定义可由模型通过结构化参数调用的函数。

**图像输入**：向具备视觉能力的模型发送图像和文本。

**推理**：通过可配置的思考强度，启用扩展思考。

**供应商回退**：配置跨模型和供应商的自动回退链。

使用您的 AI Gateway 密钥调用 OpenResponses，并通过更改模型字符串来切换不同供应商的模型。

```
1const response = await fetch('https://ai-gateway.vercel.sh/v1/responses', {2  method: 'POST',3  headers: {4    'Content-Type': 'application/json',5    Authorization: `Bearer ${process.env.VERCEL_AI_GATEWAY_KEY}`,6  },7  body: JSON.stringify({8    model: 'anthropic/claude-sonnet-4.5',9    input: [10      {11        type: 'message',12        role: 'user',13        content: 'Explain quantum computing in one sentence.',14      }15    ],16  }),17});
```

您也可以将 OpenResponses 用于更复杂的场景，例如工具调用。

```
1const response = await fetch('https://ai-gateway.vercel.sh/v1/responses', {2  method: 'POST',3  headers: {4    'Content-Type': 'application/json',5    Authorization: `Bearer ${process.env.VERCEL_AI_GATEWAY_KEY}`,6  },7  body: JSON.stringify({8    model: 'zai/glm-4.7',9    input: [{ type: 'message', role: 'user', content: 'What is the weather in SF?' }],10    tools: [{11      type: 'function',12      name: 'get_weather',13      description: 'Get current weather for a location',14      parameters: {15        type: 'object',16        properties: { location: { type: 'string' } },17        required: ['location'],18      },19    }],20  }),21});
```

阅读 [OpenResponses API 文档](https://sdk.vercel.ai/docs/ai-gateway/providers/openresponses) 或 [查看规范](https://github.com/openai/openresponses)。

---

> 本文由AI自动翻译，原文链接：[OpenResponses API now supported on Vercel AI Gateway - Vercel](https://vercel.com/changelog/openresponses-api-now-supported-on-vercel-ai-gateway)
> 
> 翻译时间：2026-01-17 04:16
