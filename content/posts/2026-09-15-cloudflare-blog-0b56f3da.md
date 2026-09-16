---
title: 'Have it both ways: stay discoverable in search while disallowing AI training'
title_original: 'Have it both ways: stay discoverable in search while disallowing
  AI training'
date: '2026-09-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/accountable-mixed-use-ai-crawlers/
author: ''
summary: '[翻译失败，原文如下]


  Without proper controls, website owners have long faced a difficult tradeoff: allow
  your content to be used for AI training, or risk losi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:47.447626'
---

[翻译失败，原文如下]

Without proper controls, website owners have long faced a difficult tradeoff: allow your content to be used for AI training, or risk losing discoverability in search. That tradeoff exists because some of the largest organizations on the Internet use mixed-use crawlers: a single crawler serving both search and AI training. Refuse one, and you refuse the other.

Today, Cloudflare is announcing a newDisallow AI Trainingsetting that lets you easily stay indexed for search while refusing to let that same crawler train on your content. Apple, Google, and Microsoft honor or have committed (in a specified time frame) to honor this setting.

Mixed-use crawlers were the hard part of the training question. AI Summaries are next. A site-wide yes or no is too blunt: how much of your content appears in a summary matters as much as whether it appears at all. An opt-out for AI summaries is already one of the requirements we've set for mixed-use crawler operators. By early next year, our goal is to let you control how much of your content is included â set once on Cloudflare, rather than with each operator separately.

## Why asking isnât enough

Most site owners want to be found: by humans, agents, and (good) bots. But a significant portion of the open Internet is funded by advertising, subscriptions, or direct relationships with visitors, and those models only pay when someone actually arrives.

Almost every site owner considers Search beneficial: less than 1% of Cloudflare sites choose to block Search bots. Training, however, is a different story: 17% of sites choose to enable some mechanism to block training. This is exactly why we decided site owners needed more granular controls, rather than a one-size-fits-all âBlock AI.â

A robots.txt directive alone cannot solve this problem. Anyone can publish one, but it cannot identify who is crawling, determine why they are crawling, or stop a crawler that ignores it.

A network can solve it, however: we publish the preference, identify who is crawling, classify why they are crawling, and block the ones that ignore it â then report what each operator actually does onRadar.

But blocking removes a crawler. It doesn't change how crawlers behave. The better outcome is operators that don't make you choose at all. So since July, we've been talking to them directly. The response has been encouraging: almost all agreed that site owners should have control and transparency into how their content is used, and reassurance that their choices will be respected. To help site owners understand that, we created a designation: Accountable.

The Accountable designation recognizes both capabilities available today and concrete commitments to deliver them. To qualify, a bot operator must meet or commit to meeting the following requirements:

1. A mechanism for site owners to opt out of AI training, through robots.txt or a similar standard.
2. A mechanism for site owners to opt out of AI summaries set with the operator directly, and next year through Cloudflare (see section below for more detail).
3. URL-level visibility into which pages were made available for training, along with metrics showing how content appeared in search.
4. Assurance that opting out of AI training will not affect traditional search results.

Apple, Google, and Microsoft all demonstrate that they meet the qualifications to be Accountable. Each combines capabilities available today with time-bound commitments for those still in development. The details of each of these companiesâ crawlers are shared below.

## New security setting options

Cloudflare classifies bots by behavior, and a single bot can exhibit more than one behavior. Three behaviors are available as controls:

- Search- crawling to build a search index.
- Training- crawling to train or fine-tune a model.
- Agent- user-directed agents visiting a page on behalf of a human, such as chat fetch bots and browser-use agents.

A mixed-use crawler is a single crawler doing both Search and Training. Without controls, that combination creates the tradeoff described above: site owners cannot refuse one use without refusing the other.

To avoid blocking Accountable mixed-use crawlers â the ones that don't force that tradeoff on website owners â we are introducing a new setting: Disallow AI Training. Disallow AI Training is named for the Disallow: directive it publishes in your robots.txt.

### âBlockâ setting now means something different

