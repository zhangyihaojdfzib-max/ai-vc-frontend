---
title: Databricks推出Google Sheets连接器：在表格中实时获取湖仓受控数据
title_original: 'Introducing the Databricks Connector for Google Sheets: Real-Time,
  Governed Lakehouse Data in the Sheets Users Love'
date: '2026-04-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-databricks-connector-google-sheets-real-time-governed-lakehouse-data-sheets-users
author: ''
summary: 本文介绍了Databricks新推出的Google Sheets连接器，旨在解决企业用户在电子表格中工作与可信数据存储在湖仓平台之间的割裂问题。该连接器允许用户直接在Google
  Sheets中实时查询和刷新由Unity Catalog管控的Databricks数据，无需导出CSV文件，从而确保数据的一致性和实时性。它通过无代码界面或SQL查询，支持定时刷新，在赋能业务用户使用熟悉工具的同时，保持了数据治理与安全。文章以Nubank为例说明了其应用价值，并提供了快速入门指南。
categories:
- AI产品
tags:
- Databricks
- Google Sheets
- 数据湖仓
- 数据治理
- 实时分析
draft: false
translated_at: '2026-04-17T04:55:14.270193'
---

企业运营离不开电子表格。每天，商业用户都在Google Sheets中进行规划、分析和报告。然而，最准确且受管控的业务数据日益集中于湖仓平台，这导致了数据驱动决策的发生地与可信数据存储地之间的割裂。

Databricks for Google Sheets连接器通过将受管控的实时Databricks数据直接融入用户熟悉的Sheets环境，成功弥合了这一鸿沟。该连接器基于Databricks SQL和Unity Catalog的性能与安全性构建，使团队能够直接在Sheets中大规模探索、分析真实数据并开展协作，无需再依赖CSV文件导出。

## 过往挑战：CSV文件、数据副本与指标冲突

此前，将受管控数据接入Sheets只能通过CSV导出、快照或定制化管道实现，这些方式均会迅速导致数据不同步，并耗费分析师大量宝贵时间。业务团队在孤立的数据副本上工作，而数据团队则疲于维护数据治理与一致性。

其结果是决策速度放缓、指标口径不一，以及数据团队陷入处理零散数据请求的困境。

## 全新可能：Sheets中实时受管控的Databricks数据

Databricks for Google Sheets连接器改变了这一现状，它将Sheets转变为通往湖仓的实时窗口。用户无需导出数据快照，即可将Sheets直接连接至Databricks SQL，对Unity Catalog管控的数据运行查询，并按需刷新结果。

通过该连接器，团队能够：

- 通过无代码图形界面或SQL，在Sheets中查询受管控数据集（如Unity Catalog指标视图），所有权限均由Unity Catalog自动管理。

![轻松从Google Sheets查询Databricks数据集](/images/posts/fd54044404f1.gif)

- 设置定时刷新或手动更新数据，确保表格始终反映最新信息

![](/images/posts/4a39fc425cc0.gif)

这使得数据管理者能够在保持严格治理的同时，赋能业务用户在其偏好的生产力工具中开展工作。

## 客户聚焦：Nubank在Google Sheets中实现数据民主化

全球领先的数字银行平台Nubank将Databricks作为其湖仓架构的核心。随着公司规模扩大，数据团队需要在不牺牲管控的前提下，将受管控的高质量数据更贴近业务决策者。

Databricks中的受管控数据与Sheets中的灵活分析相结合，帮助Nubank在赋能各团队就地工作的同时，保持了强大的数据文化。

## 快速入门：简易设置，全员可用

Databricks for Google Sheets连接器现已面向所有Databricks客户正式发布。要开始使用，请打开Google Marketplace并安装“Databricks Connector for Google Sheets”。随后在Google Sheets中通过“扩展程序”菜单访问该连接器。

更多详情请查阅我们的技术文档。

## 正在寻找新的数据仓库？试试Databricks SQL

最好的数据仓库就是湖仓！要了解更多关于Databricks SQL的信息，请访问产品页面或阅读文档。如果您希望将数据仓库迁移至具备卓越用户体验、更低总成本的高性能无服务器湖仓，Databricks SQL正是您需要的解决方案——立即免费试用。

---

> 本文由AI自动翻译，原文链接：[Introducing the Databricks Connector for Google Sheets: Real-Time, Governed Lakehouse Data in the Sheets Users Love](https://www.databricks.com/blog/introducing-databricks-connector-google-sheets-real-time-governed-lakehouse-data-sheets-users)
> 
> 翻译时间：2026-04-17 04:55
