---
title: Basic build machines are now available on Pro and Enterprise - Vercel
title_original: Basic build machines are now available on Pro and Enterprise - Vercel
date: '2026-09-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/basic-build-machines
author: ''
summary: '[翻译失败，原文如下]


  Pro and Enterprise teams can now select Basic build machines.


  Basic build machines have 2 vCPUs and 8 GB of memory, offering a more cost...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-04T07:07:56.104488'
---

[翻译失败，原文如下]

Pro and Enterprise teams can now select Basic build machines.

Basic build machines have 2 vCPUs and 8 GB of memory, offering a more cost-efficient option for smaller apps or agents that build with fewer resources. New Pro and Enterprise projects still default toElastic build machines, which scale automatically and are recommended for most use cases.

To use Basic build machines, update your project configuration inteam settings,project settings, or with Vercel CLI59.6.0or later:

```
vc project update --build-machine basic
```

Hobby accounts continue to build on the same 2 vCPU machines, now called Basic build machines.

Basic build machines are charged at the same $0.0035 per vCPU per minute, which works out to $0.007 per build minute. See thepricing pageor read thebuild machines documentation.

## Contributors

Jon Vincent,Cody Wong,Pranav Kanchi,Caleb Boyd,Eric Dodds

---

> 本文由AI自动翻译，原文链接：[Basic build machines are now available on Pro and Enterprise - Vercel](https://vercel.com/changelog/basic-build-machines)
> 
> 翻译时间：2026-09-04 07:07
