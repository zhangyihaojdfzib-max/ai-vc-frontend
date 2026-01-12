---
title: Discord如何索引万亿级消息：从Elasticsearch架构到挑战
title_original: How Discord Indexes Trillions of Messages
date: '2025-04-24'
source: Discord Engineering
source_url: https://discord.com/blog/how-discord-indexes-trillions-of-messages
author: ''
summary: 本文回顾了Discord早期为索引数十亿条消息而构建的搜索系统，该系统基于Elasticsearch，通过按服务器（公会）或私信分片存储消息，实现了高性能、可扩展且易于运维的目标。系统采用延迟索引和消息队列批量处理，以优化资源使用。然而，随着Discord的快速发展，这一基础设施开始面临新的挑战。文章核心探讨了大规模消息索引的技术架构演进与局限性。
categories:
- 技术趋势
tags:
- 搜索引擎
- Elasticsearch
- 可扩展性
- 消息队列
- 基础设施
draft: false
translated_at: '2026-01-12T04:57:25.886763'
---

早在2017年，我们就曾分享过如何构建能够索引数十亿条消息的搜索系统。我们设计的搜索基础设施旨在实现高性能、高性价比、可扩展且易于运维。我们选择使用Elasticsearch，将Discord消息分散存储在两个Elasticsearch集群的多个索引（即Elasticsearch消息的逻辑命名空间）中。消息按Discord服务器（下文将称为"公会"）或私信（DM）进行分片。这使得我们可以将所有公会消息集中存储以实现快速查询，并运行规模更小、更易管理的集群。由于并非所有用户都会使用搜索功能，消息采用延迟索引的方式进入Discord系统，我们还构建了一个消息队列，允许工作节点批量拉取消息进行索引，从而充分利用Elasticsearch的批量索引能力。

但随着Discord的快速发展，我们的搜索基础设施开始显现出一些裂痕……

---

> 本文由AI自动翻译，原文链接：[How Discord Indexes Trillions of Messages](https://discord.com/blog/how-discord-indexes-trillions-of-messages)
> 
> 翻译时间：2026-01-12 04:57
