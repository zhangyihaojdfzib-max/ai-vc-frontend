---
title: X / Twitter OAuth 2.0 is now available for Supabase Auth
title_original: X / Twitter OAuth 2.0 is now available for Supabase Auth
date: '2026-02-06'
source: Supabase Blog
source_url: https://supabase.com/blog/x-twitter-oauth-2-provider
author: ''
summary: '[翻译失败，原文如下]


  You can now add "Sign in with X" to your application using the newX / Twitter (OAuth
  2.0)provider inSupabase Auth.


  ## What''s new#


  The n...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-11T09:04:32.614763'
---

[翻译失败，原文如下]

You can now add "Sign in with X" to your application using the newX / Twitter (OAuth 2.0)provider inSupabase Auth.

## What's new#

The new provider uses X's OAuth 2.0 implementation, replacing the legacy OAuth 1.0a flow. OAuth 2.0 offers a more modern authentication experience with better security practices, including PKCE support.

## Getting started#

Setting up X / Twitter authentication takes a few steps:

1. Create an OAuth 2.0 app in theX Developer Portal
2. Enable "Request email from users" in your app's authentication settings
3. Add your callback URL from the Supabase dashboard
4. Copy yourClient IDandClient Secretfrom the "Keys and tokens" section
5. Enter these credentials inAuthentication > Providers > X / Twitter (OAuth 2.0)in the Supabase dashboard

Once configured, you can use the Supabase client libraries to authenticate users via X / Twitter:

For a complete guide on setting up X / Twitter authentication, see thefull documentation.

## Migration note#

If you're currently using the legacyTwitter (OAuth 1.0a)provider, we recommend migrating to the new OAuth 2.0 provider. The legacy provider will remain available while X / Twitter continues to support OAuth 1.0a.

## Resources#

- X / Twitter Auth documentation
- Social Login overview

---

> 本文由AI自动翻译，原文链接：[X / Twitter OAuth 2.0 is now available for Supabase Auth](https://supabase.com/blog/x-twitter-oauth-2-provider)
> 
> 翻译时间：2026-11-11 09:04
