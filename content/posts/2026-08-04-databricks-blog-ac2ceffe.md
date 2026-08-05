---
title: Unity AI Gateway正式发布：统一管理AI成本、安全与模型选择
title_original: Unity AI Gateway is Generally Available
date: '2026-08-04'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unity-ai-gateway-generally-available
author: ''
summary: Unity AI Gateway现已正式发布，旨在帮助企业应对AI规模化带来的成本、控制和选择三大挑战。该网关提供端到端的可观测性、成本控制与智能路由，支持跨Agent、模型、MCP和工具的集中管理。通过集成Unity
  Catalog，实现数据和AI的统一治理，并强制执行运行时防护栏。Rivian、Asana等数千家客户已采用，过去一年处理超千万亿Token，助力企业负责任地推广AI。
categories:
- AI基础设施
tags:
- AI网关
- 成本控制
- AI安全
- 模型路由
- 企业AI
draft: false
translated_at: '2026-08-05T05:31:18.605470'
---

• Unity AI Gateway现已正式发布，为企业提供了一种统一的方式来管理跨Agent（智能体）、模型、MCP、技能和工具的AI支出、安全性与访问权限。• 随着AI采用规模的扩大，基于Token的成本可能迅速且不可预测地增长。Unity AI Gateway提供端到端的可观测性、成本控制和智能路由，以最大化每一笔AI投入的价值。• 当Agent（智能体）访问敏感数据、调用工具并采取行动时，AI交互变得更加难以控制。Unity AI Gateway在保持开发者在模型和工具选择自由的同时，应用运行时防护栏和策略。

过去六个月，AI驱动的生产力迅速提升，各类Agent（智能体）在企业中大量涌现。虽然这些Agent（智能体）能够变革知识工作，但它们也在成本、控制和选择这三个交叉领域带来了严峻挑战：

1. 成本：不可持续的支出。随着采用规模扩大，由于基于消费的定价模式（按Token而非席位计费），AI成本呈指数级增长。更棘手的是，AI工具缺乏强大的原生成本控制机制，且无法对整个账单进行统一视图管理。
2. 控制：安全与知识产权风险。要发挥效用，Agent（智能体）必须被信任以访问最敏感的数据。然而，模型正突破安全沙箱，供应链攻击和提示词注入正在窃取数据，数据保留和记忆系统也在制造不受治理的数据副本。
3. 选择：供应商锁定。组织面临压力，需要给予开发者采用最新模型和工具的自由。AI创新的快速步伐（几乎每月都有新模型或Agent（智能体）框架问世！）使得在不被特定供应商绑定的情况下保持敏捷性变得困难。

这些挑战因Agent（智能体）的广泛蔓延而进一步加剧——组织试图在互不关联的平台上管理多种AI工具和数千个定制Agent（智能体）。

企业系统尚未跟上这些挑战的步伐。这正是我们激动地宣布Unity AI Gateway正式发布的原因。Unity AI Gateway为企业提供了所需的成本、控制和选择杠杆，以管理AI支出并在所有AI Agent（智能体）和资产（无论是编码Agent（智能体）、MCP、外部Agent（智能体）、技能还是模型）中强制执行安全策略。Rivian、Asana和Edmunds等数千家客户已使用Unity AI Gateway在其组织中负责任地推广AI，过去一年中，超过千万亿个Token已通过我们的网关。我们Databricks内部也使用Unity AI Gateway来管理数千名员工（每人可访问多种领先AI工具）的支出。

![](/images/posts/5e1f4fbd94ed.png)

## 成本：完整的AI可观测性与成本控制

组织需要全面了解每一笔AI支出的去向，具备实时阻止失控成本的能力，以及一种持续优化AI预算使用方式的方法，同时不拖慢开发者速度或增加其负担。

Unity AI Gateway充当所有AI资产（包括外部Agent（智能体）、MCP、技能和编码助手）的中心枢纽，提供跨模型、提供商、团队和应用的端到端可观测性和细粒度成本归因。通过将这些数据集中到Unity Catalog中，我们提供开箱即用的仪表板和Genie驱动的分析，让您即时深入了解AI投资情况。此外，团队可以设定主动预算并强制执行硬性支出上限，确保AI创新保持可预测性并与业务目标一致。

![](/images/posts/5d189e949879.png)

一种帮助控制AI支出的技术是在前沿模型（包括专有和开源模型）之间进行路由。智能路由现已进入Beta测试阶段，帮助组织最大化AI支出的价值，同时不限制开发者生产力。Unity AI Gateway根据质量、成本、性能、可用性和预算等因素，将每个请求动态路由到合适的模型，将最强大、最昂贵的模型保留给需要它们的任务，同时将其他工作路由到更高效的选项。结果是每一笔AI投入都能获得更大价值，而无需开发者在所用工具或所需质量上妥协。如果您希望参与Beta测试，请联系您的客户团队。

## 控制：通过统一控制平面治理数据和AI

我们坚信数据和AI必须协同治理。毕竟，Agent（智能体）与您最敏感的企业数据交互，并调用MCP服务器和工具代表用户执行操作，从而创建数据和记录系统。而生成的Agent（智能体）追踪记录中充斥着机密信息、PII数据或其他可能无意泄露的密钥。企业需要一种统一的方式来控制Agent（智能体）可以访问和执行的内容，同时维护治理每项操作所需的身份、审计追踪和策略。

借助Unity Catalog和Unity AI Gateway，组织可以在一个地方治理数据和AI。Unity Catalog提供治理数据和AI资产访问的身份、权限、血缘和审计功能，而Unity AI Gateway则在AI交互中强制执行运行时防护栏和上下文策略。两者结合，为团队提供集中化的可见性和控制力，以保护敏感数据、执行策略和调查AI活动，而无需拼凑独立的治理和安全系统。

## 选择：开放、多AI访问，无锁定之虞

开发者希望自由选择最适合其团队的模型、提供商、编码Agent（智能体）和AI工具，而不被锁定在单一AI生态系统中。Unity AI Gateway提供了一种开放、多AI的治理方法，将Unity Catalog的身份、权限、策略和可观测性扩展到团队构建的任何地方。

借助Unity Catalog，组织可以在单一事实来源中注册和发现Databricks托管的及外部的模型、编码Agent（智能体）、MCP服务器和技能。Unity AI Gateway随后在与这些AI资产的交互中强制执行治理，无论它们在哪里使用，都扩展一致性的权限、策略和控制。现有的身份提供商和安全工具可以扩展到这些AI工作流中，使团队能够灵活采用新的AI技术，而无需重建治理体系或替换可信的企业控制措施。

Unity AI Gateway还通过单查询API原生访问前沿模型，包括Anthropic、OpenAI、Gemini、Kimi、GLM等。这使得切换模型、保持与最新最优技术同步变得极为简单。

![](/images/posts/faf64527ff45.jpg)

## 开始使用Unity AI Gateway

Unity AI Gateway今日正式发布，为组织提供统一的AI治理方法，在AI采用规模扩大时平衡成本、控制和选择。

了解更多信息：

- 浏览我们在AWS、Azure和GCP上的文档
- 访问我们的网站
- 注册参加8月13日由Databricks联合创始人兼CTO Matei Zaharia和Databricks AI产品总监Kasey Uhlenhuth主持的AI治理网络研讨会

---

> 本文由AI自动翻译，原文链接：[Unity AI Gateway is Generally Available](https://www.databricks.com/blog/unity-ai-gateway-generally-available)
> 
> 翻译时间：2026-08-05 05:31
