---
title: 利用Agent Bricks与Databricks Apps，向业务用户交付高质量企业级AI智能体
title_original: Ship quality enterprise AI agents to business users with Agent Bricks
  and Databricks Apps
date: '2026-03-16'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ship-quality-enterprise-ai-agents-business-users-agent-bricks-and-databricks-apps
author: ''
summary: 本文探讨了企业AI智能体从原型到生产部署的挑战，包括评估困难、参数复杂、成本控制及安全治理等问题。文章提出了一条基于Databricks平台的快速、受管控的部署路径，通过整合Agent
  Bricks（用于构建、评估和优化智能体）、Databricks Apps（用于安全部署交互界面）和Databricks One（提供统一用户入口）三大组件，帮助企业快速将领域特定的知识助手（如基于内部政策文档的问答系统）交付给业务用户，实现从概念验证到生产就绪的加速。
categories:
- AI产品
tags:
- 企业AI
- AI智能体
- Databricks
- 生产部署
- 知识管理
draft: false
translated_at: '2026-03-17T04:38:17.976993'
---

构建一个AI Agent（智能体）原型很容易。但交付一个能让业务用户信任、且不被安全团队阻拦的Agent，才是大多数企业项目进度放缓的关键所在。

在本博客中，我们将介绍一条利用Databricks平台实现快速、受管控的生产部署路径：

1.  构建一个生产级、领域特定的Agent，具备内置评估和持续改进能力
2.  使用Databricks Apps部署一个可定制的聊天界面，该界面内置单点登录和受管控的数据访问
3.  通过一个简化、直观的体验，将您的Agent分发给业务用户，供其消费AI和数据洞察

我们将贯穿全文使用一个共享示例：为一个名为Redwood Commerce的示例公司构建一个**Agent Bricks知识助手**，该助手能基于内部PDF文件回答公司政策问题，并提供回溯到源文档的引用。

## 为何实现Agent生产化部署仍然困难

开发企业级AI Agent的团队通常会遇到一系列常见问题：

*   **评估困难**：许多企业AI任务难以评估，无论是对人类还是对自动化的LLM（大语言模型）评判者而言都是如此。学术基准无法转化为实际用例。构建细致的评估通常需要昂贵的人工标注。结果，有前景的项目陷入无尽的调优循环，利益相关者因进展不明确而失去信心。
*   **可调参数过多**：Agent是复杂的AI系统，包含许多组件，每个组件都有其自身的可调参数。从调整提示词到索引分块策略，再到模型选择和微调参数，每次调整都会在整个系统中产生未知影响。本应快速的迭代改进变成了昂贵且繁琐的手动试错，从而拖慢了生产部署时间。
*   **成本与质量**：即使在团队解决了上述问题并构建出高质量的Agent之后，他们常常惊讶地发现，Agent的成本太高，无法扩展到生产环境。团队要么陷入漫长的成本优化过程，要么被迫在成本和质量之间做出权衡。

除此之外，您还需要为业务用户提供一个直观的UI，以及考虑到您的治理模型的安全访问。

我们的目标是减少这些摩擦，让您能在几天甚至几小时内，从概念验证阶段推进到业务就绪状态，而不是花费数月时间。

## 快速、受管控的路径：Agent Bricks、Databricks Apps 和 Databricks One

为了让您的AI Agent投入生产，Databricks提供了三个无缝集成的组件：

*   **Agent Bricks** 简化了基于企业数据构建、评估和优化生产级AI Agent的过程。您只需定义任务并连接数据，Agent Bricks会处理繁重的工作，包括内置评估和统一的Unity Catalog治理。
*   **Databricks Apps** 允许您在Databricks内部安全地部署这些Agent和可定制的聊天界面。您将获得无服务器计算、内置单点登录和细粒度权限，而无需管理云基础设施。
*   **Databricks One** 为您的业务用户提供了一个简化、精选的"前门"。用户无需搜索内部维基页面或维护仪表板书签，而是可以通过一个直观的中心与Apps、Dashboards以及其他数据和AI资产进行交互。

让我们看看这三个组件在实践中如何协同工作。

## 示例：构建公司政策助手

Redwood Commerce是一家虚构的企业，其公司政策文件（差旅、费用、病假、IT安全）以已批准的PDF形式存储。

员工反复提出类似这样的问题："我可以报销酒店干洗费吗？"

业务用户希望获得一个简单的聊天体验，能够：

1.  基于已批准的公司政策文件进行回答
2.  提供引用以建立信任和验证
3.  尊重权限和治理规则
4.  可以在组织内广泛但安全地分享给员工

### 步骤 1：在 Agent Bricks 中创建知识助手

Agent Bricks 支持多种**用例**，包括**知识助手**，它可以将您的文档转化为高质量的聊天机器人，用于回答问题并引用其来源。

