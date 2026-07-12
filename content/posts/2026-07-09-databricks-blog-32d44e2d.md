---
title: Databricks Genie黑客马拉松：对话式分析的三种力量
title_original: 'Ask, build, compose: What our 5th Genie Hackathon taught us about
  Databricks Genie'
date: '2026-07-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ask-build-compose-what-our-5th-genie-hackathon-taught-us-about-databricks-genie
author: ''
summary: 本文介绍了Databricks第五次客户黑客马拉松的成果，聚焦其Genie产品家族。Genie通过三种形式赋能不同用户：Genie Agent让业务用户用自然语言与受治理数据对话；Genie
  Code帮助分析师快速构建指标、管道和仪表板；Genie Agent还可作为工具被其他Agent调用。文章强调，受治理的对话式分析正从单一功能演变为企业基础能力，Unity
  Catalog和Ontology确保了数据治理与语义一致性。
categories:
- AI产品
tags:
- Databricks Genie
- 对话式分析
- 黑客马拉松
- 自然语言处理
- 数据治理
draft: false
translated_at: '2026-07-12T05:28:23.071769'
---

- 我们的第五次客户黑客马拉松变成了一场亲身体验Databricks Genie所有功能的实践之旅，十个项目构成了一套绝佳的课程体系。
- 三个赛道对应了使用Genie的三种方式：通过Genie Agent与数据对话，用Genie Code进行构建，以及将Genie组合到Agent中，每个赛道面向不同类型的用户。
- 从终于能与自己数据对话的催收团队，到深夜11点撰写供应链简报的Agent，这些构建成果展示了为何受治理的对话式分析正在成为一项基础能力而非一个功能特性。

## Databricks黑客马拉松如何运作

我们举办这些黑客马拉松的原因很简单：学习产品最快的方式就是用产品去构建。每次活动都以赋能环节开场，让团队了解产品及其路线图上的发展方向。随后构建正式开始。团队合作大约一周并提交项目，最优秀的解决方案将获得奖励。

这是我们的第五次活动，聚焦的产品是Databricks Genie。

## 为何Genie适合黑客马拉松

Databricks Genie产品让人们可以用自然语言而非SQL处理数据，这使其非常适合黑客马拉松的聚焦范围。Genie不是一个单一功能，而是一个产品家族，以三种不同形式呈现：

- 提问。Genie Agent是一个基于受治理数据的聊天界面。
- 构建。Genie Code是一个自主AI伙伴，协助数据、分析和机器学习工作流。
- 组合。Genie Agent可以作为工具被其他Agent和应用自主调用。

每种形式服务于组织中不同的团队，这正是我们设置三个赛道的原因。我们将按此顺序展开，从只想获得答案的业务用户，到将Genie Agent接入完整系统的工程师。三者共同的基础是：无论问题以何种方式提出，Unity Catalog都治理着谁能看到什么，而Genie Ontology提供了共享的语义理解。

## 赛道1：通过Genie Agent与数据对话

适用对象：希望向受治理的领域特定Agent提问的业务用户。Genie Agent是一个领域特定的聊天界面，由分析师在一组受治理数据上精心构建，然后可与业务用户共享，供其用自然语言提问。构建者可以指向Unity Catalog表，添加一些示例查询，用SQL表达式和指标视图定义业务词汇，并为必须精确回答的问题固定可信资产（受治理函数）。此后，业务用户只需输入问题，即可获得结果、图表及其背后的查询。当真实团队部署Genie Agent时，这会是怎样的场景？

OneTrust直接遇到了Genie Agent的一个核心机制。单个Agent设计为聚焦最多30张表，这能保证快速准确的回答，但OneTrust分析师关心的实际数据横跨190张表和300多个视图。因此他们构建了一个监督层，将数据分片到多个聚焦的Genie Agent中，将每个问题路由到正确的Agent，并将答案拼接回单一对话。从用户视角看，一切如常：他们仍然只向一个Agent提问。在幕后，自然语言自助服务现已覆盖整个企业资产，同时没有放弃确保可信度的治理机制。

