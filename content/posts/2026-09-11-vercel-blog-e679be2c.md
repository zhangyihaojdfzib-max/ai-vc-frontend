---
title: How Featured's users make 100K media pitches per month on Vercel | Customers
  | Vercel
title_original: How Featured's users make 100K media pitches per month on Vercel |
  Customers | Vercel
date: '2026-09-11'
source: Vercel Blog
source_url: https://vercel.com/blog/how-featureds-users-make-100k-media-pitches-per-month-on-vercel
author: ''
summary: '[翻译失败，原文如下]


  ### Copy link to headingFeatured on Vercel


  - 3 engineers supporting 3 brands and 100,000+ users on Vercel

  - Migrated 374 Sanity sites fr...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-20T07:20:57.380922'
---

[翻译失败，原文如下]

### Copy link to headingFeatured on Vercel

- 3 engineers supporting 3 brands and 100,000+ users on Vercel
- Migrated 374 Sanity sites from AWS Elastic Beanstalk to Vercel
- AI SDKandAI Gatewaypower Featured's chat bot across 17 models
- Workflow SDKreplaced custom long-running job infrastructure

3 engineers supporting 3 brands and 100,000+ users on Vercel

Migrated 374 Sanity sites from AWS Elastic Beanstalk to Vercel

AI SDKandAI Gatewaypower Featured's chat bot across 17 models

Workflow SDKreplaced custom long-running job infrastructure

Featuredis a co-pilot for public relations (PR) that subject matter experts and PR teams use to find media opportunities. Tell Featured's agents what you know, and it surfaces opportunities across journalist requests, podcasts, awards, and GEO, with no PR background required.

![](/images/posts/7b59df0876c2.jpg)

Founder Brett Farmiloe knows from experience how hard and time consuming getting press is. He spent 10 years running Markitors, a digital marketing agency with 500 small business clients. Every client, from an eyelash extension supplier to an equipment financing company, had real expertise to share, but no way to get it in front of journalists. PR, as Farmiloe puts it, "has always been about who has access to what." He founded Featured to change the question from who has access to who has knowledge.

Featured connects one of their users with a journalist or publisher every 6 seconds. Their agents deliver more than 100,000 media pitches per month, and have sent over 100 million Help A Reporter Out (HARO) emails in the past year.

Behind it all is an engineering team of just three people. With a team that lean, there's no time to manage servers or piece together custom integrations. Every hour spent on infrastructure is an hour taken away from building features what will help their customers land more media placements.

## Copy link to headingThe cost of managing infrastructure by hand

Before Vercel, Featured’s infrastructure work pulled the team away from product development. Hosting lived on AWS Elastic Beanstalk, AI features depended on custom provider integrations, and long-running, multi-step jobs ran on separate orchestration infrastructure. Each layer worked, but each one added operational overhead for a three-person team supporting multiple brands.

## Copy link to headingOne platform for compute, AI primitives, and model access

The migration to Vercel started with a forcing function: Featured needed to launch 374 Sanity sites at once, and every Elastic Beanstalk deploy had to be manually spun up, migrated, and then torn down.

When you multiply that process by almost four hundred, the math doesn't work, even when you divide it across a team of three. Vercel collapsed each site launch into to a single-click deploy.

Once the sites were live, the team evaluated Vercel for background jobs and AI tooling, eventually migrating their entire app and the agents that run in it.

### Copy link to headingCompute without the clusters

Deploys that once meant standing up a new EB instance, migrating the URL, and terminating the old one became a single click. On Vercel, all 374 sites shipped from one platform, and rollouts across all three brands now happen centrally, instead of one cluster at a time. "In hindsight, doing each one of those by hand was kind of crazy," Farmiloe admits.

### Copy link to headingAI SDK and AI Gateway: one abstraction for every model

AI SDKandAI Gatewayhandle all of Featured's model traffic through a single abstraction, so their team doesn't have to manage custom rate-limit or API integrations from multiple providers.

Featured routes across 17 models at any given time. Calling a model is one standardized function with a schema, and swapping providers is a configuration change instead of a rewrite. When a new model ships, the team can test it against Featured's use cases right away.

### Copy link to headingWorkflow SDK for long-running backend jobs

After migrating their AI stack, Featured moved long-running jobs from a separate orchestration system ontoWorkflow SDK. These are the processes that can't live in a request cycle: monitoring the media around the clock, qualifying opportunities, and combining all of those signals to deliver more than 100,000 pitches a month.

## Copy link to headingChat became the product

As users kept choosing conversation over navigation, the team made chat Featured's primary interface, and they deliver it through eve, Vercel's open-source agent framework.

eve'suseEveAgenthook made the new interface easy to implement. Instead of wiring up an agent by hand, the team got durable sessions, streaming, tool calls, and approval prompts out of the box, with model calls routed through AI Gateway so they can pick the right model per task without managing provider keys.

What would have been a months-long rebuild was a week-long replace and refactor. Now, instead of a dashboard with dozens of buttons, users ask Featured questions, and the team adapts the product to their needs, not the other way around.

## Copy link to headingWhat's next

Featured is building toward being the AI layer for public relations, the same way dedicated agent platforms have emerged for legal and finance. The goal is to make it faster and easier for anyone with expertise to share their knowledge and get featured in the media.

The team's advice to other founders building in the agentic era:

- Know that your data is your moat. For us, access to good information is what lets Featured connect people with the sources that want to publish them.
- Lean on tested abstractions like Vercel instead of reinventing security and infrastructure by hand.

Know that your data is your moat. For us, access to good information is what lets Featured connect people with the sources that want to publish them.

Lean on tested abstractions like Vercel instead of reinventing security and infrastructure by hand.

AboutFeatured:Featured is a co-pilot for public relations that helps people find media opportunities, submit pitches, and get featured in the press. Featured also owns and operatesHelp A Reporter Out (HARO)andConnectively, journalist request platforms connecting sources with publishers.

## Contributors

Eric Dodds

---

> 本文由AI自动翻译，原文链接：[How Featured's users make 100K media pitches per month on Vercel | Customers | Vercel](https://vercel.com/blog/how-featureds-users-make-100k-media-pitches-per-month-on-vercel)
> 
> 翻译时间：2026-09-20 07:20