#### 连接政策文档

知识助手可以使用：

*   Unity Catalog卷中的文件（txt、pdf、md、ppt/pptx 和 doc/docx）。
*   使用 databricks-gte-large-en 作为其嵌入/向量模型的现有**向量搜索索引**。

对于 Redwood Commerce，我们将采用最简单的路径：将公司政策 PDF 存储在 Unity Catalog 卷中。

#### 构建 Agent

在 Databricks 工作区 UI 中：

1.  导航到 Agents
2.  在 Knowledge Assistant 下，选择 Build
3.  为其命名（例如，`Redwood Policy Assistant`）并添加描述
4.  选择 Unity Catalog 文件位置作为知识源
5.  创建 Agent

知识助手会创建一个 Agent 端点，您可以在下游应用程序中使用。

### 步骤 2：快速验证质量（并借助领域专家进行改进）

一个常见的失败模式是部署一个听起来正确但不可信的Agent。Agent Bricks知识助手明确设计为返回带有引用的高质量响应，这是建立利益相关者信心的关键。

我们可以直接在知识助手UI或**AI Playground**中测试Agent，并提出现实问题：

*   "我可以报销酒店干洗费吗？"
*   "我如何报告病假？"
*   "差旅报销流程是什么？"

Agent的回答基于文档，并引用了相关政策章节。

Agent Bricks支持基于领域专家提供的自然语言反馈来改进Agent行为，方式是提供标注问题和指导原则。

指导原则通过为语气、结构和行为设定明确期望，用于改进Agent的响应。它们有助于确保Agent沟通清晰、保持品牌一致性，并以正确方式处理不同场景。这些相同的指导原则也用作评估标准，为每个响应生成质量分数。

在您的知识助手Agent的"示例"标签页下添加问题。要邀请领域专家提供标注问题和指导原则，请通过三点菜单选择"权限"来分享知识助手。

### 步骤 3：使用 Databricks Apps 部署聊天界面

一旦我们对Agent质量感到满意，就可以将Agent端点转化为员工实际可以使用的东西：为Redwood Commerce量身定制的聊天体验。

Databricks Apps允许您部署完全自定义的应用，或者从预构建的聊天模板开始，并根据您的品牌进行定制。

1.  导航到 Compute 并选择 Apps 标签页
2.  选择 Create app
3.  选择 Agents 标签页并选择 Chat UI 模板
4.  将其指向知识助手端点
5.  部署您的应用

部署应用后，您可以通过提供的应用URL直接在应用模板中使用您的知识助手聊天机器人。

要创建更具品牌特色的体验，您可以通过将模板克隆到本地机器来进行定制。只需进行一些简单的调整，我们就可以为Redwood Commerce创建一个专属的聊天界面：

Databricks Apps内置了安全性和治理功能，无需开发和维护自定义的身份验证或授权代码。

Apps仅对使用单点登录进行身份验证的用户开放。没有匿名或公共访问权限。得益于**用户授权**，您的应用可以通过以应用用户的身份进行操作来应用细粒度权限。

### 步骤 4：通过 Databricks One 发布给业务用户

我们可以简单地通过发送应用URL来分发应用。但是，当您向业务用户提供更多数据和AI资产时，团队需要一个单一的、精选的地方，让员工可以可靠地找到正确的工具。

Databricks One 就是为此"前门"而设计的：一个简化的UI，业务用户可以在其中访问Databricks中共享的数据和AI资产，包括Databricks Apps。

启用 Databricks One 并配置正确的工作区权限后，我们就可以与从身份提供商同步的员工组分享 Databricks App。

如今，员工只需打开 Databricks One，点击策略助手，然后提问：

“我可以报销酒店延迟退房费用吗？”

他们便能获得附带引用的答案，且整个治理流程始终保持一致。

## 开始向业务用户交付 Agent（智能体）

Agent Bricks 知识助手为您提供了一条快速、自动化的路径，可将您的企业文档转化为特定领域的 Agent（智能体），同时通过内置的评估和优化功能，确保质量可衡量并持续提升。

借助 Databricks Apps 和 Databricks One，您可以将该 Agent（智能体）打包成便于业务使用的聊天体验，并通过精心设计的入口点进行分发，同时确保端到端的安全性和 Unity Catalog 治理。

如需深入了解，请从以下资源开始：

- Agent Bricks 文档和演示：知识助手和监督员 Agent（智能体）
- Databricks Apps 演示、入门指南和文档
- Databricks One 文档和消费者访问权限

---

> 本文由AI自动翻译，原文链接：[Ship quality enterprise AI agents to business users with Agent Bricks and Databricks Apps](https://www.databricks.com/blog/ship-quality-enterprise-ai-agents-business-users-agent-bricks-and-databricks-apps)
> 
> 翻译时间：2026-03-17 04:38
