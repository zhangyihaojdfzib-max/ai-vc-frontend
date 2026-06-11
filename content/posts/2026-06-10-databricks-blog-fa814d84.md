---
title: Databricks存储生态：治理企业数据，无论它在哪里
title_original: 'Announcing the Databricks storage ecosystem: Governing the enterprise
  data estate, wherever it lives'
date: '2026-06-10'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-databricks-storage-ecosystem-governing-enterprise-data-estate-wherever-it-lives
author: ''
summary: Databricks推出存储生态系统，通过OpenSharing协议将本地、私有云和边缘存储平台原生连接至其数据智能平台。该方案采用零拷贝架构，企业无需迁移数据即可在本地数据集上运行无服务器计算、Genie和LLM，实现集中式数据治理和生成式AI扩展。文章指出，企业正从“迁移一切”转向“治理一切”，数据主权、成本、延迟和暗数据AI需求驱动了这一转变。首批合作伙伴包括MinIO等存储提供商。
categories:
- AI基础设施
tags:
- Databricks
- 数据治理
- 混合云
- OpenSharing
- 存储生态
draft: false
translated_at: '2026-06-11T06:49:49.058605'
---

- 挑战：企业需要在本地、私有云和边缘环境中保留海量数据，以满足严格的数据主权和监管要求、维持边缘低延迟或应对巨大的数据引力——同时还要将现代云AI和治理能力引入这些环境。
- 定义：Databricks存储生态系统利用OpenSharing协议，将混合云和本地存储平台原生连接到Databricks。这使得企业能够建立集中式数据治理，并在整个混合基础设施上扩展生成式AI。
- 成果：采用零拷贝架构，企业无需复制任何文件，即可直接在本地数据集上运行Databricks无服务器计算、Genie和LLM（大语言模型）。这能瞬间将孤立数据转化为活跃的、可用于AI的资产，以支持高级用例，例如在机密工程数据上训练模型或就地分析网络遥测数据。

## 无法迁移的数据

多年来，企业数据策略很简单：将所有数据迁移到云端。将数据湖和数据仓库迁移到云端，治理问题随之解决。这是一个清晰的故事——直到它不再成立。

如今，一些全球最先进的企业明确告诉我们：它们不能——也不会——将所有数据迁移到云端。领先的半导体制造商正在使用绝不能离开本地的工程机密数据集训练模型。全球贸易公司拥有海量历史行情数据，其云端出口的经济成本使得迁移不可能实现。一级银行已采用“永久混合”策略，在现代化本地存储的同时维持严格的数据主权。大型制药公司每天在PB级本地数据资产上运行数百万次药物实验，这些数据受到严格监管。

这些并非边缘案例。它们代表了企业看待数据的结构性转变：从“迁移一切”转向“治理一切”。

驱动因素真实且不断叠加：

- 数据主权与监管：金融服务、医疗保健和政府机构必须遵守GDPR、HIPAA、NIS2以及特定行业的数据驻留规则，要求数据保留在特定司法管辖区或隔离环境中。对于某些数据集，云迁移并非可选，而是法律禁止。
- 数据引力与成本：在PB级和EB级规模下，云迁移的经济性完全失效。出口费用、存储成本以及庞大的数据量使得“一次性迁移”模式在财务上不可持续。一些全球最大的零售商正是出于这个原因，正在将分析工作负载从云端迁回本地基础设施。
- 延迟与边缘工作负载：零售、制造和电信工作负载需要低延迟访问本地和边缘数据。电信提供商每天在本地摄取海量网络遥测数据，以支持无法容忍云端往返延迟的AI驱动网络运营。
- 暗数据上的AI：企业内海量的备份数据、非结构化归档和辅助数据集（总计达数百EB）蕴含着巨大的AI价值，但由于治理未能覆盖而从未被解锁。

信号清晰无误。我们已收到数百名客户的请求，明确要求将本地和混合存储连接至Unity Catalog。软件定义存储（SDS）市场在2026年将达到数千亿美元规模，而管理这些资产的企业合作伙伴（共同管理超过2ZB的数据）正在与我们共同构建。

## 推出Databricks存储生态系统

今天，我们激动地宣布推出Databricks软件定义存储（SDS）生态系统——这是一个全新的合作伙伴类别，旨在将Databricks智能平台带到企业数据所在的任何地方：本地、私有云和边缘环境。如果您是当前在这些平台上运行PB级数据的企业，您不再需要在现有的非云存储基础设施和Databricks AI之间做出选择。

