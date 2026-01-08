---
title: Replicate加入Cloudflare，共同构建AI应用默认平台
title_original: Replicate is joining Cloudflare – Replicate blog
date: '2025-11-17'
source: Replicate Blog
source_url: https://replicate.com/blog/replicate-cloudflare
author: ''
summary: AI模型托管平台Replicate宣布正式加入Cloudflare，未来将作为独立品牌运营。此次整合旨在利用Cloudflare强大的全球网络和开发者平台资源，提升Replicate的服务速度与规模，并实现与Workers、R2等服务的深度集成。文章强调现有API和用户应用将保持稳定，核心目标是通过结合双方优势，为开发者提供更完善的AI基础设施抽象层，共同打造构建AI应用的默认选择。
categories:
- AI基础设施
tags:
- 企业并购
- AI平台
- 开发者工具
- 云计算
- 模型部署
draft: false
translated_at: '2026-01-08T04:44:43.309639'
---

- Replicate
- 博客

# Replicate 正式加入 Cloudflare

- bfirsh

重大消息：我们即将加入 Cloudflare。

Replicate 将继续作为一个独立品牌运营，唯一的变化是它将变得更好。速度会更快，我们将拥有更多资源，并且它将与 Cloudflare 开发者平台的其他部分深度集成。

API 不会改变。您当前使用的模型将继续正常工作。如果您在 Replicate 上构建了任何应用，它将继续像现在一样运行。

那么，我们为什么要这样做？

在 Replicate，我们致力于构建 AI 的基础构件：那些让软件开发人员能够使用 AI，而无需理解底层所有复杂技术的工具和抽象层。

我们从 **Cog** 开始，这是一个开源工具，它为模型定义了一个标准格式。然后，我们创建了 Replicate 平台，人们可以在这里共享模型并通过 API 运行它们。我们定义了什么是模型、如何发布、如何运行、如何输入和输出数据。

这些抽象层就像是操作系统的底层原语。但有趣的是，这些原语运行在云端。它们必须如此——它们需要专门的 GPU 和集群来在生产环境中扩展。这就像一个运行在云端的、为 AI 服务的分布式操作系统。换句话说，**网络即计算机**。

谁拥有最好的网络？Cloudflare。

Cloudflare 已经构建了这个操作系统的许多其他部分。Workers 是运行 Agent（智能体）和粘合代码的完美平台。Durable Objects 用于管理状态，R2 用于存储文件，WebRTC 用于流媒体传输。

既然我们已经有了这些底层抽象，我们就可以构建更高层次的抽象。例如，编排模型和构建 Agent（智能体）的方法，运行实时模型或在边缘运行模型的方法。

这就是我们加入 Cloudflare 的原因。

在我的整个职业生涯中，我一直很钦佩 Cloudflare。他们如何为开发者打造产品，并将其发展成一个庞大的企业业务。它是唯一一家真正**理解**开发者并知道如何为他们构建优秀产品的上市公司。

Cloudflare 是构建 Web 应用的默认选择。从 Replicate 诞生的第一天起，当我们构建申请 Y Combinator 的原型时，我们就将 Cloudflare 置于其前端。

携手合作，我们将成为构建 AI 应用的默认选择。

更多详情，请查看 Cloudflare 博客上的**官方公告**。

---

> 本文由AI自动翻译，原文链接：[Replicate is joining Cloudflare – Replicate blog](https://replicate.com/blog/replicate-cloudflare)
> 
> 翻译时间：2026-01-08 04:44
