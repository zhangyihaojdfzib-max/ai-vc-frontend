---
title: Vercel CLI 新增域名搜索功能
title_original: Domain Search is now available through the Vercel CLI - Vercel
date: '2026-06-09'
source: Vercel Blog
source_url: https://vercel.com/changelog/domain-search-is-now-available-through-the-vercel-cli
author: ''
summary: Vercel 宣布其 CLI 工具现已支持域名搜索功能。用户可通过 `vercel domains search` 命令查询任意域名的可用性及价格，支持按顶级域（TLD）筛选、排序、过滤不可用域名，并支持
  JSON 格式输出。该功能需将 Vercel CLI 升级至 54.10.1 版本。此举简化了开发者在终端中直接查找和购买域名的流程，提升了部署效率。
categories:
- AI基础设施
tags:
- Vercel
- 域名搜索
- CLI工具
- 开发者体验
draft: false
translated_at: '2026-06-10T06:26:47.529381'
---

现在您可以使用 Vercel CLI 搜索域名。通过 `vercel domains search` 命令，您可以提供域名并获取 Vercel 支持的所有顶级域名的可用性和价格结果。

```
~ vercel domains search acmesite --limit 5
> 域名            可用性        购买价格          续费价格
  acmesite.com    不可用        -                 -
  acmesite.dev    可用          $13 / 1 年        $13 / 1 年
  acmesite.app    可用          $14.99 / 1 年     $15 / 1 年
  acmesite.io     可用          $37.99 / 1 年     $46 / 1 年
  acmesite.ai     可用          $160 / 2 年       $160 / 2 年
> 继续运行：`vercel domains search acmesite --next eyJxdWVyeSI6ImFjbWVza...
```

您还可以按 TLD 筛选、应用排序以及过滤掉不可用的域名。

```
1vercel domains search acmesite --tld com --tld ai
2vercel domains search acmesite --available
3vercel domains search acmesite --order alphabetical
4vercel domains search acmesite --format json
5vercel domains search --help
```

请将您的 Vercel CLI 升级至版本 54.10.1 以开始使用。

---

> 本文由AI自动翻译，原文链接：[Domain Search is now available through the Vercel CLI - Vercel](https://vercel.com/changelog/domain-search-is-now-available-through-the-vercel-cli)
> 
> 翻译时间：2026-06-10 06:26
