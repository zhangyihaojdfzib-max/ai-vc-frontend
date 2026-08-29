---
title: 'BotBase for Operators: A clearer path to joining Cloudflare''s directory of
  bots and agents'
title_original: 'BotBase for Operators: A clearer path to joining Cloudflare''s directory
  of bots and agents'
date: '2026-08-28'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/botbase-for-operators/
author: ''
summary: '[翻译失败，原文如下]


  Last month, on our second Content Independence Day, we announceda couple of featuresdesigned
  to give website owners more visibility and c...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-29T08:49:19.788280'
---

[翻译失败，原文如下]

Last month, on our second Content Independence Day, we announceda couple of featuresdesigned to give website owners more visibility and control over automated traffic:BotBaseadded a searchable directory of known bots to the Cloudflare dashboard, whileBusiness Insightshelped owners understand how crawlers interact with their content. We know that the ecosystem of bots is vast, making it all the more important for site owners to be able to manage bot traffic sustainably.

But this ecosystem goes both ways. While website owners need to decide which automated traffic they allow, bot operators need a clear way to identify themselves, explain what their bots do, and keep that information current. BotBase works best when both sides can participate.

When we launched BotBase, we said we would build tools to bring bot operators into this ecosystem. Until now, their experience largely ended at submission. After pressing submit, an operator had no easy way to check the submission's status, understand why it was rejected, or update an existing entry. Today, we start to change that with the launch of BotBase for Operators, tackling what bot operators need first: transparency.

## A new home for bot submissions

Imagine youâre a bot operator looking to submit your bot toBotBase. Where on thedashboardwould you look for such a submission form? Previously, the form lived underManage Account â Configurations, which tied the bot clearly to your account, but didnât acknowledge its connection to the bots ecosystem.

Starting today, the bot submission experience has a home next to the rest of your bot and trust tools:Protect & Connect â Application Security â BotBase(new!). All customers can access this today directly from theCloudflare dashboard.

Here, weâve split BotBase for Operators by use case:

- Bots directoryâ browse, search, and filter the bots Cloudflare already tracks (the same catalogue you can explore onCloudflare Radar).
- Submission formâ submit a new bot.
- Submission historyâ track everything you have submitted.

![BLOG-3473 2.png](/images/posts/0312f3258249.jpg)

Finding BotBase solves the "where" problem. The "what happens next" problem is the one that weâve heard is deeply important to bot operators, so weâll cover that in the rest of this post.

## See where your submission stands

We spoke to many bot operators, and the resounding feedback was this:submitting a bot feels like a black box. You fill in the form, press submit, and wait, with no way to tell whether anything happened next.

Now, theSubmission historytab shows every bot submitted from your account, each with a clear status:

- Waiting for reviewâ we have received your submission and it is in our queue.
- Acceptedâ we have reviewed it and your bot is now tracked in the directory.
- Rejectedâ something in the submission needs to change. We tell you why, with steps you can act on, so you can fix it and resubmit.

Open any submission to see its full details. If it was rejected, you will see the reason why. If it was accepted but we adjusted how your bot is classified, you will see what we changed.

![BLOG-3473 3.png](/images/posts/ace74c21e505.jpg)

Previously, operators would need to email support just to ask whether their bot got reviewed or to check on their submission's progress. That's exactly the gap weâre closing with this new tab.

Today, the submission form is no longer a black box. Every operator can now view the record of every bot they've submitted starting from todayâs launch, with a status you can check anytime. We also provide a way to filter âMy bots,â from the Bots directory screen, so you can see all bots that have been submitted under the account with which youâre currently logged in.

## Keep your bot's information up to date

A bot's identification details can change over time. You might redesign your website and end up hosting your IP list at a new endpoint. Or you might move from an IP allowlist to signing your traffic withWeb Bot Auth, and need your entry to match. Before today, the only way to reflect either change was to fill out the whole form again and submit a brand-new entry. Now, you can edit a submission you have already made.

You can also cancel a submission that is still waiting for review.

We encourage every operator to keep their bot's information current. Accurate details are a key component of how a bot earns and keepsVerifiedstatus, which increasingly determines whether sites across Cloudflare's network can easily allow it based on its behavior. Of course, it is ultimately up to the individual site owner to decide what traffic is allowed and what is not.Â

