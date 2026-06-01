---
title: AI SDK 4.2发布：推理与MCP客户端等新特性
title_original: AI SDK 4.2
date: '2025-03-21'
source: Vercel Blog
source_url: https://vercel.com/blog/ai-sdk-4-2
author: ''
summary: AI SDK 4.2版本正式发布，带来多项重要更新。新版本支持推理模型（如Anthropic Sonnet 3.7和DeepSeek R1），可访问模型的推理Token，并通过中间件实现跨提供商一致体验。新增模型上下文协议（MCP）客户端，支持通过stdio或SSE连接数百个预构建工具（如GitHub、Slack），扩展应用功能。此外，还引入useChat消息片段、语言模型图像生成、URL来源、OpenAI
  Responses API、Svelte 5支持及中间件更新。该SDK每周下载量超100万次，助力开发者构建AI驱动应用。
categories:
- AI基础设施
tags:
- AI SDK
- 推理模型
- MCP客户端
- JavaScript
- TypeScript
draft: false
translated_at: '2026-06-01T06:55:18.209795'
---

推出MCP客户端、推理功能及来源等新特性。

AI SDK是一套开源工具包，用于使用JavaScript和TypeScript构建AI应用程序。其统一的提供商API允许您使用任何语言模型，并支持与Next.js和Svelte等主流Web框架进行强大的UI集成。

该SDK每周下载量超过100万次，开发者正利用它创建令人惊叹的应用程序，例如AI驱动的研究工具Otto：

今天，我们宣布发布AI SDK 4.2，其中引入了以下功能：

- 推理
- 模型上下文协议（MCP）客户端
- useChat消息片段
- 语言模型图像生成
- URL来源
- OpenAI Responses API
- Svelte 5
- 中间件更新

推理

模型上下文协议（MCP）客户端

useChat消息片段

语言模型图像生成

URL来源

OpenAI Responses API

Svelte 5

中间件更新

让我们来探索这些新功能和改进。

## 链接到标题推理

推理模型——如Anthropic Sonnet 3.7和DeepSeek R1——在推理时投入计算资源，有条不紊地解决问题，很像人类展示其思维链。这种方法比传统模型能产生更准确、更可靠的结果，尤其适用于涉及逻辑或多步骤分析的任务。

AI SDK现在支持主流提供商的推理模型。您可以像使用任何其他模型一样，使用AI SDK调用Anthropic的Claude 3.7 Sonnet等推理模型。您可以通过`reasoning`属性访问模型的推理Token：

```
1import { generateText } from 'ai';2import { anthropic } from '@ai-sdk/anthropic';3
4const { text, reasoning } = await generateText({5  model: anthropic('claude-3-7-sonnet-20250219'),6  prompt: '2040年世界将有多少人口？',7});
```

您可以尝试不同的模型，以找到最适合您应用的方案。只需更改两行代码，即可轻松切换提供商：

```
1import { generateText } from 'ai';2import { bedrock } from '@ai-sdk/amazon-bedrock'; 3
4const { text, reasoning } = await generateText({5  model: bedrock('anthropic.claude-3-7-sonnet-20250219-v1:0'), 6  prompt: '2040年世界将有多少人口？',7});
```

对于将推理作为文本输出的一部分而非单独Token提供的提供商，您可以使用`extractReasoningMiddleware`，它会自动从格式化响应中提取推理内容。这确保了在OpenAI、Anthropic、Groq、Together AI、Azure OpenAI等提供商之间获得一致的体验——无需更改您的应用程序代码。

要查看推理的实际效果，请查看AI SDK推理模板。要了解更多信息，请查看我们的推理文档。

## 链接到标题模型上下文协议（MCP）客户端

AI SDK现在支持模型上下文协议（MCP），这是一种开放标准，可将您的应用程序连接到不断增长的工具和集成生态系统。借助MCP支持，您可以访问数百个预构建的工具（“服务器”），为您的应用程序添加强大的功能。一些流行的MCP服务器包括：

