---
title: Cloudflare Agents Week：构建Agent互联网的全面布局
title_original: Everything we launched during Agents Week
date: '2026-08-10'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/agents-week-review-august-2026/
author: ''
summary: Cloudflare在Agents Week期间发布了一系列工具和产品，旨在构建一个支持智能自主应用的互联网。文章涵盖了从运行时基础设施（如@cloudflare/computer）、Agent开发生命周期（ADLC）、可编程钱包、CI/CD自动化，到Zero
  Trust安全模型和WebMCP接口等多个方面。Cloudflare强调Agent不仅是AI的新应用，更是计算的下一次演进，并致力于通过开放协议和平台，让Agent与人类协作而非冲突，推动Agent互联网的落地。
categories:
- AI基础设施
tags:
- Cloudflare
- Agent
- AI基础设施
- 开发者工具
- 互联网架构
draft: false
translated_at: '2026-08-11T03:37:33.987865'
---

在Agents Week开始之际，Rita分享道，Agent代表了计算的下一次演进：不仅是AI的新应用，更是一类新的软件，正在塑造人们与技术互动的方式，以及软件与互联网互动的方式。在过去一年左右的时间里，我们着手探索这一转变对开发者和客户构建AI原生应用及支撑这些应用所需基础设施的意义。随着Agent变得愈发强大和自主，挑战已超越模型本身——延伸至身份、通信、编排、记忆、可观测性和安全等领域。

在过去一周中，我们分享了如何将这些要素整合到Cloudflare平台上，以服务于一个Agent互联网。每一天我们都推出了新的工具、产品和理念，致力于构建一个人与Agent协作而非冲突的互联网。

### 8月3日，星期一

周一的重点是构建和运行智能自主应用的基础——Agent所依赖的运行时和基础设施。

你的Agent需要一台计算机，而不是一个容器——推出@cloudflare/computer

@cloudflare/computer引入了一个专为Agent设计的新运行时，能够为任务选择合适的环境。

Workers RPC现已支持Python和JavaScript互操作

Python和JavaScript Workers现在可以直接相互通信，使混合语言项目更加简便。

更小、更快、更安全：大规模运行Kimi和GLM

探索我们如何在不大幅牺牲质量、可靠性或安全性的前提下，更高效地服务大型模型。

推出Billable Usage API：Cloudflare可编程成本可视化

一种更简单的方式来跟踪我们自助服务产品的使用量和成本。

Cloudflare Workers和Containers现已支持入站TCP连接和gRPC

使用Cloudflare Workers托管语音AI后端或其他实时语音Agent。

### 8月4日，星期二

周二介绍了Agent开发生命周期（ADLC）以及将Agent软件从原型推进到生产环境的原语。

Agent开发生命周期已登陆Cloudflare

用ADLC取代SDLC（软件开发生命周期）；我们关于将Agent从原型推进到生产环境的见解，以及支撑下一代“软件工厂”的原语。

推出：Cloudflare Agents

在Cloudflare上构建Agent，实时查看每次运行，支持追踪、回放和人工审批，全面掌控生产环境中的操作。

你的Agent现在可以使用本地追踪调试Workers

将分布式追踪引入本地开发环境，使Agent更容易在生产环境之前发现并调试问题。

宣布Cloudflare Wallets：面向Agent互联网的可编程钱包

钱包为Agent提供了一种安全的方式，使其能够作为新兴Agent经济中的参与者执行交易。

在Cloudflare上为数百万仓库运行CI/CD——在你的平台上

可编程CI/CD；用代码而非配置编写的流水线，配备可修复故障并暂存修复以供审查的Agent。

Cloudflare如何利用AI执行工程标准

我们如何在开发工作流程中使用AI驱动的自动化来保持代码标准和流程的一致性，帮助我们的软件工厂大规模交付高质量且一致的代码。

我们如何构建软件工厂将Astro的GitHub问题数降至零

自动化问题的分析、分类和路由，以最小化软件维护负担并最大化开发者生产力。

### 8月5日，星期三

周三将Zero Trust从用户和设备扩展到Agent本身——我们分享了如何在Cloudflare内部运行这一体系。

