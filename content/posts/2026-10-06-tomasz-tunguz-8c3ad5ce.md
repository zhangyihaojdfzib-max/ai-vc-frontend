---
title: How to Automate Inbound
title_original: How to Automate Inbound
date: '2026-10-06'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/how-to-automate-inbound/
author: ''
summary: '[翻译失败，原文如下]


  In short :Jeanne DeWitt Grosser, COO of Vercel, walks through the construction of
  the company''s inbound sales agent: one GTM engineer at ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-08T08:38:37.214880'
---

[翻译失败，原文如下]

In short :Jeanne DeWitt Grosser, COO of Vercel, walks through the construction of the company's inbound sales agent: one GTM engineer at 20% time, a prompt written by the top SDR, six weeks of human-in-the-loop QA, & the eventual migration from a 1,000-line prompt to 14 deterministic rules with the model reserved for judgment.

Jeanne DeWitt Grosser, COO of Vercel, joined me onOffice Hoursto walk through how she & her team actually built the agent that now runs the top of Vercel’s sales funnel.

It started with one engineer.

Vercel founded a go-to-market engineering team & handed the problem to a single engineer spending roughly 20% of his time on it. The first version of the agent was a prompt of about 125 lines, written by the best SDR on the team, encoding Vercel’s rules for qualification.

“We kicked it off in June, kept human in the loop from our top SDRs, & by August pulled the human out. So that was sort of what I think succeeded at first, was picking a problem that was reasonably deterministic & then throwing all of our unique context around how do you get the model to behave within Vercel’s four walls.”

Then the SDR managed the agent like a new rep. For the first phase, the agent did everything except send messages. It researched, qualified, & drafted.

“I almost think about this the way you would think about a human QA. If I’m its manager, I probably read 100% of that person’s first hundred emails while I’m teaching him or her the job. And that was our human in the loop phase on this. Then afterwards, I assume that person is now generally competent. And so maybe I do a simple random sample of like one out of every 100 outreaches they do.”

Six weeks of that produced a enough data & improvement to complete the effort. Rather than reviewing many posts, the effort shifted to sampling a few.

The business grew & evolved. So did the prompt - to 1000 lines.

Over the following year Vercel added product surface area & moved upmarket into enterprise, enticing a greater diversity of companies.

“The model actually won’t always follow some of the rules that are embedded in that prompt. And again, there are a bunch of things in qualification & sales that are actually pretty deterministic. It’s really a rule.”

The team divided the prompt into two parts : rules & judgment. Engineers encoded the rules & left the model the work that required judgment.

Inbound now runs on 14 rules. When a lead arrives, the system performs a Salesforce lookup to determine whether there is an open opportunity associated with the account, & if so, routes it to the account executive.

“The model shouldn’t get to decide, we just want that to occur. So now actually, our inbound is 14 rules. And we’re really only using the model for thinking exactly where a human would have thought previously.”

This is the same pattern I found in 14 production agent workflows & wrote about inIs AI Doing Less & Less?. 65% of the nodes in those workflows run as pure code, & only 14% remain fully agentic.

Because the rules are explicit, Vercel runs a second agent that watches for breaches. When the system breaks one of the 14 rules, the escalation agent determines whether the breach should have occurred & fixes it or blesses the exception.

The team changed, too. The SDR team all received promotions to outbound, skipping the customary year.

“The value of humans is talking to humans. And so the more that I can get folks out of email marketing & back into having a conversation, the more value I think we’ll get out of the BDR function.”

Jeanne provides the clearest template yet for the future of inbound, running the entire function for a unicorn for about $1,000 per year in inference & infrastructure.

Apple Podcasts|YouTube

---

> 本文由AI自动翻译，原文链接：[How to Automate Inbound](https://tomtunguz.com/how-to-automate-inbound/)
> 
> 翻译时间：2026-10-08 08:38
