---
title: 'Data Modeling Best Practices for an Agentic CDP, Part 1: The Data Foundation'
title_original: 'Data Modeling Best Practices for an Agentic CDP, Part 1: The Data
  Foundation'
date: '2026-11-24'
source: Databricks Blog
source_url: https://www.databricks.com/blog/agentic-cdp-data-modeling-data-foundation
author: ''
summary: '[翻译失败，原文如下]


  - An Agentic CDP needs the same data foundation as any CDP. That means the right
  sources, clean data, one identity per customer and trust...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-26T10:39:34.807851'
---

[翻译失败，原文如下]

- An Agentic CDP needs the same data foundation as any CDP. That means the right sources, clean data, one identity per customer and trusted profiles. What changes is speed: agents decide for one person in seconds, so a gap in the data becomes a bad decision just as fast.
- Resolve identity once, after silver, then build gold on one canonical ID. In a medallion architecture, raw data lands in bronze and gets cleaned in silver. Identity resolution then creates a persistent canonical_id, and the gold layer is built from a customer table, 1:1 attribute tables and 1:many behavior tables.
- Flag every gold table as batch or event, and land responses back as data. Event tables built as streaming tables, plus engagement and outcomes stored with holdouts, mean you can add trigger-based campaigns and closed-loop measurement later without a remodel.

A customer saved a jacket to their wishlist on your site 9 days ago. This morning its price dropped 30%. Should you let them know?

That depends on your goal. If you want first-time buyers to come back for a second purchase, the alert could help. If you're growing lifetime value and this customer usually pays full price, the discount may cost more than it earns. Whatever the goal, an agent needs six answers about this one person before it makes the call (Figure 1).

![What an agent has to know before a price-drop alert goes out](/images/posts/358e25a60921.png)

Figure 1. The goal frames one price-drop decision, and the decision needs answers from six kinds of data.

If you're getting customer data ready for an Agentic CDP, start here. At Databricks, we work with many brands on this, and the data model is usually the hardest part. This post is for the data architect who designs the stack that marketers, and now agents, build on.

This is Part 1 of a two-part series. Part 1: the modeling steps, from raw data to omnichannel activation. Part 2: mapping B2C and B2B datasets, attributes and use cases onto the model.

## CDP data modeling: What stays the same, and what changes

An Agentic CDP needs everything a traditional CDP needs: the right sources, clean data, one identity per customer and golden profiles marketers trust. If you've built a CDP before, that work carries over. If you haven't, it's the place to start.

What changes is who does the work and how fast the data has to be right. Agents take on more of the work, such as matching records and drafting audiences, while people choose the sources, review the matches and approve what goes out. And because an agent decides for one person in seconds, a gap in the data turns into a bad decision just as fast.

What changes

Campaign era

Agentic era

What it means for your data model

Unit of work

A segment, refreshed on a schedule

A decision for one person, on demand

Each attribute resolves to one trustworthy value per person

Identity

Matched nightly inside a tool

Owned, explainable and reversible

An identity graph you can audit, with a persistent ID

Context

A profile snapshot

Deep history plus what's happening now

Batch and event data keyed to the same ID

Guardrails

A human reviews the list

Rules people set and agents check before each action

Consent, suppression and business definitions stored as data

Measurement

A report after the campaign

Teams and agents adjust daily from measured results

Engagement and outcomes land back in the lakehouse, with holdouts

Databricks builtCustomerLakearound the same idea. Data teams can define trusted datasets and models once through Databricks and Unity Catalog. Marketers can then use purpose-built interfaces to ask questions, build segments, and activate audiences faster without working around IT or exporting data into unmanaged tools.

## The architecture: six steps from raw data to every channel

Here's the flow we recommend. It's a medallion architecture with one important rule: identity resolution runs after silver, and the canonical ID it creates becomes the join key for gold.

