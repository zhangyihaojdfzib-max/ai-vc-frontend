---
title: All Sandbox runtimes now use Vercel Managed Images
title_original: All Sandbox runtimes now use Vercel Managed Images
date: '2026-11-24'
source: Vercel Blog
source_url: https://vercel.com/changelog/all-sandbox-runtimes-now-use-vercel-managed-images
author: ''
summary: '[翻译失败，原文如下]


  AllVercel Sandboxruntimes now use Vercel Managed Images (VMIs).


  Legacy runtimes, such asnode22, now use the open-source images in thever...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-27T10:43:05.006622'
---

[翻译失败，原文如下]

AllVercel Sandboxruntimes now use Vercel Managed Images (VMIs).

Legacy runtimes, such asnode22, now use the open-source images in thevercel/sandbox repository, distributed through Vercel Container Registry (VCR). Sandboxes created with these now come with 64 GB of storage and use the same infrastructure as sandboxes powered by VCR.

The universal image is released nightly, and rolling tags such aslatestpick up operating system, dependency, and coding agent updates. Pin an image digest when you need a reproducible environment.

Sandboxes created with version 3 or later of the JavaScript Sandbox SDK usevercel/sandbox/universal:latestby default. The universal image includes Node.js, Python, coding agents such as Claude Code and Pi, and common utilities. You can pull it atvcr.vercel.com/vercel/sandbox/universal:latest.

Learn more in theSandbox documentation.

## Contributors

Kevin Sundstrom

---

> 本文由AI自动翻译，原文链接：[All Sandbox runtimes now use Vercel Managed Images](https://vercel.com/changelog/all-sandbox-runtimes-now-use-vercel-managed-images)
> 
> 翻译时间：2026-11-27 10:43
