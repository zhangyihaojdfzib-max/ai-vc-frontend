---
title: 'Say it once: introducing Bot Preference Sync'
title_original: 'Say it once: introducing Bot Preference Sync'
date: '2026-08-21'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/bot-preference-sync/
author: ''
summary: "[翻译失败，原文如下]\n\nWeâ\x80\x99re constantly building for the different goals\
  \ of our customers. Some customers want to optimize for discovery, while others\
  \ want to..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:00:24.882579'
---

[翻译失败，原文如下]

Weâre constantly building for the different goals of our customers. Some customers want to optimize for discovery, while others want to protect their content with the strictest security policy. Among these differing policies, there are multiple ways to mitigate bot traffic. Some mechanisms simply state your preference, assuming best intent from crawlers, and other approaches actually lock down content by outright blocking with a Bot Management solution.

We recognize that it's cumbersome to maintain multiple layers of protection on your website. For example, there are cases in which your robots.txt states that a crawler is Disallowed from accessing your website, while your enforcement rules actually donât block that crawler. When your stated preferences and your enforced rules disagree, some crawlers treat it as a basis to disregard your preferences or try to bypass your enforced rules.

A couple of years ago, Cloudflare announced an easier way to disallow AI training on your website by tackling two of these layers: a managed value of robots.txt that told a fixed list of major Training crawlers not to train on your content, along with edge-enforced blocks to Training crawlers. On July 1, 2026, we launched easier options to manage different kinds of AI traffic use cases. You can say what you want to do about Search, Agent, and Training traffic on your website.

We're announcingBot Preference Sync, available toallcustomers from the Free tier to Enterprise. Bot Preference Sync reflects what you've set in your AI bot configuration by updating corresponding preferences to your robots.txt, and it can be turned on or off at any time. No more static file for one use case: we'll help youtailor your robots.txt to reflect what youâve already configured for different AI bot categories.

## New questions facing the Internet

For years, the most pressing question in this space was: "Is my content being used to train AI models without my permission?" It's an important question, and it isn't going away. Alongside this, the questions we increasingly hear are about discoverability and engagement. How do I show up when someone asks an AI assistant something my site can answer? How much of my traffic is coming from AI crawlers versus real people? What content is actually driving referrals, and what is it worth?

The answers differ by business model. Discoverability and engagement are key, top-of-mind issues for any businesses trying to thrive on the modern web, but the funnels for these are different: an e-commerce store may want everything crawled and trained on, so its products surface when a shopper asks a chatbot for "the best sofa for a small apartment." A publisher that monetizes pages with ads may want the opposite: stay in the search index that sends readers to the page, but keep its articles out of model training and, crucially, be able to verify that its content really wasn't used without permission.

There's no single right answer, which is exactly the point. Your controls should reflect your strategy, which is why we've been building tools to give you visibility and choice at every layer. Bot Preference Sync ties these together, so the preference yousetis the preference youpublish.

## The call for Transparency

On July 1, 2026, we made the case that mixed-use crawlers, or âbots that blend search, agent use, and training behind a single user agent,â put site owners at a disadvantage precisely because they make it hard to separate what you want from what you don't. That's still true, and our position on Transparency for site owners hasn't changed.

But thereâs more than one way to approach Transparency. We want to reward the operators who are clear about their identity and how they are using the data they crawl. For purposes of botVerification, the owners ofbots that perform both Search and Training will need to provide additional informationin order to not be blocked when âDisallow Trainingâ is set. Those requirements are:

- The bot must respect, via any mechanism, a âno trainingâ preference in robots.txt
- They give site owners a way to opt out of AI summaries.
- They provide URL-level visibility into which pages were made available for training, as well metrics on search results, so you can see how your content was used for search and for training.
- They can show publicly that Disallowing Training does not hurt your traditional search results.

Bots of leading AI models and service providers that meet these criteria are tracked publicly in theAI bot transparencysection in Cloudflare Radar, which includes examples in which best practices are honored, as well as when they are not. Crawlers that don't provide Transparency willnotget the benefit of the doubt â they're still blocked when you disallow training. In other words, this is a way of making Transparency the price of admission.Â

