---
title: nOps迁移至Databricks Lakebase：ISV架构升级指南
title_original: How nOps Rebuilt Their Cloud Optimization Platform on Databricks Lakebase,
  and Why Other ISVs Should Too
date: '2026-05-05'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-nops-rebuilt-their-cloud-optimization-platform-databricks-lakebase-and-why-other-isvs
author: ''
summary: nOps作为管理超40亿美元云支出的自动化成本优化平台，将其生产应用从传统“Lakehouse+独立关系型数据库”的双系统架构迁移至Databricks
  Lakebase。新架构消除了ETL管道、定时任务和变更检测等胶水代码，实现了分析数据与前端应用的紧密耦合。Lakebase的全托管PostgreSQL、自动扩展与自动停止能力，以及无缝集成，显著降低了运营开销和延迟。文章为其他ISV提供了从分离架构走向统一平台的参考路径。
categories:
- 技术趋势
tags:
- Databricks Lakebase
- 云成本优化
- ISV架构
- OLTP与Lakehouse集成
- 无服务器数据库
draft: false
translated_at: '2026-05-06T05:31:09.878108'
---

nOps 是一家 Databricks Built On 合作伙伴，管理着超过 40 亿美元的年度云支出，现已将其生产应用迁移至 Databricks Lakebase。其结果是架构更快、更简单，消除了应用与分析之间的胶水代码，并为其他希望效仿的 ISV 提供了参考指南。

每个在 Databricks 上构建的 ISV 最终都会面临同样的架构抉择：你的分析数据存在于 Lakehouse 中，但你的应用需要一个关系型数据库来实现低延迟读写。于是你额外搭建一个独立的 Postgres 实例（可能是 RDS，也可能是自管理方案），然后突然之间，你不得不维护 ETL 管道、定时任务和变更检测逻辑，仅仅是为了让两个系统保持同步。

nOps 多年来一直处于这种现实之中。然后他们找到了一条更好的路。

## nOps：大规模自动化云成本节省

对于不熟悉的人来说，nOps 是一个自动化云成本优化平台，管理着 AWS、GCP 和 Azure 上基于承诺的折扣。他们的方法明显是“始终在线”的。他们按小时监控、购买和交换云承诺，利用机器学习在有效节省率与承诺锁定风险之间取得平衡。其模式基于绩效：nOps 仅从他们产生的增量节省中收取一定比例的费用。

这是一项数据密集型操作。每小时，nOps 都会分析数千个客户账户的使用模式，评估三大云提供商及数十项服务的承诺组合，并做出自动购买决策。除此之外，他们还通过一个集中的 FinOps 平台提供成本可见性、预测和异常检测。

所有这些工作的分析基础长期以来一直是 Databricks Lakehouse。但前端应用——客户登录查看节省情况、管理预算和探索成本数据的平台——则需要更多支持。

## 问题：两个世界，松散连接

nOps 之前的架构是 Databricks 上 ISV 的常见模式。高级分析和指标计算在 Lakehouse 中运行。面向客户的数据（账户配置、用户偏好、快速变化的客户端特定状态）则存在于由第三方供应商和自研方案支持的独立关系型数据库中。

这两个系统之间的接缝造成了实际摩擦。需要定时任务和基于 cron 的变更检测来保持前端数据库与 Lakehouse 同步。在一个系统中“实时”的数据可能需要几分钟或更长时间才能出现在另一个系统中。而管理独立数据库栈（包括其自身的扩展、备份和安全问题）所带来的运营开销，占用了 nOps 本应用于其最擅长领域——构建承诺自动化——的工程时间。

当 nOps 在 2026 年初从仅支持 AWS 扩展到覆盖 GCP 和 Azure 的多云时，不断增长的工作负载使这一架构不堪重负。团队决定重建平台，这次专注于自身专长，并选择能够简单运行的底层基础设施。

## 决策：为何选择 Lakebase

nOps 选择了 Databricks Lakebase，这是一个与 Lakehouse 直接集成的全托管 PostgreSQL 数据库，作为其新平台的 OLTP 骨干。

nOps 产品总监 Jordan Stein 指出了使 Lakebase 成为合适选择的三个因素：

