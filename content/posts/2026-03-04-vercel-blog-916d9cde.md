---
title: Vercel 全面支持 MCP 应用开发与部署
title_original: MCP Apps support on Vercel - Vercel
date: '2026-03-04'
source: Vercel Blog
source_url: https://vercel.com/changelog/mcp-apps-support-on-vercel
author: ''
summary: Vercel 平台现已支持构建和部署 MCP（Model Context Protocol）应用，并全面集成 Next.js。MCP 应用是一种与供应商无关的嵌入式
  UI 开放标准，运行在 iframe 中，通过共享桥接和 `postMessage` 使用 `ui/*` JSON-RPC 与任何兼容主机（如 ChatGPT）通信。该架构使单一
  UI 能在不同平台通用，无需针对特定平台集成。结合 Vercel 和 Next.js，开发者可利用服务器端渲染和 React 服务器组件，构建高性能、可移植的智能体界面。
categories:
- AI基础设施
tags:
- Vercel
- MCP
- Next.js
- AI应用开发
- 前端架构
draft: false
translated_at: '2026-03-05T04:47:22.180411'
---

团队现可在 Vercel 上构建和部署 MCP 应用，并全面支持 Next.js。

MCP 应用类似于 ChatGPT 应用，但它是一种与供应商无关的嵌入式 UI 开放标准。它们运行在 iframe 中，并通过共享桥接与任何兼容主机（例如 ChatGPT）进行通信。

该架构通过 `postMessage` 使用 `ui/*` JSON-RPC，使得单一 UI 能够在任何兼容主机上运行，无需针对特定平台进行集成。

通过将此标准与 Vercel 上的 Next.js 结合，开发者可以利用服务器端渲染（SSR）和 React 服务器组件来构建可移植、高性能的 Agent（智能体）界面。

部署模板或查阅文档以了解更多信息。

---

> 本文由AI自动翻译，原文链接：[MCP Apps support on Vercel - Vercel](https://vercel.com/changelog/mcp-apps-support-on-vercel)
> 
> 翻译时间：2026-03-05 04:47