## A submission form built on an updated, pragmatic taxonomy

Picture a bot. Maybe it only crawls pages to build a search index. Maybe it also acts on a user's behalf, or pulls in data for something else entirely. How it uses what it reads matters just as much as what it does.Â

The new intake form asks you to describe your bot the way it actually behaves. It follows the samebehavior and content use model we introduced on July 1, so instead of squeezing your bot into a single label, you now tell us three things.

First, what your bot does. Maybe it only does one thing, like indexing pages for search. Maybe it's an agent acting on a user's behalf, or it collects data, trains models, or supports SEO tools. You can select every behavior that applies, not just the closest match.

Second, how it uses what it reads. A crawler that skims a page for a search snippet is not the same as one that stores that page to train a model. You tell us the level of content use your bot needs, using the sameContent Signalsmodel website owners already use to set their own rules. For example, a site's robots.txt might read Content-Signal: search=yes, ai-train=no, use=reference, telling every crawler it's fine to index the page for search and keep a reference, but not to train a model on it. Your bot's content-use declaration is what gets checked against exactly that kind of preference.

Third, who's actually running it. If you operate your bot yourself, straight from your own infrastructure, like a search engine crawling the web to build its own index, that's direct. If you run a platform other companies build on, carrying their traffic without being the one who decided to send it, that's an intermediary. Picture a general-purpose AI assistant fetching a page because someone typed a question into a different company's app built on that assistant's API: the assistant operator runs the infrastructure, but it was someone else's product that decided to send the request. (You can read more about these classificationshere.)

![BLOG-3473 4.png](/images/posts/d06190a38e9f.jpg)

That's the full picture: what your bot does, how it treats what it reads, and who's behind it, described as it actually is instead of squeezed into one label. The clearer that picture, the more accurately website owners can decide how to treat your bot.

## Faster, more consistent review

Operators also asked for faster reviews. We hear you on this, too.

The number of new bots submitted each year has grown sharply â increasing about 7 times in volume since 2023 â and reviewing every one of them by hand doesn't scale at that pace. Until now, every submission followed the same fully manual path: someone on our team checks it against an internal rubric and makes a judgment call. That kind of review is thorough, but it doesn't scale.Â

[翻译失败，原文如下]

We rebuilt that process to run automatically. Your bot runs through a series of checks â is it a duplicate of one we already track, is your user-agent pattern specific enough to identify your bot without overlapping one that's already registered, and, most importantly, does your claimed verification method actually hold up? We fetch your IP list, confirm your reverse DNS, or validate yourWeb Bot Authsignature automatically, instead of a person doing it by hand. If everything checks out, your bot can be tracked right away. If something needs a closer look, it's routed to our team with the specific reason already flagged, instead of landing as a blank entry in a queue.

For operators, that means most submissions move faster than before.

## Submit your bot today

To join hundreds of bots in BotBase who declare their behavior and content use, and be part of an ecosystem where website owners and bot operators can coexist:

1. Go toProtect & Connect â Application Security â BotBasein theCloudflare dashboard.
2. Open theSubmission formand declare your bot: who operates it, what it does, how it uses content, and how it proves its identity.
3. Submit. Your submission appears inSubmission historyasWaiting for review.

## What's next

This launch is about visibility; there's more coming. Here are our guiding goals:

- Visibility, targeted by this launch. This gives operators the ability to see, understand, and edit submissions.
- Ownership and observability, being targeted soon. This gives operators the ability to claim bot ownership, manage its live directory entry, and better understand how websites are treating their bot.
- Conversation, a longer-term goal. This would open a more sustainable way for bot operators to ask websites to be let in if they can show they provide value rather than harm.Â

Our vision is to keep expanding BotBase so operators can understand exactly how their bot is treated and get guidance on how to crawl the web more politely, turning a one-way submission into an ongoing relationship.

BotBase started as a directory for website owners. It is becoming a place where bot operators take part in the ecosystem, understand where they stand, and keep their information accurate. If you run a bot,submit it and tell us what you need next. We are building the operator side alongside the operators who use it.

## Related tags

Follow on Social Media

- Cloudflare
- Julian Laxman

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[BotBase for Operators: A clearer path to joining Cloudflare's directory of bots and agents](https://blog.cloudflare.com/botbase-for-operators/)
> 
> 翻译时间：2026-08-29 08:49
