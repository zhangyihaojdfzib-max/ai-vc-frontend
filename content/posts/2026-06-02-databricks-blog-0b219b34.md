---
title: Query Tags：为仓库查询注入缺失的业务上下文
title_original: 'Query Tags: The Context Your Warehouse Queries Have Been Missing'
date: '2026-06-02'
source: Databricks Blog
source_url: https://www.databricks.com/blog/query-tags-context-your-warehouse-queries-have-been-missing
author: ''
summary: Databricks SQL 推出 Query Tags 公开预览版，允许用户将自定义键值对（如项目、成本中心、团队）附加到每次 SQL 执行中，并通过系统表或
  Genie 进行查询。该功能解决了传统查询日志缺乏业务上下文的问题，支持从 dbt、Power BI、Tableau 等合作伙伴工具自动注入标签，也可通过 API、连接器或
  SQL 编辑器手动标记。Query Tags 已获数百客户采用，每周标记数百万查询，显著提升成本分摊、性能排查和工作负载分析效率。
categories:
- AI基础设施
tags:
- Databricks SQL
- Query Tags
- 数据仓库
- 查询标记
- 成本分摊
draft: false
translated_at: '2026-06-03T06:53:27.059330'
---

- 按团队、项目、仪表盘或任何自定义维度分摊共享仓库成本
- 通过自动标记 dbt（模型名称）、PowerBI（报告 ID）、Tableau（工作簿名称）等，监控或排查来自合作伙伴工具的查询
- 从任何位置标记查询：SQL 编辑器、笔记本、仪表盘、API、连接器和驱动程序

Databricks SQL 会自动记录每个查询的关键属性：谁运行的、在哪个仓库上、以及来自哪个工具。但这通常还不够。

当 Power BI 查询运行缓慢时，你知道它来自 Power BI，但不知道要修复哪个仪表盘。当成本飙升时，你可以看到哪些用户运行了查询，但不知道应该向哪个成本中心或项目收费。缺失的部分是自定义上下文，而这正是 Query Tags 所添加的功能。

今天，我们推出 Query Tags 公开预览版。Query Tags 允许你将业务上下文作为多个键值对附加到每次 SQL 执行中，并通过系统表使用标准 SQL 进行查询——或者直接询问 Genie。Query Tags 在查询配置文件 UI 中也可见（查询历史 UI 中的搜索支持即将推出）。

Query Tags 已被广泛采用，数百名客户每周标记数百万个查询。

## 只需标记：介绍 Query Tags

通过 Query Tags，你可以将自定义键值对（例如“project”：“finance_planning”）附加到每次 SQL 执行中。这些标签随查询一起传输，并记录在查询历史系统表中，从而可用于分组、过滤和分析工作负载。

标签在三种场景下增加价值：

1. 合作伙伴工具：使用 dbt、Power BI 或 Tableau 时，将 dbt 模型名称、Power BI 报告 ID 或 Tableau 工作簿名称等标识符传播到每个查询中。
2. 自定义应用程序：通过 SQL 语句执行 API 或连接器构建应用程序时，将 `customerid`、`applicationname` 或 `app_version` 等元数据附加到每次执行中。
3. Databricks UI 中的临时工作：使用与你相关的维度标记查询——开发与生产环境、成本中心、实验名称或团队。

让我们深入探讨这些场景。

### (1) 将每个合作伙伴工具查询追溯到其来源

来自 dbt、Power BI 和 Tableau 的查询流入你的仓库——但如果没有标签，除了用户 ID 和它们来自哪个工具之外，这些查询无法追溯。这些工具通过自动注入 Query Tags 来解决这个问题，无需手动标记。

dbt 会自动用模型名称、核心版本、适配器版本和物化类型标记每个查询。如果某个 dbt 模型突然性能下降，你可以精确定位是哪个模型、哪个版本以及何时发生的：

ASOS 的员工工程主管 Dipesh Bhundia 和 Dave Couse 补充道：

Power BI 和 Tableau 在连接级别支持自定义 Query Tags。设置一次，来自该连接的每个查询都会自动携带这些标签。对于 Tableau，客户发现使用 [WorkbookName] 等参数作为标签值很有用，这样即使工作簿被重命名，归属关系也能保留。

![设置查询标签](/images/posts/73ab90f7c069.png)

有关支持 Query Tags 的合作伙伴工具的完整列表，请参阅文档。如果你的工具未列出，请联系你的客户团队。