另一个团队将Genie Agent指向约16万条贷款记录，并关键地教会了Agent使用团队的语言，定义了"cure"的含义和"DNC"代表什么，使模型能将日常问题映射到正确的数据。很快，催收团队可以用自然语言提问，了解到诸如大多数逾期贷款在约15天内解决的事实。最精彩的时刻是计划外的：一旦词汇就位，Agent开始主动提出团队未曾想到的犀利问题。这就是优质上下文将聊天框变成的样子。

## 赛道2：用Genie Code进行构建

提问只是开始。接下来的问题是：谁来进行构建，以及构建速度有多快。

适用对象：分析师和构建者。那些了解数据并能写一些SQL的半技术人员，但过去一旦项目需要管道、函数或精美的仪表板就会遇到瓶颈。

Genie Code是这个产品家族中的构建者。你用自然语言描述需求，它就能完成工作：编写指标视图、Unity Catalog函数、管道和仪表板，全部在Databricks内部完成，无需设置独立的开发环境。由于与Unity Catalog深度集成，它能理解你的真实模式和语义，因此会选择正确的连接而非凭空编造列名。对分析师而言，这就是杠杆效应。过去需要向数据工程团队提交工单或花一周手写SQL的工作，现在只需一个下午，这正是该赛道旨在展示的内容。

一个团队将Genie用在了数据团队自身。他们用Genie Code构建了一个治理智能平台，标记值得淘汰的休眠报告，利用血缘关系和SQL逻辑聚类组织中隐藏的重复报告，并评估数据是否真正准备好被AI使用。这通常是需要一整个季度和路线图的跨领域治理项目。而用Genie Code构建，它在黑客马拉松期间就完成了。

Procore在不离开Databricks的情况下，为一个度假租赁平台构建了完整的分析体验。Avinash、Abdullah、Amy和Jason使用内置AI函数（如ai_extract()）自动分类和评分房源，然后交付了包含KPI、同比趋势和预测的仪表板，并附带一个Genie Agent，能在几秒内回答投资组合经理的问题："我应该添加哪些设施来提高满意度？"一个精良的多组件产品，在几天而非几周内完成。

Fanatics Betting and Gaming构建了一个客户体验工具，能在请求时向管理者提供按ROI排序的、有理由支撑的行动清单，端到端仅用一个下午。然后他们做了一件我们非常欣赏的事：用Genie对自己的流失模型进行压力测试，发现两个基于历史记录的特征承载了几乎全部信号，并诚实地得出结论：更简单的方法同样有效。他们甚至将工作流打包成了可复用的分析师技能。当构建如此快速时，你就有资本挑战自己的成果，这正是优秀分析师使用该工具的方式。

## 赛道3：将Genie组合到Agent中

你可以与数据对话，也可以用数据构建。最后的飞跃最令我们兴奋。

适用对象：氛围编码者。这是深水区，一切在此汇聚。任务要求是在Databricks Apps上构建一个完整的Agent，将Genie作为其工具之一，并自带其他工具。

这部分改变了Genie的本质。Genie Agent不必是一个终点。通过Genie Conversation API和Databricks内置的托管MCP服务器，Genie Agent成为一个受治理的工具，任何Agent都可以调用它来提出自然语言数据问题并获得有依据的回答。因此，工程师在Databricks Apps上构建Agent，将Genie与其他MCP服务器、模型服务端点和自定义逻辑连接起来，在MLflow中追踪整个过程，并通过OAuth和Unity Catalog治理每次调用。Genie负责"与数据仓库对话"。你组合其余部分。

ShipBob 构建了那个让所有人铭记的项目——晚上11点的运营简报。供应链团队通常一觉醒来就要应对已经发生的突发状况。ShipBob 的系统在他们之前就写好了夜间简报，由一名主管协调多个专业 Agent（智能体）：Genie 负责查询仓库，其他 Agent（智能体）则融合17个实时公共数据源、识别重复出现的模式，并起草和核查结果。最终输出是一份包含真实数据的简明英文简报，例如约19.2万美元的收入面临风险，同时附有待人工审批的回写操作，且每一步都在 MLflow 中留有追踪记录。原本30分钟的站会变成了30秒的阅读。这清晰地展现了 Genie 作为团队协作者而非独奏者的角色。