该生态系统的核心是OpenSharing，一个用于安全、受控数据共享的开源协议。我们的存储合作伙伴正在实施OpenSharing服务器，以将其数据资产直接暴露给Databricks无服务器计算。路径很简单：存储合作伙伴建立一个OpenSharing端点，您将其连接到Unity Catalog，即可立即在Databricks中安全、受控地访问您的本地数据，无需数据迁移。

此集成在整个混合环境中提供了一个统一的目录。客户现在可以使用Databricks无服务器计算、Genie、AgentBricks和模型训练来查询和推理从未离开本地的数据。结果是：零数据移动、无数据重复、零合规风险。

这并非路线图上的愿景。客户今天即可试用这些集成。构建这些集成的合作伙伴遵循合作伙伴良好架构框架——一份涵盖架构、安全和认证标准的技术蓝图。

![OpenSharing示意图](/images/posts/575ac19e86ef.png)

## 我们的首发合作伙伴

我们自豪地宣布与以下领先存储提供商达成集成：

![Databricks存储生态系统](/images/posts/77b284accfbc.png)

### MinIO — 正式发布（演示，博客）

MinIO AIStor是一座桥梁，无缝连接Databricks数据智能平台与无法迁移到云端的企业数据。通过在存储层原生实现开放的OpenSharing协议，AIStor消除了复杂性，使Databricks客户能够在完整的Unity Catalog治理下，高效查询实时的本地Apache Iceberg™️和Delta表。它将无服务器计算、Genie和AgentBricks扩展到本地数据，将Databricks平台的全部能力带给企业最关键的数据。

### Everpure（原Pure Storage）— 私有预览（演示，博客）

Everpure和Databricks使组织能够直接在云端使用本地数据，无需数据复制或重复。这是通过一个OpenSharing连接器实现的，该连接器以安全且受控的方式，桥接了对象存储中的数据与Databricks核心工作区。

### Qumulo — 2026年7月私有预览（博客）

Qumulo已将其新的NeuralSearch与OpenSharing集成，允许客户安全地将Qumulo存储的数据与Databricks共享，覆盖核心、云端和边缘环境——无需复制、额外成本或复杂性。通过NeuralSearch，用户可以通过自然语言查询发现相关数据集（包括非结构化内容），并通过OpenSharing将这些精选表无缝共享给Databricks。

### VAST Data — 2026年8月私有预览

VAST Data正在扩展VAST AI操作系统，加入OpenSharing支持，以帮助企业桥接Databricks工作流与驻留在本地和混合基础设施中的数据——无需大规模数据移动或迁移。该集成将为客户提供更大的灵活性，以便在云端、数据中心和新兴AI基础设施环境中访问、处理数据并将其投入运营，同时支持现代混合AI和分析工作负载。

## 下一步计划

### 即将推出的集成

除了我们的首发合作伙伴，存储生态系统的势头持续加速。我们已获得Cohesity、Commvault、HPE、NetApp、Nutanix和Rubrik的承诺——将在年底前构建原生集成。

这些合作伙伴与首发合作伙伴一起，共同管理着数百EB的企业数据，涵盖高性能非结构化媒体、二级备份归档、经济高效的云存储以及超融合私有云资产。

### 解锁非结构化数据

今天的发布建立了结构化表格数据在整个生态系统中的全面治理与可访问性。但我们深知，真正的机遇在于非结构化数据：图像、PDF、视频、医学扫描、工程仿真以及备份归档——这些构成了企业所管理数据的主体，也是下一代RAG（检索增强生成）流水线和微调模型的原材料。

我们正积极致力于通过Volumes API扩展OpenSharing协议——将本地存储中的非结构化文件直接暴露给Databricks，用于生成式AI工作负载。随着这一功能的推出，管理海量非结构化资产（从媒体与影像归档到企业备份存储库）的合作伙伴，将为其客户解锁全新类别的AI应用场景。

这正是"治理一切"的真正含义。

## 加入生态系统

如果您是有意构建OpenSharing集成的存储供应商，请访问合作伙伴良好架构框架，或联系Databricks合作伙伴团队以获取入门指导。

如果您是希望将本地存储资产连接到Databricks的企业客户，请联系您的客户团队了解更多信息。

"迁移一切"的时代已经终结。"治理一切"的时代从今天开始。

### 在收件箱中获取最新文章

订阅我们的博客，即可将最新文章直接发送至您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Announcing the Databricks storage ecosystem: Governing the enterprise data estate, wherever it lives](https://www.databricks.com/blog/announcing-databricks-storage-ecosystem-governing-enterprise-data-estate-wherever-it-lives)
> 
> 翻译时间：2026-06-11 06:49