### (2) 将匿名 API 查询转变为可追溯的工作负载

自定义应用程序通过 API 和连接器访问你的仓库，但它们生成的查询不携带任何应用程序上下文——没有应用程序名称、没有团队名称、没有客户 ID。Query Tags 允许你在连接或语句级别附加此元数据。

SQL 语句执行 API 支持在语句级别进行标记。作为参数传递的标签适用于该特定执行：

Python 连接器支持连接级别和语句级别的标记。在连接上设置团队名称；在需要时按语句覆盖：

Unit21 的 DevOps 工程师 Matthew Haber 分享道：

有关连接器和驱动程序支持（Node.js、Go、JDBC 等）的完整列表，请查看文档。

### (3) 标记你自己的工作，使其不会在噪音中丢失

分析师每周运行数百个查询（探索、生产、调试等），如果没有标签，它们在系统表中看起来都一样。Query Tags 允许从业者在使用一行 SQL 时随时标记，无论他们在哪里提交查询：SQL 编辑器、笔记本、仪表盘和警报。

一旦设置，会话中的所有后续语句都会自动携带这些标签。无需单独注释每个查询。例如，在 AI/BI 仪表盘中为每个数据集查询添加 SET QUERY_TAGS 语句，会将该仪表盘中的每个查询标记为“environment: production”。

数据从业者可以利用此功能：

- 按项目或团队标记临时分析
- 标记实验或 A/B 测试
- 识别开发与生产工作负载
- 在调查问题时附加调试上下文

## 从标签到答案：使用系统表进行监控

一旦查询被标记，标签就会记录在查询历史系统表的 `query_tags` 列中。现在，难题变成了简单的 SQL。

哪个团队在推动仓库成本？

许多组织需要按团队或产品分摊共享仓库成本。使用 Query Tags，只需一个查询——无需拆分仓库或猜测。

哪个 dbt 模型引入了回归？

当管道变慢时，你需要知道是哪个模型，而不仅仅是哪个仓库。通过自动注入的 dbt 模型名称标签过滤 system.query.history 来隔离问题。

或者，完全跳过编写 SQL，直接询问 Genie。因为 Query Tags 将业务上下文存储在系统表中，Genie 可以用自然语言推理你的工作负载数据。例如：“哪个 dbt 模型的查询数量最多？哪个的平均查询时间最长？”

![自然语言查询分析示例](/images/posts/498fae78f600.png)

Query Tags 解锁了更多监控用例：

1. 按 query_tags['cost_center'] 分组以进行成本回收
2. 按 query_tags['@@dbt_model_name'] 过滤以监控管道健康
3. 识别每个 Tableau 工作簿中的长时间运行查询
4. 比较 query_tags['env'] 以区分开发和生产流量

## 下一步计划

Query Tags 目前已在 SQL 仓库的公开预览版中推出，我们已经在努力使其对客户的监控体验更有帮助。请参阅文档以获取更新。

- Power BI 自动标记：Power BI 将自动将 DatasetId 和 ReportId 等元数据附加到每个查询，无需任何配置。你现在可以按照文档中的步骤手动启用此功能。自动标记将在下一个 Power BI 版本中默认开启。
- 更广泛的连接器支持：除了 Python，语句级标记现在可用于 Go 和 Node.js。
- UI 中的可搜索性：我们将很快在查询历史 UI 中支持搜索，以便你可以搜索具有特定标签的查询（例如 "@@dbt_model_name": "my_model"）。
- 支持超越 SQL 仓库：我们正在将 Query Tags 引入无服务器笔记本和作业，以便相同的标记和归属模型扩展到笔记本工作负载。

## 立即试用 Query Tags

每个未标记的查询都是错失归属机会。无论你是需要按团队分摊仓库成本、将慢查询追溯到特定仪表盘，还是按项目标记分析师工作——Query Tags 都为你提供了执行此操作的上下文。

如果你使用 dbt，你已经在标记了（检查你的查询历史系统表）。对于 Power BI、Tableau 和自定义应用程序，设置只需几分钟。对于临时工作，只需一行 SQL。

Query Tags 现已在所有云平台的公开预览版中提供。从文档开始使用。

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章直接发送到你的收件箱。

---

> 本文由AI自动翻译，原文链接：[Query Tags: The Context Your Warehouse Queries Have Been Missing](https://www.databricks.com/blog/query-tags-context-your-warehouse-queries-have-been-missing)
> 
> 翻译时间：2026-06-03 06:53
