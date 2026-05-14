---
title: Airbnb数据网格Viaduct 1.0发布与未来展望
title_original: Viaduct 1.0 and the future of Airbnb’s data mesh
date: '2026-05-13'
source: Airbnb Engineering
source_url: https://medium.com/airbnb-engineering/viaduct-1-0-and-the-future-of-airbnbs-data-mesh-6bab4ec98b89?source=rss----53c7c27702d5---4
author: ''
summary: Airbnb宣布其面向数据的服务网格Viaduct 1.0正式发布，从内部工具转型为社区驱动的开源项目。Viaduct基于GraphQL，提供统一接口访问和交互数据源，解决中心化模式与去中心化开发的矛盾。通过多租户运行时，团队可独立开发和测试租户模块，无需管理独立服务器。文章还比较了Viaduct与GraphQL
  Federation的异同，指出两者可互补使用，并强调了对API稳定性和社区参与的承诺。
categories:
- AI基础设施
tags:
- Viaduct
- 数据网格
- GraphQL
- Airbnb
- 开源
draft: false
translated_at: '2026-05-14T05:50:07.413238'
---

# Viaduct 1.0 与 Airbnb 数据网格的未来

收听

从内部工具迈向社区驱动、生产就绪的数据网格。

作者：Ryan Tanner，Raymie Stata，Adam Miskiewicz

## 引言

我们很高兴宣布 Viaduct 1.0 版本发布。此次发布标志着 Viaduct 从一个恰好开源的 Airbnb 内部工具，转变为一个拥有稳定公共 API 的真正社区驱动项目。1.0 版本包含大量新特性和增强功能，我们在 Viaduct 博客中进行了描述。

Viaduct 面向构建公司级数据 API 的平台工程师、希望为共享图谱做出贡献但无需自行搭建服务器的服务所有者，以及那些已超越单一 GraphQL 服务规模的工程组织。

## 什么是 Viaduct？

Viaduct 是 Airbnb 面向数据的服务网格，一个基于 GraphQL 的系统，为访问和交互任何数据源提供统一接口。多年来，它一直支撑着 Airbnb 的数据基础设施，使产品工程师能够高效、安全地访问数据，同时让服务所有者能够将实现细节与 API 表面解耦。

## 什么是面向数据的服务网格？

Viaduct 服务网格通过一个 GraphQL 模式来定义，该模式包含：

- **类型**（及接口）：描述服务网格内管理的数据
- **查询**（及订阅）：提供访问这些数据的方式，与提供数据的服务入口点相抽象
- **变更**：提供更新数据的方式，同样与服务入口点相抽象

## 为什么选择 Viaduct？

构建 Viaduct 是为了解决大多数战略性采用 GraphQL 的组织所面临的一个特定问题：**中心化模式的去中心化开发**。

## 为什么需要中心化模式？

中心化模式为组织的全部数据和能力提供了单一、一致的接口。每个客户端无需知道该调用哪个后端服务，而是与一个连接组织所有领域的统一图谱进行交互。这使得 API 更易于发现，支持更丰富的跨域查询，并为实施策略、可观测性和模式治理提供了统一场所。

## 为什么需要去中心化开发？

中心化模式只有在能够快速演进时才能发挥作用。理解业务各个领域的领域专家必须能够设计和实现他们最熟悉的模式部分。中心团队无法掌控一切，也不应试图这样做。挑战在于，在保持共享模式的一致性和稳定性的同时，赋予团队对其自身领域贡献的自主权。

Viaduct 通过多租户解决了这一问题。一个共享的多租户运行时托管着独立开发和测试的租户模块，每个模块拥有模式的一部分。希望做出贡献的团队只需为其模块创建一个目录，定义其模式定义语言（SDL）和解析器，即可开始提供服务。无需设置或运行单独的 GraphQL 服务、管理路由器组合，或成为 GraphQL 基础设施专家。团队专注于领域逻辑；平台负责执行、扩展和集成。

## Viaduct 与 GraphQL Federation

我们经常被问及 Viaduct 与 GraphQL Federation 的比较。两者解决的是同一个问题——中心化模式的去中心化开发——但采取了不同的方法。

Federation 通过服务来分发开发。每个团队拥有并运行自己的 GraphQL 子图服务器；这些子图由 federation 路由器组合成一个统一的图谱。Viaduct 通过模块来分发开发。一个共享的多租户运行时托管着定义和实现模式部分的租户模块。

