---
title: Replicate加入Cloudflare：共同构建下一代AI基础设施
title_original: Why Replicate is joining Cloudflare
date: '2025-12-01'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/why-replicate-joining-cloudflare/
author: Andreas Jansson
summary: AI模型服务平台Replicate宣布正式加入Cloudflare。文章回顾了Replicate自2019年创立以来的使命——通过开发Cog标准化工具和云平台，将研究模型转化为开发者可用的API服务，并在Stable
  Diffusion发布时成功支撑了大规模应用。随着AI技术栈日益复杂，涉及推理、微服务、存储等多个环节，Replicate认为Cloudflare拥有的全球网络、边缘计算、对象存储等基础设施能力，将帮助双方共同构建更完整的AI技术栈，实现在边缘运行模型、Worker流水线等愿景。
categories:
- AI基础设施
tags:
- Replicate
- Cloudflare
- AI平台
- 模型部署
- 边缘计算
draft: false
translated_at: '2026-01-05T17:25:28.547Z'
---

我们很高兴地宣布，从今天起，Replicate 正式成为 Cloudflare 的一部分。

2019 年我们创立 Replicate 时，OpenAI 刚刚开源了 GPT-2，机器学习社区之外很少有人关注 AI。但对于我们这些身处该领域的人来说，感觉一件大事即将发生。卓越的模型正在学术实验室中诞生，但你需要一件象征性的"实验服"才能运行它们。

我们的使命是将研究模型带出实验室，交到开发者手中。我们希望程序员能创造性地改造和运用这些模型，构建出研究人员从未设想过的产品。

我们将其视为一个工具问题来解决。就像 Heroku 这样的工具让运行网站而无需管理 Web 服务器成为可能一样，我们想要构建运行模型所需的工具，而无需理解反向传播或处理 CUDA 错误。

我们构建的第一个工具是 Cog：一个机器学习模型的标准打包格式。然后我们构建了 Replicate 平台，用于在云端将 Cog 模型作为 API 端点运行。我们既抽象了底层的机器学习细节，也抽象了大规模运行推理所需的复杂 GPU 集群管理。

事实证明，时机恰到好处。当 2022 年 Stable Diffusion 发布时，我们已经拥有了成熟的基础设施，能够应对开发者运行这些模型的巨大热情。大量出色的应用程序和产品在 Replicate 上构建起来，这些应用通常运行一个封装在精美 UI 中的单一模型，以解决特定的用例。

自那时起，AI 工程学已发展为一门严谨的技艺。AI 应用不再仅仅是运行模型。现代 AI 技术栈包含模型推理，但也包含微服务、内容分发、对象存储、缓存、数据库、遥测等。我们看到许多客户正在构建复杂的异构技术栈，其中 Replicate 模型只是跨多个平台的高阶系统中的一个组成部分。

这正是我们加入 Cloudflare 的原因。Replicate 拥有运行模型的工具和基础组件。Cloudflare 拥有最佳的网络、Workers、R2、Durable Objects 以及构建完整 AI 技术栈所需的所有其他基础组件。

AI 技术栈完全存在于网络上。模型在数据中心 GPU 上运行，并通过调用向量数据库、从对象存储中获取数据、调用 MCP 服务器等的小型云函数粘合在一起。"网络即计算机"这句话从未像现在这样真实。

在 Cloudflare，我们现在将能够构建自公司创立以来就梦寐以求的 AI 基础设施层。我们将能够实现诸如在边缘运行快速模型、在即时启动的 Workers 上运行模型流水线、通过 WebRTC 流式传输模型输入和输出等功能。

我们为在 Replicate 所构建的一切感到自豪。我们是首个生成式 AI 服务平台，并定义了大多数同行所采用的抽象和设计模式。我们围绕产品培育了一个由构建者和研究人员组成的优秀社区。

---

> 本文由AI自动翻译，原文链接：[Why Replicate is joining Cloudflare](https://blog.cloudflare.com/why-replicate-joining-cloudflare/)
> 
> 翻译时间：2026-01-05 17:25
