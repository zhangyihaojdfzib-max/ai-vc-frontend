---
title: Vercel CLI 更新：链接时保留本地环境变量
title_original: Preserve local environment variables when linking with the Vercel
  CLI - Vercel
date: '2026-06-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/preserve-local-environment-variables-when-linking-with-the-vercel-cli
author: ''
summary: Vercel CLI 最新版本在执行 `vercel link` 命令时，会保留 `.env.local` 文件中的已有变量，仅更新或追加 `VERCEL_OIDC_TOKEN`，不再覆盖其他内容。用户可通过
  `pnpm i -g vercel@latest` 更新后使用该功能。这一改进避免了链接操作导致的环境变量丢失问题，提升了开发体验。
categories:
- AI基础设施
tags:
- Vercel
- CLI
- 环境变量
- 开发工具
- 部署
draft: false
translated_at: '2026-06-27T05:53:29.889953'
---

Vercel CLI 现在在执行 `vercel link` 时会保留你的 `.env.local` 文件。此前，链接操作可能会覆盖文件中已有的变量。CLI 现在会更新 `VERCEL_OIDC_TOKEN`（如果存在），或者在缺失时追加该变量，而不会改动其他内容。

运行 `pnpm i -g vercel@latest` 进行更新，然后执行 `vercel link` 即可开始使用。更多信息请参阅 `vercel link` 文档。

## 准备部署？

加载状态中…

---

> 本文由AI自动翻译，原文链接：[Preserve local environment variables when linking with the Vercel CLI - Vercel](https://vercel.com/changelog/preserve-local-environment-variables-when-linking-with-the-vercel-cli)
> 
> 翻译时间：2026-06-27 05:53
