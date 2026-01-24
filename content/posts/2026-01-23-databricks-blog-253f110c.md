---
title: Databricks Delta Sharing 宣布原生支持 Iceberg 格式
title_original: Announcing first-class support of Iceberg format in Databricks Delta
  Sharing
date: '2026-01-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-first-class-support-iceberg-format-databricks-delta-sharing
author: ''
summary: Databricks 宣布在其 Delta Sharing 数据共享服务中提供对 Apache Iceberg 格式的一流支持。此举旨在进一步推动数据湖仓的开放性和互操作性，允许用户更灵活、安全地跨平台共享
  Iceberg 表格式的数据，无需数据移动或复制。这加强了 Databricks Lakehouse 平台对开放标准的承诺，并为企业提供了在混合多云环境中统一数据管理和分析的新能力。
categories:
- AI基础设施
tags:
- Databricks
- Iceberg
- 数据湖仓
- 数据共享
- Delta Sharing
draft: false
translated_at: '2026-01-24T04:33:25.685428'
---

-   为何选择 Databricks
    探索
        面向高管
        面向初创企业
        Lakehouse 架构
        Mosaic 研究
    客户
        客户案例
    合作伙伴
        云服务提供商
            Databricks on AWS, Azure, GCP, and SAP
        咨询与系统集成商
            构建、部署和迁移至 Databricks 的专家
        技术合作伙伴
            将您现有工具连接到您的 Lakehouse
        C&SI 合作伙伴计划
            构建、部署或迁移至 Lakehouse
        数据合作伙伴
            接入数据消费者的生态系统
        合作伙伴解决方案
            寻找定制行业与迁移解决方案
        Built on Databricks
            构建、营销和发展您的业务

-   产品
    Databricks 平台
        平台概览
            面向数据、分析和 AI 的统一平台
        数据管理
            数据可靠性、安全性和性能
        共享
            面向所有数据的开放、安全、零拷贝共享
        数据仓库
            用于 SQL 分析的无服务器数据仓库
        治理
            面向所有数据、分析和 AI 资产的统一治理
        数据工程
            批处理和流式数据的 ETL 与编排
        人工智能
            构建和部署 ML 与 GenAI 应用
        数据科学
            大规模协作式数据科学
        商业智能
            面向真实世界数据的智能分析
        应用开发
            快速构建安全的数据和 AI 应用
        数据库
            用于数据应用和 AI Agent（智能体）的 Postgres
    集成与数据
        市场
            面向数据、分析和 AI 的开放市场
        IDE 集成
            在您喜爱的 IDE 中基于 Lakehouse 进行构建
        Partner Connect
            发现并与 Databricks 生态系统集成
    定价
        Databricks 定价
            探索产品定价、DBU 等更多信息
        成本计算器
            估算您在任意云上的计算成本
    开源
        开源技术
            深入了解平台背后的创新

-   解决方案
    面向行业的 Databricks
        通信
        媒体与娱乐
        金融服务
        公共部门
        医疗保健与生命科学
        零售
        制造业
        查看所有行业
    跨行业解决方案
        AI Agent（智能体）
        网络安全
        营销
        迁移与部署
            数据迁移
            专业服务
        解决方案加速器
            探索加速器
            更快地实现重要成果

-   资源
    学习
        培训
            发现为您量身定制的课程
        Databricks Academy
            登录 Databricks 学习平台
        认证
            获得认可与差异化优势
        免费版
            免费学习专业的数据和 AI 工具
        University Alliance
            想要教授 Databricks？了解详情。
    活动
        Data + AI Summit
        Data + AI World Tour
        AI Days
        活动日历
    博客与播客
        Databricks 博客
            探索新闻、产品公告等更多内容
        Databricks Mosaic 研究博客
            发现我们 Gen AI 研究的最新进展
        Data Brew 播客
            让我们聊聊数据！
        Champions of Data + AI 播客
            来自推动创新的数据领导者的见解
    获取帮助
        客户支持
        文档
        社区
    深入探索
        资源中心
        演示中心
        架构中心

-   关于
    公司
        我们是谁
        我们的团队
        Databricks Ventures
        联系我们
    职业
        在 Databricks 工作
        开放职位
    新闻
        奖项与认可
        新闻中心
    安全与信任
        安全与信任

