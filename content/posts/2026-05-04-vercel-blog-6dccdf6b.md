---
title: 用智能体构建智能体平台：通用智能的Vercel实践
title_original: How General Intelligence used agents to build an agent platform on
  Vercel
date: '2026-05-04'
source: Vercel Blog
source_url: https://vercel.com/blog/how-general-intelligence-used-agents-to-build-an-agent-platform-on-vercel
author: ''
summary: 通用智能（General Intelligence）是一家8人公司，正构建一个让创始人通过AI智能体运营公司的平台。其旗舰产品Cofounder提供涵盖工程、营销、财务等部门的智能体团队。为打造这一平台，团队自身率先采用智能体驱动开发，每天提交10个PR和70+次提交，运行4000+预览分支。他们从Render迁移到Vercel，因为后者能让智能体通过API完成100%的云操作，而非仅部分自动化。文章展示了小团队如何通过统一平台和智能体协作实现百人团队的交付效率。
categories:
- AI基础设施
tags:
- AI智能体
- Vercel
- 基础设施
- 自动化开发
- 创业
draft: false
translated_at: '2026-05-05T05:08:08.220873'
---

### 链接到标题Vercel上的通用智能

- 8人团队（5名工程师）每人每天提交10个PR和70+次提交
- 4000+个预览分支，随时运行着约100个并行应用版本
- 90%的SRE工作通过Vercel和自有Agent（联合创始人）实现自动化
- 为每位客户提供托管Vercel账户的联合创始人服务

8人团队（5名工程师）每人每天提交10个PR和70+次提交

4000+个预览分支，随时运行着约100个并行应用版本

90%的SRE工作通过Vercel和自有Agent（联合创始人）实现自动化

为每位客户提供托管Vercel账户的联合创始人服务

通用智能正在构建一个平台，让任何创始人完全通过AI Agent（智能体）运营公司。他们的愿景是打造一人十亿美元公司，每个部门都由Agent（智能体）驱动。

他们的旗舰产品Cofounder为创始人提供完整的Agent（智能体）团队，涵盖工程、营销、SEO、财务、销售、客户支持和运营。

![](/images/posts/6d644890f31f.jpg)

![](/images/posts/50d9a2ef9611.jpg)

通用智能是一家8人公司，其中5名工程师。为了构建一个让客户运营Agent（智能体）驱动公司的平台，他们自己必须首先这样运营。他们希望使用Cofounder的CTO Agent（智能体）来构建其他Agent（智能体）驱动的业务功能，而开发人员很快意识到这是一个基础设施问题，而非Agent（智能体）问题。

对于一个复杂的多租户平台，要求是全面的程序化控制：人类在底层云平台上能执行的每个操作，都必须通过CLI或API提供给编码Agent（智能体）。这意味着要处理部署下线、更改DNS、管理计费、编辑配置等所有操作。大多数云服务商未能通过这一测试，这也是通用智能迁移到Vercel的原因。

## 链接到标题Agent（智能体）需要为Agent（智能体）构建的基础设施

编码Agent（智能体）并行运行数十个进程。它将日志作为数据查询，将错误作为输入解析，并将每次仪表盘点击视为缺失的API。瓶颈不再是Agent（智能体）编写代码的速度，而是它能实际触及多少云资源。

大多数云平台并非为此模式设计。它们是为人类开发者构建的：可点击的仪表盘、可读取的控制台、覆盖部分操作但止步于其他操作的API。Agent（智能体）越接近端到端运行开发，这些缺口就越堆积。

通用智能最初托管在Render上。这对早期产品有效，但从第一天起，为全栈配置预览环境就非常痛苦。

当他们开始构建Cofounder的CTO Agent（智能体）时，这种痛苦变成了障碍。平台必须通过代码实现端到端可访问，而Render的Python支持无法满足Agent（智能体）的需求。

"有些供应商让Agent（智能体）完成5%的工作，有些让Agent（智能体）完成50%，"Pignanelli解释道。"我们需要一个能让Agent（智能体）完成100%工作的平台。"他们以此标准评估供应商，并最终选择迁移到Vercel。

## 链接到标题五名工程师如何像百人团队一样交付

迁移到Vercel改变了通用智能构建软件的方式，他们的工程师不再进行本地开发。Cofounder的CTO Agent（智能体）所做的每项更改都直接进入Git分支，启动预览环境，并由浏览器Agent（智能体）在实时URL上进行端到端测试。

通用智能拥有超过4000个进行中的分支。在工作日的任何时刻，大约有100个应用版本在Vercel上运行，每个版本都有独立的预览环境，由编码Agent（智能体）或浏览器Agent（智能体）操作。今年早些时候，Fluid计算量月环比增长6.5倍，其中大部分增长来自内部工程工作：编码Agent（智能体）在Cofounder中构建业务Agent（智能体）。

如今，工程师平均每天提交10个PR，每个PR包含70+次提交，每位工程师每月的Token预算为5000美元。

### 链接到标题将Cofounder的Python后端迁移到Vercel

通用智能运行Python后端，他们是首批将复杂全栈应用迁移到Vercel的团队之一。他们刻意这样做，因为Agent（智能体）必须驱动整个堆栈的部署、配置和计算，而不仅仅是前端。

统一到一个平台将团队和Agent（智能体）的接触面缩小到一个CLI、一个API和一个可观测性层。当出现问题时，Agent（智能体）和开发人员可以在一个地方看到全局。

### 链接到标题在Vercel上将Cofounder作为多租户应用运行

当创始人在Cofounder上启动一家公司时，他们获得的不仅仅是一组Agent（智能体），而是一个真实的GitHub仓库和托管的Vercel部署，通过Vercel for Platforms自动配置。每个公司还拥有自己的域名，SSL和DNS自动处理。

客户公司内部的工程Agent（智能体）就是Cofounder的CTO，与通用智能内部使用的产品相同。它运行相同的工作流程：分支、预览环境、测试实时URL的浏览器Agent（智能体）。

## 链接到标题下一步计划

通用智能将继续在与交付给客户相同的产品上构建自己的公司。随着他们增加新的部门和Agent（智能体），Pignanelli表示Vercel使他们能够专注于客户，而非配置底层云平台。

通用智能正在构建Cofounder，首个全栈Agent（智能体）公司平台。

---

> 本文由AI自动翻译，原文链接：[How General Intelligence used agents to build an agent platform on Vercel](https://vercel.com/blog/how-general-intelligence-used-agents-to-build-an-agent-platform-on-vercel)
> 
> 翻译时间：2026-05-05 05:08
