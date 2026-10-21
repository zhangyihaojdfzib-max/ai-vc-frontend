---
title: AI Gateway logs now show session affinity - Vercel
title_original: AI Gateway logs now show session affinity - Vercel
date: '2026-10-18'
source: Vercel Blog
source_url: https://vercel.com/changelog/ai-gateway-logs-now-show-session-affinity
author: ''
summary: '[翻译失败，原文如下]


  AI Gateway logsnow have aSessions viewthat groups requests into sessions and shows
  how session affinity routed each one. Each row shows t...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:25.232429'
---

[翻译失败，原文如下]

AI Gateway logsnow have aSessions viewthat groups requests into sessions and shows how session affinity routed each one. Each row shows thecoding agentor app that ran the session, such as Claude Code, Codex, or Cursor, along with its cost, models, providers, and how much of its input was cached across every turn.

![See logs grouped by sessions with a view into cache hit rate, session id, cost, and more.](/images/posts/4e1a2dd4e491.jpg)

![See logs grouped by sessions with a view into cache hit rate, session id, cost, and more.](/images/posts/d67e6e2b1060.jpg)

![See logs grouped by sessions with a view into cache hit rate, session id, cost, and more.](/images/posts/affd469ec429.jpg)

![See logs grouped by sessions with a view into cache hit rate, session id, cost, and more.](/images/posts/d543a0870640.jpg)

Open a session to see its cache hit rate, duration, and path. The path lists each turn with its model and timing, and names the provider serving the session along with any earlier ones.Session affinitysends each turn to the provider that served the one before it, so the provider already has most of the prompt in cache. A session that stays on one provider reads more of each prompt fromcache.

Filter sessions by turns, client, model, provider, authentication, or cost. Single-turn sessions are hidden until you clear the minimum turns filter.

![View individual sessions to see more detailed information on the requests and metrics.](/images/posts/e66da215e87f.jpg)

![View individual sessions to see more detailed information on the requests and metrics.](/images/posts/d41da0d91460.jpg)

![View individual sessions to see more detailed information on the requests and metrics.](/images/posts/52e7e9b307fa.jpg)

![View individual sessions to see more detailed information on the requests and metrics.](/images/posts/4ee7f3fec055.jpg)

Session affinity runs by default on text and chat requests. To group requests yourself, send the samesessionIdinproviderOptions.gateway, or the samex-session-idheader, on every request in a conversation. Requests without one are grouped by a fingerprint of the conversation's opening and appear as fingerprinted sessions.

Read thesession affinity documentationfor more information on how AI Gateway identifies sessions.

---

> 本文由AI自动翻译，原文链接：[AI Gateway logs now show session affinity - Vercel](https://vercel.com/changelog/ai-gateway-logs-now-show-session-affinity)
> 
> 翻译时间：2026-10-21 06:58
