---
title: Vercel Drives is now generally available - Vercel
title_original: Vercel Drives is now generally available - Vercel
date: '2026-10-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-drives-is-now-generally-available
author: ''
summary: '[翻译失败，原文如下]


  Vercel Drivesis now generally available forVercel Sandboxon Hobby, Pro, and Enterprise.


  A Drive is persistent storage that you mount as ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-26T07:17:29.957568'
---

[翻译失败，原文如下]

Vercel Drivesis now generally available forVercel Sandboxon Hobby, Pro, and Enterprise.

A Drive is persistent storage that you mount as a directory in a Vercel Sandbox. Its files remain available after the sandbox stops, so later runs and other sandboxes can access them by mounting the same Drive.

Use Drives to preserve an agent’s workspace or file-based memory across runs, or to make datasets, models, dependencies, and build artifacts available across sandboxes.

You can also fork a Drive into independent writable Drives. Forks inherit the source Drive's data, region, and maximum size, then store their own changes. Parallel workers can start with the same files and make changes without affecting the original or one another.

```
1import { Sandbox, Drive } from '@vercel/sandbox';2const drive = await Drive.get({ name: 'base-drive' })3
4for (let i = 0; i < 2; i++) {5  const fork = await drive.fork({ name: `worker-${i}` })6  const sandbox = await Sandbox.create({7    mounts: {8      '/data': fork,9    }10  })11  12  await fork.delete()13}14

```

Start parallel workers from the same saved workspace while keeping their changes isolated.

Learn more in theDrives documentation.

---

> 本文由AI自动翻译，原文链接：[Vercel Drives is now generally available - Vercel](https://vercel.com/changelog/vercel-drives-is-now-generally-available)
> 
> 翻译时间：2026-10-26 07:17
