---
title: Vercel MCP正式支持Devin、Raycast、Windsurf和Goose四大AI客户端
title_original: Devin, Raycast, Windsurf, and Goose now supported on Vercel MCP -
  Vercel
date: '2025-08-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/devin-raycast-windsurf-and-goose-now-supported-on-vercel-mcp
author: ''
summary: Vercel宣布其官方模型上下文协议（MCP）服务器现已支持Devin、Raycast、Windsurf和Goose四大AI客户端。出于安全考虑，目前仅限经过Vercel审核批准的客户端接入。文章详细介绍了在每个客户端中配置和安装Vercel
  MCP的具体步骤，包括在Devin的MCP市场中搜索安装、在Raycast中通过HTTP传输方式添加服务器、在Windsurf的配置文件中添加代码片段，以及Goose的一键安装方式。通过Vercel
  MCP，用户可授权AI智能体访问受保护的部署、分析构建日志等Vercel平台资源，从而增强AI工具与开发基础设施的集成能力。
categories:
- AI基础设施
tags:
- Vercel
- MCP
- AI工具集成
- 开发工具
- 模型上下文协议
draft: false
translated_at: '2026-04-02T05:06:08.590657'
---

您现在可以使用Devin、Raycast、Windsurf和Goose配合Vercel MCP，这是我们的官方模型上下文协议（MCP）服务器。出于安全考虑，Vercel MCP目前仅支持经过Vercel审核批准的AI客户端。

请按照以下步骤开始使用每个客户端：

### 链接到标题Devin

1.  导航至Devin的`设置 > MCP市场`
2.  搜索`Vercel`并选择该MCP
3.  点击`安装`

导航至Devin的`设置 > MCP市场`

搜索`Vercel`并选择该MCP

点击`安装`

### 链接到标题Raycast

1.  运行`安装服务器`命令
2.  输入以下详细信息：
    *   `名称`：`Vercel`
    *   `传输方式`：`HTTP`
    *   `URL`：`https://mcp.vercel.com`
3.  点击`安装`

运行`安装服务器`命令

输入以下详细信息：

*   `名称`：`Vercel`
*   `传输方式`：`HTTP`
*   `URL`：`https://mcp.vercel.com`

`名称`：`Vercel`

`传输方式`：`HTTP`

`URL`：`https://mcp.vercel.com`

### 链接到标题Windsurf

1.  将以下代码片段添加到您的`mcp_config.json`文件中

将以下代码片段添加到您的`mcp_config.json`文件中

```
1{2  "mcpServers": {3    "vercel": {4      "serverUrl": "https://mcp.vercel.com"5    }6  }7}
```

### 链接到标题Goose

1.  点击`此处`一键安装Vercel MCP。

点击`此处`一键安装Vercel MCP。

通过Vercel MCP，您可以授予Agent（智能体）访问受保护部署、分析构建日志等权限。

阅读更多关于使用AI工具与Vercel MCP的信息。

连接到Vercel MCP

阅读文档以了解更多关于该服务器的信息

开始使用

---

> 本文由AI自动翻译，原文链接：[Devin, Raycast, Windsurf, and Goose now supported on Vercel MCP - Vercel](https://vercel.com/changelog/devin-raycast-windsurf-and-goose-now-supported-on-vercel-mcp)
> 
> 翻译时间：2026-04-02 05:06
