---
title: Cloudflare CASB推出修复功能，一键修复SaaS文件共享风险
title_original: 'See risk, fix risk: introducing Remediation in Cloudflare CASB'
date: '2026-03-03'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/remediation-in-cloudflare-casb/
author: ''
summary: Cloudflare宣布为其云访问安全代理（CASB）推出“修复”功能，标志着产品从风险检测迈向主动修复的新阶段。该功能集成于Cloudflare
  One仪表板，用户可直接对Microsoft 365和Google Workspace中检测到的高风险文件共享（如公共链接、全公司共享、外部共享等）执行“移除共享”操作，而无需跳转至其他管理界面。此举旨在帮助安全和IT团队快速闭环处理过度共享等常见数据风险，提升SaaS应用安全管控效率。
categories:
- AI产品
tags:
- Cloudflare
- CASB
- SaaS安全
- 数据防泄漏
- 云安全
draft: false
translated_at: '2026-03-08T04:38:42.041566'
---

# 发现风险，修复风险：Cloudflare CASB 推出修复功能

2026-03-03

- Alex Dunbrack
- Michael Leslie

![](/images/posts/173c2d5efefd.png)

从今天起，Cloudflare CASB 客户不仅能查看其 SaaS 应用中的高风险文件共享，还能直接通过 Cloudflare One 仪表板修复它。

此次发布标志着 Cloudflare 云访问安全代理（CASB）的巨大进步。自发布以来，Cloudflare 基于 API 的 CASB 一直专注于提供强大、全面的可见性和检测能力。它还能连接到您业务所依赖的 SaaS 工具，发现配置错误，并在过度共享的数据演变为事故之前发出警报。

随着今天修复功能的发布——这是一种只需在 CASB 发现结果页面点击一下即可解决问题的新方式——CASB 开启了新的篇章，从告知您问题所在，转变为帮助您解决问题。

CASB 发现结果中一个修复操作（移除公共文件共享）的示例。

## CASB 入门：查看 SaaS 风险的单一平台

在我们的 SASE 平台 Cloudflare One 内部，CASB 连接到您的团队已经在使用的 SaaS 和云工具。通过 API 与提供商通信，CASB 为安全和 IT 团队提供：

-   对 Microsoft 365、Google Workspace、Slack、Salesforce、Box、GitHub、Jira 和 Confluence 等应用中的配置错误、过度共享文件和风险访问模式的统一视图（CASB 集成）。
-   在用户协作、共享和采用新工具时持续扫描新问题。
-   为分类和报告而整理、可搜索且可导出的发现结果。

对 Microsoft 365、Google Workspace、Slack、Salesforce、Box、GitHub、Jira 和 Confluence 等应用中的配置错误、过度共享文件和风险访问模式的统一视图（CASB 集成）。

在用户协作、共享和采用新工具时持续扫描新问题。

为分类和报告而整理、可搜索且可导出的发现结果。

但在此之前，实际的修复工作通常发生在其他地方，无论是在每个应用的管理界面内，还是通过工单提交给拥有该工具的团队。修复功能则完成了这个闭环。

## 修复功能：CASB 的新篇章

CASB 修复功能的发布标志着该产品和 Cloudflare One 向前迈出了一大步，并且我们为明年规划了大量重大更新。

通过今天的发布，我们专注于修复 Microsoft 365 和 Google Workspace 中的文件共享问题。

借助修复功能，您可以修复我们在客户中看到的最高影响、最常见的文件风险，包括：

-   允许互联网上任何人查看或编辑文件的公共链接。
-   在您的租户或域内全公司共享的文件，即使只有少数人应该有权访问。
-   向组织外部的个人账户和外部域共享的文件。
-   当上述情况也匹配数据防泄漏（DLP）配置文件时。例如，一份包含客户记录、凭证或财务详情的文档。

允许互联网上任何人查看或编辑文件的公共链接。

在您的租户或域内全公司共享的文件，即使只有少数人应该有权访问。

向组织外部的个人账户和外部域共享的文件。

当上述情况也匹配数据防泄漏（DLP）配置文件时。例如，一份包含客户记录、凭证或财务详情的文档。

当您在受支持的发现结果上触发“移除共享”修复操作时，CASB 会立即着手从相关文件中移除风险共享配置（例如，公共链接或组织范围内的访问权限）。至关重要的是，修复功能仅移除风险共享；它不会删除文件或更改文件所有者。

用于跟踪已修复 CASB 发现结果的进度和成功情况的新页面。

## 两个起点：Microsoft 365 和 Google Workspace

我们选择从 Microsoft 365 和 Google Workspace 开始，是因为对许多组织而言，其大部分关键业务文档都存储于此：内部财务数据、产品路线图、客户合同、人力资源记录等等。

这里也是“临时”共享往往停留过久的地方：

-   为快速审核而共享的“任何拥有链接的人均可编辑”的电子表格。
-   为全员会议而设为全公司可访问的文档，随后被悄然遗忘。
-   共享给承包商个人邮箱的客户记录表格。

为快速审核而共享的“任何拥有链接的人均可编辑”的电子表格。

为全员会议而设为全公司可访问的文档，随后被悄然遗忘。

共享给承包商个人邮箱的客户记录表格。

