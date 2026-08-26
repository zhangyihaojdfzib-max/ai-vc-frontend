---
title: "The Cloudflare Blog â\x80\x93 Brought to you by EmDash"
title_original: "The Cloudflare Blog â\x80\x93 Brought to you by EmDash"
date: '2026-08-24'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/cloudflare-blog-uses-emdash/
author: ''
summary: '[翻译失败，原文如下]


  You likely noticed the recent redesign of the Cloudflare Blog. We added dark mode,
  modernized the look and feel, and made a lot of other ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:00:25.458707'
---

[翻译失败，原文如下]

You likely noticed the recent redesign of the Cloudflare Blog. We added dark mode, modernized the look and feel, and made a lot of other small improvements along the way.

What you might not have noticed â well, except for those who aremore terminally onlineâ is that the redesign was part of a much bigger migration project. On Wednesday, August 12, we moved the blog toEmDash, a content management system (CMS) built especially to work on Astro and with Cloudflare.

Weâll take you into the migration story â what we learned and how EmDash got better â as well as into the benefits weâre already seeing from a new platform.

## We are Customer Zero

At Cloudflare, Cloudflare itself is Customer Zero. This means that we use our products. And â in use â we make them better for ourselves and our customers.

This is a very real cultural value at Cloudflare. The burden of proof is on you if you want to use an external vendor. Why canât that team support you, what gaps are there, why canât those gaps be filled, and are those âgapsâ true requirements?

This preference is even enshrined in our internal engineering standards, known as our Codex.

We donât just build products for others; we build them to run Cloudflare itself. We are our own first, most demanding customer.

We validate scale, security, and usability on our own massive infrastructure before a paying customer ever touches the product. If a product breaks, it breaks us first. This forces us to fix issues immediately, ensuring that by the time a feature reaches the enterprise, it has already survived the harshest production environment on earth.

With the launch of EmDash and some limitations with our current CMS vendor, we knew that weâd likely be the Customer Zero for EmDash internally at Cloudflare.

## Customer Zero in Action

When we began our initial migration conversations, we started with two main questions:

- Does EmDash work for us?
- Can EmDash scale?

### Does the platform work?

Our first question was the most broad,does EmDash work for us? This is something youâd want to know broadly about any new platform, but especially one thatâs pre-1.0.Â

To answer this question, we ran through a bunch of common user flows, such as:

- Publishing and unpublishing a post
- Authoring a new post
- Scheduling a post
- Adding media items

By and large, EmDash held up pretty well to these usability tests. The gaps we found were generally related to:

- The sheer scale of the Cloudflare Blog (media,content entity search, andbylines)
- Nuances aroundlocalization,SEO, andContent Security Policies (CSPs)
- Usability features for the admin editor â especially ones that might delay the publishing of a post â such aseasier findability for custom HTML blocks,bugs in the in-entity content editor, andkeeping the formatting toolbar in view for longer posts.

The biggest oversight we found was aroundscheduled posts, which didnât work until EmDash version 0.19.0. This gap was understandable given the early version of EmDash, but it was also definitely something we didnât want to be finding outafterthe scheduled time for a post.

### Can EmDash scale?

Our biggest concerns were whether our proposed EmDash setup could handle the traffic we saw on the Cloudflare Blog.

The traffic pattern to our blog is incredibly varied. Normal load sits in the neighborhood of 75 requests per second (RPS), but also spikes up to over 5,000 RPS. Some of these spikes line up with the publishing times of new posts, meaning those posts went viral and attracted a lot of attention. Others happen during all points of the day and night, which likely means folks are sending someextra trafficour way, just to see what happens.Â

Performance also matters for our systems (and our readers). Cloudflare is a web performance company, after all, so the speed at which a page loads becomes incredibly important.

With those two concerns in mind, we built out some scenarios usingk6, an open-source performance testing tool:

- Ramp: Where we gradually increase requests up to triple the prod baseline and then cool down.
- Breakpoint: Where we ramp from 0 to 100 RPS over 10 minutes, stopping when something breaks.
- Burst: Where we throw an immediate traffic load of 7,000 RPS and see what happens.