- 面向行业的Databricks通信媒体与娱乐金融服务公共部门医疗与生命科学零售制造业查看所有行业跨行业解决方案AI Agents（智能体）网络安全营销迁移与部署数据迁移专业服务解决方案加速器探索加速器更快实现关键成果

- 面向行业的Databricks通信媒体与娱乐金融服务公共部门医疗与生命科学零售制造业查看所有行业
- 跨行业解决方案AI Agents（智能体）网络安全营销
- 迁移与部署数据迁移专业服务
- 解决方案加速器探索加速器更快实现关键成果

- 通信
- 媒体与娱乐
- 金融服务
- 公共部门
- 医疗与生命科学
- 零售
- 制造业
- 查看所有行业

- AI Agents（智能体）
- 网络安全
- 营销

- 数据迁移
- 专业服务

- 探索加速器更快实现关键成果

- 学习培训发现满足您需求的定制课程Databricks Academy登录Databricks学习平台认证获得认可与区分免费版免费学习专业数据与AI工具大学联盟想教授Databricks？了解详情。活动Data + AI 峰会Data + AI 全球巡演AI Days活动日历博客与播客Databricks 博客探索新闻、产品公告等Databricks Mosaic 研究博客发现我们生成式AI研究的最新进展Data Brew 播客让我们聊聊数据！Champions of Data + AI 播客来自推动创新的数据领导者的洞见获取帮助客户支持文档社区深入探索资源中心演示中心架构中心

- 学习培训发现满足您需求的定制课程Databricks Academy登录Databricks学习平台认证获得认可与区分免费版免费学习专业数据与AI工具大学联盟想教授Databricks？了解详情。
- 活动Data + AI 峰会Data + AI 全球巡演AI Days活动日历
- 博客与播客Databricks 博客探索新闻、产品公告等Databricks Mosaic 研究博客发现我们生成式AI研究的最新进展Data Brew 播客让我们聊聊数据！Champions of Data + AI 播客来自推动创新的数据领导者的洞见
- 获取帮助客户支持文档社区
- 深入探索资源中心演示中心架构中心

- 培训发现满足您需求的定制课程
- Databricks Academy登录Databricks学习平台
- 认证获得认可与区分
- 免费版免费学习专业数据与AI工具
- 大学联盟想教授Databricks？了解详情。

- Data + AI 峰会
- Data + AI 全球巡演
- AI Days
- 活动日历

- Databricks 博客探索新闻、产品公告等
- Databricks Mosaic 研究博客发现我们生成式AI研究的最新进展
- Data Brew 播客让我们聊聊数据！
- Champions of Data + AI 播客来自推动创新的数据领导者的洞见

- 客户支持
- 文档
- 社区

- 资源中心
- 演示中心
- 架构中心

- 公司关于我们我们的团队Databricks Ventures联系我们职业发展在Databricks工作开放职位新闻奖项与认可新闻中心安全与信任安全与信任

- 公司关于我们我们的团队Databricks Ventures联系我们
- 职业发展在Databricks工作开放职位
- 新闻奖项与认可新闻中心
- 安全与信任安全与信任

- 关于我们
- 我们的团队
- Databricks Ventures
- 联系我们

- 在Databricks工作
- 开放职位

- 奖项与认可
- 新闻中心

- 安全与信任

- 准备开始了吗？
- 预约演示

- 登录
- 联系我们
- 试用Databricks

1. 博客
2. /公告
3. /文章

# 宣布在Databricks Delta Sharing中提供对Iceberg格式的一流支持

## 数据接收方现可在任何兼容Iceberg的客户端中使用Delta Shares；数据提供方可从外部目录Delta Share任何Iceberg表

![宣布在Delta Sharing协议中提供对Iceberg格式的一流支持](/images/posts/353456993e3a.png)

![宣布在Delta Sharing协议中提供对Iceberg格式的一流支持](/images/posts/353456993e3a.png)

![宣布在Delta Sharing协议中提供对Iceberg格式的一流支持](/images/posts/353456993e3a.png)

发布日期：2026年1月23日

作者：Tia Chang, Qinghao Wu 和 Harish Gaur

- 
- 
- 