Block and âBlock on pages with adsâ previously did not apply to mixed-use crawlers because blocking them could also affect search discoverability. Now that we have the new Disallow AI Training setting, Block and âBlock on pages with adsâ apply toalltraining crawlers, including mixed-use crawlers.

Training, Search, and Agent controls are applied at the domain level. With the addition of Disallow AI Training, the available settings are:

1. Allow: All crawlers are allowed, unless blocked by another setting or a WAF rule.
2. Disallow AI Training: Bot Preference Sync publishes the applicable no-training preference in robots.txt. Accountable mixed-use crawlers remain allowed for search. Every other training crawler is blocked, including the training-only crawlers run by Amazon, Anthropic, Meta, and OpenAI â blocking those does not affect search. Disallow AI Training is only available as a setting for Training, not Search or Agent.
3. Block on pages with ads: Crawlers, including mixed-use crawlers, are blocked only on pages detected to be serving an ad.
4. Block: All crawlers, including mixed-use crawlers, are blocked.

Disallow AI Training works by publishing a preference in robots.txt. An ads-only preference cannot be expressed that way: Cloudflare can detect which pages serve ads, but that list is too large and changes too frequently to enumerate in robots.txt. That's why there's no Disallow AI Training on pages with ads.

Agents do not create the same search-discoverability tradeoff as mixed-use crawlers, and the Internet does not yet have a well-established directive for expressing Disallow preferences to agents. For now, weâre not including a Disallow setting for Agents. As standards such asai-prefsmature, we will revisit this approach.

## What changes on September 15?

We are making the following changes to Bot Management and AI Crawl Control:

1. Block and Block on pages with ads now apply to mixed-use crawlers, including Applebot, Bingbot, and Googlebot, so either setting impacts search as well as training. To stop training andkeepsearch, use Disallow AI Training.
2. âBlock AI Botsâ will be deprecated in favor of the more granular Search, Training, and Agent controls.
3. Managed Robots.txt will be deprecated in favor of Bot Preference Sync. Customers who enabled Managed Robots.txt will migrate to the new system.
4. Disallow AI Training will become part of the recommended configuration for certain new domains.
5. Existing customers will have their preferences migrated to the new controls as described below.

### What you need to do

Nothing, in almost every case. Your current settings carry over on their own.

If you want mixed-use crawlers gone entirely, you now have to say so. Select Block. It will stop Applebot, Bingbot, and Googlebot from reaching your site â search included.

#### Existing domains that never used the Search/Training/Agent controls

Site owners that never configured the more granular controls will be migrated to the new settings based on their legacy Block AI Bots setting:

#### Existing domains that previously configured the Search/Training/Agent controls

For domains that previously configured the granular controls, we will preserve the practical effect of their selections under the new definitions. Previous Training selections of Block or Block on pages with ads will migrate to Disallow AI Training.

### Recommendations for new domains

[翻译失败，原文如下]

Beginning September 15, customers onboarding a new domain will be offered one of two preset configurations, depending on whether the site earns money from advertising. Ad revenue depends on a human actually seeing the page. Training replaces that visit with an answer; agents fetch the page with nobody there to see the ads. So the presets for ad-supported sites are more restrictive. You can change any of these settings during onboarding, or at any time afterward.

Recommended settings for new domains

![BLOG-3499 2.png](/images/posts/773f1ef855e3.jpg)

## What does this mean for specific mixed-use crawlers?

Applebot, Bingbot, and Googlebot are Accountable. Apple, Google, and Microsoft are committed to the same principles of publisher choice and transparency. Under Disallow AI Training they can keep crawling your site for search. Selecting Block stops them entirely.

We also categorize the relevant crawlers from Amazon, Anthropic, Meta, and OpenAI as Accountable. These organizations separate their Search and Training crawlers, so Cloudflare can block the Training crawler without affecting search.

### Applebot

Applebot allows site owners to opt out of training by adding a Disallow rule to robots.txt for âApplebot-Extendedâ. Site owners can also currently express preferences for AI Summaries via their nosnippetdirectivein the page HTML. Content can also be labeled aspaywalled contentto exclude it from generative output. Applebot does not yet provide a tool for URL-level inspection. However, we have met with their team, and they have shared details of their in-progress solution for next year. Apple has also stated that disallowing trainingdoes not impact search ranking.

