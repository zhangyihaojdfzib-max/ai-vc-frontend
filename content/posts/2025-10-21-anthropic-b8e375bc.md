---
title: Claude生命科学版：AI驱动科研全流程革新
title_original: Claude for Life Sciences
date: '2025-10-21'
source: Anthropic
source_url: https://www.anthropic.com/news/claude-for-life-sciences
author: ''
summary: Anthropic推出Claude生命科学专项改进，通过提升模型性能、新增科学工具连接器（如Benchling、PubMed、BioRender）、开发Agent
  Skills技能库，支持从早期研究到临床合规的全流程科学任务。该版本旨在帮助研究人员进行文献综述、实验设计、数据分析和法规申报，并联合多家合作伙伴提供领域专家支持，加速生命科学领域的发现与创新。
categories:
- AI产品
tags:
- Claude
- 生命科学
- AI科研
- 生物信息学
- Anthropic
draft: false
translated_at: '2026-02-09T04:24:19.085709'
---

# Claude 生命科学版

提升科学进步速度是Anthropic公益使命的核心组成部分。

我们致力于构建工具，让研究人员能够做出新发现——并最终使AI模型能够自主实现这些发现。

直到最近，科学家们通常将Claude用于独立任务，例如编写统计分析代码或总结论文。制药公司及其他行业企业也将其用于业务其他环节（如销售）以资助新研究。如今，我们的目标是让Claude能够支持从早期发现到转化与商业化的全流程。

为此，我们正在推出一系列改进措施，旨在使Claude成为生命科学领域工作者（包括研究人员、临床协调员和法规事务经理）更优质的合作伙伴。

## 打造更卓越的研究伙伴

首先，我们提升了Claude的基础性能。我们最强大的模型Claude Sonnet 4.5在一系列生命科学任务上显著优于先前模型。例如，在测试模型对实验室方案理解与应用能力的Protocol QA基准测试中，Sonnet 4.5得分为0.83，而人类基线为0.79，Sonnet 4的表现则为0.74。¹在衡量生物信息学任务表现的BixBench评估中，Sonnet 4.5相较前代模型也展现出类似的提升。

为使Claude在科研工作中更具实用性，我们现正新增多项科学平台连接器、Agent Skills使用能力，以及以提示词库和专属支持形式提供的生命科学专项支持。

## 连接Claude与科学工具

连接器使Claude能够直接访问其他平台和工具。我们新增了多个专为简化科研发现流程设计的连接器：

- **Benchling**：使Claude能够回应科学家提问，并提供返回原始实验、笔记本和记录的链接；
- **BioRender**：将Claude与其海量经审核的科学图表、图标和模板库相连；
- **PubMed**：提供数百万生物医学研究文章和临床研究的访问权限；
- **Wiley开发的Scholar Gateway**：在Claude内提供权威、经同行评审的科学内容以加速科研发现；
- **Synapse.org**：支持科学家在公开或私有项目中协同共享与分析数据；
- **10x Genomics**：让研究人员能够使用自然语言进行单细胞与空间分析。

这些连接器是对我们现有集合的补充，后者已包含Google Workspace和Microsoft SharePoint、OneDrive、Outlook、Teams等通用工具。Claude现已可直接与Databricks协作，为大规模生物信息学研究提供分析支持，并能通过Snowflake使用自然语言问题搜索大型数据集。

## 为Claude开发技能

上周，我们发布了**Agent Skills**：包含指令、脚本和资源的文件夹，Claude可借此提升执行特定任务的表现。技能天然契合科研工作，因为它们使Claude能够持续且可预测地遵循特定方案和流程。

我们正在为Claude开发多项科学技能，首项为**single-cell-rna-qc**。该技能使用scverse最佳实践对单细胞RNA测序数据进行质量控制和过滤：

![Claude对单细胞RNA-seq数据进行质量控制。](/images/posts/93440f629783.jpg)

除了我们创建的技能外，科学家也可构建自己的技能。有关详细信息与指导（包括设置自定义技能），请参阅此处。

## 使用Claude进行生命科学研究

Claude可用于以下生命科学任务：

- **研究类任务**，如文献综述与假设提出：Claude可引用和总结生物医学文献，并根据发现生成可检验的设想。
- **生成实验方案**：通过Benchling连接器，Claude可起草研究方案、标准操作程序和知情同意文件。
- **生物信息学与数据分析**：使用Claude Code处理和分析基因组数据。Claude可以幻灯片、文档或代码笔记本格式呈现结果。
- **临床与法规合规**：Claude可起草和审阅监管申报材料，并汇编合规数据。

此外，为帮助科学家快速上手，我们正在创建**提示词库**，以在上述任务中获得最佳效果。

## 合作伙伴与客户

我们通过应用AI团队和客户服务团队中的专属领域专家提供实操支持。

我们还与专注于帮助机构采用AI进行生命科学工作的公司合作。这些合作伙伴包括Caylent、德勤、埃森哲、毕马威、普华永道、Quantium、Slalom、Tribe AI和图灵，以及我们的云合作伙伴AWS和Google Cloud。

我们许多现有客户和合作伙伴已将Claude用于广泛的现实世界科研任务：

## 支持生命科学发展

除上述更新外，我们还通过**AI for Science**项目支持生命科学研究。该项目提供免费API额度，以支持全球从事高影响力科研项目的顶尖研究人员。

与这些实验室的合作帮助我们发掘Claude的新应用场景，同时助力科学家解答他们最紧迫的问题。我们持续欢迎项目设想的提交。

Anthropic生命科学领域合作与研发负责人Jonah Cool和Eric Kauderer-Abrams将在下文中探讨此项工作及其他近期进展。

## 开始使用

要了解更多关于Claude生命科学版的信息或与我们团队预约演示，请参阅此处。

Claude生命科学版可通过Claude.com和AWS Marketplace获取，Google Cloud Marketplace即将上线。

#### 脚注

¹Protocol QA分数（多项选择格式），采用10样本提示。更多信息请参阅我们的Sonnet 4.5系统卡第132-133页。

## 相关内容

### 推出Claude Opus 4.6

我们正在升级最智能的模型。在智能体编码、计算机使用、工具使用、搜索和金融领域，Opus 4.6是行业领先的模型，通常优势显著。

### Claude是一个思考空间

我们做出选择：Claude将保持无广告。我们解释为何广告激励与真正有用的AI助手不相容，以及我们计划如何在维护用户信任的同时扩大访问。

### 苹果Xcode现支持Claude Agent SDK

---

> 本文由AI自动翻译，原文链接：[Claude for Life Sciences](https://www.anthropic.com/news/claude-for-life-sciences)
> 
> 翻译时间：2026-02-09 04:24
