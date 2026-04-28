---
title: LangGuard用Lakebase实现Agent治理
title_original: 'Inside one of the first production deployments of Lakebase: LangGuard''s
  agentic workflow governance engine'
date: '2026-04-27'
source: Databricks Blog
source_url: https://www.databricks.com/blog/inside-one-first-production-deployments-lakebase-langguards-agentic-workflow-governance-engine
author: ''
summary: 文章介绍了LangGuard如何利用Databricks Lakebase构建Agent工作流治理引擎。当前仅不到10%的企业能安全大规模部署自主AI
  Agent，主要原因是Agent运行时自行生成逻辑，绕过传统安全控制。LangGuard通过GRAIL™数据架构实时捕获Agent行为并执行策略，而Lakebase作为无服务器Postgres数据库，提供弹性伸缩至零的计算能力和低延迟查询，完美匹配Agent行为突发性强的特点，为生产级Agent治理提供了基础设施支撑。
categories:
- AI基础设施
tags:
- Agent治理
- Lakebase
- 运行时执行
- 无服务器数据库
- Databricks
draft: false
translated_at: '2026-04-28T05:34:33.676379'
---

- 不到10%的企业已成功大规模部署自主AI Agent（智能体），主要原因在于Agent在运行时自行生成逻辑，绕过了传统安全控制，形成了无形的治理缺口。
- Databricks通过Unity Catalog和AI Gateway为数据、模型和访问策略提供统一治理。LangGuard在此基础上扩展了平台级控制，为Agent工作流增加了运行时执行层——跨端到端的行动、决策、工具和凭证链条进行监控与策略执行。它采用正在申请专利的GRAIL™数据架构，将每个Agent行为捕获到实时知识图谱中，并在不影响Agent性能的前提下实时评估每项策略决策。
- Databricks Lakebase是业界首个完全托管、无服务器的Postgres数据库，构建于湖仓一体架构之上，正是这一能力使其成为可能。它提供弹性伸缩至零的计算能力、针对热操作数据的低延迟查询执行，以及用于安全治理策略测试的即时数据库分支功能。

## Agent AI的隐形问题

大多数企业正在尝试自主AI Agent。但极少有企业能安全地大规模部署它们。根据麦肯锡2025年11月发布的《2025年AI现状》调查，在任何业务职能中，将AI Agent规模化投入生产的企业比例均未超过10%。失败的原因很少是缺乏雄心，而是缺乏可见性。

与传统软件不同，自主Agent会即时自行生成逻辑。它们绕过传统安全监控，以事后难以审计的方式调用工具和访问数据，并在复杂的多Agent工作流中运行——其中任何一个配置错误的权限或策略漏洞都可能引发重大安全事件。企业需要一种新型控制基础设施：一种在决策做出时而非损害发生后就能发挥作用的基础设施。

这正是LangGuard旨在解决的问题。

## 运行时执行与平台治理的结合

LangGuard充当Agent工作流的运行时执行层，监控并执行跨端到端行动、决策、工具、凭证和意图链条的策略，覆盖Agent所触及的每个系统。Databricks通过Unity Catalog和AI Gateway（数据、模型和访问策略的记录系统）提供统一治理。当企业将Agent部署到生产环境时，工作流本身也需要一个运行时执行层，将这些平台级控制扩展到Agent执行的每一步。这正是LangGuard的定位所在。LangGuard的治理引擎GRAIL™（治理AI运行时链接）数据架构将每个Agent行为捕获为多维追踪数据，并构建工作流行为与上下文的实时知识图谱。当Agent尝试调用工具、访问数据集或调用模型时，LangGuard会在执行前根据策略评估该行为，覆盖工作流所触及的每个系统，无论其在何处运行。

企业级Agent生产部署的规模使这一任务极具挑战性。单个工作流可能涉及数十个协调Agent、数百次工具调用、多个基础模型，以及跨越十五个以上企业记录系统管理的策略，包括ServiceNow等IT工单系统、IAM和IDP平台、Salesforce等CRM系统、Workday等HR平台、Wiz和CrowdStrike等云安全平台、TalkDesk等联络中心平台、MCP网关和API网关。在不影响Agent性能的前提下实时治理这一切，需要专为此问题构建的基础设施。

## 为何选择Lakebase

LangGuard团队曾花费多年构建IBM QRadar——多次位列Gartner魔力象限领导者、全球部署最广泛的企业SIEM平台之一。QRadar在严格的延迟和可靠性要求下，每天摄取并关联PB级的安全遥测数据。这段经历让我们学到了一个深刻的教训：数据库架构决定命运。在设计LangGuard的工作流治理引擎时，我们面临了之前解决过的同样挑战：以不可预测、高强度突发方式到达的操作安全数据，其中每毫秒的决策延迟都至关重要，而闲置基础设施成本不可接受。传统将计算与存储耦合的数据库迫使你为峰值负载进行配置，并全天候为这种容量付费。Lakebase的无服务器模型完全解耦计算与存储，并在突发之间伸缩至零——这正是我们在构建QRadar时一直需要却无法获得的答案。它与问题完美匹配。

## Lakebase为何是合适的选择

Lakebase是一种新型操作数据库架构，它将计算与存储分离，使计算能够随工作负载需求弹性伸缩，而持久状态则独立存在于复制的存储层中。基于PostgreSQL的开放基础，Lakebase架构保留了开发者在成熟关系型数据库中所依赖的一切，同时消除了使传统单体RDBMS不适合现代应用、Agent和AI所需速度与规模的基础设施限制。

