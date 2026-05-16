---
title: Vercel支持MCP服务器部署，简化AI集成
title_original: MCP server support on Vercel - Vercel
date: '2025-05-07'
source: Vercel Blog
source_url: https://vercel.com/changelog/mcp-server-support-on-vercel
author: ''
summary: Vercel宣布支持部署MCP（模型上下文协议）服务器和客户端，为AI模型构建集成提供新方式。MCP不同于传统API，更像是为AI任务定制的工具包，支持HTTP和OAuth协议。Vercel发布了@vercel/mcp-adapter包简化部署，并支持Fluid计算以降低成本。AI
  SDK内置MCP连接功能，已有客户在生产环境成功部署，节省超90%成本。
categories:
- AI基础设施
tags:
- MCP
- Vercel
- AI集成
- 模型上下文协议
- 无服务器架构
draft: false
translated_at: '2026-05-16T05:29:36.205544'
---

![](/images/posts/1dd058e62033.jpg)

![](/images/posts/e3e697a7260e.jpg)

模型上下文协议（MCP）是一种为AI模型构建集成的方式。

Vercel现在支持部署MCP服务器（AI模型可连接）以及MCP客户端（调用服务器的AI聊天机器人应用）。

立即从我们的Next.js MCP模板开始上手。

## 链接到标题MCP与API有何不同？

API允许不同服务之间相互通信。MCP略有不同。

与其将MCP视为REST API，不如将其看作是为帮助AI完成特定任务而量身定制的工具包。单个MCP工具可能在后台使用多个API和其他业务逻辑。

如果你已经熟悉AI中的工具调用，MCP是一种调用托管在不同服务器上的工具的方式。

MCP现在支持与其他Web API类似的协议，即使用HTTP和OAuth。这是对之前有状态的服务器发送事件（SSE）协议的改进。

## 链接到标题将MCP服务器部署到Vercel

为简化在Vercel上构建MCP服务器，我们发布了一个新包@vercel/mcp-adapter，它同时支持旧的SSE传输和新的无状态HTTP传输。

更新：@vercel/mcp-adapter包已重命名为mcp-handler。

```
1import { createMcpHandler } from '@vercel/mcp-adapter';2
3const handler = createMcpHandler(server => {4  server.tool(5    'roll_dice',6    'Rolls an N-sided die',7    { sides: z.number().int().min(2) },8    async ({ sides }) => {9      const value = 1 + Math.floor(Math.random() * sides);10      return { content: [{ type: 'text', text: `🎲 You rolled a ${value}!` }] };11    }12  );13});14
15export { handler as GET, handler as POST, handler as DELETE };
```

一个包含单个工具调用的MCP服务器示例。

目前大多数MCP客户端仅支持SSE传输选项。为处理SSE传输所需的状态，你可以通过我们市场中的任何提供商（如Upstash和Redis Labs）集成Redis服务器。

我们已经看到客户成功地将MCP服务器部署到生产环境。一位客户在使用Vercel的Fluid计算时，相比传统无服务器架构节省了超过90%的成本。Fluid使你能够拥有完整的Node.js或Python兼容性，同时为AI推理和Agent工作负载提供更具成本效益和高性能的平台。

## 链接到标题开始使用MCP

Vercel的AI SDK内置支持将你的Node.js或Next.js应用连接到MCP服务器。

我们期待未来使用HTTP传输构建的MCP服务器，并开始探索OAuth支持等最新进展。

其他Vercel项目（如shadcn/ui）正在探索集成MCP的方式。如果你对Vercel上的MCP服务器用例有建议，可以在我们的社区中分享反馈。

Next.js上的MCP服务器

立即开始在Vercel上构建你的第一个MCP服务器。

立即部署

---

> 本文由AI自动翻译，原文链接：[MCP server support on Vercel - Vercel](https://vercel.com/changelog/mcp-server-support-on-vercel)
> 
> 翻译时间：2026-05-16 05:29
