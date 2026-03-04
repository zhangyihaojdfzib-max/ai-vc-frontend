---
title: Vercel Sandbox 现支持创建时设置环境变量
title_original: Vercel Sandbox now accepts environment variables at creation - Vercel
date: '2026-03-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-sandbox-now-accepts-environment-variables-at-creation
author: ''
summary: Vercel 宣布其 Sandbox SDK 和 CLI 现已支持在创建沙盒时预设环境变量。这些变量将自动应用于后续的每个命令执行中，例如安装依赖、构建项目或启动开发服务器，简化了多步骤流程的配置。用户可以在
  `Sandbox.create()` 中定义全局变量，并在必要时通过单个命令的 `env` 参数进行局部覆盖。这一更新提升了开发体验的便捷性和一致性，开发者需更新至最新的
  `@vercel/sandbox` 包以使用此功能。
categories:
- AI基础设施
tags:
- Vercel
- 开发工具
- 环境变量
- SDK
- CLI
draft: false
translated_at: '2026-03-04T04:45:23.166452'
---

Vercel Sandbox SDK 和 CLI 现已支持在创建沙盒时设置环境变量，这些变量将自动应用于每个命令。

在 Vercel Sandbox 中运行多步骤流程时，例如安装依赖、构建项目或启动开发服务器，每个步骤通常需要相同的环境变量。现在，这些变量可通过每次 `runCommand` 调用自动获取。

```
1await using sandbox = await Sandbox.create({2  env: { HELLO: "world", DEBUG: "true" },3});4
56await sandbox.runCommand({ cmd: "node", args: ["-p", "process.env.HELLO"] });7
89await sandbox.runCommand({ cmd: "node", args: ["-p", "process.env.DEBUG"], env: { DEBUG: "false" } });
```

传递给 `Sandbox.create()` 的环境变量会自动被所有命令继承。必要时，仍可通过 `runCommand` 中针对单个命令的 `env` 参数覆盖特定值。

请更新至最新的 Sandbox CLI 和 SDK，运行 `npm i @vercel/sandbox` 即可开始使用。

---

> 本文由AI自动翻译，原文链接：[Vercel Sandbox now accepts environment variables at creation - Vercel](https://vercel.com/changelog/vercel-sandbox-now-accepts-environment-variables-at-creation)
> 
> 翻译时间：2026-03-04 04:45
