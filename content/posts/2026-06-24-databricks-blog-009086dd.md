---
title: Databricks连续两年领跑Gartner魔力象限
title_original: Databricks positioned highest in execution and furthest in vision
  for the second consecutive year in Gartner Magic Quadrant
date: '2026-06-24'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-positioned-highest-execution-and-furthest-vision-second-consecutive-year-gartner
author: ''
summary: Gartner将Databricks评为2026年数据科学与机器学习AI平台魔力象限的领导者，在执行能力和愿景完整性上均居首位。文章指出，市场正从模型构建转向基于企业数据的Agent应用部署，Databricks通过统一数据、AI和治理的平台（如Unity
  Catalog和Unity AI Gateway）支持这一转变。其核心创新包括基于企业数据推理的Agent AI、开放灵活的设计以及跨数据、模型和应用的统一治理，强调没有数据策略就没有AI策略。
categories:
- AI产品
tags:
- Databricks
- Gartner魔力象限
- AI平台
- Agent应用
- 数据治理
draft: false
translated_at: '2026-06-25T06:08:20.918396'
---

- Gartner 将 Databricks 评为 2026 年数据科学与机器学习 AI 平台魔力象限的领导者，在执行能力方面排名最高，在愿景完整性方面最为超前。
- 我们认为从“DSML”到“AI Platforms for DSML”的转变反映了一个根本性的市场变化：企业正在从模型构建转向部署能够基于其数据进行推理的 Agent 应用，这些数据必须作为一级生产系统进行治理。
- 在单一平台上统一数据、AI 和治理，使企业能够将 Agent 应用从概念转化为生产，并具备规模化所需的信任、安全、可观测性和策略执行能力，这一切由 Unity Catalog 和 Unity AI Gateway 提供支持。

企业正在快速大规模部署 Agent 应用，从自动化日常任务的后台微应用，到跨行业和部门提升客户体验的 Agent。但脱离企业数据且缺乏集中治理控制的通用基础模型，无法提供这些 Agent 和应用所需的准确性、合规性或业务上下文。同样关键的是，它们会引入风险：不受控制的模型和数据访问、不一致的策略、缺乏可观测性以及碎片化的审计追踪。

我们认为 Gartner 决定将此类别从“数据科学与机器学习”重新分类为“面向数据科学与机器学习的 AI 平台”，证实了我们长期以来的观点：AI 不再是一个边缘实验——它是现代企业的运营模式，根植于业务上下文。

![image1.png](/images/posts/79ee9a3f89f2.png)

在此处免费下载报告副本

## 战略：在统一平台上构建、编排和治理 Agent 应用

我们认为我们在该类别中被评为领导者源于一个核心理念：没有数据策略就没有 AI 策略——没有治理策略，两者都无法规模化。当许多供应商将数据、模型、Agent 和治理的独立产品拼凑在一起时，Databricks 提供了一个统一的平台。

这意味着您的一份数据、一个跨数据和 AI 的治理层，以及一种在生产中构建、监控和控制 Agent 的一致方式。通过统一湖仓一体、Lakebase、Agent Bricks 和 Unity Catalog，我们为从开发者到业务用户的每个团队提供了一个单一场所，将企业数据转化为可信、合规、生产级的 Agent 和应用。借助 Unity AI Gateway，组织可以获得集中的策略执行、模型访问控制、使用追踪、成本管理以及跨每个请求和响应的实时护栏。

## Agent 时代的核心创新

### 1. 基于您的数据进行推理的 Agent AI

Agent 的有用程度取决于它们能够推理的数据和上下文。借助 Agent Bricks，团队可以构建生产就绪的自定义 Agent，这些 Agent 会自动针对成本和质量进行优化，以 Databricks 湖仓一体中受治理的企业数据为基础，并由 Lakebase（我们用于 Agent 状态和应用的无服务器、兼容 Postgres 的操作性存储）提供支持。Agent 能够检索正确的信息，一致地解释业务语义，并以企业所需的准确性和可靠性执行操作。YipitData 使用这种方法扩展了非结构化数据智能，实现了公司覆盖范围 20 倍的增长以及开箱即用的 92-95% 的标签准确率。

业务用户可以通过 Databricks Genie One 和 Genie Agents 获得可信的洞察并执行 Agent 操作，这些功能由提供业务上下文的 Genie Ontology 提供支持，并基于您的数据。easyJet 正利用这种灵活性，在 Lakebase、Agent Bricks 和 Apps 之上重新构想航空零售。

### 2. 开放且灵活的设计

构建者需要自由地快速行动，而不会被锁定。Databricks 原生支持所有前沿模型（OpenAI、Anthropic、Google）和领先的开源模型（Meta、Qwen、DeepSeek 等），因此团队可以交换模型而无需重新谈判合同或重写应用。开发者可以使用他们偏好的 AI 编码 Agent（如 Cursor 或 Replit）以及新的元框架 Omnigent 进行 Vibe 编码。他们可以连接到受治理的 Lakebase，并通过 Databricks Apps 在数天内交付 Agent 应用。

### 3. 跨数据、模型、Agent 和应用的统一治理

没有治理的创新无法规模化。Unity Catalog 和 Unity AI Gateway 在 Databricks 上托管及外部的每个数据资产、模型、Agent、MCP 服务器、应用和工具之间，提供端到端的治理——所有这些都在一个单一记录系统中。端到端的权限确保没有任何东西可以访问超出其允许范围的内容，无论是前沿模型还是嵌入在面向客户应用中的自主 Agent。Block 使用 Unity Catalog 统一其跨业务单元的 AI 和数据资产，而 Novo Nordisk 已将 1.57 亿美元以上的净新增价值归因于受治理的、AI 驱动的临床试验优化。

## 未来展望

我们相信这一认可验证了我们在各个行业观察到的现象：统一、受治理的数据与 AI 平台与拖慢第一波企业 AI 发展的碎片化技术栈之间的差距正在扩大。随着 Agent 应用从实验转向业务关键型，它们需要统一的数据、AI 和治理。我们邀请您加入我们的旅程，共同继续改变世界构建、治理和扩展智能的方式。

[阅读完整的 2026 Gartner® 数据科学与 AI 平台魔力象限™ 报告]

Gartner，AI 平台数据科学与机器学习平台魔力象限，Yogesh Bhatt、Afraz Jaffri、Diarmuid Curran，2026 年 6 月 22 日。

GARTNER 是 Gartner, Inc. 和/或其关联公司在美国和国际上的注册商标和服务标志，MAGIC QUADRANT 是 Gartner, Inc. 和/或其关联公司的注册商标，经许可在此使用。保留所有权利。

Gartner 不认可其研究出版物中描述的任何供应商、产品或服务，也不建议技术用户仅选择那些具有最高评级或其他称号的供应商。Gartner 研究出版物包含 Gartner 研究机构的意见，不应被解释为事实陈述。Gartner 对本研究不作任何明示或暗示的保证，包括任何适销性或特定用途适用性的保证。

此图形由 Gartner, Inc. 作为更大研究文档的一部分发布，应结合整个文档进行评估。Gartner 文档可应要求从 Databricks 获取。

---

> 本文由AI自动翻译，原文链接：[Databricks positioned highest in execution and furthest in vision for the second consecutive year in Gartner Magic Quadrant](https://www.databricks.com/blog/databricks-positioned-highest-execution-and-furthest-vision-second-consecutive-year-gartner)
> 
> 翻译时间：2026-06-25 06:08
