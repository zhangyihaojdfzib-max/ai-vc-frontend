---
title: Vercel CLI 新增命令：管理 Flags 细分
title_original: Manage Vercel Flags segments with Vercel CLI - Vercel
date: '2026-07-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/manage-vercel-flags-segments-with-vercel-cli
author: ''
summary: Vercel 在 CLI 中推出了新的 `vercel flags segments` 命令，允许开发者通过命令行管理标志的细分（segments）。细分由
  include、exclude 和 rule 三种 Token 组成，支持增量编辑和完整替换，并可通过 `--json` 输出实现脚本化操作。该功能简化了 CI/CD
  和本地工作流中的标志目标定位管理，提升了开发效率。
categories:
- 技术趋势
tags:
- Vercel
- CLI
- Flags
- 细分管理
- 开发工具
draft: false
translated_at: '2026-07-06T06:51:55.491072'
---

现在可以通过新的 `vercel flags segments` 命令，在 Vercel CLI 中管理 Vercel Flags 的细分（segments）。

细分是标志（flag）用于决定谁看到什么内容的目标定位原语。成员资格由三个可重复的 Token 组成：`include:`、`exclude:` 和 `rule:`。将它们传递给 `--add` 或 `--remove` 进行增量编辑。如需完全替换，`--data` 接受以原始 JSON 格式提供的完整细分定义。

```
12vercel flags segments create beta-users \3  --label "Beta users" \4  --add include:user.id=user_123 \5  --add include:user.id=user_45667vercel flags segments update beta-users \8  --add rule:user.plan:eq:enterprise \9  --remove include:user.id=user_123
```

在创建和更新操作中组合使用 include、exclude 和 rule Token

所有细分命令都支持 `--json` 输出，使其可从 CI、本地工作流以及需要从终端检查或更新标志目标定位的 Agent 驱动管道中进行脚本化操作。

更新到最新版本的 Vercel CLI，并在 Vercel Flags CLI 文档中了解更多信息，以开始使用。

---

> 本文由AI自动翻译，原文链接：[Manage Vercel Flags segments with Vercel CLI - Vercel](https://vercel.com/changelog/manage-vercel-flags-segments-with-vercel-cli)
> 
> 翻译时间：2026-07-06 06:51
