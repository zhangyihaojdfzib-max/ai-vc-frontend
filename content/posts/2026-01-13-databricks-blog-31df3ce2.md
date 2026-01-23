---
title: 开源Dicer：Databricks的自动分片器
title_original: 'Open Sourcing Dicer: Databricks’ Auto-Sharder'
date: '2026-01-13'
source: Databricks Blog
source_url: https://www.databricks.com/blog/open-sourcing-dicer-databricks-auto-sharder
author: ''
summary: 本文介绍了Databricks开源其内部工具Dicer（自动分片器）的背景与意义。Dicer旨在解决大规模数据处理中的自动数据分片与优化问题，提升数据湖仓一体架构的性能与可管理性。作为Databricks平台在数据管理、工程及AI应用领域的重要基础设施组件，其开源体现了公司对开放生态的承诺，并有助于社区共同推动数据与AI基础设施的技术演进。
categories:
- AI基础设施
tags:
- 数据分片
- 开源
- Databricks
- 数据湖仓
- 大数据处理
draft: false
translated_at: '2026-01-14T04:52:26.340980'
---

-  为何选择 Databricks
    探索
    面向高管
    面向初创企业
    湖仓一体架构
    Mosaic 研究
    客户
    客户案例
    合作伙伴
    云服务提供商
    Databricks 在 AWS、Azure、GCP 和 SAP 上的服务
    咨询与系统集成商
    构建、部署和迁移至 Databricks 的专家
    技术合作伙伴
    将现有工具连接至您的湖仓一体平台
    C&SI 合作伙伴计划
    构建、部署或迁移至湖仓一体平台
    数据合作伙伴
    接入数据消费者生态系统
    合作伙伴解决方案
    查找定制化行业与迁移解决方案
    基于 Databricks 构建
    构建、推广和发展您的业务

-   产品
    Databricks 平台
    平台概览
    数据、分析与 AI 的统一平台
    数据管理
    数据可靠性、安全性与性能
    共享
    面向所有数据的开放、安全、零拷贝共享
    数据仓库
    用于 SQL 分析的无服务器数据仓库
    治理
    面向所有数据、分析与 AI 资产的统一治理
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
    数据、分析与 AI 的开放市场
    IDE 集成
    在您喜爱的 IDE 中基于湖仓一体进行开发
    合作伙伴连接
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
    更快实现关键成果

-   资源
    学习
    培训
    发现为您量身定制的课程
    Databricks 学院
    登录 Databricks 学习平台
    认证
    获得认可与差异化优势
    免费版
    免费学习专业数据与 AI 工具
    大学联盟
    想要教授 Databricks？了解详情。
    活动
    Data + AI 峰会
    Data + AI 全球巡演
    数据智能日
    活动日历
    博客与播客
    Databricks 博客
    探索新闻、产品发布等
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
    职业发展
    在 Databricks 工作
    开放职位
    新闻
    奖项与认可
    新闻中心
    安全与信任
    安全与信任

-   探索
    面向高管
    面向初创企业
    湖仓一体架构
    Mosaic 研究

-   客户案例

-   合作伙伴
    云服务提供商
    Databricks 在 AWS、Azure、GCP 和 SAP 上的服务
    咨询与系统集成商
    构建、部署和迁移至 Databricks 的专家
    技术合作伙伴
    将现有工具连接至您的湖仓一体平台
    C&SI 合作伙伴计划
    构建、部署或迁移至湖仓一体平台
    数据合作伙伴
    接入数据消费者生态系统
    合作伙伴解决方案
    查找定制化行业与迁移解决方案
    基于 Databricks 构建
    构建、推广和发展您的业务

-   面向高管
-   面向初创企业
-   湖仓一体架构
-   Mosaic 研究

-   客户案例

-   云服务提供商
    Databricks 在 AWS、Azure、GCP 和 SAP 上的服务
-   咨询与系统集成商
    构建、部署和迁移至 Databricks 的专家
-   技术合作伙伴
    将现有工具连接至您的湖仓一体平台
-   C&SI 合作伙伴计划
    构建、部署或迁移至湖仓一体平台
