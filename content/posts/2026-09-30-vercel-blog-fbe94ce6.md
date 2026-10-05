---
title: Vercel Sandbox now supports Secure Compute - Vercel
title_original: Vercel Sandbox now supports Secure Compute - Vercel
date: '2026-09-30'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-sandbox-now-supports-secure-compute
author: ''
summary: '[翻译失败，原文如下]


  Vercel Sandbox now supportsSecure Compute, connecting sandboxes to a team''s dedicated
  network. Public-internet traffic exits through the ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-05T08:02:33.917049'
---

[翻译失败，原文如下]

Vercel Sandbox now supportsSecure Compute, connecting sandboxes to a team's dedicated network. Public-internet traffic exits through the network's static IPs, and sandboxes can reach private resources in an AWS VPC through VPC peering.

You can attach a sandbox to your network in your code or via the CLI.

In your code, pass an existing Secure Compute network ID when creating a sandbox:

```
1import { Sandbox } from '@vercel/sandbox';2
3const sandbox = await Sandbox.create({4  networkId: '3k9x7m2p5q8w1z4n',5});
```

In the CLI, append--network-idand your network id value when you run the sandbox create command.

Existing sandboxes can attach to or change networks withsandbox.update(). The change takes effect on the next session. A running session keeps its current network until it stops.

Available to Enterprise teams with Secure Compute.

Learn more in theSandbox documentation.

## Contributors

Eric Dodds

---

> 本文由AI自动翻译，原文链接：[Vercel Sandbox now supports Secure Compute - Vercel](https://vercel.com/changelog/vercel-sandbox-now-supports-secure-compute)
> 
> 翻译时间：2026-10-05 08:02
