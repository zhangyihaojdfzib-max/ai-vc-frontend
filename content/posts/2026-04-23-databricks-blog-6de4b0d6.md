---
title: Databricks推出Lakeflow Designer公开预览版
title_original: Announcing the Public Preview of Lakeflow Designer
date: '2026-04-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-public-preview-lakeflow-designer
author: ''
summary: Databricks宣布Lakeflow Designer进入公开预览阶段，这是一款可视化、无代码、AI原生的数据准备与分析工具。它直接构建在Databricks平台之上，由Unity
  Catalog管理，无需移动数据即可提供数据血缘、权限和生产就绪代码。通过将工作分解为可视化算子并逐步预览数据变化，AI生成的转换更易于审查和信任。该工具旨在降低技术门槛，让分析师和领域专家也能轻松进行数据准备，同时底层生成可投入生产的Python代码。
categories:
- AI产品
tags:
- Databricks
- Lakeflow Designer
- 无代码数据准备
- AI原生
- 数据治理
draft: false
translated_at: '2026-04-24T04:57:52.867621'
---

- Lakeflow Designer 现已进入公开预览阶段，为 Databricks 用户提供了一种可视化、无代码、AI 原生的数据准备和分析方式。
- Lakeflow Designer 直接构建在 Databricks 之上，并由 Unity Catalog 管理，在保持数据原位的同时，从第一天起就提供数据血缘、权限和生产就绪的代码。
- Lakeflow Designer 通过将工作分解为可视化算子，并逐步预览数据变化，使 AI 生成的转换更易于审查和信任。

我们去年在数据与 AI 峰会上首次介绍了 Lakeflow Designer。此后，我们与早期客户密切合作，完善产品并更好地了解其最适用的场景。今天，我们很高兴地宣布 Lakeflow Designer 进入公开预览阶段。Lakeflow Designer 消除了当今数据领域最大的瓶颈之一：技术门槛。

## 什么是 Lakeflow Designer？

Lakeflow Designer 是一种用于数据准备和分析的可视化、无代码、AI 原生的体验。它直接构建在 Databricks 中，允许分析师、领域专家和其他技术能力较弱的用户通过拖拽画布和自然语言来准备和探索数据。

Lakeflow Designer 中的每一步都表示为一个算子，为用户提供数据在整个工作流中如何变化的清晰图景。这使得在操作过程中更容易构建、验证和理解数据转换。

Lakeflow Designer 将 Databricks Lakeflow 的能力扩展到更广泛的用户群体，支持无代码数据准备，同时在底层生成生产就绪的代码。工作流可以通过 Lakeflow Jobs 进行调度和运维，从而轻松地从交互式数据准备过渡到生产管道。

## Lakeflow Designer 有何不同？

自助式数据准备并非新概念，但现有工具位于您的中央数据平台之外。这带来了权衡：
- 数据准备工具与数据平台之间的脱节造成了治理缺口和额外的 IT 开销
- AI 是附加功能，由于工具对数据没有真正的理解，其建议是通用的
- 可视化工作流难以投入生产，逻辑常常被困在特定领域语言或 UI 中
- 按用户许可费用昂贵，限制了访问权限

Lakeflow Designer 采取了不同的方法。

1. 原生构建于 Databricks，实现治理与简化
Lakeflow Designer 直接在您的数据所在位置——Databricks 上运行。无需将数据移动到单独的工具或本地机器上。数据保持原位，从一开始就由 Unity Catalog 管理，同时简化了整个数据栈。组织无需管理一个拥有自己许可、权限和管理模式的独立低代码工具，而是可以直接在 Databricks 内启用自助服务工作。

立即开始使用原生源数据

2. 从头开始为 AI 构建，并旨在使 AI 可审查
Lakeflow Designer 构建于 Genie Code（Databricks 的原生智能体编码助手）之上。AI 在这里不是附加功能，而是产品运作的核心。只需用简单的英语描述您的需求，Genie Code 就可以直接生成或修改工作流。

AI 原生创作，即开即用

由于 Lakeflow Designer 直接嵌入在 Databricks 工作区中，Genie Code 不仅可以推理列名。它可以使用 Unity Catalog 元数据、表描述、血缘、流行度和示例查询来理解数据的语义含义，并为任务识别正确的资产。与仅能看到模式的工具相比，这能带来更具上下文感知和更准确的建议。

这种架构也为更智能的 Agent 行为打开了大门。系统不是一次性地生成静态结果，而是可以执行转换、检查输出，并在需要时进行迭代。例如，如果连接失败或返回空行，Genie Code 可以评估结果并尝试替代方法。

同样重要的是，Lakeflow Designer 通过将 AI 生成的转换分解为离散的可视化算子，并在每一步提供数据预览，使其易于理解和验证。您可以确切地看到哪些内容发生了变化，哪些行被过滤，连接是如何解决的，以及在继续之前输出结果的样子。

![](/images/posts/7b320ee90d78.png)

3. 每个可视化转换都能生成真实的、生产就绪的代码
Lakeflow Designer 中的每个转换都在底层生成生产就绪的 Python 代码。这些代码可以被审查、在 Git 中进行版本控制，并直接集成到更大的生产工作流中。随着时间的推移，Designer 还将支持更多原生生产输出，例如物化视图。这最终降低了自助服务工具的最大成本之一：将工作移交给工程团队以重建用于生产。中央数据团队无需在另一个系统中重做工作，而是可以在用户已创建的基础上进行构建。

4. 无按用户许可
我们在传统低代码工具中看到的最大采用障碍之一是定价。基于座位的许可迫使团队预先决定哪些用户值得授予访问权限，这减慢了采用速度，并在自助服务开始之前就对其进行了限制。

使用 Lakeflow Designer，没有按用户许可模式。您只需为您使用的计算资源付费。企业中的每个人都可以参与数据工作，而不会产生新的采购瓶颈。

## 团队如何使用 Lakeflow Designer

我们已经看到来自不同行业的数百个团队使用 Lakeflow Designer 以以前难以在没有工程支持的情况下扩展的方式准备和处理数据。

例如：
- 咨询和专业服务团队使用 Lakeflow Designer 清理来自电子表格、PDF 和共享文件的客户数据，然后应用可重复的审计或分析工作流来生成报告。
- 金融服务组织使用 Lakeflow Designer 进行自助数据准备、监管报告和风险分析。
- 营销、运营和物流等业务团队使用它来合并来自多个来源的数据，回答运营问题，并为仪表板准备数据。

我们还看到 Lakeflow Designer 在更广泛的 Databricks 平台中扮演着重要角色。团队正在使用它来准备流入 Metric Views 和 AI/BI 仪表板的数据，创建一个完整的自助服务循环。分析师无需编写代码即可从原始表格过渡到精美的仪表板。

## 开始使用

Designer 目前在所有工作区中可用。要开始使用，请单击工作区左上角的 + New 按钮，然后选择 Visual data prep。如果您没有看到 Visual data prep 选项，则可能需要管理员在预览门户中启用 Designer。

以下是您可以使用 Lakeflow Designer 进行的一些后续步骤：
- 观看 Lakeflow Designer 的 8 分钟演示视频
- 查看文档页面，获取有关开始使用 Lakeflow Designer 的更详细资源。
- 客户反馈持续塑造产品并在我们的路线图中发挥关键作用。如果您有任何反馈或问题，我们期待通过 [email protected] 收到您的来信。

### 在您的收件箱中获取最新文章

订阅我们的博客，将最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Announcing the Public Preview of Lakeflow Designer](https://www.databricks.com/blog/announcing-public-preview-lakeflow-designer)
> 
> 翻译时间：2026-04-24 04:57
