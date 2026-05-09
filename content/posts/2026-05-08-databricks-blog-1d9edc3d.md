---
title: MCP市场为智能Agent注入实时决策能力
title_original: MCP Marketplace Brings Real-Time Intelligence to Agentic Applications
date: '2026-05-08'
source: Databricks Blog
source_url: https://www.databricks.com/blog/mcp-marketplace-brings-real-time-intelligence-agentic-applications
author: ''
summary: 文章指出，仅依赖内部数据的Agent应用无法实现真正的自主决策，因为缺乏实时市场、信用和房地产等外部智能。Databricks推出的MCP Marketplace通过连接You.com、Moody's和Cotality等可信数据源，使Agent能够查询实时信息并自主推理。结合Lakebase和Genie，企业可构建端到端工作流，在保持治理与合规的同时，消除人工研究瓶颈，加速决策。
categories:
- AI产品
tags:
- MCP
- Agentic应用
- 实时智能
- Databricks
- 企业AI
draft: false
translated_at: '2026-05-09T05:24:35.453803'
---

- Agentic应用需要实时智能——基于静态内部数据构建的Agent无法真正进行推理或大规模自主决策  
- MCP Marketplace填补了这一空白——You.com、Moody's和Cotality提供了可治理、实时的外部智能，Agent可以信任并调用  
- Lakebase + Genie支持端到端工作流——Agent能够记住上下文和状态，同时Genie以自然语言向业务用户呈现决策，供其审查和批准  

Agentic应用是一种AI系统，它了解你的业务上下文，能够自主推理，并基于实时数据和专业知识采取行动。Agent Bricks、Genie、Apps和Lakebase为企业提供了大规模构建Agentic应用的工具。但存在一个关键缺口：仅基于内部数据构建的Agent无法真正思考。

以贷款审批Agent为例。它可以访问你银行的贷款账簿、客户历史和信用评分。但它缺乏人类本能使用的上下文：  

- 当前市场状况和行业趋势  
- 实时信用度信号（更新的评级、展望变化）  
- 房产估值和权益变动  
- 竞争对手活动和经济逆风  

没有这些实时智能，Agent就会变得知识受限——受限于历史数据，无法理解当前世界的真实状况。它们可以执行工作流，但无法做出明智的决策。

旧的解决方案是什么？人工研究。分析师从多个来源提取数据，在工具之间切换时丢失上下文，造成瓶颈。决策速度变慢。风险增加。

Agent需要一种在推理复杂问题时访问实时、可信智能的方式。这就是MCP Marketplace的作用所在。

### 解决方案：Agentic应用的实时智能

Databricks Marketplace是一个面向数据、分析和AI的开放市场。它是发现、连接和管理MCP服务器及AI就绪数据的中心枢纽，使Agent能够以最小摩擦大规模访问外部数据。

![Databricks Marketplace](/images/posts/208479bfe401.png)

让我们通过三个特定领域的示例来说明Agentic应用如何利用实时智能解决具体问题。这三个提供商代表了你的Agent可能需要的不同类型的外部智能：  

- You.com——实时网络智能和市场情绪  
- Moody's——机构信用研究和实体智能  
- Cotality——面向贷款机构的房地产和抵押贷款专业知识  

这些不仅仅是数据源。它们是Agent可以查询、评估并据此采取行动的**可执行智能源**，所有操作都在一个可治理、可审计的环境中进行。每个连接都通过Unity Catalog进行身份验证，为访问控制和合规性创建单一事实来源。

通过将你的Agentic应用连接到这些MCP服务器，你正在做三件关键的事情：  

1. 弥合知识差距。Agentic应用可以访问训练集或数据仓库中未包含的实时数据。  
2. 消除人工研究。曾经需要人工干预的工作流现在可以自主运行。  
3. 保持治理。一切都在Lakehouse内进行，具有完整的血缘和合规性跟踪。  

## 工作原理：三个提供商的实践

为了说明Agentic应用如何利用实时智能，以下是这三个提供商如何在不同用例中驱动自主决策：

#### You.com：实时网络上下文和市场情绪

You.com MCP充当实时研究助手，可以在你的Agent内部调用，为内部绩效指标提供“为什么”的解释。  

- 差距：你的仪表板显示EMEA业务区域销售额下降10%。为什么？  
- Agent的行动：你的Agent调用You.com MCP检索实时市场新闻、天气模式、竞争对手定价和监管变化。你的Agent综合这些上下文。  
- Agent访问的内容：You.com允许Agent将实时新闻、监管变化和竞争对手定价直接拉入Databricks Genie对话中，提供即时、有依据的研究。  

此演示展示了主管Agent如何使用Genie进行内部数据仓库查询，以及使用You.com MCP服务器进行外部网络研究。

#### Moody's：大规模机构信用研究

Moody's MCP服务器提供可信、GenAI就绪的智能，可以嵌入金融应用以加速决策。通过调用Moody's精心策划的数据生态系统，包括全球实体所有权、财务报表以及Moody's Ratings信用评级和研究，结合你银行的私人贷款账簿，你可以从人工研究转向决策就绪的智能。  

