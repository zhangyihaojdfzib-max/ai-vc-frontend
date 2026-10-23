---
title: We're Transferring the Stripe Sync Engine to Stripe
title_original: We're Transferring the Stripe Sync Engine to Stripe
date: '2026-04-14'
source: Supabase Blog
source_url: https://supabase.com/blog/stripe-sync-engine-transfer
author: ''
summary: '[翻译失败，原文如下]


  In 2021, we open-sourced the Stripe Sync Engine repo to solve a problem we had ourselves.
  Billing data lived in Stripe, product data live...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-23T07:13:57.967085'
---

[翻译失败，原文如下]

In 2021, we open-sourced the Stripe Sync Engine repo to solve a problem we had ourselves. Billing data lived in Stripe, product data lived in Postgres, and there was no good way to join them. We built a tool to sync Stripe data into astripeschema in Postgres, kept building it in the open, and it grew into something bigger than we expected.

Today, the repo moves fromsupabase/stripe-sync-enginetostripe/sync-engine.

## How we got here#

In December 2025, we announced a one-click integration that brought the Stripe Sync Engine directly into the Supabase dashboard. That launch came from close collaboration with Stripe's engineering team.

Stripe engineers contributed directly to the repo: incremental sync using cursor-based pagination, JSONB storage with generated columns, multi-account support forStripe Connectplatforms, and a new CLI with proper event ordering.

A key part of that collaboration was Stripe's work on automatic, incremental backfilling usingSupabase CronandQueue. This is what made it possible to ingest all of your existing Stripe data into Postgres reliably and at scale, and what unlocked the dashboard integration.

Both teams kept iterating after launch on reliability, install flows, and expanded Stripe object support. The result is a more stable, more capable integration than either team would have shipped alone.

Moving the repo tostripe/sync-engineis the next step in that collaboration, and both teams will keep building it together. All our changes going forward will be made to the newstripe/sync-enginerepo.

## What changes for you#

The Stripe Sync Engine stays open source under the Apache 2.0 license. Thesupabase/stripe-sync-enginerepo will redirect tostripe/sync-engine. Nothing breaks for existing users. The one-click integration in the Supabase dashboard continues to work as before.

This is how Supabase has always worked. We build in the open, support the tools and communities around us, and contribute back as things grow. We are proud to collaborate with companies like Stripe to deliver the best tech for builders.

## What's new#

Alongside the transfer, the latest release includes improvements to reliability and day-to-day management.

New capabilities:

- Coupons sync, one of the most requested additions
- Branching support, so you can install the engine on a branch for safer dev workflows
- Data starts syncing immediately on install, no need to wait for the first cron cycle

Better management:

- One-click upgrades for existing installations
- SSL enforcement now supported (previously a blocker for projects with SSL enforcement turned on)
- Install and uninstall controls restricted to Admins and Owners to prevent partial installs

Reliability and UX:

- Smarter install flow: buttons auto-reset if a process gets stuck
- Clearer, more actionable error messages
- Edge Function source code now visible directly in the dashboard

## Get started#

With your Stripe data in Postgres, you can join it directly with your application data. Useful for operational decisions like feature gating and subscription checks, and analytical queries like calculating MRR or understanding churn. For a full walkthrough with SQL examples, seeSync Stripe Data to Your Supabase Database in One Click.

The Stripe Sync Engine is available from theIntegrations section of your Supabase dashboard. The repo is atgithub.com/stripe/sync-engine.

---

> 本文由AI自动翻译，原文链接：[We're Transferring the Stripe Sync Engine to Stripe](https://supabase.com/blog/stripe-sync-engine-transfer)
> 
> 翻译时间：2026-10-23 07:13