-   数据合作伙伴
    接入数据消费者生态系统
-   合作伙伴解决方案
    查找定制化行业与迁移解决方案
-   基于 Databricks 构建
    构建、推广和发展您的业务

-   Databricks 平台
    平台概览
    数据、分析与 AI 的统一平台
    数据管理
    数据可靠性、安全性与性能
    共享
    面向所有数据的开放、安全、零拷贝共享
    数据仓库
    用于 SQL 分析的无服务器数据仓库
    治理
    面向所有数据、分析与 AI 资产的统一治理
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

-   集成与数据
    市场
    数据、分析与 AI 的开放市场
    IDE 集成
    在您喜爱的 IDE 中基于湖仓一体进行开发
    合作伙伴连接
    探索并与 Databricks 生态系统集成

-   定价
    Databricks 定价
    探索产品定价、DBU 等
    成本计算器
    估算您在任意云上的计算成本

-   开源
    开源技术
    深入了解平台背后的创新

-   平台概览
    数据、分析与 AI 的统一平台
-   数据管理
    数据可靠性、安全性与性能
-   共享
    面向所有数据的开放、安全、零拷贝共享
-   数据仓库
    用于 SQL 分析的无服务器数据仓库
-   治理
    面向所有数据、分析与 AI 资产的统一治理
-   数据工程
    批处理和流式数据的 ETL 与编排
-   人工智能
    构建和部署机器学习与生成式 AI 应用
-   数据科学
    大规模协作式数据科学
-   商业智能
    面向真实世界数据的智能分析
-   应用开发
    快速构建安全的数据与 AI 应用
-   数据库
    用于数据应用和 AI Agent（智能体）的 Postgres

-   市场
    数据、分析与 AI 的开放市场
-   IDE 集成
    在您喜爱的 IDE 中基于湖仓一体进行开发
-   合作伙伴连接
    探索并与 Databricks 生态系统集成

-   Databricks 定价
    探索产品定价、DBU 等
-   成本计算器
    估算您在任意云上的计算成本

-   开源技术
    深入了解平台背后的创新

-   Databricks 行业解决方案通信媒体与娱乐金融服务公共部门医疗保健与生命科学零售制造业查看所有行业跨行业解决方案AI Agents（智能体）网络安全营销迁移与部署数据迁移专业服务解决方案加速器探索加速器更快实现重要成果

-   Databricks 行业解决方案通信媒体与娱乐金融服务公共部门医疗保健与生命科学零售制造业查看所有行业
-   跨行业解决方案AI Agents（智能体）网络安全营销
-   迁移与部署数据迁移专业服务
-   解决方案加速器探索加速器更快实现重要成果

-   通信
-   媒体与娱乐
-   金融服务
-   公共部门
-   医疗保健与生命科学
-   零售
-   制造业
-   查看所有行业

-   AI Agents（智能体）
-   网络安全
-   营销

-   数据迁移
-   专业服务

-   探索加速器更快实现重要成果


-   培训发现满足您需求的定制课程
-   Databricks Academy登录 Databricks 学习平台
-   认证获得认可与区分
-   免费版免费学习专业的数据与 AI 工具
-   大学联盟想要教授 Databricks？了解详情。

-   Data + AI 峰会
-   Data + AI 全球巡展
-   Data Intelligence Days
-   活动日历

-   Databricks 博客探索新闻、产品公告等
-   Databricks Mosaic 研究博客发现我们生成式 AI 研究的最新进展
-   Data Brew 播客让我们聊聊数据！
-   Champions of Data + AI 播客来自推动创新的数据领导者的洞见

-   客户支持
-   文档
-   社区

-   资源中心
-   演示中心
-   架构中心

-   安全与信任

-   安全与信任

-   关于我们
-   我们的团队
-   Databricks Ventures
-   联系我们

-   在 Databricks 工作
-   开放职位

-   奖项与认可
-   新闻中心

-   安全与信任

-   准备开始了吗？
-   获取演示

-   登录
-   联系我们
-   试用 Databricks

1.  博客
2.  /工程
3.  /文章

