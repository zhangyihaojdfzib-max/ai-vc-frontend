---
title: Vercel Sandbox 开放端口8080，控制器端口迁移
title_original: Port 8080 is now available in Vercel Sandboxes - Vercel
date: '2026-05-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/port-8080-is-now-available-in-vercel-sandboxes
author: ''
summary: Vercel 宣布其 Sandbox 产品现在支持打开端口 8080 并将其绑定为入口域名，此前该端口用作控制器端口，现已迁移至端口 23456。用户可以通过简单的
  API 调用创建 Sandbox 实例并指定端口，然后运行如 Python HTTP 服务器等命令。这一更新简化了开发者在沙盒环境中暴露服务的流程，提升了灵活性和易用性。
categories:
- AI基础设施
tags:
- Vercel
- Sandbox
- 端口8080
- 开发者工具
- 云基础设施
draft: false
translated_at: '2026-05-30T05:46:36.494214'
---

Vercel Sandbox 现在允许打开端口 8080 并将其绑定为入口域名。

该端口曾用作控制器端口，现已迁移至端口 23456。

```
1import { Sandbox } from "@vercel/sandbox";2
3const sandbox = await Sandbox.create({4  ports: [8080],5});6
7await sandbox.runCommand({8  cmd: "python3",9  args: ["-m", "http.server", "8080", "--bind", "0.0.0.0"],10  detached: true,11});12
13console.log(`url: ${sandbox.domain(8080)}`);
```

创建一个打开端口 8080 的 Sandbox

在文档中了解更多关于 Sandbox 的信息。

---

> 本文由AI自动翻译，原文链接：[Port 8080 is now available in Vercel Sandboxes - Vercel](https://vercel.com/changelog/port-8080-is-now-available-in-vercel-sandboxes)
> 
> 翻译时间：2026-05-30 05:46
