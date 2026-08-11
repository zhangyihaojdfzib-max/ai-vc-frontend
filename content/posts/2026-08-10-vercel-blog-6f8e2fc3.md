---
title: Vercel Functions 支持 Bun.serve 入口点
title_original: Bun runtime for Vercel Functions now accepts Bun.serve as an entrypoint
  - Vercel
date: '2026-08-10'
source: Vercel Blog
source_url: https://vercel.com/changelog/bun-serve-entrypoint-for-vercel-functions
author: ''
summary: Vercel Functions 的 Bun 运行时现已支持将 Bun.serve() 作为函数入口点，包括 WebSocket 处理器。开发者可在本地使用
  Bun 运行服务器，无需框架包装即可直接部署。通过设置 bunVersion 启用该功能，支持静态、动态和通配符路由，并允许 WebSocket 连接在 Fluid
  compute 上运行，采用 Active CPU 定价，按处理消息时间计费。
categories:
- 技术趋势
tags:
- Vercel
- Bun
- WebSocket
- Serverless
- 部署
draft: false
translated_at: '2026-08-11T03:38:05.096742'
---

Vercel Functions 的Bun运行时现在支持将Bun.serve()作为函数入口点，包括 WebSocket 处理器。你在本地使用 Bun 运行的服务器将原样部署，无需包装在框架中。

通过在vercel.json中设置"bunVersion": "1.x"来启用该运行时。

### 复制链接到标题部署基于路由的服务器

在项目根目录的server.ts中创建一个带有routes映射的服务器。

```
1Bun.serve({2  routes: {3    "/api/boolean": () => Response.json({ success: true }),4    "/api/users/:id": (request) => Response.json({ user: request.params.id }),5    "/*": () => new Response("api catch-all"),6  },7});
```

部署到 Vercel 的 Bun.serve 服务器，支持静态、动态和通配符路由

### 复制链接到标题接受 WebSocket 连接

添加一个websocket处理器，并在fetch中调用server.upgrade(request)来升级匹配的请求。服务器的其余部分保持不变。

```
1Bun.serve({2  routes: {3    "/health": Response.json({ status: "ok" }),4  },5  fetch(request, server) {6    const { pathname } = new URL(request.url);7    if (pathname === "/ws" && server.upgrade(request)) {8      return;9    }10    return new Response("Not found", { status: 404 });11  },12  websocket: {13    message(socket, message) {14      socket.send(message);15    },16  },17});
```

WebSocket 处理器将消息回显，fetch 将请求升级到 /ws，并回退到 404

WebSocket 连接在Fluid compute上运行，采用Active CPU定价，因此你只需为处理消息的时间付费，而无需为空闲连接时间付费。一个连接在其生命周期内固定到一个函数实例，单个实例可以处理多个并发连接。使用外部数据存储来协调跨实例的消息。

阅读文档开始使用。

## 贡献者

Eric Dodds

---

> 本文由AI自动翻译，原文链接：[Bun runtime for Vercel Functions now accepts Bun.serve as an entrypoint - Vercel](https://vercel.com/changelog/bun-serve-entrypoint-for-vercel-functions)
> 
> 翻译时间：2026-08-11 03:38
