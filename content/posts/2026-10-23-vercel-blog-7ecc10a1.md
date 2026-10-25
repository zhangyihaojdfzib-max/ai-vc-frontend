---
title: Vercel Connect adds managed Stripe API keys - Vercel
title_original: Vercel Connect adds managed Stripe API keys - Vercel
date: '2026-10-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-connect-adds-managed-stripe-api-keys
author: ''
summary: '[翻译失败，原文如下]


  Vercel Connectcan now create a separaterestricted Stripe API keyfor each agent or
  task. When you create a Stripe connector, you can now c...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-25T07:10:20.926452'
---

[翻译失败，原文如下]

Vercel Connectcan now create a separaterestricted Stripe API keyfor each agent or task. When you create a Stripe connector, you can now choose Managed API Key as the connection method.

Vercel creates the key in your Stripe account, limited to the permissions you pick. The existing MCP and bring-your-own API key methods are unchanged.

![](/images/posts/abd58002d484.jpg)

![](/images/posts/fa8dedb8d12a.jpg)

Most apps and agents run on Stripe’s default secret key, which has full access to the account. With per-agent keys, each agent gets only the access its job needs. For example, a daily revenue report agent can be limited to read-only access to charges, and an onboarding agent can be limited to write access to customers.

Vercel creates and stores the key, so there is no secret key to paste. You can rotate it from the connector's settings without redeploying, and the old key stays valid for up to 24 hours while you switch.

### Copy link to headingAdd the Stripe connector

Create a Stripe connector from the connectors directory, choose Managed API Key, pick its permissions, and attach it to your project. You can also start from the CLI, which opens the browser to finish setup:

```
1vercel connect create stripe --connection-method managed-api-key --name acme-stripe2vercel connect attach stripe/acme-stripe --project my-app --environment production
```

Add the Stripe connector with the Vercel CLI

```
1import Stripe from 'stripe';2import { getToken } from '@vercel/connect';3const key = await getToken('stripe/acme-stripe', {4  subject: { type: 'app' },5});6const stripe = new Stripe(key);7const customers = await stripe.customers.list({ limit: 10 });
```

Call getToken with the connector’s UID to get the restricted key at runtime

To get started, add theStripe connectoror read thedocumentation.

---

> 本文由AI自动翻译，原文链接：[Vercel Connect adds managed Stripe API keys - Vercel](https://vercel.com/changelog/vercel-connect-adds-managed-stripe-api-keys)
> 
> 翻译时间：2026-10-25 07:10
