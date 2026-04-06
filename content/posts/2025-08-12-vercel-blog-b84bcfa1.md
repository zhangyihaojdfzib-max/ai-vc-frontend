---
title: Vercel机器人验证支持Web Bot Auth协议，提升自动化流量管理
title_original: Vercel's bot verification now supports Web Bot Auth - Vercel
date: '2025-08-12'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercels-bot-verification-now-supports-web-bot-auth
author: ''
summary: Vercel宣布其机器人验证系统已支持新兴的Web Bot Auth协议。该协议利用HTTP消息签名技术，通过非对称加密验证自动化机器人（如SEO爬虫、AI机器人）的身份，确保合法自动化流量可靠访问，同时有效拦截伪造请求。此举特别适合动态或无服务器环境，ChatGPT等已验证机器人已采用该协议进行签名认证。Vercel通过整合IP、反向DNS及Web
  Bot Auth多重验证，持续更新其已知机器人目录，强化了Bot Protection与Challenge Mode的识别能力。
categories:
- AI基础设施
tags:
- Vercel
- 机器人验证
- Web Bot Auth
- Bot Protection
- HTTP签名
draft: false
translated_at: '2026-04-06T04:54:33.187970'
---

我们与行业合作伙伴协作，共同推进了IETF关于**Web Bot Auth**的提案，目前**Vercel的机器人验证系统**已支持该新协议。现在，**Bot Protection**（机器人防护）可利用**HTTP消息签名**来验证来自动态分布式来源的自动化流量。

Vercel维护着一个全面且持续更新的**已知机器人目录**，这些机器人通过IP、反向DNS以及现新增的Web Bot Auth进行验证。Web Bot Auth通过签名标头中的公钥加密技术验证机器人身份，从而确保合法的自动化程序（如SEO爬虫、性能监控工具和平台集成AI机器人）能够可靠地访问您的网站，同时拦截伪造的机器人。

Web Bot Auth的非对称签名能验证流量的真实性，无论其网络来源如何，因此非常适合在动态或无服务器环境中运行的机器人。

使用Web Bot Auth的**已验证机器人**会在每个请求中包含签名标头以进行身份验证，使其能够被Bot Protection和Challenge Mode识别并放行。例如，**ChatGPT运营商**现已使用Web Bot Auth对其请求进行签名，因此获得访问许可。

了解更多关于**Bot Management**（机器人管理）的信息。

---

> 本文由AI自动翻译，原文链接：[Vercel's bot verification now supports Web Bot Auth - Vercel](https://vercel.com/changelog/vercels-bot-verification-now-supports-web-bot-auth)
> 
> 翻译时间：2026-04-06 04:54
