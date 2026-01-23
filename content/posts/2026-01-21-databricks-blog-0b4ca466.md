---
title: 北极星数据湖：面向PB级数据的液态集群架构
title_original: Arctic Wolf’s Liquid Clustering Architecture Tuned for Petabyte Scale
date: '2026-01-21'
source: Databricks Blog
source_url: https://www.databricks.com/blog/arctic-wolfs-liquid-clustering-architecture-tuned-petabyte-scale
author: ''
summary: 本文介绍了Databricks平台如何通过其Lakehouse架构，为北极星（Arctic Wolf）等企业提供支持PB级数据处理能力的液态集群架构。文章重点阐述了该统一平台在数据管理、数据工程、人工智能、数据科学及商业智能等核心领域的集成能力，并展示了其跨行业解决方案与合作伙伴生态。该架构旨在实现数据可靠性、安全共享与高性能分析，帮助企业构建和部署大规模数据与AI应用。
categories:
- AI基础设施
tags:
- 数据湖
- 集群架构
- 大数据
- Databricks
- 数据工程
draft: false
translated_at: '2026-01-23T04:45:24.477936'
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
            接入数据消费者生态系统
        合作伙伴解决方案
            寻找定制化行业与迁移解决方案
        Built on Databricks
            构建、推广和发展您的业务

-   产品
    Databricks 平台
        平台概览
            面向数据、分析和 AI 的统一平台
        数据管理
            数据可靠性、安全性与性能
        共享
            面向所有数据的开放、安全、零拷贝共享
        数据仓库
            用于 SQL 分析的无服务器数据仓库
        治理
            面向所有数据、分析和 AI 资产的统一治理
        数据工程
            批处理和流式数据的 ETL 与编排
        人工智能
            构建和部署机器学习与生成式 AI 应用
        数据科学
            大规模协作式数据科学
        商业智能
            面向真实世界数据的智能分析
        应用开发
            快速构建安全的数据与 AI 应用
        数据库
            用于数据应用和 AI Agent（智能体）的 Postgres
    集成与数据
        市场
            面向数据、分析和 AI 的开放市场
        IDE 集成
            在您喜爱的 IDE 中基于 Lakehouse 进行构建
        Partner Connect
            探索并与 Databricks 生态系统集成
    定价
        Databricks 定价
            探索产品定价、DBU 等
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
        Free Edition
            免费学习专业的数据与 AI 工具
        University Alliance
            想要教授 Databricks？了解详情。
    活动
        Data + AI Summit
        Data + AI World Tour
        AI Days
        活动日历
    博客与播客
        Databricks 博客
            探索新闻、产品公告等
        Databricks Mosaic 研究博客
            发现我们生成式 AI 研究的最新进展
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

- 面向行业的Databricks通信媒体与娱乐金融服务公共部门医疗保健与生命科学零售制造业查看所有行业跨行业解决方案AI Agents（智能体）网络安全营销迁移与部署数据迁移专业服务解决方案加速器探索加速器加速实现关键成果

- 面向行业的Databricks通信媒体与娱乐金融服务公共部门医疗保健与生命科学零售制造业查看所有行业
- 跨行业解决方案AI Agents（智能体）网络安全营销
- 迁移与部署数据迁移专业服务
- 解决方案加速器探索加速器加速实现关键成果

- 通信
- 媒体与娱乐
- 金融服务
- 公共部门
- 医疗保健与生命科学
- 零售
- 制造业
- 查看所有行业

- AI Agents（智能体）
- 网络安全
- 营销

- 数据迁移
- 专业服务

- 探索加速器加速实现关键成果

- 
- 学习培训发现满足您需求的定制课程Databricks Academy登录Databricks学习平台认证获得认可与区分免费版免费学习专业数据与AI工具大学联盟想教授Databricks？了解详情。
- 活动Data + AI 峰会Data + AI 全球巡演AI 日活动日历
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
- AI 日
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

- 
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
- 获取演示

- 登录
- 联系我们
- 试用Databricks

1.  博客
2.  /行业
3.  /文章

# Arctic Wolf 为 PB 级规模优化的液态集群架构

![Arctic Wolf 的液态集群架构为 PB 级规模优化](/images/posts/0db8afe349bf.png)

![Arctic Wolf 的液态集群架构为 PB 级规模优化](/images/posts/0db8afe349bf.png)

![Arctic Wolf 的液态集群架构为 PB 级规模优化](/images/posts/0db8afe349bf.png)

发布日期：2026年1月21日

作者：Justin Lai, Rajneesh Arora, Krishan Kumar 和 Cindy Jiang