Federation 通过分发服务器来分发开发。Viaduct 通过分发模块来分发开发。

我们不认为 Viaduct 是 federation 的替代品，而是其补充。Viaduct 可以作为子图参与 federated 架构。在一个拥有数百个团队为整体图谱做出贡献的大型组织中，federated 方法需要运行数百个独立的子图服务器。使用 Viaduct，组织可以运行较少数量的 Viaduct 实例，每个实例托管许多紧密相关的租户模块。然后 Federation 可以将这些实例组合成一个更大的企业图谱。

## 社区

Viaduct 的 "1.0" 标识是对稳定性的承诺。到目前为止，Viaduct 为满足内部需求而快速演进，通常通过我们的内部单体仓库工具管理破坏性变更。公开发布需要不同的方法。我们在所有公共表面应用了 @StableApi、@ExperimentalApi 和 @InternalApi 注解，并在 CI 中运行 Kotlin 的二进制兼容性验证器，以便在破坏性变更发布前捕获它们。Viaduct 现已发布到 Maven Central，支持自动发布和 Dokka 生成的 API 文档。

我们致力于在开放环境中开发 Viaduct。我们的意图是在代码编写之前，而非之后，让社区参与重大架构决策。我们的首次公开讨论是 GitHub 上的 Connections RFC，我们计划继续朝这个方向前进。我们未来的目标是成为一个真正的社区项目，而不仅仅是一个恰好开源的内部项目。

无论您是希望统一数据层、为核心引擎做贡献，还是基于图谱进行构建，现在都是参与的好时机。从 入门指南 开始 →

如果您对此类工作感兴趣，请查看我们的一些 开放职位！

## GraphQLConf 2026

下周要去 GraphQLConf 吗？请关注 5 月 20 日由 Airbnb 工程师主持的四场基于 Viaduct 的演讲。

演讲者：James Bellenger

时间：太平洋时间下午 3:50–4:15

本演讲将解释概率性测试如何揭示复杂 GraphQL 系统中的隐藏错误——以 Airbnb 推出新 GraphQL 引擎为例——并展示如何使用相同的方法来加固您自己的系统。

演讲者：Vickey Yeh

时间：太平洋时间下午 1:55–2:20

探讨 Airbnb 的 Viaduct 系统如何让每个团队轻松监控和调试自己的代码——使用内置的所有权标签、自动告警/仪表盘和成本感知追踪——使每个人都能将共享服务中属于自己的部分视为己有。

演讲者：Linquan Zhang 和 Cetlin Sahin

时间：太平洋时间下午 2:30–2:55

我们将介绍如何架构我们的分片解决方案，以及它如何提升了我们的运维能力。您将清晰了解我们的实现权衡随时间推移的表现、自上线以来获得的关键生产洞察，以及在不断裂 API 表面的前提下将 GraphQL 网关推向更高隔离度的策略。

演讲者：Michael Rebello

时间：太平洋时间下午 3:05–3:30

生成有效且逼真的模拟数据用于原型设计和测试多年来一直是一个未解决的挑战。模拟数据编写和维护繁琐，而随机值生成和字段存根等改进尝试又因缺乏必要的领域上下文而无法使测试数据逼真且有意义。在本演讲中，我将分享我们如何通过结合现有 GraphQL 基础设施、丰富的产品和模式上下文以及 LLM，仅需向字段或操作添加一个指令（@generateMock），即可在 Airbnb 重新构想 GraphQL 模拟，生成令人信服、类型安全的模拟数据。

无论您是在微调单个服务还是运行多租户网关，这些会议都将为您提供构建健壮、可观测且对开发者友好的 GraphQL 系统的实用策略。5 月 20 日见！

## 致谢

感谢整个 Viaduct 团队，特别是 Aileen Chen 和 Raymie Stata，为 Viaduct Modern 所做的不懈努力。

所有产品名称、徽标和品牌均为其各自所有者的财产。本网站中使用的所有公司、产品和服务名称仅用于标识目的。使用这些名称、徽标和品牌并不表示认可。

---

> 本文由AI自动翻译，原文链接：[Viaduct 1.0 and the future of Airbnb’s data mesh](https://medium.com/airbnb-engineering/viaduct-1-0-and-the-future-of-airbnbs-data-mesh-6bab4ec98b89?source=rss----53c7c27702d5---4)
> 
> 翻译时间：2026-05-14 05:50
