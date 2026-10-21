---
title: Vercel and Shopify make agents first-class shoppers
title_original: Vercel and Shopify make agents first-class shoppers
date: '2026-10-16'
source: Vercel Blog
source_url: https://vercel.com/blog/vercel-and-shopify-make-agents-first-class-shoppers
author: ''
summary: '[翻译失败，原文如下]


  Agents already shop on the web, but they often use pages and tools originally built
  for people and search engines. Building a better shop...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T07:19:54.731545'
---

[翻译失败，原文如下]

Agents already shop on the web, but they often use pages and tools originally built for people and search engines. Building a better shopping experience for agents means treating them as first-class shoppers, with product information they can read directly and tools designed for agents to shop.

Today,Vercel Shop, our open sourceNext.jsstorefront template forShopify, is generally available. Teams can launch storefronts optimized for how people, search engines, and agents interact with them.

![Shopify CEO Tobi Lütke and Vercel CEO Guillermo Rauch discuss the future of agent commerce at Vercel Ship SF.](/images/posts/4266e020093c.jpg)

Vercel Shop is built onShopify’s Hydrogen SDK. The SDK gives teams access to the store’s product catalog, cart and order management, payments, and checkout to build custom storefronts. Earlier this year,Vercel and Shopify announced plans to rebuild Hydrogento work across JavaScript frameworks. Today,the rebuilt SDK is generally available.

## Copy link to headingGive agents the information and tools they need

Vercel Shop makes product pages available asmachine-readable content, including price, availability, and options. The same product URL can serve a visual page to people or product information that agents can read without interpreting the page’s layout. The template also includes structured data embedded in pages and sitemaps to help search and answer engines discover and understand the products.

Shopify co-developed theUniversal Commerce Protocol(UCP), which gives agents a standard way to search a store’s catalog, read product details, check availability, build a cart, and get a checkout link. Vercel Shop makes these capabilities discoverable at the merchant’s own domain, so agents can use MCP to search products and build carts without navigating the site.

## Copy link to headingCustomize the experience for all customers

Vercel Shop brings the store’s product catalog, cart, and checkout together with a Next.js storefront, product information and shopping tools for agents, and a shopping assistant powered byeve. The storefront and assistant live in the same codebase, so teams can customize the store’s design and how the assistant helps shoppers.

Skills included in the templateguide coding agents through setup, customization, and template updates. Teams can create an experience where shoppers browse product pages or ask the assistant to find products and add them to their cart. Both share the same cart, so shoppers keep what they’ve added as they move between experiences.

## Copy link to headingStorefronts built with Shopify and Vercel

Today, we launched our merch store atvercel.storewith limited-edition drops. It’s built on Vercel Shop. The store’s shopping agent helps shoppers find products, add them to their cart, and continue to checkout.

Shopify, Next.js, and Vercel already power storefronts for brands including AG1, Bombas, and PAIGE. When PAIGEre-architected its ecommerce platform, it saw a 22% increase in revenue and a 76% increase in conversion over Black Friday and Cyber Monday, with no downtime.

## Copy link to headingGet started with Vercel Shop

Create a storefront:

```
pnpm create next-app@latest my-store --example https://github.com/vercel/shop
```

Get started withVercel Shop. Check thedocumentationto connect your Shopify store and configure the storefront.

---

> 本文由AI自动翻译，原文链接：[Vercel and Shopify make agents first-class shoppers](https://vercel.com/blog/vercel-and-shopify-make-agents-first-class-shoppers)
> 
> 翻译时间：2026-10-21 07:19