-   Arctic Wolf 每天处理超过 1 万亿个安全事件，生成超过 2600 亿条丰富的观测数据，这些数据保存在 PB 级的 Delta Lake 中。我们的架构旨在提供对这些数据的近实时访问。
-   我们最近迁移到在 Unity Catalog 托管表上使用液态集群，并结合预测性优化（PO），为我们分区的外部表补充了增量、工作负载感知的集群功能，以获得更好的查询性能。
-   液态集群和 PO 共同作用，使表保持优化状态，查询速度提升高达 8 倍，并将数据新鲜度从数小时缩短到数分钟。

每天，Arctic Wolf 处理超过一万亿个事件，将数十亿条丰富的记录提炼成与安全相关的洞察。这相当于超过 60 TB 的压缩遥测数据，为 AI 驱动的威胁检测和响应提供动力——7x24 小时不间断。为了支持实时威胁狩猎，我们需要这些数据能够尽快提供给客户和安全运营中心，目标是大多数查询在 15 秒内返回。

历史上，我们不得不利用其他快速数据存储来提供对近期数据的访问，因为分区 + Z 排序无法跟上需求。当我们检测到可疑活动时，我们的团队可以立即在三个月的历史上下文中进行切换，以了解攻击模式、横向移动和完整的入侵范围。这种针对超过 3.8 PB 压缩数据的实时历史分析在现代威胁狩猎中至关重要：将入侵控制在数小时而非数天之内，可能意味着防止数百万美元的损失。

当每一秒都至关重要时，速度和新鲜度就变得非常重要。Arctic Wolf 需要加速对海量数据集的访问，同时不推高数据摄取成本或增加复杂性。挑战是什么？调查因繁重的文件 I/O 和过时数据而变慢。通过重新思考数据组织方式，我们的架构有效地管理了多租户数据倾斜（少数客户产生了大部分事件），同时也适应了可能在初始摄取后数周才到达的延迟数据。可衡量的收益包括将文件数量从 400 万以上减少到 200 万，各百分位的查询时间缩短了约 50%，并将 90 天查询从 51 秒减少到仅 6.6 秒。数据新鲜度从数小时提高到数分钟，使得几乎可以立即访问安全遥测数据。

请继续阅读，了解液态集群和 Unity Catalog 托管表如何使之成为可能——在大规模下提供一致的性能和近实时洞察。

## 遗留瓶颈：Arctic Wolf 为何重建

我们遗留的表按发生日期-小时分区并按租户标识符进行 Z 排序，由于分区中存在大量小文件，无法进行近实时查询。此外，数据在最近 24 小时之外才可用，因为我们必须先运行带有 Z 排序的 OPTIMIZE 操作，然后才能查询数据。

即便如此，由于延迟到达的数据，性能问题仍然存在。当系统在传输数据之前离线时，就会发生这种情况，这会导致新数据落入旧分区并影响性能。

陈旧的数据会蒙蔽我们的双眼。这种延迟，是遏制对手与放任其横向移动之间的关键区别。

为缓解这些性能挑战并提供所需的数据新鲜度，我们曾将热数据复制到数据加速器中，并与数据湖的数据混合查询以满足业务需求。该系统运行成本高昂，且需要大量工程投入来维护。为解决使用数据加速器带来的这些挑战，我们重新设计了数据布局，以实现数据均匀分布并支持延迟到达的数据。这优化了查询性能，并为当前及新兴的Agent（智能体）AI应用场景提供了近实时访问能力。

## 利用液态聚类构建流数据基础

通过新架构，我们的核心目标是能够查询最新数据，在不同规模的客户间提供一致的查询性能，同时确保查询在数秒内返回。

![medallion architecture](/images/posts/c7ad54d47228.png)

重新设计的流水线遵循奖牌（medallion）架构，首先通过Kafka持续将原始事件数据摄取到青铜层。随后，每小时运行的结构化流作业会扁平化嵌套的JSON负载，并使用液态聚类写入白银表，形成主要的分析基础。在此，从青铜到白银的转换处理模式演进、生成派生的时间列，并为具有严格延迟SLA的下游分析工作负载准备数据。

液态聚类取代了僵化的分区方案，采用与查询模式（具体包括租户标识符、日期粒度、表大小和数据到达特征）对齐的、基于工作负载感知的多维聚类键。这使得数据分布更加均匀，在我们的实例中，平均文件大小增加到超过1GB，从而显著减少了针对我们表的典型时间窗口查询期间需要扫描的文件数量。

## 深入探讨：写入时聚类

此外，我们的结构化流作业利用写入时聚类功能，在新数据到达时维护文件布局。其功能类似于局部OPTIMIZE操作，仅对新摄取的数据应用聚类。因此，摄取的数据已经是优化过的。然而，如果摄取批次过小，会产生许多虽聚类良好但体积很小的文件，这些文件仍需要在全局OPTIMIZE期间进行聚类，以实现理想的数据布局。相反，如果摄取时的批次大小接近全局OPTIMIZE所需的批次大小，则通常不需要额外的优化。

