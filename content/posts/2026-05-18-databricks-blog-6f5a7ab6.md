---
title: Databricks推出分析工程师学习路径
title_original: Announcing the Databricks analytics engineer learning pathway
date: '2026-05-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-databricks-analytics-engineer-learning-pathway
author: ''
summary: Databricks宣布推出全新的分析工程师学习路径，专为SQL从业者设计，旨在帮助他们将原始数据转化为受管控、AI就绪的语义模型和指标视图。该路径涵盖数据建模、声明式SQL管道、语义层构建及对话式Agent等核心技能，包含六门实践课程，支持自定进度和讲师指导两种学习形式。课程现已上线Databricks
  Academy，有效订阅用户可免费学习。
categories:
- AI产品
tags:
- Databricks
- 分析工程
- SQL
- 数据建模
- AI Agent
draft: false
translated_at: '2026-05-19T06:14:42.451855'
---

- 可靠的分析和AI依赖于构建良好的数据基础，而SQL从业者正是构建为其提供支持的管道、模型和指标的人。
- 一条为SQL从业者设计的新学习路径，涵盖在Databricks上使用完整SQL ETL工具包的技能——数据建模、用于轻量级转换或受管控端到端工作流的声明式SQL管道、一致的语义层以及对话式Agent（智能体）。
- 课程现已在Databricks Academy上线，提供自定进度和讲师指导两种形式，因此您可以立即开始学习。任何有效的Databricks学习订阅也包含该课程。

今天，我们推出全新的Databricks分析工程师学习路径。该课程教您如何将原始数据转换为受管控、AI就绪的语义模型和指标视图，这是为湖仓一体上的分析、仪表板和AI Agent（智能体）提供支持的可靠基础。该路径专为准备对其团队所依赖的数据承担更多责任的SQL从业者设计。

![学习路径 分析工程师](/images/posts/70e532f44846.png)

## 为什么分析工程正变得至关重要

SQL一直是现代分析的基石。但在此基础上构建的工作正在扩展——进入建模、管道、指标以及现在Agent（智能体）和仪表板所依赖的数据层。

可靠的分析和AI运行在同一个基础上：受管控、经过建模且可信的数据。构建这一基础比过去更加困难。数据分布在更多来源中，并服务于更多下游消费者。传统上负责准备数据的数据团队已不堪重负。根据《经济学人》企业近期的一份报告，近三分之二的组织完全依赖数据工程师处理管道创建的每个方面，而这些工程师中几乎有一半将大部分时间花在配置和修复数据源连接上。吸收新工作的能力有限。越来越多地，这项工作落到了最接近业务的从业者身上：那些使用SQL的人。

SQL从业者更接近业务，了解所提出的问题、底层数据以及团队关心的指标。分析工程正是利用这种背景来构建业务可以依赖的模型、管道和指标的学科。这项工作的工具现在已是SQL原生。如何善用这些工具的判断力正是本路径所教授的。

## 路径内容

分析工程师路径包含实践课程，涵盖Databricks上完整的SQL ETL工具包。从分析基础开始，了解分析如何在湖仓一体上运作。之后，课程其余部分将深入探讨分析工程技能集的每个部分，由Databricks专家授课，并围绕实践示例构建。

1. **分析基础**：了解分析如何在Databricks上运作：统一语义、AI/BI仪表板和Genie。一小时的入门课程。

2. **数据建模策略**：学习如何设计在湖仓一体上生产环境中经得起考验的数据模型。
   - 将数据组织和模型设计与业务需求对齐
   - 使用Delta Lake和Unity Catalog定义数据架构
   - 了解湖仓一体上的数据产品生命周期
   - 应用数据集成和共享技术

3. **使用SQL构建ETL管道**：学习如何使用物化视图、流式表和Lakeflow作业构建生产级SQL ETL管道。
   - 利用流式表、物化视图和AUTO CDC构建声明式管道
   - 在Medallion架构中实现增量摄取和转换
   - 使用AUTO CDC处理SCD类型1和类型2
   - 使用Lakeflow作业和基于SQL的工作流编排管道

4. **使用UC指标视图构建语义模型**：学习如何在SQL中定义和管理业务指标，然后在所有消费位置呈现可信的数字。
   - 在Unity Catalog中定义和管理指标视图
   - 对高级指标进行建模，包括窗口和半加性度量
   - 与Databricks仪表板、Genie空间和SQL工作流集成
   - 应用治理、安全和维护实践

5. **使用Genie构建可靠的对话式Agent（智能体）**：学习如何设计、发布并持续改进业务用户可信赖的Genie空间。
   - 使用Unity Catalog表、SQL仓库和基准配置Genie空间
   - 使用同义词、描述和提示词匹配功能策划知识库
   - 使用派生表达式、连接和指令在SQL中编码业务逻辑
   - 使用Unity Catalog权限和ABAC策略管理访问
   - 使用基准、用户反馈和观察到的输出进行迭代

6. **使用Lakeflow Spark声明式管道构建管道**：学习如何使用Spark声明式管道编辑器构建受管控的端到端SQL管道。
   - 理解流式表、物化视图和临时视图
   - 使用内置期望强制数据质量
   - 使用AUTO CDC INTO处理缓慢变化维度
   - 通过事件日志和指标分析管道执行

每门课程均提供自定进度和讲师指导两种形式。完整路径也包含在任何有效的Databricks学习订阅中。

## 立即开始您的旅程

分析工程师学习路径现已在Databricks Academy上线。完成课程后，您将能够对原始数据进行建模、发布管道，并定义为仪表板和AI提供支持的指标。

如果您领导一个团队，该路径也是让您的团队交付业务用户赖以决策的洞察的最快方式。

立即从分析基础开始探索，并访问Databricks Academy继续在路径其余部分提升您的技能。

---

> 本文由AI自动翻译，原文链接：[Announcing the Databricks analytics engineer learning pathway](https://www.databricks.com/blog/announcing-databricks-analytics-engineer-learning-pathway)
> 
> 翻译时间：2026-05-19 06:14
