---
title: Tevogen Bio携手微软与Databricks，用AI加速救命疗法研发
title_original: Tevogen Bio’s Journey to Streamlining Life-Saving Therapies
date: '2026-03-25'
source: Databricks Blog
source_url: https://www.databricks.com/blog/tevogen-bios-journey-streamlining-life-saving-therapies
author: ''
summary: 本文介绍了生物技术公司Tevogen Bio如何通过与微软和Databricks合作，利用其专利的ExacTcell平台和AI技术，应对药物研发周期长、成本高的挑战。通过构建基于Databricks
  Medallion架构的现代数据湖仓，团队将数据处理时间从50天缩短至24小时，并训练出高召回率的PredicTcell模型，旨在精准预测蛋白质结合肽段，从而加速针对病毒、肿瘤等疾病的疗法开发，最终目标是提供更快速、经济、可及的医疗方案。
categories:
- AI研究
tags:
- AI制药
- 生物信息学
- Databricks
- 机器学习
- 药物发现
draft: false
translated_at: '2026-03-26T05:06:16.826243'
---

## 加速长达十年的药物发现进程

药物开发成本超过30亿美元，需要投入10-12年时间才能将产品推向市场。这些因素直接导致了特定产品在可及性和成本方面的问题。

Tevogen Bio 创建了获得专利的 ExacTcell 平台，旨在针对任何给定的病毒性、肿瘤性或神经系统疾病，确定针对单一 HLA 限制的目标，以解决这些问题。其针对单一病毒候选株 SARS-COV2 的概念验证试验的初始靶点选择是通过人工方法进行的。这种单一 HLA 限制的产品虽然能够覆盖大多数人群，但需要投入大量的时间和资源，需要通过湿实验室科学进行 18-24 个月的测试和确认。

为了实现 Tevogen 提供更快、更便宜、更易获取的医疗服务的使命，Tevogen.AI 与 Microsoft 和 Databricks 合作，优化其核心平台的科学理解，同时旨在简化和加速其针对其他适应症的研发管线。

面临的挑战是：摄取并创建一个涵盖多种疾病的蛋白质序列库，使科学家和研究人员能够将原本需要数月的过程缩短至数天，乃至数小时。

此外，该数据集将用于训练 Tevogen.AI 获得专利的基础算法模型，这些模型由 Tevogen Bio 的专有科学支持。Tevogen 的高管团队还提出了另一个挑战：策划一个已知遗传蛋白质的数据集，用于训练算法模型，使其能够利用机器学习方法预测具有免疫活性的肽段。

## 瓶颈：处理数太字节规模的数据集

为了策划这个数据集，团队面临一个独特的挑战：必须获取并组织一个数太字节规模的数据集，并包含相关特征以促进算法训练。这带来了两个主要问题：

1.  创建数据管道，通过多级清洗和过滤快速获取并组织相关信息；
2.  将原本设计为串行运行的流程转换为并行运行。

这正是 Databricks 成为关键合作伙伴的地方。

### 使用 Databricks 构建现代数据湖仓

我们选择 Databricks 平台作为我们现代化工作的基础。利用 **Medallion 架构** 和 **Unity Catalog** 的强大功能，我们构建了众多数据管道，将数据精心存储到青铜层、白银层和黄金层，同时保持严格的治理和细粒度的访问控制。

借助分布式计算的力量以及更清晰的结构，我们成功将流程所需时间从 50 天缩短至 24 小时。Medallion 架构也成为开发各种机器学习模型的基础。

得益于 Databricks 专业服务团队专家（特别感谢 Vibhor Nigam 和 Mohamad Abafoul）的帮助，Tevogen.AI 得以进行大规模处理，积累了一个包含 2400 万个蛋白质的数据集，然后经过提炼和排序，从 Medallion 架构的青铜层到白银层，衍生出 160 亿个数据点和约 7 亿个独特的肽段。此外，我们还策划了约 3700 万篇交叉匹配的专家文章。

![数据智能重塑行业](/images/posts/a64d41133ca4.png)

## 从数据到 AI：训练 PredicTcell 模型

任何在生物信息学领域工作过的人都明白，在几个月内完成这项工作绝非易事。在此过程中，团队能够并行工作，创建了一个 MLOps 框架，以实现自动化的训练、推理、监控和留存。在合作初始阶段完成后，团队成功交付了 PredicTcell 模型的 Alpha 版本，该模型使用传统的 XGBoost 方法和 ESM 模型进行训练，最终实现了 93-97% 的召回率和 38-43% 的准确率。

此外，数据集的扩展使 Tevogen 的科学团队能够获得并为模型训练周期提供新的见解，从而在每次迭代中完善训练方法。我们继续为训练集添加更多特征，例如，通过集成 RAG 的 Agent Bricks 结合生化特性，快速评估专家文章。

## 展望未来：解锁医学的圣杯

随着 PredicTcell 模型 Beta 版本的训练启动，以及我们 AdapTcell 模型 Alpha 版本工作的开始，Tevogen.AI 在创建最先进的肽段-蛋白质结合亲和力预测模型方面处于独特地位，其准确性不断提高，这是解锁医学圣杯的关键。

凭借其专有模型，Tevogen.AI 有信心能够实现其最终目标：以极高的准确度预测任何蛋白质（无论是新型的还是已知的）的结合肽段。

"在概率性工作流程中增加确定性是解锁成功的关键。平衡体内/计算机模拟的试错过程是每家生物技术公司在药物开发中都应关注的重点。" Tevogen 首席信息官兼 Tevogen.AI 负责人 Mittul Mehta 表示。

"我对我们与 Databricks 和 Microsoft 的合作关系感到非常满意，因为双方都带来了最佳能力，使我们能够持续创新，并实现 Tevogen 为大量患者群体提供负担得起且可及的疗法的目标。我期待继续与这两个优秀的合作伙伴合作，在药物研发的 AI 领域进行创新。"

---

> 本文由AI自动翻译，原文链接：[Tevogen Bio’s Journey to Streamlining Life-Saving Therapies](https://www.databricks.com/blog/tevogen-bios-journey-streamlining-life-saving-therapies)
> 
> 翻译时间：2026-03-26 05:06
