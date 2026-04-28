---
title: Chat SDK：让AI Agent走进用户的工作平台
title_original: Chat SDK brings agents to your users - Vercel – Vercel
date: '2026-03-19'
source: Vercel Blog
source_url: https://vercel.com/blog/chat-sdk-brings-agents-to-your-users
author: ''
summary: Vercel推出Chat SDK，旨在解决AI Agent跨平台部署的难题。该库通过统一的抽象层，让开发者只需一套代码即可将Agent部署到Slack、Teams、Discord、Telegram等主流聊天平台，无需为每个平台单独集成API。Chat
  SDK自动处理平台间的不一致性（如流式传输差异），并支持通过适配器灵活切换目标平台。这一工具延续了AI SDK的核心理念——降低集成复杂度，让Agent主动融入用户已有的工作环境，而非要求用户适应新的界面。
categories:
- AI基础设施
tags:
- Vercel
- Chat SDK
- AI Agent
- 跨平台部署
- 聊天机器人
draft: false
translated_at: '2026-04-28T05:34:02.454595'
---

**9分钟阅读**

一月初，我们给整个公司布置了一项挑战：想办法将你的产出翻倍。

大家开始创建 Agent（智能体）。大部分是聊天机器人，但都是专用型的，专为实际工作流程增强而构建：这些 Agent（智能体）能够自动完成那些原本繁琐且耗时的工作。

最初，大家为各自的 Agent（智能体）构建了单独的界面，而 AI SDK 通过开箱即用的模型集成和简化 UI 设计的 AI Elements，让这一过程变得简单。

然后我们遇到了一个限制。大家希望在 Slack 中与这些 Agent（智能体）交互，这意味着每个人都得想办法集成 Slack 的 API。

接着问题变得更糟了。一旦 Agent（智能体）进入了 Slack，大家又希望将它们集成到更多平台，比如 Discord、Github，甚至像 Linear 这样的问题追踪器。每个平台都为每个 Agent（智能体）带来了新的集成挑战。

我们恍然大悟。与其让人们来找 Agent（智能体），不如把 Agent（智能体）送到他们已经在工作的地方。

#### 链接到标题聊天需要集成抽象层

我们意识到，我们已经让团队能够轻松创建 Agent（智能体），但我们需要让跨平台扩展和采用变得更加容易。

这对每家公司都是如此。人们已经在使用 Microsoft Teams、WhatsApp、Telegram 和 Google Chat，而 Agent（智能体）需要在这些平台上都能使用。

这正是 Chat SDK 所做的：让 Agent（智能体）在企业和消费者聊天平台上都能使用。

就像 AI SDK 将不同模型提供商的 API 统一到一个接口一样，我们构建了 Chat SDK，将消息 API 的各种特性抽象成一个简单的框架，供开发者及其编码 Agent（智能体）使用。

```
1import { streamText } from "ai";2
3const result = await streamText({4  model: "anthropic/claude-opus-4.6", 5  prompt: "Hello world",6});
```

AI SDK 抽象了各个提供商的具体逻辑，使得更换提供商和模型只需更改一个简单的字符串。

开发者不再需要考虑不同平台之间的流式传输有何不同，或者如何为各个 API 处理格式化、分支逻辑，甚至是反应处理。

## 链接到标题一次编写，随处部署

Chat SDK 是一个 TypeScript 库，用于构建能在 Slack、Microsoft Teams、Google Chat、Discord、Telegram、GitHub 和 Linear 上运行的机器人，且只需一个代码库。核心的 `chat` 包处理事件路由和应用逻辑。平台特定的行为由适配器处理，因此当你的部署目标改变时，你的处理程序无需更改。

以下是一个基础机器人的样子：

```
1import { Chat } from "chat";2import { createSlackAdapter } from "@chat-adapter/slack";3import { createRedisState } from "@chat-adapter/state-redis";4
5const bot = new Chat({6  userName: "mybot",7  adapters: {8    slack: createSlackAdapter(),9  },10  state: createRedisState(),11});12
13bot.onNewMention(async (thread) => {14  await thread.subscribe();15  await thread.post("Hello! I'm listening to this thread now.");16});17
18bot.onSubscribedMessage(async (thread, message) => {19  await thread.post(`You said: ${message.text}`);20});
```

每个适配器都会从环境变量中自动检测凭证，因此你无需任何额外配置即可开始使用。从 Slack 切换到 Discord 意味着更换适配器，而不是重写机器人。

## 链接到标题平台不一致性，已处理

各个平台的行为差异很大，Chat SDK 不会用虚假的承诺来掩盖这些差异。相反，它在适配器层处理这些差异，这样你的应用程序代码就不必操心了。

以流式传输为例。Slack 有一个原生流式传输路径，可以在响应到达时实时渲染粗体、斜体、列表和其他格式。其他平台则使用回退流式传输路径，在每次中间编辑时，通过每个适配器的 markdown 到原生格式的转换管道传递流式文本。

在 Chat SDK 之前，这些适配器接收的是原始的 markdown 字符串，因此 Discord 或 Teams 上的用户会看到字面上的 `**bold**` 语法，直到最终消息解析完成。现在，这种转换会自动发生。

