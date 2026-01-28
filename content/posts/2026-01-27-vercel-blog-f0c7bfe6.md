---
title: Vercel CLI 新增 `api` 命令，赋能AI Agent直接访问平台API
title_original: Introducing the vercel api CLI command - Vercel
date: '2026-01-27'
source: Vercel Blog
source_url: https://vercel.com/changelog/introducing-the-vercel-api-cli-command
author: ''
summary: Vercel CLI 在 50.5.1 版本中新增了 `api` 命令，为开发者与AI Agent（如Claude Code）提供了从终端直接访问Vercel全套API的能力。该命令无需额外配置，AI
  Agent在拥有环境和CLI访问权限的情况下即可自动继承用户权限，实现与Vercel平台的无缝交互。用户可通过 `vercel api ls` 列出可用API，交互式构建请求，或直接指定端点发送请求，极大简化了自动化工作流和集成开发过程。
categories:
- AI基础设施
tags:
- Vercel
- CLI工具
- AI Agent
- 开发者工具
- API集成
draft: false
translated_at: '2026-01-28T04:43:06.173008'
---

vercel@50.5.1 新增了一个 `api` 命令，让你可以直接从终端访问 Vercel 的全套 API。

`api` 命令为 AI Agent（智能体）通过 CLI 与 Vercel 交互提供了一个直接访问点。像 Claude Code 这样的 Agent（智能体）无需额外配置即可直接访问 Vercel。如果一个 Agent（智能体）有权访问环境和 Vercel CLI，它将自动继承用户的访问权限。

使用 `vercel api ls` 列出可用的 API，使用 `vercel api` 交互式地构建请求，或直接使用 `vercel api [endpoint] [options]` 发送请求。

通过 `npx vercel@latest api --help` 开始使用。

---

> 本文由AI自动翻译，原文链接：[Introducing the vercel api CLI command - Vercel](https://vercel.com/changelog/introducing-the-vercel-api-cli-command)
> 
> 翻译时间：2026-01-28 04:43
