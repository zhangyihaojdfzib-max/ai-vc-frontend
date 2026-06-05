---
title: Vercel 自动支持 pnpm v10
title_original: Automatic pnpm v10 support - Vercel
date: '2025-02-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/automatic-pnpm-v10-support
author: ''
summary: 'Vercel 宣布自动支持 pnpm v10，新项目若包含 `lockfileVersion: ''9.0''` 的 `pnpm-lock.yaml`
  文件，将默认使用 pnpm v10 进行安装和构建。现有项目则继续使用 pnpm v9 以确保向后兼容性。用户可通过构建日志查看当前使用的版本，并利用 Corepack
  手动升级或降级。此举简化了包管理流程，提升了构建效率。'
categories:
- AI基础设施
tags:
- Vercel
- pnpm
- 包管理
- 构建工具
- 版本支持
draft: false
translated_at: '2026-06-05T06:22:35.104065'
---

博客/更新日志

# 自动支持 pnpm v10

![](/images/posts/ee67f2abb39b.jpg)

![](/images/posts/509681a9bfe2.jpg)

Vercel 现已支持 pnpm v10。

对于包含 `lockfileVersion: '9.0'` 的 `pnpm-lock.yaml` 文件的新项目，将自动在安装和构建命令中使用 pnpm v10。现有项目将继续使用 pnpm v9 以保持向后兼容性，因为 pnpm v9 也使用 `lockfileVersion: '9.0'`。

请查看您的构建日志以了解部署使用的版本。如需手动升级或降级版本，请使用 Corepack。

访问包管理器文档了解更多信息。

加载状态…

---

> 本文由AI自动翻译，原文链接：[Automatic pnpm v10 support - Vercel](https://vercel.com/changelog/automatic-pnpm-v10-support)
> 
> 翻译时间：2026-06-05 06:22