- **与 Lakehouse 紧密耦合。** 这是最重要的因素。借助 Lakebase，nOps 的数据工程团队可以立即从其 Lakehouse 管道中访问频繁变化的客户数据，无需定时任务、cron 或延迟。正如 Jordan 所说：“我们之前有必须运行的定时任务，有来抓取这些变更的 cron 任务，而现在我们知道，一旦数据上线，我们就能消费它。这对我们来说是一个游戏规则的改变。”
- **自动扩展和自动停止。** 即使在开发期间设置了激进的自动停止策略，nOps 团队也“对性能感到震惊”。Lakebase 的无服务器计算会根据工作负载需求进行调整，并在空闲时缩减至零，这对于一家言行一致的成本优化公司来说至关重要。
- **易于采用。** 时间点恢复功能已被证明很有价值。灵活的 OAuth 角色简化了访问控制。而且由于 Lakebase 位于 Databricks 工作区内，他们的团队在一个他们已经熟悉的平台上工作。无需学习新工具，无需管理单独的控制台。

## 架构：一个平台，紧密集成

以下是 nOps 新架构的样子：

Lakebase 作为中央 Postgres 数据库和单一事实来源，服务于前端应用和 AI 基础设施。

Databricks Lakehouse 持续从 Lakebase 消费数据，用于分析和指标计算。

nOps 平台自动发现并展示 Databricks 指标视图，因此在 Lakehouse 中计算的标准指标能够一致地显示在前端。

数据单向流动，从 Lakebase 流入 Lakehouse 进行分析，无需直接写回。这保持了架构的简洁性，并使事实来源清晰明确。

技术栈的其余部分遵循相同的方法：Vercel 用于托管和可观测性，WorkOS 用于身份验证，Databricks 用于所有数据相关事务。

## 听听 nOps 怎么说

Jordan Stein 最近在一次合作伙伴专题演讲中详细介绍了 nOps 完整的 Lakebase 迁移故事。观看视频，了解迁移过程如何、性能方面有哪些惊喜，以及 Lakehouse 集成如何改变了他们的数据工程工作流：

## ISV 参考指南：为何 Lakebase 改变游戏规则

nOps 的故事并非个例。几乎每个在 Databricks 上构建的 ISV 都面临同样的 OLTP 与分析之间的张力。值得关注的是 Lakebase 如何干净利落地解决了这个问题。

**消除同步成本。** 任何 ISV 技术栈中最昂贵的代码，往往是那些在系统间移动数据的代码。Lakebase 与 Unity Catalog 的原生集成以及一键式 Delta Lake 同步，用托管基础设施取代了自定义 ETL 管道。这为你节省了工程时间。

**单一治理模型。** 当你的 OLTP 数据库注册为 Unity Catalog 资产时，你可以在运营数据和分析数据上获得统一的治理、血缘和访问控制。无需再在两个地方管理安全策略。

**Postgres 兼容性意味着零重写。** Lakebase 是完全托管的 PostgreSQL。你现有的库、ORM 和 SQL 工具开箱即用。支持 pgvector 和 PostGIS 等扩展。你只需将应用指向一个新的连接字符串即可完成迁移，无需重写查询。

**有意义的规模经济。** 基于使用量的定价与缩减至零功能，意味着你无需为空闲容量付费。对于工作负载可变的 ISV（哪个 ISV 没有可变工作负载呢？）来说，这直接影响单位经济性。

**更快交付。** 当你的应用数据库和数据仓库是同一个平台时，一整类集成工作就消失了。你的团队可以专注于交付功能，而不是维护管道。

## 早期采用者，真实影响

nOps 是一个创新型的 Built On 合作伙伴的绝佳范例。他们没有等待 Lakebase 经过多个发布周期才成熟，而是早早认识到其架构契合度，致力于生产迁移，并且已经看到了成果：更快的数据管道、更低的运营开销，以及更好的客户体验。

这种尽早行动的意愿在战略上也很明智。通过现在就在 Lakebase 上构建，nOps 与 Databricks 平台的集成比那些仍在将独立数据库栈拼凑在一起的竞争对手更加紧密。他们的平台更易于运营，也更快扩展。

## 开始使用

探索 Lakebase。如果你是一个在 Databricks 上构建或正在考虑这样做的 ISV，请了解更多关于 Lakebase 及其如何简化你架构的信息。

探索 nOps。如果您的组织希望在不承担承诺风险的情况下降低 AWS、GCP 或 Azure 的云成本，请访问 nOps，了解其自动化优化平台（现已由 Databricks Lakebase 提供支持）如何提供帮助。

### 将最新文章发送到您的收件箱

订阅我们的博客，即可将最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[How nOps Rebuilt Their Cloud Optimization Platform on Databricks Lakebase, and Why Other ISVs Should Too](https://www.databricks.com/blog/how-nops-rebuilt-their-cloud-optimization-platform-databricks-lakebase-and-why-other-isvs)
> 
> 翻译时间：2026-05-06 05:31