- GitHub - 管理仓库、问题和拉取请求
- Slack - 发送消息并与工作区交互
- 文件系统 - 具有可配置访问控制的安全文件操作

GitHub - 管理仓库、问题和拉取请求

Slack - 发送消息并与工作区交互

文件系统 - 具有可配置访问控制的安全文件操作

由于MCP是一种开放协议，您的用户还可以构建并连接他们自己的自定义MCP服务器，以根据需要扩展您的应用程序功能。MCP有许多用例，但在本地代码自动化方面尤其强大。

该SDK支持通过stdio（用于本地工具）或SSE（用于远程服务器）连接到MCP服务器。连接后，您可以直接在AI SDK中使用MCP工具：

```
1import { experimental_createMCPClient as createMCPClient } from 'ai';2import { openai } from '@ai-sdk/openai';3
4const mcpClient = await createMCPClient({5  transport: {6    type: 'sse',7    url: 'https://my-server.com/sse',8  },9});10
11const response = await generateText({12  model: openai('gpt-4o'),13  tools: await mcpClient.tools(), 14  prompt: '查找价格低于100美元的产品',15});
```

要了解有关在项目中实现MCP的更多信息，请查看我们的MCP工具文档和我们的分步MCP指南。

## 链接到标题useChat消息片段

语言模型产生的不仅仅是文本——它们将推理、来源、工具调用和文本响应组合在一条消息中。对于多步骤的Agent用例，这些不同类型的输出经常混合在单个响应中。

AI SDK 4.2为useChat引入了消息片段，这是一种处理这些不同类型输出的新方法，可以保留它们的确切顺序。

```
1function Chat() {2  const { messages } = useChat();3  return (4    <div>5      {messages.map(message => (6        message.parts.map((part, i) => {7          switch (part.type) {8            case "text": return <p key={i}>{part.text}</p>;9            case "source": return <p key={i}>{part.source.url}</p>;10            case "reasoning": return <div key={i}>{part.reasoning}</div>;11            case "tool-invocation": return <div key={i}>{part.toolInvocation.toolName}</div>;12            case "file": return <img key={i} src={`data:${part.mimeType};base64,${part.data}`} />;13          }14        })15      ))}16    </div>17  );18}
```

我们计划在未来的4.2.x版本中添加更多片段类型。要了解更多信息，请查看我们的4.2迁移指南。

## 链接到标题语言模型图像生成

Google的Gemini 2.0 Flash是第一个能够直接作为响应一部分生成图像的语言模型。AI SDK支持此功能，支持能够生成和理解文本和图像的多模态聊天机器人。

在客户端，您可以通过useChat使用`file`消息片段访问语言模型生成的图像：

```
1import { useChat } from '@ai-sdk/react';2
3export default function Chat() {4  const { messages } = useChat();5
6  return (7    <div>8      {messages.map(message => (9        <div key={message.id}>10          {message.role === 'user' ? '用户: ' : 'AI: '}11          {message.parts.map((part, i) => {12            if (part.type === 'text') {13              return <div key={i}>{part.text}</div>;14            } else if (15              part.type === 'file' &&16              part.mimeType.startsWith('image/')17            ) {18              return (19                <img20                  key={i}21                  src={`data:${part.mimeType};base64,${part.data}`}22                  alt="生成的图像"23                />24              );25            }26          })}27        </div>28      ))}29    </div>30  );31}
```

当图像生成时，它们会像文本消息一样成为您聊天历史的一部分。您可以通过自然对话引用、迭代或“编辑”先前生成的图像——要求模型修改颜色、调整样式或创建变体，同时保持视觉对话的上下文。

要了解更多信息，请查看我们的文件生成文档。

## 链接到标题URL来源

许多提供商（如OpenAI和Google）可以在其响应中包含搜索结果，但每个提供商都实现了自己独特的方式来公开和访问这些来源。AI SDK标准化了URL来源（即网站），允许您构建使用来源归属的AI应用程序。

例如，以下是如何使用Gemini Flash发送来源：

