---
title: 在Databricks上构建FHIR原生医疗数据平台
title_original: Building a FHIR-native health data platform on Databricks Lakebase
date: '2026-05-27'
source: Databricks Blog
source_url: https://www.databricks.com/blog/building-fhir-native-health-data-platform-databricks-lakebase
author: ''
summary: 本文介绍了Health Samurai与Databricks合作打造的FHIR原生健康数据平台，该平台在数据摄取阶段将HL7v2、C-CDA和X12等异构临床数据标准化为FHIR，并内置术语标准化和患者去重功能。通过原生运行于Databricks
  Lakebase之上，FHIR数据无需ETL或迁移即可直接用于Spark、ML和AI应用，同时将CMS-0057和ONC合规要求作为架构的自然副产品实现，解决了传统医疗数据碎片化、治理复杂和AI应用受阻的难题。
categories:
- AI基础设施
tags:
- FHIR
- 医疗数据平台
- Databricks
- 互操作性
- 数据标准化
draft: false
translated_at: '2026-05-29T06:13:45.910588'
---

- Health Samurai 在数据摄取阶段将 HL7v2、C-CDA 和 X12 中的临床数据标准化为 FHIR，并内置术语标准化和患者去重功能
- Aidbox 原生运行于 Databricks Lakebase 之上，使 FHIR 数据无需 ETL 或数据迁移即可立即用于 Spark、ML 和 AI
- 该架构将 CMS-0057 和 ONC 合规要求作为副产品实现，而非独立的工作流

医疗数据存在于数十个系统、EHR、理赔、实验室、药房、SDoH 中，每个系统都有各自的格式、编码和重复数据。将这种碎片化格局转变为统一、FHIR 标准化且可信赖的数据基础，是实现更好疗效、更智能运营和监管合规的关键一步。在本博客中，您将了解 Health Samurai 和 Databricks 如何为您提供基于开放标准、可任意规模构建该基础的技术。

如今，智能医疗应用已不再处于业务的边缘。它们驱动着业务本身：从主动缩小护理差距，到赋能实时会员互动，再到确保设计上的监管合规。但这些应用需要一个大多数医疗机构都难以构建的数据基础：一个标准化、受治理、且无需在系统间移动数据即可被技术栈中每个工具访问的基础。

如果您的运营智能和分析能力能够统一并真正实现互操作，驱动相同的洞察，会怎样？

## 挑战：碎片化的数据，碎片化的治理

医疗数据环境异常复杂。患者信息分布在 HL7v2 消息、C-CDA 文档、X12 事务和专有格式中，每个系统对相同临床概念的编码方式各不相同。一个诊断可能在多个词汇表中以多个代码出现。一个患者可能在多个系统中存在多条记录。

统一这些数据的传统方法涉及搭建一个用于互操作的 FHIR 服务器、一个用于分析的独立数据仓库，以及连接两者的 ETL 管道网络。每个系统都维护着自己的访问控制、审计追踪和合规状态。

这种重复成本高昂。相同的临床数据在 FHIR 服务器、数据仓库和多个临时层之间被复制——每一层都增加了存储、计算和运营开销。与此同时，FHIR 服务器本身往往成为瓶颈。大多数实现是为事务性用例设计的——文档交换、点查询、监管 API——而非现代分析、ML 管道或需要高效扫描数百万资源的 AI Agent 的访问模式。

结果，组织被迫做出权衡：过度配置 FHIR 基础设施以维持性能，或者将数据提取到另一个系统中使其可用。

结果是可以预见的：数据移动缓慢、治理碎片化、AI 计划停滞——因为模型无法在需要的地方可靠地访问干净、可信赖且治理良好的数据。成本增加，而灵活性降低；您无法在孤立、不一致且治理不善的数据之上构建智能护理应用。

## 愿景：一个数据集，所有工具，无需数据移动

设想一个单一平台，临床数据在入口点即标准化为 FHIR——相同的数据，无需任何移动或转换，即可立即用于 Spark 分析、ML 模型、AI Agent 和 BI 仪表板。合规性不再是独立的工作流，而是架构的自然属性。每个工具，从 EHR 到数据科学家的笔记本，都能看到相同的、受治理的、可信赖的数据。

这就是 Health Samurai 和 Databricks 共同构建的成果。

## 工作原理：Health Samurai

### 聚合与标准化

数据质量的第一英里决定了洞察的最后一英里。Health Samurai 提供技术和专业知识，将来自不同来源的数据收集并标准化为统一的、FHIR 原生的数据基础。该层的一切都以互操作性为设计目标。数据格式和 API 基于 HL7 和 X12——包括 FHIR R4/R5、HL7 v2、C-CDA 和 X12。临床含义使用广泛采用的编码系统表示，如 LOINC、SNOMED CT、RxNorm 和 ICD-10。特定用例的一致性通过 FHIR 实施指南定义，如 US Core、CARIN Blue Button、Da Vinci PDex 和 mCODE——随着法规和合作伙伴需求的变化，还会纳入额外的编码系统和 IG。

