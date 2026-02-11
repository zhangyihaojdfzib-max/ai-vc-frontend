---
title: Agent Bricks Supervisor Agent正式发布：统一编排企业级智能体
title_original: 'Agent Bricks Supervisor Agent is Now GA: Orchestrate Enterprise Agents'
date: '2026-02-10'
source: Databricks Blog
source_url: https://www.databricks.com/blog/agent-bricks-supervisor-agent-now-ga-orchestrate-enterprise-agents
author: ''
summary: 随着企业智能体（Agent）数量的激增，管理分散、查找困难等问题日益凸显。Agent Bricks Supervisor Agent现已正式发布，它作为一个受Unity
  Catalog全面管控的托管编排层，旨在解决这一挑战。该智能体采用动态监督者模式，能够理解用户意图，在结构化数据、非结构化数据及各类工具间进行智能协调，为用户提供统一入口。其核心优势在于通过Unity
  Catalog实现原生安全治理，确保所有操作均符合用户权限；同时内置基于人类反馈的学习机制，支持Agent的持续评估与改进，助力企业构建安全、可控且不断进化的智能体生态系统。
categories:
- AI产品
tags:
- 智能体编排
- 企业AI
- AI治理
- Unity Catalog
- Agent Bricks
draft: false
translated_at: '2026-02-11T04:35:14.759248'
---

企业正在快速推进Agent（智能体）开发，用于财务分析助手、客服助理和内部知识检索。但这种快速增长带来了新的挑战：如何查找和管理所有这些Agent。团队不得不玩起“Agent轮盘赌”，在数十个细分机器人之间切换，试图记住“差旅政策”究竟存放在HR Agent还是财务Agent中。这种认知负担正在拖慢工作效率，导致团队漫无目的地搜索、重复创建已存在的Agent，或引用过时信息。企业需要一个统一的入口点，能够理解用户意图、协调专业Agent，并安全地代表用户执行操作。

Agent Bricks Supervisor Agent现已正式发布（GA），它是一个受Unity Catalog全面管控的托管编排层，可让您将Agent与工具整合起来。它采用动态监督者模式来分析用户问题，并在结构化数据的Genie Spaces、非结构化数据的Knowledge Assistant Agent以及工具类MCP服务器之间进行编排，以回答复杂问题并提供深度分析。这使得团队能够独立拥有并迭代优化其Agent的质量，同时为用户提供完成工作的统一入口。

![Agent Bricks Supervisor Agent](/images/posts/28935bfb8244.gif)

## 设计即治理：由Unity Catalog保障安全

对于IT和安全团队而言，Agent式AI往往在企业安全体系外运行。大多数工具需要复制权限或使用宽泛的服务账户，这造成了合规缺口——Agent可能访问最终用户无权查看的数据。

Agent Bricks将Unity Catalog作为Agent及其模型、数据和工具的控制与治理层。Supervisor Agent原生支持**代理身份（OBO）认证**，充当人类用户的透明代理。每次数据获取或工具执行都会根据用户在Unity Catalog中的现有权限进行验证：无论是查询表的权限，还是通过MCP Catalog访问特定工具的权限。这确保了Agent始终符合您的治理策略，无需额外工作。

对于富兰克林邓普顿而言，扩展AI意味着在合规前提下利用受监管的基金文档。通过使用内置Unity Catalog治理功能的Agent Bricks，该团队将公开基金文档与业绩数据结合，构建了一个基于企业认可数据源的受监管基金分析Agent。

## 通过研究支持的学习实现持续改进

生产级Agent永远不会“完成”；它必须根据实际表现不断演进。您需要评估其响应、整合新信息并持续改进，以保持Agent的实用性。

Supervisor Agent内置了由**人类反馈的Agent学习（ALHF）** 驱动的质量闭环。您可以添加问题和指导原则，Supervisor能据此改进答案质量、优化子Agent间的路由策略，并为系统提供上下文。这也使得与领域专家（SME）的协作更加容易：例如，您的营销团队可以提供关于Agent响应的品牌与风格指南，Supervisor能直接从中学习。通过内置的MLflow实验与集成，每次交互都可追踪和量化，让您快速发现并弥补不足。

像Zapier这样的客户已利用人类反馈的Agent学习来快速迭代改进其Agent。Zapier正使用Supervisor Agent实现数据访问民主化，并借助ALHF提升Supervisor在不同Genie空间和工具间的编排能力。

## 立即使用Supervisor Agent

随着正式发布，Supervisor Agent为企业级AI Agent编排提供了托管基础。团队现在可以通过统一控制平面实现意图路由、通过Unity Catalog治理访问权限，并持续提升Agent质量。

立即开始使用Supervisor Agent，创建您的第一个Agent并将其连接到现有Agent和工具。查阅文档了解Supervisor Agent如何融入您的生产工作流。

立即构建您的第一个Supervisor Agent →

---

> 本文由AI自动翻译，原文链接：[Agent Bricks Supervisor Agent is Now GA: Orchestrate Enterprise Agents](https://www.databricks.com/blog/agent-bricks-supervisor-agent-now-ga-orchestrate-enterprise-agents)
> 
> 翻译时间：2026-02-11 04:35
