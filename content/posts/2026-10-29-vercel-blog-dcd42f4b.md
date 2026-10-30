---
title: IP geolocation now covers more visitors at higher resolution - Vercel
title_original: IP geolocation now covers more visitors at higher resolution - Vercel
date: '2026-10-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/improved-ip-geolocation-data
author: ''
summary: '[翻译失败，原文如下]


  IP geolocationon Vercel now resolves visitor locations with finer network granularity,
  delivering city-level data for nearly all requests...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:47:56.822716'
---

[翻译失败，原文如下]

IP geolocationon Vercel now resolves visitor locations with finer network granularity, delivering city-level data for nearly all requests and postal-code data for 90% of traffic.

Geolocation data is now refreshed more often, so locations keep up as IP ranges are reassigned and routing changes. This is enabled for all projects with no code or configuration changes required. Existing geolocation headers along with thegeolocation()helperin@vercel/functions, return the same fields forVercel FunctionsandRouting Middleware.

If you use geolocation for access controls, localization, or compliance, some visitors will now resolve to a different city or country, most often traffic from VPNs, hosting providers, and leased IP ranges:

- Physical termination location:Subnets announced from a hosting provider in a different country than their regional internet registry (RIR) record now resolve to the data center where the traffic actually terminates.
- Testing geo-dependent routes:Verify access rules against an IP's active network location rather than its static registry allocation.

Physical termination location:

Subnets announced from a hosting provider in a different country than their regional internet registry (RIR) record now resolve to the data center where the traffic actually terminates.

Testing geo-dependent routes:

Verify access rules against an IP's active network location rather than its static registry allocation.

Read therequest headers documentationfor all available geolocation headers and fields.

---

> 本文由AI自动翻译，原文链接：[IP geolocation now covers more visitors at higher resolution - Vercel](https://vercel.com/changelog/improved-ip-geolocation-data)
> 
> 翻译时间：2026-10-30 08:47