这是一个深思熟虑的架构选择，而非简单的勾选框。开放标准意味着确保您的数据模型不会锁定在单一供应商。今天支持互操作的相同 FHIR 资源，无需返工即可支持分析、AI 和未来的应用。切换工具不应要求重新建模您的数据。

关键能力包括：

- 开源 HL7v2、C-CDA 和 X12 转换器将遗留数据转换为 FHIR——医疗互操作的现代标准。
- FHIR 原生术语服务器跨词汇表规范化代码，确保一个诊断无论来自哪个源系统都只被计数一次。
- MDM/MPI（主数据管理/主患者索引）对患者记录进行去重，确保一个患者对应一条黄金记录。
- FHIR 实施指南和验证在入口点强制执行数据质量和一致性——而非事后进行。

结果是干净、标准化的 FHIR 数据，每个患者对应一条黄金记录。质量和透明度是基础，而非事后补救方法。

Health Samurai 帮助为每个组织的特定数据环境配置这些管道和工具。

### 随处访问——零 ETL

这就是架构实现变革之处。Aidbox——Health Samurai 的 FHIR 服务器和数据库——原生运行于 Databricks Lakebase 之上。

Lakebase 是一个完全托管、无服务器的 Postgres 数据库，集成在 Databricks 数据智能平台中。由于 Aidbox 直接运行在 Lakebase 上，FHIR 数据可立即在整个 Databricks 工具包中使用——无需 ETL。

数据通过 Moonlink 复制，这是一个在运营和分析格式之间实现实时同步的引擎，零 ETL。这使得 FHIR 数据能够无缝流入分析层，消除了对管道、转换或延迟的依赖。

这从单个数据集创建了两种互补的访问模式，同时为您的分析和工作负载提供支持：

1. Databricks 原生访问：Spark、SQL、ML、AI/BI——用于分析、数据科学和 AI
2. 基于标准的访问：FHIR API、SMART on FHIR 和 SQL on FHIR ViewDefinitions（一种新的 HL7 标准，将嵌套的 FHIR 资源展平为表格视图用于分析）

![](/images/posts/c2d4d427ff6d.png)

### 您可以构建什么

借助统一的 FHIR 数据以及 Health Samurai 和 Databricks 的联合力量，组织可以灵活地应对其特定挑战：

#### EHR 优化与价值导向护理

由 Databricks AI 驱动的临床和行政决策支持，通过 SMART on FHIR 和 CDS Hooks 连接回 EHR 和计费工作流。这实现了：

- HEDIS/STARS 评分和质量测量
- 风险调整和 HCC 捕获优化
- 合同分析和共享储蓄追踪
- 主动（而非回顾性）缩小护理差距的 Agentic AI

FHIR 原生基础意味着洞察可直接流回临床医生所在的护理点，嵌入其现有工作流中。

#### 大规模会员互动

通过以下方式与患者和会员建立有意义的关系：

- 以 FHIR API 为骨干的患者门户——设计上符合标准
- 利用 Databricks 上的倾向模型进行大规模个性化外展，为数百万会员确定正确的渠道、信息和时机
- 患者访问 API 作为架构的自然属性包含在内

#### 合规——内置，而非附加

通过基于FHIR构建，组织能够自然满足CMS-0057（互操作性与患者访问）及ONC要求等监管规定，具体体现在以下方面：

- 患者访问规则合规性
- 支付方间数据交换
- ONC健康IT认证就绪状态

合规并非独立项目，而是正确行事的必然产物。

## 为何此刻至关重要

CMS与ONC的监管截止日期日益临近，人工智能正从试点阶段迈向生产环境——但这一切必须建立在可信且受治理的数据基础之上。传统模式下，维护独立的FHIR服务器、独立分析平台以及连接两者的ETL管道，对于现代医疗需求而言过于缓慢、昂贵且脆弱。

Lakebase为您的互操作性投资提供前瞻性保障：您的FHIR服务器运行在数据智能平台上，临床运营与分析共享同一信息源，Unity Catalog统一治理从运营数据到洞察及AI的全链路信息。开放标准意味着零供应商锁定的灵活性。

## 立即开始

Health Samurai与Databricks——为您的健康数据平台提供开放技术。

- 了解更多关于Databricks Lakebase的信息
- 探索Health Samurai的Aidbox
- 联系我们讨论您的健康数据平台战略

---

> 本文由AI自动翻译，原文链接：[Building a FHIR-native health data platform on Databricks Lakebase](https://www.databricks.com/blog/building-fhir-native-health-data-platform-databricks-lakebase)
> 
> 翻译时间：2026-05-29 06:13
