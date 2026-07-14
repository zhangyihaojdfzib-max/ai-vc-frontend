---
title: Vercel CLI 新增标志定向规则管理功能
title_original: Manage Vercel Flags targeting rules from the CLI - Vercel
date: '2026-07-13'
source: Vercel Blog
source_url: https://vercel.com/changelog/manage-vercel-flags-targeting-rules-from-the-cli
author: ''
summary: Vercel 宣布其 CLI 工具新增 `vercel flags rules` 命令，允许用户和智能体在终端中直接管理 Vercel Flags
  的定向规则，无需离开命令行。该功能支持添加、移动和查看规则，规则条件可针对实体或片段，结果可指定变体、加权拆分或渐进式发布。通过 `--json` 输出可获取完整规则集，便于脚本集成。环境可继承配置，新增规则时会自动切换为自有配置。用户需更新至最新
  CLI 版本以使用此功能。
categories:
- AI产品
tags:
- Vercel
- CLI
- 功能标志
- 定向规则
- 开发者工具
draft: false
translated_at: '2026-07-14T04:52:16.737706'
---

您现在可以通过Vercel CLI管理Vercel Flags的定向规则。使用`vercel flags rules`命令，您和您的Agent（智能体）无需离开终端即可添加新规则、移动现有规则并查看当前排序。

通过CLI创建的规则与仪表盘使用相同的模型。条件可以针对实体或可复用片段，结果可以服务于单个变体、加权拆分或渐进式发布，规则按从上到下的顺序评估。对于脚本和Agent（智能体），`vercel flags rules ls --json`会输出完整的规则集。

```
vercel flags rules add checkout-redesign \  --environment production \  --condition "user.country:in:DE,FR,ES" \  --variant new-checkout
```

在生产环境中添加一条规则，向德国、法国和西班牙的用户提供new-checkout变体。

一个环境可以从另一个环境继承其标志配置。当您在继承环境中添加或更新规则时，CLI会将该环境切换为自有配置，因此您的规则会在该环境中生效，而不会更改其继承来源的环境。

请更新至最新版本的Vercel CLI，并运行`vercel flags rules`开始使用。更多信息请参阅Vercel Flags CLI文档。

---

> 本文由AI自动翻译，原文链接：[Manage Vercel Flags targeting rules from the CLI - Vercel](https://vercel.com/changelog/manage-vercel-flags-targeting-rules-from-the-cli)
> 
> 翻译时间：2026-07-14 04:52
