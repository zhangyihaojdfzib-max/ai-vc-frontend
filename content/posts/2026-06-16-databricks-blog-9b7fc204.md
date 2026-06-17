---
title: Databricks Marketplace上线应用，数据安全与AI应用新突破
title_original: Announcing Apps on Databricks Marketplace
date: '2026-06-16'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-apps-databricks-marketplace
author: ''
summary: Databricks宣布在Marketplace上推出Apps公开预览，允许用户直接在安全的工作区内发现、安装和运行第三方数据和AI应用程序。该功能通过Unity
  Catalog实现内置治理，应用程序在消费者环境中运行，无需移动数据，保障安全与知识产权。提供商可零出站流量分发应用，降低合规与集成成本，开启新的收入来源。
categories:
- AI产品
tags:
- Databricks
- 数据应用
- AI应用
- 数据安全
- 市场平台
draft: false
translated_at: '2026-06-17T07:10:21.949621'
---

直接从 Databricks Marketplace 即时访问强大的数据和 AI 应用程序。应用程序原生部署在您安全、受管控的 Unity Catalog 中——您的数据保留在您的环境中，位置不变。提供商可以安全地向数千个 Databricks 客户分发专有数据应用程序并从中获利，从而开启新的收入来源。

数据智能正在重塑组织将数据转化为成果的方式。团队不再仅仅需要原始数据集——他们需要能够立即让数据发挥作用的应用程序，例如交互式仪表盘、自定义 AI Agent（智能体）和专门的分析工具。其中一些应用程序完全运行在客户自己的数据上，而另一些则将提供商的专有数据或逻辑与客户的数据相结合。

去年，我们推出了 Databricks Apps，使团队能够使用流行的框架（如用于 Python 的 Streamlit、Dash 和 Gradio，以及用于 Node.js 的 React、Angular、Svelte 和 Express）原生构建和部署安全的数据和 AI 应用程序。今天，我们在普及数据和 AI 应用程序方面迈出了下一步重大举措。

我们激动地宣布 Databricks Marketplace 上的 Apps 进入公开预览阶段。Databricks 客户现在可以直接在其安全的 Databricks 工作区内发现、安装和运行第三方数据和 AI 应用程序。对于软件供应商和数据提供商而言，这开启了一个无缝、零出站流量的分发渠道，能够为全球数千家企业提供即时、交互式的价值。

![Marketplace 上的 Apps 启动合作伙伴](/images/posts/623fa3e94a70.png)

## 挑战：第三方应用程序采购的"最后一公里"

从历史上看，采用新的第三方分析工具或数据应用程序一直是一场安全与工程上的噩梦。对于企业数据团队来说，该过程通常涉及：

- 将敏感的 corporate 数据从安全环境迁移到外部供应商的基础设施。
- 花费数周或数月进行信息安全与合规审查，以确保外部应用程序符合严格的安全标准。
- 复杂的设置，涉及自定义 ETL 管道、API 集成和分散的身份管理。

Databricks Marketplace 上的 Apps 完全颠覆了这种模式。不再是移动您的数据到应用程序，而是应用程序来到您的数据所在之处。

## Databricks Marketplace 上 Apps 的关键能力

Databricks Marketplace 是一个面向数据以及 AI 和分析资产（如 ML 模型、笔记本、应用程序）的开放市场。通过将应用程序共享直接嵌入到 Databricks Marketplace 生态系统中，我们引入了一种快速、统一且企业就绪的方式来使用第三方软件。

### 1. 无缝发现与一键安装

用户可以浏览由顶级行业合作伙伴构建的丰富应用程序目录。一旦找到适合您需求的应用程序，只需点击几下即可完成安装，自动将应用程序原生配置到您的工作区内。

### 2. 通过 Unity Catalog 实现内置治理

从 Marketplace 安装的每个第三方应用程序都在消费者 Databricks 账户内一个安全、隔离的沙箱中运行，并继承 Unity Catalog 的安全性、审计和细粒度访问控制。每个应用程序都会声明其确切需要的资源和范围，消费者在安装时明确授权。

### 3. 为 ISV 和 SaaS 提供商提供庞大的新分发渠道

