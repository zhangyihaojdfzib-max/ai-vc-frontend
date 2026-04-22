---
title: Databricks推出Excel插件：业务用户轻松访问湖仓数据
title_original: Introducing the Databricks Excel Add-in for Business Users
date: '2026-04-21'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-databricks-excel-add-business-users
author: ''
summary: Databricks近日发布Excel插件公开预览版，旨在弥合湖仓一体平台与业务分析工具之间的鸿沟。该插件允许业务用户无需SQL知识或复杂配置，即可在熟悉的Excel环境中直接访问和分析受Unity
  Catalog治理的Databricks表与指标视图。通过简化数据访问流程、统一业务语义定义，它既提升了业务团队的分析效率与自主性，又确保了数据治理的一致性，有助于推动数据平台在组织内的普及与应用。
categories:
- AI产品
tags:
- Databricks
- Excel插件
- 数据分析
- 数据治理
- 湖仓一体
draft: false
translated_at: '2026-04-22T05:06:34.770414'
---

- **让Excel与您的湖仓一体平台协同工作**：通过简单、无代码的界面，在熟悉的工具中使用Databricks表和指标视图。
- **降低业务用户的使用门槛**：通过开箱即用的轻量级插件，跳过繁琐的手动驱动设置和复杂配置。
- **替代传统语义层**：通过Unity Catalog指标视图一次性定义业务指标，无需为服务Excel而维护独立工具。

电子表格始终是日常业务分析的支柱。财务团队在Excel中构建预测模型，运营团队追踪绩效数据，管理者依赖电子表格快速获取问题答案。

然而，最可信、最完整的业务数据正日益集中于湖仓一体平台。对许多组织而言，当前将这些数据与Excel连接的过程复杂脆弱，且业务用户难以独立操作。手动ODBC配置、多步骤设置指南以及持续的IT支持形成了使用阻力，拖慢了工作效率和平台采纳速度。数据重复和多语义层则带来了风险，并限制了实际能使用治理数据的人员范围。

最终导致：数据提取滞后、数据集重复、业务用户绕开数据平台开展工作，往往只能依赖传统BI工具或下游系统。

## 解决方案：在Excel中简单、受治理地访问Databricks数据

**Databricks Excel插件**正是为弥合这一差距而设计。该插件现已进入公开预览阶段，让业务用户无需编写SQL或配置ODBC驱动，即可直接从Excel导入和分析Databricks数据。

该插件基于**Databricks SQL**和**Unity Catalog**构建，将实时、受治理的湖仓数据与精心设计的业务语义融入用户熟悉的Excel环境。设置步骤从数十个手动操作简化为数次点击，极大降低了业务团队的使用门槛。

![展示如何设置Excel插件的简短动画](/images/posts/ef35d4c38370.gif)

关键在于，Excel插件支持**Unity Catalog指标视图**，让数据团队能够一次性定义业务语义，并在Excel及其他分析工作流中保持一致性。

通过Excel插件，用户可以：
- 通过点击式界面选择和筛选Databricks表及指标视图——无需SQL知识
- 基于受治理的湖仓数据创建原生Excel数据透视表
- 刷新数据以保持电子表格实时更新
- 跨工作簿访问Databricks工作区查询，确保定义一致性
- 可选地编写并保存SQL查询以供重复使用

这使得数据团队能够在保持严格治理的同时，支持业务用户在Excel中独立开展工作。

## 核心价值：业务语义+Excel改变游戏规则

对业务用户而言，价值立即可见：无需等待IT支持或学习新界面，就能在日常使用的工具中更快获取可信数据。

对数据领导者而言，Excel插件有助于：
- 在业务相关方间普及数据使用
- 通过Unity Catalog指标视图确保业务团队始终基于可信、最新的业务语义开展工作
- 执行Unity Catalog权限管理、数据血缘和治理策略
- 消除因电子表格和仪表板中逻辑重复导致的指标漂移
- 减轻数据从业者执行临时分析任务的负担，使其更专注于核心工作

这些优势共同使Databricks更自然地融入日常业务工作流。

## 实际应用场景

1. **数据团队定义数据资产**（如Unity Catalog指标视图）
   数据团队在Unity Catalog中创建受治理的指标视图，基于Databricks数据一次性标准化KPI和业务定义。
2. **集中管理治理与访问权限**
   通过Unity Catalog统一管理和配置权限控制，确保相应用户在完全合规的前提下查看对应指标。
3. **业务用户在Excel中直接分析数据**
   业务用户通过Databricks插件在Excel中访问这些指标，构建数据透视表并探索数据，无需重写逻辑或导出数据副本。

**成果**：基于统一的业务语义源和Excel无缝访问能力，实现更快速、更可靠的决策。这是普及湖仓一体平台的关键一步，将受治理的分析能力带入业务团队早已依赖的工具中。

## 当前功能与未来规划

公开预览版已支持业务用户的核心工作流：
- 选择Unity Catalog表和指标视图
- 执行带参数的自定义函数
- 手动刷新查询结果
- 创建Excel数据透视表及数据筛选
- 选择并复用现有Databricks工作区查询
- 切换工作区

即将推出的增强功能包括定时刷新、AI集成及更多可用性改进，以进一步优化使用体验。

## 开始使用

**Databricks Excel插件**已开放公开预览，可通过**Microsoft Office应用商店**安装，或从**Databricks文档**手动下载。管理员可通过Microsoft 365管理中心集中部署，个人用户（在获得适当权限后）可直接在网页版、Windows或macOS版Excel中安装。完成快速设置后，业务用户即可连接其Databricks工作区，立即开始使用受治理的湖仓数据。

---

> 本文由AI自动翻译，原文链接：[Introducing the Databricks Excel Add-in for Business Users](https://www.databricks.com/blog/introducing-databricks-excel-add-business-users)
> 
> 翻译时间：2026-04-22 05:06
