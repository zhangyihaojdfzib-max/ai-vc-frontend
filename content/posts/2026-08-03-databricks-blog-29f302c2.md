---
title: Databricks完成收购Panther，加速安全数据湖仓时代
title_original: 'Databricks Completes Acquisition of Panther: Accelerating the Security
  Lakehouse Era'
date: '2026-08-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-completes-acquisition-panther-accelerating-security-lakehouse-era
author: ''
summary: Databricks正式完成对Panther的收购，将Panther成熟的SOC工作流与AI检测引擎整合至Lakewatch开放数据湖仓，旨在解决传统SIEM在数据存储成本、留存限制及手动告警分诊方面的痛点。此举使安全团队能够以开放格式留存PB级遥测数据，部署自主AI
  Agent进行实时分诊，并执行检测即代码，从而加速事件响应，推动安全数据湖仓成为新一代安全运营范式。
categories:
- AI基础设施
tags:
- Databricks
- Panther
- 安全数据湖仓
- AI SOC
- SIEM
draft: false
translated_at: '2026-08-06T05:12:03.494592'
---

- 它是什么：Databricks 已正式完成对 Panther 的收购，将其成熟的 SOC 工作流和软件驱动的检测引擎与 Lakewatch 的开放安全数据湖仓基础相结合。
- 它解决的挑战：传统 SIEM 迫使安全团队在高存储成本和有限数据留存之间做出妥协，造成数据孤岛，并因手动告警分诊导致分析师倦怠。
- 成果与影响：安全团队现在可以以开放格式留存 PB 级遥测数据，部署自主 AI Agent 进行实时分诊，并执行检测即代码以加速事件响应。

今天，我们激动地宣布，Databricks 已正式完成对 Panther 的收购。Panther 是一个专为现代安全运营而构建的 AI SOC 平台。网络安全已从根本上转变为数据管理和 AI 问题。大规模、实时地收集、留存和分析数据的能力，如今已成为 SOC 检测和响应速度的关键制约因素。攻击者正在利用自动化和 AI 来加快攻击速度，隐藏在海量复杂数据中，并在云、身份和 SaaS 环境中发起日益复杂的多阶段攻击。要防御现代企业，安全团队需要一种能够处理 PB 级遥测数据、具备持续上下文和自动化智能的架构。

传统 SIEM 建于十多年前，围绕有限的数据接入、严格的采样取舍、僵化的计算架构和手动告警分诊而设计。受制于高昂的计算成本和缺乏弹性的处理能力，这种传统方法根本无法扩展以防御 AI 驱动的威胁和快速的零日攻击。行业需要一种新的范式。Databricks 通过安全数据湖仓确立了这一范式：一个开放、受治理的数据湖仓，将安全、IT 和业务数据统一在一个地方，使 SOC 团队能够直接在该数据之上运行检测、调查和响应。

今年早些时候，Databricks 推出了 Lakewatch，作为构建在安全数据湖仓之上的 Agent 型 SIEM。今天，Panther 的加入将成熟、经过验证的运营 SOC 工作流和 100 多个开箱即用的集成直接带到 Lakewatch 的开放数据基础之上，极大地加速了安全数据湖仓愿景的实现。

## 为什么传统 SIEM 在 Agent 时代力不从心

多年来，安全团队一直被迫在不可能的两难中做出选择：要么接入所有数据，承受不断攀升的 SIEM 成本和嘈杂的输出；要么减少接入以控制成本，却在覆盖范围上留下缺口。当告警触发时，分析师不得不在互不关联的工具之间来回切换，手动拼接来自云服务、端点、身份提供商和 SaaS 应用的日志。

安全数据湖仓通过打破数据孤岛，将安全、IT 和业务遥测数据统一在开放、受治理的架构中，消除了这种两难。借助 Lakewatch 和 Panther，安全团队不再需要在丰富的数据规模和快速可执行的工作流之间做出选择。他们从第一天起就能两者兼得。

## Lakewatch：开放数据基础

Lakewatch 是支撑安全数据湖仓基础的核心产品，提供运营 Agent 型 SOC 所需的高保真、开放数据生态系统。它使组织能够以开放的湖仓格式，将 PB 级安全遥测数据与 IT 和业务数据无缝地收集、治理和分析。借助 Lakewatch 和 Panther 的协同工作，安全团队不再仅仅收集数据——他们可以部署经过验证的自主 AI Agent，主动进行告警分诊、威胁狩猎，并持续优化检测逻辑。

通过在 Databricks Data + AI 平台上原生运行，Lakewatch 提供：

