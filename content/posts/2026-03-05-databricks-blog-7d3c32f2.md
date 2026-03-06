---
title: Lakebridge新功能：更快速、更可预测的数据仓库迁移
title_original: 'New in Migrations: Faster and More Predictable'
date: '2026-03-05'
source: Databricks Blog
source_url: https://www.databricks.com/blog/new-migrations-faster-and-more-predictable
author: ''
summary: 本文介绍了数据迁移工具Lakebridge的三项最新进展，旨在消除数据仓库迁移的不确定性。新功能包括更全面的评估功能，可预测迁移工作量和成本；AI驱动的SQL转换，利用LLM将专有SQL方言转换为兼容Databricks的ANSI
  SQL，减少手动重写；以及全新的引导式桌面应用用户体验，简化迁移规划和执行流程。这些改进帮助团队更自信、高效地将遗留系统迁移至Databricks平台。
categories:
- AI产品
tags:
- 数据迁移
- Lakebridge
- AI驱动
- Databricks
- 数据仓库
draft: false
translated_at: '2026-03-06T04:40:29.866342'
---

迁移遗留数据仓库面临诸多挑战——时间线难以预测、技术债务、手动验证以及高执行风险。自去年夏季推出以来，Lakebridge 通过将迁移转变为可预测、自动化的流程，帮助数据工程师消除了这种不确定性，使迁移更易于规划、执行和信任。作为专为应对现实复杂场景而构建的免费工具，Lakebridge 将评估、代码转换、数据迁移和核对整合为端到端的引导式流程。且成效显著：已有超过 1,000 家客户和合作伙伴使用 Lakebridge 从缓慢、昂贵的遗留系统迁移至 Databricks 平台。

本篇博客将详细介绍 Lakebridge 的三项最新进展——更全面的评估功能、AI 驱动的 SQL 转换以及全新的引导式用户体验——这些功能消除了数据仓库迁移的不确定性，助力团队自信前行。

## 可预测的迁移工作量和成本

规划迁移往往是最困难的环节。团队在工作开始前难以理解现有环境的真实范围、使用模式和成本概况，导致遗漏依赖项、估算不准确以及意外的返工。

Lakebridge 会自动生成对现有环境的评估，帮助您了解迁移至 Databricks 的影响和工作量。其性能分析功能（现已支持 Synapse）从数据库系统中提取并分析元数据，提供对源环境的深入洞察，包括系统配置、资源利用率、查询模式和性能指标。这些洞察会发布到 Databricks 工作空间的仪表板中，让您了解遗留系统的使用情况，并与 Databricks 团队协作准确测算迁移至 Databricks 带来的成本节约。

您还可以利用 Lakebridge 的评估功能分析迁移的范围、使用情况和复杂性。分析器功能可提前揭示不受支持的构造、依赖关系和复杂性，使团队能够自信规划、避免返工，并加速迁移进程。

## AI 驱动的代码转换

代码转换历来是迁移中最耗时的步骤之一。遗留系统依赖专有方言、深度嵌套的逻辑和存储过程，传统的基于规则的工具无法完全翻译，迫使团队进行冗长且易出错的手动重写。

Lakebridge 利用 AI 将专有 SQL 方言（包括 T-SQL、Redshift、Teradata、Oracle 和 Snowflake）转换为开放的、兼容 Databricks 的 ANSI SQL。这种由 LLM（大语言模型）驱动的方法成功处理了复杂的 SQL 转换和嵌套逻辑——这些通常是传统基于规则工具的挑战——从而显著减少了手动代码重写的需求。

![Lakebridge 代码转换功能简化和加速数据仓库迁移](/images/posts/a8e9e99ce71a.gif)

使用 Databricks Assistant，您还可以直接在 Databricks 笔记本或 SQL 编辑器中将源 SQL 转换为 ANSI SQL。新的 `/migrate` 功能会自动分析源代码，解释其与 ANSI SQL 的差异，并生成推荐的转换。

![Lakebridge 的 AI 驱动迁移功能通过自然语言提示将源 SQL 转换为 ANSI SQL](/images/posts/44a134c94f6a.gif)

这些 AI 辅助功能共同减少了手动返工和风险，更早地发现问题，并帮助迁移以更快、更可预测的速度推进。

## 引导式用户界面

![Lakebridge 改进的用户体验，提供简洁的桌面应用](/images/posts/f0d1e69123ce.gif)

这些 Lakebridge 功能现已全部集成在一个新的桌面应用中。用户可以遵循引导式的可视化体验来规划和执行迁移，使所有用户都能更轻松地开始使用 Lakebridge。数据工程师可以更快地推进工作，分析师和项目经理能清晰了解迁移范围，团队也能更早地在时间线和风险上达成一致——从而减少前期阻力，更快地在 Databricks 上实现价值。

关键新功能包括：

- **引导式设置与自动检查**：在开始前验证系统要求
- **安全、简化的工作空间连接**：无需编辑配置文件
- **共享可见性**：工程师、架构师和利益相关者可以基于相同数据进行规划
- **一键分析**：分析源环境并生成评估报告

## 实际成功案例

通过简化团队评估、转换和验证迁移的方式，Lakebridge 帮助您自信地现代化迁移至 Databricks 数据智能平台。在 Databricks，已有数百家客户体验到使用 Lakebridge 加速实际迁移的好处。

由于 Lakebridge 免费且开源，我们约 200 家合作伙伴也利用 Lakebridge 为其客户提供更大价值，且无许可障碍。

## 未来展望

Lakebridge 帮助团队实现数据仓库现代化，使其能够在单一平台上整合数据、扩展分析并支持 AI——同时避免了通常拖慢迁移进程的风险和不确定性。结合 Databricks 的开放架构，它提供了一条快速、可预测的路径，通向**灵活的数据湖仓**，且无供应商锁定。

Lakebridge 将继续扩展其 AI 驱动能力，以更自信地处理更复杂的环境。即将发布的版本将增加更先进的评估工具和增强的 SQL 语法验证。敬请关注直至 **2026 年数据与 AI 峰会**的更新。

## 了解更多

无论您是在评估选项还是准备开始迁移，以下资源都能帮助您迈出下一步。

- **文档**：通过我们的[文档](https://docs.databricks.com/en/migration/lakebridge/index.html)深入了解 Lakebridge 的细节
- **电子书**：获取《**变革遗留数据仓库**》副本以制定您的策略
- **迁移指南**：查找从 [Microsoft SQL Server](https://docs.databricks.com/en/migration/lakebridge/sql-server.html) | [Oracle](https://docs.databricks.com/en/migration/lakebridge/oracle.html) | [Snowflake](https://docs.databricks.com/en/migration/lakebridge/snowflake.html) | [Redshift](https://docs.databricks.com/en/migration/lakebridge/redshift.html) | [Netezza](https://docs.databricks.com/en/migration/lakebridge/netezza.html) | [Teradata](https://docs.databricks.com/en/migration/lakebridge/teradata.html) 迁移的特定指南
- **技巧与窍门**：阅读 DBA 迁移至 Databricks 的[十大建议](https://www.databricks.com/blog/top-10-tips-dbas-migrating-databricks)

准备开始了吗？Lakebridge 对 Databricks 客户和合作伙伴**免费提供**。尝试新功能来规划和运行您的迁移，或联系[认证的 Databricks 迁移合作伙伴](https://www.databricks.com/partners/migration-partners)获取任何阶段的实际支持。

---

> 本文由AI自动翻译，原文链接：[New in Migrations: Faster and More Predictable](https://www.databricks.com/blog/new-migrations-faster-and-more-predictable)
> 
> 翻译时间：2026-03-06 04:40
