---
title: 7-Eleven如何借助Databricks Agent Bricks革新维修技师知识获取
title_original: How 7‑Eleven Transformed Maintenance Technician Knowledge Access with
  Databricks Agent Bricks
date: '2026-01-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-7-eleven-transformed-maintenance-technician-knowledge-access-databricks-agent-bricks
author: ''
summary: 本文介绍了全球连锁便利店7-Eleven如何利用Databricks的Agent Bricks技术平台，彻底改变其维护技师获取设备维修知识和操作指南的方式。通过构建一个统一、智能的知识访问系统，7-Eleven将分散在不同文档、系统和经验中的维修知识整合到湖仓一体平台中，使技术人员能够通过自然语言快速、准确地查询解决方案，从而大幅提升设备维护效率、减少停机时间，并赋能一线员工。这体现了企业利用现代数据与AI平台解决具体业务痛点、推动运营数字化转型的典型案例。
categories:
- AI产品
tags:
- 企业数字化转型
- 知识管理
- 智能运维
- Databricks
- 零售科技
draft: false
translated_at: '2026-01-10T04:15:34.640062'
---

# 7‑Eleven 如何利用 Databricks Agent Bricks 变革维护技术员的知识获取方式

## 了解 7‑Eleven 如何构建一个由 AI 驱动的技术员维护助手，该助手能在 Microsoft Teams 内直接提供来自维护手册、图表和图像的快速、准确答案。

发布日期：2026年1月9日

作者：Sai Sandeep Kantareddy

- Databricks Agent Bricks 统一了向量索引和可观测性，将延迟降低了 40% 以上，并取代了复杂的多服务 AWS 实现。

## 赋能每家门店的技术员

7‑Eleven 的维护技术员通过维护各种设备（从食品服务设备和制冷机组到加油机和思乐冰机器）来确保门店顺利运营。每次维修都依赖于技术员的知识和对支持文档（如服务手册、接线图和带注释的图像）的即时访问。

## 为技术员创建统一且更快的设备信息查找方式

随着时间的推移，设备文档已演变为包含多种格式，并分散在不同位置。这使得技术员更难快速找到所需信息。此外，当遇到不熟悉的设备、部件等时，技术员通常依赖聊天或电子邮件向同行寻求支持。

因此，我们发现了简化信息访问、共享等方式的机会；最终能为门店运营提供更一致的支持。

## 构建技术员维护助手

为了应对这些挑战，7‑Eleven 设想了一个能够实现以下功能的 AI 驱动助手：

- 从图像中识别设备部件并建议相关材料。
- 与 Microsoft Teams 无缝集成。

通过与 Databricks 合作，7-Eleven 开发了技术员维护助手，这是一个集成了文档检索、视觉模型和协作的智能解决方案，形成了简化的工作流程。

## 文档存储与索引

所有相关的维护文档都上传到 Unity Catalog Volume，它管理跨云存储的非表格数据（如文本和图像）的权限。

开发团队使用 Databricks Vector Search，实现了带嵌入计算的 Delta Sync。他们使用 BAAI bge-large-en-v1.5 模型生成向量嵌入，并通过 Vector Search 端点提供服务，以实现高速、低延迟的检索。

![Document Storage and Indexing](/images/posts/841c49dc7f8d.png)

## Microsoft Teams 集成

技术员通过 Microsoft Teams 直接访问 TMA。Teams Bot 通过一个 API 层路由每个查询，该 API 层编排对 Databricks Model Serving 的调用。助手在聊天窗口中直接提供上下文答案、匹配文档链接并建议相关部件。

## 路由 Agent（智能体）与子 Agent（智能体）设计

**路由Agent（智能体）** 负责判断技术人员的查询是基于文档还是基于图像，并将其导向正确的子Agent（智能体）：

    技术人员可以在Teams中使用自然语言进行查询。系统通过Databricks Model Serving调用Claude 3.7 Sonnet，将这些查询转换为向量嵌入，搜索索引，并使用RAG（检索增强生成）技术返回上下文感知的答案。即使面对冗长的手册或设备指南，技术人员也能即时获得响应。

- **图像识别Agent（智能体）**
    早期版本通过Claude 3.7 Sonnet进行简单的文本提取，但效果参差不齐。工程师通过针对技术人员工作流程定制提示词——涵盖产品编号、制造商详情、规格、安全警告和认证日期——从而提升了性能。
    提取的数据直接映射到Delta Table的字段，将视觉参考与向量索引中的正确文档关联起来。这项改进带来了更准确、更可靠的部件识别。

## 日志记录与分析

为了保持透明度和数据治理，所有交互——路由、查询和图像请求——都被记录在**Amazon DynamoDB**中。一个每日运行的Databricks作业会提取这些日志，将其存储在Delta表中，并驱动一个专用的**AI/BI仪表板**。

该仪表板为7-Eleven提供了以下方面的可视性：

- 按技术人员统计的每日/每周/每月（见下图）查询量。
- 最常被搜索或维护的设备。
- 聊天机器人解决趋势和延迟情况。
- TMA采用率与首次修复率提升之间的相关性。

![IHM仪表板](/images/posts/3077f3336b2d.png)

## 从AWS迁移至Databricks

最初的验证概念使用了AWS组件，包括SageMaker、FAISS和Bedrock，来托管Claude 3.7 Sonnet和Llama 3.1 405B等大语言模型。虽然功能可用，但此设置需要手动重新索引、涉及多个分离的服务，并引入了延迟。

为了简化其基础设施，7-Eleven端到端地迁移到了一个完整的Databricks Agent Bricks解决方案，从而加快了响应时间。

- 使用Databricks Vector Search实现自动化向量索引。
- 通过单一的湖仓一体架构降低了延迟并简化了可观测性。

![从AWS迁移至Databricks](/images/posts/47350c094599.png)

## 实现运营影响

7-Eleven的企业维护培训师James David Coterel表示：“根据我目前的经验，技术人员维护助手（TMA）有潜力极大地提高我们的技术人员获取预防性维护和设备维修关键文档的速度、准确性和一致性。”

通过简化文档检索并减少对同事支持的依赖，TMA增强了技术人员的信心，提高了首次修复率，并将搜索时间从几分钟甚至几小时缩短到几秒钟；直接减少了停机时间并加快了门店恢复运营的速度。

与此同时，将检索、嵌入和推理从AWS迁移到Databricks，消除了对FAISS的维护和EC2负载，降低了基础设施开销并改善了延迟，这共同转化为了可衡量的运营节省和更一致的客户体验。

虽然具体的财务影响仍在测算中，但更快的首次解决率、更少的人工升级以及更低的基础设施开销相结合，显然避免了在人工工时和非计划设备停机方面的成本，这两者都与门店收入保护和客户体验稳定性密切相关。

7-Eleven计划通过以下方式扩展TMA的能力：

- 基于视频的维护指南，用于视觉和实践学习。
- 为全球维护团队提供多语言支持。
- 数据驱动的反馈循环，以持续优化响应的准确性和相关性。

了解Databricks如何帮助像7-Eleven这样的企业在单一平台上构建集成数据、文档和视觉模型的智能助手。

探索Databricks AI解决方案

##


> 本文由AI自动翻译，原文链接：[How 7‑Eleven Transformed Maintenance Technician Knowledge Access with Databricks Agent Bricks](https://www.databricks.com/blog/how-7-eleven-transformed-maintenance-technician-knowledge-access-databricks-agent-bricks)
> 
> 翻译时间：2026-01-10 04:15
