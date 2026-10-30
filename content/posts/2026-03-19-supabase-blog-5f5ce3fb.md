---
title: Supabase Joins the Stripe Projects Developer Preview
title_original: Supabase Joins the Stripe Projects Developer Preview
date: '2026-03-19'
source: Supabase Blog
source_url: https://supabase.com/blog/supabase-joins-the-stripe-projects-developer-preview
author: ''
summary: '[翻译失败，原文如下]


  Supabase is part of theStripe Projectsdeveloper preview. Stripe Projects is a new
  workflow in the Stripe CLI that lets developers and AI ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:48:03.088419'
---

[翻译失败，原文如下]

Supabase is part of theStripe Projectsdeveloper preview. Stripe Projects is a new workflow in the Stripe CLI that lets developers and AI agents provision real services and get working credentials from a single command. With Supabase in the catalog, one command provisions a Postgres database along with the rest of Supabase (Auth, Storage, Edge Functions, and Realtime) without ever opening a dashboard.

AI Agents need a fast way to provision infrastructure, with deterministic steps and real credentials. They cannot click through a browser or guess at setup docs.

Stripe Projectsoffers a standard provisioning workflow for AI Agents and humans. One command handles account setup, resource provisioning, and credential delivery. Credentials land in your environment in a format that both humans and agents can use. Your Supabase account and dashboard stay yours and are always accessible.

We worked closely with Stripe as a co-design partner on the integration spec. That means provisioning a Supabase project through Stripe Projects is deterministic and repeatable. Whether you run it yourself or an agent runs it for you, the steps are the same.

## How it works#

Install the Stripe CLI, then run:

That's it. A new Supabase project is created in your account with a full Postgres database ready to connect. To open the Supabase dashboard directly:

If you already have a Supabase account, the flow will prompt you to link it instead of creating a new one.

## What you get#

A complete Supabase project

Every project includes a Postgres database, Auth, Storage, Edge Functions, and Realtime.Learn more in the docs.

Credentials in your environment

After provisioning,stripe projects env --syncwrites your project credentials to a local.envfile. They are also stored in your Stripe Project so agents can access them directly.

Your account, your data

The database lives in your own Supabase account. You keep full access to the Supabase dashboard, your connection strings, and your data. Nothing is proxied or white-labeled.

Credential rotation

You can rotate your database credentials at any time:

This updates the stored secrets in your Stripe Project automatically.

## Get started#

This is a developer preview. Install the Stripe CLI, then run:

Install the Stripe CLI

Stripe Projects docs

We want to hear from you. If you run into issues or have feedback,reach out on Discordor open an issue onGitHub.

---

> 本文由AI自动翻译，原文链接：[Supabase Joins the Stripe Projects Developer Preview](https://supabase.com/blog/supabase-joins-the-stripe-projects-developer-preview)
> 
> 翻译时间：2026-10-30 08:48