1. Land raw data in bronze.Agree with your marketing team on the sources each use case needs, then connect them: apps and databases withLakeflow Connect, event streams withZerobus Ingest, and partner tables read in place withOpenSharing. People own this step: someone has to choose each source and authorize each connection. Keep bronze raw and append-only, so you can replay history.
2. Clean in silver.Normalize emails, phones and addresses, put timestamps in UTC, put events on one schema and remove duplicates. Leave identity matching for the next step.
3. Resolve identity after silver,in one place, and rerun it as new records arrive. The result is one canonical ID (canonical_id) per person and a crosswalk from every source ID. Agents can do the matching, and people review it.
4. Build the gold layer on the canonical ID:a customer table, 1:1 attribute tables and 1:many behavior tables.
5. Add derived attributes and ML.Compute derived attributes and score models such as propensity and next best action on gold, then write the results back as 1:1 attribute tables on a schedule.
6. Activate across channels, and close the loop.Build audiences on gold-layer data and sync them to the channels you use. CustomerLake Campaign Agents helps marketers build audiences in natural language, powered by Genie, or in the purpose-built UI. Land the responses and engagement metrics back in bronze as new data.

You build the layers withSpark Declarative Pipelines, keep them on schedule withLakeflow Jobsand govern every layer inUnity Catalog.

![Agentic CDP from raw data to omnichannel activation, on one canonical ID](/images/posts/c4c38d8eeb98.png)

Figure 2. One governed path from raw data to connected channels, keyed by one canonical ID.

## Own your identity graph

Brands have asked for years why they can't own their identity graph and run deterministic matching on their own data. The usual answer was upkeep: the rules, reruns and reviews take people and time. With identity resolution running next to the data, owning the graph becomes practical, and in our experience it's the most important table you'll build.

![Agentic CDP data modeling - identity resolution after silver](/images/posts/81ace4c53c1d.png)

Figure 3. Four source records resolve to one person. The id_graph keeps the rule and confidence behind each link.

Run deterministic rules first (exact email, exact phone, a partner ID that maps to your customer ID), then score the gaps with probabilistic matching. Then cluster the matches and mint, or keep, a persistent ID.

- Keep the ID persistent.Don't derive it from one mutable source key, and record merges and splits so downstream systems can follow.
- Decide survivorship explicitly.Pick which source wins for each attribute (most recent, most trusted, most complete) and write the rule down.
- Tune for precision first.Shared family emails, shared devices and business addresses cause false merges, and with a false merge you send one person's offer to someone else.
- Keep people in the loop.Review a sample of matches before each publish, and let data stewards fix the wrong ones.

You can build this with SQL rules plus an open-source matcher such as Splink or Zingg. Or use CustomerLake: Profile Agents handle the heavy lifting of matching and golden-record survivorship. The approach is called Agentic Identity Resolution, which combines deterministic, probabilistic, and LLM-based matching to connect fragmented records. Manual data steward overrides allow teams to apply human judgment where needed.

## Model the gold layer as an entity, attribute tables, and behavior tables

![Agentic CDP data modeling - model gold as three kinds of tables](/images/posts/ff8c8dd66277.png)

Figure 4. Use attribute columns directly; aggregate or filter behavior tables first.

[翻译失败，原文如下]

- Customer table (the entity).One row percanonical_id, with every identifier you activate on: email, phone, address, app user, device, loyalty and CRM IDs. In B2B, accounts and contacts are the entities.
- Attribute tables (1:1).Use several, each with one row percanonical_id: one or two for model outputs such as propensity scores and next best action, one for consent on every channel, and one for other derived attributes such as recency and lifecycle stage. Separate tables let each owner refresh on their own schedule.
- Behavior tables (1:many).Orders, web and app events, engagement and service cases, with one row per event and a timestamp. Keep that grain, because that's where marketers create their own attributes in Campaign Agents, such as orders in the last 30 days.

Keep the full consent history (one row per person, channel, purpose, source and time) and the suppressions, such as unsubscribes and bounces, in silver. Derive the 1:1 consent table from them, so audiences and agents check one place before they send.

### Flag every table: batch or event

Flag each gold table so campaign builders know how fresh it is:

What it means

Examples

Good for

Batch

Refreshed on a schedule

customer, attribute tables

Scheduled campaigns

Event

Updated incrementally as events arrive, one row per event with a timestamp

Web and app events, cart, transactions

In-session decisions, filters and triggers

Build event tables asstreaming tablesin Spark Declarative Pipelines and record the flag as a Unity Catalogtag. Streaming tables can update on a schedule or continuously; for triggers like a cart reminder, run their pipelines in continuous mode, which "keeps tables fresh as new data arrives." Behavior that arrives only on a schedule, such as nightly store sales, stays Batch until you stream it. If the events carry the canonical ID, adding triggers later shouldn't need a remodel.

Two more habits help: compute time windows against a declared as-of date, so a rerun gives the same answer, and keep one governed copy, giving each activation tool only the tables it needs.

