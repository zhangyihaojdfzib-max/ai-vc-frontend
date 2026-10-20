---
title: Ship changes to your Supabase backend with Grok Bot
title_original: Ship changes to your Supabase backend with Grok Bot
date: '2026-10-13'
source: Supabase Blog
source_url: https://supabase.com/blog/ship-changes-to-your-supabase-backend-with-grok-bot
author: ''
summary: '[翻译失败，原文如下]


  Supabase is joining the SpaceXAI Partner Network. With Grok Bot connected to Cursor,
  anyone on your team can request a change in chat, an...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:39.786247'
---

[翻译失败，原文如下]

Supabase is joining the SpaceXAI Partner Network. With Grok Bot connected to Cursor, anyone on your team can request a change in chat, and Cursor builds and runs it against your Supabase backend through theSupabase MCP server.

Grok Bot takes a request from the person who needs it, in the place they already work, and hands it to Cursor as scoped engineering work. Cursor writes and runs the code, and through the Supabase MCP server, it can query the database, inspect the schema, read logs, and deploy Supabase Edge Functions, all inside the one Supabase project where the data already lives.

## Agents work the way developers do#

To see what that looks like in practice, we analyzed millions of Supabase tool calls from Cursor sessions. When an agent runs a query against a Supabase database, the next call is another query 92% of the time: it investigates, tests, fixes, and checks its work rather than looking something up and stopping. Ask why signups dropped last week, and Cursor narrows to a single broken referral source in a dozen steps.

Mistakes don't break the loop. When a query fails, the next call is anotherexecute_sql79% of the time, and only about 2% of errors end the session, so a query written againstcreatedinstead ofcreated_atgets corrected without anyone stepping in. Tell Cursor a Stripe webhook is failing, and it pulls the logs, checks the payments table, patches the Edge Function, and redeploys.

## Requests can come from anyone#

The person asking doesn't need to know which project holds the answer or which table to look in. Cursor already knows which Supabase project it's working in most of the time and lists projects to find the right one when it doesn't, then reads the schema withlist_tablesbefore it queries. When the person who made the request isn't watching the code, that's what keeps the work moving.

## Add a security check to the loop#

Agents already verify their own changes: after anapply_migration, 81% of sessions follow up with a query orlist_tablesto confirm the change landed.get_advisorsgoes further and scans the project for issues like tables missingRow Level Securityor unindexed foreign keys, which matters when requests can come from anyone and ship automatically.

A simple Cursor rule makes the scan part of every schema change:

With that rule in place, a request to add a comments feature ships with RLS enabled and the security check already run.

## Built in partnership with SpaceXAI#

Developers found the Supabase integration on their own, and it consistently ranks among the top community plugins for SpaceXAI's tools. Joining the Partner Network lets us support that demand directly and keep the integration a first-class experience as those tools evolve.

## Get started#

- Connect the Supabase MCP server
- New to Supabase?Start your project for free, then connect it to Cursor

---

> 本文由AI自动翻译，原文链接：[Ship changes to your Supabase backend with Grok Bot](https://supabase.com/blog/ship-changes-to-your-supabase-backend-with-grok-bot)
> 
> 翻译时间：2026-10-20 07:22
