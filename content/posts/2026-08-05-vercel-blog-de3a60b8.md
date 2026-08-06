---
title: v0 API正式发布：编程式应用构建代理
title_original: Introducing the new v0 API
date: '2026-08-05'
source: Vercel Blog
source_url: https://vercel.com/blog/introducing-the-new-v0-api
author: ''
summary: Vercel今日推出v0 API，允许开发者以编程方式、无头访问v0应用构建代理。用户发送提示词，v0即可生成应用，在Sandbox中启动开发服务器，并提供可嵌入的预览URL。每个聊天对应一个独立工作空间，支持流式传输工作过程，实时捕获并修复错误。API支持同步、异步和流式响应，可解锁白标应用构建器、自动化应用变更及Agent构建工具等用例。该API现已全面开放，旨在将v0的能力集成到任何产品或流程中。
categories:
- AI产品
tags:
- v0 API
- Vercel
- 应用构建
- AI代理
- 无头开发
draft: false
translated_at: '2026-08-06T05:11:41.174871'
---

今天我们推出了全新的v0 API：以编程方式、无头访问v0的应用构建代理。发送提示词，v0即可生成应用，在Vercel Sandbox中启动开发服务器，并为你提供一个可嵌入到自己UI中的预览URL。

每个聊天都是一个应用的独立工作空间，v0可以在其中读取、编辑和运行文件。后续消息会从当前状态继续。v0会验证Sandbox中运行的代码，因此可以实时捕获并修复应用中的错误。

新API现已全面开放。

## 工作原理

从提示词创建聊天，流式传输其工作过程，并在你自己的界面中渲染实时预览。首先，安装v0 SDK。

```
pnpm add v0@latest
```

然后，创建聊天。发送提示词，v0即可生成你的应用。

```
1import { v0 } from 'v0' 2
3const result = await v0.chats.create({ 4  message: '为支持团队构建一个工单分类应用。', 5}) 6
7if (result.error) { 8  throw new Error(result.error.message) 9} 10
11const chatId = result.data.chat.id
```

创建聊天并保存其ID，供后续所有请求使用。

向同一聊天发送后续消息以继续构建。每条消息都从当前状态继续。

```
1const message = await v0.messages.send({ 2  chatId, 3  message: '添加优先级筛选器和负责人列。', 4}) 5
6if (message.error) { 7  throw new Error(message.error.message) 8}
```

发送后续消息；v0会就地编辑现有应用。

然后嵌入应用。

```
<iframe src="/api/v0-preview/chat_abc123/" />
```

通过将iframe指向你的代理路由来嵌入应用。

输入提示词，输出运行中的应用。v0在后台运营Sandbox、开发服务器和预览。当你准备好后，通过一次API调用即可部署到Vercel。v0管理整个流程。

## 解锁的能力

新API让你可以在自己的产品或流程中运行v0的应用构建器。这开启了以下用例：

- 白标应用构建器：你的用户描述一个应用，即可获得一个应用。
- 自动化应用变更：通过脚本、CI任务或webhook触发v0，生成新应用或更新现有应用。
- 面向你Agent的构建工具：Agent返回一个可运行的应用，而非代码片段。

白标应用构建器：你的用户描述一个应用，即可获得一个应用。

自动化应用变更：通过脚本、CI任务或webhook触发v0，生成新应用或更新现有应用。

面向你Agent的构建工具：Agent返回一个可运行的应用，而非代码片段。

下面，我们分解该工作流背后的API原语。

## 从聊天开始

每个聊天保存一个应用的状态，一个仓库或Vercel项目可以拥有多个聊天。保存每个聊天的ID，并将后续消息发送到该聊天。元数据允许你按客户、工作空间、应用或你已使用的任何键对聊天进行分组。

了解更多关于消息的信息。

## 流式传输轨迹

你的界面需要展示从发送请求到看到更新预览之间发生了什么。

