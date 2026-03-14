---
title: Azure Databricks无服务器工作空间正式发布，实现秒级就绪
title_original: Serverless Workspaces in Azure Databricks is now Generally Available
date: '2026-03-13'
source: Databricks Blog
source_url: https://www.databricks.com/blog/serverless-workspaces-azure-databricks-now-generally-available
author: ''
summary: 微软Azure Databricks正式推出无服务器工作空间，彻底简化了数据平台部署流程。该模式无需用户预先配置虚拟网络、防火墙等底层基础设施，由Databricks托管计算与存储资源，实现分钟级工作空间创建和即时无服务器计算。它内置与Unity
  Catalog集成的安全存储、Entra ID集成及企业级治理能力，同时保留了经典工作空间模式以满足自定义网络等高级需求，为分析、BI和AI工作负载提供了更快速、简单的安全起点。
categories:
- AI基础设施
tags:
- Azure Databricks
- 无服务器计算
- 数据平台
- 云计算
- 微软Azure
draft: false
translated_at: '2026-03-14T04:52:06.981205'
---

我们很高兴地宣布，**无服务器工作空间现已在 Azure 上全面推出**，使 Azure Databricks 成为一个可在数秒内就绪的完全托管平台。

无服务器工作空间简化了工作空间的创建。传统上，在 Azure 上创建 Databricks 工作空间意味着首先要设计和部署云基础设施——设置虚拟网络、分配 IP 地址范围、配置 NAT 网关以及定义防火墙规则——然后团队才能开始处理数据。这些经典工作空间提供了对网络和基础设施的深度控制，但它们通常需要 IT、网络和安全团队之间进行大量的规划和协调。

无服务器工作空间消除了工作空间创建的障碍。

借助无服务器工作空间，Databricks 开箱即用地提供无服务器计算和默认存储，无需进行任何基础设施设置。计算在 Databricks 托管的 Azure 网络中运行，将网络、扩展和隔离的责任转移给 Databricks——这样团队就可以专注于洞察分析，而非基础设施。

## 客户为何选择无服务器工作空间

无服务器工作空间帮助团队更快地开展工作，减少跨组织的协调，同时仍能保持强大的治理和安全性。

主要优势包括：

-   **更快实现价值**：在几分钟内启动工作空间，无需等待 IT 部门。团队可以立即访问分析和 AI 工具，并内置成本可见性。
-   **零设置、安全的存储**：每个工作空间都包含与 Unity Catalog 集成的 Databricks 托管存储。多密钥保护、无法直接访问对象存储等功能确保只有授权用户才能访问您的数据。
-   **即时无服务器计算**：无需预配或管理集群即可立即运行工作负载。Azure Databricks 会自动高效地部署和扩展无服务器计算，从而减少 Azure 数据团队的操作开销。
-   **内置治理**：从第一天起即可使用现有的 Unity Catalog 数据和权限。这确保了一致的访问控制和血缘追踪，并可集成 Microsoft Purview 以获得更广泛的数据资产可见性。
-   **简化的 Azure 网络**：无需设计虚拟网络、NAT 网关或专用终结点，无服务器网络策略由我们为您管理。

## 这对 Azure Databricks 客户意味着什么

对于在 Microsoft Azure 上进行标准化的组织而言，无服务器工作空间为分析、BI 和 AI 提供了一个**简单、安全的起点**，而无需重新架构其 Azure 环境。

无服务器工作空间遵循 Azure 原生、服务托管的模式，可与客户已经依赖的 Microsoft 生态系统无缝集成，同时通过 Unity Catalog 保持企业级治理，包括访问 UC 中已定义的现有数据资产和权限。

团队可以立即利用以下功能：

-   与 **Entra ID** 原生集成，用于身份和访问管理
-   通过 Unity Catalog 将受治理的数据无缝发布到 **Power BI**
-   结合 **Azure Databricks 与 Azure OpenAI** 进行安全的 AI 开发
-   在 Microsoft 分析生态系统中实现互操作性，无需复制数据或治理模型

## 何时使用无服务器与经典模式

Azure Databricks 同时支持**无服务器和经典工作空间模型**，让客户可以根据工作负载和组织需求灵活选择。

在以下情况选择无服务器工作空间：

-   速度和简单性很重要
-   您希望最大限度地减少基础设施设置和操作开销
-   团队需要快速启动，无需 IT 部门深度参与

在以下情况选择经典工作空间：

-   您需要自定义网络配置
-   您需要对 Azure 基础设施进行直接控制
-   您的环境有高级或特殊的安全要求

许多客户**同时使用这两种模型**，为每个工作负载选择合适的方法。

立即了解如何设置 Azure 无服务器工作空间 | 免费开始使用 Azure Databricks →

---

> 本文由AI自动翻译，原文链接：[Serverless Workspaces in Azure Databricks is now Generally Available](https://www.databricks.com/blog/serverless-workspaces-azure-databricks-now-generally-available)
> 
> 翻译时间：2026-03-14 04:52
