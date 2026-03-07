---
title: Chat SDK新增表格渲染与流式Markdown处理功能
title_original: Chat SDK adds table rendering and streaming markdown - Vercel
date: '2026-03-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adds-table-rendering-and-streaming-markdown
author: ''
summary: Vercel的Chat SDK最新更新引入了两项重要功能：一是新增Table()组件，可在所有平台适配器中原生渲染表格，SDK会自动将表格转换为各平台（如Slack、Teams、Discord等）支持的最佳格式；二是全面改进了流式Markdown的处理，现在支持在流式传输过程中实时将Markdown语法转换为各平台的原生格式（如粗体、斜体等），而非显示原始标记符号，从而提升了消息的实时渲染体验。这些改进使得开发者无需针对不同平台进行单独适配，更新至最新SDK即可使用。
categories:
- AI基础设施
tags:
- Chat SDK
- Vercel
- 表格渲染
- 流式Markdown
- 跨平台适配
draft: false
translated_at: '2026-03-07T04:33:36.118065'
---

Chat SDK 现已支持在所有平台适配器中原生渲染表格，并在流式传输过程中将 Markdown 转换为各平台的原生格式。

`Table()` 组件是 Chat SDK 中的一个新卡片元素，它为您提供了一个简洁、可组合的 API，用于在所有平台适配器中渲染表格。只需传入表头和行数据，Chat SDK 会处理其余工作。

```
1import { Table } from "chat";2
3await thread.post(4  Table({5    headers: ["Model", "Latency", "Cost"],6    rows: [7      ["claude-4.6-sonnet", "1.2s", "$0.003"],8      ["gpt-4.1", "0.9s", "$0.005"],9    ],10  })11);
```

适配器层会将表格转换为每个平台支持的最佳格式。

Slack 渲染 Block Kit 表格块，Teams 和 Discord 使用 GFM Markdown 表格，Google Chat 使用等宽文本部件，而 Telegram 将表格转换为代码块。GitHub 和 Linear 已通过其 Markdown 管道支持表格，并继续像以前一样工作。普通的 Markdown 表格（不使用 `Table()`）也会通过相同的管道进行转换。

流式 Markdown 的处理也得到了全面改进。Slack 的原生流式路径现在可以在响应到达时实时渲染粗体、斜体、列表和其他格式，而不是等到消息完成时才解析。所有其他平台都使用备用流式路径，因此流式文本现在会在每次中间编辑时通过每个适配器的 Markdown 到原生格式的转换管道。以前，这些适配器接收的是原始的 Markdown 字符串，因此用户在最终消息之前看到的是字面上的 `**bold**` 语法。

没有平台特定渲染功能的适配器现在包含了改进的默认设置，因此新的格式化功能可以在所有平台上工作，而无需逐个适配器进行更新。

更新到最新的 Chat SDK 即可开始使用，并查看相关文档。

---

> 本文由AI自动翻译，原文链接：[Chat SDK adds table rendering and streaming markdown - Vercel](https://vercel.com/changelog/chat-sdk-adds-table-rendering-and-streaming-markdown)
> 
> 翻译时间：2026-03-07 04:33
