---
title: Claude金融版功能升级：新增Excel插件、实时数据连接与智能体技能
title_original: Advancing Claude for Financial Services
date: '2025-10-27'
source: Anthropic
source_url: https://www.anthropic.com/news/advancing-claude-for-financial-services
author: ''
summary: Anthropic宣布升级其面向金融服务的Claude AI功能，新增Claude for Excel插件（研究预览版），允许用户在Excel侧边栏直接与Claude协作分析、修改和创建电子表格。同时，扩展了实时市场数据连接器，新增Aiera、LSEG、Moody's等数据源，并推出6项新的预置智能体技能，如贴现现金流模型和可比公司分析，旨在提升金融建模、尽职调查等关键任务的效率与准确性。
categories:
- AI产品
tags:
- Claude
- 金融科技
- AI助手
- Excel集成
- 实时数据
draft: false
translated_at: '2026-02-08T04:35:18.790556'
---

# 金融服务业Claude功能升级

我们正在扩展**金融服务业Claude**的功能，新增Excel插件、更多实时市场数据与投资组合分析连接器，以及新的预置Agent（智能体）技能，例如构建贴现现金流模型和启动覆盖报告。

这些更新基于Sonnet 4.5在金融任务上的顶尖性能，其在Vals AI的**金融Agent（智能体）基准测试**中以55.3%的准确率位居榜首。这些更新通过为耗时但关键的金融工作提供解决方案，增强了Claude的智能，并已集成到行业首选工具中。

## Claude for Excel

我们正在以研究预览版的形式发布**Claude for Excel**测试版。这使得用户可以在Microsoft Excel的侧边栏中直接与Claude协作，Claude能够读取、分析、修改和创建新的Excel工作簿。Claude对其执行的操作提供完全透明度：它会跟踪并解释其更改，并允许用户直接导航到其解释中引用的单元格。

![Claude分析包含Acme Grille公司2020-2024年合并损益表的电子表格，提供关于财务建模的实时指导。](/images/posts/cc2f84a87e61.jpg)

这意味着Claude可以讨论电子表格的工作原理，在保持其结构和公式依赖关系的同时进行修改，调试和修复单元格公式，用新数据和假设填充模板，或者完全从头开始构建新的电子表格。

Claude for Excel是对我们现有Microsoft应用程序集成的补充。在Claude应用中，Claude也可以创建和编辑文件，包括Excel电子表格和PowerPoint幻灯片，并连接到Microsoft 365以搜索文件、电子邮件和Teams对话。部分Claude模型也可在Microsoft Copilot Studio和Researcher agent中使用。

Claude for Excel目前作为研究预览版，面向Max、Enterprise和Teams用户开放测试。我们将在更广泛推广该功能之前，收集来自1000名初始用户的真实反馈。要加入等候名单，请[点击此处](https://www.anthropic.com/claude-for-excel)。

## 将Claude连接到实时信息

**连接器**为Claude提供直接访问外部工具和平台的途径。**7月**，我们增加了对S&P Capital IQ、Daloopa、Morningstar和PitchBook的连接器。我们正在添加新的连接器，让Claude能够实时获取更多信息：

- **Aiera**为Claude提供实时财报电话会议记录以及投资者活动（如股东大会、演示和会议）的摘要；
- Aiera的连接器还支持来自**Third Bridge**的数据馈送，使Claude能够访问一个包含专家和前高管洞察访谈、公司情报和行业分析的资料库；
- **Chronograph**为私募股权投资者提供用于投资组合监控和进行尽职调查的运营和财务信息，包括绩效指标、估值和基金层面数据；
- **Egnyte**使Claude能够安全地搜索内部数据室、投资文件和已批准的财务模型中的许可数据，同时保持受控的访问权限；
- **LSEG**将Claude连接到实时市场数据，包括固定收益定价、股票、外汇汇率、宏观经济指标以及分析师对其他重要财务指标的预测；
- **Moody's**提供对专有信用评级、研究和公司数据的访问——包括超过6亿家上市公司和私营公司的所有权、财务数据和新闻——支持合规、信用分析和业务开发方面的工作和研究；
- **MT Newswires**为Claude提供关于金融市场和经济的全球多资产类别最新新闻。

有关MCP连接器设置和提示词指导以最大化每个连接器效益的详细信息，请参阅[我们的文档](https://docs.anthropic.com/en/docs/agents-and-tools/connectors)。

## 面向金融任务的新Agent（智能体）技能

本月早些时候，我们推出了**Agent（智能体）技能**。技能是包含指令、脚本和资源的文件夹，Claude可以利用这些来执行特定任务。技能适用于所有Claude应用，包括Claude.ai、Claude Code和我们的API。为了让Claude更擅长金融服务任务，我们新增了6项技能：

- **可比公司分析**，包含估值倍数和运营指标，可轻松用更新数据刷新；
- **贴现现金流模型**，包括完整的自由现金流预测、加权平均资本成本计算、情景切换和敏感性分析表；
- **尽职调查数据包**，将数据室文档处理成包含财务信息、客户列表和合同条款的Excel电子表格；
- **公司简介和概况**，为推介书和买家列表准备的简明公司概述；
- **财报分析**，研究季度电话会议记录和财务报表，提取重要指标、指引变化和管理层评论；
- **启动覆盖报告**，包含行业分析、公司深度剖析和估值框架。

与Claude for Excel一样，这些新技能正在面向Max、Enterprise和Teams用户以预览版形式推出。您可以代表您的团队或组织[在此注册](https://www.anthropic.com/claude-for-financial-services)。

## Claude在金融服务领域的影响力

Claude已被领先的银行、资产管理、保险和金融科技公司广泛使用。它支持前台任务（如客户体验）、中台任务（如承销、风险和合规）以及后台任务（如代码现代化和遗留流程处理）。随着我们针对金融服务持续更新模型和产品，我们预计Claude将在这些角色中表现得更加出色。

下方，金融服务应用人工智能负责人Alexander Bricken和金融服务产品负责人Nicholas Lin讨论了Anthropic在金融服务领域的研究和产品战略，以及客户案例。

## 开始使用

要了解更多关于使用金融服务业Claude的信息，请[参阅此处](https://www.anthropic.com/claude-for-financial-services)或[联系](mailto:sales@anthropic.com)我们的销售团队。要观看新功能的实际演示并直接听取金融服务领导者的意见，您也可以[在此注册](https://www.anthropic.com/claude-for-financial-services-webinar)参加我们的发布网络研讨会。

## 相关内容

### 推出Claude Opus 4.6

我们正在升级我们最智能的模型。在Agent（智能体）编码、计算机使用、工具使用、搜索和金融领域，Opus 4.6是一个行业领先的模型，通常优势明显。

### Claude是一个思考空间

我们做出了一个选择：Claude将保持无广告。我们解释了为什么广告激励与真正有帮助的AI助手不相容，以及我们计划如何在不妨碍用户信任的情况下扩大访问。

### Apple的Xcode现在支持Claude Agent（智能体）SDK

---

> 本文由AI自动翻译，原文链接：[Advancing Claude for Financial Services](https://www.anthropic.com/news/advancing-claude-for-financial-services)
> 
> 翻译时间：2026-02-08 04:35
