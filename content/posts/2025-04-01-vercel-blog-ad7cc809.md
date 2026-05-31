---
title: Vercel攻击挑战模式支持验证机器人与Cron任务
title_original: Attack Challenge Mode now allows verified bots and Vercel cron jobs
  - Vercel
date: '2025-04-01'
source: Vercel Blog
source_url: https://vercel.com/changelog/attack-challenge-mode-now-allows-verified-bots-and-vercel-cron-jobs
author: ''
summary: Vercel宣布其攻击挑战模式现已允许已验证的Webhook提供商（如Stripe、PayPal）和合规搜索引擎机器人（如Googlebot）自动绕过挑战，确保支付处理与搜索抓取不受中断。同时，同一账户内的Vercel
  Cron任务也免于挑战，被视为受信任内部流量。用户可通过自定义规则屏蔽特定已知机器人，但所有已知机器人都经过真实性验证，无法伪造。此举旨在平衡安全防护与关键业务流量的连续性。
categories:
- AI基础设施
tags:
- Vercel
- 攻击挑战模式
- Webhook
- 机器人验证
- Cron任务
draft: false
translated_at: '2026-05-31T06:17:07.074626'
---

已验证的Webhook提供商（包括Stripe和PayPal）现已在攻击挑战模式下自动获得许可，确保支付处理不受中断。来自主要搜索引擎（如Googlebot）和分析平台的合规机器人同样获得支持。

Vercel Cron任务在同一账户内运行时，现可免于挑战。与其他受信任的内部流量一样，它们会自动绕过攻击挑战模式。

如需屏蔽特定已知机器人，可创建一条匹配其用户代理（User Agent）的自定义规则。已知机器人均经过真实性验证，无法通过伪造手段绕过攻击挑战模式。

进一步了解攻击挑战模式，以及Vercel如何维护其合法机器人目录。

---

> 本文由AI自动翻译，原文链接：[Attack Challenge Mode now allows verified bots and Vercel cron jobs - Vercel](https://vercel.com/changelog/attack-challenge-mode-now-allows-verified-bots-and-vercel-cron-jobs)
> 
> 翻译时间：2026-05-31 06:17