Iceberg客户现在可以受益于Delta Sharing的高级共享功能，包括视图共享和无密钥认证。从Databricks安全地共享到任何支持Apache Iceberg REST Catalog API的客户端，包括Snowflake、Trino、Flink、Spark等。您可以从任何外部目录引入Iceberg表，通过Databricks和Unity Catalog进行管理，然后共享给任何接收方。

- Iceberg客户现在可以受益于Delta Sharing的高级共享功能，包括视图共享和无密钥认证。
- 从Databricks安全地共享到任何支持Apache Iceberg REST Catalog API的客户端，包括Snowflake、Trino、Flink、Spark等。
- 您可以从任何外部目录引入Iceberg表，通过Databricks和Unity Catalog进行管理，然后共享给任何接收方。

Delta Sharing连续两年实现超过300%的同比增长，是应用最广泛的数据与AI共享开放协议。包括SAP、Walmart、Atlassian和LSEG在内的主要数据提供商都使用Delta Sharing跨云和跨平台与合作伙伴及客户共享数据。今天，我们很高兴地宣布，Databricks Delta Sharing为Apache Iceberg格式提供了一流支持。

数据提供方现在可以安全、实时地从Databricks向任何支持Apache Iceberg REST Catalog API的客户端共享数据。Snowflake、Trino、Flink以及所有云上的Spark等平台的接收方都可以使用此功能——这进一步丰富了Delta Sharing的开放生态系统。

此外，我们正在启动一项私人预览，使数据提供方能够使用Delta Sharing来共享由Databricks外部目录（包括AWS Glue、Hive Metastore、Snowflake Horizon等）管理的Iceberg表。

![图1：为开放生态系统统一共享与协作的格式](/images/posts/f40f03118139.png)

![图1：为开放生态系统统一共享与协作的格式](/images/posts/f40f03118139.png)

总之，您可以共享任何新的或现有的表（Delta或Iceberg，托管或外部）。这为实现完全开放的互操作性奠定了基础。您可以从任何外部目录引入Iceberg表，通过Databricks和Unity Catalog进行管理，然后共享给任何接收方——无论他们使用的是Databricks、Iceberg客户端还是Delta客户端。这使您能够利用Unity Catalog作为统一的数据治理层，为所有共享提供一个集中管理点。

在这篇博客文章中，我们将解释开放数据共享为何重要。我们还将通过实际操作演示，深入探讨Delta Sharing如何与Iceberg客户端协同工作。

为何重要：开放共享与封闭共享

大多数数据共享解决方案并非真正的共享——它们是陷阱。它们在本质上是封闭的，旨在确保供应商锁定，因此您只能与已经在其封闭生态系统内的其他方共享。这限制了您的选择，扼杀了创新，并导致了大量无意义的数据复制。

Delta Sharing是应用最广泛的开放安全数据共享标准。它被各领域的领先数据提供商所采用，旨在支持不同的云和平台。Delta Sharing遵循三个核心原则：

- 共享任何资产。
- 与任何人共享。
- 无摩擦地共享。

增加对 Iceberg 客户端的支持强化了这一承诺。它允许您共享 Delta 表，而接收方体验到的却是原生的 Iceberg 表。共享通过 Iceberg REST API 进行，因此接收方可以从任何兼容 Iceberg 的平台进行连接。这使您能够兼收两者之利：数据提供方受益于 Delta Sharing 的高级功能（例如视图共享），而接收方则通过 Iceberg REST API 获得原生 Iceberg 表。

![图 2：直接将数据共享给兼容 Iceberg 的工具](/images/posts/09def78f091d.png)

![图 2：直接将数据共享给兼容 Iceberg 的工具](/images/posts/09def78f091d.png)

接收方能够安全、实时地访问源数据。这消除了数据孤岛，使您可以与任何人开放地共享数据。

此功能非常适合需要使用 Iceberg 客户端（例如运行在 Snowflake 上或与 Trino、Flink 或 Spark 等平台集成的客户端）与合作伙伴和客户进行外部数据共享的组织。在多个平台上运营的多个业务部门也能从中受益，它能在多云或混合环境中实现无缝、双向的数据交换。已采用这些模式的行业包括医疗保健、零售、金融、广告技术等。

## 互操作性：既是源头也是目的地

