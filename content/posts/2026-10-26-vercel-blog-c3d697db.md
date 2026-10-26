---
title: Faster pnpm installs - Vercel
title_original: Faster pnpm installs - Vercel
date: '2026-10-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/faster-pnpm-installs
author: ''
summary: '[翻译失败，原文如下]


  pnpm installs on Vercel are now faster, reducing the time spent installing dependencies
  before your build.


  For Pro deployments with rest...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-26T07:41:41.132346'
---

[翻译失败，原文如下]

pnpm installs on Vercel are now faster, reducing the time spent installing dependencies before your build.

For Pro deployments with restored build cache, we observed 14% lower average install times with the optimization enabled.

Vercel now reuses successful dependency verification across deployments. In the best case, when dependencies are unchanged and the previous verification can be reused, installs can complete in milliseconds.

Before:

```
✓ Lockfile passes supply-chain policies (461 entries in 2.5s)Done in 2.8s using pnpm v12.3.4
```

After:

```
✓ Lockfile passes supply-chain policies (verified 58s ago)Done in 135ms using pnpm v12.3.4
```

This improvement is available on all plans and applies automatically, with no configuration required.

---

> 本文由AI自动翻译，原文链接：[Faster pnpm installs - Vercel](https://vercel.com/changelog/faster-pnpm-installs)
> 
> 翻译时间：2026-10-26 07:41
