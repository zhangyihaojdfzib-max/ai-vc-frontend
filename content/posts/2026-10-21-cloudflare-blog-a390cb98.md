---
title: How Commerce.com and Cloudflare are getting storefronts ready for AI agents
title_original: How Commerce.com and Cloudflare are getting storefronts ready for
  AI agents
date: '2026-10-21'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/webmcp-commerce/
author: ''
summary: "[翻译失败，原文如下]\n\nAI can write code and pass the bar exam, but it still struggles\
  \ to buy a pair of shoes online.\n\nThatâ\x80\x99s because websites were built for\
  \ ..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:55:51.866711'
---

[翻译失败，原文如下]

AI can write code and pass the bar exam, but it still struggles to buy a pair of shoes online.

Thatâs because websites were built for humans, not agents. Most agents that shop for someone today work from a siteâs HTML â they look at the page, guess which button does what, click, and try again when they get it wrong. This process is slow, uses a lot of tokens, and something as seemingly innocuous as a theme change can break it.

Enter WebMCP: a browser standard from Google that gives AI agents structured tools on a page, likesearch_products. Instead of hunting for buttons, the agent calls the exact tool it needs directly, making shopping faster, cheaper, and far more reliable. Because WebMCP is still an experimental proposed browser standard in early preview, itâs currently available behind experimental Chrome flags (chrome://flags/#enable-webmcp-testing), in Chrome Origin Trials, in some agentic browsers, and across developer environments likeCloudflare Kitesurf.

In August, we launchededge implementation of WebMCPÂ in beta. Turn it on, and Cloudflare injects a tiny script at the edge to make those tools available automatically, without site owners writing a single line of code.

Commerce.com, a flexible commerce platform built for the age of AI, already uses Cloudflare to run their almost 100,000 domains. So when the preview came out, they asked:Can we turn this on for all of our stores at once?

Hereâs why Commerce.com wanted WebMCP, how we built edge-level opt-outs to give every merchant control, and what we learned along the way.

## Why Commerce.com wanted WebMCP

Kristina Pototska, Product Management Director at Commerce.com, explains why this matters for storefronts:

âMerchants keep asking us how they can keep up with agentic shopping. When a shopper asks an agent to find something, merchants want their store to be in the answer. They want to keep the customer, keep control of the checkout, and do it without rebuilding their site. WebMCP helps with all three. The agent gets real tools to search products, check details, build a cart, and get a checkout link, so it doesnât have to guess its way around the page. The human shopper stays on the merchantâs site, and the merchant keeps the relationship.

We wanted to turn this on in a secure way, and without asking merchants to edit their theme or do anything by hand. Thatâs where the Cloudflare partnership worked perfectly.

WebMCP also works side by side with our server-sideMCP, and together they cover the different ways people shop with agents. Server-side MCP supports agents that connect to a store directly, like an assistant helping someone shop across several sites. WebMCP supports agents that work in the shopperâs browser. Itâs the same set of shopping tools in both cases, so merchants donât have to choose between the two or manage them separately.â

Under the hood, this integration relies on two key principles. First, the WebMCP tools execute directly inside the shopper's active browser session on the storefront's domain, ensuring the agent sees the same prices and cart. No credentials go to a third party, and the visit still happens on the merchant's site. Second, Cloudflare serves as the edge delivery layer for Commerce.comâs backend MCP server, proxying tool definitions and actions unchanged so merchants maintain full control over their tool logic.

## What a shopper's agent sees

When visiting an enabled Commerce.com storefront, an AI assistant no longer has to guess how to navigate the site. Instead, it can instantly discover tools via WebMCP.

Suppose you tell your agent:"Find me a waterproof trail running shoe under $140 in size 10 and add it to my cart."

Without WebMCP:Â The agent attempts to simulate human clicks, only to get blocked by cookie banners, misinterpret variant drop-downs, or get tripped up by bot challenges that try to distinguish automated traffic from real customers.

With WebMCP:The agent detects the store's tools ondocument.modelContextÂ and makes two clean calls:

1. search_products({ query: "trail running shoe", max_price: 140, size: 10 })
2. add_to_cart({ product_id: "shoe_123" })

![](/images/posts/0a0ef4a28dfb.jpg)

Because the agent runs inside your active browser session on the store's domain, your cart updates in real time. Commerce.comâs backend MCP server determines the commerce flow:Â when youâre ready to complete the purchase, you click checkout yourselfÂ â keeping your payment details secure and leaving you in complete control of the final buy.

## What we built together

When Commerce.com asked to turn on WebMCP across almost 100000 storefronts, we ran into a practical challenge: WebMCP was originally designed as a single on-or-off switch for an entire domain zone.

Commerce wanted to enable our mcp-server-client toolpack, which acts as an edge bridge â proxying tool definitions and requests directly from Commerce.comâs backend MCP server to the visitor's browser. Because Commerce.com uses Cloudflare for SaaS to host thousands of merchant vanity domains on shared zones, we needed a way to deliver this platform-wide while giving individual store owners an easy way to opt out.

### 1. On for all stores on Commerce.com, with an opt-out for each merchant

Instead of building a complex custom allowlist, we hooked WebMCP into the existing Cloudflare concepts ofConfiguration RulesÂ andcustom hostname metadata.

Commerce.com turns WebMCP on for their main zone, then adds a rule at the edge that checks merchant metadata. If a merchant flips the "opt-out" switch in their Commerce.com dashboard, Cloudflare bypasses WebMCP for that specific storefront automatically:

```
{
  "action": "set_config",
  "expression": "cf.hostname.metadata.webmcp_opt_out eq \"true\"",
  "action_parameters": {
    "webmcp_enabled": false
  }
}
```

Because Cloudflare evaluates these rules at the edge before serving the page, an opted-out store gets zero extra latency, no remote lookups, and no injected scripts.

### 2. Tailored endpoints and safe fallbacks

As with any preview release, working with a partner in the real world revealed a few practical details we hadn't accounted for:

Custom MCP paths:Â When the mcp-server-client toolpack was enabled, our bridge originally expected to find every site's MCP server at /mcp. Commerce.comâs server lives at /api/mcp. To handle this, we added a configurable MCP URL setting at the zone level. When this is set, we pass the custom path into the injected script tag:

```
<script type="module"
    src="/.webmcp/bridge.js"
    data-packs="c2pa,mcp-server-client"
    data-mcp-url="/api/mcp"></script>
```

Seamless fallbacks:Â If a store's MCP server is offline or a customer's browser doesn't support WebMCP, the script exits. The storefront loads normally and human shoppers aren't affected.

## What's next

We'll keep investing in WebMCP as the standard evolves, starting with helping agents find a site's tools more easily. Cloudflare andCommerce.comÂ will continue to work together to make shopping with agents fast, reliable and safe for both merchants and shoppers.

If you're atCloudflare ConnectÂ in San Francisco on October 21, 2026, come see us atGetting your storefront agent ready for peak season,Â a panel discussion featuring Kristina Pototska (Product Management Director, Commerce), Justis Blasco (CTO and Co-Founder, Popmenu), Ross Harvey (Head of Infrastructure, Fruugo), and Josh Mills (VP of Engineering, Gopuff).

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[How Commerce.com and Cloudflare are getting storefronts ready for AI agents](https://blog.cloudflare.com/webmcp-commerce/)
> 
> 翻译时间：2026-10-22 06:55
