---
title: 携手Rockset：重塑数据驱动应用的未来
title_original: 'Partnering with Rockset: The Future of Data-Driven Apps'
date: '2024-09-03'
source: 红杉资本 (Sequoia)
source_url: https://sequoiacap.com/article/rockset-and-the-future-of-data-driven-apps/
author: ''
summary: 本文阐述了数据驱动应用发展中的核心痛点——传统数据管道复杂、缓慢且难以维护。红杉资本投资的Rockset提出了一种颠覆性解决方案：通过云原生服务，直接在原始数据上建立索引并运行生产级SQL，从而彻底消除数据管道。文章介绍了Rockset的创始团队背景、产品理念及其如何帮助开发者快速构建实时应用，并展望了数据技术从分析、机器学习到实时应用的演进趋势。
categories:
- AI基础设施
tags:
- 实时数据分析
- 云原生
- 数据管道
- SQL引擎
- 红杉资本
draft: false
translated_at: '2026-02-14T04:04:30.066698'
---

# 携手Rockset：数据驱动应用的未来

![Four people standing outside](/images/posts/c5240cc51bf5.jpg)

红杉资本于2016年与Rockset建立合作关系，该公司在2024年被OpenAI收购。

过去十年最重要的技术主题之一，简而言之就是数据。

在这十年之初，新的数据技术推动了对分析和A/B测试的日益关注。而在过去几年，焦点已转向机器学习。这两项技术都植根于同一趋势——数据的指数级增长。

我们接触的CEO们深知，企业必须实现数据驱动才能在竞争中生存。但并非所有人都清楚如何实现。

起步很容易——为产品或业务部署监测工具并开始收集数据。但将这些数据转化为有价值、可操作的洞见则要困难得多。

最大的痛点之一仅仅是物理层面上的数据流转。将数据从初始原始形态迁移至最终应用的数据管道和ETL作业，往往缓慢、脆弱且难以维护。

尽管已有诸多简化这些管道的尝试，但最先进的方案仍如同鲁布·戈德堡机械般复杂。新型数据可能需要数周甚至数月才能进入生产应用——如果它们最终能够成功部署的话。

## Rockset

在红杉资本，我们热衷于与挑战传统思维的创始人合作。

当我们初次遇见Venkat和Dhruba时，他们提出了一个疑问——我们究竟为何需要数据管道？在这个云原生基础设施的新时代，为何不能运用网络级搜索技术直接在原始数据之上构建数据驱动应用？与其将管道效率提升10%，何不彻底消除它们？

他们的答案就是Rockset。这项云原生服务帮助开发者直接在原始数据上运行生产就绪的SQL。入门极其简单：

1. 创建账户
2. 将Rockset指向您的数据源（例如Apache Kafka、Amazon S3）
3. 开始编写SQL

配置数据源后，Rockset会立即开始为数据建立索引，使您能在数秒内探索数据并编写可直接应用于程序的SQL。在红杉资本内部，我们已运用Rockset将许多繁重的夜间作业迁移至实时仪表板。这不仅让我们的内部工具更高效，数据科学团队如今也能减少维护管道的时间，将更多精力投入助力被投企业成长。

Rockset诞生于Facebook一支卓越的跨学科数据团队。首席执行官Venkat Venkataramani是TAO（Facebook在线图数据库）的创始人，曾任Oracle数据库工程师。首席技术官Dhruba Borthakur是Facebook数据仓库的核心架构师之一，也是RocksDB与HDFS的共同创造者。Tudor Bosman曾参与开发Unicorn（Facebook内部搜索后端）和Gmail后端。Shruti Bhat则在VMware和Oracle担任高级产品职位。

我们最初于2016年种子轮阶段与Rockset建立合作，Greylock的朋友们也同期参与。当时，Rockset只是一个受传统SQL数据库与云原生搜索引擎融合理念启发的初步构想。如今，我们很荣幸能通过Rockset的A轮融资深化这段合作伙伴关系。

与这支团队的旅程至今精彩非凡——而这仅仅是个开始。我们无比期待看到您运用Rockset构建的成果。

本文最初由Mike Vernal发表于Medium平台。

Rockset诞生于Facebook一支卓越的跨学科数据团队。

---

> 本文由AI自动翻译，原文链接：[Partnering with Rockset: The Future of Data-Driven Apps](https://sequoiacap.com/article/rockset-and-the-future-of-data-driven-apps/)
> 
> 翻译时间：2026-02-14 04:04
