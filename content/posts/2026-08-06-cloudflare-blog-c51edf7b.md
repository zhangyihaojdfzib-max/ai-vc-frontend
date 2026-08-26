---
title: 'From ranking to recommended: get your site ready to thrive in the age of AI
  agents'
title_original: 'From ranking to recommended: get your site ready to thrive in the
  age of AI agents'
date: '2026-08-06'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/aeo/
author: ''
summary: '[翻译失败，原文如下]


  Your next customer may not find you through a search engine. Instead, they''ll ask
  an AI assistant: "how do I do X?"; "which option is bes...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:00:27.771515'
---

[翻译失败，原文如下]

Your next customer may not find you through a search engine. Instead, they'll ask an AI assistant: "how do I do X?"; "which option is best for someone like me?"; "just handle it for me" and an agent will find the answer, weigh the options, and act on their behalf. Increasingly, the moment that determines whether a customer chooses you happens inside a model's response â before a human ever sees your homepage.

This agentic audience is already here: by our count, fewer than half of all HTML page requestsnow come from a human. Not all of those machines are agents acting for a person, but that share is growing fast, and answer engines, shopping assistants, and research tools will shape which businesses are found and recommended. Discoverability used to mean ranking on a results page. Now it means being found, read, and confidently recommended by the agents that guide your customers.

The old metrics, human clicks and page views, no longer paint the full picture. We spent time talking to site owners who were staring at access logs full of AI bots, completely blind to whether those bots were capable of using their site or recommending their products and services to their users. We heard two main questions:

- Can agents actually use my site?
- Am I getting recommended?

To help site owners answer these questions, we have integrated ourprevious work on Agent Readinessinto the Cloudflare dashboard, and added our new Answer Engine Optimization (AEO) tool as well. These tools treat agents as a core user base for your site, showing you how an agent will see it, and how often you get recommended.

The opportunity is big, and the bar is low, because most sites aren't built for this user yet. Just as early SEO rewarded the sites built for search engines, the sites built for agents will be rewarded now. The ones that are easy to find, read, and trust are the ones agents will recommend.

## Diagnostics: is your site ready for agents?

Diagnostics is the technical checkup within Agent Readiness. It scans your site the way an agent reads it: it works out whether it's allowed in and whether it can discover your content, fetches a clean machine-readable copy, and finds the interfaces it can call.Â

While a person just loads your homepage, an agent leans on your robots.txt, your sitemap, your response headers, a Markdown version of your content, and published metadata for authentication and tools.

![BLOG-3440 2.png](/images/posts/a6be677817bc.jpg)

Diagnostics runs those checks against a hostname and rolls the results into a single agent-readiness view, from "Not Ready" to fully agent-native. Every check comes back as pass, fail, or neutral, with a note on why it matters, and an evidence trail showing the exact request and response we saw.

The checks are grouped by effort, so you know where to start:

- Quick wins: the high-impact basics most sites are missing, including a crawler-readable robots.txt, an XML sitemap, AI-crawler rules, and serving clean Markdown to agents
- Technical groundwork: the next layer, including Content Signals that state how your content may be used, an API catalog, link headers, and agent login instructions
- Advanced integration: the agent-native features, including OAuth discovery, MCP (Model Context Protocol) and A2A (Agent2Agent) agent cards, a skills index, Web Bot Auth, and WebMCP
- Commerce: the emerging agent-payment standards includingx402(an extension of the classic HTTP 402 Payment Required status code), ACP (Agent Commerce Protocol), Universal Commerce Protocol (UCP), and AP2 (Agent Payments Protocol). This is informational for now, and not counted in your score.

![BLOG-3440 3.png](/images/posts/4eaad4623d8e.jpg)

Every suggested improvement comes with a next step. When thereâs a Cloudflare feature that can help, there's a "Set up in Cloudflare" link straight to the setting, such as switching on Markdown for Agents or managed robots.txt. For everything else, thereâs a "Copy Agent Prompt" button that proposes what your coding agent needs to build. Make the change, re-scan, and watch the checkmark turn green.

## AEO: are AI assistants recommending you?

Diagnostics tells you whether agents can read your site. The AEO tab tells you what happens next: when a customer asks an AI assistant a question in your category, does it recommend you or a competitor? You can't look this up like a search ranking. There's no impression count and no missed-click report, so when a competitor gets named instead of you, the sale is gone and nothing tells you it happened.

