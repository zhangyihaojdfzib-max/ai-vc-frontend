---
title: 跨引擎ABAC：统一湖仓治理新突破
title_original: Introducing Cross-Engine ABAC
date: '2026-06-02'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-cross-engine-abac
author: ''
summary: Unity Catalog推出跨引擎ABAC（基于属性的访问控制）Beta版，基于Iceberg REST Catalog扫描API构建，允许企业在目录层集中定义一次行过滤器和列掩码策略，并在任何支持Iceberg
  REST的引擎上强制执行。该方案解决了传统治理中策略分散、需手动复制或牺牲安全性的痛点，实现了开放存储与统一治理的结合。目前支持Apache Spark，未来将集成Starburst、DuckDB等引擎，并计划通过Apache
  Iceberg社区推动标签交换标准，实现更灵活的元数据共享。
categories:
- AI基础设施
tags:
- Unity Catalog
- ABAC
- Iceberg REST
- 湖仓一体
- 数据治理
draft: false
translated_at: '2026-06-04T06:36:15.725224'
---

- Unity Catalog 在外部引擎上实施基于属性的访问控制（ABAC）。只需定义一次基于标签的行过滤器和列掩码，即可在任何引擎上强制执行。
- 在目录层进行集中治理意味着策略在数据到达引擎之前就已强制执行——引擎本身无需任何策略逻辑。
- 跨引擎 ABAC 基于 Iceberg REST Catalog 扫描 API 构建，这是一个开放规范，任何引擎都可以采用它来将策略执行委托给目录。

去年12月，我们分享了完成湖仓一体愿景：开放存储、开放访问和统一治理。我们描述了一个世界，组织可以在 Unity Catalog 中一次性定义细粒度访问策略，并在每个引擎、每个表、每个用户上强制执行。今天，我们正在扩展这一愿景。

我们宣布跨引擎 ABAC 的 Beta 版本，它使企业能够使用 Iceberg REST Catalog API 在外部引擎上实施基于属性的访问控制（ABAC）。借助跨引擎 ABAC，Unity Catalog 成为第一个也是唯一一个提供跨引擎 ABAC 执行的目录，允许从每个引擎强制执行基于标签的行过滤器和列掩码。

## 为何重要

Databricks 开创的开放湖仓一体使互操作性成为可能。Delta Lake 和 Apache Iceberg 等开放表格式将组织从锁定中解放出来；任何引擎都可以读取同一份数据副本，而无需复制或将数据转换为不同格式。然而，治理并未随之而来。行级和列级策略仍然孤立在各个引擎运行时内部。

这给安全团队带来了痛苦的权衡：在每个引擎上手动复制策略并希望它们保持同步，为不同的消费者维护单独的表副本，或者授予比预期更广泛的访问权限并接受风险。

跨引擎 ABAC 消除了这种权衡。

## 跨引擎 ABAC 带来的价值

通过此 Beta 版本，Unity Catalog 对由外部引擎读取的数据强制执行细粒度访问控制策略。这包括：

- **行过滤器和列掩码**—— Unity Catalog 策略的全部表达能力，包括基于标签的规则、条件逻辑和 SQL UDF
- **多引擎支持**—— 由于策略执行通过 Iceberg REST Catalog 扫描 API 运行，因此支持任何 Iceberg REST 客户端。跨引擎 ABAC 在设计上是开放的，不绑定到特定连接器。今天，您可以通过 Iceberg-Spark 和 Delta-Spark 连接器使用 Apache Spark。即将推出其他引擎集成，例如 Starburst 和 DuckDB。

在 Unity Catalog 中定义一次 ABAC 策略，并确保它们在 Databricks 或任何与 Iceberg REST Catalog 集成的引擎上都能强制执行。

## 工作原理

跨引擎 ABAC 基于 Iceberg REST Catalog 扫描 API 构建，这是一个开放规范，任何引擎都可以采用它来将策略执行委托给目录。借助跨引擎 ABAC，目录处理策略执行，引擎处理查询。组织可以在不牺牲查询运行灵活性的情况下获得细粒度安全性。

当用户从外部引擎查询具有细粒度访问控制策略的表时：

1. 引擎通过 Iceberg REST Catalog 扫描 API 向 Unity Catalog 发送扫描请求
2. Unity Catalog 评估用户的权限和所有适用的策略
3. Unity Catalog 返回一个限定于用户被授权访问数据的过滤扫描计划
4. 引擎针对扫描计划中的过滤文件完成查询

策略执行发生在目录层，在数据到达引擎之前。引擎不需要理解或实现任何策略逻辑；它只处理接收到的数据。这意味着跨引擎 ABAC 可以适用于任何引擎，即使它没有原生治理运行时。

## 未来展望

跨引擎 ABAC 通过集中执行实现了今天的统一治理：目录评估策略并仅返回用户被授权访问的数据。这是对于没有原生治理运行时的“不可信”引擎的最佳方法，并且可以立即与任何采用 Iceberg REST Catalog 扫描 API 的引擎配合使用。

集中执行是图景的一部分。行业还需要一种可扩展的策略和元数据交换方法——一种目录可以共享治理元数据，以便策略可以在外部引擎中原生执行的方法。

我们正在 Apache Iceberg 社区中为此讨论做出贡献，提出了一项关于目录交换标签的提案，这些标签承载着治理和语义上下文。通过共享标签，湖仓一体中的引擎可以基于相同的治理和业务上下文进行操作，无论数据在哪里读取。

集中执行和元数据交换是互补的。随着数据生态系统的发展，Unity Catalog 将同时支持两者。

## 开始使用

跨引擎 ABAC 现已在 Beta 版本中可用。要试用：

1. **启用预览**：在 Databricks 预览门户中注册“跨引擎 ABAC”（请参阅管理 Databricks 预览）
2. **定义您的 ABAC 策略**：在您的 Unity Catalog 表上创建基于标签的行过滤器和列掩码（请参阅 ABAC 文档）
3. **从外部引擎查询**：通过 Iceberg-Spark 或 Delta-Spark 连接器连接 Apache Spark，并确认策略在读取时已强制执行

完整的设置说明和配置详情可在跨引擎 ABAC 文档中找到。

刚接触 Unity Catalog？请按照适用于 AWS、Azure 或 GCP 的入门指南操作。

## 参加 2026 年数据与 AI 峰会

2026 年数据与 AI 峰会即将到来！2026 年 6 月 15 日至 18 日，加入我们在加利福尼亚州旧金山 Moscone 中心的活动，了解领先组织如何使用 Unity Catalog 跨引擎治理数据和 AI。立即注册，抢先了解开放、统一治理的未来。

### 在您的收件箱中获取最新文章

订阅我们的博客，将最新文章发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Introducing Cross-Engine ABAC](https://www.databricks.com/blog/introducing-cross-engine-abac)
> 
> 翻译时间：2026-06-04 06:36
