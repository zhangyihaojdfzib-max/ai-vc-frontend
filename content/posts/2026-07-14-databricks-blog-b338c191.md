---
title: Genie One移动端：口袋里的数据智能AI同事
title_original: Take insights anywhere with Genie One on mobile
date: '2026-07-14'
source: Databricks Blog
source_url: https://www.databricks.com/blog/take-insights-anywhere-genie-one-mobile
author: ''
summary: Databricks推出Genie One的iOS和Android原生移动应用，让业务用户随时随地通过自然语言提问获取基于企业数据的可信洞察。该应用支持聊天、仪表板探索和Databricks应用访问，并内置企业级治理与安全功能，包括通过身份提供商实现SSO/MFA、源原生ACL和Unity
  Catalog权限控制，以及与网页端一致的网络安全策略。移动端自动适配竖屏和横屏布局，未来还将加入深色模式、推送通知和语音聊天等功能。
categories:
- AI产品
tags:
- Genie One
- 移动应用
- 数据智能
- 企业治理
- 自然语言查询
draft: false
translated_at: '2026-07-15T04:54:44.343820'
---

- Genie One 现已作为 iOS 和 Android 的原生移动应用推出，将数据智能型 AI 同事装进每个人的口袋，让业务用户无论在哪里工作都能获得答案。
- 用户可以通过手机与 Genie 聊天、安排任务、探索仪表板和使用应用，所有这些都像在网页端一样基于业务上下文。
- 基于您现有的控制措施构建：通过身份提供商实现 SSO 和 MFA，通过源原生 ACL 和 Unity Catalog 强制执行权限，以及相同的网络安全，无需单独的移动后端。

我们近期发布了 Genie One，这是一款面向业务用户的数据智能型 AI 同事。今天，我们将深入探讨业务用户如何通过 Genie One 的 iOS 和 Android 移动应用随时随地访问 Genie。

在许多行业中，业务决策往往发生在办公桌之外。零售员工需要现场了解库存数据，现场团队需要实地获取洞察，领导者需要在会议间隙移动中回答问题。这通常意味着记下一个缺乏上下文的提问，希望稍后能想起来，在不方便的时候匆忙找笔记本电脑，或者干脆忘记问题继续工作。

移动端的 Genie One 提供了一种快速、安全的方式，让您无论身在何处都能向数据提问并根据答案采取行动。完整的 Genie One 体验随您而行：聊天、仪表板、Databricks 应用等——所有这些都由您的团队在 Databricks 中依赖的同一受治理数据和业务逻辑驱动。

![databricks apps](/images/posts/3655cc5e6449.png)

## 随时随地获得基于上下文的即时洞察并采取行动

Genie One 移动应用能在几秒钟内将自然语言问题转化为可信的答案。它利用 Genie Ontology（Genie 的自我改进自动上下文层）以及 Genie Agent 提供的进一步策划的领域特定逻辑，生成基于您公司数据和企业治理的结果。内置的与 Google Drive、Microsoft 365 和 Atlassian 等外部业务工具的连接器确保这些答案基于您的业务事实，无论数据存储在哪里，并在每一步都尊重源权限。

对于领导者而言，这意味着可以即时、随时随地检查 KPI 或快速询问“为什么发生了变化”——无需等待分析师队列。对于业务用户而言，这意味着无论在哪里工作，都能以通俗语言获得自助答案和洞察，无需了解数据存储位置或建模方式。

因为找到答案通常只是开始，Genie One 移动应用具备您对 AI 同事所期望的相同 Agent 能力。用户可以使用与网页端相同的核心对话能力与 Genie 聊天，包括对技能和 MCP 的支持。他们还可以查看仪表板、访问 Databricks 应用，并在任何地方获得答案和洞察。我们正在持续扩展移动端功能，以便用户能够从任何地方管理更多工作流程。

## 在移动端探索仪表板

对于需要在移动中探索和交互数据的用户，AI/BI 仪表板已自动适配移动端，这意味着探索比以往任何时候都更容易。在竖屏模式下，组件会重新排列为单列布局，以简化小屏幕上的体验。我们采用行优先排序，因此您放置在顶部和左侧的组件会首先显示。在横屏模式下，我们完全保留您设计的现有布局。

![dashboards](/images/posts/a518b061c8e9.png)

## 无论在哪里工作，都享有企业级治理

与所有 Genie 产品一样，Genie One 移动应用在设计之初就将企业治理和安全作为基础。通过源原生 ACL 或 Unity Catalog，每个答案默认强制执行权限，这意味着用户获得的答案基于他们有权访问的企业数据——而不会看到无权访问的数据。

用户通过身份提供商登录，使用与浏览器相同的 OAuth 流程，并且只能看到他们至少拥有 Consumer 访问权限的工作空间。现有的 MFA、条件访问和设备状态策略会自动延续。没有单独的移动后端，也没有仅限移动端的端点：该应用通过 HTTPS 与浏览器相同的工作空间和账户 URL 通信，因此您现有的网络控制措施（包括 IP 访问列表、Private Link 和 VPN）与在网页端完全一致。支持合规安全配置文件工作空间，数据与在网页端一样保留在区域内。

## 下一步计划

这只是 Genie One 移动应用的开始。我们已经在开发客户最常要求的功能，包括深色模式、定时任务和自动化洞察的推送通知、语音聊天模式，以及在移动端通过账户级别访问 Genie One。随着越来越多的业务用户依赖 Genie One 在他们工作的任何地方获得基于上下文的洞察和 Agent 行动，Genie One 移动应用将继续演进，成为始终装在口袋里的真正 AI 同事。

## 立即开始

您的团队的下一个决策不必等到他们回到办公桌前。将 Genie One 装进他们的口袋，答案在问题出现时即刻准备就绪，基于他们每天依赖的同一可信数据。立即开始。

移动端 Genie One 现已提供公开预览版：

- 下载适用于 iOS 和 iPadOS 的 Genie One
- 下载适用于 Android 的 Genie One
- 管理员：在我们的文档中了解如何推广 Genie One 移动应用

---

> 本文由AI自动翻译，原文链接：[Take insights anywhere with Genie One on mobile](https://www.databricks.com/blog/take-insights-anywhere-genie-one-mobile)
> 
> 翻译时间：2026-07-15 04:54