对于 Microsoft 365，这意味着清理 OneDrive 和 SharePoint 等位置的风险共享。对于 Google Workspace，则意味着收紧对 Docs、Sheets、Slides 以及存储在 Drive 中的其他文件的共享设置。

您无需从 CASB 导出风险文件的 CSV 文件，发送给应用所有者，并期望每个人都能抽空修复其共享设置，而是可以直接从 CASB 驱动清理工作，并了解这些风险何时真正得到解决。

当您和您的团队使用 CASB 修复功能时，每个操作都会记录在 Cloudflare One 的管理日志中，因此您可以查看谁在何时对哪些文件采取了行动，或者将该活动导出到您的安全信息和事件管理工具（SIEM）。

## 工作原理

在设计支持 CASB 修复功能的系统时，我们知道它必须出色地完成三件事：

-   快速，即使在大规模下
-   稳健执行，以优雅地处理意外情况
-   易于我们的客户使用

快速，即使在大规模下

稳健执行，以优雅地处理意外情况

易于我们的客户使用

为了实现这些目标，我们使用多个 Cloudflare 产品构建了一个系统：Workers、Workflows、Queues、Workers KV、Secrets Store 和 Hyperdrive。

当启动修复任务时，会向一个 Worker 发起 API 调用。该 Worker 将任务写入一个队列，由第二个 Worker 消费该队列以启动一个 Workflow。Workers KV 和 Secrets Store 用于安全分发凭证，供 Workflow 使用。Workflow 运行一系列步骤来收集信息并执行第三方 API 调用以完成修复。操作的最終结果通过 Hyperdrive 记录在数据库中。

在大规模情况下，我们必然会遇到来自供应商 API 的 429 错误。Workflows 的原生重试机制简化了对此的处理，内置的步骤日志记录提供了每次重试的可见性。这意味着我们无需为每个操作构建复杂的、单一用途的状态跟踪系统或数十个无服务器函数。

负载测试和早期访问客户的性能结果显示，即使在重负载下也表现出色。平均（p50）端到端任务完成时间为 48 秒，p90 为 72 秒。持久执行（通过 Workflows）使我们的团队完全无需手动管理任务，即使 Workflow 遇到第三方 API 问题。最终系统的简洁性使得故障排除快速而直接。

## CASB 修复功能的下一步计划

针对 Microsoft 365 和 Google Workspace 的文件共享修复只是第一步。

近期，我们正在努力为客户带来新的隔离操作，可以将高风险文件移动或隔离到更安全的位置。我们还将引入自定义 Webhook 操作，这些钩子可以让您触发下游工作流，例如创建工单、发送聊天通知或运行您自己的自动化脚本。

更广泛地说，我们很高兴探索各种方法，使 CASB 更成为一个主动的控制平面：

- **自动修复策略**：针对经过仔细界定、由策略驱动的修复措施，您可放心让CASB自动执行操作。
- **自定义CASB检测结果**：您可定义对组织最重要的精确模式、数据类型或访问条件。
- **批量修复**：支持通过单次操作修复大量相似检测结果。
- **将修复功能扩展至更多SaaS集成**：除Microsoft 365和Google Workspace外，未来还将逐步覆盖Box、Dropbox、Salesforce、GitHub、Slack、Atlassian等工具，提供统一体验。

**自动修复策略**：针对经过仔细界定、由策略驱动的修复措施，您可放心让CASB自动执行操作。

**自定义CASB检测结果**：您可定义对组织最重要的精确模式、数据类型或访问条件。

**批量修复**：支持通过单次操作修复大量相似检测结果。

**将修复功能扩展至更多SaaS集成**：除Microsoft 365和Google Workspace外，未来还将逐步覆盖Box、Dropbox、Salesforce、GitHub、Slack、Atlassian等工具，提供统一体验。

## 如何开始使用

CASB修复功能需要付费CASB许可，但这不应阻碍您立即体验CASB！

- **现有Cloudflare One/CASB客户**：集成您的Microsoft 365或Google Workspace租户（或将现有集成更新为读写权限），即可在与文件共享相关的检测类型侧边栏中直接开始修复高风险共享。
- **Cloudflare One新用户？**立即注册即可获得50个免费席位，即刻开始使用CASB。如需大规模部署，请申请与我们的专家进行咨询。

**现有Cloudflare One/CASB客户**：集成您的Microsoft 365或Google Workspace租户（或将现有集成更新为读写权限），即可在与文件共享相关的检测类型侧边栏中直接开始修复高风险共享。

**Cloudflare One新用户？**立即注册即可获得50个免费席位，即刻开始使用CASB。如需大规模部署，请申请与我们的专家进行咨询。

完成上述步骤后，请联系我们的团队为您的Microsoft 365和Google Workspace租户启用CASB修复功能，以便集中发现并修复过度共享的文件。

我们期待看到您如何运用修复功能消除长期存在的文件共享风险，并共同塑造CASB下一代修复能力的发展方向。

---

> 本文由AI自动翻译，原文链接：[See risk, fix risk: introducing Remediation in Cloudflare CASB](https://blog.cloudflare.com/remediation-in-cloudflare-casb/)
> 
> 翻译时间：2026-03-08 04:38