![Reach Mobile Genie Hackathon](/images/posts/3eb3fc9af475.gif)

Reach Mobile 构建了 DBX Lens，将同样的理念指向了 Databricks 自身。它将一个嵌入式 Genie Agent（智能体）与自己的 MCP 服务器配对，这样你就可以询问“按 SKU 显示过去30天的 DBU”，并获得基于 Unity Catalog 系统表、按你的权限范围、以简明英文呈现的成本和治理答案。它甚至包含一个功能，可以利用 Model Serving 将自然语言治理规则转化为经过净化的 SQL。可以把它看作一个内置的 FinOps 分析师，帮助团队保持高效并遵循最佳实践。

Kin Insurance 构建了一个用于增长和营销的 Agent（智能体），它研究新市场，在 Genie 的参与下进行分析，并给出团队可执行的建议。通过将自主规划与 Genie Agent（智能体）相结合，它将原本多步骤的研究和报告工作变成了一个简单的请求。减少询问，更多行动。

另外两个构建从不同角度展示了相同的组合理念。

Ripple 为受监管的金融领域构建了一个 KYC（了解你的客户）简报 Agent（智能体）：Genie 提供内部 CRM 上下文，而 Agent（智能体）则对照外部制裁、执法和负面媒体来源进行筛查，将原本三到四小时的手动会前研究压缩成一个提示词和一份不到一分钟、带有完整引用的简报。经过认证的指标视图确保数据准确，每次运行都会记录到 Unity Catalog 中，形成清晰的审计追踪。

Fanatics Betting and Gaming 构建了 FirstBet Coach，这是一个面向新体育博彩客户的入门指南，它将 Genie 与十几个受治理的表以及团队自己构建的自定义体育数据 MCP 服务器相结合，并配有持久化记忆和用于内置审计追踪的 MLflow 追踪。两个 MCP 服务器，一次对话，并预先设置了负责任的博彩护栏。

## 更广阔的图景

将这三条路线串联起来看，你就完成了一次对 Databricks Genie 家族的工作巡礼。一位收藏负责人通过 Genie Agent（智能体）提问。一位分析师通过 Genie Code 交付一个治理平台。一位工程师将 Genie 作为众多工具之一交给自主 Agent（智能体）。与它对话，用它构建，将它组合。

这三者之所以都能安全地交付给真实用户，是因为它们都不必费心考虑的那一层：Unity Catalog。决定业务用户在 Genie Agent（智能体）中能看到什么的同一套治理体系，也限定了 Genie Code 可以触及的范围以及 Agent（智能体）可以返回的内容。只要你的数据得到一次良好的描述和治理，Genie 就能在业务用户、构建者和工程师各自的工作场景中精准地满足他们的需求。

向所有十个团队致敬，感谢他们构建了真正可用的产品。以下是一些入门 Databricks Genie 家族的推荐资源：

- 观看 Data + AI Summit 上的对话式和 Agent（智能体）式分析会议。
- 刚接触 Genie Agents（智能体）？从 Genie 入门指南和策划 Agent（智能体）的最佳实践开始。
- 想要构建？了解 Genie Code，并查看如何将 Genie Agent（智能体）置于另一个 Agent（智能体）之后。
- 准备好尝试了吗？开始免费试用，并将 Genie Agent（智能体）指向你自己的数据。

---

> 本文由AI自动翻译，原文链接：[Ask, build, compose: What our 5th Genie Hackathon taught us about Databricks Genie](https://www.databricks.com/blog/ask-build-compose-what-our-5th-genie-hackathon-taught-us-about-databricks-genie)
> 
> 翻译时间：2026-07-12 05:28
