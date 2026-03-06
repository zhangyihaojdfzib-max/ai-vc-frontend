---
title: Databricks推出KARL：基于自定义RL的更快企业知识智能体
title_original: 'Meet KARL: A Faster Agent for Enterprise Knowledge, powered by custom
  RL'
date: '2026-03-05'
source: Databricks Blog
source_url: https://www.databricks.com/blog/meet-karl-faster-agent-enterprise-knowledge-powered-custom-rl
author: ''
summary: 本文介绍了Databricks利用自定义强化学习技术开发的名为KARL的企业知识智能体。该智能体专注于解决基于事实的推理任务，如文档搜索与交叉验证，旨在以更低的推理成本和延迟，匹配甚至超越前沿大模型的性能。文章指出，通过数千GPU小时的训练和合成数据，KARL在内部测试中表现优异，其背后的RL流水线现已作为Custom
  RL私有预览版向客户开放，帮助企业优化自身智能体的效率与成本。
categories:
- AI产品
tags:
- 强化学习
- 企业智能体
- Databricks
- 推理优化
- 知识助手
draft: false
translated_at: '2026-03-06T04:40:07.559535'
---

![Meet KARL: A Faster Agent for Enterprise Knowledge, powered by custom RL](/images/posts/49d022aec07a.png)

面向企业智能体的强化学习

欲阅读完整技术报告，请点击此处。有兴趣在您的企业智能体上尝试 Databricks 自定义 RL 吗？请点击此处。

当前模型推理能力的提升，导致了用于知识工作的智能体部署激增，例如编写代码、回答关于企业数据的问题以及自动化常见工作流。虽然用于企业任务的模型非常强大，但也极其昂贵，对于许多用例而言，推理成本已开始增长到难以为继的程度。在本文及相应的技术报告中，我们将分享使用强化学习构建自定义模型来支持我们 Agent Bricks 产品关键用例的经验。这个例子表明，以相对较低的成本，可以构建在推理成本、延迟和质量这三个关键维度上全面优于前沿模型的自定义模型。我们的发现与其他行业观察结果一致，例如 Cursor 的 Composer 模型，其中基于 RL 的定制化能够显著提高速度和品质。

KARL：为 Databricks 用户提供的更快、更强、更便宜的知识智能体

![KARL: A Faster, Stronger, Cheaper Knowledge Agent for Databricks Users](/images/posts/acd758d3c4eb.png)

我们训练的模型名为 KARL，它解决了一项关键的企业能力——**基于事实的推理**：通过搜索文档、事实核查、交叉引用信息以及进行数十步甚至数百步的推理来回答问题。多项 Databricks 产品都需要基于事实的推理，例如 Agent Bricks 知识助手。与数学和编码不同，基于事实的推理任务**难以验证**——通常没有唯一正确答案。在这种情况下，引导强化学习找到好的解决方案尤其困难。

利用 Databricks 开发的 **RL** 技术和基础设施，KARL 以极低的服务成本和延迟，匹配了全球最强大的专有模型的性能，包括在它从未见过的新的基于事实的推理任务上也是如此。（详见技术报告。）我们仅用了几千个 GPU 小时的训练和完全合成的数据就实现了这一点。

在内部用户测试中，KARL 提供了比我们现有产品和最新前沿模型更好、更全面的回答。这项研究正在融入您今天使用的 Databricks 智能体中，例如 Agent Bricks，将答案建立在您的 Databricks 湖仓一体平台中的非结构化和结构化数据之上。

面向 Databricks 客户的可复用 RL 流水线

我们很高兴地分享，我们用于创建 KARL（以及我们即将讨论的其他智能体）的相同 RL 流水线和基础设施，现已可供寻求提升模型性能并降低其高流量智能体工作负载成本的 Databricks 客户使用。几乎所有现实世界的企业任务都难以验证，因此 KARL 不仅为 Databricks 用户带来更好的体验，也为我们的客户为其热门智能体创建自己的自定义 RL 模型铺平了道路。我们的 **Custom RL 私有预览版**，由**无服务器 GPU 计算**提供支持，使您能够使用 KARL 基础设施来构建一个更高效、特定领域的智能体版本。如果您有一个正在快速扩展的 AI 智能体，并且有兴趣使用 RL 对其进行优化，请在此处注册以表达您对此预览版的兴趣。

## 为您推荐

---

> 本文由AI自动翻译，原文链接：[Meet KARL: A Faster Agent for Enterprise Knowledge, powered by custom RL](https://www.databricks.com/blog/meet-karl-faster-agent-enterprise-knowledge-powered-custom-rl)
> 
> 翻译时间：2026-03-06 04:40
