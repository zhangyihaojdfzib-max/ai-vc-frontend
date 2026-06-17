---
title: Databricks发布三大功能，赋能企业级Vibe Coding
title_original: Enabling Governed Vibe Coding for Enterprise Apps on Databricks
date: '2026-06-16'
source: Databricks Blog
source_url: https://www.databricks.com/blog/enabling-governed-vibe-coding-enterprise-apps-databricks
author: ''
summary: Databricks在2026年数据与AI峰会上推出三项新功能，旨在将Vibe Coding引入企业应用开发。App Spaces提供治理边界，实现应用组的资源与安全策略统一管理；Genie
  App Builder作为原生AI创作工具，能感知数据资产和Unity Catalog语义；无服务器微应用运行时支持缩容至零，降低间歇性应用成本。这些功能使业务人员能快速构建应用，同时不牺牲数据治理、安全性和成本控制。
categories:
- AI产品
tags:
- Databricks
- Vibe Coding
- 企业应用
- AI治理
- 无服务器
draft: false
translated_at: '2026-06-17T07:09:48.843049'
---

- 在2026年数据与AI峰会上，Databricks发布了三项用于在Databricks上构建应用的新功能：用于管理应用组的App Spaces、具备数据感知能力的Databricks原生Agent构建工具Genie App Builder，以及一种新的轻量级微应用运行时，用于构建成本更低、可缩容至零的应用。
- Vibe coding快速且易用，但企业应用同样需要数据上下文和控制能力。这些功能填补了这一空白，使团队能够快速构建应用，同时不牺牲治理能力。
- 总而言之，这些功能释放了最了解业务的人员的创新潜力，同时无需放弃对数据、治理或成本的控制。

### Vibe coding需要上下文和控制才能在企 业中发挥作用

编码Agent的崛起不容忽视。仅在过去六个月中，Databricks Apps的客户构建应用数量大幅增长，活跃运行应用数量几乎翻倍，每周与应用交互的用户数量增长了3倍以上。

任何有明确想法的人——无论是业务分析师、领域专家还是运营负责人——都可以用自然语言描述需求，并在数小时内获得一个可运行的应用。这正在改变我们的客户与数据交互的方式。

但在企业中，团队需要的不仅仅是快速起步来获取价值。大多数vibe coding工具都针对速度和易用性进行了优化。然而，如果没有基于真实业务数据构建应用的上下文，或者缺乏确保所构建内容安全部署且成本效益的控制能力，应用就无法在组织中产生广泛影响。

在2026年数据与AI峰会上，我们讨论了Databricks如何通过三项针对Databricks Apps的新关键功能，将vibe coding引入企业：

- App Spaces，一种新的治理边界，用于为应用组配置资源、访问管理及安全策略。
- Genie App Builder，一款专为Databricks打造的AI应用创作工具，原生感知您的数据资产、Unity Catalog语义及工作空间上下文。
- 全新类别的无服务器微应用，可在需要时快速启动，空闲时缩容至零，使组织能够支持广泛的应用组合，而无需承担始终在线基础设施的成本。

![](/images/posts/fd9181e5aceb.png)

### App Spaces：治理优先的方法

我们的目标是让组织中的任何用户都能在Databricks上安全地创建和部署应用。

但这意味着Databricks管理员需要确保开发者——他们可能并非应用安全专家——能够安全地处理数据。随着越来越多的人构建越来越多的应用，治理不能逐个应用进行。逐个应用的配置无法扩展，并会给平台团队带来瓶颈。

App Spaces旨在解决这一问题。管理员在App Space级别定义资源和数据访问权限、用于“代表用户”访问的API范围以及安全策略。该空间中的每个应用都会自动继承这些设置。防护措施在第一个应用创建之前就已就位。

这使治理从被动响应转变为系统化管理。平台团队无需逐一审查每个新应用，而是可以为构建者创建预批准的环境。构建者获得更多自主权，管理员则能获得整个应用组合的一致可见性——哪些应用存在、谁拥有它们、它们如何被使用。

### Genie App Builder：借助所有Databricks上下文的AI辅助创作

Genie App Builder为技术团队和非技术团队提供了一条从自然语言描述到可运行内部应用的AI辅助路径。用户描述他们想要构建的内容，或提供截图作为上下文，审查生成的计划，然后通过侧面板中的实时应用预览进行迭代。

![Genie App Builder是一款感知Databricks的应用构建工具，允许您用自然语言构建应用，并通过实时侧面板预览进行迭代。](/images/posts/03e2a544ea9f.png)

在底层，应用基于AppKit构建——这是一个专为生产级Databricks应用设计的TypeScript SDK。AppKit开箱即用地处理内置缓存、遥测、重试逻辑以及与Databricks中数据和资源的无缝集成。

由于Genie App Builder构建于Databricks之上，它能够直接感知您的工作空间：您拥有的表、在Unity Catalog中定义的语义层以及已存在的治理策略。因此，当您在提示词中描述需求时，构建Agent可以找到正确的数据并将其呈现在应用中，而无需手动连接任何内容。

### 无服务器微应用：为可缩容至零的应用构建的基础设施

传统应用基础设施的经济性对于较小、更专业化的应用并不有利。许多此类应用——如部门工具和业务线工作流——是间歇性使用的，大部分时间处于空闲状态。使用始终在线的专用计算意味着要为经常不使用的容量付费。然而，替代方案历来也有其权衡：冷启动慢、缺乏隔离的共享环境，或者由于基础设施成本难以合理化而从未被优先考虑的应用。

无服务器微应用基于新的微VM运行时构建，解决了这一问题。每个应用在其自己的轻量级虚拟机中运行，这意味着它可以在需要时快速启动，空闲时完全缩容，并与其他应用保持隔离。实际结果是，在Databricks上部署轻量级应用变为按使用量计费，而非预留容量计费。这使得创建整类因成本问题而被降级处理的应用变得更为可行。

### 总结

Vibe coding的速度、易用性和快速迭代不必以牺牲生产环境中重要的因素为代价。App Spaces在构建任何应用之前就建立了治理层，Genie App Builder在该层内进行创作，并完全感知您的数据和工作空间上下文，而基于微VM的无服务器微应用则使整个模式在规模上具有经济可持续性。结果是，最接近业务问题的人员可以在真实企业数据上构建和交付应用，组织可以支持广泛的应用组合，而无需承担治理债务或失控的基础设施成本。这三项功能即将登陆Databricks Apps，私有预览即将推出。了解更多信息，请访问Databricks Apps文档。准备好开始构建了吗？前往Databricks Developers获取可复制的提示词，在编码助手的帮助下启动并运行您的第一个应用。如果您错过了峰会会议，可在databricks.com/dataaisummit获取录播内容。

---

> 本文由AI自动翻译，原文链接：[Enabling Governed Vibe Coding for Enterprise Apps on Databricks](https://www.databricks.com/blog/enabling-governed-vibe-coding-enterprise-apps-databricks)
> 
> 翻译时间：2026-06-17 07:09
