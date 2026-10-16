---
title: 'Cloudflare and OpenAI: making AI discovery better for everyone'
title_original: 'Cloudflare and OpenAI: making AI discovery better for everyone'
date: '2026-10-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/cloudflare-openai-discovery-agentic-web/
author: ''
summary: '[翻译失败，原文如下]


  Optimizing your site for AI is of little use if AI can''t find it. The answer to
  someone''s question may already be on your website: the in...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:40:52.730048'
---

[翻译失败，原文如下]

Optimizing your site for AI is of little use if AI can't find it. The answer to someone's question may already be on your website: the installation guide you spent a week writing, or a first-hand account of using a product, with the details that make the difference for whether they buy it. As more people turn to AI for help, you want those systems to find your work, represent it accurately, and send interested people your way. You also want control over how they access your site.

Cloudflare and OpenAIlaunched a research pilotÂ in July 2026 with those interests in mind. We wanted to find out whether signals from Cloudflareâs network could help ChatGPT users discover new content more efficiently.

Today, weâre sharing early results. So far, the answer is a resounding yes: the pilot has brought previously unknown pages into OpenAIâs search index, giving ChatGPT more sources to draw on to help people find relevant, timely information. Along the way, weâve learned more about what makes a page worth discovering and how AI systems use the web.

## Finding more of the web

The web is full of specifics. Someone fixing a washing machine needs the manual for their exact model. Someone applying for a passport needs the current requirements and fees. Someone choosing a local restaurant needs its latest menu and opening hours. Finding the right page can be the difference between a wrong answer and one that actually helps. These pages can be valuable even if few other sites link to them.

In the previous version of the web, discoverability was getting to the top of a search result page. It was then up to the human who visited your page to determine the value of the information, book that table, apply for that passport. As people increasingly rely on AI to find information and complete tasks, discoverability matters in new ways. AI systems need to find the right sources, understand what's useful, and connect people with relevant information â whether that's through an answer, a citation, or a visit to the website itself.

Cloudflare's network provides signals that can help OpenAIâs search crawler discover more useful pages across the web to surface to ChatGPT users. OpenAI then independently evaluates and ranks how those pages appear based on how relevant and helpful they are. Together, this creates a feedback loop that can improve both discovery and the quality of information people find.

This joint pilot, which used a participating cohort of ~1% of Cloudflareâs total network, has enabled OpenAI to discover and index hundreds of millions of new web pages, helping people discover more useful content and get more questions answered through ChatGPT. By linking back to relevant sources, ChatGPT Search also gives people a way to explore the original content and discover the websites and publishers behind it.

WithGPT-6 and Intelligent UI, OpenAI is also making ChatGPT an even better place to shop, learn, and find answers, with more visual, interactive experiences tailored to what people need. This work complements these advances by helping ChatGPT discover more useful, up-to-date information from across the web.

## From discovery to useful answers

Finding a URL is only the start. We need to know whether it leads to a page someone can access, whether that page offers anything distinct, and what it might help someone do.

Weâve learned, for example, how easily automated traffic can make a nonexistent page look interesting. Bots repeatedly ask for files that arenât there. Some sites redirect almost any address to their homepage. Other addresses lead to copies of the same content. Recognizing these patterns gives us a way to cut wasted work before a crawler fetches the page, and improve efficiency in a way that benefits site owners.

We're also testing signals that identify and flag potentially harmful pages, adding another layer of information to support safer, more reliable discovery. A legitimate site can have a single compromised page, such as a fake login form planted by an attacker. Flagging that one page, rather than the whole domain, keeps people safe without penalizing the site owner. Early results suggest these signals can help identify pages that should be kept out of an index.

## Making discovery easier

As more people use AI to discover information, website owners have new opportunities to reach interested audiences. For those who choose to make their content available to AI systems, these improvements make discovery easier and more efficient.

Keeping up by fetching every page more often would be expensive for everyone. For a website owner, a crawler that repeatedly downloads an unchanged page adds load without bringing any benefit.

The signals above are how we avoid that. Filtering keeps crawlers away from pages that don't exist or that redirect elsewhere. Change signals tell them when a page is worth another visit, and when it isn't.

There's a balance to get right. Finding new pages can initially increase crawling as those pages are evaluated and indexed. The goal is to keep discovering and stay current while reducing the work that takes. For Cloudflare customers, that means less unnecessary load. For OpenAI, it means more of its search resources are spent on information that helps people.

## Making it worthwhile to participate

The next phase will build on what weâve learned: improve the selection of pages, test faster and more reliable change signals, and measure what happens after content is discovered.

Weâre continuing to work with OpenAI to understand how better site discovery can translate into real business outcomes, and weâll keep sharing what we learn along the way.

Domain ownersâ choices matter throughout. A signal about a page doesnât grant permission to access it. This research uses metadata about the web for search and discovery, rather than sharing page content for model training.

You can useCloudflareâs AI Crawl ControlÂ to understand and manage how AI systems access your website.

![](/images/posts/8ea74e881a24.jpg)

## Related tags

Follow on Social Media

- Cloudflare
- Jack Galilee
- Henry Aspegren (OpenAI)
- James Balfour (OpenAI)

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Cloudflare and OpenAI: making AI discovery better for everyone](https://blog.cloudflare.com/cloudflare-openai-discovery-agentic-web/)
> 
> 翻译时间：2026-10-16 06:40
