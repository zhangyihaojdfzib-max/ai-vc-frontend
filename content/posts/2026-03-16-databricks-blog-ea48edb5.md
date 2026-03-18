---
title: 无服务器JAR开发与部署指南：基于Databricks Connect和Spark 4
title_original: Develop and deploy Serverless JARs
date: '2026-03-16'
source: Databricks Blog
source_url: https://www.databricks.com/blog/develop-and-deploy-serverless-jars
author: ''
summary: 本文介绍了如何在Databricks平台上使用无服务器计算开发和部署Scala/Java Spark作业（JAR）。文章阐述了无服务器JAR的三大优势：快速启动、免版本升级和无需管理基础设施，并详细说明了其基于Spark
  4（Scala 2.13）和Spark Connect的架构原理。此外，文章还提供了使用Databricks Connect进行交互式开发调试，以及通过Databricks
  Asset Bundles将作业部署到生产环境的完整工作流程，包括编译、上传和创建无服务器作业的具体步骤。
categories:
- AI基础设施
tags:
- 无服务器计算
- Spark
- Databricks
- Scala
- 大数据开发
draft: false
translated_at: '2026-03-18T05:02:08.914840'
---

## 无服务器 JAR 与适用于 Scala 的 Databricks Connect

无服务器 JAR 使团队能够在完全托管的无服务器计算上构建和运行 Scala 和 Java Spark 作业。团队可以继续使用他们已信任的语言构建生产级 Spark 流水线，享受自动升级，而无需承担管理集群的运维开销：

-   **快速启动**：借助无服务器，Scala 和 Java 作业可在数秒内启动，而非数分钟。工程师可以立即运行和迭代代码，无需等待集群启动。
-   **无版本升级**：无服务器持续运行在最新支持的 Spark 运行时上，因此您永远无需规划或管理 Databricks Runtime 升级。
-   **无需管理基础设施**：无需集群配置、容量规划或运行时管理。Databricks 自动处理基础设施、扩展和性能优化，让开发人员专注于编写代码。
-   **按使用付费**：团队只需为实际使用的计算付费，而无需为始终在线的集群或闲置容量付费。

## 无服务器 JAR 如何工作？

您可以使用 Lakeflow Jobs 在无服务器计算上运行 JAR。无服务器 JAR 基于 Spark 4（Scala 2.13）和 Spark Connect 构建，采用与 Python 相同的架构。用户代码与引擎的解耦实现了无版本升级，消除了依赖冲突，并借助 Lakeguard 实现了原生细粒度访问控制。

此架构具有以下几个关键优势：

-   **无版本执行**：应用程序不再绑定到特定的 Databricks Runtime 版本。无服务器始终运行在最新支持的运行时上，消除了规划、安排或管理 Databricks Runtime 升级的需要。
-   **借助 Lakeguard 实现原生细粒度访问控制**：由于所有执行都发生在服务器端，Databricks 可以低成本地强制执行行级筛选器和基于属性的访问控制（ABAC）。
-   **精简且独立的依赖集**：无服务器环境与 Spark 隔离运行，因此可以提供独立且精简的依赖集，同时也消除了依赖冲突。

## 使用 Databricks Connect 和 Databricks Asset Bundles 进行开发

借助 Databricks Connect，您可以在您选择的 IDE（如 IntelliJ 或 Cursor）中交互式地编写和调试代码，并使用启动时间近乎即时的无服务器计算。

这使得开发周期更快、更可靠，因为您可以在不离开 IDE 的情况下针对真实数据和环境进行测试。开发完成后，您可以使用 Databricks Asset Bundles 将作业投入生产。

## 如何通过提供 JAR 在无服务器上部署

### 步骤 1：为无服务器编译您的 JAR

-   使用 **Spark 4（Scala 2.13）** 和 **Spark Connect** 进行编译
-   显式捆绑所有非 Spark 依赖项，或将其作为额外的 JAR 提供

### 步骤 2：创建无服务器作业

-   将您的 JAR 上传到 Unity Catalog 卷或 UC 工作区文件夹。
-   使用 JAR 任务创建新作业，并选择无服务器作为计算类型。

## 开始使用无服务器 JAR。

要快速入门，请遵循关于使用 Databricks Asset Bundle 模板开发和部署 Scala 作业的教程。有关手动编译 JAR 的教程，请参阅在无服务器计算上运行 Scala 代码。

---

> 本文由AI自动翻译，原文链接：[Develop and deploy Serverless JARs](https://www.databricks.com/blog/develop-and-deploy-serverless-jars)
> 
> 翻译时间：2026-03-18 05:02
