---
title: Operate with confidence
title_original: Operate with confidence
date: '2026-10-02'
source: Supabase Blog
source_url: https://supabase.com/blog/select-2026-operate-with-confidence
author: ''
summary: '[翻译失败，原文如下]


  Today at Supabase Select, we announced new tools that let your coding agent find
  production problems, test fixes, and report back, and ne...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-04T07:59:47.485637'
---

[翻译失败，原文如下]

Today at Supabase Select, we announced new tools that let your coding agent find production problems, test fixes, and report back, and new controls that set what the agent can access and when it stops to ask you first.

Diagnosing a production problem today means reading logs, usage charts, and database reports separately and correlating them yourself. Your agent could already read that data, but it had no procedure for investigating and no safe place to test a fix.

For an agent to confidently operate a project:

- It needsdatato observe
- It needsknowledgeon what to look for in that data
- It needsautonomyto test and validate fixes in its own environment
- It needspermissionto do only what is required

## Data#

### query_logs#

Previously your agents were limited in what logs they could access via our MCP. We’ve introduced a new MCP tool that gives your agents raw access to your project logs via SQL, which enables more in-depth and precise investigations.

### More advisor checks#

Programmatic checks can catch obvious issues and provide signal for an agent to investigate further. Advisor previously focused on security and performance checks. We’ve now extended it to health. Advisor will signal when error rates go beyond what is considered normal across Data API, Auth, Storage, and Edge Functions. Checks run on demand from the dashboard or the Management API, and results show up under a new Health tab on the Advisors page.

### Database Connections#

See which sessions hold connections, which queries run long, which are idle in a transaction, which are blocked, and who holds the lock. You can cancel a query or terminate its connection from there. It's on by default for every project, including self-hosted.

### Introducing Notebooks#

A notebook is a file in your supabase folder that combines saved database or log queries with markdown notes. Run Notebooks yourself or get your agents to run them as part of their ongoing observations. You can create notebooks directly in the dashboard via the Assistant, then pull them down locally as files withsupabase notebooks pullif needed. You can also create notebooks locally (including with your own agent) and push them withsupabase notebooks pushto make them accessible in the dashboard.

Notebooks can be found in the new Explorer, an evolution of the SQL editor, which is rolling out to every project through October 12. Once it reaches your project, you can turn it on under Feature Previews in the dashboard. Notebook CLI tools are available in the beta version of our CLI.

## Knowledge#

### Updated Skills#

Supabase skills now point to a living document of common health, security, performance, and resource signals your agent should watch for and how to monitor those signals.

## Autonomy#

Agents operate best in code. Today at Supabase Select we announced several improvements to how Supabase projects are expressed as code, and how that code can run in more environments. This is an important upgrade for the observing → detection → resolving loop: it lets agents test and validate proposed fixes in their own environment before opening a PR. That environment may not be your local machine.

Read more about pg-delta and upgrades to the local runtime in theBuild post.

## Permissions#

Give your agent only the access it needs to do its job, and get alerted when it attempts a riskier action.

### Enterprise-Managed Auth for MCP#

Your company decides who can connect to the Supabase MCP server through its identity provider, starting with Okta. Each token is short-lived and bound to the member who signed in. To cut off access, remove the app from Authorized Apps, or remove the member. This is generally available.

### Scoped Personal Access Tokens#

Limit a token to the organizations, projects, and permissions you choose. Start with a read-only token. It's generally available and is now the default for new tokens created in the dashboard.

### MCP Elicitations#

Before the agent creates a paid project or branch, the Supabase MCP server asks you to confirm the resource, rate, and billing interval in your agent client, then waits for your answer. It also asks for confirmation before running SQL that could delete data. This helps prevent unwanted charges and data loss, but it’s not a guarantee. Your agent client must support elicitations for the prompt to appear.

## Supabase Pipelines#

Pipelines stream your Postgres data to analytical destinations in near real time, so heavy analytics queries don’t impact primary Postgres. Create a pipeline in the dashboard, choose the destination, and select the tables to replicate. The initial sync starts, and schema changes are detected and applied to the destination automatically. The dashboard shows each pipeline's health and the status of every replicated table.

Pipelines are in public alpha on the Pro, Team, and Enterprise plans, with BigQuery, ClickHouse, DuckLake, and Snowflake as destinations.

## Getting started#

Setting up an agent that autonomously observes your project, detects issues, and proposes fixes can be daunting, but it’s really only a prompt away with your favorite agent harness. We’ve created a few prompts and suggested schedules to set your agent up for success.

- Health
- Security
- Performance
- Resources
- Supabase Pipelines: on a paid plan, open Database, then Pipelines in the Dashboard, add a BigQuery, ClickHouse, DuckLake, or Snowflake destination, and pick your tables.Docs.

---

> 本文由AI自动翻译，原文链接：[Operate with confidence](https://supabase.com/blog/select-2026-operate-with-confidence)
> 
> 翻译时间：2026-10-04 07:59
