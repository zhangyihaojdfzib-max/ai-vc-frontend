---
title: 掌控数据安全：Lakebase Postgres客户托管密钥详解
title_original: 'Take Control: Customer-Managed Keys for Lakebase Postgres'
date: '2026-04-20'
source: Databricks Blog
source_url: https://www.databricks.com/blog/take-control-customer-managed-keys-lakebase-postgres
author: ''
summary: 本文介绍了Lakebase Postgres的客户托管密钥（CMK）功能，该功能允许企业使用自身云密钥管理服务（如AWS KMS、Azure Key
  Vault）的密钥来加密和管理数据。文章详细阐述了Lakebase分离存储与计算的架构如何通过分层信封加密模型，在持久化存储和临时计算资源两个层面实现全面的客户控制。核心在于CMK作为信任根源永不离开客户KMS，Databricks仅能使用加密后的密钥，从而在严格监管环境下满足企业对数据主权和安全性的高阶要求。
categories:
- AI基础设施
tags:
- 数据安全
- 客户托管密钥
- 云数据库
- 加密架构
- Lakebase
draft: false
translated_at: '2026-04-21T05:15:41.276983'
---

静态加密是云服务的基础要求，但对于在严格监管环境中运营的企业而言，组织必须掌控信任根源。Lakebase 客户托管密钥（CMK）通过允许您使用来自自身密钥管理服务（如 AWS KMS、Azure Key Vault 或 Google Cloud KMS）的加密密钥，在整个 Lakebase 生命周期内保护和管理数据，从而实现了这种控制。

与传统托管数据库不同，Lakebase 客户托管密钥（CMK）在整个架构中提供全面的管理与控制。传统数据库通常仅对存储进行加密，而 Lakebase CMK 则同时管理持久化存储和临时计算资源。

## Lakebase 加密架构

Lakebase 架构将存储与计算分离为独立层——这种设计实现了弹性扩展和无服务器化操作。存储层（Pageserver 和 Safekeeper）在对象存储和本地缓存中维护长期存在的持久化数据，而计算层则运行独立的 Postgres 实例，可根据需求进行扩展、收缩甚至归零。

![架构图展示了跨云托管密钥服务、Databricks 以及 Lakebase 密钥执行机制的加密机制](/images/posts/a03d28cfce83.png)

这种分离给加密带来了独特挑战：两个层级（以及架构中所有相关缓存）都必须加密并保持在客户控制之下。Lakebase CMK 通过分层信封加密模型解决了这一问题。

## 密钥层级结构

信封加密是一种安全模型，其中数据使用唯一的数据密钥（DEK）加密，而这些密钥本身又由更高级别的密钥加密。这种层级结构确保您的 CMK 永远不会离开您的云 KMS——Databricks 仅接收解密数据所需的已封装（加密）版本密钥。该模型还能实现大规模的高性能加密，因为仅需联系 KMS 解封密钥，而无需加密每个数据块。正是这种架构实现了无缝密钥轮换以及在需要时的及时撤销。

该层级结构包含三个级别：

1.  **客户托管密钥（CMK）**：信任根源，驻留在您的云 KMS（AWS KMS、Azure Key Vault 或 Google Cloud KMS）中。Databricks 永远无法看到此密钥的明文。
2.  **密钥加密密钥（KEK）**：Databricks 密钥管理服务用于封装数据密钥的临时密钥。
3.  **数据加密密钥（DEK）**：为每个数据段生成的唯一密钥。这些密钥以加密（封装）状态与数据一同存储。

![信封加密的层级结构](/images/posts/6b93b71d3261.png)

当需要访问数据时，Lakebase 组件使用从您的 KMS 获取的密钥解封所需的 DEK。如果发生密钥撤销，解封操作将失败，从而使数据在加密层面无法访问。作为此过程的一部分，所有临时计算实例将被终止，以移除对缓存数据的访问权限。

## CMK 实践：存储与计算

在存储和计算层面的具体实现有所不同：

### 1. 持久层（存储）

Lakebase 管理的所有数据段，包括 WAL 段（由 Safekeeper 存储的事务日志）和数据文件，都使用受您 CMK 保护的密钥进行加密。这提供了深度防御：静态数据由您控制下的加密密钥保护，而非 Databricks。

### 2. 临时层（计算）

Postgres 计算虚拟机持有操作系统和 PostgreSQL 使用的临时数据——例如性能缓存、WAL 工件、临时文件等。因此，确保所有这些数据也由 CMK 管理至关重要。CMK 通过以下方式保护这些临时计算数据：

*   **每次启动密钥**：每次 Lakebase 计算实例启动时，都会生成一个唯一的临时密钥。
*   **自动销毁**：当 CMK 被撤销时，Lakebase Manager 将终止实例，销毁临时内存中的密钥，并使本地磁盘数据无法访问。

## 在 Lakebase 工作流中实施 CMK

实施遵循标准的 Databricks 账户到工作区委托模型。这种职责分离确保安全管理员可以管理密钥，而无需访问数据本身。一旦在工作区级别配置了密钥，所有 Lakebase 项目都会将 CMK 作为加密工作流的一部分使用。

### 步骤 1：密钥配置

账户管理员在 Databricks 账户控制台中创建密钥配置。此对象包含密钥标识符（AWS KMS 的 ARN、Azure 的 Key Vault URL 或 Google Cloud KMS 的密钥 ID）以及 Lakebase 将用于执行封装和解封操作的 IAM 角色或服务主体。

### 步骤 2：工作区绑定

然后将该配置映射到特定的工作区。对于 Lakebase，这意味着：

*   **新项目**：所有新的 Lakebase 项目自动继承工作区的 CMK。
*   **隔离**：不同的工作区可以使用不同的 CMK，以满足多租户或多部门的安全要求。

### 步骤 3：生命周期管理与轮换

Lakebase 支持无缝密钥轮换。当您在云提供商控制台中轮换 CMK 时：

*   信封加密层级结构支持无缝轮换——您可以在云 KMS 中轮换 CMK，而无需重新加密数据或更改 DEK。
*   无需停机或手动重新加密。

## 安全可审计性

由于 CMK 驻留在您的云账户中，针对您密钥的加密操作会记录在您提供商的审计服务中（AWS CloudTrail、Azure Monitor 或 Google Cloud Audit Logs）。

## 开启增强的数据主权之旅

如果您的组织需要对 Postgres 工作负载实施最高级别的加密控制，Lakebase CMK 现已面向企业级客户开放。

准备好保护您的数据了吗？请联系您的 Databricks 客户团队，为工作区启用客户托管密钥，或访问我们的技术文档以查看先决条件的 IAM 策略和 KMS 配置。

还不是 Databricks 客户？开始免费试用。

---

> 本文由AI自动翻译，原文链接：[Take Control: Customer-Managed Keys for Lakebase Postgres](https://www.databricks.com/blog/take-control-customer-managed-keys-lakebase-postgres)
> 
> 翻译时间：2026-04-21 05:15
