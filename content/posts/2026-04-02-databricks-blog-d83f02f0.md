---
title: Unity Catalog业务语义正式发布并开源，构建统一开放的语义基础
title_original: Announcing General Availability and Open Sourcing of Unity Catalog
  Business Semantics
date: '2026-04-02'
source: Databricks Blog
source_url: https://www.databricks.com/blog/redefining-semantics-data-layer-future-bi-and-ai
author: ''
summary: Databricks宣布Unity Catalog业务语义正式发布并开源其核心实现。该方案旨在解决传统业务语义层分散、专有且对AI不灵活的问题，通过在数据平台核心建立统一、开放的语义定义。它允许企业一次定义业务概念（如KPI），即可在BI工具、开发工作流和AI智能体中一致复用，并继承底层数据的治理与安全策略。此举旨在消除数据理解分歧，提升AI时代的数据可信度与敏捷性。
categories:
- AI基础设施
tags:
- 数据治理
- 业务语义
- 开源
- Databricks
- AI智能体
draft: false
translated_at: '2026-04-04T04:31:02.647818'
---

随着数据和人工智能成为每家企业的核心，对业务概念形成统一理解至关重要。分析师、工程师、高管以及如今的AI智能体，常常对相同数据做出不同解读，导致指标漂移、报告冲突和信任度下降。

多年来，这些业务概念一直存在于BI工具和仪表板中。在智能体AI时代，当智能体基于数据进行推理并自主行动时，分散的定义不仅会造成混乱，还会使其规模化扩散。企业需要在数据和AI平台的核心建立统一的语义基础，一次定义，处处应用。而且它必须是开放的。业务语义定义了组织如何衡量收入、增长、客户价值和风险。这些定义是战略资产，不能被锁定在专有系统中，或局限于单一应用层。

今天，我们通过**Unity Catalog业务语义的正式发布**来改变这一现状。这是一个统一且开放的语义基础，可在BI仪表板、开发者工作流和AI智能体之间提供一致、可信的上下文。为使这一基础真正可移植，我们还将其在Apache Spark中的核心实现开源，并将在**Unity Catalog OSS v0.5**中提供支持。

## 为何传统的业务语义方法存在不足

长期以来，客户使用特定于BI工具的语义层来确保该工具内部的一致性，但这种方法存在局限性：

*   **专有且分散**：在多工具、多智能体的环境中，每个BI模型都使用自己的语言。结果，定义被锁定在仪表板、模型和电子表格中，使得跨组织进行治理、执行访问策略或追溯血缘关系几乎不可能。
*   **定义过于下游**：因为这些层位于展示层而非数据基础层，团队需要为不同的仪表板和报告反复重新定义相同的指标。这种下游方法使得语义变得脆弱、不一致且难以扩展。
*   **对AI不灵活**：传统层依赖于繁重的前期建模，无法跟上快速变化的业务问题或AI智能体的开放式提示词。每次变更都需要专家干预，拖慢响应速度并削弱信任。

这些局限性长期困扰着数据和AI团队。在当今以AI驱动的环境中，敏捷性和可信答案不容妥协，它们已成为发展的关键障碍。

## Unity Catalog业务语义：统一且开放的业务语义方法

Unity Catalog业务语义代表了一种根本性的转变，因为语义现在在Databricks数据智能平台的核心实现了统一和治理。它直接构建在Unity Catalog中，扩展了您所依赖的相同治理、安全和血缘功能，并使这些定义在您工作的任何地方都可用。

这种方法带来三个关键优势：

1.  **开放且可复用**：通过SQL和API访问，业务语义可在仪表板、Notebook、应用程序和AI智能体中进行查询。以开放格式存储，它们完全可移植，不局限于专有工具。
2.  **核心治理**：继承与底层数据相同的治理策略。这种上游方法确保了一致的使用、治理、血缘和访问控制，为数据和业务含义提供单一可信来源。
3.  **为AI设计**：丰富的语义元数据提供了智能体准确回答新问题以及随业务概念演变而适应所需的上下文，无需繁重的前期建模。

![Unity Catalog业务语义](/images/posts/e0790cca027d.png)

## 业务语义的开源基础

**Unity Catalog业务语义**的一个关键目标是确保客户能够以开放、可移植且旨在跨其现有生态系统工作的方式定义业务含义，避免锁定。语义定义应能与BI工具、SQL工作负载和AI智能体无缝集成，并随着平台和消费模式的发展而保持持久性。

为实现这一点，我们正在Apache Spark OSS中开源核心的Metric View实现，目标是在即将发布的Apache Spark版本中提供（您可以在**SPARK-54119**中关注进展），并将在**Unity Catalog OSS v0.5**中提供支持。这使得客户能够在开放系统中使用标准SQL定义业务语义，在数据基础层进行治理，而非嵌入下游工具，并在分析和AI界面中一致地复用。