对于摄取海量数据（例如TB级）的工作负载，我们建议在源头进行批处理，例如使用带有`maxBytesPerTrigger`的`foreachBatch`，以确保高效的聚类和文件布局。通过`maxBytesPerTrigger`，我们可以控制批次大小，消除许多需要通过OPTIMIZE操作进行协调的微小聚类"孤岛"。通过使用接近OPTIMIZE操作处理的大小，我们能够创建最优批次，从而减少OPTIMIZE进一步所需的工作量。

## 对Arctic Wolf安全分析的影响

Arctic Wolf迁移到液态聚类在性能、数据新鲜度和运营效率方面带来了显著的可量化改进。带有预测性优化的Unity Catalog托管表也减少了对计划性维护的需求。

文件数量从400万以上降至200万，在保持良好聚类质量的同时，最小化了查询期间的文件I/O。因此，查询性能大幅提升，使安全分析师能够更快地调查事件：在百分位数上**提速约50%**，对我们大量客户**提速约90%**，90天查询时间从**51秒降至6.6秒**。

通过实施写入时聚类，我们将数据新鲜度从小时级提升到分钟级，将洞察时间**加速了约90%**。这一改进使得Arctic Wolf数据湖能够实现**近实时威胁检测**。

转向液态聚类和Unity Catalog托管表，消除了遗留的分区方案，减少了技术债务，并解锁了先进的治理和性能特性。凭借能够每日处理和查询**超过2600亿行**数据的架构，我们为来自所有这些来源的关键安全数据提供了更快、更高效的访问。结合我们7x24小时的Concierge Security®团队和实时威胁检测，这实现了更快速、更准确的威胁响应和缓解。这些差异化优势帮助我们的**客户**建立更强大、更敏捷的安全态势，并对Arctic Wolf保护其环境和支持业务持续成功的能力更有信心。


## 不错过任何Databricks文章

![siem-blog-og](/images/posts/5e5f35b12bae.png)

![siem-blog-og](/images/posts/5e5f35b12bae.png)

![siem-blog-og](/images/posts/5e5f35b12bae.png)

2022年2月4日 / 8分钟阅读

#### OMB M-21-31：使用Databricks满足并超越传统SIEM的一种经济高效的替代方案

![Announcing the General Availability of AWS GovCloud with FedRAMP High and Department of Defense IL5 Authorization](/images/posts/8401e3916806.png)

![Announcing the General Availability of AWS GovCloud with FedRAMP High and Department of Defense IL5 Authorization](/images/posts/8401e3916806.png)

![Announcing the General Availability of AWS GovCloud with FedRAMP High and Department of Defense IL5 Authorization](/images/posts/8401e3916806.png)

2024年4月30日 / 4分钟阅读

#### 宣布AWS GovCloud（具有FedRAMP High和美国国防部IL5授权）全面上市

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

- 面向高管
- 面向初创公司
- 湖仓一体架构
- Mosaic研究

- 客户案例

- 云提供商
- 技术合作伙伴
- 数据合作伙伴
- 基于Databricks构建
- 咨询与系统集成商
- C&SI合作伙伴计划
- 合作伙伴解决方案

- 面向高管
- 面向初创公司
- 湖仓一体架构
- Mosaic研究

- 客户案例

- 云提供商
- 技术合作伙伴
- 数据合作伙伴
- 基于Databricks构建
- 咨询与系统集成商
- C&SI合作伙伴计划
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
- IDE集成
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
- IDE集成
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
- Databricks学院登录

- Data + AI峰会
- Data + AI全球巡展
- AI日
- 活动日历

- Databricks博客
- Databricks Mosaic研究博客
- Data Brew播客
- 数据与AI冠军播客

- 培训
- 认证
- 免费版
- 大学联盟
- Databricks学院登录

- Data + AI峰会
- Data + AI全球巡展
- AI日
- 活动日历

- Databricks博客
- Databricks Mosaic研究博客
- Data Brew播客
- 数据与AI冠军播客

- 关于我们
- 我们的团队
- Databricks Ventures
- 联系我们

- 开放职位
- 在Databricks工作

- 奖项与认可
- 新闻中心

- 关于我们
- 我们的团队
- Databricks Ventures
- 联系我们

- 开放职位
- 在Databricks工作

- 奖项与认可
- 新闻中心

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

Databricks Inc.
160 Spear Street, 15th Floor
San Francisco, CA 94105
1-866-330-0121


查看 Databricks 的招聘职位


- 隐私声明
- |使用条款
- |现代奴隶制声明
- |加州隐私
- |您的隐私选择

---

> 本文由AI自动翻译，原文链接：[Arctic Wolf’s Liquid Clustering Architecture Tuned for Petabyte Scale](https://www.databricks.com/blog/arctic-wolfs-liquid-clustering-architecture-tuned-petabyte-scale)
> 
> 翻译时间：2026-01-23 04:45
