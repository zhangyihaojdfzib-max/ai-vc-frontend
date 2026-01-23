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

# 宣布BlackIce：用于AI安全测试的容器化红队工具包

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

##

---

> 本文由AI自动翻译，原文链接：[Announcing BlackIce: A Containerized Red Teaming Toolkit for AI Security Testing](https://www.databricks.com/blog/announcing-blackice-containerized-red-teaming-toolkit-ai-security-testing)
> 
> 翻译时间：2026-01-23 04:45