因为我们坚信完全开放的数据访问，所以我们并不止步于向 Iceberg 客户端共享数据。我们正在开发下一阶段的演进：共享位于外部目录（如 AWS Glue 或 Snowflake Horizon）中的外部 Iceberg 表。我们很高兴地宣布，支持共享外部 Iceberg 表的 Delta Sharing 功能现已开启私密预览。

您可能会问：如果 Iceberg 表位于 AWS Glue 或 Snowflake 中，为什么要通过 Delta Sharing 来共享它？为什么不直接从该平台内部共享呢？

首先，通过在 Unity Catalog 中编目您的外部 Iceberg 数据，您将在 Unity Catalog 中获得一个统一的治理层，从而能够全面了解并治理您的整个数据资产。此外，使用 Delta Sharing 可以让您兼收两者之利：您既能受益于 Delta Sharing 一流的共享功能，又能保持数据为 Iceberg 格式。例如，这包括能够通过 Delta Sharing 共享视图以实现细粒度访问控制，而这是 Iceberg IRC API 原生不支持的。

通过此私密预览，Databricks 湖仓平台实现了双向开放。您的湖仓平台可以与日益增长的 Iceberg 生态系统共享数据，也可以接收来自该生态系统的数据。

这种双重能力为您带来：

- **简单协作**：无论您使用哪种开放表格式（Delta 或 Iceberg），都能协同工作。
- **受控共享**：Unity Catalog 控制访问并提供审计日志。
- **最广泛覆盖**：既可以作为提供方，也可以作为接收方共享数据，打破平台壁垒。

设想您的公司 Provider Corp 使用 Databricks 和 Delta Lake 来管理客户数据。您需要与使用 Snowflake 并偏好 Iceberg 格式的合作伙伴 Partner Inc 安全地共享每日产品销售清单。

在此功能之前：Provider Corp 必须手动导出数据，将其转换为 Snowflake 可读的格式，上传到合作伙伴的云存储，并设置复杂的同步作业。这过程缓慢、成本高昂，涉及大量管理开销，并且存在数据过时的风险。

借助 Delta Sharing 向 Iceberg 客户端共享：

1.  Provider Corp 通过 UniForm 在销售数据上启用 Iceberg 读取（这可以包括托管和外部 Delta 表、视图、物化视图和流表），并通过 Delta Sharing 共享它。这提供了实时访问，无需复制或重新摄取。
2.  Partner Inc 在 Snowflake 中使用提供的凭据设置简单连接，通过短期持有者令牌进行安全身份验证。
3.  Partner Inc 的分析师可以立即使用标准 SQL 查询共享表，就像在 Snowflake 环境中处理原生 Iceberg 表一样。
4.  他们看到的数据始终是实时的（零拷贝），并且 Provider Corp 使用 Unity Catalog 进行审计和监控，保持了完全的安全性和治理。

这使得数据共享即时、安全且完全与格式无关。

请查看此演示，其中详细介绍了在 Snowflake 中共享和读取表的步骤。

1.  通过 Delta Sharing 共享表，为接收方生成凭据。
2.  接收方下载凭据文件，将其上传到激活链接页面，并生成 SQL。生成的 SQL 将包含所有必要的凭据，以及其 Iceberg 客户端（例如 Snowflake）所需的目录和表引用。
3.  完成后，接收方可以立即对实时共享数据运行查询，就像数据原生在其平台上一样——无需手动摄取或复制。

- 立即在产品中直接试用 Delta Sharing 到 Iceberg 客户端的公开预览——请参阅 Databricks 文档和工作区 UI 以获取指南和资源。
- 如果您有兴趣参与共享外部 Iceberg 表的私密预览，或想了解更多关于完整 Iceberg 互操作性的信息，请联系您的 Databricks 客户团队。

- 阅读 Delta Sharing 文档以开始使用 Delta Sharing
- 观看 2025 年数据与人工智能峰会上关于 Delta Sharing 实践：架构与最佳实践的演讲
- 观看 2025 年数据与人工智能峰会上关于保障数据协作：深入探讨安全、框架和用例的演讲，以了解更多关于 Delta Sharing 安全、框架和用例的信息

## 不错过任何 Databricks 文章

![引入统计预测优化](/images/posts/ab77da589535.png)

![引入统计预测优化](/images/posts/ab77da589535.png)

![引入统计预测优化](/images/posts/ab77da589535.png)

