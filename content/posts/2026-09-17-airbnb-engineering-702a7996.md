---
title: 'The guest journey, updated in real time: extending Airbnb’s sequence recommender
  with Chronon'
title_original: 'The guest journey, updated in real time: extending Airbnb’s sequence
  recommender with Chronon'
date: '2026-09-17'
source: Airbnb Engineering
source_url: https://medium.com/airbnb-engineering/the-guest-journey-updated-in-real-time-extending-airbnbs-sequence-recommender-with-chronon-8f1582578553?source=rss----53c7c27702d5---4
author: ''
summary: '[翻译失败，原文如下]


  # The guest journey, updated in real time: extending Airbnb’s sequence recommender
  with Chronon


  ## How two new Chronon capabilities, Pus...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-18T06:56:40.279282'
---

[翻译失败，原文如下]

# The guest journey, updated in real time: extending Airbnb’s sequence recommender with Chronon

## How two new Chronon capabilities, Push Mode and NRT Model Transform, allows us to provide more relevant search results instantly as a guest explores, rather than waiting for the next batch run.

Listen

By:Pengyu Hou,Yuli Han,Daochen Zha,Haozhen Ding,Xin Liu,Sophie Wang,Pallavi Adusumilli,Sherry Li,Henry Saputra,Chun How Tan,Huiji Gao,Yan Zhang,Stephanie Moyerman,Yi Li, andSanjeev Katariya

A guest’s interaction with Airbnb doesn’t pause to wait for a nightly batch job. Someone might browse a dozen listings on a Tuesday afternoon, run a new search that evening, and expect the next search to reflect the recent activity; it’s also to Airbnb’s benefit for that to be the case. In our previous post,Personalizing Airbnb search by learning from the guest journey, we described how we built a Transformer-based sequence encoder that creates better, more personalized search rankings for a guest using the booking, review, and browsing data that is most relevant to them — their own. That system ran as a daily batch job: each night it processed the previous day’s activity and refreshed embeddings for guests who had something new to show for it.

That design worked well, but it left a gap. Activity from earlier the same day wouldn’t show up in the embedding until the following day’s run, on top of the pipeline’s own processing lag — in practice, up to nearly two days of staleness. For a guest actively planning a trip, that meant the ranking model was often working from a slightly outdated picture of what they wanted, and the recent activities are often highly relevant to current search needs. This is a limitation that our original JourneyFormer research had already flagged as needing new serving infrastructure to solve.

In this post, we describe how we closed that gap by adding two new capabilities toChronon, Airbnb’s feature platform: Near-real-time Model Transform and Push Mode. Chronon is an open source project, and these capabilities have been contributed back to ourpublic repo.

## Background

To keep a multi-layer Transformer off the critical serving path, our original design split inference into two stages. Offline, the sequence encoder would run as a scheduled batch job: each night, it would process the previous day’s guest activity and write a fresh embedding to a low-latency store for any guest who had something new to show for it. Online, retrieval was already real-time: the moment a guest ran a search, the ranking model read that guest’s embedding straight out of the store and combined it with the live query to score candidate listings.

This split kept serving latency low while still letting every ranking decision draw on years of guest history — but it meant an embedding was only ever as fresh as the last completed batch run.

## Challenges

Moving from daily batch updates to near-real-time updates introduced three potential challenges that we needed to address:

- First, staleness had two separate sources: the batch schedule itself, which only ran once a day, and processing lag within that job, which pushed effective staleness closer to two days. Fixing only one of these wouldn’t have been enough to fully close the gap; we needed a pipeline that could react to a guest’s activity as it happened, not simply run more often.
- Second, our sequence encoder was built to run as a scheduled inference job over a full day’s snapshot of guest events, not as a service reacting to individual activity events one at a time. Wiring model inference into a real-time pipeline meant rethinking where and how the encoder got called, without duplicating the offline logic used for training.
- Third, guest activity signals — page views, searches, and other interactions — arrive as independent event streams. Reacting to any one of them in isolation risked missing the fact that these events need to be merged with a guest’s longer-term profile and routed through the encoder consistently, so the resulting embedding stays comparable to the one produced by the batch pipeline it replaces.

## Solutions

We addressed these challenges by building two general-purpose capabilities into Chronon, rather than by building a modified pipeline specific to our use case.

## Push Mode in Chronon

The first is Push Mode. Chronon already runs streaming jobs that keep feature values up-to-date as new events arrive. Push Mode extends this by having a streaming job publish a lightweight notification as soon as it commits a new feature value, instead of waiting for something downstream to poll for it. This turns a reactive step into an event-driven trigger: the moment a guest’s activity feature updates, downstream consumers are notified and can act immediately. For our use case, this meant a guest’s newest search or listing view could kick off embedding generation right away, instead of waiting for a scheduled job to notice it.

