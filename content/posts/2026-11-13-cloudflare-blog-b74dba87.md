---
title: 'Introducing Spend Management: Spending limits and alerts for Cloudflare'
title_original: 'Introducing Spend Management: Spending limits and alerts for Cloudflare'
date: '2026-11-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/spend-management/
author: ''
summary: '[翻译失败，原文如下]


  Spend controls have been at the top of the list of most requested features from
  developers building on our developer platform for quite s...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-14T08:49:31.899302'
---

[翻译失败，原文如下]

Spend controls have been at the top of the list of most requested features from developers building on our developer platform for quite some time now. Withmore than 10 million developersÂ now building on Cloudflare,Â this matters more than ever.

Although weâve hadusage notificationsÂ andbudget alertsÂ available to paid plans for a while, this doesnât solve the problem completely; informing is not the same as controlling.

You can now set spending thresholds and choose to have Cloudflare pause activity when those limits are reached, thus avoiding unexpected bills from unplanned usage. Today, we're introducingSpend ManagementÂ in Beta, for any pay-as-you-go (PayGo) customer, starting with Workers and Durable Objects.

Use Spend Management alongsideAI Gateway spend limitsto manage compute and AI inference costs across your application. AI Gateway already supports per-user and per-model budgets for Workers AI and other AI providers, applied to requests routed through your gateway.

## How it works

You can start using Spend Management using the dashboard,cf CLI, orREST API.

In thedashboard, head over to ManageAccountÂ >BillingÂ >Spend limitsÂ and enable the products for which you want to control spending.

When you enable controls on a product, you can define a spending limit, specify a recipient email for notifications, and set one or more alert thresholds.

![workers spending controls.png](/images/posts/766a0cf09fd0.jpg)

If you configure a recipient email, Cloudflare will send notifications when the evaluated spend reaches one of the thresholds or your spending limit. When the limit is reached, a blocking policy is enforced and your product is paused automatically.

![](/images/posts/a487ddb802e6.jpg)

If you go to thedashboard,Â you can see the current billing cycle costs for each supported product in near real time (under 10 minutes), and manage your settings and thresholds from there. The overview panel tells you which products have thresholds and limits configured. In this example, you can see that Workers triggered two alerts before hitting the hard limit.

![](/images/posts/8778d740af4f.jpg)

Note that the billing cycle starts when the paid subscription begins, not when you deploy a Worker or create a spending cap; a subscription starting October 10 generally has a cycle of October 10-November 10 â not a calendar month.

The dashboard also shows an audit log, so you can see who changed a limit and when, or when a cap was reached.

![](/images/posts/f14f2c3d1602.jpg)

As with most Cloudflare services, Spend Management is also an API that you can use programmatically; the documentation can be found in ourDeveloper Documentation. Hereâs an example, but using the API:

```
curl --fail-with-body --request POST \
  "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/billing/spend-policies" \
  --header "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Workers spending cap",
    "product_id": "workers",
    "enabled": true,
    "threshold_cents": 10000,
    "action": "usage_block",
    "notification_email": "me@example.com"
  }'
```

And, of course, you can usecf, the CLI for the entire Cloudflare API:

```
cf billing spend-policies list
cf billing spend-policies create
cf billing spend-policies get
cf billing spend-policies update
cf billing spend-policies delete
cf billing spend-policies audit list
cf billing spend-policies activity list

cf billing spend-policies create --body '{
  "name": "Workers spending cap",
  "product_id": "workers",
  "enabled": true,
  "threshold_cents": 10000,
  "action": "usage_block",
  "notification_email": "me@example.com"
}'
```

Once a cap is enforced, new invocations of that product are rejected. Note that we only pause customer-code invocations that incur costs â in Workers, for example, Cron Triggers and Queue consumer invocations are paused, but static assets continue to be served.

To resume service, you can:

- Raise the limit above the current cycleâs accumulated spend.
- Disable or delete the blocking policy.
- Wait until the next billing cycle, when the existing block expires.

Thatâs it. You can start using Spend Management for Workers and Durable Objects today, and other products will follow soon.

Read on to learn how we built the system, and whatâs going to happen next.

## How we built Spend Management

As easy and straightforward as it seems on the surface, building a system like this at Cloudflare scale was no small feat. From an invocation anywhere on our distributed network to a blocking decision that we need to apply globally, building Spend Management requiredÂ working with multiple teams, changing code in existing systems, and creating new systems from scratch.

Letâs start by looking at the bird's-eye view of a capped billable event:

![](/images/posts/9e079c3bd71d.jpg)

Now let's dig deeper.

## Collecting and aggregating close to the source

Each invocation produces usage measurements: requests, CPU time, execution duration, or storage operations, depending on the product. But transporting and processing this volume of raw data all the way from the sources down to the rating engine would not scale or be efficient.

So what we do is we collect and aggregate the measurements as close to the source as possible using a two-stage metering pipeline that combines events into usage aggregates, so the engine sees accumulated usage rather than having to process all the events one by one.

Let's look at a diagram.

![](/images/posts/f7b07ba8e016.jpg)

The first stage reduces raw-event volume close to parsing down to one-minute windows. Each metering parser converts raw events into usage measurements, then combines matching measurements into typically one-minute buckets. Still, several records can describe the same account and time window.

In the second stage, a separate service merges those first-stage partial aggregates using the same grouping rules, but over typically five-minute windows, and further reduces the volume before downstream processing by the Usage Engine. Here we also archive the consolidated aggregates; this gives us a durable dataset for later analytics and reconciliation.

The nice thing about this two-stage pipeline is that it reduces the raw event volume early, so the downstream engines process only the aggregated usage they need to calculate spend and act on it. Thatâs what makes this practical at Cloudflareâs scale.

