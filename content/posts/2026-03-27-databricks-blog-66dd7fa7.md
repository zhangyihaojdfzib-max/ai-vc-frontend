---
title: 利用默认仓库保障性能并降低意外成本
title_original: Protect Performance and Reduce Surprise Costs with Default Warehouse
date: '2026-03-27'
source: Databricks Blog
source_url: https://www.databricks.com/blog/protect-performance-and-reduce-surprise-costs-default-warehouse
author: ''
summary: Databricks SQL推出的默认仓库功能，允许管理员为临时查询场景指定自动使用的SQL仓库。该功能解决了因仓库选择不当导致的性能下降、成本不可预测和治理挑战。通过工作区级别默认设置、用户自定义覆盖以及管理员API，实现了对探索性查询资源的有效引导与控制。已有超过300家客户验证其成效，显著降低了探索性查询成本并减少了用户手动选择仓库的需求。
categories:
- AI基础设施
tags:
- Databricks
- 数据仓库
- 成本优化
- 性能管理
- SQL
draft: false
translated_at: '2026-03-31T05:06:41.301729'
---

默认仓库（Default Warehouse）现已在 Databricks SQL 中全面推出，它允许管理员指定在临时查询场景中自动选择哪个 SQL 仓库。默认仓库确保探索性查询能在合适的计算资源上运行，成本可控，而无需用户了解应选择哪个仓库。

从而减少意外的仓库启动、实现更好的工作负载隔离，并获得更可预测的性能与支出。

## 当前仓库选择面临的挑战

随着 Databricks SQL 的普及，工作区中的仓库数量也在增加。客户通常会为 ETL、BI 和临时查询配置不同的仓库，并根据所需的价格/性能需求调整其规模（例如，T恤尺码和最大集群数量）。

对于生产环境的 ETL 和 BI 工作负载，特定的仓库会与相关资产或工具绑定。然而，对于临时查询，没有预先分配的仓库，需要用户手动选择。

如果没有可配置的默认选项，系统会回退到“最后选择”行为或按字母顺序排序。这可能导致以下挑战：

- **性能下降** – 临时查询落在大型生产仓库上，与关键工作负载竞争资源
- **成本不可预测** – 为轻量级的探索性查询不必要地启动大型仓库
- **治理挑战** – 本用于探索的查询在团队专用或应用专用的仓库上运行

默认仓库直接解决了这个问题。

## 解决方案：默认仓库

默认仓库允许管理员为临时 SQL 界面设置一个工作区级别的默认 SQL 仓库，这些界面包括 SQL 编辑器、目录浏览器、AI/BI 仪表板、警报和 Genie Spaces。

用户可以根据需要自定义自己的默认仓库（例如，他们是拥有专用仓库的高级用户）。管理员对用户设置的默认仓库拥有可见性和最终控制权。

这为两个层面提供了灵活性：

- 管理员将大多数临时工作负载引导至目标仓库。
- 大多数用户甚至无需考虑选择仓库，而高级用户可以选择适合其工作流程的自己的默认仓库。

结果是：临时工作负载在目标仓库上运行，为管理员节省成本，为用户节省时间。

## 客户验证的成效

已有超过 300 家客户使用了默认仓库，其价值清晰且一致：

- **有效降低探索性查询成本**：在管理员将默认仓库设置为较小仓库的工作区中，目录浏览器查询流向较小仓库的比例从 **77% 提高到了 96%**。
- **有助于减少手动选择仓库的需求**：跨多个仓库运行临时 SQL 的用户数量减少了 **15%**。用户现在可以专注于分析，而不是计算资源的选择。

客户已经在生产工作负载中看到了实际成效。

## 功能详情

### 1. 管理员的工作区级别默认设置

管理员可以在“工作区设置” → “计算”中配置一个默认 SQL 仓库。

- 适用于所有临时 SQL 界面
- 支持无服务器、专业版和经典版 SQL 仓库，并遵守现有的治理和访问控制
- 选择加入（未设置工作区级别默认值时采用“最后选择”）
- 在新资产中自动选择

![compute level default warehouse](/images/posts/4eaf778f6c53.gif)

### 2. 用户级别自定义以实现灵活性

用户可以在“仓库下拉菜单” -> “自定义您的默认仓库”中为自己配置覆盖设置：

- 查看工作区默认仓库（截图中为“alp-sql-controltower”）
- 选择退出（如果未设置覆盖，则遵循工作区级别默认值）
- 将其覆盖为另一个仓库，或者如果愿意，选择“最后选择”

![user level default warehouse](/images/posts/a4b1e93ad7a9.gif)

### 3. 用于自定义和治理的管理员 API

为了使管理员能够为每个用户分配不同的仓库，我们添加了用于查看和设置用户级别默认值的 API。这使管理员能够：

- 根据用户所属团队，以编程方式为每个用户设置不同的仓库
- 审计哪些用户设置了用户级别覆盖
- 对每个用户的默认仓库选择拥有最终控制权

示例 1：将“财务”组中所有用户的默认仓库设置为

示例 2：审计所有已设置自己默认仓库的用户

完整的 API 参考，请查阅 [Databricks 文档](https://docs.databricks.com)。

此 API 也可作为 [Terraform 资源](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/sql_user_default_warehouse) 使用。

## 下一步计划

我们正在扩展默认仓库功能，以支持 Databricks UI 之外的临时工作负载，包括来自 MLflow、Lakeflow CLI 和 DBSQL MCP 等平台外来源的工作负载。

请告诉我们您希望接下来看到什么功能，以便让您的 Databricks SQL 管理体验更上一层楼！

## 立即试用默认仓库

为了保护关键工作负载的性能并减少意外成本，请使用默认仓库将临时查询引导至正确的仓库。默认仓库现已全面推出。要开始使用，请参阅 [Databricks 文档](https://docs.databricks.com)。

---

> 本文由AI自动翻译，原文链接：[Protect Performance and Reduce Surprise Costs with Default Warehouse](https://www.databricks.com/blog/protect-performance-and-reduce-surprise-costs-default-warehouse)
> 
> 翻译时间：2026-03-31 05:06