Databricks也支持更广泛的行业努力，以改善业务语义的互操作性。公司已加入**开放语义交换（OSI）** 倡议并积极参与其中。我们认为像OSI这样的倡议是迈向生态系统对齐的重要一步，并将做出相应贡献，同时继续专注于构建一个开放的、受治理的、客户可以大规模信赖的语义基础。

## 解读正式发布版的新功能

### Metric Views：可信、一致的KPI

本次正式发布的核心是**Metric Views**，它通过显示名称、格式、同义词等语义元数据，为业务KPI建立可信、一致的定义，帮助人类和AI自信地解读和应用这些定义。Metric Views允许您用SQL集中定义数据映射、度量和维度，并在Unity Catalog中直接治理它们。然后，这些定义可以在每个界面上移植：AI/BI仪表板、Genie、Notebook、SQL应用程序以及连接到Databricks的第三方工具。由于每个指标都是声明式定义的，引擎在查询时会确定性地编译和执行底层SQL，确保每个使用者，无论是人类还是AI智能体，都能从相同的定义获得相同的结果，无论他们如何或在何处访问它。

#### 新功能：

*   **物化以提升查询性能**：Unity Catalog业务语义通过物化，将受治理的定义与大规模性能相结合。它无需团队决定使用哪个聚合表、为不同性能层级重复逻辑或为不同工作负载构建单独的管道，语义层会自动处理性能。具体方式如下：
    *   **自动预聚合**：当您为指标定义物化时，平台会自动维护优化的预聚合结果，无需人工干预。
    *   **增量刷新**：物化结果通过增量更新保持最新，因此指标永远不会过时，很少需要完全重新计算。
    *   **智能查询重写**：在查询时，引擎会重写查询以利用最佳的可用物化。
    *   **透明路由**：用户以一贯的方式查询指标，而系统则在后台将每个请求路由到最快的路径。

