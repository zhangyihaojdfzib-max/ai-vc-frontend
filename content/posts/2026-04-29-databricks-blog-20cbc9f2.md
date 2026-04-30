---
title: AI Agent自主配置数据库：Databricks与Stripe合作
title_original: 'Databricks and Stripe Projects: Infrastructure Built for Agents'
date: '2026-04-29'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-and-stripe-projects-infrastructure-built-agents
author: ''
summary: Databricks与Stripe合作推出Stripe Projects，这是一款Agent优先的CLI工具，允许AI编码Agent自动发现、配置并支付Neon
  Postgres数据库，无需人工介入。借助Neon的Lakebase无服务器架构，Agent可在350毫秒内获得生产就绪的数据库，实现全栈应用的快速搭建与部署。该合作填补了AI应用开发中手动配置基础设施的缺口，推动自主应用开发迈向新阶段。
categories:
- AI基础设施
tags:
- Databricks
- Stripe Projects
- Neon
- AI Agent
- 无服务器数据库
draft: false
translated_at: '2026-04-30T05:34:00.803287'
---

- Databricks 是 Stripe Projects 的发布合作伙伴，Stripe Projects 是一款全新的 Agent 优先 CLI 工具，可让 AI 编码 Agent 直接发现、配置并支付 Neon Postgres 数据库，无需人工介入。
- Agent 可以在几分钟内搭建并部署全栈应用，但配置底层基础设施仍需依赖人工。
- 借助 Neon 和 Stripe Projects，Agent 可在数秒内启动一个生产就绪的 Postgres 数据库，该数据库基于 Lakebase 的无服务器架构。

AI 编码 Agent 可以在几分钟内创建、搭建并部署一个全栈应用。但配置应用基础设施仍需人工操作，这会显著拖慢进度。

人类仍然需要配置服务、操作界面、设置账户、输入信用卡信息等。每一个手动步骤都意味着自主应用开发的失败——手动配置不再只是一个摩擦点，而是 AI 应用开发中的一个明显缺口。

Databricks 已与 Stripe Projects 合作，以填补这一缺口。

## 介绍使用 Stripe Projects 进行 Neon 数据库的 Agent 化配置。

今天，Stripe 发布了 Stripe Projects——一款全新的 Agent 优先 CLI 工具，允许 AI Agent 发现、配置并支付 Neon 数据库。这是同类工具中首个完全 Agent 化的配置工具。

Databricks 自豪地成为发布合作伙伴，将 Neon 数据库无缝引入每一个 AI 开发环境。现在，Agent 可以在不到 350 毫秒内获得一个生产就绪的 Neon Postgres 数据库，无需任何人工交互。

## Lakebase 与 Neon：自主基础设施的基础

为了让 AI Agent 能够独立管理基础设施，底层数据库必须像 Agent 本身一样灵活且可编程。由 Neon 开发的 Lakebase 架构是首个专为 AI 时代设计的无服务器 Postgres 数据库。通过将计算与存储分离，Agent 可以在数秒内创建、构建并拆除 OLTP 数据库。

这种 Agent 优先的架构建立在三个核心技术支柱之上：

- **无服务器扩展与缩至零**：传统数据库需要手动配置并承担“始终在线”的成本。Lakebase 计算资源会动态调整以实时应对流量高峰，并在空闲时自动缩至零。对于 Agent 而言，这意味着它们可以启动生产就绪的环境，而无需担心容量规划或资源浪费。
- **即时数据库分支**：利用零拷贝克隆，Agent 可以在数秒内创建生产数据的隔离分支。这使得自主系统能够安全地测试代码、运行迁移或针对实时数据状态实验新提示词，而不会危及主生产环境或产生巨大的存储开销。
- **它是 Postgres**：Agent 对 Postgres 的理解优于任何其他 OLTP 数据库，这意味着使用 Lakebase 架构进行软件开发既快速又易于自动化。

通过将数据库视为一种可编程、按需提供的服务，而非静态硬件，Lakebase 架构使 Agent 能够弥合搭建创意应用与运行生产应用之间的差距。

## 开始使用 Neon 与 Stripe Projects

了解更多关于如何使用编码 Agent 与您的 Stripe Projects 账户的信息。

## 与 Databricks 和 Stripe 的更多合作

除了 Stripe Projects，Databricks 还宣布推出 Stripe 数据管道，现已在 Databricks Marketplace 上架。了解更多关于 Stripe 客户如何直接在 Databricks 账户中分析支付和业务数据的信息——无需 ETL。

### 在收件箱中获取最新文章

订阅我们的博客，让最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Databricks and Stripe Projects: Infrastructure Built for Agents](https://www.databricks.com/blog/databricks-and-stripe-projects-infrastructure-built-agents)
> 
> 翻译时间：2026-04-30 05:34
