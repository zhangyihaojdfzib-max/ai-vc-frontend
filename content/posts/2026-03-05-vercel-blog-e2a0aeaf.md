---
title: Vercel 正式集成 Stripe，支持生产环境支付与一键切换
title_original: Stripe is now generally available on the Marketplace and v0 - Vercel
date: '2026-03-05'
source: Vercel Blog
source_url: https://vercel.com/changelog/stripe-is-now-generally-available-on-the-marketplace-and-v0
author: ''
summary: Vercel 宣布 Stripe 支付服务在其 Marketplace 和 v0 平台上正式可用。用户现在可以将生产环境的 Stripe 账户安全连接到
  Vercel，通过环境变量配置 API 密钥，并支持沙盒与实时模式的无缝切换。该集成利用 Stripe 的新密钥管理 API，简化了设置流程并提升了安全性，适用于实时电子商务、SaaS
  计费订阅等生产环境用例，开发者无需手动管理密钥即可从测试迁移到生产环境。
categories:
- AI产品
tags:
- Vercel
- Stripe
- 支付集成
- SaaS
- 开发工具
draft: false
translated_at: '2026-03-08T04:39:15.600803'
---

![](/images/posts/aead310dff62.jpg)

![](/images/posts/914713dd3930.jpg)

您现在可以将您的生产环境 Stripe 账户连接到 Vercel，并开始接受真实支付。该集成会安全地将您的 API 密钥配置为环境变量，并同时支持沙盒和实时模式。

在沙盒环境中测试您的支付流程，然后无需手动交换或管理密钥即可切换到生产环境。通过与 Stripe 合作构建的新密钥管理 API，可以从一开始就减少设置摩擦，同时增强安全性。

这解锁了真实的生产环境用例，例如：

-   **实时电子商务**：接受真实支付并管理生产环境店铺的结账流程
-   **生产环境 SaaS 计费**：从第一天起就为客户收取订阅、使用量和发票费用
-   **向真实用户交付**：无需重新调整集成，即可从沙盒环境迁移到生产环境

实时电子商务：接受真实支付并管理生产环境店铺的结账流程

生产环境 SaaS 计费：从第一天起就为客户收取订阅、使用量和发票费用

向真实用户交付：无需重新调整集成，即可从沙盒环境迁移到生产环境

```
1import Stripe from "stripe"2
3const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)4
5const session = await stripe.checkout.sessions.create({6    ui_mode: 'embedded',7    redirect_on_completion: 'never',8    line_items: [9      {10        price_data: {11          currency: "usd",12          product_data: { name: "T-Shirt" },13          unit_amount: 40_00,14        },15        quantity: 1,16      },17    ],18    mode: 'payment',19  })
```

立即通过此示例开始使用 Vercel 和 Stripe 构建您的第一个简单在线商店。查看文档以了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Stripe is now generally available on the Marketplace and v0 - Vercel](https://vercel.com/changelog/stripe-is-now-generally-available-on-the-marketplace-and-v0)
> 
> 翻译时间：2026-03-08 04:39