每条消息都包含有序的部分：文本、思考、文件读取和编辑、搜索、bash命令、工具调用和Agent操作。同一个对象可以驱动一行状态、变更文件视图或完整轨迹。

```
1const stream = await v0.messages.sendStream({ 2  chatId: 'chat_abc123', 3  message: '添加身份验证并解释你更改的文件。', 4}) 5
6for await (const update of stream.stream) { 7  console.log(update.parts) 8  if (update.usage) { 9    console.log(update.usage) 10  } 11}
```

流式传输消息的工作过程；每次更新都是部分的完整快照。

使用量随聊天和消息响应一起返回，因此你可以在工作完成时进行核算。

## 选择同步、异步或流式

聊天创建和消息支持同步、异步和流式响应。当调用方需要完整响应时使用同步。使用异步来排队工作并通过webhook接收更新或稍后轮询v0的响应。流式传输请求以实时渲染v0的工作过程。

```
1const message = '为支持团队构建一个工单分类应用。' 2
34const completed = await v0.chats.create({ message }) 5
6if (completed.error) { 7  throw new Error(completed.error.message) 8} 9
1011const queued = await v0.chats.createAsync({ message }) 12
13if (queued.error) { 14  throw new Error(queued.error.message) 15} 16
17console.log(queued.data.chatId, queued.data.messageId) 18
1920const stream = await v0.chats.createStream({ message })
```

以三种方式创建聊天：等待、排队或流式传输同一提示词。

## 从现有代码开始

你也可以从仓库、ZIP归档或一组文件创建聊天。

```
1const result = await v0.chats.createFromRepo({ 2  repo: { 3    url: 'https://github.com/acme/app', 4    branch: 'main', 5  }, 6  title: 'Acme应用', 7  metadata: { 8    source: 'github', 9  }, 10}) 11
12if (result.error) { 13  throw new Error(result.error.message) 14} 15
16const chatId = result.data.chat.id 17console.log(chatId)
```

从现有仓库创建聊天。

## 渲染开发服务器预览

每个聊天都会获得一个短期预览令牌。从服务器路由获取它，并通过它代理浏览器请求，这样你的v0 API密钥永远不会到达浏览器。当预览就绪时，流量会转发到它；在Sandbox启动期间，请求会回退到加载路由。将iframe指向你的代理路由，并缓存预览详情直到它们过期。

```
1import { fetchPreview, v0 } from 'v0' 2
3export async function proxyPreviewRequest( 4  request: Request, 5  chatId: string, 6  path: string[], 7) { 8  const result = await v0.chats.getPreview({ chatId }) 9  10  if (result.error) { 11    throw new Error(result.error.message) 12  } 13
14  return fetchPreview({ 15    request, 16    preview: result.data, 17    path, 18    fallbackUrl: `/api/v0-preview/${chatId}/loading`, 19  }) 20}
```

通过服务器路由代理预览请求。

在文档中了解更多关于访问预览的信息。

## 使用你自己的工具和设计系统

为聊天开启特定的MCP服务器，或使用默认设置。

Design Systems 2.0将设计系统保存为技能。在请求中包含它，即可加载其组件、令牌、设置和启动应用。

```
1const designSystem = { 2  type: 'memory', 3  scope: 'team', 4  skillName: 'geist-ui', 5} 6
7const result = await v0.chats.create({ 8  message: '构建一个带筛选器和图表的管理控制台。', 9  skills: [ 10    designSystem, 11  ], 12})
```

创建设计系统作为技能加载的聊天。

每个请求最多可以传递三个技能，来自团队或用户记忆、skills.sh或连接的仓库，或者让Agent为你拉取它们。

## 从Agent中使用v0

如果你正在构建Agent，将v0作为工具提供给它是很合适的。当Agent需要生成一个可运行的应用时，它调用v0，并返回一个正在运行的预览或部署给用户。你的Agent继续负责其他所有事情。

有三种连接方式：

### MCP

