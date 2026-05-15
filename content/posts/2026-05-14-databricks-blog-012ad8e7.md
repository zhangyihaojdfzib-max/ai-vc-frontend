---
title: Unity Catalog开放API扩展：外部引擎可访问托管表
title_original: Expanded interoperability with Unity Catalog Open APIs
date: '2026-05-14'
source: Databricks Blog
source_url: https://www.databricks.com/blog/expanded-interoperability-unity-catalog-open-apis
author: ''
summary: Unity Catalog推出多项开放API更新，包括对托管Delta表的外部访问进入Beta阶段，支持Apache Spark、Flink、DuckDB等引擎创建、读写托管表，并实现事务安全与审计。凭证分发功能全面可用，新增M2M
  OAuth认证和自动凭证刷新，支持企业级安全访问。此外，卷凭证分发进入公开预览，扩展了对非结构化数据的治理。这些更新旨在打破数据孤岛，实现统一治理与跨引擎协作。
categories:
- AI基础设施
tags:
- Unity Catalog
- Delta Lake
- 开放API
- 数据治理
- 湖仓一体
draft: false
translated_at: '2026-05-15T05:58:36.172308'
---

- 对UC托管Delta表的外部访问现已进入Beta阶段。Apache Spark、Flink和DuckDB等外部引擎现在可以创建、读取和写入托管Delta表。
- UC托管Delta表基于Delta Lake的新目录提交功能构建——这是一种开放标准，通过目录协调提交，实现安全的并发写入、可审计性和多语句事务。
- 凭证分发现已全面可用。数千名客户使用凭证分发从外部引擎安全访问UC数据资产，现在支持M2M OAuth认证，并为长时间运行的管道提供自动凭证刷新。

Unity Catalog专为开放湖仓一体而设计。过去，数据团队被困在孤岛中，常常被迫跨平台复制数据，仅仅为了使用他们想要的工具。每个新平台或工具都意味着复制数据集、从头重建访问策略，并保持一切同步。结果是冗余存储导致成本增加、策略不同步而偏离，以及数据访问和发现变得碎片化。

当我们开源Unity Catalog并推出开放API时，我们打破了此前将客户锁定的孤岛。企业终于可以保留一份数据副本，使用任何计算引擎，并从一处管理所有内容。UC生态系统自此蓬勃发展。如今，数千名客户使用Unity Catalog来治理和访问Delta Lake和Apache Iceberg表，在日益壮大的Unity Catalog生态系统中拥有数十种集成——从Apache Spark和Trino到DuckDB和Confluent Tableflow。

## 对托管表的外部访问，现已进入Beta阶段

UC托管表是开放性与性能的结合点。这些高级表使用预测优化和液态聚类自动调整数据布局、运行压缩和清理、保持统计信息新鲜——在通过开放API完全可访问的同时，实现高达20倍的查询加速和50%的存储成本降低。

现已进入Beta阶段，Apache Spark、Flink和DuckDB等外部引擎可以创建和写入UC托管Delta表，并享受集中治理和自动优化。

借助Beta版本，外部引擎可以：

- 创建托管表——直接从外部引擎建立新的UC托管表。
- 批量读取和写入——以完整的事务安全性读取和写入托管表。
- 流式读写托管表——将托管表同时用作流式源和接收端，在Apache Spark上实现端到端实时管道。

由于每个操作都流经基于目录提交构建的UC托管表，您将获得序列化提交，防止日志损坏，并对每次读取和写入实现完全可审计性。预测优化继续无缝运行，即使在外部引擎访问的表上也是如此。目录提交还为需要集中提交协调器的多语句、多表事务等功能奠定了基础。

随着引擎扩展对托管表外部访问的支持，蓬勃发展的UC生态系统持续壮大。Delta Kernel——用于读取、写入和提交Delta表的开源Java和Rust库——抽象了底层协议细节，使连接器开发者可以专注于UC集成，而非Delta实现。Apache Spark、Delta Flink和DuckDB都利用了Delta Kernel来支持对UC托管表的外部写入，并与目录管理的提交集成，生态系统持续发展。通过处理底层协议复杂性，Delta Kernel使任何引擎都能轻松与Unity Catalog集成，从而促进连接器生态系统的增长。

## 凭证分发实现安全的外部访问

对于外部引擎访问UC中的数据，它需要一种安全的方式来认证并获得对云存储的范围限定访问，而无需广泛、静态的权限或绑定到特定账户的凭证。Unity Catalog通过凭证分发来处理这一问题，该功能现已全面可用（GA）：UC按需向外部引擎发放短期、范围限定的凭证，并集中执行访问策略。

数千名客户已使用UC开放API，而两项新增功能使其在企业规模下达到生产就绪状态。外部引擎现在可以使用机器对机器（M2M）OAuth向UC进行认证，满足企业安全要求，而无需依赖个性化访问令牌（PAT），后者是每用户、长期有效且难以轮换的。凭证由引擎通过UC凭证分发API自动刷新，因此运行数小时的管道可以可靠完成，而不会在作业中途出现令牌过期。

![使用外部计算引擎通过凭证分发执行查询](/images/posts/80f2328a5ea3.png)

借助凭证分发，企业可以从任何兼容的引擎或工具在Unity Catalog中读取、写入和创建托管表及外部表。这些凭证是短期有效的，范围限定于所请求的资源，并受UC权限管理。这意味着您的平台团队可以完全控制哪些主体可以外部访问数据以及他们可以对其执行哪些操作。

## 针对卷的凭证分发

凭证分发不仅适用于表，还扩展到非结构化数据。卷凭证分发现已进入公开预览阶段，因此外部客户端可以请求临时、范围限定的凭证，以访问存储在卷中的图像、PDF和视频，并受Unity Catalog治理。无论您是查询表还是在外部处理原始视频文件，相同的访问控制模型、审计跟踪和范围限定凭证都适用。

## 下一步是什么？

我们持续投资以增强外部访问能力。目前凭证分发管理外部引擎的粗粒度访问控制。我们还开发了针对外部读取实施基于属性的访问控制（ABAC）的功能，使治理更加精细。这使得在从外部引擎读取UC托管表时，可以强制执行行级和列级ABAC策略。

## 立即开始

要开始使用凭证分发，请参阅我们的文档。要使用对托管Delta表外部访问的Beta版本：

1. 在Databricks预览门户中注册“External Access to Unity Catalog Managed Delta Table”（请参阅管理Databricks预览）。
2. 在您的元存储上启用外部数据访问，并在包含您要访问的表的模式上授予EXTERNAL_USE_SCHEMA权限。
3. 创建一个新的UC托管表。要迁移现有数据，请参阅将外部表转换为托管表的迁移指南。
4. 使用Delta-Spark 4.2和Unity Catalog 0.4.1从外部计算创建、读取和写入托管表。请参阅外部访问文档。

## 参加2026年数据与AI峰会

2026年数据与AI峰会即将到来！请于2026年6月15日至18日加入我们在加利福尼亚州旧金山莫斯康中心的活动，了解领先组织如何使用Unity Catalog跨引擎治理数据和AI。立即注册，抢先了解开放统一治理的未来发展。

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Expanded interoperability with Unity Catalog Open APIs](https://www.databricks.com/blog/expanded-interoperability-unity-catalog-open-apis)
> 
> 翻译时间：2026-05-15 05:58