2024年11月20日 / 4 分钟阅读

#### 引入统计预测优化

![如何在 AI/BI 仪表板中呈现和共享您的 Notebook 洞察](/images/posts/5cc2f5e4940f.png)

![如何在 AI/BI 仪表板中呈现和共享您的 Notebook 洞察](/images/posts/5cc2f5e4940f.png)

![如何在 AI/BI 仪表板中呈现和共享您的 Notebook 洞察](/images/posts/5cc2f5e4940f.png)

2024年11月21日 / 3 分钟阅读

#### 如何在 AI/BI 仪表板中呈现和共享您的 Notebook 洞察

![databricks 徽标](/images/posts/443a5359ee28.png)

![databricks 徽标](/images/posts/443a5359ee28.png)

![databricks 徽标](/images/posts/443a5359ee28.png)

- 面向高管
- 面向初创公司
- 湖仓架构
- Mosaic 研究

- 客户案例

- 云提供商
- 技术合作伙伴
- 数据合作伙伴
- 基于 Databricks 构建
- 咨询与系统集成商
- C&SI 合作伙伴计划
- 合作伙伴解决方案

- 面向高管
- 面向初创公司
- 湖仓架构
- Mosaic 研究

- 客户案例

- 云提供商
- 技术合作伙伴
- 数据合作伙伴
- 基于 Databricks 构建
- 咨询与系统集成商
- C&SI 合作伙伴计划
- 合作伙伴解决方案

- 平台概览
- 共享
- 治理
- 人工智能
- 商业智能
- 数据库
- 数据管理
- 数据仓库
- 数据工程
- 数据科学
- 应用开发

- 定价概览
- 定价计算器

- 市场
- IDE 集成
- 合作伙伴连接

- 平台概览
- 共享
- 治理
- 人工智能
- 商业智能
- 数据库
- 数据管理
- 数据仓库
- 数据工程
- 数据科学
- 应用开发

- 定价概览
- 定价计算器

- 市场
- IDE 集成
- 合作伙伴连接

- 通信
- 金融服务
- 医疗保健与生命科学
- 制造业
- 媒体与娱乐
- 公共部门
- 零售业
- 查看全部

- 网络安全
- 市场营销

- 通信
- 金融服务
- 医疗保健与生命科学
- 制造业
- 媒体与娱乐
- 公共部门
- 零售业
- 查看全部

- 网络安全
- 市场营销

- 培训
- 认证
- 免费版
- 大学联盟
- Databricks Academy 登录

- 数据与人工智能峰会
- 数据与人工智能全球巡展
- 人工智能日
- 活动日历

- Databricks 博客
- Databricks Mosaic 研究博客
- Data Brew 播客
- 数据与人工智能冠军播客

- 培训
- 认证
- 免费版
- 大学联盟
- Databricks 学院登录

- 数据与人工智能峰会
- 数据与人工智能全球巡展
- 人工智能日
- 活动日历

- Databricks 博客
- Databricks Mosaic 研究博客
- Data Brew 播客
- 数据与人工智能冠军播客

- 关于我们
- 我们的团队
- Databricks Ventures
- 联系我们

- 职位空缺
- 在 Databricks 工作

- 奖项与认可
- 新闻中心

- 关于我们
- 我们的团队
- Databricks Ventures
- 联系我们

- 职位空缺
- 在 Databricks 工作

- 奖项与认可
- 新闻中心

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

Databricks Inc.
160 Spear Street, 15th Floor
San Francisco, CA 94105
1-866-330-0121

- 
- 
- 
- 
- 
- 

查看 Databricks 的招聘职位

- 
- 
- 
- 
- 
- 

© Databricks 2026。保留所有权利。Apache、Apache Spark、Spark、Spark 徽标、Apache Iceberg、Iceberg 以及 Apache Iceberg 徽标均为 Apache 软件基金会的商标。

- 隐私声明
- |使用条款
- |现代奴隶制声明
- |加州隐私
- |您的隐私选择
-

---

> 本文由AI自动翻译，原文链接：[Announcing first-class support of Iceberg format in Databricks Delta Sharing](https://www.databricks.com/blog/announcing-first-class-support-iceberg-format-databricks-delta-sharing)
> 
> 翻译时间：2026-01-24 04:33
