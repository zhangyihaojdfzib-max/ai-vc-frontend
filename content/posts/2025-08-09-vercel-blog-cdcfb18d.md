---
title: Cursor现支持Vercel MCP，可在编辑器内直接管理Vercel项目
title_original: Cursor now supported on Vercel MCP - Vercel
date: '2025-08-09'
source: Vercel Blog
source_url: https://vercel.com/changelog/cursor-now-supported-on-vercel-mcp
author: ''
summary: Vercel宣布其官方模型上下文协议（MCP）服务器现已支持Cursor编辑器。通过Vercel MCP，开发者无需离开Cursor即可直接探索项目、检查部署状态、获取日志等。为确保安全，目前仅限经Vercel审核的AI客户端使用。用户可通过一键设置或手动配置mcp.json文件快速连接，并使用Vercel账户登录。这一集成进一步提升了开发者在统一环境中管理全栈项目的效率。
categories:
- AI产品
tags:
- Cursor
- Vercel
- MCP
- 开发工具
- AI集成
draft: false
translated_at: '2026-04-07T04:46:05.582905'
---

![](/images/posts/5219488ef419.jpg)

![](/images/posts/ed9477320109.jpg)

您现在可以在 Cursor 中使用 Vercel MCP，这是我们的官方模型上下文协议（MCP）服务器。为确保安全访问，Vercel MCP 目前仅支持经过 Vercel 审核批准的 AI 客户端。

通过 Vercel MCP，您可以探索项目、检查失败的部署、获取日志等，所有这些都无需离开 Cursor。

要连接，您可以点击此处进行一键设置，或者将以下内容添加到您的 `.cursor/mcp.json` 文件中：

```
1{2  "mcpServers": {3    "vercel": {4      "url": "https://mcp.vercel.com"5    }6  }7}
```

添加后，Cursor 将提示您使用 Vercel 账户登录。

阅读更多关于在 Vercel MCP 中使用 Cursor 的信息。

---

> 本文由AI自动翻译，原文链接：[Cursor now supported on Vercel MCP - Vercel](https://vercel.com/changelog/cursor-now-supported-on-vercel-mcp)
> 
> 翻译时间：2026-04-07 04:46