```
1import { google } from "@ai-sdk/google";2import { streamText } from "ai";3
4export async function POST(req: Request) {5  const { messages } = await req.json();6
7  const result = streamText({8    model: google("gemini-1.5-flash", { useSearchGrounding: true }),9    messages,10  });11
12  return result.toDataStreamResponse({13    sendSources: true,14  });15}
```

以下是如何在客户端组件中使用 `useChat` 显示来源：

```
1function Chat() {2  const { messages } = useChat();3  return (4    <div>5      {messages.map((message) => (6        <div key={message.id}>7          {message.role === "user" ? "User: " : "AI: "}8          {message.parts9            .filter((part) => part.type !== "source")10            .map((part, index) => {11              if (part.type === "text") {12                return <div key={index}>{part.text}</div>;13              }14            })}15          {message.parts16            .filter((part) => part.type === "source")17            .map((part) => (18              <span key={`source-${part.source.id}`}>19                [20                <a href={part.source.url} target="_blank">21                  {part.source.title ?? new URL(part.source.url).hostname}22                </a>23                ]24              </span>25            ))}26        </div>27      ))}28    </div>29  );30}
```

AI SDK 支持在兼容模型中使用 URL 来源，包括 OpenAI Responses、Google、Vertex 和 Perplexity。要查看实际来源，请查看 sources 模板。

## Link to headingOpenAI Responses API

OpenAI 最近发布了 Responses API，这是一种在 OpenAI 平台上构建应用程序的全新方式。新 API 提供了持久化聊天历史记录、用于接地 LLM 响应的网络搜索工具，以及将在未来更新中推出的文件搜索和计算机使用等工具。

借助 AI SDK 的即日支持，从现有的 Completions API 迁移到新的 Responses API 非常简单：

```
1import { openai } from '@ai-sdk/openai';2
3const completionsAPIModel = openai('gpt-4o-mini');4const responsesAPIModel = openai.responses('gpt-4o-mini');
```

新的网络搜索工具使模型能够访问互联网获取相关信息，从而提高事实性查询的响应质量：

```
1import { openai } from '@ai-sdk/openai';2import { generateText } from 'ai';3
4const result = await generateText({5  model: openai.responses('gpt-4o-mini'),6  prompt: '上周旧金山发生了什么？',7  tools: {8    web_search_preview: openai.tools.webSearchPreview(),9  },10});11
12console.log(result.text);13console.log(result.sources);
```

Responses API 还简化了对话历史记录的管理。无需在每次请求时发送完整对话，您可以通过 ID 引用之前的交互，从而降低应用程序的复杂性。

要了解更多关于这些功能的信息，请查看 OpenAI Responses API 指南。

## Link to headingSvelte 5

随着 AI SDK 4.2 的发布，`@ai-sdk/svelte` 包已由 Svelte 团队完全重写，以支持 Svelte 5 并正确利用原生模式。

这个新的实现用 Svelte 原生的基于类的模式取代了 React 基于 Hook 的方法：

```
1<script>2  import { Chat } from '@ai-sdk/svelte';3
4  // 使用 Chat 类代替 useChat hook5  const chat = new Chat();6</script>7
8<div>9  {#each chat.messages as message}10    <div class="message {message.role}">{message.content}</div>11  {/each}12</div>
```

要了解更多信息，请查看 Svelte 快速入门指南，或查看实现了这些模式的开源 Svelte 聊天机器人模板。

## Link to heading中间件更新

语言模型中间件现已稳定，是一种通过拦截和修改对语言模型的调用来增强语言模型行为的方式。这种模式支持防护、缓存和日志记录等功能，同时保持提供商的灵活性。中间件通过一个简单的包装函数应用，该函数保留了标准模型接口。

SDK 现在包含三个生产就绪的中间件选项：

