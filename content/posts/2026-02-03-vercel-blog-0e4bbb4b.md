---
title: Vercel Toolbar 新增“为 Agent 复制”功能，为编码助手提供视觉上下文
title_original: Copy visual context to agents from Vercel Toolbar - Vercel
date: '2026-02-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/copy-visual-context-to-agents
author: ''
summary: Vercel 为其工具栏新增“为 Agent 复制”功能，该功能能够从页面评论中捕获完整的视觉和技术上下文，并将其转化为结构化数据供编码 Agent
  使用。捕获的信息包括页面 URL、视口尺寸、选定文本、节点路径、React 组件树详情及评论文本，旨在帮助 AI 助手准确理解已部署应用程序中的问题位置及所需更改，从而提升开发反馈的效率和精准度。该功能现已向所有
  Vercel 用户开放。
categories:
- AI产品
tags:
- Vercel
- AI助手
- 前端开发
- 开发者工具
- 低代码/无代码
draft: false
translated_at: '2026-02-04T04:21:47.657718'
---

![](/images/posts/840793238cd1.jpg)

![](/images/posts/4fda065bbc8a.jpg)

Vercel Toolbar 现已包含“为 Agent 复制”功能，该功能可从评论中捕获完整的视觉上下文，为编码 Agent 提供理解应用程序部署反馈所需的技术细节。

当团队使用此功能复制评论时，Agent 会接收到结构化上下文，包括页面 URL 和视口尺寸、选定的文本和节点路径信息、React 组件树详情以及原始评论文本。这有助于 Agent 准确理解问题在您已部署应用程序中的发生位置以及需要进行的更改。

示例上下文输出：

```
1页面 URL: /dashboard/projects
2视口: 1920x1080
3选定文本: "Deploy your latest changes"
4选择器: button.deploy-btn
5组件树: App > Dashboard > ProjectList > DeployButton
```

这种结构化格式消除了向 Agent 手动解释部署上下文的需要，可直接从工具栏复制，获得组件位置和实现的完整技术细节。

该功能现已对所有 Vercel 用户开放。

详细了解 Vercel Toolbar 或开始使用 Agent。

---

> 本文由AI自动翻译，原文链接：[Copy visual context to agents from Vercel Toolbar - Vercel](https://vercel.com/changelog/copy-visual-context-to-agents)
> 
> 翻译时间：2026-02-04 04:21