# 开源 Dicer：Databricks 的自动分片器

## 为高性能和低成本构建大规模高可用分片服务

发布日期：2026年1月13日

作者：Atul Adya, Colin Meek, Jonathan Ellithorpe, Vivek Jain 和 Yongxin Xu

-   Open sourcing Dicer: We are officially open sourcing Dicer, the foundational auto sharding system used at Databricks to build fast, scalable, and highly available sharded services.
-   The What and Why of Dicer: We describe the problems with typical service architectures today, and why auto-sharders are needed, how Dicer solves these problems, and discuss its core abstractions and use cases.
-   Success stories: The system currently powers mission critical components like Unity Catalog and our SQL query orchestration engine, where it has successfully eliminated availability dips and maintained cache hit rates above 90% during pod restarts.

-   开源 Dicer：我们正式开源 Dicer，这是 Databricks 用于构建快速、可扩展且高可用分片服务的基础自动分片系统。
-   Dicer 的来龙去脉：我们描述了当今典型服务架构存在的问题，为什么需要自动分片器，Dicer 如何解决这些问题，并讨论其核心抽象和用例。
-   成功案例：该系统目前为 Unity Catalog 和我们的 SQL 查询编排引擎等关键任务组件提供支持，成功消除了 Pod 重启期间的可用性下降，并将缓存命中率保持在 90% 以上。

今天，我们很高兴地宣布开源我们最关键的基础设施组件之一——**Dicer：Databricks 的自动分片器**。这是一个旨在构建低延迟、可扩展且高度可靠的分片服务的基础系统。它支撑着 Databricks 的每一个主要产品，使我们能够在提高集群效率和降低云成本的同时，提供始终如一的快速用户体验。Dicer 通过动态管理分片分配来实现这一点，即使在面对重启、故障和负载变化时，也能保持服务的响应能力和弹性。正如这篇博文所详述的，Dicer 被用于多种用例，包括高性能服务、工作分区、批处理管道、数据聚合、多租户、软领导者选举、AI 工作负载的高效 GPU 利用等等。

通过将 Dicer 提供给更广泛的社区，我们期待与业界和学术界合作，共同推进构建稳健、高效和高性能分布式系统的技术水平。在本文的其余部分，我们将讨论 Dicer 背后的动机和设计理念，分享其在 Databricks 内部使用的成功案例，并提供如何自行安装和试验该系统的指南。

## 2. 动机：超越无状态和静态分片架构

Databricks 提供了一套快速扩展的数据处理、分析和 AI 产品。为了大规模支持这一点，我们运营着数百个服务，这些服务必须处理海量状态，同时保持响应能力。历史上，Databricks 工程师依赖两种常见的架构，但随着服务的增长，这两种架构都带来了显著问题：

### 2.1. 无状态架构的隐性成本

Databricks 的大多数服务最初都采用无状态模型。在典型的无状态模型中，应用程序不会在请求之间保留内存状态，必须在每个请求上从数据库重新读取数据。这种架构本质上是昂贵的，因为每个请求都会命中数据库，从而推高运营成本和延迟[1]。

为了降低这些成本，开发人员通常会引入远程缓存（如 Redis 或 Memcached）来分担数据库的工作负载。虽然这提高了吞吐量和降低了延迟，但未能解决几个根本性的低效问题：

- **网络延迟**：每个请求仍需支付网络跳转至缓存层的“税”。
- **CPU开销**：数据在缓存与应用间移动时，大量计算周期浪费在（反）序列化上[2]。
- **“过度读取”问题**：无状态服务常从缓存中获取整个对象或大型数据块，却仅使用其中一小部分数据。这种过度读取浪费了带宽和内存，因为应用会丢弃其花费时间获取的大部分数据[2]。

转向分片模型并在内存中缓存状态，通过将状态直接与操作逻辑并置，消除了这些开销层。然而，静态分片引入了新的问题。

### 2.2. 静态分片的脆弱性

在Dicer之前，Databricks的分片服务依赖于**静态分片**技术（例如一致性哈希）。虽然这种方法简单且允许我们的服务在内存中高效缓存状态，但在生产环境中引入了三个关键问题：

