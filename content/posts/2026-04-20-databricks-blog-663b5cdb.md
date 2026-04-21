---
title: Databricks与Adobe联手：Delta Sharing集成加速营销数据实时激活
title_original: 'Bridging Data Science and Marketing: Databricks Unveils Delta Sharing
  Integration for Adobe Experience Platform and Agentic Marketing Workflows'
date: '2026-04-20'
source: Databricks Blog
source_url: https://www.databricks.com/blog/adobe-databricks-delta-sharing-agentic-marketing
author: ''
summary: Databricks宣布与Adobe深化合作，通过三项关键进展弥合数据科学与营销执行间的鸿沟：Adobe Experience Platform支持Delta
  Sharing协议，实现对Databricks中受治理第一方数据的零拷贝直接访问；Databricks Genie通过模型上下文协议与Adobe Marketing
  Agent连接，让营销人员在平台内即可获取运营智能；即将推出的Adobe Marketing Agent测试版将支持构建监督智能体，协调双方系统提供关联洞察。这些举措旨在消除数据复制延迟与成本，让数据、激活和AI在共享实时上下文中协同运作，提升营销个性化和效率。
categories:
- AI产品
tags:
- 数据科学
- 营销技术
- 数据集成
- 实时分析
- AI工作流
draft: false
translated_at: '2026-04-21T05:15:55.775100'
---

在当今高度竞争的市场环境中，“洞察速度”已不再是终点线。新的黄金标准是**激活速度**。

多年来，客户智能的管理与营销的执行之间一直存在巨大鸿沟。数据团队在湖仓一体平台中构建复杂的模型和指标，从倾向性评分到客户终身价值（CLV）。营销团队则在基于Adobe Experience Platform构建的专用应用程序（如Journey Optimizer和Real-Time CDP）中执行营销活动和客户旅程。

直到最近，弥合这一鸿沟仍意味着需要构建数据管道、进行数据复制并承受延迟。营销人员一直陷于等待CSV导出、安排SFTP传输以及维护昂贵的ETL管道，仅仅是为了在Experience Platform中激活其自有客户数据的循环中。

如今，Databricks与Adobe正在弥合这一鸿沟。我们宣布双方合作取得三项重大进展：

1.  **Adobe Experience Platform支持Delta Sharing**，实现对Databricks中受治理的第一方数据的直接、零拷贝访问。
2.  **Databricks Genie通过模型上下文协议（MCP）与Adobe Marketing Agent连接**，使营销人员无需离开Experience Platform即可获取Databricks中的运营智能。
3.  **即将在Databricks Marketplace推出的Adobe Marketing Agent测试版**，允许Databricks客户构建监督智能体，协调Genie与Adobe的Marketing Agent，为营销活动效果、客户旅程分析和业务影响衡量提供关联洞察。

这些发布共同为营销人员建立了一个新的基础，使得数据、激活和AI能够在共享的实时上下文中运行，而无需承担数据移动或复制的开销。

这标志着Databricks与Adobe战略合作伙伴关系向前迈出了重要一步，加速了我们提供更互联、更智能的客户体验的能力。

## 挑战：为何现在至关重要

AI正在加速营销活动的创建、优化和执行。与此同时，客户对相关性和时效性的期望比以往任何时候都高。但大多数营销架构并非为AI智能体实时跨上下文和系统运作的现实而构建。

结果是：

*   洞察结果到达太晚，无法指导营销活动执行，导致预算分配效率低下，并限制了预测模型和实验的影响力。
*   客户上下文分散在各个系统中，使得及时、一致的个性化变得困难且成本高昂。
*   数据必须复制才能被激活，增加了基础设施成本，并带来了治理和合规风险。

与此同时，营销团队希望通过利用已存在于Databricks中的经过精炼、受治理且有价值的AI增强数据集来改进个性化和定向。同时，技术团队面临着加速数据访问和洞察时间、同时减少重复和基础设施成本的压力。

缺失的是一种能够直接实时激活数据的方式，而无需承担系统间移动数据所带来的成本、延迟和风险。

为了解决这个问题，我们与Adobe紧密合作，推出了两项新的重要功能：

## 通过Delta Sharing为Adobe Experience Platform提供零拷贝数据访问

借助Delta Sharing，Experience Platform现在可以直接访问Databricks中的数据，无需ETL管道、数据复制或延迟。这解决了现代营销中三个最大的限制：

*   **延迟**：Databricks中的洞察结果通常需要24-48小时才能到达下游营销系统。
*   **成本**：跨云移动PB级数据会产生出口费用和冗余存储成本。
*   **治理**：将数据复制到其他平台会破坏在Unity Catalog中定义的血缘关系、访问控制和一致性。

