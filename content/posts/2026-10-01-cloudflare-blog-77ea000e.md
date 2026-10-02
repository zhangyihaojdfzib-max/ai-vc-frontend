---
title: "Introducing Workers KV Instant â\x80\x94 powered by Quicksilver"
title_original: "Introducing Workers KV Instant â\x80\x94 powered by Quicksilver"
date: '2026-10-01'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workers-kv-instant/
author: ''
summary: "[翻译失败，原文如下]\n\nToday, weâ\x80\x99re introducing Workers KV Instant, a new\
  \ mode for Workers KV that pushes your changes globally for instant availability\
  \ witho..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:38.611831'
---

[翻译失败，原文如下]

Today, weâre introducing Workers KV Instant, a new mode for Workers KV that pushes your changes globally for instant availability without cold read penalties.

Workers KVhas been one of our most popular services on the Developer Platform sincelaunching during Birthday Week in 2018. Itâs great for quickly accessing data like static assets and user configuration that is written occasionally but read frequently. We use it ourselves across many Cloudflare products.

We also have another key-value store, Quicksilver, which weâveblogged aboutmany times sinceintroducing it in 2020. We designed Quicksilver for incredibly fast global replication and low-latency access, and nearly every request to Cloudflare looks up at least one key in Quicksilver. People have asked us for years, but weâve never made Quicksilver available to our customers.

Weâre changing that today with Workers KV Instant. KV Instant mode provides the same API as Workers KV, but powers it using Quicksilver. KV Instant offers 100 times faster p99 reads and immediate updates, with no need to wait for a TTL to expire. Itâs not for every type of data, but, for infrequently updated application configuration data âÂ the same thing we use Quicksilver for ourselves â KV Instant shines.Â

## 100x faster reads than Workers KV

KV Instant offers read latency that is over 100 times faster than classic mode, with reads resolving in under two milliseconds even at the 99th percentile of response time (p99), and 95th percentile (p95) times measured in microseconds. Writes are pushed to the edge over 20 times faster, with 99% of all writes replicating in around 250ms.

These high-performance characteristics of KV Instant make it ideal for reading data in the hot path of your applications, especially flags and settings that should be available globally nearly instantly after theyâve been written.

p99 reads (cached)

p99 reads (all)

median write replication

p95 write replication

p99 write replicationÂ

Instant

1.62 ms

107 ms(1)

181ms(1)

256 ms(1)

Classic

160 ms

287 ms

< 1 s(2, 3)

4.38 s(2)

Table notes:

1. Time to replicate to all edge locations (over 300 as of publication)
2. Time to replicate across all required storage backends
3. We do not have sub-second fidelity for replication lag in classic mode

KV Instant is powered byQuicksilver v2, a key-value store developed internally by Cloudflare to enable fast global replication and low-latency access on a planet scale.

## The same simple API as Workers KV â get(), put() list(), delete()

KV Instant uses the familiarWorkers KV APIyou build with today.

For example, letâs say youâre working on a big product launch, and need to be able to switch whatâs on the homepage right at 10:13 AM when the product is introduced at the keynote on stage. You need some key that you can read, that introduces near zero latency, you can read on every request no matter the scale, and updates instantly when you change it.

```
async fetch(request, env, ctx) {
  // Read the launch flag from KV Instant on every request
  const launched = (await env.APP_CONFIG.get("new-product-launched")) === "true";

  if (launched) {
    // Serve the launch homepage
    return new Response({...});
  }

  return new Response({...});
},
```

Most binding operations are compatible with the Workers KV classic equivalents. There are three key differences when working with KV Instant:

- You must specify KV Instant mode when creating a KV namespace. (pass theâmodeâ:âinstantâattribute)
- Metadata is not supported, sogetWithMetadatacalls always returnnulland there is no support for passing metadata input.
- listoperations in KV Instant returnallmatching keys in a namespace; there is no pagination.

For additional API examples, seethe Workers KV docs.

## Pricing â reads cost 60% less than classic Workers KV

KV Instant is priced to fit the read-heavy, small data workloads it excels at serving. Because we propagate data to every Cloudflare location, using the sameQuicksilverkey-value store weâve spent years learning how to operate at scale on the hot path of every request, we can offer pricing for reads that is 60% less than Workers KV, and much less than other global configuration products.

Conversely, storage and Class A operations are significantly more expensive than Workers KV. If you need to store large amounts of data, or update it frequently, Workers KV continues to be a great fit. Each mode is designed for a very different type of data and access pattern.

KV Instant namespaces are priced in three dimensions: data storage, class A operations, and class B operations.

Class B operations (reads)

Class A operations (put, delete, list)

Storage

Workers KV Instant

$0.20 per million

$0.10 per operation

$100 per MB, per month

Workers KV

$0.50 per million

$5.00 per million

$0.50 per GB, per month

Storage is billed at $100 per MB, per month. Each key can be up to 300 bytes, and values can be any size that does not cause the namespace to exceed one megabyte in total size. KV Instant namespaces can contain up to 10,000 key value pairs of any type.

Class A operations

Class A operationsÂ  (put,delete, andlist) are charged at $0.10 per operation. Each key written or deleted counts as one Class A operation. Each list request counts as one Class A operation,regardless of how many keys are returned in the response.A singlelistoperation can return all the key value pairs in a namespace in a single page.

Because writes must pass through a single system of record, KV Instant also restricts write frequency to one write per namespace per second. This is similar to classic Workers KVâs restriction of one write per key per second, and makes it easier for you to reason about update order in your application.

Class B operations

Class B operations (get) are charged at $0.20 per million keys requested, 60%cheaperthan Workers KV default mode. When requesting multiple keys in a singlegetoperation, each requested key is billed as one class B operation. For example, the following approaches both incur three class B operations and are equivalent from a billing perspective.

```
// Requesting keys via three individual get operations 
// incurs three Class B operations.
let routeAPAC = await APP_CONFIG.get("route_APAC");
let routeEUR = await APP_CONFIG.get("route_EUR");
let routeNAMER = await APP_CONFIG.get("route_NAMER");

// Requesting three keys in a single get operation 
// also incurs three Class B operations.
let routes = await APP_CONFIG.get(["route_APAC", "route_EUR", "route_NAMER"]);
```

## Workers KV Instant is in private beta

KV Instant is launching today in private beta. Weâre excited to start working with customers who want to try it, then open it up more widely, and would love to hear from you. You can sign up for the private betahere. Tell us what youâre building!

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Introducing Workers KV Instant â powered by Quicksilver](https://blog.cloudflare.com/workers-kv-instant/)
> 
> 翻译时间：2026-10-02 08:10
