---
title: Vercel Functions公测支持WebSocket双向通信
title_original: WebSocket support is now in Public Beta - Vercel
date: '2026-06-22'
source: Vercel Blog
source_url: https://vercel.com/changelog/websocket-support-is-now-in-public-beta
author: ''
summary: Vercel宣布其Functions功能现已进入公测阶段，支持WebSocket连接，实现客户端与服务器端的双向实时通信。该功能适用于交互式AI流式传输、聊天和协作应用等场景。WebSocket连接运行于Fluid
  compute之上，采用Active CPU定价模式，仅对消息处理时间计费，空闲连接不收费。开发者可使用标准Node.js库（如ws、Socket.IO）快速部署，无需额外配置。
categories:
- AI基础设施
tags:
- Vercel
- WebSocket
- 实时通信
- Serverless
- Node.js
draft: false
translated_at: '2026-06-23T06:09:33.121811'
---

Vercel Functions 现在可以支持 WebSocket 连接，实现客户端与 Vercel 服务端代码之间的双向通信。

使用 WebSocket 实现实时功能，例如交互式 AI 流式传输、聊天和协作应用。

WebSocket 连接运行于 Fluid compute 之上，并遵循与其他 Function 调用相同的限制和定价。采用 Active CPU 定价模式，计费仅适用于 Function 处理消息的时间，而非空闲连接时间。

您可以使用标准 Node.js 库提供 WebSocket 连接，无需额外配置：

```
1import express from 'express';2import { createServer } from 'http';3import { WebSocketServer } from 'ws';4
5const app = express();6const server = createServer(app);7const wss = new WebSocketServer({ server });8
9wss.on('connection', (ws) => {10  ws.on('message', (data) => {11    ws.send(data);12  });13});14
15export default server;
```

使用 Express 和 ws 库构建的 Node.js WebSocket 服务器，作为 Vercel Function 部署

也支持 Socket.IO 等更高级的库。

阅读文档开始使用。

---

> 本文由AI自动翻译，原文链接：[WebSocket support is now in Public Beta - Vercel](https://vercel.com/changelog/websocket-support-is-now-in-public-beta)
> 
> 翻译时间：2026-06-23 06:09