物化功能目前处于预览阶段，了解更多信息，请参阅文档（[AWS](https://docs.databricks.com/en/sql/language-manual/sql-ref-metric-views.html), [Azure](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-metric-views), [GCP](https://docs.gcp.databricks.com/en/sql/language-manual/sql-ref-metric-views.html)）。

*   **通过新UI和智能体AI体验进行创作**：现在，在公开预览中，您可以通过Unity Catalog Explorer中新的点击式UI创建和管理Metric Views，使技术和非技术用户都能进行语义建模，无需复杂的SQL或深厚的数据建模专业知识。该UI允许您可视化地定义表之间的关系、内联绘制指标图表，并在发布前进行端到端测试，所有这些都无需离开浏览器。了解更多关于基于UI的创作，请参阅文档（[AWS](https://docs.databricks.com/en/sql/language-manual/sql-ref-metric-views.html), [Azure](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-metric-views), [GCP](https://docs.gcp.databricks.com/en/sql/language-manual/sql-ref-metric-views.html)）。

**Genie Code**通过将智能体AI直接引入创作工作流，进一步加速了创作过程。它无需从空白页开始，而是可以：

- **更快地构建语义模型**：提供度量指标、维度、同义词和文档建议，让团队在几分钟内即可上手，而无需耗费数周时间。
- **优化与重构**：识别现有定义中的问题，并在业务逻辑演进时推荐改进方案。
- **验证变更**：基于真实数据测试拟议的修改，从而在错误扩散前及时发现。
- **实现精细化的变更管理**：审查并批准单个指标变更，全面了解变更内容及原因。

指标视图不仅限于定义关键绩效指标。每个指标视图都包含丰富的语义元数据、显示名称、格式和同义词，使其易于人类和AI理解与使用，确保在仪表板和对话式界面中呈现一致，同时帮助AI正确解读业务术语和自然语言查询。

## 业务语义如何赋能Databricks AI/BI

随着此次正式发布，AI/BI仪表板和Genie现已与Unity Catalog业务语义完全集成。实际上，这带来了三大关键优势：

1. **基于受治理指标的AI/BI仪表板**：您现在可以直接在Unity Catalog的指标视图上构建仪表板。每个可视化图表、筛选器、下钻和比较都使用同一套经过认证的度量指标和维度，确保跨团队和工具的数据一致性。
2. **基于业务语言的Genie**：Genie空间可以直接建立在指标视图之上，这意味着Genie回答的每个自然语言查询都基于受治理的确定性定义，而非推断逻辑。由于指标视图在运行时被编译为逻辑查询，用户总能获得正确、一致的结果。Genie不再"幻觉"指标，而是从单一可信源解析它们。
3. **将仪表板逻辑提升至语义层**：在创建新的AI/BI仪表板时，若没有现成的指标视图，您构建的任何表连接、筛选器或计算字段现在都可以一键提升为Unity Catalog中的新指标视图。它将立即成为您组织语义层的一部分，可在Genie、SQL、笔记本和外部BI工具中使用。此外，您的仪表板将自动受益于指标视图的物化，显著提升底层查询性能。

## 将语义扩展至您喜爱的工具

强大的语义基础在跨平台使用时价值更为凸显。正因如此，我们与丰富的技术合作伙伴生态系统紧密合作，他们直接集成了Unity Catalog业务语义。

![Unity Catalog业务语义合作伙伴生态系统](/images/posts/c745fce86d69.png)

- **Tableau**：Tableau计划在其关系数据模型中增加对外部指标提供商（包括Databricks Unity Catalog业务语义）委托语义的支持。这将确保分析师可以信任指标由底层语义层一致定义和准确聚合。集成预计于2026年底推出。Tableau很高兴将Unity Catalog业务语义引入我们的关系数据模型，让分析师和组织能够一次性定义指标和元数据，并由Tableau自动应用正确的语义，以获得一致、可信的洞察。—— Nicolas Brisoux，Tableau高级产品总监
- **Sigma Computing**：Sigma通过实时查询指标视图直接与Databricks Unity Catalog业务语义集成，确保最新定义即时反映而无需移动数据。这种架构使Sigma能够作为您湖仓平台的透明延伸，在执行点严格继承Unity Catalog的安全和治理协议。在Sigma，我们正努力与Unity Catalog业务语义集成，因为它让我们的客户能将Sigma类电子表格的体验与受治理的业务定义相结合，确保为每个人提供快速、一致且可信的分析。—— Jordan Stein，Sigma产品经理
- **ThoughtSpot**：今年晚些时候，ThoughtSpot将增加对Unity Catalog指标视图的原生支持，让Spotter用户能够用自然语言即时查询受治理的Databricks指标。这消除了自定义SQL的需求，并让组织能够灵活、准确、快速地访问其数据栈中可信的业务指标。ThoughtSpot很高兴通过Unity Catalog业务语义深化与Databricks的合作，让客户在管理和使用业务语义的方式和地点上拥有更大的灵活性。—— Francois Lopitaux，ThoughtSpot产品高级副总裁
- **Hex**：Unity Catalog指标视图现已完全集成到Hex中。用户可以直接从Databricks连接浏览指标视图，在Hex笔记本中用SQL查询它们，并构建基于受治理定义的数据应用。这使得从探索到生产应用的过渡更加顺畅，无需重新定义指标。

Tableau：Tableau计划在其关系数据模型中增加对外部指标提供商（包括Databricks Unity Catalog业务语义）委托语义的支持。这将确保分析师可以信任指标由底层语义层一致定义和准确聚合。集成预计于2026年底推出。

Sigma Computing：Sigma通过实时查询指标视图直接与Databricks Unity Catalog业务语义集成，确保最新定义即时反映而无需移动数据。这种架构使Sigma能够作为您湖仓平台的透明延伸，在执行点严格继承Unity Catalog的安全和治理协议。

ThoughtSpot：今年晚些时候，ThoughtSpot将增加对Unity Catalog指标视图的原生支持，让Spotter用户能够用自然语言即时查询受治理的Databricks指标。这消除了自定义SQL的需求，并让组织能够灵活、准确、快速地访问其数据栈中可信的业务指标。

- **Omni**：借助Omni，团队可以通过电子表格、SQL或AI驱动的聊天等熟悉体验来分析指标视图。Omni还支持双向集成，因此在Omni中进行的更新可以推送回Unity Catalog，确保企业内的定义保持一致。这使得数据团队和业务专家都能直接为语义模型做出贡献。将AI植根于业务背景是使其可靠的唯一途径。我们与Unity Catalog指标视图的集成将受治理的定义带入每个界面——AI、电子表格、仪表板和SQL。通过Omni与Databricks之间的双向同步，团队可以在任一系统中定义和更新指标，同时保持一切对齐。这种一致性有助于客户扩展自助服务、加速AI采用，并构建值得信赖的面向客户的数据产品。—— Jamie Davidson，Omni联合创始人

- **Atlan**：Atlan与UC Metrics的原生集成将您最关键的指标直接引入Atlan上下文图谱，将其与血缘关系、所有者和业务定义关联起来，而无需增加任何新的权限开销。这为团队在工作流中提供了单一、可信的指标视图，从而实现更快速的故障排除、更好的决策制定以及规模化AI就绪的数据。指标是每个企业数据与AI平台的命脉。通过将UC Metrics引入Atlan的上下文图谱——附带血缘关系、业务上下文且无需额外权限——我们的客户获得了以往难以企及的运营智能。这是迈向规模化AI就绪数据的重要一步。—— Chandru，Atlan产品负责人

- **Monte Carlo**：Monte Carlo现已支持Unity Catalog中的指标视图，为您提供跨标准化业务指标及其支撑管道的端到端可观测性。可靠的数据和AI始于受治理的业务指标。Unity Catalog Metrics使规模化标准化KPI变得更加容易，借助Monte Carlo，数据领导者可以信赖这些洞察来驱动真正的业务影响。—— Lior Gavish，Monte Carlo联合创始人兼CTO

- **Collibra**：Collibra为您的Databricks指标带来可信的可见性，使人类和AI智能体都能轻松发现并将其用于业务决策。增强的集成改进了指标可视化，允许Collibra批准的指标直接流入Databricks，并添加双向同步以确保整个数据资产中指标的一致性和可靠性。AI智能体和数据用户需要受治理且一致的指标来理解、信任和自动化工作流。我们的共同客户持续期望Databricks与Collibra之间保持紧密协作。—— Tom Dejonghe，Collibra数据治理产品管理副总裁

- **Domo**：现已与Unity Catalog指标视图集成，使受治理的Databricks指标能够直接流入Domo的仪表板、分析和AI驱动的工作流。这减少了重复工作，加强了治理，并加快了基于可信KPI的洞察速度。将Databricks的受治理指标与Domo集成有助于客户减少重复、改进治理，并加速基于可信KPI的洞察。—— Matthew Payne，Domo工程副总裁

- **Anomalo**：Anomalo作为Unity Catalog受治理指标的发布合作伙伴加入，将Databricks的统一语义层与Anomalo的自动化指标监控相结合。此集成帮助企业及早发现漂移和数据质量问题，确保关键决策所用指标的准确性和可信度。通过将Databricks的统一语义层与Anomalo的指标监控相结合，我们帮助客户及早发现漂移，并使其指标在大规模应用中保持准确和可信。—— Amy Reams，Anomalo业务发展与营销副总裁

**Omni**：借助Omni，团队可以通过电子表格、SQL或AI驱动的聊天等熟悉体验来分析指标视图。Omni还支持双向集成，因此在Omni中进行的更新可以推送回Unity Catalog，确保企业内的定义保持一致。这使得数据团队和业务专家都能直接为语义模型做出贡献。

**Atlan**：Atlan与UC Metrics的原生集成将您最关键的指标直接引入Atlan上下文图谱，将其与血缘关系、所有者和业务定义关联起来，而无需增加任何新的权限开销。这为团队在工作流中提供了单一、可信的指标视图，从而实现更快速的故障排除、更好的决策制定以及规模化AI就绪的数据。

**Monte Carlo**：Monte Carlo现已支持Unity Catalog中的指标视图，为您提供跨标准化业务指标及其支撑管道的端到端可观测性。

**Collibra**：Collibra为您的Databricks指标带来可信的可见性，使人类和AI智能体都能轻松发现并将其用于业务决策。增强的集成改进了指标可视化，允许Collibra批准的指标直接流入Databricks，并添加双向同步以确保整个数据资产中指标的一致性和可靠性。

**Domo**：现已与Unity Catalog指标视图集成，使受治理的Databricks指标能够直接流入Domo的仪表板、分析和AI驱动的工作流。这减少了重复工作，加强了治理，并加快了基于可信KPI的洞察速度。

**Anomalo**：Anomalo作为Unity Catalog受治理指标的发布合作伙伴加入，将Databricks的统一语义层与Anomalo的自动化指标监控相结合。此集成帮助企业及早发现漂移和数据质量问题，确保关键决策所用指标的准确性和可信度。

这些以及即将推出的集成共同确保了受治理的一致语义在更广泛的分析和AI生态系统中流动，其影响远不止于Databricks。

## 开始使用Unity Catalog业务语义

我们对此次发布感到无比兴奋。随着语义成为您数据平台的核心部分，企业上下文将无处不在——从仪表板和AI智能体到笔记本和外部BI工具，从而消除指标孤岛、供应商锁定以及跨工具的不一致。基于开放基础构建，您的语义层将在您的数据所到之处发挥作用。探索[文档](https://docs.databricks.com/)（AWS、Azure、GCP），获取关于如何开始定义业务语义、控制权限和各种消费方式的详细指南。探索产品演示，通过AI/BI仪表板和Genie空间查看业务语义的实际应用。

- Unity Catalog指标视图概述
- 在AI/BI中呈现指标视图
- 从SQL编辑器查询指标视图

---

> 本文由AI自动翻译，原文链接：[Announcing General Availability and Open Sourcing of Unity Catalog Business Semantics](https://www.databricks.com/blog/redefining-semantics-data-layer-future-bi-and-ai)
> 
> 翻译时间：2026-04-04 04:31
