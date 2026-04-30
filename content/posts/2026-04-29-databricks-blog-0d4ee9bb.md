---
title: Stripe数据现已通过Databricks Marketplace实时共享
title_original: Stripe data now available on Databricks via Databricks Marketplace
date: '2026-04-29'
source: Databricks Blog
source_url: https://www.databricks.com/blog/stripe-data-now-available-databricks-databricks-marketplace
author: ''
summary: Stripe Data Pipeline现已通过Databricks Marketplace提供，利用Delta Sharing技术将Stripe支付和业务数据直接共享到Unity
  Catalog。用户无需轮询或维护代码，即可实时查询支付数据，为AI模型、智能体和Genie工作空间提供动力。该集成消除了API调用费用、数据重复和治理难题，支持行级和列级访问控制。文章还介绍了多种应用场景，如欺诈监控、客户流失预测和自然语言查询，使Stripe数据成为Unity
  Catalog中的普通表，简化了数据分析和AI应用开发。
categories:
- AI基础设施
tags:
- Stripe
- Databricks
- Delta Sharing
- 数据管道
- AI应用
draft: false
translated_at: '2026-04-30T05:33:53.219769'
---

在几分钟内通过Delta Sharing激活Stripe数据管道，即刻赋能AI应用。将Stripe支付和业务数据直接共享到Unity Catalog，为所有AI和分析计划创建单一数据源。在Databricks中查询实时支付数据，立即为模型、Agent（智能体）和Genie工作空间提供动力。

如果你正在使用Databricks，很可能已经构建了一个Stripe集成。它可能是一个ETL工具，也可能是一个每晚轮询的自定义Python任务。它能工作，但代价不菲：API调用、维护负担、数据陈旧，以及时刻担心夜间某处出错的焦虑。

Stripe Data Pipeline改变了这一切。它现在通过Databricks Marketplace提供，借助Delta Sharing进行共享。无需轮询，你的Stripe数据直接流入Unity Catalog——新鲜、实时，且无需一行维护代码即可立即为你的AI模型提供燃料。

![Marketplace上的Stripe数据管道](/images/posts/435a3bffdb6e.png)

### 这实际上能为你带来什么

你的Stripe支付和业务数据完整到达：交易记录、客户历史、订阅、退款、付款。数据保留在Stripe的基础设施中。你通过Delta Sharing直接查询它。

与你的API任务的主要区别在于，所有数据直接落入你的Databricks平台，使你能够通过单个查询将其与其他表连接。这种统一的数据层是可靠AI的基础。它消除了对单独转换层的需求，通过避免按次调用费用来降低成本，并移除了连接器许可费。它还能防止可能增加存储需求的数据重复。治理是集成的，数据出现在Unity Catalog中，并支持行级和列级访问控制、审计追踪以及合规功能。此外，你的Stripe API密钥不再分散在不同的凭证库中。

### 使用Stripe与Databricks你实际上能构建什么

Stripe数据解锁了多种可能性

- 随着Stripe数据流入Unity Catalog，你可以部署一个AI Agent（智能体），持续监控交易，在欺诈、退款激增或对账缺口成为问题之前进行标记。
- 你可以将交易历史与行为信号相结合，对哪些客户可能流失进行评分，然后自动将他们路由到由LLM（大语言模型）驱动的留存工作流中。
- 你可以向Genie提出诸如“按地理位置显示MRR”之类的随意问题，无需编写SQL即可获得即时仪表盘。
- 你可以构建合规就绪的分析应用，让财务团队探索支付数据，而无需接触原始表。

所有这些之所以可行，是因为你的Stripe数据现在只是Unity Catalog中的另一个表。

### 开始使用

访问Databricks Marketplace上的Stripe Data Pipeline即可开始。

### 获取最新文章到你的收件箱

订阅我们的博客，让最新文章直接发送到你的收件箱。

---

> 本文由AI自动翻译，原文链接：[Stripe data now available on Databricks via Databricks Marketplace](https://www.databricks.com/blog/stripe-data-now-available-databricks-databricks-marketplace)
> 
> 翻译时间：2026-04-30 05:33
