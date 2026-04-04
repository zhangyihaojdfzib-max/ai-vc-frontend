---
title: Vercel MCP服务器推出新工具，助力Agent访问受保护部署
title_original: Agents can now access protected deployments via Vercel’s MCP server
  - Vercel
date: '2025-08-19'
source: Vercel Blog
source_url: https://vercel.com/changelog/give-agents-access-to-protected-deployments-via-vercels-mcp-server
author: ''
summary: Vercel宣布其MCP服务器新增两款工具：get_access_to_vercel_url可生成临时共享URL，让网页抓取或Playwright等Agent工具无需登录凭证即可访问受Vercel身份验证保护的部署；web_fetch_vercel_url则允许Agent直接从受保护的部署中获取内容，绕过常规抓取可能遇到的401或403错误。这些工具旨在简化Agent对安全部署内容的访问流程，提升自动化处理效率。
categories:
- AI基础设施
tags:
- Vercel
- MCP服务器
- Agent工具
- 身份验证
- 网页抓取
draft: false
translated_at: '2026-04-04T04:29:29.128280'
---

Vercel的MCP服务器现已推出两款新工具：

- **get_access_to_vercel_url**：生成一个**可共享的URL**，允许诸如网页抓取或Playwright之类的Agent工具访问受**Vercel身份验证**保护的部署。该URL是临时的，无需登录凭证即可授予访问权限。
- **web_fetch_vercel_url**：允许Agent直接从受**Vercel身份验证**保护的部署中获取内容，即使常规的抓取请求会返回`401 Unauthorized`或`403 Forbidden`错误。

**get_access_to_vercel_url**：生成一个**可共享的URL**，允许诸如网页抓取或Playwright之类的Agent工具访问受**Vercel身份验证**保护的部署。该URL是临时的，无需登录凭证即可授予访问权限。

**web_fetch_vercel_url**：允许Agent直接从受**Vercel身份验证**保护的部署中获取内容，即使常规的抓取请求会返回`401 Unauthorized`或`403 Forbidden`错误。

开始使用**Vercel MCP服务器**。

连接到Vercel MCP

阅读文档以了解更多关于该服务器的信息

开始使用

---

> 本文由AI自动翻译，原文链接：[Agents can now access protected deployments via Vercel’s MCP server - Vercel](https://vercel.com/changelog/give-agents-access-to-protected-deployments-via-vercels-mcp-server)
> 
> 翻译时间：2026-04-04 04:29
