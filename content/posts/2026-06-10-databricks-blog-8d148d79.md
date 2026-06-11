---
title: Databricks推出自定义URL，统一账户体验
title_original: Announcing the Public Preview of Custom URLs
date: '2026-06-10'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-public-preview-custom-urls
author: ''
summary: Databricks宣布公开预览自定义URL功能，允许账户使用统一品牌域名（如mycompany.databricks.com）替代每个工作区的独立URL。用户只需登录一次即可无缝访问所有工作区，解决了多工作区管理中的登录繁琐和导航不便问题。该功能还解锁了账户级Genie体验、跨工作区Unity
  Catalog血缘关系，并简化了灾难恢复。启用需统一登录，支持前端Private Link和Azure环境。
categories:
- AI基础设施
tags:
- Databricks
- 自定义URL
- 统一登录
- 工作区管理
- 数据治理
draft: false
translated_at: '2026-06-11T06:49:18.166393'
---

- 自定义URL为您的Databricks账户提供一个统一的品牌域名（如mycompany.databricks.com），取代账户中每个工作区的独立URL。
- 此前，每个工作区都有独立的URL和登录会话。这在仅有少数工作区时尚可管理，但随着客户扩展到数十个工作区，这种方式变得难以维护。
- 用户现在只需登录一次，即可无缝访问账户中所有可用的工作区。这为业务用户解锁了账户级Genie功能、跨所有工作区的Unity Catalog血缘关系，并简化了灾难恢复。

## 统一的Databricks体验

您的Databricks账户现在可以托管在单一品牌域名（例如mycompany.databricks.com）上，用户只需登录一次，即可在所有使用的工作区中保持登录状态。

此前，每个Databricks工作区都有自己晦涩难记的URL（例如dbc-a3abed8a-27dfe.cloud.databricks.com）。这些URL难以记忆、不便分享，且需要额外努力才能实现品牌化。当客户扩展到数十个工作区时，这变成了日常的用户体验负担，因为每次切换工作区都需要重新登录，网页书签开始堆积，而Genie等账户级功能也没有明确的入口。

自定义URL使账户成为Databricks的自然入口点。一个品牌域名现在服务于账户中的所有工作区，用户只需登录一次，即可在切换工作区时保持登录状态。在底层，当用户切换工作区时，其访问权限会被自动验证，并无缝创建新会话。相同的授权边界得以强制执行，无需重复登录。现有的每个工作区URL仍然有效，因此书签和程序化工具不受影响。

## 自定义URL的主要优势

1. 跨工作区更便捷的导航

日常跨工作区操作的用户不再被打断。Databricks中的典型工作流可能跨越多个工作区（例如，在开发环境中打开笔记本，在预发布环境中运行作业，在生产环境中查询表）。使用自定义URL，您的登录会话会跟随您在账户中的操作，让您无需每次都登录即可无缝切换可访问的工作区。

![image1.gif](/images/posts/8645db4d859b.gif)

2. 为业务用户提供无缝的Genie体验

自定义URL（mycompany.databricks.com/one）实现了统一的Genie聊天体验，使业务用户能够轻松访问整个数据资产中的洞察，发现AI/BI仪表板、应用程序和Genie空间。登录会话覆盖整个账户，因此用户只需登录一次。

![image3.png](/images/posts/e2098203919d.png)

3. Unity Catalog中的跨工作区血缘关系和资产治理

使用自定义URL，Unity Catalog血缘关系反映的是您账户的完整形态，而不仅仅是单个工作区。用户可以看到一个单一的血缘视图，其中包含您账户中每个工作区的上游和下游资产。例如，用户可以查看其他工作区中的哪些仪表板依赖于某个特定表，或者哪些作业会写入该表。由于血缘视图使用共享的账户会话，这些信息会从每个工作区无缝拉取，无需额外的登录提示。

![image4.png](/images/posts/57790b8b7f5c.png)

4. 更简单的灾难恢复

自定义URL提供了一个单一的账户级入口点，可以将用户路由到正确的工作区，无论该工作区当前位于何处。这使得灾难恢复更加简单，因为当发生故障转移时，URL本身不会改变。Power BI、ODBC客户端和CI/CD管道等下游工具继续使用其现有的连接字符串，并且用户无需再次登录，因为他们的会话会跟随他们跨区域移动。

![image2.png](/images/posts/71b2108bde0a.png)

## 公开预览注意事项

在启用前需要了解的一些细节：

- 需要统一登录。自定义URL需要统一登录。这是2023年6月21日之后创建的账户以及2024年12月12日之前配置了SSO的账户的默认设置。
- 前端Private Link。启用了FE Private Link的工作区将回退到每个工作区的URL。用于自定义URL的账户级FE Private Link即将在Beta版中推出。
- Azure Databricks：Azure Databricks客户的自定义URL遵循mycompany.azuredatabricks.net约定。

## 开始使用自定义URL

账户管理员可以从账户控制台的“账户设置”中启用自定义URL：

- 认领您的URL。如果您的账户已有自定义URL，您只需将其切换为开启即可。我们稍后将扩展自助服务选项。
- 开启自动重定向。开启自动重定向后，访问旧版每个工作区URL（例如dbc-a3abed8a-27dfe.cloud.databricks.com）的用户将被自动重定向到自定义URL上的等效路径。您的书签仍然有效，但所有新的导航都将通过您的品牌域名进行。启用后，您和您的用户可以导航到mycompany.databricks.com/one以访问账户级主页。请注意，对旧版URL的程序化流量不会受到影响。

启用后，导航到mycompany.databricks.com/one以访问Genie、您的AI/BI仪表板、Genie空间和应用程序的账户级主页。

## 后续计划

- 自定义URL和账户级前端Private Link支持正式发布。
- 在此基础上增加更多账户级体验，包括统一的IAM管理、账户级搜索和跨工作区资产视图。

认领您的自定义URL

为您的Databricks账户认领您的品牌自定义URL，让用户无缝访问每个工作区。

### 在您的收件箱中获取最新文章

订阅我们的博客，将最新文章发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Announcing the Public Preview of Custom URLs](https://www.databricks.com/blog/announcing-public-preview-custom-urls)
> 
> 翻译时间：2026-06-11 06:49
