---
title: Spotify与Anthropic对谈：Agentic开发如何重塑软件工程
title_original: 'Let’s Talk Agentic Development: Spotify x Anthropic Live | Spotify
  Engineering'
date: '2026-04-06'
source: Spotify Engineering
source_url: https://engineering.atspotify.com/2026/4/anthropic-agentic-development/
author: ''
summary: 本文记录了Spotify与Anthropic关于Agentic开发的炉边谈话。双方探讨了AI Agent（如Spotify的Honk）如何改变软件开发流程，从代码生成扩展到软件全生命周期管理。对话重点涉及大规模部署Agent所需的工具设施、组织变革、上下文管理、代码评审新范式以及责任归属等核心挑战与未来趋势。
categories:
- AI产品
tags:
- AI Agent
- 软件开发
- Spotify
- Anthropic
- 工程实践
draft: false
translated_at: '2026-04-07T04:48:00.783183'
---

# 探讨Agentic开发：Spotify与Anthropic现场对话

AI Agent正在改变我们的构建方式——甚至改变我们作为软件开发者的自我认知。Spotify和Anthropic都在探索这一转变的实际意义，并于3月30日在Spotify伦敦总部齐聚一堂，分享我们的实践心得。

在题为"探讨Agentic开发"的炉边谈话中，Spotify首席架构师Niklas Gustavsson与Anthropic的David Soria Parra（MCP联合创造者）和Christian Ryan（应用AI负责人）展开广泛讨论，深入探讨大规模Agent优先开发的实际形态——从支撑其运行的工具设施，到所需的组织变革。

观看我们与Anthropic的特别炉边谈话

对话亮点摘要：

## 超越感知：Opus 4.5上线的历史时刻

2025年11月25日——Agent优先软件开发成为现实的关键节点。一次模型更新在Spotify内部图表中呈现为显著拐点，并彻底改变了两家公司工程师的日常工作模式。聆听亲历者的讲述。

###### "这对我来说是真正的转折——某周走进办公室看到人们面对IDE工作，三周后再来发现所有人都在终端前操作。" —— David Soria Parra, Anthropic

## Honk：Spotify基于Claude的智能编码Agent

Spotify允许任何人通过Slack消息唤醒Agent。这会带来什么变化？了解从确定性代码迁移到Slack原生编码Agent，再到运用Agent同时执行数千代码库复杂迁移的演进历程，以及Honk的下一步发展方向。

###### "如今典型的用户场景是：人们在Slack上讨论待解决的问题，然后直接@提及Honk——就像在说‘去解决这个问题’。" —— Niklas Gustavsson, Spotify

## 上下文与控制：规模化AI的基石

如何实现生态系统标准化，并在数千代码库中协调Claude运作？两个团队分享了在企业规模下为Agent提供恰当上下文的有效方案，以及当前仍存在的不足。

###### "在上下文管理与工程方面，我认为关键在于建立一套简洁可复现的标准化配置，配合完善的Claude MD设置，以及能精准捕捉目标角色或领域本质的技能组合。这就是核心，无需过度复杂化。" —— Christian Ryan, Anthropic

## 人类与Agent：测试、评审与治理新范式

当Agent提交代码的速度超越人类评审能力时，会发生什么变化？小组讨论了规模化Agent产出带来的新瓶颈，以及关于责任归属的深刻议题。

###### "代码由谁生成或背后机制如何并不重要。无论是Agent还是人类，最终都应以结果为导向，并且必须有人对结果负责。" —— Christian Ryan, Anthropic

## 未来展望？

对话尾声，David指出2025年聚焦于代码创造，而下一前沿将是Agent承担完整软件生命周期——包括维护、删除以及那些无人愿做却不可或缺的工作。

Backstage正从面向人类的开发者门户转型为Agent优先平台，通过MCP连接取代人工工作流。

在Anthropic内部，孕育了Claude Code和Cowork的"内部自用"文化（他们称之为"ant-fooding"）持续催生新产品创意，其速度连构建者都感到惊讶。

观看上方完整对话，并查阅我们的Honk博客系列，深入了解Spotify如何运用后台编码Agent：

- 提交1500+PR后：Spotify后台编码Agent实践之路（Honk系列一）
- 后台编码Agent：上下文工程实践（Honk系列二）
- 后台编码Agent：通过强反馈循环实现可预测结果（Honk系列三）

提交1500+PR后：Spotify后台编码Agent实践之路（Honk系列一）

后台编码Agent：上下文工程实践（Honk系列二）

后台编码Agent：通过强反馈循环实现可预测结果（Honk系列三）

感谢Anthropic伙伴们的精彩讨论，以及所有线上线下参与的朋友。

---

> 本文由AI自动翻译，原文链接：[Let’s Talk Agentic Development: Spotify x Anthropic Live | Spotify Engineering](https://engineering.atspotify.com/2026/4/anthropic-agentic-development/)
> 
> 翻译时间：2026-04-07 04:48
