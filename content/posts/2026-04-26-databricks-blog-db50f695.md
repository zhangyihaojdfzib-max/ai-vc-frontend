---
title: Databricks Genie升级：统一数据与AI门户
title_original: The next generation of Databricks Genie
date: '2026-04-26'
source: Databricks Blog
source_url: https://www.databricks.com/blog/next-generation-databricks-genie
author: ''
summary: Databricks推出新一代Genie，它能够回答超出Genie Space边界的问题，并连接Google Drive、SharePoint等外部知识库以增强企业上下文。新Genie整合了结构化与非结构化数据，无需预先建模即可提供准确响应，并支持网页及原生iOS/Android应用。此前名为Databricks
  One的业务用户体验已更名为Genie，成为用户访问Databricks的主要方式，提供统一登录、自动化身份管理和按业务概念分组的领域功能。
categories:
- AI产品
tags:
- Databricks Genie
- 自然语言分析
- 企业知识库
- AI门户
- 数据治理
draft: false
translated_at: '2026-04-28T05:34:22.518505'
---

-  Genie 的新版本现已推出，能够回答超出 Genie Space 边界的问题。
-   Google Drive 和 Sharepoint 等外部知识库现在可以连接到 Genie，以增强企业上下文。
-   新的 Genie 体验可在网页以及原生 iOS 和 Android 移动应用上使用。
-   之前被称为“Databricks One”的面向业务用户的体验已更名为 Genie，以反映 Genie 是该体验核心的事实。

今天，我们很高兴地推出下一代 Genie。新的 Genie 可以回答超出 Genie Space 边界的问题，连接到 Google Drive 和 Sharepoint 等企业知识源，并整合结构化与非结构化数据以生成洞察。Genie 现在包含了之前被称为 Databricks One 的所有功能，标志着业务用户与平台互动方式的重大转变。结合账户级访问权限以及原生 iOS 和 Android 应用，Genie 正成为用户体验 Databricks 的主要方式——随时随地可用。

## 无需预先建模即可获得准确响应

自然语言分析现已广泛可用，但提供准确、一致的答案仍然是一个挑战。当 Databricks 进入这一领域时，我们选择不构建另一个容易出错的文本到 SQL 接口。相反，我们引入了 Genie Spaces：一种精心策划的体验，团队可以在其中为 AI 应用防护措施，包括专用知识库、基准测试以及针对特定领域的已验证指标逻辑。客户欣然接受了这种方法，仅在 2026 年就创建了超过 150 万个 Genie Space。随着采用率的增长，他们希望找到一种方法，在不牺牲信任的情况下将这些体验整合在一起。

新的 Genie 正是做到了这一点。从一个单一的聊天界面，它能够利用最相关且最受信任的资产，包括经过认证的 Genie Space、受控的仪表板和 Databricks Apps，并复用其中已嵌入的逻辑。它依赖于您的分析师和工程师已经验证过的相同业务逻辑，并通过元数据引导路由，使高信任度的来源获得优先处理。这意味着您无需新的上下文层或冗长的模型构建即可获得高质量的结果。Genie 建立在您的企业多年来发展的逻辑之上。

![Genie 新的统一聊天界面](/images/posts/5f0075fff113.gif)

新的 Genie 由最新的推理模型和新的 Agent 架构驱动，增强了其回答复杂和开放式问题的能力。当您处理跨多个数据领域的问题时，这一点最为明显。

## 连接企业系统和知识库

我们知道许多上下文，尤其是较高级别的业务知识，存在于非结构化来源中，例如 Google Docs、SharePoint 和其他企业系统。这就是为什么我们现在在 Genie 中增加了内置连接器并支持 MCP 连接。这使得 Genie 能够访问这些来源并采取行动，将洞察与执行联系起来。所有连接都通过 Unity Catalog AI Gateway 进行管理，确保它们易于使用且得到良好治理。

![Genie 现在连接到不同的结构化和非结构化来源](/images/posts/fd221a12ad57.gif)

## 面向业务用户的全球统一门户

AI 正在让数据更贴近每一位业务用户，但访问仍然是碎片化的。用户仍然需要知道去哪里，而 Agent 则因孤立的视图而运作，限制了其有效性。这种模式已不再适用。

去年，我们推出了 Databricks One，这是一种简化的体验，帮助业务用户在一个地方访问仪表板、应用和 Genie。该产品的采用率非常高。

我们已将这些概念融入 Genie，并通过消除 Databricks 工作区边界，移除了简单访问的最后一道障碍，为 Databricks 创建了一个全球门户。此体验现已取代 Databricks One。为了保持与现有用户的兼容性，我们保留了 `/one` URL，为数据和 AI 提供了一个统一入口。

对于许多团队来说，Genie 正迅速成为业务用户的默认界面。

为业务用户创建一个真正的门户需要的不仅仅是聚合资产。它必须直观、易于导航，并抽象掉底层复杂性。为此，新的 Genie 体验还提供：

-   **自动化身份管理**：通过 Entra 和 Okta 持续同步访问权限
-   **领域**：按业务概念（例如供应链或营销）而非工作区对资产进行分组
-   **自定义 URL**：提供单一、易记的入口点，例如 `mycompany.databricks.com`
-   **统一登录**：消除用户在不同工作区之间切换时的障碍，现已支持超过 10 万名用户
-   **Unity Catalog**：确保整个体验中的一致治理
-   **业务语义**：为资产和 Genie 的统一聊天提供受信任的指标定义

有了这个基础，Genie 成为业务用户查找、理解和使用数据的唯一场所，而无需了解数据在后台是如何组织的。

## 在任何设备上使用数据和 AI

Genie 的使命是让每位员工都能访问数据、AI 和洞察，但仅限桌面的体验无法覆盖大多数员工。零售店员、临床医生、现场团队以及移动中的领导者都远离笔记本电脑。因此，我们很高兴为 Genie 推出适用于 iOS 和 Android 的原生移动应用。

完整的 Genie 体验现已呈现在您的手机上，包括仪表板、应用和聊天，并由相同的受控数据和逻辑驱动。用户无论身在何处，都能获得同样值得信赖的答案。这使得业务用户能够随时随地获得即时答案。

![Genie 即将通过原生应用登陆 iOS 和 Android](/images/posts/6227f03baec4.gif)

## 开始使用

如果您有兴趣了解更多关于这些令人难以置信的新 Genie 功能：

-   查看新 Genie UI 的**产品文档**
-   阅读关于**新统一聊天**体验的内容
-   了解 Genie 现在如何在**账户级别**运作
-   与您的 Databricks 客户团队合作，申请访问 Genie 移动应用

我们期待看到 Genie 如何将数据和 AI 带给您组织中的每一位用户。

---

> 本文由AI自动翻译，原文链接：[The next generation of Databricks Genie](https://www.databricks.com/blog/next-generation-databricks-genie)
> 
> 翻译时间：2026-04-28 05:34
