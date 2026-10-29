---
title: Automate your Supabase backend with Make
title_original: Automate your Supabase backend with Make
date: '2026-10-28'
source: Supabase Blog
source_url: https://supabase.com/blog/automate-your-supabase-backend-with-make
author: ''
summary: '[翻译失败，原文如下]


  TheSupabase integration for Makeis now available. Connect your Supabase account
  to Make, and your automation and AI agents can work with ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-29T08:15:55.699244'
---

[翻译失败，原文如下]

TheSupabase integration for Makeis now available. Connect your Supabase account to Make, and your automation and AI agents can work with your projects directly: query your database, read logs, deploy Edge Functions, and manage your projects as workflow steps.

Make, part of Celonis, is an AI automation platform where more than 400,000 organizations build workflows, called scenarios, across 3,000+ connected apps. Scenarios live on a visual canvas, so people across a business can build them and every step stays visible and governable. This integration adds your Supabase projects to that lineup.

## Two ways to connect: Supabase API apps or AI agents via MCP#

How you bring Supabase into a scenario depends on the job:

- Supabase API apps:drop pre-built modules into the scenario builder for steps that run the same way every time, like querying the week's signups every Monday morning to post a summary where your team already works, or writing a record into Postgres when a deal closes in your CRM.
- MCP client and AI agents:connect a scenario or a Make AI Agent to the Supabase MCP server. The agent gets structured access to your project, so it can route errors from your logs into your issue tracker, or answer a question from what's actually in the database.

Either way, you can build the scenario visually or describe it in plain language to Maia, Make's AI assistant.

## Live data instead of exports#

Inside a scenario, Supabase looks like any other app, the same as the CRM or help desk beside it. That puts the database within reach of anyone who builds scenarios, and they're usually on a different team from whoever runs Postgres. The scenario builder works with live data without asking for an export, and the engineer gets to delete the nightly sync that used to sit between them.

Make tracks every scenario run and agent tool call as it happens, so both of them can open the history and see exactly what touched the database.

## How to connect#

You'll need aMake accountand a Supabase project:

1. Add the MCP Client app to your scenario and choose the Call a tool module, or add it as a tool for a Make AI Agent
2. Create a connection and select Supabase
3. Pick a tool and map its inputs

Every tool the Supabase MCP server exposes is annotated as read-only or destructive, so you know what a scenario can touch before it runs. The pre-built Supabase apps connect with project credentials instead; setup for those lives inMake's app directory.

## Built in partnership with Make#

AI automation earns trust when engineering and leadership can both see what it's doing. Whether a scenario runs deterministic steps or hands a task to an agent, bringing Supabase to Make keeps every database action visible and governed.

—Ina Adamczyk, Tech partnerships lead, Make

## Get started#

The integration runs through Make's MCP Client, included on every Make plan.

- Connect Supabase in Make

---

> 本文由AI自动翻译，原文链接：[Automate your Supabase backend with Make](https://supabase.com/blog/automate-your-supabase-backend-with-make)
> 
> 翻译时间：2026-10-29 08:15