- **重启和自动扩缩期间的不可用性**：缺乏与集群管理器的协调，导致在滚动更新等维护操作或动态扩缩服务时出现停机或性能下降。静态分片方案无法主动适应后端成员变化，仅在节点已被移除后被动反应。
- **故障期间长时间脑裂和停机**：没有中央协调，当Pod崩溃或间歇性无响应时，客户端可能对后端Pod集合形成不一致的视图。这导致“脑裂”场景（两个Pod都认为拥有同一个键）甚至完全丢弃客户流量（没有Pod认为拥有该键）。
- **热键问题**：根据定义，静态分片无法动态重新平衡键分配或根据负载变化调整复制。因此，单个“热键”会使特定Pod不堪重负，形成瓶颈，可能在整个集群中引发连锁故障。

随着我们的服务为满足需求而不断增长，静态分片最终看起来是个糟糕的主意。这导致我们的工程师普遍认为，无状态架构是构建健壮系统的最佳方式，即使这意味着承受性能和资源成本。大约就在此时，Dicer被引入。

### 2.3. 重新定义分片服务的叙事

静态分片的生产风险与无状态化的成本形成对比，使我们几个最关键的服务陷入困境。这些服务依赖静态分片为客户提供快速响应的用户体验。将它们转换为无状态模型将带来显著的性能损失，更不用说增加我们的云成本。

我们构建Dicer就是为了改变这一点。Dicer通过引入一个智能控制平面来解决静态分片的根本缺陷，该平面持续异步更新服务的分片分配。它能响应多种信号，包括应用健康状态、负载、终止通知和其他环境输入。因此，即使在滚动重启、崩溃、自动扩缩事件和严重负载倾斜期间，Dicer也能保持服务的高可用性和良好平衡。

作为一个自动分片器，Dicer建立在包括**Centrifuge**[3]、**Slicer**[4]和**Shard Manager**[5]在内的一系列先前系统之上。我们将在下一节介绍Dicer，并描述它如何帮助我们提高服务的性能、可靠性和效率。

## 3. Dicer：面向高性能和高可用性的动态分片

我们现在概述Dicer、其核心抽象，并描述其各种用例。请关注后续博客文章，我们将深入探讨Dicer的设计和架构。

Dicer将应用程序建模为处理与逻辑键关联的请求（或执行某些工作）。例如，提供用户档案的服务可能使用用户ID作为其键。Dicer通过持续生成键到Pod的分配来对应用程序进行分片，以保持服务的高可用性和负载均衡。

为了扩展到拥有数百万或数十亿键的应用程序，Dicer操作键的范围而非单个键。应用程序使用**SliceKey**（应用键的哈希值）向Dicer表示键，连续的SliceKey范围称为一个**Slice**。如图1所示，一个**Dicer分配**是多个Slice的集合，它们共同覆盖整个应用键空间，每个Slice分配给一个或多个**资源**（即Pod）。Dicer根据应用健康状态和负载信号动态地拆分、合并、复制/去复制和重新分配Slice，确保整个键空间始终分配给健康的Pod，并且没有单个Pod过载。Dicer还能检测热键并将其拆分到自己的Slice中，并将此类Slice分配给多个Pod以分散负载。

图1展示了一个按用户ID分片的应用程序在3个Pod（P0、P1和P2）上的Dicer分配示例，其中ID为13的用户由SliceKey K26（即ID 13的哈希值）表示，当前分配给Pod P0。一个用户ID为42、由SliceKey K10表示的热用户已被隔离在其自己的Slice中，并分配给多个Pod（P1和P2）以处理负载。

图2展示了与Dicer集成的分片应用程序的概览。应用程序Pod通过一个名为**Slicelet**（S代表服务器端）的库了解当前分配。Slicelet通过从Dicer服务获取并监听更新，在本地缓存最新的分配。当收到更新的分配时，Slicelet通过监听器API通知应用程序。

