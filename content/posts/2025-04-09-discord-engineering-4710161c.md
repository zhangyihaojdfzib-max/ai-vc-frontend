---
title: Discord超频dbt：处理PB级数据的定制化方案
title_original: 'Overclocking dbt: Discord''s Custom Solution in Processing Petabytes
  of Data'
date: '2025-04-09'
source: Discord Engineering
source_url: https://discord.com/blog/overclocking-dbt-discords-custom-solution-in-processing-petabytes-of-data
author: ''
summary: 本文介绍了Discord如何扩展开源数据工具dbt以应对PB级数据处理和数百名开发者并行工作的挑战。面对原有方案在编译时间、增量策略和团队协作上的瓶颈，Discord团队实施了一系列定制化改造，包括优化编译流程、改进物化策略和防止测试冲突，从而构建了一个高效、稳健且可扩展的数据转换平台，显著提升了开发效率与数据质量。
categories:
- AI基础设施
tags:
- 数据工程
- dbt
- 大数据处理
- 数据仓库
- 可扩展性
draft: false
translated_at: '2026-01-14T04:52:50.750525'
---

在Discord，我们曾面临一个令大多数数据团队望而却步的挑战：扩展dbt以处理PB级数据，同时支持100多名开发者在2500多个模型中并行工作。最初看似简单的实现方案，很快在应对数百万并发用户生成PB级数据的场景中暴露出关键瓶颈。

dbt（数据构建工具）是一款命令行工具，用于在数据仓库中进行数据转换，并将软件工程原则引入SQL领域。它最初由费城咨询公司Fishtown Analytics开发，从默默无闻到被全球数据从业者广泛采用，该公司也因此更名为dbt Labs，以体现该工具的重要地位。

我们与dbt的结缘始于数年前，当时我们正在评估能够满足快速增长的数据需求、同时保持Discord工程师所重视的灵活性与透明度的解决方案。我们选择dbt主要因其开源特性，这与Discord尽可能利用并回馈开源社区的工程理念高度契合。

dbt的几个关键特性恰好契合我们的数据转换需求：

- 与数据技术栈中其他工具无缝集成（可参阅我们之前关于编排器Dagster的博客文章！）
- 为数据转换提供开发者友好的体验
- 模块化设计促进代码复用性和可维护性
- 全面的测试框架确保稳健的数据质量

然而，随着Discord业务规模扩大，我们最初的dbt实施方案开始不堪重负。整个dbt项目频繁重新编译，导致每次需痛苦等待20分钟以上。默认的增量物化策略未针对我们的数据量级进行优化。开发者经常意外覆盖彼此的测试表，造成混乱和精力浪费。若不解决这些扩展性挑战，我们提供及时数据洞察的能力将受到严重制约。

为突破dbt的标准能力限制，我们实施了一系列扩展其核心功能的定制方案。我们构建了一套更适配Discord规模的前沿dbt系统，该系统提升了开发效率、防止破坏性变更，并简化了复杂计算流程。我们将在本文详细阐述的定制化改造，帮助我们克服了这些挑战，建立起一个稳健、可扩展的数据转换平台，成为分析基础设施的支柱。

这不仅是又一个"我们如何使用dbt"的故事——更是将dbt扩展至真正海量规模的蓝图。我们将痛苦的编译时间转化为快速开发周期，在确保数据质量的同时，自动化了原本需要大量人工干预的复杂数据回填流程。

虽然我们使用Google BigQuery作为云服务提供商，但该解决方案基本与云平台无关，也可应用于其他云平台。


> 本文由AI自动翻译，原文链接：[Overclocking dbt: Discord's Custom Solution in Processing Petabytes of Data](https://discord.com/blog/overclocking-dbt-discords-custom-solution-in-processing-petabytes-of-data)
> 
> 翻译时间：2026-01-14 04:52