## Near-real-time model transform in Chronon

The second is Near-real-time (NRT) Model Transform, which lets model inference run as part of the same streaming pipeline. Historically, running a model meant either embedding its logic directly into application code or waiting for an offline batch job. NRT Model Transform lets Chronon call an already-deployed model — in our case, the same Transformer sequence encoder from the batch pipeline — directly from within the streaming flow, and write the result back as a feature value that is immediately available for serving.

## Integration

Combining the two, our new pipeline works like this: a guest’s activity event, such as a page view or a new search, is captured by a streaming job that merges it with the guest’s existing long-term and short-term sequence data. Push Mode then signals that new sequence data is ready, and NRT Model Transform runs the sequence encoder over it, producing a fresh embedding without waiting for the next scheduled run. The embedding is written to the same low-latency store the batch job uses, so the ranking model retrieves it exactly as it always has — the only difference is how quickly the embedding it retrieves has been updated.

Because both capabilities live in the platform rather than in a use-case-specific pipeline, other teams working on different near-real-time use cases can build on the same foundation.

## Results

The impact showed up on two relevant dimensions of our search results: freshness and quality.

On freshness, we replaced a pipeline where embeddings could lag actual guest behavior by roughly two days with one where the typical delay is well under a minute. In practice, updates often land within 10 to 30 seconds of the underlying activity. A guest who views a handful of new listings can now have that context reflected in their very next search.

On quality, offline evaluation showed a +1.67% improvement in Normalized Discounted Cumulative Gain (NDCG) over the daily-batch baseline — a large jump for a ranking system that has already been refined for over a decade, where even gains of a fraction of one percent are considered meaningful. Online A/B tests confirmed an approximately one-third of a percent increase in uncancelled bookings. This confirms something we suspected, but hadn’t measured directly: freshness itself is a meaningful source of ranking quality. The same guest representation becomes more valuable to the ranking model, and to the guest themselves, simply by being more current.

Rather than a one-off integration, Push Mode and NRT Model Transform represent general platform capabilities that we expect to serve as a foundation for other near-real-time modeling efforts across Airbnb. Since Chronon is open source, and since both features are already available in the public repository, their impact extends far beyond Airbnb. With these additions, any team running Chronon to build a near-real-time model is able to build on the foundation we’ve created.

## Conclusion

[翻译失败，原文如下]

Our previous post described how encoding a guest’s full history — their bookings, reviews, and recent browsing — allows our ranking system to better prioritize relevant listings based on current search intent. This post closes the remaining gap: making sure that understanding reflects a guest’s most recent activity, not just what they did as of last night’s batch run.

By combining Push Mode’s event-driven triggering with NRT Model Transform’s in-pipeline model inference, we turned a daily batch process into a near-real-time one, cutting effective staleness from roughly two days to less than a minute, and improving offline ranking quality by +1.67% NDCG in the process. More broadly, the pattern we used here: react to an event, merge it with existing state, run inference immediately, and serve the result; is one we expect to generalize to other guest-facing models that depend on freshness.

You can learn more about our team’s work on personalization and search ranking by checking out our previous post onsequence modeling the guest journeyand other engineering blog posts from Airbnb. To learn more about Chronon, check out our previousblog postson the project, and browse the code at our repo:https://github.com/airbnb/chronon.

Interested in learning more about our technical journey? Browse ourprevious publicationsto see how our systems have evolved. If tackling these kinds of challenges excites you, explore ouropen roles.

## Acknowledgments

We would like to especially thank the following people for their great collaboration (listed alphabetically): Ashish Jain, Ben Mendler, Bin Xu, Casey Getz, Gil Forsher, Han Zhao, Hao Li, Jiawei Yao, Jun Shi, Kedar Bellare, Linyun He, Liwei He, Michael Kinoti, Michael Sestito, Mingyang Xu, Pallavi Adusumilli, Ruirong Yang, Shashank Dabriwal, Sid Reddy, Sophie Wang, Tanya Piplani, Tracy Yu, Vijay Velagapudi, Xiaowei Liu, Yangbo Zhu, Yan Zhang, Yi Li, Yiwei Wang, Zach Barahal, and Zhiwei Wang.

All product names, logos, and brands are property of their respective owners. All company, product, and service names used in this website are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.

---

> 本文由AI自动翻译，原文链接：[The guest journey, updated in real time: extending Airbnb’s sequence recommender with Chronon](https://medium.com/airbnb-engineering/the-guest-journey-updated-in-real-time-extending-airbnbs-sequence-recommender-with-chronon-8f1582578553?source=rss----53c7c27702d5---4)
> 
> 翻译时间：2026-09-18 06:56