表格渲染遵循相同的模式。`Table()` 组件为你提供了一个可组合的 API，用于在每个适配器上渲染表格。传入表头和行，Chat SDK 会处理其余部分。Slack 渲染 Block Kit 表格块。Teams 和 Discord 使用 GFM markdown 表格。Google Chat 使用等宽文本小部件。Telegram 将表格转换为代码块。GitHub 和 Linear 继续使用它们现有的 markdown 管道。

```
1import { Table } from "chat";2
3await thread.post(4  <Table5    headers={["Name", "Status", "Region"]}6    rows={[7      ["api-prod", "healthy", "iad1"],8      ["api-staging", "degraded", "sfo1"],9    ]}10  />11);
```

卡片、模态框和按钮的工作方式类似。

你使用 JSX 编写一次元素，每个适配器会以平台原生支持的任何格式渲染它们。如果某个平台不支持某个元素，它会优雅地回退。

## 链接到标题为什么 Chat SDK 对单一平台也很重要

即使你的 Agent（智能体）只针对 Slack，Chat SDK 仍然能解决实际问题。频道和用户名会自动转换为纯文本，以便你的 Agent（智能体）理解对话的上下文。

这种转换是双向的。当 Agent（智能体）使用纯文本 @ 提及某人时，Chat SDK 确保通知实际上会在 Slack 中触发。

Agent（智能体）需要完整的上下文才能有效工作。Chat SDK 会自动将链接预览内容、引用的帖子和图像直接包含在 Agent（智能体）的提示词中。此外，当模型生成标准 markdown 时，Slack 本身并不原生支持它。

Chat SDK 会自动将标准 markdown 转换为 Slack 的变体。即使在使用 Slack 的原生仅追加流式传输 API 时，这种转换也是实时发生的。

## 链接到标题内置 AI 流式传输

`post()` 函数直接接受 AI SDK 的文本流，这意味着你可以将流式 LLM 响应直接输送到任何聊天平台，无需任何额外的连接：

```
1import { streamText } from "ai";2
3bot.onNewMention(async (thread) => {4  await thread.subscribe();5
6  const result = await streamText({7    model: "anthropic/claude-sonnet-4",8    prompt: "Summarize what's happening in this thread.",9  });10
11  await thread.post(result.textStream);12});
```

适配器层处理该流的平台特定渲染，包括在平台支持的情况下的实时格式化。

## 链接到标题可扩展的状态管理

线程订阅、分布式锁和键值缓存状态通过可插拔的状态适配器处理。Redis 和 ioredis 自发布以来就已可用。现在 PostgreSQL 也作为生产就绪选项得到支持，因此已经在运行 Postgres 的团队无需向基础设施添加 Redis 即可持久化机器人状态。

```
1import { createPostgresState } from "@chat-adapter/state-postgres";2import { createSlackAdapter } from "@chat-adapter/slack";3import { Chat } from "chat";4
5const bot = new Chat({6  userName: "mybot",7  adapters: {8    slack: createSlackAdapter(),9  },10  state: createPostgresState(),11});
```

PostgreSQL 适配器使用 `pg`（node-postgres）和原始 SQL，并在首次连接时自动创建所需的表。它支持基于 TTL 的缓存、跨多个实例的分布式锁定，以及通过可配置的键前缀进行命名空间状态管理。社区贡献者 @bailaid 在 PR #154 中奠定了基础。

## 链接到标题WhatsApp 及更多

Chat SDK 现在支持 WhatsApp，将一次编写的模式扩展到了世界上最大的消息平台之一。

WhatsApp 适配器支持消息、反应、自动分块、已读回执、多媒体下载（图片、语音消息、贴纸）以及带有 Google Maps URL 的位置共享。卡片渲染为最多包含三个选项的交互式回复按钮，在需要时会回退为格式化文本。

```
1import { createWhatsAppAdapter } from "@chat-adapter/whatsapp";2import { Chat } from "chat";3
4const bot = new Chat({5  userName: "mybot",6  adapters: {7    whatsapp: createWhatsAppAdapter(),8  },9  state: createRedisState(),10});11
12bot.onNewMention(async (thread) => {13  await thread.post("Hello from WhatsApp!");14});
```

请注意，WhatsApp 强制执行 24 小时消息窗口，因此机器人只能在该时间段内回复。该适配器不支持消息历史记录、编辑或删除。社区贡献者 @ghellach 在 PR #102 中奠定了基础。

## 链接到标题

开始使用

要增强您的编码 Agent（智能体），请安装 Chat 技能：

```
1npx skills add vercel/chat
```

这将使您的 Agent（智能体）能够访问 Chat SDK 的文档、模式及最佳实践，从而帮助您基于该 SDK 构建机器人。

您还可以修改并使用以下入门提示词：

Chat SDK 文档涵盖了入门指南、平台适配器设置、状态配置，以及常见模式的指南，包括基于 Next.js 和 Redis 的 Slack 机器人、基于 Nuxt 的 Discord 支持机器人，以及基于 Hono 的 GitHub 代码审查机器人。

Chat SDK 是开源项目，目前处于公开测试阶段。您的团队一直在构建的 Agent（智能体）不必局限于单一平台。它们可以部署到用户实际所在的任何地方。

---

> 本文由AI自动翻译，原文链接：[Chat SDK brings agents to your users - Vercel – Vercel](https://vercel.com/blog/chat-sdk-brings-agents-to-your-users)
> 
> 翻译时间：2026-04-28 05:34