- `extractReasoningMiddleware`：从带有特殊标签（如 `<think>`）的文本中提取推理步骤。
- `simulateStreamingMiddleware`：模拟非流式语言模型响应的流式行为。
- `defaultSettingsMiddleware`：在模型调用中应用一致的配置，与任何模型（包括自定义提供商）无缝协作。只需为参数（如 temperature）指定默认值，并使用 `providerMetadata` 设置提供商特定选项。

```
1import { openai } from "@ai-sdk/openai";2import { anthropic } from "@ai-sdk/anthropic";3import {4  customProvider,5  defaultSettingsMiddleware,6  wrapLanguageModel,7} from "ai";8
910export const model = customProvider({11  languageModels: {12    fast: openai("gpt-4o-mini"),13    writing: anthropic("claude-3-5-sonnet-latest"),14    reasoning: wrapLanguageModel({15      model: anthropic("claude-3-7-sonnet-20250219"),16      middleware: defaultSettingsMiddleware({17        settings: {18          providerMetadata: {19            anthropic: {20              thinking: { type: "enabled", budgetTokens: 12000 },21            },22          },23        },24      }),25    }),26  },27});
```

这些中间件选项可以组合使用，以创建强大、可组合的功能，适用于任何支持的语言模型。请查看我们的中间件文档以了解更多信息。

## Link to heading其他功能

我们最近将几个实验性功能转为稳定版，这意味着它们现已生产就绪并经过充分测试。这些功能包括：

- 自定义提供商：将 ID 映射到任何模型，允许您设置自定义模型配置、别名等。
- 中间件改进：同时应用多个中间件以增强请求处理和转换。中间件已转为稳定版。
- 工具调用流式传输：将部分工具调用作为数据流的一部分进行流式传输。已转为稳定版。
- 响应体访问：在使用 `generateText` 或 `generateObject` 时，通过 `response.body` 属性直接访问原始响应体。
- 数据流增强：为 `streamText` 发送开始/结束事件，并使用 `write`/`writeSource` 方法更精细地控制流数据。
- 错误处理：利用 `streamText`/`streamObject` 的 `onError` 回调来优雅地管理错误。
- 对象生成：利用 `generateObject` 的 `repairText` 功能来修复和改进生成的内容。
- 提供商选项：配置提供商特定的请求选项（例如 OpenAI 的 `reasoningEffort`）。具体细节取决于提供商。已转为稳定版。
- 提供商元数据：访问提供商特定的响应元数据。具体细节取决于提供商。已转为稳定版。

## Link to heading提供商更新

AI SDK 提供商生态系统持续增长，新增和改进的提供商包括：

- Amazon Bedrock：更紧密地集成到 AI SDK 标准功能中，支持中止、获取和错误处理。新增对缓存点支持、Amazon Nova Canvas 图像生成、预算 Token 支持以及推理支持。
- Anthropic：新增推理支持、针对推理内容的模型设置调整、工具更新（bash、文本编辑器、计算机）以及图片 URL 支持。
- Azure：新增图像生成支持。
- Cohere：改进了工具处理，修复了参数和工具计划内容的问题。
- DeepInfra：新增图像生成支持。
- Google：增强了 Schema 支持、对未定义部分的容错性、种子支持、动态检索、空内容处理、推理支持以及模型 ID 更新。
- Google Vertex AI：新增新的 Gemini 模型、消息中公共文件 URL 的支持，以及 Anthropic Claude 模型的提示词缓存。
- Mistral：改进了内容处理，修复了未定义内容、复杂内容类型、PDF 支持以及多个文本内容部分的问题。
- OpenAI：新增对 gpt-4.5、o3-mini、responses API 以及 PDF 输入的支持。
- OpenAI Compatible：新增在 generateText/streamText 中对 providerOptions 的支持。
- Perplexity：新增来源支持。
- Replicate：新增对版本化模型的支持。
- Together AI：新增图像生成支持并扩展了 provider V1 规范。
- xAI：新增图像生成支持。

Amazon Bedrock：更紧密地集成到 AI SDK 标准功能中，支持中止、获取和错误处理。新增对缓存点支持、Amazon Nova Canvas 图像生成、预算 Token 支持以及推理支持。

