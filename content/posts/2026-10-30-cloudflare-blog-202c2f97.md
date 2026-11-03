---
title: Cloudflare servicesÂ for private originsÂ is now generally available
title_original: Cloudflare servicesÂ for private originsÂ is now generally available
date: '2026-10-30'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/private-origins-public-to-private/
author: ''
summary: '[翻译失败，原文如下]


  Today, Cloudflare services for private origins is generallyÂ available. Point a
  proxied DNS record at a private IP, and Cloudflare reache...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-03T09:14:35.053596'
---

[翻译失败，原文如下]

Today, Cloudflare services for private origins is generallyÂ available. Point a proxied DNS record at a private IP, and Cloudflare reaches the origin over your existingCloudflare One connection. Your origin stays private, while web application firewall (WAF),caching,bot management, andWorkersÂ work just as they do for public origins.

In June,we launched this capability in closed betaÂ to address a problem we kept hearing from customers: Their internal APIs, AI agent backends, MCP servers, and operational tools werenât built to face the Internet, but those services still need to accept requests from partners, customers, or agents over the Internet. Before the beta, putting Cloudflare in front of these services meant exposing a public IP, opening a firewall port, or runningcloudflaredÂ alongside the origin.

Those requirements often left private applications without the same protections and controls they used for public applications, including WAF, bot management, rate limiting, caching, traffic acceleration, rewrites, and Workers.

### What is generally available today

During the closed beta, eligible customers requested access through their account team. Today, weâre opening access beyond that beta group.

Point a proxied A or AAAA record at a private IP, and Cloudflareâs application services work as they do for public origins:

- WAF and managed rules
- Bot management
- Rate limiting
- Caching
- Transform and rewrite rules
- Workers

Some limitations remain.Argo Smart RoutingandDedicated CDN Egress IPsarenât supported, and origin health checks requireLoad Balancing. See thedeveloper documentationfor the full list of current limitations.Â

Your origin keeps its private IP, with no inbound firewall exception required. WithCloudflare WAN,Â  no connector software on the origin is required. WithCloudflare Mesh, a connector runs within your private network and can serve multiple origins.

### How it works

Create a proxied A or AAAA record pointing to your origin. For supported private IP ranges,useprivate network routingÂ is enabled automatically. If your origin uses a public IP thatâs reachable only through your private network, you can enable the setting manually.

The rest of the request flow stays the same: TLS termination, WAF, rules, and caching continue to run on Cloudflareâs network.

![](/images/posts/42cd64733817.jpg)

The setting turns on automatically for RFC 1918 private IPv4 addresses, RFC 6598 CGNAT addresses (100.64.0.0/10), and RFC 4193 unique local IPv6 addresses (fc00::/7). It canât be turned off for these ranges; attempts to disable it through the API return an error.

### What the API looks like

For customers automating deployments through the API, private routing is simply an additional attribute on a standard DNS record.

```
POST /zones/{zone_id}/dns_records
{
 "type": "A",
 "name": "app.example.com",
 "content": "10.0.0.50",
 "ttl": 300,
 "proxied": true,
 "private_routing": true
}

```

Behind the scenes, Cloudflare's proxy platform determines where to send traffic forapp.example.comÂ by querying Cloudflare's Origin API. The response includes metadata indicating that the destination should be reached through a private network path:

```
{
 "zone_name": "example.com",
 "ipv4_addresses": ["10.0.0.50"],
 "private_routing": true
}
```

Theprivate_routingÂ flag is the key signal. When our proxy sees it, instead of attempting to connect directly to the private IP address over the public Internet, it hands the request to our private networking layer, which then routes the connection across the customer's existing private network connectivity, whether that'sIPsec,GRE,Cloudflare Tunnel,CNI, or Cloudflare Mesh.

TheÂbeta postÂ covers the routing layer in more detail.

### Get started

Before you begin, youâll need:

1. The Private Origins entitlement on your account. Ask your account team to turn it on.
2. Cloudflare One connectivityusing IPsec, GRE, CNI, Cloudflare Tunnel, orCloudflare Mesh.
3. Unified Routing enabled on your account, unless you connect over Cloudflare Tunnel (Tunnel doesn't need it). New and existing accounts can upgrade through their account team.
4. If you connect over Cloudflare WAN or Cloudflare Mesh, configure a return route for Cloudflareâs source ranges: 100.64.0.0/12 for IPv4 and 2606:4700:cf1:5000::/64 for IPv6. Then, create a proxied A or AAAA record for the private IP and confirm thatUse private network routingis enabled. Your existing WAF, cache, and bot management configuration applies to that hostname without further changes.

Then, create a proxied A or AAAA record for the private IP and confirm thatUse private network routingÂ is enabled. Your existing WAF, cache, and bot management configuration applies to that hostname without further changes.

One note from the beta: if requests time out and nothing arrives at the origin, check the return route first. A missing route for Cloudflareâs source range was the most common setup failure we saw.

Once enabled, follow ourÂdeveloper documentation, which walks through the full setup.

### What comes next

Todayâs release covers public traffic reaching private origins. Next, weâre working on private-to-private traffic: users, services, and AI agents on private networks reaching applications on other private networks through Cloudflareâs application services.

![](/images/posts/d7ab4639f9ed.jpg)

Engineering work is underway, and weâre targeting a closed beta in early 2027. If youâd like to participate, talk to your account team.

The goal is to give private applications the same protections and controls as public applications. An employee openingwiki.company.internal, for example, could benefit from WAF, rate limiting, and bot management. Service-to-service traffic between clouds and data centers could use those controls too, even when neither side touches the public Internet.

For now, todayâs release brings the WAF, caching, bot management, and Workers you use for public applications to private origins over connectivity you already operate.

Questions or feedback? Join the conversation in ourÂcommunity forumsÂ or reach out to your account team.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Cloudflare servicesÂ for private originsÂ is now generally available](https://blog.cloudflare.com/private-origins-public-to-private/)
> 
> 翻译时间：2026-11-03 09:14