Slicelet观察到的分配是最终一致的，这是一个深思熟虑的设计选择，优先考虑可用性和快速恢复，而非强键所有权保证。根据我们的经验，这对绝大多数应用程序来说是正确的模型，尽管我们确实计划在未来支持更强的保证，类似于Slicer和Centrifuge。

除了保持分配最新外，应用程序还使用Slicelet在处理请求或为某个键执行工作时记录每个键的负载。Slicelet在本地聚合此信息，并异步地将摘要报告给Dicer服务。请注意，与分配监听一样，这也发生在应用程序的关键路径之外，确保了高性能。

Dicer分片应用程序的客户端通过一个名为**Clerk**（C代表客户端）的库查找给定键的分配Pod。与Slicelet类似，Clerk也在后台主动维护最新分配的本地缓存，以确保关键路径上键查找的高性能。

最后，**Dicer分配器**是负责根据应用健康状态和负载信号生成和分发分配的控制器服务。其核心是一个分片算法，通过Slice的拆分、合并、复制/去复制和移动来计算最小调整，以保持键分配给健康的Pod，并使整个应用程序充分负载均衡。分配器服务是多租户的，旨在为一个区域内所有分片应用程序提供自动分片服务。由Dicer服务的每个分片应用程序被称为一个**目标**。

### 3.2 Dicer增强的广泛应用程序类别

Dicer对广泛的系统都有价值，因为将工作负载亲和到特定Pod的能力能带来显著的性能改进。根据我们的生产经验，我们确定了几个核心用例类别。

#### 内存和GPU服务

Dicer 擅长处理需要将海量数据加载并直接从内存提供服务的场景。通过确保特定键的请求始终命中相同的 Pod，键值存储等服务能够实现亚毫秒级延迟和高吞吐量，同时避免从远程存储获取数据的开销。

Dicer 也非常适合现代 LLM（大语言模型）推理工作负载，其中保持亲和性至关重要。示例包括在每会话 KV 缓存中累积上下文的有状态用户会话，以及需要服务大量 LoRA 适配器并必须在受限的 GPU 资源上高效分片的部署。

#### 控制与调度系统

这是 Databricks 最常见的用例之一。它包括集群管理器和查询编排引擎等系统，这些系统持续监控资源以管理扩缩容、计算调度和多租户。为了高效运行，这些系统在本地维护监控和控制状态，避免重复序列化，并能及时响应变化。

Dicer 可用于构建高性能分布式远程缓存，我们已在 Databricks 的生产环境中实现。通过利用 Dicer 的能力，我们的缓存可以实现无缝自动扩缩容和重启，且命中率不受影响，并能避免因热键导致的负载不均衡。

#### 工作分区与后台任务

Dicer 是在服务器集群中划分后台任务和异步工作流的有效工具。例如，负责清理或垃圾回收大表中状态的服务可以使用 Dicer 来确保每个 Pod 负责键空间中互不重叠的特定范围，从而防止冗余工作和锁争用。

#### 批处理与聚合

对于高吞吐量的写入路径，Dicer 支持高效的记录聚合。通过将相关记录路由到同一个 Pod，系统可以在将更新提交到持久化存储之前在内存中进行批处理。这显著降低了每秒所需的输入/输出操作，并提高了数据管道的整体吞吐量。

#### 软领导者选择

Dicer 可用于实现“软”领导者选择，方法是将特定 Pod 指定为给定键或分片的主要协调者。例如，服务调度器可以使用 Dicer 来确保单个 Pod 作为管理一组资源的主要权威。虽然 Dicer 目前提供基于亲和性的领导者选择，但它为需要协调主节点而又无需传统共识协议沉重开销的系统奠定了强大基础。我们正在探索未来的增强功能，为这类工作负载提供更强的互斥保证。

#### 会合与协调

对于需要实时协调的分布式客户端，Dicer 充当了一个天然的会合点。通过将所有针对特定键的请求路由到同一个 Pod，该 Pod 成为一个中央会合点，可以在本地内存中管理共享状态，而无需外部网络跳转。

例如，在实时聊天服务中，加入相同“聊天室 ID”的两个客户端会自动路由到同一个 Pod。这使得 Pod 能够在内存中即时同步他们的消息和状态，避免了共享数据库或复杂通信背板的延迟。