Anthropic：新增推理支持、针对推理内容的模型设置调整、工具更新（bash、文本编辑器、计算机）以及图片 URL 支持。

Azure：新增图像生成支持。

Cohere：改进了工具处理，修复了参数和工具计划内容的问题。

DeepInfra：新增图像生成支持。

Google：增强了 Schema 支持、对未定义部分的容错性、种子支持、动态检索、空内容处理、推理支持以及模型 ID 更新。

Google Vertex AI：新增新的 Gemini 模型、消息中公共文件 URL 的支持，以及 Anthropic Claude 模型的提示词缓存。

Mistral：改进了内容处理，修复了未定义内容、复杂内容类型、PDF 支持以及多个文本内容部分的问题。

OpenAI：新增对 gpt-4.5、o3-mini、responses API 以及 PDF 输入的支持。

OpenAI Compatible：新增在 generateText/streamText 中对 providerOptions 的支持。

Perplexity：新增来源支持。

Replicate：新增对版本化模型的支持。

Together AI：新增图像生成支持并扩展了 provider V1 规范。

xAI：新增图像生成支持。

## 链接到标题 入门指南

借助 MCP 支持、语言模型图像生成以及推理等强大新功能，现在正是使用 AI SDK 构建 AI 应用的最佳时机。

- 启动新的 AI 项目：准备好构建新东西了吗？查看我们的最新指南
- 探索我们的模板：访问我们的模板库，查看 AI SDK 的实际应用
- 加入社区：在我们的 GitHub 讨论中分享你正在构建的内容

启动新的 AI 项目：准备好构建新东西了吗？查看我们的最新指南

探索我们的模板：访问我们的模板库，查看 AI SDK 的实际应用

加入社区：在我们的 GitHub 讨论中分享你正在构建的内容

## 链接到标题 展示

自 4.1 版本发布以来，我们看到了一些由 AI SDK 驱动的出色产品，我们想重点介绍：

- Otto 是一款能够自动化重复性知识工作的智能电子表格。
- Payload 是一个开源的 Next.js 全栈框架，可将你的配置无缝转化为包含管理 UI、API 和数据库管理的完整后端。

Otto 是一款能够自动化重复性知识工作的智能电子表格。

Payload 是一个开源的 Next.js 全栈框架，可将你的配置无缝转化为包含管理 UI、API 和数据库管理的完整后端。

## 链接到标题 贡献者

AI SDK 4.2 是 Vercel 核心团队（Lars、Jeremy、Walter 和 Nico）以及众多社区贡献者共同努力的成果。感谢贡献了已合并拉取请求的各位：

Xiang-CH、d3lm、dreamorosi、MrunmayS、valstu、BrianHung、jstjoe、rmarescu、lasley、shaneporter、FinnWoelm、threepointone、minpeter、UrielCh、Younis-Ahmed、edukure、O1af、abhishekpatil4、sandonl、NVolcz、nihaocami、yudistiraashadi、mattlgroff、gianpaj、habeebmoosa、KABBOUCHI、franklin007ban2、yoshinorisano、jcppman、gravelBridge、peetzweg、patelvivekdev、ggallon、zeke、epoyraz、IObert、KitBurgess、marwhyte、niranjan94、asishupadhyay、SalmanK81099。

特别感谢：

- elliott-with-the-longest-name-on-github 对 Svelte 5 的支持
- iteratetograceness 对 MCP 的支持
- Und3rf10w 对 Amazon Bedrock 推理的支持

elliott-with-the-longest-name-on-github 对 Svelte 5 的支持

iteratetograceness 对 MCP 的支持

Und3rf10w 对 Amazon Bedrock 推理的支持

你们的反馈和贡献持续塑造着 AI SDK。我们很期待看到你们利用这些新功能构建出怎样的成果。

---

> 本文由AI自动翻译，原文链接：[AI SDK 4.2](https://vercel.com/blog/ai-sdk-4-2)
> 
> 翻译时间：2026-06-01 06:55
