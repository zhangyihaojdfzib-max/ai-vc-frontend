---
title: Introducing the unified Supabase .NET SDK
title_original: Introducing the unified Supabase .NET SDK
date: '2026-10-19'
source: Supabase Blog
source_url: https://supabase.com/blog/introducing-the-unified-supabase-net-sdk
author: ''
summary: '[翻译失败，原文如下]


  The latest major version of our .NET SDK,v8, is now available!

  It brings every Supabase .NET package under a single repository with a uni...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-12T08:23:17.242319'
---

[翻译失败，原文如下]

The latest major version of our .NET SDK,v8, is now available!
It brings every Supabase .NET package under a single repository with a unified version number, and provides a new extension for dependency injection.

This is the first release where all the packages ship together, so here is what to expect.

## One version for every package#

Until now, the packages were scattered across multiple repositories, with their own version and lifecycle.
Gotrue was onv6.x.x, Realtime onv7.x.x, while the main package was onv1.x.x.

Fromv8.0.0, all packages share the same version number. Gotrue, PostgREST, Realtime, Storage, Functions, and the umbrellasupabasepackage all release together.
When you see a version, you know exactly which packages and dependencies it pairs with.
On your side, it makes upgrades much easier.

Moving fromv1.x.xtov8.0.0, in one go, is quite a bump and unusual.
It was our only option to guarantee lockstep-versioning:v8.0.0was the first major bump available with Realtime already onv7.x.x.
It's a price we only have to pay once.

## Everything in one repo#

All the packages now live in a single repository:supabase-community/supabase-csharp.
It simplifies everything (especially cross-package work), whether it's contributions, maintenance or releases.

Previous repositories are still available but have been archived, and are now read-only.
They also have been removed from ourCommunity page.

## New extension package#

A new package,Supabase.Extensions.DependencyInjection(available onNuGet), registers the Supabase client with the .NET service container and letsIHttpClientFactorymanage itsHttpClient.
If you run ASP.NET Core, this is the way to register Supabase into your app.

This package also follows lockstep-versioning, and therefore start atv8.0.0as well.

## Misc updates#

These did not deserve an entire section, but are worth mentioning:

- All serialization is handled withSystem.Text.Jsoninstead ofNewtonsoft.Json.
- Retry with backoff is built into every service package, and configurable.
- The client also accepts publishable and secret API keys.
- All packages targetnetstandard2.1. If you use the umbrella package you were already on it, so nothing changes.

## Upgrading fromv7.x.x#

v8.0.0being a major version, breaking changes are expected.
We wrote amigration guideto help you upgrade.
It covers all the breaking changes you might encounter, and how to address them.

## Wrap up#

For the full list of changes, see therelease notes.

Update your packages to v8.0.0, and let us know how it goes onGitHub.
We're excited to hear your feedbacks.

---

> 本文由AI自动翻译，原文链接：[Introducing the unified Supabase .NET SDK](https://supabase.com/blog/introducing-the-unified-supabase-net-sdk)
> 
> 翻译时间：2026-10-12 08:23
