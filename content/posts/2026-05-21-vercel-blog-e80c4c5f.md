---
title: Vercel CLI 新增加权流量拆分命令
title_original: Configure weighted traffic splits for Vercel Flags from the Vercel
  CLI - Vercel
date: '2026-05-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/configure-weighted-traffic-splits-for-vercel-flags-from-the-vercel-cli
author: ''
summary: Vercel 在 CLI 中新增了 `vercel flags split` 命令，支持为 Vercel Flags 配置加权流量拆分。用户可通过交互式运行或传递标志参数，按环境、分桶属性和变体权重分配流量。例如，可为生产环境的
  redesigned-checkout 设置 95/5 的权重拆分，并按 user.id 进行分桶。该功能需更新至最新版 Vercel CLI。
categories:
- 技术趋势
tags:
- Vercel
- 流量拆分
- CLI工具
- A/B测试
draft: false
translated_at: '2026-05-23T05:40:24.092663'
---

您现在可以使用 Vercel CLI 中新增的 `vercel flags split` 命令，为 Vercel Flags 配置加权流量拆分。这使您能够将一定比例的流量发送至一个变体，其余流量发送至另一个变体。

您可以交互式运行该命令，或通过标志传递环境、分桶属性及变体权重：

```
1vercel flags split redesigned-checkout \2  --environment production \3  --by user.id \4  --weight off=95 \5  --weight on=5
```

为生产环境的 redesigned-checkout 设置 95/5 的权重拆分，并按 user.id 进行分桶。

请更新至最新版本的 Vercel CLI，并阅读相关文档以开始使用。

---

> 本文由AI自动翻译，原文链接：[Configure weighted traffic splits for Vercel Flags from the Vercel CLI - Vercel](https://vercel.com/changelog/configure-weighted-traffic-splits-for-vercel-flags-from-the-vercel-cli)
> 
> 翻译时间：2026-05-23 05:40
