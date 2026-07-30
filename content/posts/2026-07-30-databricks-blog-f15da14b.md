---
title: Genie Code Agentic转换器：专有SQL一键转ANSI
title_original: Convert proprietary code to open ANSI SQL with Genie Code
date: '2026-07-30'
source: Databricks Blog
source_url: https://www.databricks.com/blog/convert-proprietary-code-open-ansi-sql-genie-code
author: ''
summary: Databricks推出Genie Code的Agentic代码转换器，可将T-SQL、Snowflake等专有SQL方言自动转换为开放ANSI
  SQL。该工具通过迁移项目集中管理源文件、评估复杂度、生成血缘关系，并启动并行Agent集群迭代转换代码、验证语法与语义。支持多语句事务、临时表等企业级功能，大幅简化从传统数据仓库到Lakehouse的迁移流程，将复杂项目转变为配置、启动和监控的自动化任务。
categories:
- AI产品
tags:
- Databricks
- SQL转换
- Agentic代码转换
- 数据仓库迁移
- Genie Code
draft: false
translated_at: '2026-07-30T05:02:34.319270'
---

- 目前处于Beta阶段的Agentic代码转换器利用Genie Code将专有SQL转换为开放ANSI SQL，启动并行Agent集群迭代转换代码，并验证语法和语义意图。
- 在Databricks工作区中创建迁移项目，以跟踪进度、可视化血缘关系，并识别哪些对象需要一起迁移。
- 支持T-SQL、Snowflake、Redshift、Oracle、BigQuery和Teradata的SQL到SQL转换。

从传统数据仓库迁移是一项复杂的任务，需要团队分析数十年前的代码、转换专有方言、迁移海量数据集，并协调系统间的差异。Databricks通过Genie Code（Databricks的AI编码Agent）大幅简化了从传统数据仓库到Lakehouse的工作负载迁移。

我们很高兴宣布Genie Code中新增的Agentic转换器。该Agentic代码转换器可将专有方言转换为开放ANSI SQL，首批支持T-SQL、Snowflake、Redshift、Oracle、BigQuery和Teradata。它将数据仓库迁移从需要团队人员配置和管理的项目，转变为只需配置、启动和监控的项目。

## 自动化迁移规划

为了展示Agentic转换器的实际工作方式，我们将通过一个概念验证来演示如何将一组T-SQL存储过程转换为ANSI SQL。

要开始迁移，我们需创建一个**迁移项目**，这是Databricks工作区的新功能。迁移项目为团队提供了一个集中管理源文件、跟踪转换进度并在整个迁移过程中协作的中心枢纽。我们将项目命名为**Migration Project - POC**，将源方言设置为**T-SQL**，目标设置为**ANSI SQL**，并为转换后的文件选择一个目标文件夹。创建完成后，我们可以将之前上传到工作区的源SQL文件填充到项目中。每个文件都会在项目中显示其文件类型、代码行数和迁移状态：

![image6.gif](/images/posts/9124303723af.gif)

Genie Code会分析并评估每个文件的复杂度，并在右侧面板中展示评估结果。在我们的示例中，`mixed_5cats_sp_string_agg.sql`的复杂度评分较低，因为它仅包含能清晰映射到ANSI SQL的SQL特性。对于大规模迁移，团队可以利用复杂度评分来优先处理较简单的文件。

![image3.gif](/images/posts/278d067a1e9f.gif)

Genie Code还会生成血缘关系，映射传统环境中所有对象（表、视图和存储过程）之间的关联。血缘关系图显示`sps_sp_update_from.sql`和`sps_sp_pivot.sql`没有共享依赖关系，这意味着它们可以安全地独立迁移。

![image4.gif](/images/posts/e4c7fd3363e5.gif)

在大规模迁移中，复杂度和血缘关系为团队提供了清晰的视图，明确需要迁移什么、按什么顺序迁移，以及哪些对象需要一起迁移。

## 完全Agentic代码转换

分析完源代码后，我们可以开始转换代码。点击**运行**时，Genie Code会分析每个脚本的T-SQL，并启动子Agent集群并行转换文件。每个子Agent会迭代修复错误，验证语法和语义意图，确保转换后的代码保留原始业务逻辑并能成功解析。

完成后，转换后的文件会被写入目标文件夹，并根据状态进行颜色编码。在我们的概念验证中，8个文件中有6个成功转换。但`mixed_5cats_sp_string_agg.sql`和`mixed_6cats_sp_string_agg.sql`需要进一步审查。查看右侧面板，我们可以看到修复脚本所需的待办事项列表。Genie Code解释称，被标记的存储过程必须在Unity Catalog中使用三部分名称（catalog.schema.sp_string_agg）进行限定。

![image2.gif](/images/posts/ef131b6c6ba2.gif)

点击文件，我们可以打开原生SQL编辑器查看并排差异。我们可以在编辑器中手动修复，或者通过在Genie Code中创建**自定义技能**来编写转换规则。当我们准备运行完整迁移时，Genie Code会自动将规则（本例中为存储过程在Unity Catalog中使用三部分名称）应用于整个代码库。自定义技能也适用于更广泛的定制，例如遵循已批准的ETL模式或内部命名约定。

对于寻求“直接迁移”的团队，Databricks提供了全套企业级SQL功能。**多语句事务**、**临时表**和**存储过程**——这些传统数据仓库中常用的功能——在Databricks中均可使用，因此无需重新设计逻辑以适应新平台。

## 立即开始使用Agentic转换器

Agentic代码转换器是下一代数据仓库迁移工具，建立在Lakebridge大规模成功的基础上。自2025年数据和AI峰会发布以来，Lakebridge的转换工具已帮助超过一千名客户采用Databricks Lakehouse：

作为下一步，我们正在扩展Agentic转换器，以支持常见的传统ETL源和新的目标方言。我们还计划将数据迁移和验证纳入迁移项目体验中，通过原生Lakeflow Connect集成来迁移数据，并利用自动化工具在切换前验证迁移数据是否与源数据一致。

准备好迁移了吗？请联系您的Databricks客户团队评估您的传统环境，并在此处试用Agentic代码转换器。

---

> 本文由AI自动翻译，原文链接：[Convert proprietary code to open ANSI SQL with Genie Code](https://www.databricks.com/blog/convert-proprietary-code-open-ansi-sql-genie-code)
> 
> 翻译时间：2026-07-30 05:02