- **PB 级数据留存：** 留存数月或数年的高保真遥测数据，而无需承担高昂的 SIEM 许可费用或被迫进行数据采样，为 AI Agent 提供检测复杂多阶段攻击所需的完整历史深度。
- **统一上下文：** 将安全事件直接与 HR 记录、资产清单和业务数据等企业上下文关联。通过将 Panther 的 AI Agent 直接集成到 Lakewatch 中，这种丰富的上下文为深度自动化分诊提供支持，带来更高的信号质量和更少的误报。
- **开放标准：** 使用 OCSF、Spark、Unity Catalog、Delta、Parquet 和 SQL 保持对组织安全数据的所有权和治理权。这避免了专有锁定，同时确保您的遥测数据可被 AI 工具即时访问。
- **Agent 就绪：** 安全、IT 和业务数据以开放格式共存，使受治理的实时数据可立即供 Panther 的生产级 AI Agent 使用，以自动化调查、生成检测即代码，并简化 SOC 运营。

## Panther：加速安全数据湖仓愿景

Panther 弥合了原始湖仓数据与实时安全执行之间的差距。Panther 专为现代云原生团队而设计，将软件工程实践和深度检测逻辑与原生嵌入数据层的 AI 工作流相结合。安全团队不再局限于基本的告警摘要，而是可以部署智能 Agent，以机器速度主动调查事件、起草检测规则并执行响应操作。

### Panther 为安全数据湖仓带来的关键能力：

- **检测即代码：** 用检测工程取代手动管理的 SIEM 规则和不受治理、以 UI 为中心的工作流。安全工程师通过标准 CI/CD 管道编写、测试、版本控制和部署检测即代码，将软件工程严谨性引入威胁检测。
- **100+ 开箱即用集成：** 覆盖主要云提供商（AWS、Microsoft Azure、Google Cloud）、身份系统（Okta、Entra ID）、SaaS 应用和端点的深度解析连接器，确保即时实现价值。
- **AI 原生分诊与调查：** 自动化、Agent 型的分诊工作流实时丰富告警信息，在分析师打开工单之前就将原始遥测信号转化为可操作的上下文。当其他安全工具将 AI 视为外挂的聊天机器人时，Lakewatch 提供真正的原生 Agent 工作流：AI Agent 持续从分析师反馈中学习，自动化规则优化，将您的团队从告警处理者提升为战略工程师。

## 强强联合：重塑安全运营

当您将 Lakewatch 开放的 PB 级数据基础与 Panther 软件驱动的工作流层相结合时，对日常安全运营的实际影响是变革性的。Databricks 和 Panther 将共同简化检测与响应的整个生命周期：

- **无缝接入与标准化：** 安全团队不再需要管理复杂的自定义 ETL 管道，而是可以利用 100 多个开箱即用的连接器，将标准化遥测数据直接送入 Lakewatch 的开放数据存储。
- **安全导向的检测工程：** 检测以代码形式直接针对存储在 Lakewatch 中的 PB 级遥测数据运行。安全团队可以通过自动化 CI/CD 管道编写、单元测试、版本控制和部署检测规则，消除专有 SIEM 语言的维护负担。
- **加速的信号到上下文分诊：** 当检测到威胁时，原生 Agent 型 SOC 能力会在整个安全数据湖仓中自动触发。通过在 PB 级数据基础之上直接部署 AI 分诊 Agent，平台即时关联云日志、身份信号和业务上下文。分析师收到的是完整丰富、可操作的事件摘要，而非告警洪流，大幅缩短了驻留时间并减少了分析师倦怠。

## 以开放性和客户控制为基石

除了技术能力之外，Databricks和Panther还共享一个基本信念：客户必须拥有自己的数据。传统SIEM供应商的商业模式建立在专有数据格式和高昂的数据接入费用之上。Databricks和Panther则致力于构建开放生态系统。存储在安全数据湖仓中的安全遥测数据，在整个企业技术栈中保持可访问、可治理且可互操作。安全团队以开放格式完全保有对自身数据的所有权，使他们能够使用最优秀的工具无缝分析遥测数据，不受任何摩擦或人为障碍的限制。

## 共同构建安全的未来

Databricks和Panther携手，为现代Agent（智能体）驱动的安全运营中心提供了完整蓝图。Lakewatch提供了开放的、PB级的数据基础，而Panther则提供了基于该数据采取行动的Agent（智能体）自动化引擎。由此打造出一个自我完善的安全组织，能够从容应对现代威胁的速度和规模。

通过将原生Agent（智能体）工作流直接引入安全数据湖仓，Databricks为防御者提供了超越现代威胁所需的规模、自动化和速度。我们很高兴欢迎Panther团队加入Databricks，共同在Agent（智能体）时代重新定义安全运营。

### 获取最新文章

订阅我们的博客，最新文章将直接发送至您的邮箱。

---

> 本文由AI自动翻译，原文链接：[Databricks Completes Acquisition of Panther: Accelerating the Security Lakehouse Era](https://www.databricks.com/blog/databricks-completes-acquisition-panther-accelerating-security-lakehouse-era)
> 
> 翻译时间：2026-08-06 05:12
