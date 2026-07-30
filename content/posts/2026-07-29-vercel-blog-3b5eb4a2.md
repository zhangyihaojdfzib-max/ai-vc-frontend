---
title: Vercel 推出 CLI 集成发现与安装功能
title_original: Discover and install eve integrations from the CLI - Vercel
date: '2026-07-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/discover-and-install-eve-integrations-from-the-cli
author: ''
summary: Vercel 宣布用户现在可以直接从 eve CLI 发现并安装 eveagents 的集成，包括官方目录和第三方来源。通过 `eve add`
  命令可安装浏览器扩展、Slack 频道、Vercel MCP 连接等集成，集成文件会直接写入项目。新增的 `eve registry` 命令支持列出、搜索和查看集成，并允许添加第三方注册表。文章强调集成应视为项目代码，需审查差异并添加信任来源。
categories:
- AI基础设施
tags:
- Vercel
- CLI
- 集成
- eveagents
- 开发者工具
draft: false
translated_at: '2026-07-30T05:16:57.562263'
---

您现在可以直接从 eve CLI 发现并安装 eveagents 的集成。集成来自官方 eve 目录和第三方来源。

在 eve 项目中运行 `eve add` 来安装集成：

```
eve add extension/agent-browser
eve add channel/slack
eve add connection/vercel
eve add instrumentation/braintrust
```

添加 Agent 浏览器扩展、Slack 频道、Vercel MCP 连接以及 Braintrust 检测工具

集成会将其文件直接写入您的项目，并可以添加 eve agent 使用的任何内容，从单个工具到频道再到完整扩展。在运行您的 agent 之前，请检查生成的文件并添加任何必要的配置。

使用新的 `eve registry` 命令查找集成：

- `eve registry list`：列出可用的集成。
- `eve registry search <term>`：在目录中搜索某项能力，例如 `browser`。
- `eve registry view <name>`：在安装前检查集成。

您也可以浏览 `integrations` 目录来查看官方目录。

使用命名空间和 URL 模板添加第三方来源：

```
eve registry add @acme=https://registry.acme.com/r/{name}.json
```

然后通过 `eve add @acme/analytics` 从该来源安装。注册表使用 shadcn 注册表格式，因此任何兼容的注册表都可以使用。

您也可以直接传递集成 URL，无需配置来源：

```
eve add https://registry.acme.com/r/analytics.json
```

集成可以添加依赖项并写入文件，因此请将其视为项目代码。添加您信任的来源，使用 `eve registry view` 检查集成，并在运行 agent 之前审查项目差异。

开始使用前，请阅读文档并浏览目录。

## 贡献者

Ben Sabic

---

> 本文由AI自动翻译，原文链接：[Discover and install eve integrations from the CLI - Vercel](https://vercel.com/changelog/discover-and-install-eve-integrations-from-the-cli)
> 
> 翻译时间：2026-07-30 05:16
