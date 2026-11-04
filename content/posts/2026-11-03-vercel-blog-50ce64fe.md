---
title: How Zapier turns ideas into working software in hours with Vercel | Customers
  | Vercel
title_original: How Zapier turns ideas into working software in hours with Vercel
  | Customers | Vercel
date: '2026-11-03'
source: Vercel Blog
source_url: https://vercel.com/blog/how-zapier-turns-ideas-into-working-software-in-hours-with-vercel
author: ''
summary: '[翻译失败，原文如下]


  ## Copy link to headingZapier on Vercel


  - Interactive partner demos in under two hours withv0, replacing a process that
  could take weeks...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-04T08:50:43.601522'
---

[翻译失败，原文如下]

## Copy link to headingZapier on Vercel

- Interactive partner demos in under two hours withv0, replacing a process that could take weeks
- First versions of three internal applications, each built in one day
- A shared daily briefing for more than 60 marketers, replacing individual efforts to assemble the same information
- 3.3 million sandboxes created in one month, isolating the code execution behind Zapier’s AI workloads

Interactive partner demos in under two hours withv0, replacing a process that could take weeks

First versions of three internal applications, each built in one day

A shared daily briefing for more than 60 marketers, replacing individual efforts to assemble the same information

3.3 million sandboxes created in one month, isolating the code execution behind Zapier’s AI workloads

Before the industry had a word for agents, Zapier was building them. TodayZapieris the AI orchestration platform connecting AI to the workflows, data, and systems businesses use every day.

Zapier has been a Vercel customer since they began using Vercel for web experiences several years ago. They stayed, and expanded, because every team that needed to ship quickly found the same answer: speed, with the security guardrails already in place. As they grew, so did their adoption of Vercel as more teams found new uses for the platform. Today, Vercel supports work across engineering, partnerships, and marketing, from customer-facing AI to interactive partner demos and internal applications.

The needs vary by team, but the priority is getting useful work into people’s hands quickly. A backend engineer can create an interactive demo of an integration inside a partner’s product. In marketing, a former product marketer with no prior deployment experience can share tools containing sensitive information through a company-approved environment and keep improving them as colleagues use them.

Zapier’s teams are moving faster and doing more than they could before. When the next launch comes around, building on Vercel is a given.

## Copy link to headingFrom weeks of prototype work to a demo in under two hours

Every partnership Zapier signs extends what its customers can automate. The Powered by Zapier team is how those partnerships become product, helping SaaS and AI companies embed Zapier’s automation capabilities directly into their own tools, so users can automate without ever leaving the partner’s app. The stakes are high, because Zapier relies on this team to make its platform the entry point to all the software in the world. The problem was speed: collaborating outside the organization took forever, with every prototype requiring screenshots, design time, and frontend resources, and weeks could pass before a partner saw anything clickable.

Withv0, the team can create a fully interactive, multi-view prototype in under two hours, showing an embedded Zapier experience inside the partner’s own product.

Chu’s background is in backend development, not frontend engineering or design, butv0lets her build these experiences without coordinating a separate design and frontend effort for every partner conversation. Partners can click through the flow and share it with colleagues, using the prototype as a blueprint for implementation alongside the API documentation.

## Copy link to headingSharing sensitive internal data securely

In marketing, Joe Stych set out to make the team’s scattered knowledge easier to use. He had spent years in product marketing before becoming a agentic go-to-market engineer, but had never worked out of a Git repository or deployed an application.

At an internal hackathon, he built Marketing Hive, a shared source for positioning, messaging, personas, and competitive intelligence. Sharing his local prototype meant making sensitive information accessible to colleagues without exposing it to everyone else.

“The Hive holds our positioning, personas, and competitive intel, so I couldn't just send people a link. On Vercel it was behind our SSO from the first deploy, so I could share it without exposing it” says Joe Stych, Senior Lead, Agentic GTM at Zapier.

Zapier’s data and security teams had already endorsed Vercel. Stych deployed through the company’s approved internal tooling environment, with access gated behind Zapier’s single sign-on.

He develops in Cursor and keeps code and source material in GitLab, where changes triggerVercel builds and deployments. If an update needs to be undone, he canroll back the deployment.

The first versions of three of his internal applications took about a day each. In roughly two months, a hackathon project had grown into production software used across marketing. It was built by someone who had never deployed anything before.

## Copy link to headingInternal apps for marketing and sales

Marketing Hive holds the knowledge. Marketing OS puts it to work. It gives more than 60 marketers a daily briefing in Slack and a dashboard with what changed across marketing, one update from each team, a win worth celebrating, and progress against goals. Each marketer can start from the briefing instead of assembling the same information from separate channels.

![](/images/posts/a5837baaa471.jpg)

![](/images/posts/26ff46789a51.jpg)

“The first five minutes of your day, you need to look at the Marketing OS update,” says Dan Slagen, Zapier’s CMO.

Readers mark what they found useful, helping Stych prioritize improvements. The briefings also spark discussions in a marketing channel open to everyone at the company.

Stych is building a sales coaching application that brings together account context and industry messaging before a call. Afterward, it reviews the Gong recording to highlight what worked and suggest changes to the talk track.

For the internal applications, he checks reported numbers and the evidence behind claimed insights. Decisions about positioning remain with people, and he says additional safeguards will come before agents publish without human review.

## Copy link to headingModel access and isolated code execution

Beyond Marketing OS, a separate team at Zapier usesAI Gatewayto send requests to AI models on behalf of customers using Zapier products.

A common endpoint lets an application change or add models without maintaining a separate integration for each provider. Failover gives requests another route when a provider cannot serve them, while unified reporting lets a team see their usage across providers in once place.

## Copy link to headingWhat's next

Zapier’s relationship with Vercel began with web experiences and expanded as the company grew, with more teams finding uses for the platform as their needs changed. Today its role spans the software Zapier runs for customers and the tools its people build for one another, and every thread is still widening.

The clearest picture of where it leads is in marketing, where other teams are starting to borrow the pattern. The goal is more versions across the company, and perhaps a Revenue OS for Zapier’s customer-facing teams next, each built the way the first one was, by someone close to the problem. First comes trust. Stych still checks reported numbers and the evidence behind claimed insights, and additional safeguards will come before agents publish without human review.

Across all of it, Vercel helps Zapier put useful work into people’s hands and keep adapting it to the needs of the business.

---

> 本文由AI自动翻译，原文链接：[How Zapier turns ideas into working software in hours with Vercel | Customers | Vercel](https://vercel.com/blog/how-zapier-turns-ideas-into-working-software-in-hours-with-vercel)
> 
> 翻译时间：2026-11-04 08:50
