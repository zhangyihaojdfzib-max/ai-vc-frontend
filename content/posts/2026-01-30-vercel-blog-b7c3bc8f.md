---
title: AssistLoop入驻Vercel智能体市场，为Next.js应用提供AI客户支持
title_original: Assistloop joins the Vercel Agents Marketplace - Vercel
date: '2026-01-30'
source: Vercel Blog
source_url: https://vercel.com/changelog/assistloop-joins-the-vercel-agents-marketplace
author: ''
summary: AssistLoop作为一款AI驱动的客户支持集成，正式在Vercel市场上架。该集成与Vercel原生连接，允许团队通过智能体ID快速安装，将AI支持直接嵌入Next.js应用。用户可基于内部文档、常见问题解答或知识库训练智能体，定制品牌化助手，并能在需要时查看对话记录或转接人工支持。该方案无缝融入Vercel工作流，提供统一计费、自动环境变量注入，无需复杂配置或单独控制面板，显著简化了AI支持功能的部署流程。
categories:
- AI产品
tags:
- Vercel
- AI客户支持
- Next.js
- 智能体市场
- 低代码集成
draft: false
translated_at: '2026-01-31T04:03:25.072351'
---

![](/images/posts/01bb3373651c.jpg)

![](/images/posts/c20ef410f0a3.jpg)

AssistLoop 现已作为一款 AI 驱动的客户支持集成，在 Vercel 市场上架。

该集成与 Vercel 原生连接，因此添加 AI 驱动的客户支持只需几分钟。通过 AssistLoop，团队可以：

*   使用 Agent（智能体）ID 以最少的设置安装 AssistLoop
*   将 AI 驱动的支持直接添加到 Next.js 应用中
*   基于内部文档、常见问题解答或知识库训练智能体
*   定制助手以匹配您的品牌
*   查看对话并在需要时转接至人工支持

使用 Agent（智能体）ID 以最少的设置安装 AssistLoop

将 AI 驱动的支持直接添加到 Next.js 应用中

基于内部文档、常见问题解答或知识库训练智能体

定制助手以匹配您的品牌

查看对话并在需要时转接至人工支持

此集成能自然地融入现有的 Vercel 工作流，提供统一的计费、自动环境变量且无需手动配置。团队可以更快地部署 AI 驱动的支持，而无需管理单独的控制面板或进行复杂的设置。

AssistLoop 会自动将 `NEXT_PUBLIC_ASSISTLOOP_AGENT_ID` 注入到您的项目环境中。只需将小组件脚本添加到您的网站：

```
1import Script from 'next/script'2
3<Script4  src="https://assistloop.ai/assistloop-widget.js"5  strategy="afterInteractive"6  onLoad={() => {7    window.AssistLoopWidget?.init({8      agentId: process.env.NEXT_PUBLIC_ASSISTLOOP_AGENT_ID,9    });10  }}11/>12

```

AssistLoop 会自动将 NEXT_PUBLIC_ASSISTLOOP_AGENT_ID 注入到您的项目环境中。只需将小组件脚本添加到您的网站：

### 开始使用

从市场上部署 AssistLoop Next.js 模板以查看实际效果。

---

> 本文由AI自动翻译，原文链接：[Assistloop joins the Vercel Agents Marketplace - Vercel](https://vercel.com/changelog/assistloop-joins-the-vercel-agents-marketplace)
> 
> 翻译时间：2026-01-31 04:03