将v0 MCP服务器连接到支持MCP的IDE、桌面助手或Agent运行时。

```
1{ 2  "mcpServers": { 3    "v0": { 4      "url": "https://v0.app/api/mcp" 5    } 6  } 7}
```

v0服务器的MCP客户端入口。

首次连接会启动OAuth流程。MCP服务器暴露了用于创建聊天、列出聊天、获取聊天详情、列出和发送消息、解决待处理任务以及获取预览URL的工具。

### AI SDK

对于使用AI SDK构建的TypeScript Agent，使用@v0-sdk/ai-tools将v0的API操作作为工具暴露在Agent自身的循环中。

```
pnpm add @v0-sdk/ai-tools ai @ai-sdk/openai
```

使用AI SDK和提供商安装v0工具。

```1import { openai } from '@ai-sdk/openai' 2import { generateText, stepCountIs } from 'ai' 3import { v0ToolsByCategory } from '@v0-sdk/ai-tools' 4
5const { chats, messages } = v0ToolsByCategory() 6
7const result = await generateText({ 8  model: openai('gpt-5.5'), 9  system: `使用v0创建和修改Web应用。当有可用的聊天ID时，继续现有的v0聊天。`, 10  prompt: '构建一个带有图表的客户洞察应用。', 11  tools: { 12    ...chats, 13    ...messages, 14  }, 15  stopWhen: stepCountIs(10), 16})
```

为AI SDK Agent提供v0的聊天和消息工具。

Agent决定何时创建或继续聊天。您的AI SDK运行保持对编排和最终响应的控制。

### 连接Vercel项目

为聊天创建一个Vercel项目，然后通过Vercel API管理其环境变量、集成和设置。您的应用默认获得Vercel的安全性和可观测性。

```
1const result = await v0.chats.createVercelProject({ 2  chatId: 'chat_123', 3}) 4
5if (result.error) { 6  throw new Error(result.error.message) 7} 8
9const vercelProjectId = result.data.vercelProjectId
```

将Vercel项目附加到聊天。

当您准备好发布时，将聊天部署到Vercel。

```
1const result = await v0.chats.deploy({ chatId }) 2
3if (result.error) { 4  throw new Error(result.error.message) 5} 6
7const { deploymentId, vercelProjectId } = result.data
```

将聊天发布到Vercel。

## 迁移您的聊天

来自先前版本v0 API的聊天无法在新版本上运行，因此请将其迁移。选择您想保留的版本，将其下载为ZIP文件，并从该ZIP文件创建新的聊天。如果需要可追溯性，请将旧标识符存储在新聊天的元数据中。

迁移指南涵盖了完整的映射。主要变更：

- 对新请求使用`https://api.v0.dev/v2`。
- 聊天保存当前应用状态，消息保存其历史记录。
- 用聊天文件工作流替换版本工作流，用聊天元数据替换`v0Project`组织。
- 使用`vercelProjectId`以及Vercel API进行项目操作。
- 渲染消息`parts`，而不仅仅是最终文本。

使用`https://api.v0.dev/v2`进行新请求。

聊天保存当前应用状态，消息保存其历史记录。

用聊天文件工作流替换版本工作流，用聊天元数据替换`v0Project`组织。

使用`vercelProjectId`以及Vercel API进行项目操作。

渲染消息`parts`，而不仅仅是最终文本。

## 开始使用

在v0设置中创建API密钥并安装SDK。

```
pnpm add v0@latest
```

或者，搭建一个完整的应用。

```
pnpm create v0-sdk-app@latest my-v0-app
```

阅读文档和迁移指南。

使用v0 API构建您的第一个应用生成界面。

阅读快速入门指南，从提示词到在您自己的UI中运行的应用。

开始使用

## 贡献者

Amelia Charles

---

> 本文由AI自动翻译，原文链接：[Introducing the new v0 API](https://vercel.com/blog/introducing-the-new-v0-api)
> 
> 翻译时间：2026-08-06 05:11
