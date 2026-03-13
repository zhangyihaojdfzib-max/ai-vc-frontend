---
title: Notion Workers如何利用Vercel沙箱安全运行不可信代码
title_original: How Notion Workers run untrusted code at scale with Vercel Sandbox
  - Vercel
date: '2026-03-12'
source: Vercel Blog
source_url: https://vercel.com/blog/notion-workers-vercel-sandbox
author: ''
summary: 本文介绍了Notion Workers如何借助Vercel Sandbox解决大规模运行用户自定义代码的安全与扩展性挑战。Vercel Sandbox通过Firecracker微虚拟机提供强隔离，每个Worker运行在独立内核中，确保数据与状态互不干扰。其核心能力包括凭据注入（密钥通过网络代理注入，不暴露给代码）、动态网络策略控制、文件系统快照以实现快速冷启动，以及按活跃CPU计费的经济模型。这些基础设施使Notion能够专注于开发者体验，安全支持数据同步、自动化与AI智能体等自定义功能，而无需自建复杂的安全执行环境。
categories:
- AI基础设施
tags:
- Vercel Sandbox
- 代码安全
- 微虚拟机
- Notion Workers
- 云原生
draft: false
translated_at: '2026-03-13T05:03:20.122409'
---

Notion Workers 允许您编写和部署代码，为自定义 Agent（智能体）赋予新能力：同步外部数据、触发自动化流程、调用任何 API。借助 Workers，开发者可以构建能够定时同步 CRM 数据、在错误率激增时创建问题工单、并将 Slack 线程转化为格式化内容的智能体。

在底层，每个 Worker 都运行在 Vercel Sandbox 上。

## 问题：安全地运行来自任何开发者或智能体的代码

Notion 希望允许任何人通过自定义代码扩展其平台。这是一个困难的基础设施问题，但更是一个重大的安全问题。每个 Notion Worker 都代表一个 Notion 用户（可能是在企业工作空间内），运行由第三方开发者或智能体生成的任意代码。

如果没有适当的隔离，Worker 将与自定义 Agent（智能体）运行在同一个环境中，能够访问其密钥、权限以及该执行上下文中的所有其他内容。一次简单的提示词注入就可能窃取凭据或访问另一用户的数据。

需求非常明确：

- **强隔离**：一个 Notion Worker 绝不能访问另一个 Worker 的数据或状态
- **凭据安全**：Notion Workers 需要 API 密钥来与外部服务通信，但这些密钥绝不能暴露给代码本身
- **网络控制**：企业客户需要确保 Worker 只能访问被允许的外部服务
- **可扩展性**：Workers 需要支持数百万用户并发执行，且性能不下降
- **状态保持**：Workers 需要快速的冷启动，这要求具备快照和恢复文件系统状态的能力
- **经济性**：需要一个为 CPU 利用率较低的智能体设计的计费模型

## 为何选择 Vercel Sandbox

Vercel Sandbox 在临时的 Firecracker 微虚拟机中运行每个 Notion Worker。每个虚拟机都启动自己的内核，提供比容器更强的隔离性。每次执行都拥有自己的文件系统、自己的网络栈和自己的安全边界。当 Notion Worker 执行完毕，微虚拟机要么被销毁，要么被快照以供后续检索。

![通过密钥注入实现独立的安全上下文。生成的代码在运行时可以通过代理使用凭据，但无法窃取它们。](/images/posts/1a23c1b2bdaf.jpg)

![通过密钥注入实现独立的安全上下文。生成的代码在运行时可以通过代理使用凭据，但无法窃取它们。](/images/posts/bf44692c53cb.jpg)

![通过密钥注入实现独立的安全上下文。生成的代码在运行时可以通过代理使用凭据，但无法窃取它们。](/images/posts/6ea9f338a4eb.jpg)

![通过密钥注入实现独立的安全上下文。生成的代码在运行时可以通过代理使用凭据，但无法窃取它们。](/images/posts/45625bb4bad1.jpg)

为了大规模支持像 Notion Workers 这样的工作负载，Vercel Sandbox 提供了几个关键能力：

**凭据注入**。Sandbox 的防火墙代理可以在网络层面拦截出站请求并注入 API 密钥，因此凭据永远不会进入执行环境。对于智能体驱动的工作负载，这消除了最危险的提示词注入攻击向量：即智能体被诱骗泄露密钥。（我们在《智能体架构中的安全边界》一文中深入探讨过这种架构）。

**网络策略**。Sandbox 支持动态网络策略，可以在运行时更新而无需重启进程：开始时拥有互联网访问权限以下载依赖，然后在运行不受信任的代码前锁定出口。平台构建者可以将这些控制权传递给自己的客户。

**快照**。一次性安装依赖，对文件系统状态进行快照，并在后续调用时从该快照恢复。结合按活跃 CPU 计费的模式（仅在代码实际执行而非等待 I/O 时产生 CPU 成本），这确保了成本随使用规模增长而可预测。

## 更宏大的图景：作为开发者平台的 Notion

Notion Workers 并非一次性功能。它是 Notion 开始转型为开发者平台的开端。

这种转变需要 Notion 不必自行构建的基础设施。安全的代码执行、凭据管理、网络隔离、基于文件系统的快照：这些都是随着平台扩展而愈发复杂的难题。

Vercel Sandbox 处理了基础设施的复杂性，使得 Notion 可以专注于开发者体验。

## 开发者正在用 Notion Workers 构建什么

Notion Workers 支持三种主要模式：第三方数据同步、自定义自动化和 AI 智能体工具。

开发者使用它们来按计划将外部数据（如 CRM 记录、分析数据、支持工单）同步到 Notion。Worker 也可以附加到按钮上，通过单击触发任意代码。并且，当 Notion 的自定义智能体将 Workers 作为工具调用时，它们的能力将远超那些仅限于预置集成的智能体。

## 使用 Vercel Sandbox 扩展您的平台

Notion Workers 所需的能力与其他智能体平台相同。任何希望允许用户或智能体运行自定义代码的平台都面临着同样的问题：隔离、凭据安全、网络控制和可扩展性。

Vercel Sandbox 将这些能力作为开箱即用的功能提供。如果您正在构建一个需要运行不受信任代码的平台，无论是用于 AI 智能体、开发者插件还是工作流自动化，这就是您的实现方式。

---

> 本文由AI自动翻译，原文链接：[How Notion Workers run untrusted code at scale with Vercel Sandbox - Vercel](https://vercel.com/blog/notion-workers-vercel-sandbox)
> 
> 翻译时间：2026-03-13 05:03
