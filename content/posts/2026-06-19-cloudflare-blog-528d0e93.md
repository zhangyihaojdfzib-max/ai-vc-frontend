---
title: Cloudflare推出面向AI Agent的临时账户
title_original: Temporary Cloudflare Accounts for AI agents
date: '2026-06-19'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/temporary-accounts/
author: ''
summary: Cloudflare发布临时账户功能，允许AI Agent无需事先注册即可通过wrangler deploy --temporary命令部署Worker，部署保持在线60分钟，之后可被认领或自动过期。该功能解决了AI
  Agent在部署时遇到的浏览器OAuth、API Token复制粘贴等人类设计障碍，为Agent提供廉价、可丢弃的部署目标，支持快速迭代的“编写→部署→验证”循环，使Agent编码和发布更加无缝。
categories:
- AI产品
tags:
- Cloudflare
- AI Agent
- 临时账户
- 无摩擦部署
- Wrangler
draft: false
translated_at: '2026-06-20T06:20:35.775592'
---

# 面向AI Agent的临时Cloudflare账户

2026-06-19

- Sid Chatterjee
- Celso Martinho
- Brendan Irvine-Broque

![](/images/posts/c84f48830ee4.png)

如今每个人都在用AI Agent编写代码。但当Agent需要部署某些东西——并且需要注册和创建账户时——它就会一头撞上为人类设计的障碍：基于浏览器的OAuth流程、需要点击操作的仪表盘、需要复制粘贴的API Token、需要完成的多因素认证提示。对于开发者身边的交互式编程助手来说，这很烦人。对于后台Agent来说，这则是一个硬性阻断。

今天，我们推出面向Agent的临时Cloudflare账户。

Agent现在可以立即部署网站、API和Agent，无需事先注册账户。

任何Agent现在都可以运行`wrangler deploy --temporary`，将Worker部署到Cloudflare。这个临时部署会保持在线60分钟，在此期间你可以认领该临时账户，使其永久归你所有。如果你不认领，它会自动过期。

我们的目标？让你的Agent编写代码并发布。

## 为什么无摩擦部署对AI Agent至关重要

无摩擦临时账户的重要性可能远超表面所见：

- 后台AI会话没有人类参与，并且正在成为常态。任何需要浏览器、复制粘贴或"在60秒内点击此处"的身份验证步骤，都会导致Agent卡住，并可能选择部署到其他地方。
- 试错是Agent的超能力。Agent需要一个紧密的"编写→部署→验证"循环。它们需要廉价、可丢弃的部署目标，以便能够curl自己的输出并判断是否正确。
- Agent平台正在构建自己的方式，让代码部署能够"直接运行"，无需额外步骤或凭证。人们开始期望这个过程能够直接运行，无需注册他们之前从未使用或听说过的其他服务。

后台AI会话没有人类参与，并且正在成为常态。任何需要浏览器、复制粘贴或"在60秒内点击此处"的身份验证步骤，都会导致Agent卡住，并可能选择部署到其他地方。

试错是Agent的超能力。Agent需要一个紧密的"编写→部署→验证"循环。它们需要廉价、可丢弃的部署目标，以便能够curl自己的输出并判断是否正确。

Agent平台正在构建自己的方式，让代码部署能够"直接运行"，无需额外步骤或凭证。人们开始期望这个过程能够直接运行，无需注册他们之前从未使用或听说过的其他服务。

## 工作原理

临时账户基于Wrangler构建，Wrangler是我们的开发者平台命令行界面（CLI）工具，让开发者能够引导新项目、管理配置和资源，以及部署和更新它们。

Wrangler的使用方法在线上有广泛文档记录，Agent也非常清楚如何使用它。但如果你尚未登录并授予Wrangler访问你Cloudflare账户的权限，当Agent尝试部署时，它就会卡在注册和身份验证步骤。你可能会合理地问：Agent和LLM如何知道Wrangler中存在这个新的`--temporary`标志，以便在没有人类明确告知的情况下实际使用它？

为了解决这个问题，我们更新了Wrangler，使其向Agent提示一条消息，告知它`--temporary`标志的存在：

当Agent发现这一点，然后再次使用`--temporary`标志运行`wrangler deploy`时，Cloudflare会为Agent提供一个临时账户使用，给Wrangler一个可用的API Token，并提供一个认领URL，Agent可以将其返回给人类。

## 让我们逐步了解整个流程

### 部署和迭代新项目

确保你使用的是最新的Wrangler版本，启动你最喜欢的编码Agent，并编写一个提示词，以构建模式部署一个"hello world"应用：

用TypeScript创建一个非常简单的hello world Cloudflare Worker，并使用wrangler部署，不要问我问题，尽你所能做到最好

Agent将运行wrangler，从输出消息中获取`--temporary`标志，构建你的脚本，并立即部署，无需人类参与：

如你所见，Agent编写了脚本，使用`--temporary`标志部署了它，curl了从输出中获得的预览链接，并验证了结果与代码匹配。

这很棒，但Agent编码往往不止涉及一次部署。一个会话可能会经历多次代码变更的循环。这不是问题：Agent可以迭代Worker脚本并根据需要多次重新部署更改（在60分钟的认领窗口内）。输入这个提示词：

现在将hello world改为"hello cloudflare"并重新部署

观察Agent更改源代码，重用之前创建的临时账户，重新部署新版本并重新检查结果：

### 认领账户

在任何时候，你都可以认领临时账户并使其永久归你所有。当你点击认领链接时，你会被带到一个页面，你可以在那里注册或登录Cloudflare，然后认领你的Worker所部署到的临时账户。这不仅包括认领Worker，还包括数据库和其他绑定等资源。

如果你在60分钟内没有认领这些临时账户，它们将被自动删除。

## 通往无摩擦Agent部署之路

这只是我们消除Agent注册障碍的一种方式。我们最近宣布了与Stripe的合作关系，以及我们共同设计的一个新协议，该协议允许Agent代表其用户配置Cloudflare——创建账户、启动订阅、注册域名、获取用于部署代码的API Token，无需复制粘贴Token或输入信用卡详细信息。上个月，我们与WorkOS合作推出了auth.md，任何人都可以采用它，让Agent使用成熟且现有的OAuth标准来配置新账户。

这个领域正在发生很多事情，我们很高兴能继续让Agent更容易使用Cloudflare，也让开发者更容易让自己的应用具备Agent就绪能力。临时账户是迈向无摩擦Agent部署的又一步——敬请期待更多。

临时账户有一些限制，其功能可能会随时间变化；查看开发者文档了解更多信息，然后去构建一些东西吧。让你的Agent指向Cloudflare，看看它能走多远，并告诉我们我们可以改进什么，或者什么让你感到惊喜——在X上分享你构建的内容，或加入Cloudflare社区。

---

> 本文由AI自动翻译，原文链接：[Temporary Cloudflare Accounts for AI agents](https://blog.cloudflare.com/temporary-accounts/)
> 
> 翻译时间：2026-06-20 06:20
