---
title: Agentic Coding on Supabase with OpenCode
title_original: Agentic Coding on Supabase with OpenCode
date: '2026-06-30'
source: Supabase Blog
source_url: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
author: ''
summary: '[翻译失败，原文如下]


  The OpenCode integration for Supabase is now available.


  Type/supabase, authenticate, and your agent can work with Supabase account/proje...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:39.681086'
---

[翻译失败，原文如下]

The OpenCode integration for Supabase is now available.

Type/supabase, authenticate, and your agent can work with Supabase account/project management APIs plus bundled Supabase skills. For database, Edge Functions, logs, and other project-scoped capabilities, the plugin guides users through connectingSupabase MCP.Requires OpenCode 1.3.4 or later.

OpenCodeis an open source AI coding agent with more than 180,000 GitHub stars and 7.5M monthly active users. It runs in your terminal, IDE, or desktop, supports 75+ LLM providers, and lets you run multiple agents in parallel on the same project.

AI agents are taking on more of the coding workflow, and they need access to more than just the codebase. Teams likeRamp,JFrog,Cloudflare, andAppleare already running OpenCode at scale. This integration gives those agents direct access to your Supabase backend, so they can go beyond writing code and verify their own work, query data, check logs, and deploy functions.

## What the OpenCode integration includes#

Once connected, the integration can:

- Monitor agent activity in real time from OpenCode
- List your Supabase organizations and projects
- Create new Supabase projects from your coding session
- Open the Supabase MCP setup flow for a chosen project
- Bundle Supabaseagent skillsso your agent gets Supabase-specific guidance without a separate install step

Here's the integration running inside Minecraft. OpenCode connected to Supabase via MCP, created a table, populated it with data, and deployed an Edge Function without ever leaving a survival world. Everything you see is running on a real Supabase project. The dirt house, however, is optional.

The plugin is open source and built in collaboration withJumskifrompgflow. You can find ithere.

## Get started#

→ Connect OpenCode to your Supabase project

---

> 本文由AI自动翻译，原文链接：[Agentic Coding on Supabase with OpenCode](https://supabase.com/blog/agentic-coding-on-supabase-with-opencode)
> 
> 翻译时间：2026-10-20 07:22