对于提供商而言，每次新客户上线都需要单独集成、设置基础设施、审查合规性并提供支持，这非常令人头疼。通过 Marketplace 上的 Apps，提供商只需发布一次，任何 Databricks 客户都可以完全在其自身环境中发现、请求访问、安装和运行应用程序，无需维护供应商基础设施，也无需为每个客户承担上线开销。由于应用程序原生运行在客户的 Databricks 计算资源上，采购和合规障碍显著降低，大大缩短了 B2B 销售周期。

### 4. 设计上确保安全与知识产权保护

Databricks Marketplace 上的 Apps 继承了 Databricks 平台的安全和治理态势，并增加了传统采购模式无法提供的提供商端保护。

- **默认闭源。** 提供商应用程序以闭源容器形式提供。消费者在其工作区中安装并运行应用程序，但永远看不到底层代码。提供商的知识产权得到端到端保护。
- **消费者控制出站流量。** 应用程序在消费者的 Databricks 账户内无服务器计算资源上执行，具有与其余 Databricks Apps 相同的隔离性——每个应用程序专用计算资源、网络分段、静态和传输中加密。应用程序所需的任何外部 API 调用或数据移动都预先声明，在安装时由消费者管理员授权，并受工作区的无服务器出站网关策略管控。
- **合规就绪。** 在 Databricks 合规安全配置文件可用的所有区域均受支持。

## Databricks 技术栈的原生组成部分

Databricks Marketplace 上的 Apps 是 Databricks 平台的原生组成部分，直接连接到技术栈的其他部分：

- **Unity Catalog** 用于治理和数据访问。
- **SQL Warehouse** 用于对受管控数据进行分析查询。
- **Lakebase** 作为托管 Postgres 后端，用于应用程序状态、会话存储或低延迟操作数据。
- **Model Serving** 和 **Foundation Model APIs** 用于推理——需要 AI 能力的应用程序可以原生调用服务端点，无需外部 LLM 提供商。
- **Genie spaces** 和 **Agent Bricks** 用于嵌入到应用程序体验中的自然语言和 Agent（智能体）工作流。
- 以及更多……

这意味着许多启动应用程序开箱即具备 AI 能力。提供商也从中受益：基于这些原语构建比连接外部服务更快，并且消费者的安全审查更简单，因为无需额外添加白名单。

## 与精英合作伙伴生态系统共同启动

我们很自豪地与 20 个合作伙伴共同启动 Databricks Marketplace 上的 Apps，他们在数据和 AI 领域构建生产级应用程序。这些应用程序涵盖了广泛的行业用例：

![Marketplace 上的 Apps 生态系统](/images/posts/9258242812de.png)

## 工作原理：从发现到行动

开始使用 Databricks Marketplace 上的 Apps 很简单，并且能自然地融入您现有的工作流程：

1. **浏览：** 导航到 Databricks 工作区中的 Marketplace 选项卡，并按新的 Apps 类别进行筛选。
2. **安装：** 工作区管理员选择一个应用程序，查看并授权其所需的权限和资源绑定，然后点击安装。
3. **启动：** 应用程序部署到您工作区中一个安全的、无服务器运行时上，生成一个干净、专用的 URL。
4. **使用：** 业务和技术用户打开并使用该应用程序。

![](/images/posts/433b53f5c216.gif)

## 未来展望

这仅仅是个开始，我们很高兴在未来几个月继续在体验方面进行投入：

- **捆绑资产：** 将应用程序与其支持的作业、笔记本、仪表盘和库一起打包上架，这样消费者在安装前无需任何手动设置。
- **更丰富的提供商分析：** 为提供商提供每个上架产品的使用情况、安装漏斗和 DBU 消耗可见性。
- **应用程序的商业变现：** 在我们平台内变现试点的基础上，为 Marketplace 应用程序带来交易能力。

Databricks Marketplace 上的 Apps 弥合了安全数据治理与强大商业软件之间的鸿沟。通过将 Marketplace 的发现层与 Databricks Apps 原生的、工作区内的运行时相结合，组织现在可以比以往任何时候都更快、更安全地采用第三方软件。

- **对于消费者：** 立即探索 Databricks Marketplace，发现并安装第三方应用程序。
- **对于提供商：** 阅读我们的开发者文档，了解如何在 Databricks Marketplace 上创建、发布您的应用程序并从中获利。

### 在您的收件箱中获取最新文章

订阅我们的博客，让最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Announcing Apps on Databricks Marketplace](https://www.databricks.com/blog/announcing-apps-databricks-marketplace)
> 
> 翻译时间：2026-06-17 07:10