### 无服务器自动伸缩与伸缩至零

Agent行为以突发性著称。一个Agent工作流可能数小时完全休眠，然后突然在几秒内生成数百次追踪写入和执行读取。Lakebase会在这些追踪数据涌入我们系统的确切时刻动态配置计算资源，并在活动停止时完全关闭。由于持久状态存在于存储层而非计算节点中，启动新的计算实例无需数据移动。它只需连接到现有数据库历史，即可立即开始服务查询。

对于一家以企业规模运营的初创公司而言，这正是基础设施与实际使用量匹配与因静默期而受罚之间的区别。我们的运营成本与所服务的实际工作负载完美对齐。

### 热操作数据的毫秒级读取延迟

对任何分离式数据库的自然担忧是读取延迟。Lakebase通过在计算与存储之间引入缓存层来解决这一问题，该缓存层使热数据靠近计算。

对于LangGuard的执行查询——针对GRAIL™上下文和策略表的紧密索引查找——我们预计活跃工作集能够舒适地容纳在计算本地内存中。这种架构让我们有信心以工作流速度执行治理决策，而不会给Agent执行增加有意义的延迟。

### 用于治理策略测试的即时数据库分支

对于治理产品而言，Lakebase的即时数据库分支是其最具操作价值的特性之一。当我们创建分支时，不会物理复制任何数据。分支使用写时复制语义从当前数据库状态分叉，仅消耗新数据或修改数据的存储空间。我们的开发者可以在几秒内创建生产追踪数据的隔离精确副本，针对真实Agent行为测试新的治理策略，并验证执行逻辑，而无需冒影响实时环境稳定性的风险。

### PostgreSQL：久经考验的基础

Lakebase构建于PostgreSQL之上——全球最先进的开源关系型数据库，在各大行业经过数十年生产环境考验。对LangGuard而言，这意味着与我们团队已知的工具、库和扩展完全兼容，无需使用专有查询语言或承担迁移风险。

![PostgreSQL](/images/posts/c7b79dd72f49.png)

## LangGuard与Databricks如何协同工作

LangGuard与Databricks联合架构旨在端到端管控企业级Agent工作流，同时将所有运营数据保留在单一、可信的数据与AI平台上。架构左侧是企业级Agent工作流本身：AI Agent及其编排器与数十个记录系统（如IT服务管理、CRM、HR、身份认证、安全、联络中心及API/MCP网关）进行交互。每个Agent动作、工具调用及数据访问请求都会生成丰富的追踪事件，实时流入LangGuard。

图表中央是LangGuard治理工作流引擎，由正在申请专利的GRAIL™数据编织技术驱动。GRAIL将每个Agent动作捕获为多维追踪数据，并构建工作流行为与上下文的实时知识图谱。当Agent尝试调用工具、访问数据集或调用模型时，LangGuard会基于实时上下文及相关治理规则进行策略评估，在动作执行前返回允许/拒绝/修改决策。这为企业提供了单一控制点，可对工作流所触及的每个系统强制执行策略，无论底层Agent运行在何处。

右侧的Databricks Lakebase作为LangGuard追踪与策略数据的运营记录系统。Lakebase采用无服务器PostgreSQL架构，将计算与存储分离，实现弹性自动扩缩容及Agent活动突发期间的缩容至零，同时将热运营数据保留在靠近计算节点的低延迟缓存中。LangGuard持续将追踪事件写入Lakebase，并执行低延迟读取以进行治理策略查询与上下文检索，确保在不预置过多数据库容量的前提下，以工作流速度做出执行决策。

由于LangGuard的运营数据原生驻留在Lakebase中，无需额外ETL即可立即供更广泛的Databricks数据智能平台用于分析与AI。Databricks AI、模型服务及MLflow可直接基于GRAIL追踪数据训练并部署异常检测模型，识别偏离既定行为基线的Agent。这些预测信号反馈至LangGuard治理引擎，形成实时执行与预测监控之间的闭环，使企业能够在单一平台上从被动控制转向主动的、基于行为的AI治理。

## 下一步：面向Agent工作流的预测性治理

LangGuard引擎目前可在运行时跨完整工作流执行既定策略。下一步演进方向是预测性：基于历史GRAIL追踪数据训练行为模型，在异常Agent行为表现为策略违规之前进行检测。

由于我们的运营追踪数据已驻留在Databricks生态系统中（如上所述），无需构建单独的ETL管道或搭建第二个分析平台，即可直接从执行转向预测。

如果某个Agent开始行为异常或偏离既定基线，这些模型将在造成任何损害之前将其标记为异常。这种实时执行与预测性机器学习的融合，正是企业AI治理的未来，也是我们正在构建的架构。

准备好端到端管控您的Agent工作流了吗？请访问langguard.ai了解LangGuard如何以完整策略合规性保障、控制并运营企业级Agent工作流，或探索Databricks Lakebase，了解无服务器OLTP基础设施如何大规模支撑实时AI治理。

了解更多关于LangGuard的信息探索Databricks Lakebase

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章直接发送至您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Inside one of the first production deployments of Lakebase: LangGuard's agentic workflow governance engine](https://www.databricks.com/blog/inside-one-first-production-deployments-lakebase-langguards-agentic-workflow-governance-engine)
> 
> 翻译时间：2026-04-28 05:34
