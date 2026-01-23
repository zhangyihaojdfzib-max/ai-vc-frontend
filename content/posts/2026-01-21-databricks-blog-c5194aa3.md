---
title: BlackIce发布：面向AI安全测试的容器化红队工具包
title_original: 'Announcing BlackIce: A Containerized Red Teaming Toolkit for AI Security
  Testing'
date: '2026-01-21'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-blackice-containerized-red-teaming-toolkit-ai-security-testing
author: ''
summary: 本文介绍了BlackIce，一个专为AI安全测试设计的容器化红队工具包。该工具包旨在帮助安全研究人员和开发人员系统性地评估AI模型与系统的安全性，识别潜在漏洞与攻击面。通过提供一套集成的、可复现的测试环境，BlackIce简化了针对AI应用（如大型语言模型和机器学习系统）的对抗性测试流程，助力构建更健壮的AI防御体系。
categories:
- AI基础设施
tags:
- AI安全
- 红队测试
- 容器化工具
- 安全测试
- 对抗性攻击
draft: false
translated_at: '2026-01-23T04:45:01.635432'
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
            Databricks 在 AWS、Azure、GCP 和 SAP 上
        咨询与系统集成商
            构建、部署和迁移至 Databricks 的专家
        技术合作伙伴
            将您现有工具连接到您的 Lakehouse
        C&SI 合作伙伴计划
            构建、部署或迁移至 Lakehouse
        数据合作伙伴
            接入数据消费者生态系统
        合作伙伴解决方案
            查找定制行业和迁移解决方案
        Built on Databricks
            构建、营销和发展您的业务

-   产品
    Databricks 平台
        平台概述
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
            获得认可与差异化
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
            探索新闻、产品公告等
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
-   Databricks Academy登录Databricks学习平台
-   认证获得认可与区分
-   免费版免费学习专业的Data和AI工具
-   大学联盟想教授Databricks？了解详情。

-   Data + AI Summit
-   Data + AI World Tour
-   AI Days
-   活动日历

-   Databricks博客探索新闻、产品公告等
-   Databricks Mosaic研究博客发现我们Gen AI研究的最新进展
-   Data Brew播客让我们聊聊数据！
-   Champions of Data + AI播客来自推动创新的数据领导者的见解

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

-   在Databricks工作
-   开放职位

-   奖项与认可
-   新闻中心

-   安全与信任

-   准备开始了吗？
-   获取演示

-   登录
-   联系我们
-   试用Databricks

1.  博客
2.  /安全与信任
3.  /文章

# 宣布BlackIce：用于AI安全测试的容器化红队工具包

![Announcing BlackIce: A Containerized Red Teaming Toolkit for AI Security Testing](/images/posts/8457e65b6aa4.png)

![Announcing BlackIce: A Containerized Red Teaming Toolkit for AI Security Testing](/images/posts/8457e65b6aa4.png)

![Announcing BlackIce: A Containerized Red Teaming Toolkit for AI Security Testing](/images/posts/8457e65b6aa4.png)

发布日期：2026年1月21日

作者：Caelin Kaplan 和 Alex Warnecke

-   -
-   -
-   -

宣布发布BlackIce，这是一个用于AI安全测试的开源容器化工具包，首次在CAMLIS Red 2025上推出解释BlackIce如何整合14个开源工具，并映射到MITRE ATLAS和Databricks AI安全框架（DASF）分享论文、GitHub仓库和Docker镜像的链接，助您快速上手

-   宣布发布BlackIce，这是一个用于AI安全测试的开源容器化工具包，首次在CAMLIS Red 2025上推出
-   解释BlackIce如何整合14个开源工具，并映射到MITRE ATLAS和Databricks AI安全框架（DASF）
-   分享论文、GitHub仓库和Docker镜像的链接，助您快速上手

在CAMLIS Red 2025上，我们推出了BlackIce，这是一个开源、容器化的工具包，它将14个广泛使用的AI安全工具捆绑到一个单一、可复现的环境中。在这篇文章中，我们将重点介绍BlackIce背后的动机，概述其核心功能，并分享资源以帮助您开始使用。

BlackIce的诞生源于AI红队面临的四个实际挑战：(1) 每个工具都有独特且耗时的设置和配置；(2) 由于依赖冲突，工具通常需要独立的运行时环境；(3) 托管笔记本每个内核只暴露一个Python解释器；(4) 工具生态庞大，对新手来说难以驾驭。

受传统渗透测试中Kali Linux的启发，BlackIce旨在通过提供一个即用型容器镜像，让团队绕过繁琐的设置过程，专注于安全测试。

BlackIce提供了一个版本锁定的Docker镜像，其中捆绑了14个精选的开源工具，涵盖负责任AI、安全测试和经典对抗性机器学习。这些工具通过统一的命令行界面暴露，可以从shell运行，也可以在基于该镜像构建的计算环境的Databricks笔记本中运行。以下是此初始版本包含的工具摘要，以及其支持组织和撰写本文时的GitHub星标数：