## Omnichannel activation and the feedback loop

With the model in place, you define an audience or a decision once, on governed gold tables, and send it to the channels your customers use.

![Agentic CDP data modeling - omnichannel activation](/images/posts/425dbb4218ed.png)

Figure 5. Decide once on governed data, activate across channels, and land responses back as data.

- Pick the right shape for each channel.Batch audiences suit email, paid media and direct mail; in CustomerLake, a scheduled sync can refresh them as often as every 1 minute. Event-triggered decisions suit cart recovery, back-in-stock and in-app moments. Low-latency lookups fromLakebasesuit web personalization, contact centers and agents that need a profile mid-conversation.
- Send the payload with the audience.A personalized message needs attribute columns, such as the next best action and the offer, so sync them with the IDs.
- Close the loop.Land sends, opens, clicks, visits and purchases in bronze, key them to the samecanonical_id, and compare outcomes with a holdout group in each channel.

CustomerLake enables direct syncing of audiences and signals to martech, adtech and CX channels directly with native Reverse ETL connectors, without custom pipelines or additional activation layers.

## A data foundation checklist

If you can say yes to most of these, your foundation is ready for agents:

1. Your marketing and data teams agree on the decisions to support and the sources each one needs.
2. Identity resolution runs in one place, after silver, with incremental reruns and human review, and publishes a persistentcanonical_idwith an auditableid_graph.
3. Gold has a customer table with every identifier, 1:1 attribute tables for model scores, consent and derived attributes, and behavior tables at event grain.
4. Every gold table carries the canonical ID or a natural key and a batch or event flag, and event tables are streaming tables.
5. Engagement and outcomes land back in bronze with holdout groups, and partner data is read in place.

## Getting started

- Land and share data:Lakeflow Connect,Zerobus Ingest,OpenSharing
- Build, schedule and score:Spark Declarative Pipelines,Lakeflow Jobs,MLflow
- Govern and serve:Unity Catalog,Lakebase
- Activate with CustomerLake:Learn more about CustomerLakeand contact your Databricks account team for access.

## Coming in Part 2

The foundation is in place. In Part 2, we put it to work:

- How marketers, data teams and agents share the same gold tables, and how to describe data so every team reads it the same way.
- B2C and B2B datasets side by side, and the keys that join them.
- Attributes worth building first, including ML scores, and the use cases you can launch in weeks, starting with paid media suppression.

We'll come back to the jacket use case in the beginning, and show which datasets answer each of the six questions.

1. What is the best data model for an Agentic CDP?

A medallion architecture where identity resolution runs after silver and its canonical ID becomes the join key for gold. The gold layer has three kinds of tables: a customer table with every activation identifier, 1:1 attribute tables for model scores, consent and derived attributes, and 1:many behavior tables, such as orders and events, at event grain.

2. Where should identity resolution run in a CDP data pipeline?

Identity resolution should run in one place, after data is cleaned in silver and before the gold layer is built. Running it on normalized emails, phones and addresses gives more accurate matches. It should rerun as new records arrive and publish a persistent canonical_id plus an auditable identity graph that records the rule and confidence behind each link.

3. Why should brands own their identity graph?

An owned identity graph is explainable, auditable and reversible, and agents need that to make decisions for one person safely. Brands can run deterministic rules first, score the gaps with probabilistic matching, and record merges and splits so downstream systems can follow. With identity resolution running next to the data, keeping the graph up to date is now practical.

4. What is the difference between attribute tables and behavior tables in a CDP?

Attribute tables have one row per customer, holding values like propensity scores, consent status or lifecycle stage. Behavior tables have many rows per customer, one per event with a timestamp, such as orders, web visits or service cases. Marketers use attribute columns directly and aggregate behavior tables into new attributes, such as "orders in the last 30 days."

5. How do you prepare a CDP data model for real-time, trigger-based campaigns?

Flag each gold table as batch or event, and build event tables as streaming tables keyed to the canonical ID. For triggers like cart recovery, run those pipelines in continuous mode. If events already carry the canonical ID, you can add triggers later without remodeling. Landing responses back in the lakehouse then closes the measurement loop.

MarketingandBest Practices

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Data Modeling Best Practices for an Agentic CDP, Part 1: The Data Foundation](https://www.databricks.com/blog/agentic-cdp-data-modeling-data-foundation)
> 
> 翻译时间：2026-11-26 10:39
