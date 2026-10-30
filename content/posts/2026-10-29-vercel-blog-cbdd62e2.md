---
title: Vercel Flags starts 7x faster and no longer extends function duration - Vercel
title_original: Vercel Flags starts 7x faster and no longer extends function duration
  - Vercel
date: '2026-10-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-flags-starts-7x-faster-and-no-longer-extends-function-duration
author: ''
summary: '[翻译失败，原文如下]


  On Vercel, theVercel FlagsSDK now initializes faster on cold starts, and usage reporting
  no longer keeps functions running after the resp...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:47:56.948241'
---

[翻译失败，原文如下]

On Vercel, theVercel FlagsSDK now initializes faster on cold starts, and usage reporting no longer keeps functions running after the response.

### Copy link to headingFaster cold starts

Two changes speed up SDK initialization on cold starts:

- The SDK loads and parses the flags datafile bundled with your deployment as soon as the client is created, so it’s ready before your code evaluates its first flag.
- Every function invocation now includes the current datafile revision, so the SDK can check whether the bundled datafile is up to date without a network request.

The SDK loads and parses the flags datafile bundled with your deployment as soon as the client is created, so it’s ready before your code evaluates its first flag.

Every function invocation now includes the current datafile revision, so the SDK can check whether the bundled datafile is up to date without a network request.

In internal testing, eliminating the network wait reduced p75 cold-start SDK initialization time from over 70 ms to 10 ms, roughly 7x faster.

After initialization, flag reads are effectively instant. Across cold and warm invocations, p99 flag-read latency is under 1 ms.

### Copy link to headingUsage reporting no longer extends function duration

The SDK previously usedwaitUntilfor usage reporting, keeping functions running after the response was sent. It now passes usage events to the Vercel runtime, so reporting no longer adds to function duration.

Update@flags-sdk/vercelto version 1.5.3 or later and redeploy your application:

```
pnpm add @flags-sdk/vercel@latest
```

Learn more in theFlags SDK documentation.

---

> 本文由AI自动翻译，原文链接：[Vercel Flags starts 7x faster and no longer extends function duration - Vercel](https://vercel.com/changelog/vercel-flags-starts-7x-faster-and-no-longer-extends-function-duration)
> 
> 翻译时间：2026-10-30 08:47