Databricks 的众多服务已通过 Dicer 取得了显著收益，我们在下面重点介绍其中几个成功案例。

Unity Catalog (UC) 是 Databricks 平台上数据和 AI 资产的统一治理解决方案。UC 最初设计为无状态服务，但随着其普及度提高（主要受极高的读取量驱动），面临着巨大的扩展挑战。处理每个请求都需要重复访问后端数据库，这带来了极高的延迟。远程缓存等传统方法并不可行，因为缓存需要增量更新并保持与存储的快照一致性。此外，客户目录的大小可能达到千兆字节级别，若在远程缓存中维护部分或复制的快照而不引入大量开销，成本会非常高昂。

为了解决这个问题，团队集成 Dicer 构建了一个分片的内存中有状态缓存。这一转变使得 UC 能够用本地方法调用替代昂贵的远程网络调用，从而大幅降低了数据库负载并提高了响应速度。下图展示了 Dicer 的初始推出，以及完整的 Dicer 集成部署。通过利用 Dicer 的有状态亲和性，UC 实现了 90-95% 的缓存命中率，显著降低了数据库往返的频率。

### 4.2 SQL 查询编排引擎

Databricks 的查询编排引擎负责管理 Spark 集群上的查询调度，最初是使用静态分片构建的内存中有状态服务。随着服务规模扩大，该架构的局限性成为一个显著的瓶颈；由于实现简单，扩缩容需要手动重新分片，这极其繁琐，并且系统在滚动重启期间也经常出现可用性下降。

与 Dicer 集成后，这些可用性问题得以消除（见图 4）。Dicer 使得在重启和扩缩容事件期间实现零停机成为可能，允许团队通过启用全方位的自动扩缩容来减少繁琐工作并提高系统健壮性。此外，Dicer 的动态负载均衡功能进一步解决了长期存在的 CPU 限制问题，从而在整个集群中实现了更稳定的性能。

![Figure 4: Reduction in availability-loss by the query orchestration service due to Dicer](/images/posts/8f37b8e9ffda.png)

![Figure 4: Reduction in availability-loss by the query orchestration service due to Dicer](/images/posts/8f37b8e9ffda.png)

### 4.3 Softstore 远程缓存

对于未分片的服务，我们开发了 Softstore，一个分布式远程键值缓存。Softstore 利用了 Dicer 的一项称为状态转移的功能，该功能在重新分片期间在 Pod 之间迁移数据以保留应用程序状态。这在计划的滚动重启期间尤为重要，因为整个键空间不可避免地会发生变动。在我们的生产集群中，计划重启约占所有重启的 99.9%，使得这一机制尤其有效，能够实现无缝重启，对缓存命中率的影响微乎其微。图 5 显示了滚动重启期间 Softstore 的命中率，状态转移为一个代表性用例保持了约 85% 的稳定命中率，其余波动由正常工作负载波动引起。

![Figure 5. Comparison of Softstore cache hit rates with and without state transfer. Without state transfer, hit rates drop by roughly 30%, whereas with state transfer hit rates are preserved.](/images/posts/5e6df4515e1a.png)

![Figure 5. Comparison of Softstore cache hit rates with and without state transfer. Without state transfer, hit rates drop by roughly 30%, whereas with state transfer hit rates are preserved](/images/posts/5e6df4515e1a.png)

## 5. 现在您也可以使用它！

您今天就可以在您的机器上试用 Dicer，只需从此处下载。此处提供了一个展示其用法的简单演示 - 它展示了一个包含一个客户端和几个服务器的 Dicer 示例设置。请参阅 Dicer 的 README 和用户指南。

## 6. 即将推出的功能与文章

Dicer 是 Databricks 内部广泛使用的关键服务，其使用量正在快速增长。未来，我们将发布更多关于 Dicer 内部工作原理和设计的文章。随着我们在内部构建和测试更多功能，我们也将发布它们，例如用于客户端和服务器的 Java 和 Rust 库，以及本文中提到的状态转移功能。请给我们反馈，并敬请期待更多内容！