### Googlebot

Googlebot allows site owners to opt out of training by adding a Disallow rule to robots.txt for âGoogle-Extendedâ, and they provide a toggle inside their webmaster portal to exclude a siteâs content from generative search results. Googlebot also provides site owners with metrics and reporting regarding search results and AI summary results. Google shared information about their existing and recently launched controls, as well as information about what they're already working on, including additional URL-level transparency tools for site-owners related to Google-Extended, which they expect to launch in the weeks to come. Google has also stated that disallowing Google-Extendeddoes not impact search ranking.

### Bingbot

Bingbot provides granular controls and transparency in theirWebmaster Tools. Site owners can currently express AI training preferences through BingâsNOARCHIVEmeta tag. Microsoft is extending these capabilities and currently building the mechanism to also respect a âno trainingâ preference in robots.txt at the domain/site level, targeted for early 2027. For Cloudflare Customers who wish to opt out of training in Bing today, in addition to using theNOARCHIVEtag, site owners can use theBlock URLs or Content Removal tool. Microsoft has also stated that usingNOARCHIVEwill not impact search ranking.

Until that support launches, selecting Disallow AI Training will not automatically convey a no-training preference to Bing through robots.txt. This is the same practical behavior as the previous Training Block setting, which did not apply to mixed-use crawlers such as Bingbot.

### Continuing progress

We will continue to reach out and engage with all operators of AI crawlers as these capabilities evolve. CloudflareRadarpublicly tracks the controls, transparency, and reporting provided by Accountable crawler operators.Â

Making the Internet better requires both sides to have agency: crawlers need access to the open web, and the people who create that web need meaningful control over how their work is used. Todayâs announcement represents concrete progress toward that balance.

Progress requires infrastructure providers, content creators, technology companies, and standards bodies such as the Internet Engineering Task Force (IETF) working together to translate these principles into open, interoperable standards.

## Whatâs next: AI Summaries

Training and AI Summaries raise different questions for site owners. Training concerns whether content can be used to build AI models. Summaries affect how people discover, evaluate, and ultimately visit a business. Both matter, but they affect businesses in different ways.

Controls to opt out of AI summaries are the first step. The operators identified as Accountable either provide or are completing work to provide that capability, establishing an important baseline: site owners can say no.

But a site-wide choice between allowing and prohibiting summaries is still a blunt instrument. The right decision depends on the site, the content, and the business outcome. For publishers, training raises foundational questions about control, compensation, and the sustainability of original content. Summaries create a separate and often more immediate distribution question: does someone visit the publisherâs site, or consume the answer within a search or AI experience? For many other businesses, AI summaries increasingly sit between a potential customer and a website. They may answer a question, compare alternatives, recommend a product, or help someone decide whether to visit at all.

The data illustrates mixed impact.More than halfof consumers read summaries in Search, and those consumers areover 40% more likelytoend their searchafter reading one. This can reduce the number of visits a website receives. But consumers referred by AI Search convert at betweenthree timesandover five timesthe rate of those referred by traditional search. AI may produce fewer visits while sending customers with much greater intent.

That is not inherently good or bad. A publisher funded by advertising may optimize for audience volume. A retailer may prefer fewer visitors who are more likely to purchase. Cloudflareâs role is not to choose for them, but to provide the visibility and control needed to make an informed decision.

Summary opt-outs are a strong start, but they are not the end state. Our next focus is helping site owners understand how summaries affect their businesses and giving them more control over how much of their content can be used. Open standards such asai-prefswill be an important part of making that possible.

If you would like to have a voice in this conversation, or provide feedback, please reach out tocrawlercontrols@cloudflare.com.

These new controls are available to all customers, on all plans, and can be configured at the domain (zone)Security Settings. Not on Cloudflare yet?Start for freeto set the traffic controls that you want today.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Have it both ways: stay discoverable in search while disallowing AI training](https://blog.cloudflare.com/accountable-mixed-use-ai-crawlers/)
> 
> 翻译时间：2026-09-16 07:28
