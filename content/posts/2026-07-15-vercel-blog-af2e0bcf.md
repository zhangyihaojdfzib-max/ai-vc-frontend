---
title: Speechify在Vercel上服务6000万用户的实践
title_original: How Speechify serves 500,000 dynamic pages to 60 million users on
  Vercel | Customers | Vercel
date: '2026-07-15'
source: Vercel Blog
source_url: https://vercel.com/blog/how-speechify-serves-50000-dynamic-pages-to-60-million-users-on-vercel
author: ''
summary: 本文介绍了Speechify如何借助Vercel平台，从被黑客攻击的困境中重建，最终实现服务50万个动态页面、覆盖6000万用户，并降低50%成本。通过使用Next.js、Data
  Cache、ISR和Instant Rollbacks等技术，Speechify的小型工程团队能够高效交付，保持99.99%正常运行时间，并快速迭代AI功能。文章强调了Vercel在动态页面扩展、安全性和持续部署方面的关键作用。
categories:
- AI基础设施
tags:
- Speechify
- Vercel
- Next.js
- 动态页面扩展
- AI基础设施
draft: false
translated_at: '2026-07-17T05:12:14.439204'
---

### Speechify on Vercel

- 在40多种语言中服务超过50万个页面
- 通过Fluid compute自动扩展，成本降低50%
- 借助Instant Rollbacks，不良部署对用户零影响

在40多种语言中服务超过50万个页面

通过Fluid compute自动扩展，成本降低50%

借助Instant Rollbacks，不良部署对用户零影响

Speechify最初是为阅读障碍者打造的工具。创始人兼CEO Cliff Weitzman开发它，是因为阅读存在困难，而音频让事情变得简单得多。这一初始用例使Speechify获得了数千万用户，并因其包容性赢得了Apple设计奖。

此后，该产品发展成为一个更宏大的平台：一个AI工作平台，6000万人通过它收听文档、向Agent（智能体）委派任务，并完全通过语音完成工作。

但旅程并非一帆风顺。早期，他们被黑客攻击，半天时间内，每位访客都被重定向到一个赌博网站。此后，增长工程主管Denis Chernobai意识到，是时候重新评估他们的基础设施栈了。

他决定在Next.js和Vercel上从头重建，最终他们服务的页面数量增加了40倍，全球受众规模扩大了三倍，并实现了50%的成本降低。自迁移到Vercel以来，Speechify保持了99.99%的正常运行时间，并且没有发生过一次安全事故。

## 服务50万个动态页面的成本

Speechify的网站是其主要的增长引擎，拥有1万个基础页面，翻译成40多种语言，涵盖不断变化的 onboarding 流程、本地化落地页和定价实验。静态生成不可行，因为内容变化过于频繁。但完全动态地服务所有内容意味着每位访客都可能触发一次数据库读取，这在每天数十万次访问的情况下会迅速累积。

Vercel的Data Cache、ISR和Next.js Cache Components同时解决了这两个问题。页面在首次访问时动态渲染，立即缓存，并从最近的服务节点提供，直到内容发生变化。结果是，一个全球增长引擎得以扩展，而基础设施成本并未随之增长。

## 向6000万用户交付的风险

#### Instant Rollbacks：快速交付，更快修复

Speechify的增长团队持续交付。每隔几天，新的流程和A/B实验就会部署到数百万期望一切正常工作的用户群中。在这种规模下，一次糟糕的发布不再是开发者需要修复的bug。它是一个收入问题，可能在任何人来得及反应之前就显现出来。

在Vercel之前，一次糟糕的发布意味着在它演变成事故之前匆忙修补。从带着恐惧部署到带着信心部署的转变，使得一个小型增长团队能够以通常需要更大团队才能达到的速度运作。

## 比市场慢一步的成本

#### Vercel上的Next.js：从代码到全球交付

当AI发展如此迅速时，你需要不断交付以保持竞争力，而能力也在快速演进，通常每隔几周就有变化。“我们看到上个月还不存在的新语音功能和Agent（智能体）正在涌现，”Speechify首席商务官Rohan Pavuluri说。一个想法每搁置一周，就可能有人抢先将其变为现实。借助Vercel上的Next.js，将想法变为现实的唯一障碍就是代码本身。

Speechify在Next.js上通过持续部署进行交付。增长团队没有专门的平台工程职能，也不需要。安全补丁自动应用，基础设施通过Fluid compute按需扩展，并且无需维护部署管道。

## 下一步计划

Speechify正在拓展新的国际市场，并向数百万用户交付新的AI能力。最近，他们推出了SpeechifyAI，这是一个开发者平台，通过API将支撑其消费者成功的相同语音技术提供给开发者；其旗舰模型Simba 3.2在截至2026年7月的Artificial Analysis文本转语音排行榜上排名第一。

随着产品的增长和用户群的扩大，Vercel也在随之扩展——从缓存页面到持续部署，这个平台让Speechify小而专注的工程团队能够与规模十倍于己的公司竞争。

关于Speechify：Speechify是一个AI工作平台，帮助人们通过语音消费内容，并将工作委派给AI Agent（智能体）。其开发者平台SpeechifyAI通过API提供在Artificial Analysis上排名第一的文本转语音模型（截至2026年7月）。

## 贡献者

Eric Dodds

---

> 本文由AI自动翻译，原文链接：[How Speechify serves 500,000 dynamic pages to 60 million users on Vercel | Customers | Vercel](https://vercel.com/blog/how-speechify-serves-50000-dynamic-pages-to-60-million-users-on-vercel)
> 
> 翻译时间：2026-07-17 05:12