如果您喜欢解决棘手的工程问题并希望加入 Databricks，请查看 databricks.com/careers！

[1]Ziming Mao, Jonathan Ellithorpe, Atul Adya, Rishabh Iyer, Matei Zaharia, Scott Shenker, Ion Stoica (2025). 重新思考数据中心服务的分布式缓存成本。第24届ACM网络热点话题研讨会论文集，1–8。

[2]Atul Adya, Robert Grandl, Daniel Myers, Henry Qin. 快速键值存储：一个时代已来又去的构想。操作系统热点话题研讨会论文集（HotOS '19），2019年5月13–15日，意大利贝尔蒂诺罗。ACM，7页。DOI: 10.1145/3317550.3321434。

[3]Atul Adya, James Dunagan, Alexander Wolman. Centrifuge：云服务的集成租约管理与分区。第七届USENIX网络系统设计与实现研讨会论文集（NSDI），2010年。

[4]Atul Adya, Daniel Myers, Jon Howell, Jeremy Elson, Colin Meek, Vishesh Khemani, Stefan Fulger, Pan Gu, Lakshminath Bhuvanagiri, Jason Hunter, Roberto Peon, Larry Kai, Alexander Shraer, Arif Merchant, Kfir Lev-Ari. Slicer：数据中心应用的自动分片。第12届USENIX操作系统设计与实现研讨会论文集（OSDI），2016年，第739–753页。

[5]Sangmin Lee, Zhenhua Guo, Omer Sunercan, Jun Ying, Chunqiang Tang, 等. Shard Manager：一个用于地理分布式应用的通用分片管理框架。ACM SIGOPS第28届操作系统原理研讨会论文集（SOSP），2021年。DOI: 10.1145/3477132.3483546。

[6]Atul Adya, Jonathan Ellithorpe. 有状态服务：低延迟、高效率、可扩展性——三者难兼得。高性能事务系统研讨会（HPTS）2024，加利福尼亚州太平洋丛林，2024年9月15–18日。


## 不错过任何Databricks文章

![Booting Databricks VMs 7x Faster for Serverless Compute](/images/posts/6ee6ae17dfac.png)

![Booting Databricks VMs 7x Faster for Serverless Compute](/images/posts/6ee6ae17dfac.png)

![Booting Databricks VMs 7x Faster for Serverless Compute](/images/posts/6ee6ae17dfac.png)

2024年11月26日 / 9分钟阅读

#### 为无服务器计算实现Databricks虚拟机启动速度提升7倍

![Mosaic AI Model Serving dashboard for deploying and managing fine-tuned LLaMA models.](/images/posts/c17c6300ff0c.png)

![Mosaic AI Model Serving dashboard for deploying and managing fine-tuned LLaMA models.](/images/posts/c17c6300ff0c.png)

![Mosaic AI Model Serving dashboard for deploying and managing fine-tuned LLaMA models.](/images/posts/c17c6300ff0c.png)

2024年12月10日 / 7分钟阅读

#### 使用Mosaic AI Model Serving对微调后的Llama模型进行批量推理

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
- 零售
- 查看全部

- 网络安全
- 市场营销

- 通信
- 金融服务
- 医疗保健与生命科学
- 制造业
- 媒体与娱乐
- 公共部门
- 零售
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
- 数据智能日
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
- 数据智能日
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

Databricks Inc. 加利福尼亚州旧金山斯皮尔街160号15楼，邮编94105 1-866-330-0121


查看Databricks的职业生涯


© Databricks 2026。保留所有权利。Apache、Apache Spark、Spark、Spark徽标、Apache Iceberg、Iceberg和Apache Iceberg徽标是Apache软件基金会的商标。

- 隐私声明
- |使用条款
- |现代奴隶制声明
- |加利福尼亚州隐私
- |您的隐私选择

---

> 本文由AI自动翻译，原文链接：[Open Sourcing Dicer: Databricks’ Auto-Sharder](https://www.databricks.com/blog/open-sourcing-dicer-databricks-auto-sharder)
> 
> 翻译时间：2026-01-14 04:52