为了展示BlackIce如何融入既定的AI风险框架，我们将其能力映射到了MITRE ATLAS和Databricks AI安全框架（DASF）。下表说明该工具包涵盖了提示词注入、数据泄露、幻觉检测和供应链安全等关键领域。

BlackIce将其集成的工具分为两类。静态工具通过简单的命令行界面评估AI应用，几乎不需要编程专业知识。动态工具提供类似的评估能力，但也支持基于Python的高级定制，允许用户开发自定义攻击代码。在容器镜像内，静态工具安装在独立的Python虚拟环境（或单独的Node.js项目）中，每个环境维护独立的依赖项，并可直接从CLI访问。或者，动态工具安装到全局Python环境中，其依赖冲突通过`global_requirements.txt`文件管理。

镜像中的一些工具需要少量添加或修改，以便与Databricks Model Serving端点无缝连接。我们对这些工具应用了自定义补丁，使其开箱即用地直接与Databricks工作空间交互。

有关构建过程的详细说明，包括如何添加新工具或更新工具版本，请参阅GitHub仓库中的Docker构建README。

BlackIce镜像可在Databricks的Docker Hub上获取，当前版本可以使用以下命令拉取：

要在 Databricks 工作区中使用 BlackIce，请使用 Databricks 容器服务配置您的计算资源，并在创建集群时于 Docker 菜单中将 `databricksruntime/blackice:17.3-LTS` 指定为 Docker 镜像 URL。

集群创建完成后，您可以将其附加到此演示笔记本，以了解如何在单一环境中编排多个 AI 安全工具，从而测试 AI 模型和系统是否存在提示词注入和越狱攻击等漏洞。

请查看我们的 GitHub 仓库，以了解更多关于集成工具的信息，查找在 Databricks 托管模型上运行这些工具的示例，并获取所有 Docker 构建产物。

有关工具选择过程和 Docker 镜像架构的更多详细信息，请参阅我们的 CAMLIS 红皮书。


## 不错过任何 Databricks 动态

![Introducing Predictive Optimization for Statistics](/images/posts/ab77da589535.png)

![Introducing Predictive Optimization for Statistics](/images/posts/ab77da589535.png)

![Introducing Predictive Optimization for Statistics](/images/posts/ab77da589535.png)

2024年11月20日 / 阅读 4 分钟

#### 统计预测优化功能发布

![How to present and share your Notebook insights in AI/BI Dashboards](/images/posts/5cc2f5e4940f.png)

![How to present and share your Notebook insights in AI/BI Dashboards](/images/posts/5cc2f5e4940f.png)

![How to present and share your Notebook insights in AI/BI Dashboards](/images/posts/5cc2f5e4940f.png)

2024年11月21日 / 阅读 3 分钟

#### 如何在 AI/BI 仪表板中呈现和共享 Notebook 洞察

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

- 面向高管
- 面向初创公司
- 湖仓一体架构
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
- 湖仓一体架构
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
- Databricks 学院登录

- Data + AI 峰会
- Data + AI 全球巡展
- AI 日
- 活动日历

- Databricks 博客
- Databricks Mosaic 研究博客
- Data Brew 播客
- 数据与 AI 冠军播客

- 培训
- 认证
- 免费版
- 大学联盟
- Databricks 学院登录

- Data + AI 峰会
- Data + AI 全球巡展
- AI 日
- 活动日历

- Databricks 博客
- Databricks Mosaic 研究博客
- Data Brew 播客
- 数据与 AI 冠军播客

- 关于我们
- 我们的团队
- Databricks Ventures
- 联系我们

- 开放职位
- 在 Databricks 工作

- 奖项与认可
- 新闻中心

- 关于我们
- 我们的团队
- Databricks Ventures
- 联系我们

- 开放职位
- 在 Databricks 工作

- 奖项与认可
- 新闻中心

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

![databricks logo](/images/posts/443a5359ee28.png)

Databricks Inc.160 Spear Street, 15th FloorSan Francisco, CA 941051-866-330-0121


查看 Databricks 的职位


© Databricks2026. 保留所有权利。Apache、Apache Spark、Spark、Spark 徽标、Apache Iceberg、Iceberg 和 Apache Iceberg 徽标是 Apache 软件基金会的商标。

- 隐私声明
- |使用条款
- |现代奴隶制声明
- |加州隐私
- |您的隐私选择

---

> 本文由AI自动翻译，原文链接：[Announcing BlackIce: A Containerized Red Teaming Toolkit for AI Security Testing](https://www.databricks.com/blog/announcing-blackice-containerized-red-teaming-toolkit-ai-security-testing)
> 
> 翻译时间：2026-01-23 04:45