```
import { randomPageVisit } from "../random-page-visit.ts";

/**
 * Sudden burst to 7,000 RPS.
 */
export const options = {
  scenarios: {
    burst: {
      executor: "constant-arrival-rate",
      rate: 7000,
      timeUnit: "1s",
      duration: "1m",
      preAllocatedVUs: 4000,
      maxVUs: 10000,
    },
  },
  summaryTrendStats: [
    "avg",
    "min",
    "med",
    "max",
    "p(90)",
    "p(95)",
    "p(99)",
    "count",
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],
    "http_req_duration{status:200}": ["p(95)<500", "p(99)<1000"],
    checks: ["rate>0.99"],
  },
};

export default randomPageVisit;

```

For each of those scenarios, we evaluated:

- Availability:Failure when more than 0.01% of HTTP requests lead to 5xx errors, meaning the application couldnât handle the traffic.
- Latency:P95 latency: Failure when more than 5% of responses exceed 500ms.P99 latency: Failure when more than 1% of responses exceed 1000ms.

- P95 latency: Failure when more than 5% of responses exceed 500ms.
- P99 latency: Failure when more than 1% of responses exceed 1000ms.

Armed with these tests â and a lot of internal discussion and data points â we came to our production architecture:

- EmDash, running on a Cloudflare Worker
- Running behind the newWorkers Cache(we believe as the first major site to do so)
- Using the newEmDash object cachebuilt on Workers KV, which the EmDash team built specifically for our use case.
- Using Cloudflareâs new, first-partyHyperdrive integration with PlanetScale.

The multiple layers of caching we put in place play a key role in making the blog both fast and resilient. In the diagram below, they are ordered from top to bottom by proximity to the user:

![BLOG-3455 2.png](/images/posts/99d4837bac02.jpg)

With this setup, weâre typically serving 99.5% of static files from a cache and 70% of requests from a cache, improving frontend performance and decreasing load on the database.

Once we had that architecture in place, we could start thinking about the frontend redesign as well.

## Frontend redesign

Beyond updating the backend architecture, the migration offered us the perfect opportunity to bring the blog's interface into alignment with Cloudflareâs updated visual language. We rebuilt the frontend experience using patterns established by theKumo design system, creating visual and structural consistency between the Cloudflare homepage, dashboard, and marketing sites. The result is a cohesive reading experience that feels like a natural extension of the broader Cloudflare ecosystem.

![BLOG-3455 3.png](/images/posts/faeed48c806b.jpg)

A major priority for this redesign, and a long-overdue request from our readers, was native support for light and dark modes. We implemented theme switching tied directly to system preferences, alongside an explicit toggle, and ensured that accessibility guidelines were strictly met across both themes. Regardless of preference, the updated palette and code syntax highlighting adapt seamlessly without sacrificing legibility.

![BLOG-3455 4.png](/images/posts/90c92746a55d.jpg)

We also took the opportunity to solve a few long-standing user experience quirks, starting with our email subscription form. Previously, the subscription box lived in the top right corner of the page. Because of its placement, readers frequently mistook it for a search bar and typed their search queries directly into the input field.

![BLOG-3455 5.png](/images/posts/7dbc9fd07e8f.jpg)

To fix this, we moved the email sign-up into a dedicated call-to-action block at the bottom of posts.Â

![BLOG-3455 6.png](/images/posts/6c0a0c99fe61.jpg)

[翻译失败，原文如下]

Now, once a reader finishes an article and wants to stay updated, the prompt to subscribe appears naturally at the end of a post.

Finally, we introduced two dedicated sidebar features on interior post pages to improve navigation and community engagement. On the right, an "On this page" table of contents tracks your progress and lets you jump directly to specific sections of longer technical posts. On the left, a new "Discuss Online" section makes it effortless to share articles and engage in conversations across social platforms and developer communities.

![BLOG-3455 7.png](/images/posts/0cbc7d0dc5b1.jpg)

## Rollout strategy

As we got nearer to our migration, we started focusing on the broader question of âhow do we make this change safely?â Ensuring zero downtime for our readers was a non-negotiable requirement, alongside guaranteeing a seamless fallback mechanism if something went wrong at the last minute.