### Usage Engine: account-partitioned processing

TheUsage EngineÂ translates aggregated measurements into usage records, which are standardized records containing the account, usage window, metric, quantity, and relevant dimensions. In other words, it maps product-specific meters into supported usage metrics.

We partition processing by account, so an accountâs usage and subscription information meet in the same place. That lets us maintain its accumulated usage and apply included allowances without coordinating across pricing processors on every update.

![](/images/posts/860abac06943.jpg)

As you can see, we run different partitions in parallel, giving us a way to spread the work across accounts while keeping each accountâs pricing state together. Also note that each partition keeps both a local state for fast access, and also a durable write-ahead logging (WAL) changelog on disk. This buys us:

- Less cross-partition coordination:Â each accountâs usage and subscription state stay together.
- Consistent pricing: usage updates share the same allowance and accumulated-spend state.
- Parallel processing: different partitions calculate spend independently.
- Recoverability: durable state lets replacement processors rebuild and resume after failures, if necessary.

Then, finally, the usage metrics are fed into the Rating Engine.

### The Rating Engine

[翻译失败，原文如下]

The Rating Engine is the most important block of Spend Management; it turns usage into monetary value and itâs whatâs able to answer the question: âGiven what this account has consumed, its subscription, and its pricing, how much has it spent so far?â

Hereâs how it works.

![](/images/posts/36f517a12823.jpg)

In essence, the Rating Engine brings together three things:

- Usage records: quantities such as requests and CPU milliseconds.
- Subscription information: the accountâs billing period and plan changes.
- Pricing rules: rates, included allowances, and billing rounding.

### Usage data and subscriptions are independent streams

Usage and subscription updates arrive as independent streams, so we canât assume they reach the Rating Engine in order. Furthermore, we have to be able to recover from a data processing failure or missing subscription information from, say, a failed webhook.

If usage arrives before the subscription information needed to price it, we retain it as pending and revisit it when that information becomes available. This lets us tolerate temporary delays without treating unpriced usage as free.

### Tracking accumulated spend

Finally, we calculate and track accumulated spend. The Rating Engine uses a product catalog database that defines usage metrics, including allowances, rates, and rounding rules, alongside the accountâs subscription information. One million CPU milliseconds doesnât necessarily mean an extra charge: the engine first applies the accountâs included CPU allowance, then prices any excess. It prices accumulated usage rather than rounding and charging for each request independently.

Once the accumulated spend is calculated, two steps follow:

- Policy evaluation: decide whether one or more warning or blocking thresholds have been reached.
- Reporting: we show estimated usage charges in the dashboard via our APIs, and we send out email alerts (via CloudflareEmail Service) if necessary.

### Asynchronous cap enforcement

The Rating Engine doesnât sit in the request path or directly reject requests. Instead, the policy service sends the cap to our runtime configuration service andQuicksilver, our internal key-value store developed to enable fast global replication and low-latency access at planet scale. This propagates it to all our nodes asynchronously.

![](/images/posts/b909804feb9b.jpg)

Once the cap reaches Quicksilver, the runtime picks it up during its periodic refresh and starts rejecting capped invocations or operations.

In other words,enforcement uses local state, so requests never have to wait on the Rating Engine. By reusing our existing runtime account-limit architecture, we keep rating out of the request path while distributing caps across the global network.

## Whatâs next

Any pay-as-you-go customer can start using Spend Management today. While this is a major milestone in our roadmap, itâs also just the start. Let us share some of our plans for the next few weeks and months ahead.

### More products

We are starting with caps for Workers and Durable Objects, but youâll be able to measure and cap many other Cloudflare products and primitives in the near future. Weâve built the system in a way that makes it easy and familiar for our products to onboard, so expect the catalog to grow.

### Closer to real time

While near real time under 10 minutesÂ is a great benchmark, weâre not satisfied with it, and being the stubborn engineers we are, we have pretty good ideas on how to reduce that time even further. Expect us to shorten the gap between measurement and enforcement over time, hopefully to under a minute.

### Agent and application-based budgets

Right now, we measure spend by products and primitives, but there are other useful dimensions to explore when controlling costs. For example, a developer might want to monitor the costs of a specific application â such as a Worker script that uses other primitives like R2 or Workers AI. How can we measure the aggregated cost of an entire application and pause that application, rather than disabling the underlying primitives across all customer applications?

Another compelling use case for cost controls is AI agents. Weâve all read horror stories about rogue agents entering unconstrained recursive reasoning loops to brute-force a problem â generating thousands of dollars in costs from high-frequency, expensive API calls, not to mention causing denial-of-service (DoS) issues on databases and other services. AI Gateway already lets you give an agent a budget for AI requests routed through it. A task can also consume compute, database, and storage resources. We want to make it possible to budget for that broader resource use across products.

Youâll be able to tag the calls from your agents and our pipeline will carry that metadata from the runtime through to the Rating Engine. That will let us attribute spend and pause an application or an agentic task across products, without interrupting other unrelated applications.

## Get started

This launch is a first step toward making spend controls a normal part of building on Cloudflare, alongside deploying code and monitoring your applications.

Check out thebilling developer documentationÂ for more information. Start using Spend Management and tell us what works, whatâs missing, or where more granular budgets would help.

Join us on Discord or our socials. Weâre listening!

- Cloudflare
- Celso Martinho
- Sid Chatterjee
- Brendan Irvine-Broque
- AndrÃ© Cruz

---

> 本文由AI自动翻译，原文链接：[Introducing Spend Management: Spending limits and alerts for Cloudflare](https://blog.cloudflare.com/spend-management/)
> 
> 翻译时间：2026-11-14 08:49
