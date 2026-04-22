---
title: Vercel CLI命令现默认关联本地目录，提升开发上下文一致性
title_original: Vercel CLI commands now scoped to local directory - Vercel – Vercel
date: '2026-04-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-cli-commands-now-scope-to-the-local-directory
author: ''
summary: Vercel CLI近期更新（v50.40.0+）调整了部分命令的默认作用域行为。此前，在已关联本地目录中执行如`vc project ls`、`vc
  domains ls`等只读命令时，返回的是用户全局团队下的结果，可能导致本地工作环境与CLI输出脱节。现在，这些命令会自动限定在当前关联的本地目录所属的作用域内，使输出与本地开发上下文保持一致。用户仍可通过`--scope`标志手动指定其他团队来覆盖此默认行为。此举旨在优化开发者体验，减少因作用域混淆导致的误操作。建议用户运行`pnpm
  i -g vercel@latest`更新至最新版本以使用此功能。
categories:
- AI基础设施
tags:
- Vercel
- 命令行工具
- 开发工具
- 前端部署
- 开发者体验
draft: false
translated_at: '2026-04-22T05:05:13.497121'
---

诸如 `vc project ls` 和 `vc domains ls` 等命令现在会自动使用您关联的本地目录的作用域，而不再默认使用您的全局团队。

此前，在关联的代码仓库内查询项目或域名会返回全局结果，导致您当前的工作环境与 CLI 输出之间出现意料之外的脱节。此次更新使只读命令与您的本地上下文保持一致，不过您仍可通过传递 `--scope` 标志手动覆盖目标团队。

运行 `pnpm i -g vercel@latest` 以更新至最新的 Vercel CLI（至少为 v50.40.0 版本）。

---

> 本文由AI自动翻译，原文链接：[Vercel CLI commands now scoped to local directory - Vercel – Vercel](https://vercel.com/changelog/vercel-cli-commands-now-scope-to-the-local-directory)
> 
> 翻译时间：2026-04-22 05:05