Agent访问模型

一个关于Agent如何代表用户安全访问资源和服务的框架——适用于一个Agent日益增多的互联网。

我们如何通过Cloudflare OS重新思考Cloudflare的工作方式

我们如何将AI嵌入内部运营模式，使团队能够更智能、更快速地工作，同时不放弃安全性或监督。

Cloudflare OS：面向Agent、应用和工作的开放平台

我们开源了团队用于构建应用、自动化工作和安全访问内部系统的平台。

通过身份感知分析捕捉恶意AI行为

将AI活动归属于真实用户和系统，使异常和支出激增更容易被发现。

WriteGuard：MCP服务器的细粒度控制

为客户提供我们部署的相同工具，以更好地控制高风险工具调用，降低Agent做出非预期更改的可能性。

### 8月6日，星期四

周四定义了Agent互联网，以及网站所有者、发布者和Agent如何共同构建一个同时服务于人和Agent的互联网。

构建开放的Agent互联网：可读、可发现、可调用、可支付

一个Agent互联网模型，发布者保持控制权，Agent获得所需的有用访问权限，开放协议使双方能够进行交易。

为任何网站提供WebMCP接口

WebMCP预览版，引入了一种新的（且非常简单的）方法，使网站和Web应用能够被Agent发现和使用。

从排名到推荐：让你的网站在AI Agent时代蓬勃发展

将SEO调整为AEO（答案引擎优化）实践，以改善Web内容被Agent发现、理解和呈现的方式。

推出Kitesurf：在Cloudflare Workers的V8隔离环境中运行的Agent优先浏览器

一款专为Agent构建的浏览器，以牺牲像素级渲染换取更低的内存和CPU使用率。

下一代MCP

MCP被重写了。MCPv2引入了MCP支持的下一代演进，简化了Agent应用的部署和扩展。

Cloudflare AI Search：为你的Agent提供数据搜索引擎

AI Search通过一条命令将你的文件或网站转变为Agent就绪的搜索引擎。

### 8月7日，星期五

周五聚焦于实际发生的情况：Agent在Web上的真实行为、AI在你的应用中的运行位置、谁在为生态系统做贡献，以及分析互联网数据的新工具。

揭示Agent互联网上的好与坏行为

机器人并不总是坏的，人类也不总是好的；将机器人缓解重新定义为持续信任而非一次性风险。

将Workers AI和AI Gateway统一为单一AI控制平面

一个绑定、一个钱包、一个仪表盘即可调用任何AI模型；模型优先路由即将推出。

宣布Cloudflare大使、社区工程师以及额外100万美元开源资金

我们更新的社区计划引入了两个新项目——面向社区领袖的Cloudflare大使和面向开源维护者的社区工程师——加上未来两年额外100万美元的开源资金。

推出Radar Researcher：用自然语言探索互联网数据的AI工具

Radar的AI研究助手：输入自然语言问题，输出实时交互式图表。

### Agents Week已结束，但我们的工作仍在继续

五天过去，Rita提出的“你的Agent需要Agent云提供什么？”这一问题开始有了答案。它需要一个执行层和运行所需的原语，一个日益自我编写的开发生命周期，为执行工作的人和Agent提供安全访问，一个Agent互联网，以及让这一切保持脚踏实地的人类和社区。未来还有很多工作要做，但下一步的方向已愈发清晰：一个原生支持其服务对象——人类——以及现在代表人类行动的Agent的互联网。

我们的工作不会止步于此。请关注我们的更新日志以获取最新动态。如果你正在与我们共同构建其中的任何部分，我们很乐意听到你的声音！欢迎在X或Discord上找到我们。

## 相关标签

在社交媒体上关注

- Cloudflare
- Kathy Liao

## 订阅以接收新文章通知

我们绝不会分享你的电子邮件地址。

感谢订阅！请检查您的收件箱以确认。

---

> 本文由AI自动翻译，原文链接：[Everything we launched during Agents Week](https://blog.cloudflare.com/agents-week-review-august-2026/)
> 
> 翻译时间：2026-08-11 03:37
