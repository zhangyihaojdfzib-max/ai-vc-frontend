---
title: 实践中的智能体推理：融合结构化与非结构化数据
title_original: 'Agentic Reasoning in Practice: Making Sense of Structured and Unstructured
  Data'
date: '2026-04-14'
source: Databricks Blog
source_url: https://www.databricks.com/blog/agentic-reasoning-practice-making-sense-structured-and-unstructured-data
author: ''
summary: 本文介绍了Databricks的Agent Bricks Supervisor Agent（SA）如何通过多步骤推理，有效整合结构化和非结构化数据源，以解决复杂的现实业务问题。文章展示了SA在STaRK和KARLBench等基准测试中，相比现有最佳基线实现了20%以上的性能提升，尤其在学术检索、生物医学推理和财务分析等任务上表现突出。SA基于灵活的aroll框架构建，可通过配置调整持续优化，无需编写代码，适用于大规模并发场景。
categories:
- AI产品
tags:
- 智能体推理
- 多模态数据
- Databricks
- 基准测试
- 企业AI
draft: false
translated_at: '2026-04-15T04:50:09.394653'
---

![Databricks "Agentic Reasoning" 图表，柱状图显示 Agent Bricks Supervisor Agent 在 STaRK 和 KARLBench 基准测试中均优于 SoTA 基线。](/images/posts/019c01a47660.png)

企业数据很少在孤岛中有用。回答诸如“我们哪些产品在过去三个月中销售额下降，以及各个卖家网站上的客户评论中提到了哪些潜在相关问题？”这类问题，需要对结构化和非结构化数据源（包括数据湖、评论数据和产品信息管理系统）进行混合推理。在本博客中，我们将演示 Databricks Agent Bricks Supervisor Agent（SA）如何通过基于结构化和非结构化数据混合的多步骤推理，来帮助处理这些复杂的现实任务。

![图 1：SoTA 基线与 Agent Bricks SA 在 STaRK 和 KARLBench 基准测试上的质量对比。对于 STaRK，我们报告所有 STaRK 数据集（Amazon、MAG、Prime）的平均 Hit@1 作为质量分数。对于 KARLBench，我们报告六个数据集的归一化指标平均值（详见下文）。](/images/posts/942c477ea800.png)

通过调整指令和仔细的工具配置，我们发现 SA 在广泛的知识密集型企业任务上表现出色。图 1 显示，SA 在以下方面相比 SoTA 基线实现了 20% 或更多的提升：

- STaRK：斯坦福研究人员发布的一套包含三个半结构化检索任务的基准。
- KARLBench：Databricks 最近发布的用于复杂基础推理的基准套件。

Supervisor Agent 在广泛的经济价值任务上展现出显著增益：从学术检索（STaRK-MAG 上 +21%）到生物医学推理（STaRK Prime 上 +38%）以及财务分析（FinanceBench 上 +23%）。

## Agent 设置

Agent Bricks Supervisor Agent 是一个声明式的 Agent 构建器，用于编排 Agent 和工具。它构建在 `aroll` 之上——这是一个用于大规模构建、评估和部署多步骤 LLM 工作流程的内部 Agent 框架。`aroll` 和 SA 是专门为我们客户经常遇到的高级 Agent 用例而设计的。

`aroll` 能够通过简单的配置更改添加新工具和自定义指令，可以处理数千个并发对话和并行工具执行，并集成了先进的 Agent 编排和上下文管理技术来优化查询并从部分答案中恢复。所有这些在当今的 SoTA 单轮系统中都难以实现。

由于 SA 构建在这种灵活的架构之上，其质量可以通过简单的用户管理（例如调整顶层指令或优化 Agent 描述）来持续改进，而无需编写任何自定义代码。

![图 2：为 STaRK MAG 数据集设置 Databricks Supervisor Agent。](/images/posts/7e769b76e698.png)

图 2 展示了我们如何为 STaRK-MAG 数据集配置 Supervisor Agent。在本博客中，我们使用 Genie 空间来存储关系知识库，并使用 Knowledge Assistant 来存储用于检索的非结构化文档。我们为所有 Knowledge Assistant 和 Genie 空间提供了详细描述，以及 Agent 响应的指令。

## 混合推理：结构化与非结构化相遇

为了评估基于结构化和非结构化数据混合的基础推理，我们使用 STaRK 基准，它包含三个领域：

- Amazon：产品属性（结构化）和评论（非结构化）
- MAG：引文网络（结构化）和学术论文（非结构化）
- Prime：生物医学实体（结构化）和文献（非结构化）

例如，“找一篇由拥有 115 篇论文的合著者撰写且关于里德堡原子的论文”要求系统将结构化过滤（“拥有 115 篇论文的合著者”）与非结构化理解（“关于里德堡原子”）结合起来。**已发表的最佳基线**使用基于 LLM 的重新排序器进行向量相似性搜索——这是一种强大的单轮方法，但无法跨数据类型分解查询。为了确保公平比较，我们使用当前的 SoTA 基础模型重新运行了此基线，提供了一个显著更强的基线。

![图 3：STaRK 结果——各自数据集中人工生成的部分。我们报告了 (a) 论文中报告的最佳基线 (b) 使用当前 SoTA 基础模型重新实现的基线 (c) Agent Bricks SA 的 Hit@1。](/images/posts/d810f550d16a.png)

通过我们的方法，SA 分解每个问题，将子问题路由到适当的工具，并在多个推理步骤中综合结果。如图 3 所示，与原始最佳基线以及我们使用当前 SoTA 基础模型重新运行的基线相比，SA 在 Amazon 上实现了 +4% 的 Hit@1，在 MAG 上 +21%，在 Prime 上 +38%。我们在 MAG 和 Prime 上看到了最大的改进，这些任务的答案需要结构化和非结构化数据最紧密的集成。

