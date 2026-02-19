---
title: 利用Databricks AppKit与Replit加速企业级应用开发
title_original: Ship Enterprise Apps Faster with Databricks AppKit and Replit
date: '2026-02-17'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ship-enterprise-apps-faster-databricks-appkit-and-replit
author: ''
summary: 本文介绍了Databricks推出的AppKit框架及其与Replit的新集成，旨在简化数据与AI驱动的企业级应用程序开发。Databricks
  Apps允许用户在平台上原生构建、部署和扩展应用，而AppKit作为一个TypeScript框架，通过分层架构和预设配置降低了开发复杂性。与Replit的集成进一步提升了开发体验，支持从自然语言提示开始开发，并在Databricks上安全部署，从而帮助团队更快地交付生产就绪的应用程序。
categories:
- AI产品
tags:
- Databricks
- 应用开发
- AI驱动
- Replit
- 企业级应用
draft: false
translated_at: '2026-02-19T04:45:13.360827'
---

## 通过 Databricks Apps 加速创新

Databricks Apps 允许您在 Databricks 平台上原生地安全构建、部署和扩展数据与 AI 驱动的应用程序。自 2024 年 10 月公开预览版发布以来，我们的客户已在 Databricks 上构建了数以万计的应用程序，用例范围涵盖交互式仪表板、业务流程和数据工作流自动化，以及定制的销售助手 Agent 等等。以康卡斯特为例，他们通过将复杂的预测模型转化为交互式应用程序，弥合了数据科学与业务战略之间的鸿沟。这使得他们的销售和战略团队能够实时探索收入场景并加速营销活动决策。墨西哥领先的乳制品生产商 Alpura 在短短几天内就构建了一套包含 10 多个生产应用程序的套件。他们的用例范围从工厂运营的实时物联网监控，到使团队能够为零售合作伙伴关系运行预测性“假设分析”场景的商业应用程序。

我们的合作伙伴在高度监管的行业中推广 Databricks Apps 也取得了类似的成功。Hiflylabs 使用 Databricks Apps 在短短几周内就构建了一个生产级、符合审计要求的 AI 医疗保健应用程序。该解决方案通过在受治理的安全环境中为医生提供值得信赖的 AI 工具，用于患者数据总结和风险评估，自动化了数小时的手动管理工作。

Databricks Apps 通过将应用程序与受治理的数据和 AI 资产托管在一起，为一系列企业角色解锁了全新的用例。但是，构建一个真正可用于生产的数据与 AI 应用程序仍然需要大量的工程投入。

因为与传统 CRUD 应用程序不同，数据与 AI 应用程序是有状态的，并且能够对大量历史和实时数据进行长时间的推理。这需要复杂的工作流编排、异步执行以及对长时间运行流程的支持，同时还要协调多个数据系统、AI 模型和外部服务。此外，对于这些数据与 AI 应用程序而言，身份验证、缓存和错误处理等因素的影响也被放大了。这对于经验丰富的开发人员来说都颇具挑战性，更不用说企业内部其他希望利用数据与 AI 能力满足业务需求的角色了。

## 提升开发者体验：Databricks AppKit

为了提供一种能最大限度减少这种辛劳的开发者体验，我们创建了 Databricks AppKit。

AppKit 是一个 TypeScript 框架，用于通过基于插件的架构构建生产就绪的应用程序。它提供了预设的默认配置、内置的可观测性，以及与 Databricks 服务（如 SQL 仓库、模型服务端点和 Lakebase）的无缝集成，提供了一种专为 AI 辅助开发而优化的开发者体验。

AppKit 采用分层架构构建：

数据层：与对现代企业应用程序至关重要的现有受治理 Databricks 服务集成，包括结构化/非结构化数据、SQL 仓库、Lakebase PostgreSQL 数据库、模型服务端点、Agent 等。

服务器层：Node.js 后端层，包含不同的用例插件，这些插件是 AppKit 的构建模块。这些插件将身份验证、缓存、流式传输和遥测等功能与超时、重试和速率限制的标准化操作处理相结合。

分析仪表板应用程序服务器示例

客户端层：React 前端层，负责渲染 UI 组件和可视化效果，管理客户端状态和用户交互，并提供类型安全的查询执行钩子。

UI 组件示例

AppKit 带来的结果是，无论是人类开发者还是 AI 编码助手，都能实现更少的代码、更少的错误以及更快的生产部署时间。

## 结合使用 Databricks Apps 和 Replit

我们也很高兴地宣布，现在您可以通过我们与 Replit 的新集成，在一流的开发环境中利用 AppKit。Replit 是协作式、Agent 化应用程序开发领域的领导者。

![结合使用 Databricks Apps 和 Replit](/images/posts/22b941f570cf.png)

此集成允许应用程序开发人员在 Replit 中进行开发，并在 Databricks 上进行部署。您现在可以从 Replit 开始，使用自然语言提示词开发一个能感知您数据的应用程序。Replit Agent 可以检查您有权访问的数据类型，而数据本身无需离开 Databricks。准备就绪后，应用程序可以直接从 Replit 部署到 Databricks。运行的应用程序完全托管在 Databricks 中，并继承 Databricks 的身份验证、Unity Catalog 强制执行的数据治理以及现有的网络限制。

![Replit 部署到 Databricks](/images/posts/245094ee601f.gif)

总之，Databricks + Replit 的集成弥合了快速氛围编码与现代企业严格后端需求之间的差距，使团队能够以前所未有的速度构建复杂的、生产级的应用程序，并充分利用受治理的数据。

我们将在加利福尼亚州圣何塞举行的 AI Dev World（DevWeek 的一部分）上展示 AppKit 和我们 Replit 集成的强大功能。请于 2026 年 2 月 19 日至 20 日期间，莅临圣何塞会议中心的 Databricks 展位，观看现场演示并与我们的团队交流。

准备好开始构建了吗？查看 Replit x Databricks 合作伙伴页面以加入等候名单并获取 Replit 集成的早期访问权限。如果您尚未使用 Databricks，可以注册 Databricks 免费版来创建您的第一个 Databricks App。

## 下一步是什么？

---

> 本文由AI自动翻译，原文链接：[Ship Enterprise Apps Faster with Databricks AppKit and Replit](https://www.databricks.com/blog/ship-enterprise-apps-faster-databricks-appkit-and-replit)
> 
> 翻译时间：2026-02-19 04:45