![BLOG-3440 4.png](/images/posts/86e1c884af77.jpg)

We infer your industry (e.g. health and fitness) and category (e.g. sports apparel) from your site, and we probe the leading assistants (today, Anthropic's Claude and OpenAI's GPT) with likely customer prompts to see how they respond. We structure these prompts to mimic real-world discovery, asking for recommendations, product comparisons, and general advice within your category. By observing how models answer these realistic queries, you get metrics such as:

- Citation Rate:the share of answers in your category that cite your site as a source
- Prominence:when you are cited, how much of the answer is actually yours and how early it lands
- Mention Rate:how often assistants name your brand in their answer â for example, how often "Cloudflare" shows up in the response, whether or notcloudflare.comis cited as a source. Read alongside your Citation Rate, it separates awareness from attribution: assistants naming you far more than they cite you means you're on their radar but not yet earning the citation â a specific, targetable gap.
- Share of Voice:your slice of citations against those for your competitors, so you can see who is winning the prompts you're losing

To evaluate how an AI model perceives your market presence, we build a benchmark across each industry and category before scoring a specific site. We query AI assistants with likely prompts in that category â without specifying your brand â and record which sites are cited, where they appear, and how prominently they feature.

Rather than re-querying models every time a site owner runs a scan, we run this panel once per category and reuse the baseline across all accounts in that domain. Pre-computing this dataset provides three main benefits:

- Zero latency:Results load instantly from a snapshot rather than waiting for live model queries.
- Lower compute overhead:Aggregating queries at the category level avoids redundant AI calls across thousands of scans.
- Industry Fit scoring:Reusing the panel corpus lets us map which brands consistently appear together, allowing us to derive an Industry Fit score that measures whether an AI assistant views your site alongside your actual competitors.

AI assistants rarely answer the same question the exact same way twice. To account for this variance, we useCloudflare AI Gatewayto prompt each assistant multiple times across different models. We then read the responses a customer would see â the answer text alongside the sources each assistant cited â and extract multiple signals from it.Â

We evaluate not just whether your site was mentioned, but whether you were cited as a source, how early your citations appear in the answer, and how much of the final answer's substance is attributed to you. Where genuine judgment is required, Workers AI does the heavy lifting, running natively on our own infrastructure to read each reply and score how your citations and mentions appear. We also use exact text analysis rather than a model grading its own output. Together, this folds dozens of one-off replies into actionable metrics. By abstracting the multimodel query and evaluation pipeline, the tool provides metrics without requiring you to build your own evaluation framework.

![BLOG-3440 5.png](/images/posts/2cc1e0675cd4.jpg)

[翻译失败，原文如下]

Alongside the answers, an AI Operator Activity shows the real crawl and referral traffic on your site, per operator (OpenAI, Google, and so on): who reads your content, who sends visitors back, and the errors they hit on the way (403 blocked, 404 dead link). The pattern worth acting on is the operator that crawls thousands of your pages but refers no one, using your work without sending customers back.

Because these numbers are specific to your site, you can experiment, re-run the scan, and measure the impact on the exact questions that bring you business.

![BLOG-3440 6.png](/images/posts/647c3803bca0.jpg)

## Meet your other audience

Until now, sizing up agents meant guesswork: grepping your logs to infer who visited, or feeding a chatbot a prompt and eyeballing whether it mentioned you. But with Agent Readiness and AEO, you can get the data you need to act. And because the requests actually pass through Cloudflare, these tools measure rather than estimate where possible, and will improve over time.Â

Helping you see who's reaching your site and decide how to engage on your own terms is what we've always done. Agents are just the newest audience, and the businesses that make themselves easy for agents to find, understand, and trust are the ones that get recommended. Agent Readiness is where you find out whether you're one of them, and what to do if you're not yet.

Ready to find out if AI agents are sending customers your way? Head over to the Overview tab in your dashboard to get your site Agent Ready and request early access to AEO Visibility.

Building on the open, agent-ready web? Open theAgent Readinesstab in yourCloudflare dashboardand tell us what you're building on theCloudflare Developer Discord.

## Related tags

Follow on Social Media

- Cloudflare
- Jack Galilee

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[From ranking to recommended: get your site ready to thrive in the age of AI agents](https://blog.cloudflare.com/aeo/)
> 
> 翻译时间：2026-08-26 03:00
