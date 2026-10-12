---
title: 'Build anything: Supabase from code, and an MCP server for your app'
title_original: 'Build anything: Supabase from code, and an MCP server for your app'
date: '2026-10-02'
source: Supabase Blog
source_url: https://supabase.com/blog/select-2026-build-anything
author: ''
summary: '[翻译失败，原文如下]


  Today at Supabase Select, we announced new tools that let your coding agent set
  up your backend, test changes locally, and deploy the ser...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-12T08:23:17.064397'
---

[翻译失败，原文如下]

Today at Supabase Select, we announced new tools that let your coding agent set up your backend, test changes locally, and deploy the services behind your app. We also gave your users’ agents a way to work inside your app as the signed-in user. Your agent already writes your application code, but the backend was still your job, because most of that work happened in the dashboard: create a table, change an RLS policy, then pull the change into a migration with the CLI. Your agent works in your repo, and changes made in the dashboard don't appear there.

Now your schema and project config can live in your repo, where your agent can work on them. The agent writes the schema as SQL files, andpg-deltaworks out the migration. A setting changed in the dashboard comes back to your config file with one command. Before a change ships, your agent can try it locally: local development doesn’t need Docker, and each directory gets its own stack, so the agent can test two changes side by side and keep the one that works.

Many apps require long-running processes: agents, embeddings for a large set agents, embeddings for a large set of files, a service that stays up, or code that needs its own sandbox. Supabase Compute runs that work as a long-lived service in the same project as your database.

Your users are already in Claude, ChatGPT, or Cursor, and when one of them asks their agent to do something in your app, the agent needs a way in. Your app can now have its own MCP server, deployed inside the Supabase project you already have. Users sign in the way they already do, and their agent sees only what they're allowed to see.

## Agent-ready local development#

Local Supabase can now run as native processes, so it starts on machines without a Docker daemon: Claude Code's sandbox, Codex, Perplexity Computer, and CI runners. On a machine with Docker, nothing changes. You can also run multiple local Supabase instances, one per directory, so several checkouts or git worktrees of the same repo run at the same time. It's in alpha today, off by default.

Declarative Schemas 2.0: coding agents are good at editing schema files and bad at writing migrations. Your agent edits the SQL files, which are the source of truth, andpg-delta, the CLI's new diff engine, generates the migration from them. New projects created withsupabase initusepg-deltaby default, and existing projects can turn it on inconfig.toml.

Config in code: settings like auth providers, API limits, and storage buckets live inconfig.tomlnext to the schema. A setting changed in the dashboard comes back into the file withsupabase config pull, andsupabase pullpulls config, schema, and Edge Functions in one command.

## Supabase Compute#

Compute runs web services and agents in any language next to your database. There's no limit on how long a service runs, you choose the memory and CPU, and each service gets a full Linux environment, which Edge Functions don't have.

Deploy from the Supabase CLI, or manage services through the Management API. The service definition lives inconfig.toml, and agent skills for Compute let your coding agent write, deploy, monitor, and debug a service for you. A service gets the same default environment variables as your Edge Functions, so it connects to your database and other Supabase services. In the dashboard you see each service's runtime, invocations, and logs.

Each service gets a public HTTP URL, like an Edge Function. Set the number of instances, and Supabase balances requests across them. You can also deploy a service as private, with no HTTP endpoint, for background jobs from a database queue or as a sandbox for an agent. To tighten security further, network restrictions can limit database access to your Compute instances.

Join the waitlist for private alphahere.

## Your app's MCP server#

MCP is the standard that lets agents talk to your app on behalf of your users. Your app's MCP server is separate from the official Supabase MCP server, which helps you build your app.

Add a customizable MCP server to your own app from theSupabase library. One shadcn command adds an authenticated Edge Function to your codebase, ready to deploy to Supabase. You own the code, so your agent can use the included instructions and Supabase client to add the tools that fit your product, and your RLS policies still decide which rows each user can reach.

It's built on@supabase/serverand the new Supabase Middleware, which also work on their own in any server code that needs to know who is signed in.

We also built aheadless app template: a backend with an agent as the main interface, ready to deploy to Supabase.

## Get started#

- Agent-ready local development: update theSupabase CLI, then add[experimental]andstack = truetosupabase/config.toml, or setSUPABASE_EXPERIMENTAL_STACK=1.
- Declarative Schemas 2.0: put your schema insupabase/schemas/*.sql, runsupabase db schema declarative syncto generate and apply the migration locally, then runsupabase db push. Existing projects: add[experimental.pgdelta]andenabled = truetosupabase/config.toml.Docs.
- Supabase Compute: in private alpha.Join the waitlist.
- Your app's MCP server: get your project into code withsupabase pull, then runnpx shadcn@latest add @supabase/mcp-serverfrom theMCP server block. It needs asymmetric signing keys and the Supabase Auth OAuth server turned on.

---

> 本文由AI自动翻译，原文链接：[Build anything: Supabase from code, and an MCP server for your app](https://supabase.com/blog/select-2026-build-anything)
> 
> 翻译时间：2026-10-12 08:23
