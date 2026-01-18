---
title: Vercel Sandbox 现已默认使用 Node.js 24 运行时
title_original: Node.js runtime now defaults to version 24 for Vercel Sandbox - Vercel
date: '2026-01-14'
source: Vercel Blog
source_url: https://vercel.com/changelog/node-js-runtime-now-defaults-to-version-24-for-vercel-sandbox
author: ''
summary: Vercel 宣布其 Node.js Sandbox 环境现已默认采用 Node.js 24 作为运行时。对于未明确配置运行时的项目，系统将自动使用此版本，确保开发者能够利用
  Node.js 最新的功能与性能改进。文章提供了示例代码，展示如何在 Sandbox 中验证 Node.js 版本，并建议开发者查阅相关文档以获取更多详细信息。此次更新旨在帮助开发者社区紧跟技术演进，提升开发效率与应用性能。
categories:
- AI基础设施
tags:
- Vercel
- Node.js
- 运行时
- 开发工具
- 云平台
draft: false
translated_at: '2026-01-18T04:39:05.560366'
---

Vercel Sandbox for Node.js 现已默认使用 Node.js 24。这使 Node.js 运行时能与最新的 Node.js 功能和性能改进保持同步。

如果您未明确配置运行时，Sandbox 将使用 Node.js 24（如下所示）。

```
1import { Sandbox } from "@vercel/sandbox";2
3async function main() {4  const sandbox = await Sandbox.create();5  const version = await sandbox.runCommand("node", ["-v"]);6  console.log(`Node.js version: ${await version.stdout()}`);7}8
9main().catch(console.error);
```

阅读Sandbox文档以了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Node.js runtime now defaults to version 24 for Vercel Sandbox - Vercel](https://vercel.com/changelog/node-js-runtime-now-defaults-to-version-24-for-vercel-sandbox)
> 
> 翻译时间：2026-01-18 04:39
