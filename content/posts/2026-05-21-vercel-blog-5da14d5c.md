---
title: Vercel CLI 新增异常告警拉取功能
title_original: Pull anomaly alert details using the Vercel CLI - Vercel
date: '2026-05-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/pull-anomaly-alert-details-using-the-vercel-cli
author: ''
summary: Vercel 宣布其 CLI 工具新增 `vercel alerts` 命令，允许用户直接通过终端列出团队或项目的异常告警，并查看开始时间、类型及活跃状态。结合
  `--ai` 选项，AI 调查结果会内联显示，使用户和智能体无需离开终端即可对告警采取行动。该功能适用于 Observability Plus 用户，进一步提升了开发运维效率。
categories:
- AI基础设施
tags:
- Vercel
- CLI
- 异常告警
- AI调查
- 开发运维
draft: false
translated_at: '2026-05-22T06:06:14.462029'
---

您现在可以直接通过 Vercel CLI 访问异常告警及其详细信息。

使用 `vercel alerts` 命令，您可以列出某个团队或指定项目的所有告警。对于每条告警，您可以查看开始时间、告警类型以及该告警是否仍处于活跃状态。

![](/images/posts/d3194fe9e59f.jpg)

![](/images/posts/426f55d873e7.jpg)

使用 `--ai` 选项后，AI 调查结果会与每条告警一同显示。您和您的 Agent（智能体）无需离开终端即可对告警采取行动。

```
vercel alerts --ai
```

内联显示告警详情及 AI 调查结果。

适用于 Observability Plus。

在 CLI 文档中了解更多关于 `vercel alerts` 的信息。

---

> 本文由AI自动翻译，原文链接：[Pull anomaly alert details using the Vercel CLI - Vercel](https://vercel.com/changelog/pull-anomaly-alert-details-using-the-vercel-cli)
> 
> 翻译时间：2026-05-22 06:06
