---
title: Vercel CLI归档部署提速30%：新增split-tgz选项
title_original: CLI archive deployments are now up to 30% faster with split-tgz archive
  option - Vercel
date: '2025-01-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/cli-archive-deployments-are-now-up-to-30-faster-with-split-tgz-archive
author: ''
summary: Vercel为CLI部署引入split-tgz归档格式，将大型归档拆分为更小分片，避免静态文件上传限制，并将大型预构建项目的上传速度提升最高30%。此前tgz格式可能触及文件大小限制且上传较慢，新选项通过分片上传显著优化性能。
categories:
- AI基础设施
tags:
- Vercel
- CLI部署
- 归档优化
- split-tgz
- 性能提升
draft: false
translated_at: '2026-06-22T07:20:02.382883'
---

`--archive` 选项是为应对 CLI 部署中遇到的文件数量上限等速率限制而引入的。预构建部署通常使用归档上传，因为它们在构建时会生成数千个文件。

此前，归档部署始终会被压缩成一个大型文件，且仅支持 `--archive` 选项中的 `tgz` 格式。使用 `tgz` 格式的部署可能会触及文件大小上传限制。此外，上传单个大型归档文件比上传多个文件分片更慢。

测试版 `split-tgz` 格式通过将大型归档拆分为更小的分片来解决这些问题。`split-tgz` 可避免静态文件上传限制，并将大型预构建项目的上传速度提升最高 30%。

使用示例：`vercel deploy --archive=split-tgz`

了解更多关于 CLI 部署的信息。

---

> 本文由AI自动翻译，原文链接：[CLI archive deployments are now up to 30% faster with split-tgz archive option - Vercel](https://vercel.com/changelog/cli-archive-deployments-are-now-up-to-30-faster-with-split-tgz-archive)
> 
> 翻译时间：2026-06-22 07:20