- 差距：你的贷款官员仅根据信用评分批准申请人。他们错过了全貌。  
- Agent的行动：Moody's提供当前的Moody's Ratings信用评级、历史趋势、同行基准和行业展望。你的Agent现在可以将申请人与投资级同行进行比较，识别隐藏风险，并在几秒钟内向你的信贷官员呈现理由。  
- Agent访问的内容：业务用户可以进行高级实体搜索，访问自2000年以来的当前信用评级和展望历史，并检索前瞻性的行业轨迹以支持战略规划。  

![Moody's MCP服务器演示](/images/posts/01140e424c21.gif)  

点击此处查看Moody's MCP Server on Databricks的详细演示

#### Cotality：抵押贷款卓越的“Property 360”

Cotality MCP和AI就绪数据集为贷款机构提供了缺失的环节，使他们能够将房地产领域智能直接嵌入到他们的Agentic工作流中。  

- 差距：投资组合“流失”通常发生在暗处。如果没有跨数据源的清晰、统一视图来了解回笼表现，你就不知道你是在失去一个借款人，因为新购房还是可赢得的再融资，直到还款请求出现在你的办公桌上。  
- Agent的行动：Genie扫描你的投资组合以解析房产数据记录，并准确识别你的账簿流向何处。通过将内部数据与外部信号合并，它可以区分升级购房者和“再融资猎手”正在窃取你的权益，使你能够在最可能获胜的地方加强策略。  
- Agent访问的内容：Cotality的CLIP MCP驱动的房产解析，结合AI就绪数据集，提供了一个实时窗口，让你了解谁在获取你的账簿以及原因。贷款发起人可以看到还款是新购房还是再融资，实时跟踪竞争对手的挖角行为，并部署有针对性的外联，在流失开始之前阻止它。  

### Agent如何记忆：Lakebase作为状态引擎

实时智能解决了问题的一半。但Agentic应用还需要另一个能力：**持久记忆和状态**。

挑战在于：一个复杂的工作流——比如为期3天的商业贷款审查——涉及多个步骤、人工交接和决策。如果没有持久状态，Agent每次都会从头开始。上下文丢失。进度重置。

这就是Lakebase发挥作用的地方。Lakebase是一个专为Agentic应用构建的无服务器、有状态数据库。它存储Agent在多步骤工作流中的状态、决策和审计轨迹。

为什么这对实时智能很重要：当你的Agent在第一天访问Moody's数据，第二天访问Cotality数据时，Lakebase连接这些洞察并跨它们进行推理。Agent不会重新请求数据；它基于已知信息进行构建。每个决策都会自动记录以符合合规性要求。

## 整合起来：商业贷款决策支持应用

让我们看看一个生产级Agentic应用是如何工作的

1. 申请到达 → Lakebase 存储状态和元数据  
2. Agent（智能体）唤醒 → 从 Lakebase 检索上下文  
3. Agent（智能体）查询情报：  
   - Marketplace 上的 Moody's：当前信用评级、同行基准、风险信号  
   - Marketplace 上的 Cotality：房产估值、留置权状态、市场趋势  
   - Marketplace 上的 You.com：区域经济展望、行业动能  
4. Agent（智能体）综合 → 将内部数据（你的贷款账簿）与外部情报相结合  
5. Agent（智能体）呈现决策 → 通过 Genie 提出批准/拒绝建议并附完整推理  
6. 信贷官审核 → 在 yourDatabricks App 中一键批准  
7. Lakebase 记录决策 → 完整的审计追踪（决策、数据来源、时间戳、审批人）用于合规  

- Marketplace 上的 Moody's：当前信用评级、同行基准、风险信号  
- Marketplace 上的 Cotality：房产估值、留置权状态、市场趋势  
- Marketplace 上的 You.com：区域经济展望、行业动能  

全程治理：所有访问的数据、所有 Agent（智能体）推理、所有决策——均在 Unity Catalog 中追踪并保留完整血缘。  

![商业贷款决策工作流](/images/posts/b6e25630abad.png)  

### 立即开始：构建更智能的 Agent（智能体）  

MCP Marketplace 已上线。实时情报现已可供你的 Agent（智能体）使用：  

三家提供商已就绪：  

- You.com 提供市场情报  
- Moody's 提供信用与实体研究  
- Cotality 提供房地产专业知识  

三个后续步骤：  

1. 探索 Databricks Marketplace 查看所有可用的 MCP 服务器  
2. 使用 Agent Bricks 构建你的第一个 Agent（智能体），基于实时数据  
3. 通过 Lakebase 部署，实现记忆、治理和可审计性  

由实时情报驱动的 Agent（智能体）不仅执行工作流——它们还能推理、适应并做出自主决策，从而推动业务成果。  

### 在收件箱中获取最新文章  

订阅我们的博客，将最新文章直接发送到你的收件箱。

---

> 本文由AI自动翻译，原文链接：[MCP Marketplace Brings Real-Time Intelligence to Agentic Applications](https://www.databricks.com/blog/mcp-marketplace-brings-real-time-intelligence-agentic-applications)
> 
> 翻译时间：2026-05-09 05:24
