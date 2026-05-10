---
title: Vapi在Vercel上重建MCP服务器，提升AI Agent能力
title_original: Vapi MCP server hosted on Vercel
date: '2025-05-21'
source: Vercel Blog
source_url: https://vercel.com/blog/vapi-mcp-server-on-vercel
author: ''
summary: Vapi在Vercel上重建了其MCP服务器，利用Vercel的MCP适配器、Fluid Compute等产品套件，实现了对SSE和Streamable
  HTTP传输协议的原生支持。该服务器使用户能够创建实时语音Agent、自动化测试、分析对话记录并构建工作流。Vercel的MCP适配器简化了部署过程，Fluid
  Compute优化了计算资源利用效率。Vapi全面采用Vercel作为MCP服务器基础设施，从而更专注于产品开发而非基础设施管理。
categories:
- AI基础设施
tags:
- MCP服务器
- Vapi
- Vercel
- AI Agent
- 基础设施
draft: false
translated_at: '2026-05-10T05:39:04.083124'
---

Vercel 近期发布了一个**模型上下文协议（MCP）适配器**，可让用户在主流框架上快速搭建 MCP 服务器。

**Vapi** 正在构建用于创建实时语音 Agent（智能体）的 API。他们负责编排、扩展和电话集成，提供完全与模型无关且可互换的接口来构建 Agent（智能体）。

Vapi 在 Vercel 上重建了他们的 **MCP 服务器**，使用户能够创建 Agent（智能体）、自动化测试、分析对话记录、构建工作流，并让 Agent（智能体）访问 Vapi 的所有端点。

## 什么是 MCP 服务器？

MCP 服务器是用于 AI 模型访问外部能力的集成方案。

与其将 MCP 视为 REST API，不如将其看作是为帮助 AI 完成特定任务而量身定制的工具包。单个 MCP 工具背后可能涉及多个 API 及其他业务逻辑。

如果你已熟悉 **AI 中的工具调用**，MCP 就是一种调用托管在不同服务器上的工具的方式。

## 迁移至 Vercel

Vapi 的 MCP 服务器此前仅支持 **服务器发送事件（SSE）** 传输协议。通过使用 **Vercel 的 MCP 适配器**重建 MCP 服务器，Vapi 现在能够原生支持 SSE 传输协议和更新的 **Streamable HTTP 传输协议**。

借助 Vercel MCP 适配器，重建服务器的过程得以加速。与其他编写和部署 MCP 服务器的方式相比，MCP 适配器是一个简单的软件包，任何人都可将其放入任何兼容 Node.js 框架的路由端点中。它利用了**广泛使用的 Web 标准**，并且在部署到 Vercel 后，可使 MCP 客户端即时连接并使用该服务器。

部署在 Vercel 上使 Vapi 能够利用 **Fluid Compute**。Fluid Compute 可最大化可用计算时间和资源，从而显著优化计算占用和效率。具体到 MCP 工作负载，Fluid 会在扩展新资源之前智能地复用现有资源来处理多个 MCP 客户端连接。

## 结论

Vapi 正全面采用 Vercel 作为其 MCP 服务器基础设施。Vercel 的产品套件，包括 MCP 适配器、**可观测性**、Fluid Compute 和 **防火墙**，使 Vapi 能够更专注于构建产品，而非管理基础设施。

立即查看 **Vapi 的 MCP 服务器**、他们的**博客文章**，并通过我们的 **Next.js MCP 模板**开始部署 MCP 服务器。

---

> 本文由AI自动翻译，原文链接：[Vapi MCP server hosted on Vercel](https://vercel.com/blog/vapi-mcp-server-on-vercel)
> 
> 翻译时间：2026-05-10 05:39
