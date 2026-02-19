---
title: 灵活节点类型正式发布：提升集群弹性与成本效益
title_original: Flexible Node Types Are Now Generally Available
date: '2026-02-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/flexible-node-types-are-now-generally-available
author: ''
summary: Databricks正式推出灵活节点类型功能，旨在解决云环境中因特定实例类型容量不足导致的集群启动失败问题。该功能允许集群在首选实例类型不可用时，自动回退到计算形态兼容的替代类型，从而显著减少高流量时期的启动失败。它不仅提高了平台的弹性，还通过优化Spot实例使用来帮助降低成本。管理员可一键启用该功能，并通过API自定义回退顺序，实现对成本和性能的精确控制。
categories:
- AI基础设施
tags:
- Databricks
- 云计算
- 集群管理
- 成本优化
- 弹性计算
draft: false
translated_at: '2026-02-19T04:44:47.584302'
---

确保特定的计算容量可能具有挑战性，尤其是在高流量（和高压力）时期。数据工程师和平台管理员都太熟悉容量不足或"缺货"带来的挫败感，这些错误发生在集群启动失败时，原因是云提供商无法满足对特定实例类型的请求。

无论是：

- AWS_INSUFFICIENT_INSTANCE_CAPACITY_FAILURE
- Azure上的CLOUD_PROVIDER_RESOURCE_STOCKOUT，还是
- GCP_INSUFFICIENT_CAPACITY，

这些错误会中断关键工作负载，尤其是在业务关键时期，正常运行时间至关重要的时候。

## 什么是灵活节点类型？

传统上，Databricks集群要求每个节点都必须是配置中指定的确切实例类型。如果该特定类型不可用，集群启动就会失败。

灵活节点类型消除了这一限制。当首选实例类型不可用时，Databricks会自动回退到具有相同计算形态的兼容替代类型。换句话说，集群会成功启动，使用混合的相似实例类型，而不是直接失败。

对于需要更严格控制的团队，他们也可以通过API定义自定义回退列表，包括尝试哪些实例类型以及尝试顺序。

![灵活节点类型](/images/posts/1aaab9ad455b.png)

## 主要优势

**在需求高峰期间减少集群启动失败**
灵活节点类型减少了容量相关故障的频率和严重性。当云提供商无法提供首选实例类型时，Databricks会自动回退到兼容的替代类型，使集群能够启动，而不是报错退出。

**优化Spot实例使用**
对于配置了"Spot-with-fallback"的集群，灵活节点类型会尝试在整个回退列表中获取Spot容量，然后再回退到按需实例。这增加了集群在Spot上运行的比例，有助于降低计算成本，同时仍优先确保成功启动。

**清晰的可见性和精确的控制**
团队可以使用node_timeline系统表精确检查获取了哪些节点类型。此外，可以通过API定义自定义回退顺序，从而精确控制成本和性能行为。

## 快速开始

工作区管理员可以在管理员设置中轻松启用此功能（文档：AWS, Azure, GCP）。启用后，该功能会立即应用于所有新的集群启动。长期运行的集群将在下次重启时采用此功能，而为现有作业创建的未来的作业集群将自动利用此功能。

自定义回退列表可以通过API配置，独立于工作区设置。

**更多详情**
请参阅文档，了解有关使用实例池配置灵活节点类型、计费、节点类型配额以及选择性启用/禁用的更多详细信息（文档：AWS, Azure, GCP）。

灵活节点类型旨在使您的数据平台更具弹性和成本效益。管理员可以按照文档中的说明，立即在工作区管理员设置中一键启用此功能。

---

> 本文由AI自动翻译，原文链接：[Flexible Node Types Are Now Generally Available](https://www.databricks.com/blog/flexible-node-types-are-now-generally-available)
> 
> 翻译时间：2026-02-19 04:44
