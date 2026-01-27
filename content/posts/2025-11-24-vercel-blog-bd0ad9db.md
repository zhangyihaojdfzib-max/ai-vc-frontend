---
title: Workflow Builder：开源工作流自动化平台，基于Next.js与Vercel
title_original: 'Workflow Builder: Build your own workflow automation platform - Vercel'
date: '2025-11-24'
source: Vercel Blog
source_url: https://vercel.com/blog/workflow-builder-build-your-own-workflow-automation-platform
author: ''
summary: 本文介绍了Vercel开源的Workflow Builder，这是一个基于Next.js的完整可视化工作流自动化平台。该平台包含可视化编辑器、AI辅助生成、预置集成模块及执行引擎，允许用户通过拖放方式构建自动化流程，并支持将工作流编译为TypeScript代码。它适用于构建智能体、内部工具、客户工作流工具等多种场景，可一键部署至Vercel，为开发者提供了快速定制和扩展工作流自动化能力的基础设施。
categories:
- AI产品
tags:
- 工作流自动化
- 开源项目
- Next.js
- Vercel
- 低代码平台
draft: false
translated_at: '2026-01-12T04:52:45.516180'
---

Workflow Builder 是一个用于构建工作流自动化平台的开源 Next.js 模板

今天我们开源了 **Workflow Builder**，这是一个由 **Workflow Development Kit (WDK)** 驱动的完整可视化自动化平台。

该项目包含一个可视化编辑器、执行引擎和基础设施，为您提供了构建自己的工作流自动化工具和 Agent（智能体）所需的一切。您可以将其部署到 Vercel，并根据您的用例进行定制。

部署 Workflow Builder

一键部署您自己的 Workflow Builder。

## Workflow Builder 包含哪些内容

Workflow Builder 是一个可用于生产环境的 Next.js 应用程序，包含一个完全交互式的工作流编辑器、AI 辅助的工作流生成、六个预构建的集成模块以及端到端的可观测性。

### 可视化工作流编辑器

可视化工作流编辑器允许您使用拖放步骤来构建、连接和执行工作流。您无需编写代码即可获得实时验证、撤销/重做、自动保存和持久化状态。

预构建的集成包括：

*   Resend（电子邮件）
*   Linear（问题管理）
*   Slack（通知）
*   PostgreSQL（数据库）
*   HTTP 请求（API 调用）
*   Vercel AI Gateway（AI 模型）

### AI 驱动的文本到工作流生成

AI 驱动的文本到工作流功能可将自然语言提示词转换为可执行的工作流。输入您的自动化描述，系统将生成结构化的步骤定义和连接。

### Webhook 触发器

Webhook 触发器将您的工作流连接到外部应用程序和 API。外部事件、服务或数据源可以实时触发工作流执行。

### 引用先前步骤的输出

每个工作流步骤都可以访问和引用先前步骤的输出。这创建了动态的、数据驱动的流程，并支持后续步骤依赖于早期结果的 Agent（智能体）工作流。

### 工作流代码生成

每个可视化工作流都会通过 Workflow Development Kit (WDK) 编译成可执行的 TypeScript 代码。`"use workflow"` 和 `"use step"` 指令将您的函数转换为运行时执行图，该图负责状态管理、错误处理和步骤协调。

![](/images/posts/2cc0b83a3538.png)

![](/images/posts/734d80c9d66a.png)

## Workflow Builder 的用例

借助 Workflow Builder，您就拥有了为内部工具或面向客户的产品构建自己的工作流自动化平台的基础：

*   **Agent（智能体）**：执行由 AI 驱动的多步骤、跨系统工作流
*   **内部工具**：根据您组织的流程和系统定制的自动化系统
*   **面向客户的工作流工具**：提供特定领域的工作流构建器，如 Zapier 或 n8n
*   **集成平台**：为您的产品添加拖放式工作流功能
*   **数据管道**：设计具有可视化监控和执行跟踪功能的 ETL 或数据处理管道

> 本文由AI自动翻译，原文链接：[Workflow Builder: Build your own workflow automation platform - Vercel](https://vercel.com/blog/workflow-builder-build-your-own-workflow-automation-platform)
> 
> 翻译时间：2026-01-12 04:52
