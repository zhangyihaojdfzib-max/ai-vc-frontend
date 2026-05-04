---
title: Vercel MCP适配器：高效构建AI模型集成服务器
title_original: Building efficient MCP servers - Vercel – Vercel
date: '2025-06-12'
source: Vercel Blog
source_url: https://vercel.com/blog/building-efficient-mcp-servers
author: ''
summary: 文章介绍了模型上下文协议（MCP）的演进及其在AI集成中的重要性。Vercel推出了MCP适配器，帮助开发者使用Next.js等框架构建高效的MCP服务器。新引入的Streamable
  HTTP传输方式取代了低效的SSE，显著降低CPU消耗。文章展示了如何通过适配器优化服务器性能，并展望了MCP生态系统的未来发展。
categories:
- AI基础设施
tags:
- MCP
- Vercel
- Streamable HTTP
- AI集成
- 模型上下文协议
draft: false
translated_at: '2026-05-04T05:48:43.064550'
---

模型上下文协议（MCP）标准化了如何为AI模型构建集成。我们构建了MCP适配器，帮助开发者使用Next.js、Nuxt和SvelteKit等流行框架创建自己的MCP服务器。Zapier、Composio、Vapi和Solana等生产级应用使用MCP适配器在Vercel上部署自己的MCP服务器，并在过去一个月中实现了显著增长。

MCP已被Cursor、Claude和Windsurf等流行客户端采用。这些客户端现在支持连接MCP服务器并调用工具。企业创建自己的MCP服务器，使其工具在生态系统中可用。

MCP日益增长的采用率显示了其重要性，但扩展MCP服务器也暴露了原始设计中的局限性。让我们看看MCP规范是如何演进的，以及MCP适配器能提供哪些帮助。

## 链接到标题MCP的变化

当MCP规范的第一版于2024年11月发布时，它支持标准IO（stdio）和服务器推送事件（SSE）作为客户端与服务器之间的传输方式。Stdio需要在本地运行MCP服务器，而SSE允许服务器托管在远程并可远程访问。

然而，SSE是一种低效的传输方式。它会在客户端和服务器之间保持持久连接，即使在空闲时也是如此。虽然Vercel的Fluid计算通过复用已分配的服务器减少了开销，但对于大规模MCP服务器而言，SSE仍然是一种不可持续的选择。

### 链接到标题新的MCP服务器传输方式：Streamable HTTP

2025年3月，新版本的MCP规范引入了Streamable HTTP作为推荐的传输方式，取代了SSE。这一变化通过消除持久客户端-服务器连接的需求，提高了效率。

现有的投入和资源不足减缓了MCP客户端开发者和MCP服务器开发者对Streamable HTTP的采用。因此，许多现有的MCP客户端仍然只支持stdio和SSE。

使用Vercel MCP适配器构建的服务器开发者将获得对Streamable HTTP和SSE的内置支持，并可以选择禁用SSE，以完全符合官方支持且更高效的传输方式。

```
1import { createMcpHandler } from '@vercel/mcp-adapter';2
3const handler = createMcpHandler(server => {4  server.tool(5    'roll_dice',6    'Rolls an N-sided die',7    { sides: z.number().int().min(2) },8    async ({ sides }) => {9      const value = 1 + Math.floor(Math.random() * sides);10      return { content: [{ type: 'text', text: `🎲 You rolled a ${value}!` }] };11    }12  );13});14
15export { handler as GET, handler as POST, handler as DELETE };
```

一个包含单个工具调用的MCP服务器示例。

## 链接到标题优化MCP服务器以提高效率

Streamable HTTP凭借其标准的HTTP传输方式以及对无状态和有状态服务器模型的支持，是远程托管MCP服务器的明确发展方向。

为了支持尚未处理Streamable HTTP的客户端，mcp-remote包可以通过stdio代理它。通过像Solana使用的方法那样进行小的服务器设置更改，开发者可以在等待完整客户端支持的同时，受益于Streamable HTTP的效率。

这种方法在客户端支持持续演进的同时提供了前向兼容性。在大多数情况下，一旦Streamable HTTP的原生支持得到更广泛采用，就不再需要mcp-remote。

一个部署在Vercel上的MCP服务器能够完全切换到Streamable HTTP，并在用户持续增长的情况下将CPU使用率降低一半。

![迁移到Streamable HTTP将CPU消耗降低了超过50%](/images/posts/396d3a634150.jpg)

![迁移到Streamable HTTP将CPU消耗降低了超过50%](/images/posts/b4d54d97b8e3.jpg)

## 链接到标题面向未来构建

MCP生态系统正在快速发展。借助Fluid计算和MCP适配器，您可以交付支持当前和未来客户端的MCP服务器。

我们致力于支持每一个采用MCP的团队。探索MCP适配器并尝试Next.js MCP模板来构建您的MCP服务器。

Next.js上的MCP服务器

开始构建您在Vercel上的第一个MCP服务器。

立即部署

---

> 本文由AI自动翻译，原文链接：[Building efficient MCP servers - Vercel – Vercel](https://vercel.com/blog/building-efficient-mcp-servers)
> 
> 翻译时间：2026-05-04 05:48
