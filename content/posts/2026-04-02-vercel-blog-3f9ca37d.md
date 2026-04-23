---
title: 使用Nuxt MCP工具包构建AI服务器
title_original: Build an MCP server with Nuxt - Vercel – Vercel
date: '2026-04-02'
source: Vercel Blog
source_url: https://vercel.com/changelog/build-mcp-server-with-nuxt
author: ''
summary: 本文介绍了如何利用Nuxt MCP工具包为Nuxt应用程序构建模型上下文协议（MCP）服务器。该模块允许开发者通过Zod验证定义工具、将数据公开为资源、创建可复用提示词，并提供了集成的MCP检查器用于调试。此外，它还支持中间件、动态定义、跨工具调用的会话持久化，以及一个让模型在单次执行中编排多个工具调用的代码模式，为开发AI功能提供了强大且便捷的基础设施。
categories:
- AI基础设施
tags:
- Nuxt
- MCP
- AI开发
- 全栈开发
- Vercel
draft: false
translated_at: '2026-04-23T05:05:08.154186'
---

![](/images/posts/5de5a31b3be3.jpg)

![](/images/posts/c046dfdb626e.jpg)

使用Nuxt构建AI功能的开发者，现在可以利用Nuxt MCP工具包，直接在他们的应用程序中创建模型上下文协议（MCP）服务器。

安装模块

```
1npx nuxt module add mcp-toolkit
```

该模块允许您使用Zod验证定义工具，将数据公开为资源，并创建可复用的提示词。它还包含一个集成的MCP检查器用于调试，支持中间件、动态定义、跨工具调用的会话持久化，以及一个允许模型在单次执行中编排多个工具调用的代码模式。

阅读文档或入门指南，开始构建。

---

> 本文由AI自动翻译，原文链接：[Build an MCP server with Nuxt - Vercel – Vercel](https://vercel.com/changelog/build-mcp-server-with-nuxt)
> 
> 翻译时间：2026-04-23 05:05