## Introducing Bot Preference Sync

Bot Preference Sync is a new feature that keeps your robots.txt reflecting the AI bot preferences you've already set for Search, Agent, and Training on the Cloudflare zone-level dashboard. If a site owner already has a robots.txt file, the contents added by Bot Preference Sync will beprepended to theexisting material, so any existing Disallow directives are maintained.

Instead of a site owner maintaining a separate static file, Cloudflare generates or updates your robots.txt based on your configuration, so what you say to the world and what you enforce at the edge are kept in sync.

For Search and Agent, the three options we announced on July 1 remain: Allow, Block on pages that serve ads, or Block everywhere. ForTraining, weâre refining the option to stop your content being used for training models with theDisallowoption:

Disallow: a "no training" preference is written to your robots.txt, so that cooperating mixed-use crawlers who take the extra Transparency step can still access your content for search indexing, since theyâre allowing site owners to directly verify how their data is used. Cooperating crawlers honor the preferences in robots.txt, and your Search visibility for cooperating crawlers is unaffected.

Letâs take the example below, in which someone has configured their AI bot policy to say âAllow Search, Allow Agents, Disallow Training.â

![BLOG-3489 2.png](/images/posts/ca82bd2137f4.jpg)

Since this example site has Bot Preference Sync on, their robots.txt would prepend something like the following (which has been shortened and anonymized for the sake of the example):

```
# BEGIN Cloudflare Bot Preference Sync

User-agent: TrainingBot1
User-agent: TrainingBot2
User-agent: TrainingBot3
User-agent: MixedUseBot-Extended
Disallow: /

...

# END Cloudflare Bot Preference Sync
```

Weâll use bots that we track inBotBaseto periodically update the list of bots that is added to robots.txt when you choose to Block or Disallow a given category. The Verified bots that are classified as Search, Agent, and Training can be viewed at any time in ourpublic bots directory.

For all new customers, Bot Preference Sync will beonby default, to make it easier to manage blocks and preferences that reflect the same policy. For existing customers who are using the legacy managed robots.txt feature, we'll prompt you to review and confirm your preferences to transition to the new Bot Preference Sync upon its upcoming launch.Â

Some customers may want or need to be more hands-on in stating their preferences, for example, if they have a special arrangement with a given company to which they want to grant an exception. Because Bot Preference Sync is designed to tackle policy decisions madecategory-widerather than case-by-case, it will not directly read from individual custom rules with more complex logic. Customers with a more fine-tuned security policy always have the option to turnoffthe sync that sets group policies, and tailor their file to match their custom policy.

[翻译失败，原文如下]

Weâre also making a change that allows publishers or ad-supported sites to have a different default from other site owners. Weâve created a default to make it easier for publishing sites that rely on ads and expect them to be reserved for human visitors. At the time of onboarding, such customers can select the option, âI monetize from pages with ads on this domain", which will set Training to Disallow as the default. (Customers have the choice to change this setting at any time.) This way, you stay in search while keeping your content out of model training.

For the non-publisher case, new customers willnothave any blocks or disallows added by default when they onboard a domain: the choice is up to the customer. You can choose if you want to block Search or Agent or Training at any point, but the starting point willnotadd any blocks on your behalf.

## What's next?

Bot Preference Sync will be available toallcustomers, on every plan, in the coming week. Keep an eye on our changelog for availability, and watch your dashboard (and inbox) for the prompt to confirm your preferences!

This is one step in a longer effort. We'll keep working with the large bot operators to make sure we're not compromising on familiar challenges (like training without consent) nor emerging questions (like discoverability and engagement). Beneath it all is our effort to promote greater Transparency and control for site owners.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Say it once: introducing Bot Preference Sync](https://blog.cloudflare.com/bot-preference-sync/)
> 
> 翻译时间：2026-08-26 03:00