此次合作实现了**直达平台**的共享流程。Experience Platform现在作为原生的Delta Sharing接收方，而不是从Databricks“推送”文件到Adobe。

### 工作原理

1.  **Unity Catalog作为数据源**：数据团队在Databricks中管理受治理的表和视图，例如高价值受众、流失风险评分或倾向性模型。
2.  **安全握手**：Databricks使用开放的Delta Sharing协议生成安全凭证，允许Experience Platform直接访问共享数据集。
3.  **受治理的直接数据访问**：这些数据集在Experience Platform中显示为虚拟表，同时由Unity Catalog管理访问权限。借助Adobe Data Distiller，营销人员可以实时查询Databricks的实时数据，而无需移动任何底层记录。

![Databricks Delta Sharing现已作为Experience Platform内的数据源提供](/images/posts/b5a9038b5fbb.png)

### 基于开放标准构建

此集成由开源的Delta Sharing协议驱动，而非专有连接器或中间件。其结果是您的湖仓与Adobe之间建立了一个安全、受治理的实时连接，无需数据复制。

## 通过Adobe Experience Platform Agent Orchestrator和Genie MCP实现AI双向编排

虽然Delta Sharing解决了**数据访问**问题，但真正的挑战在于实现业务上下文的自助服务。为了解决这个组织层面的问题，我们自豪地宣布**Adobe Experience Platform Agent Orchestrator与Databricks Genie MCP的集成**。

作为此次合作的一部分，Databricks Genie MCP将可从Adobe Experience Platform Agent Orchestrator内部访问，允许Adobe用户使用自然语言与其在Databricks中的相关运营数据进行交互。同时，Adobe Marketing Agent MCP将可从Databricks平台内部访问，允许开发人员部署生产级AI智能体，这些智能体整合了AEP的受众洞察和互动指标，以解决跨领域相关用例，例如闭环归因。

### 这带来的可能性

*   **跨系统的智能体智能**：Adobe的AI智能体可以通过Genie的MCP安全地发现和使用Databricks中受治理的数据集、元数据和模型，为特定营销活动识别最佳数据集。
*   **返回Databricks的闭环执行**：Databricks Genie和AI智能体可以使用自然语言查询Adobe Marketing Agent，获取营销活动效果、互动和转化洞察，以重新训练模型、更新细分受众群或触发下游工作流。
*   **标准化、可扩展的集成**：使用MCP，Adobe和Databricks的智能体可以与Databricks工具（如SQL仓库和模型服务端点）交互，无需为每个用例进行定制集成。

![Adobe Experience Platform Agent Orchestrator与Genie MCP的AI双向编排演示](/images/posts/66dbe03fed5f.gif)

### 示例

*   **用于受众创建和激活的建模数据**：Databricks智能体根据行为和产品使用信号识别出一个高价值的微细分受众群，然后将该细分受众群推送到Adobe，以便在付费和自有渠道中激活。
*   **持续优化循环**：来自Adobe的营销活动效果数据流回Databricks，智能体在此重新训练模型并改进未来的营销活动效果，无需人工干预。

## 影响：为何这对双方共同的客户至关重要

消除“集成数据税”使组织能够通过在S3、ADLS或GCS等环境中就地激活数据，来降低存储、出口和工程成本。

同时，统一的治理确保了一致的访问控制和端到端血缘关系，因此诸如GDPR被遗忘权之类的政策可以在Databricks和Adobe Experience Platform之间无缝执行。

这一基础最终将推动营销人员赋能，使团队能够通过智能体和Adobe Experience Platform界面直接访问和激活湖仓数据，而无需持续依赖IT或数据工程团队。

## 现代营销的新基础

Databricks和Adobe共同为营销系统的工作方式建立了一个新的基础：

- 数据保持集中化、受管控且可信赖
- 激活过程无需数据复制
- AI基于共享的实时上下文运行

这正是让营销活动能够加速推进、智能化运作并持续优化的关键所在。

## 开始使用

如果您正在参加Adobe Summit，请前往**548号展位**参观，亲身体验全新集成功能，了解如何将您的Databricks数据接入Adobe Experience Platform。

---

> 本文由AI自动翻译，原文链接：[Bridging Data Science and Marketing: Databricks Unveils Delta Sharing Integration for Adobe Experience Platform and Agentic Marketing Workflows](https://www.databricks.com/blog/adobe-databricks-delta-sharing-agentic-marketing)
> 
> 翻译时间：2026-04-21 05:15
