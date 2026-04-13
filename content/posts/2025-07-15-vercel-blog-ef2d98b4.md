---
title: MCP Adapter 1.0.0 新增OAuth支持，强化MCP服务器安全
title_original: OAuth support added to MCP Adapter - Vercel
date: '2025-07-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/oauth-support-added-to-mcp-adapter
author: ''
summary: MCP Adapter 1.0.0版本正式加入对MCP Authorization规范的支持，为MCP服务器提供OAuth身份验证保护。该版本引入了符合OAuth标准的授权流程辅助函数、用于保护路由的`withMcpAuth`包装器，并提供了与Better
  Auth、Clerk、Descope、Stytch和WorkOS等主流身份验证提供商的一键部署示例。开发者可通过简单的代码集成，快速为MCP服务器添加令牌验证和权限控制功能，同时利用`protectedResourceHandler`公开资源服务器元数据，确保客户端合规访问。文章还提供了基于Next.js的模板和合作伙伴的入门指南，帮助开发者快速在Vercel上构建安全的MCP服务器。
categories:
- AI基础设施
tags:
- MCP
- OAuth
- 身份验证
- Vercel
- 服务器安全
draft: false
translated_at: '2026-04-13T05:00:53.438219'
---

使用MCP Adapter的1.0.0版本，通过OAuth来保护您的MCP服务器，该版本现已包含对MCP Authorization规范的官方支持。此版本引入了：

- 用于符合OAuth标准的授权流程的辅助函数
- 一个新的 `withMcpAuth` 包装器，用于保护路由
- 与流行身份验证提供商（如Better Auth、Clerk、Descope、Stytch和WorkOS）一键部署的示例

**用于符合OAuth标准的授权流程的辅助函数**

**一个新的 `withMcpAuth` 包装器，用于保护路由**

**与流行身份验证提供商（如Better Auth、Clerk、Descope、Stytch和WorkOS）一键部署的示例**

以下是如何在您的MCP服务器中集成身份验证的示例：

```
1import { createMcpHandler, withMcpAuth } from 'mcp-handler';2
3const handler = createMcpHandler((server) => {4  server.tool(5    'roll_dice',6    'Rolls an N-sided die',7    { sides: z.number().int().min(2) },8    async ({ sides }) => {9      const value = 1 + Math.floor(Math.random() * sides);10      return { content: [{ type: 'text', text: `🎲 You rolled a ${value}!` }] };11    }12  );13})14
15const verifyToken = async (16  req: Request,17  bearerToken?: string,18) => { 19  if (!bearerToken) return undefined;20
21  const isValid = bearerToken === '123';22  if (!isValid) return undefined;23
24  return {25    token: bearerToken,26    scopes: ['read:stuff'],27    clientId: 'client123',28  };29};30
31const authHandler = withMcpAuth(handler, verifyToken, {32  required: true, 33});34
35export { authHandler as GET, authHandler as POST };
```

此外，使用 `protectedResourceHandler` 来为合规的客户端公开资源服务器元数据。在MCP Auth文档中了解更多信息。

### 开始构建安全的MCP服务器

通过克隆我们的Next.js MCP模板来部署一个示例MCP服务器，或者探索我们身份验证合作伙伴的入门集成：

- Better Auth
- Clerk
- Descope
- Stytch
- WorkOS

**Better Auth**

**Clerk**

**Descope**

**Stytch**

**WorkOS**

**使用Next.js的MCP服务器**

开始在Vercel上构建您的第一个MCP服务器。

**立即部署**

---

> 本文由AI自动翻译，原文链接：[OAuth support added to MCP Adapter - Vercel](https://vercel.com/changelog/oauth-support-added-to-mcp-adapter)
> 
> 翻译时间：2026-04-13 05:00