To achieve this, we deployed a proxy Worker to intelligently route traffic between the legacy blog and the new EmDash-powered site. This Worker set a version cookie on requests, which then let us route incoming traffic to the new or legacy experience accordingly. Additionally, this strategy allowed us to fall back to the legacy blog if the new site experienced any 500 errors. Thanks to the flexibility of Cloudflare Workers, this proxy was relatively simple to create and scaled without any issues. The ability to configure a direct worker-to-worker connection through the NEW_BLOG service binding was particularly useful here, as it reduced latency for any end user going through the proxy. This service binding let the proxy Worker dispatch incoming requests directly to the new blog Worker instead of sending them through a public hostname, DNS, TLS, and an outbound HTTP connection.

![BLOG-3455 8.png](/images/posts/0674fca7c1f0.jpg)

On launch day, we initiated a gradual rollout, starting at just 1% of total traffic, then incrementally stepping up to 5%, 15%, and beyond as we validated system health. This phased approach allowed us to observe how the platform handled real-world production load while catching a few last-minute edge cases without impacting the vast majority of our audience. By the end of the day, we had comfortably shifted 100% of traffic over to the new platform.

![BLOG-3455 9.png](/images/posts/f7e3ea83dc4d.jpg)

## Results

### Measurable performance gains

One of our primary objectives for this migration was to deliver a faster, more reliable site to our readers, and the early data shows we accomplished exactly that.

![BLOG-3455 10.png](/images/posts/b13f4b482020.jpg)

Comparing p95 response latencies between the old architecture (green line) and the new EmDash setup (yellow line) revealed a stark difference. Where the previous platform experienced periodic latency spikes under load, the new system maintains a remarkably flat, consistent response profile. By running EmDash on Cloudflare Workers alongside our new caching layers, weâve delivered a significantly faster and more performant reading experience across the board.

![BLOG-3455 11.png](/images/posts/3623c1fdab33.jpg)

Weâve seen all these performance gains â and minimal errors â while serving up to 850 RPS.

### MCP servers

With this change, the blog also got more accessible for agents, in two distinct ways.

The first is that we released a new Model Context Protocol (MCP) server for theCloudflare Blog.

An MCP server bundles up a bunch of specific tools that your agent can then use to interact with an external resource, almost like an API for agents.

Using that MCP, you can now use the following tools with your agents:

- search_posts
- list_posts
- get_post
- list_tags

With the new, intuitive EmDash APIs and AI search endpoints exposed by our Worker, creating this new MCP took just a few hours of work.

The second is that â for our blog authors â EmDash has anMCP serverfor EmDash itself, meaning that they can browse, create, and edit content, publish and schedule posts, remove files, and more.

Though this sort of agentic tooling is becoming more standardized in the CMS industry, whatâs not standard is that itâs availablewithout any additional cost. The MCP is just another part of the platform, reflecting a growing trend ofdesigning for agents, as well as humans.

## The first test: Agents Week

At Cloudflare, we run multiple innovation âweeksâ a year, where we set ambitious goals for internal teams around specific themes. These weeks push our products forward, as well as help customers digest the changes that are constantly happening at Cloudflare.

The latest of these,Agents Week, was quite a test for the new blog. We launched 28 new posts over 9 days. And those posts got a lot of traffic, close to 3 million pageviews.

On the frontend, our new blog Worker did very well, serving up to 450 RPS without any noticeable issues. Thanks to Cloudflareâsbuilt-in DDoS protection, we also absorbed a 28,000 RPS DDoS attack on August 10th, also without any noticeable issues.

On the editing side, we continued to find some issues. Most of these involvedsmall quirksof the editing experience, though we also found some bugs specifically aroundscheduledposts. Weâve since raised these to the EmDash team and are confident that theyâll be fixed before Birthday Week.

## Give EmDash a try

We want to give a heartfelt thank you to the EmDash team, who made this migration about as smooth as possible and were incredibly receptive to our feedback. This is how Customer Zero is supposed to work, and itâs incredibly gratifying to share an inside look into that process with all of our readers as well.

If youâre in the market for a new CMS, try outEmDashtoday. Itâs pretty amazing and â with the upcominglaunch to v1â itâll be getting even better soon.

- Cloudflare
- Diogo Carneiro
- Amy Dutton

---

> 本文由AI自动翻译，原文链接：[The Cloudflare Blog â Brought to you by EmDash](https://blog.cloudflare.com/cloudflare-blog-uses-emdash/)
> 
> 翻译时间：2026-08-26 03:00
