---
title: Vercel logs CLI 命令升级，支持历史日志查询与智能体工作流
title_original: vercel logs CLI command now optimized for agents with historical log
  querying - Vercel
date: '2026-02-10'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-logs-cli-command-now-optimized-for-agents-with-historical-log
author: ''
summary: Vercel 重构了其 CLI 中的 `vercel logs` 命令，新增了强大的历史日志查询功能，并针对智能体（Agent）工作流进行了优化。更新后的命令支持跨项目查询，可按项目、部署ID、请求ID及任意字符串进行筛选，便于精准定位问题。默认使用
  git 上下文，在项目目录中运行时自动限定日志范围为当前代码仓库，简化了开发调试流程。这一增强功能既适用于生产环境问题排查，也便于构建自动化监控工作流，提升了开发者在
  Vercel 平台上的日志检索效率与控制精度。
categories:
- AI基础设施
tags:
- Vercel
- 命令行工具
- 日志查询
- 开发者工具
- 智能体工作流
draft: false
translated_at: '2026-02-11T04:33:56.140117'
---

`vercel logs` 命令已重构，具备更强大的查询能力，其设计充分考虑了 Agent（智能体）工作流。您现在可以跨项目查询历史日志，并按特定条件（如项目、部署ID、请求ID及任意字符串）进行筛选，以精准定位所需信息。

![](/images/posts/95fc4eac01ae.jpg)

![](/images/posts/329131939611.jpg)

更新后的命令默认使用 git 上下文，当在项目目录中运行时，会自动将日志范围限定于您当前的代码仓库。这使得在开发过程中调试问题变得轻松，无需手动指定项目详情。

无论您是在调试生产环境问题，还是构建自动化监控工作流，增强的筛选功能都能让您精确控制跨 Vercel 项目的日志检索。

了解 Vercel CLI 及 `vercel logs` 命令。

---

> 本文由AI自动翻译，原文链接：[vercel logs CLI command now optimized for agents with historical log querying - Vercel](https://vercel.com/changelog/vercel-logs-cli-command-now-optimized-for-agents-with-historical-log)
> 
> 翻译时间：2026-02-11 04:33
