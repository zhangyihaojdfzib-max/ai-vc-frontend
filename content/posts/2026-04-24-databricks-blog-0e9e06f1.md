---
title: Databricks原生集成GPT-5.5与Codex，企业级AI治理
title_original: OpenAI GPT-5.5 + Codex, now available and fully-governed in Databricks
date: '2026-04-24'
source: Databricks Blog
source_url: https://www.databricks.com/blog/openai-gpt-55-now-available-databricks-fully-governed-through-unity-ai-gateway
author: ''
summary: Databricks宣布原生支持OpenAI GPT-5.5和Codex，通过Unity AI Gateway提供端到端治理，包括权限控制、成本管理、安全护栏和可观测性。企业可利用GPT-5.5构建智能Agent、通过Genie以自然语言分析数据，并自动化文档处理管道。该合作将前沿AI与企业数据深度结合，确保安全可控的部署。
categories:
- AI基础设施
tags:
- GPT-5.5
- Databricks
- 企业AI治理
- Codex
- Agent构建
draft: false
translated_at: '2026-04-25T04:38:28.231164'
---

- GPT-5.5 现已原生支持在 Databricks 上使用。请听我们的联合创始人 Patrick Wendell 与 OpenAI CRO Denise Dresser 讲述我们如何携手将前沿 AI 带入企业。
- 使用 GPT-5.5 驱动 Agent（智能体）构建，并利用 Genie 以自然语言从企业数据中提出业务问题。
- Unity AI Gateway 从第一天起便通过权限、成本控制、护栏和全面可观测性来管理 GPT-5.5 和 Codex。

GPT-5.5 是 OpenAI 针对企业级 Agent（智能体）工作、复杂文档推理以及长期编码 Agent（智能体）的最强前沿模型。Databricks 现已原生支持 GPT-5.5，因此客户可以将其应用于企业数据，并实现端到端治理。

使用 GPT-5.5 驱动 OpenAI Codex 或任何编码 Agent（智能体）中的编码工作流，构建基于企业数据的 Agent（智能体），为文档管道增添更深层次的智能，并将数据洞察融入每位员工的日常工作。Databricks 上所有 GPT-5.5 的使用均通过 Unity AI Gateway 进行管理，从第一天起便为客户提供跨 Agent（智能体）、查询和编码工作流的集中式安全、成本控制和可观测性。

## Databricks 与 OpenAI 如何合作

请听 Databricks 联合创始人兼工程副总裁 Patrick Wendell 与 OpenAI CRO Denise Dresser 讲述 OpenAI 与 Databricks 的合作如何为企业客户创造独特价值：

## Unity AI Gateway：GPT-5.5 和 Codex 的统一治理层

当企业通过 Databricks 使用 GPT-5.5 时，Unity AI Gateway 通过单一控制平面管理 GPT-5.5 模型推理和 Codex 编码工作流。在此处阅读更多关于 Unity AI Gateway 如何管理 Agent（智能体）编码的信息。

Unity AI Gateway 为 GPT-5.5 增加了企业级控制：

1. 权限和速率限制：按用户和组控制访问权限。防止成本失控。
2. 护栏：检测 PII（个人身份信息），阻止提示词注入，强制执行内容安全——每个端点均可配置。
3. MCP 治理：审计每个 Agent（智能体）工具调用，实现完全可追溯性。
4. 自动故障转移：若达到速率限制，流量将路由至备用模型。
5. 可观测性：每个请求，无论是模型调用还是 Codex 交互，都会在您拥有的 Delta 表中记录身份、Token、延迟和成本。
6. 统一账单：一份整合了 GPT-5.5、Codex 以及所有其他模型/编码工具的账单。

![GPT-5.5 在 Databricks Unity AI Gateway 上实现端到端治理](/images/posts/09e139bb2bf6.png)

![Codex 在 Databricks Unity AI Gateway 上实现端到端治理](/images/posts/4bc4035f78d2.png)

## 在 Databricks 上利用完整的企业上下文让 GPT-5.5 发挥作用

使用 Genie 以自然语言提出业务问题

Genie 是 Databricks 的自然语言分析体验，由来自 OpenAI 及其他模型提供商的多个前沿 LLM（大语言模型）驱动。业务用户可以用通俗英语安全地与复杂的企业数据进行交互，以探索数据、回答临时问题，并自动化此前需要数小时或数天的知识工作。Genie 对企业数据本体和业务语义的深刻理解，加上 GPT-5.5 等前沿模型不断提升的智能，使得日常业务用户能够将强大的数据洞察融入日常工作。

使用 Agent Bricks 构建自定义 Agent（智能体）

凭借 GPT-5.5 更强的执行和推理能力，Agent Bricks 自定义 Agent（智能体）现在可以处理更复杂的多步骤工作流，从文档分析管道到自动化部门业务流程。开发者可以使用他们偏好的工具和框架构建由 GPT-5.5 驱动的 Agent（智能体），然后将其部署为完全托管、无服务器的 Databricks 应用。

自动化文档智能管道

将 GPT-5.5 链接到 Lakeflow Spark 声明式管道中，用于 GenAI ETL（生成式 AI 提取、转换、加载），以摄取文档，应用摘要、提取或分类等 AI 转换，并通过内置的治理和可观测性编排流程。GPT-5.5 改进的文档解析和基于事实的推理使这些管道更加可靠，尤其适用于扫描的 PDF、表格和多格式数据等复杂的现实工件。

## 立即开始

GPT-5.5 现已在 Databricks 上于 AWS、Azure 和 GCP 环境中可用。以下是开始使用的方法：

- 在 AI Playground 中试用 GPT-5.5：将 GPT-5.5 与其他模型并排比较。调整参数并直接将提示词导出到笔记本或 SQL 中。
- 通过 Unity AI Gateway 部署 Codex：在几秒钟内设置一个受管理的 Codex 端点，具备内置安全、成本限制和可观测性。
- 使用 Agent Bricks 构建由 GPT-5.5 驱动的 Agent（智能体）：分析您的数据，自动化复杂工作，使用自定义评估器进行评估，并大规模部署。
- 阅读基础模型 API 文档：GPT-5.5 的完整 API 参考，包括对 Responses API 的支持。

---

> 本文由AI自动翻译，原文链接：[OpenAI GPT-5.5 + Codex, now available and fully-governed in Databricks](https://www.databricks.com/blog/openai-gpt-55-now-available-databricks-fully-governed-through-unity-ai-gateway)
> 
> 翻译时间：2026-04-25 04:38
