---
title: Parallel 登陆 Vercel Agent Marketplace，为 AI 应用提供网络工具
title_original: Parallel joins the Vercel Agent Marketplace - Vercel
date: '2026-02-04'
source: Vercel Blog
source_url: https://vercel.com/changelog/parallel-joins-the-vercel-agent-marketplace
author: ''
summary: Parallel 已正式加入 Vercel Agent Marketplace，为开发者提供专为 LLM 驱动应用设计的网络工具和智能体服务，包括搜索、提取、监控等功能。通过与
  Vercel 的深度集成，开发者可以使用单一 API 密钥调用 Parallel 的所有产品，并通过 Vercel 账户统一管理账单。该集成旨在让 AI 智能体能够访问开放网络，执行信息查询、数据提取等任务，同时通过优化返回结果减少
  LLM 的交互次数，从而降低开发成本与延迟。
categories:
- AI基础设施
tags:
- Vercel
- AI Agent
- LLM
- API集成
- 开发者工具
draft: false
translated_at: '2026-02-05T04:16:28.929340'
---

Parallel 现已登陆 **Vercel Agent Marketplace**，并提供原生集成支持。

Parallel 提供专为 LLM（大语言模型）驱动应用设计的网络工具和 Agent（智能体），包括搜索、提取、任务、查找和监控功能。与 Vercel 的集成提供了一个可在所有 Parallel 产品中通用的单一 API 密钥，账单直接通过您的 Vercel 账户处理。

对于在 Vercel 上构建 AI 功能的开发者，Parallel 能让 Agent（智能体）访问开放网络，以执行回答问题、监控变化和提取结构化数据等任务。由于 Parallel 返回的结果针对 LLM（大语言模型）使用进行了优化，您的 Agent（智能体）可以用更少的往返次数完成任务，从而降低成本和延迟。

```
1import Parallel from "parallel-web";2
3const client = new Parallel({ apiKey: process.env.PARALLEL_API_KEY });4
5async function main() {6    const search = await client.beta.search({7        objective: "When was the United Nations established? Prefer UN's websites.",8        search_queries: [9            "Founding year UN",10            "Year of founding United Nations"11        ],12        max_results: 10,13        excerpts: { max_chars_per_result: 10000 },14    });15
16    console.log(search.results);17}18
19main().catch(console.error);
```

**数分钟内执行您的首次 API 调用**

从 **Marketplace** 安装 Parallel，或部署 **Next.js 模板**，即可亲身体验 Parallel 的网络研究 API 与 Vercel 的集成效果。

---

> 本文由AI自动翻译，原文链接：[Parallel joins the Vercel Agent Marketplace - Vercel](https://vercel.com/changelog/parallel-joins-the-vercel-agent-marketplace)
> 
> 翻译时间：2026-02-05 04:16