使用我们上面的示例问题（“找一篇由拥有 115 篇论文的合著者撰写且关于里德堡原子的论文”），我们发现基线失败了，因为嵌入无法编码结构约束（“合著者恰好有 115 篇论文”）。在图 4 中，我们展示了 SA 的执行轨迹：它首先使用 Genie 查找所有 759 位拥有 115 篇论文的作者，并使用 Knowledge Assistant 检索里德堡相关论文，然后交叉引用这两个集合。当未发现重叠时，SA 进行调整：它对 115 篇论文的作者列表与所有标题或摘要中提到“Rydberg”的论文执行 SQL JOIN 操作，直接从结构化数据中找出答案。然后它调用 Knowledge Assistant 验证相关性，调用 Genie 确认作者的论文数量，并成功返回**正确的论文**。

## 在知识密集型任务上的 Agent 优势

![图 5：KARLBench 结果——一套包含六个具有挑战性的基础推理任务的基准。注意：每个任务使用其自己的指标（TREC-Biogen/QAMPARI/PMBench/FreshStack 使用 Nugget Completeness，BrowseComp+ 使用二元准确率，FinanceBench 使用 Answer Correctness），并且为了便于展示，它们都被归一化到 0-100 的尺度。](/images/posts/4ad3f066dab6.png)

为了将 Agent Bricks SA 与一个强大的单轮基线（类似于 STaRK 的最佳已发表基线，无需结构化数据）的性能进行比较，我们使用 **KARLBench** 对它们进行评估。KARLBench 是一个基础推理基准套件，共同对不同的检索和推理能力进行压力测试：

- BrowseComp+：排除法实体搜索
- TREC BioGen：生物医学文献综合
- FinanceBench：财务文件上的数值推理
- QAMPARI：详尽实体召回
- FreshStack：基于文档的技术故障排除
- PMBench：Databricks 内部企业文档理解

总体而言，Supervisor Agent 在所有六个基准测试中都取得了一致的增益，在需要详尽分析或自我纠正的任务上改进最大。在 FinanceBench 上，它通过检测差距和重新制定查询，从最初不完整的检索中恢复，实现了整体 +23% 的改进。

例如，BrowseComp+ 的每个问题都有 5-10 个相互关联的约束，例如“找一位在 2015-2020 年间离开俄罗斯俱乐部、在 2010-2016 年间归化欧洲、身高 1.95-2.06 米的球员。他们在因 COVID 推迟的奥运会上拦网成功率是多少？”单轮基线发出一个宽泛的查询，正确识别了球员，但未能检索到详细的统计数据文档，因此未能回答问题。

![图 6：Supervisor Agent 处理 BrowseComp+ 问题的详细执行轨迹。](/images/posts/9e9b5d061fcb.png)

SA 将此任务分解为一个协调的搜索计划，并将计划分解为可搜索的子集。这避免了单轮基线的失败情况，即统计数据因在后续搜索中才被检索到而未被找到。因此，SA 实现了 +78% 的相对改进。

在PMBench的另一个示例中，有一个问题是“客户正在使用哪些护栏类型”，要给出详尽的答案，需要从10多份客户对话文档中提取26个信息片段（定义参见KARL报告）。单轮基线方法仅找到一个客户提及，因为它无法在单个问题中搜索所有护栏类别。而SA（监督智能体）会分别搜索每个护栏类别（“PII检测”、“幻觉”、“毒性”、“提示词注入”），并在此过程中逐步发现越来越多的客户提及。

## 我们的发现

我们各项实验的结果指向了几个关键要点：

1.  如果能够使用正确的工具和数据表示，基于事实进行推理的智能体可以从结构化和非结构化数据检索的混合方法中受益。
2.  对于高质量检索场景，应避免在异构数据集上构建自定义的RAG（检索增强生成）流程，即使在重排序阶段使用了最先进的模型。多步推理——在每一步中，智能体选择正确的数据源并反思其效用——对于提升性能至关重要。
3.  一种声明式的智能体构建方法，例如Databricks Supervisor Agent所实现的方法，在易用性和质量之间提供了良好的平衡。

我们使用Databricks Supervisor Agent为KARLBench中的所有三个STaRK领域和六个非结构化数据集构建了智能体。这九项任务中唯一不同的是指令和工具——处理这些多样化数据集无需编写自定义代码。因此，为一项新的企业任务构建一个高性能的智能体，很大程度上在于编写精确的指令并为其配备正确的工具，而不是从头开始构建一个新系统。

Agent Bricks Supervisor Agent现已面向我们所有客户开放。您只需创建一个智能体，并将其连接到您现有的智能体、工具和MCP服务器，即可开始使用Agent Bricks SA。请查阅文档，了解Supervisor Agent如何融入您的生产工作流程。

作者：Xinglin Zhao, Arnav Singhvi, Mark Rizkallah, Jonathan Li, Jacob Portes, Elise Gonzales, Sabhya Chhabria, Kevin Wang, Yu Gong, Moonsoo Lee, Michael Bendersky 和 Matei Zaharia。

1欲了解更多关于如何将roll用于合成数据生成、可扩展的RL（强化学习）训练以及智能体任务的在线推理的详细信息，请参阅我们最近的出版物“KARL: Knowledge Agents via Reinforcement Learning”。

## 为您推荐

---

> 本文由AI自动翻译，原文链接：[Agentic Reasoning in Practice: Making Sense of Structured and Unstructured Data](https://www.databricks.com/blog/agentic-reasoning-practice-making-sense-structured-and-unstructured-data)
> 
> 翻译时间：2026-04-15 04:50
