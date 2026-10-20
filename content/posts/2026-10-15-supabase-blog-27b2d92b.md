---
title: 'Supabase Middleware: composable, reusable middleware for Web Fetch handlers'
title_original: 'Supabase Middleware: composable, reusable middleware for Web Fetch
  handlers'
date: '2026-10-15'
source: Supabase Blog
source_url: https://supabase.com/blog/supabase-middleware
author: ''
summary: '[翻译失败，原文如下]


  On October 2 at Supabase Select we shipped@supabase/middleware, composable, type-safe
  middleware for Web Fetch handlers. You can now writ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:40.607523'
---

[翻译失败，原文如下]

On October 2 at Supabase Select we shipped@supabase/middleware, composable, type-safe middleware for Web Fetch handlers. You can now write per-request logic once and run it on any runtime that supports fetch. The same middleware also works inside frameworks like Hono, H3, Elysia, NestJS, and TanStack Start. To use it in a framework, you copy a short bridge file into your project.@supabase/middlewareis free, MIT-licensed, and built for TypeScript developers who write fetch handlers.

## Why we built Supabase Middleware#

@supabase/serverhas covered the setup step since May: one wrapper gives your handler a client scoped to the caller, an admin client, and verified identity and claims. But your handler still carries its own per-request logic on top: checking a flag, handling CORS, deciding what a request needs before your code runs. That logic stays stuck in the handler where you wrote it.

Move to another runtime, and you write it again. Adopt a framework, and you rewrite it as that framework's middleware, and it stays there. Start a second project and you copy the file, or your coding agent writes it from scratch, a little different each time. Every version is another chance for a security mistake.

We wanted that logic to live in one place and go wherever your handler goes. So we built Supabase Middleware. You define each piece once, compose them in order, and use them on any fetch runtime or inside a framework.

## How Supabase Middleware works#

Here's what that looks like in a handler. The setup from@supabase/serverand the logic you add on top become entries in the same list.

A request goes through the entries in order.withCorsanswers the preflight and adds CORS headers to responses.withRequiredClaimsverifies the caller's JWT; if it's invalid, the chain stops there and the caller gets a 401.withSupabaseClientaddsctx.supabase, a client scoped to that caller. Then your handler runs, and all it contains is the part that's yours.

Each entry does one job and doesn't know about the handler it sits in. It adds one typed key to a sharedctx, and your handler sees everything added before it, with the right types. An entry can also return aResponseand stop the chain, or read and change the response on its way out. That's why you can move an entry to another handler without rewriting it.

## What Supabase Middleware ships#

@supabase/middlewareis the engine behind the pipeline above, andwithSupabasein@supabase/serverruns on it.@supabase/serveralso ships the middleware below as standalone entries. Two of them,withSupabaseClientandwithSupabaseAdminClient, are the same pieceswithSupabaseis built from. The engine addswithCorsandwithFeatureFlag.

Most of these aren't new capabilities.ctx.supabase, for example, has been documented as RLS-scoped since May. What's new is the engine. Every piece is an entry in the same list, so you can add one, drop one, or write your own, and the same list goes wherever your handler goes.

## Where Supabase Middleware runs#

You can pick the runtime or framework that fits the job and change it later without rewriting your per-request logic. This section shows how that works on other runtimes and inside a framework.

### Export the pipeline as a fetch handler#

Moving to another runtime doesn't mean rewriting your logic. That matters when your code doesn't all run in one place. Say some of your functions run on Supabase Edge Functions and others on Vercel Functions or Cloudflare Workers, and the auth and CORS rules should match on both. You write those rules once, and each runtime runs them.

This works because thepipelinein the example above is a standard fetch handler: a function that takes aRequestand returns aResponse. Supabase Edge Functions, Vercel Functions, Cloudflare Workers, Deno, Bun, and Node 22 or newer can all run one, and the engine is plain Web Fetch.

Using the engine doesn't tie you to Supabase. It needs no database, no Supabase project, and no account, and it's MIT-licensed. So if you leave Supabase, the engine and everything you wrote with it go with you.

Note that one middleware doesn't run everywhere.withPostgresClientandwithPostgresAdminClientdon't run on Cloudflare Workers, becausepgneeds a TCP socket. The limit comes frompg. The engine itself runs wherever fetch does. On Workers, usewithSupabaseClientandctx.supabaseinstead.

### Inside a framework with a bridge#

Adopting a framework doesn't require rewriting your logic either. For example, say your Edge Functions are plain fetch handlers, your API runs on Hono, and the same auth and CORS rules should apply to both.

Each framework has its own middleware format and its own context object, so middleware written for one doesn't work in another. Without a bridge, adopting a framework means rewriting your logic as that framework's middleware. A bridge removes that step. It's a short file you copy into your project, not a package, so the only thing to install is@supabase/middleware. It runs the middleware you already wrote inside the framework's own middleware slot, and the file is yours to edit.

Bridges for Hono, H3, Elysia, NestJS, and TanStack Start are available now, each typechecked with a minimal example app. Here's the Hono version. Copyhono/supabase-middleware.tsinto your project, then passtoHonothe same array of entries you'd givepipelineon Edge Functions. The entries stay as you wrote them, and the bridge is the only new piece.

Hono has its own middleware, which stays in Hono. Middleware written on the fetch standard works there too, and in any other framework with a bridge.

## Build with the same engine we use#

We built the Supabase middleware withdefineMiddleware, the same public API you get, and no private API sits behind it.

### Give your app its own MCP server#

Say your users want to use your app from their own agent. That means an MCP server for your app, and an MCP server needs authorization: the OAuth protected-resource flow. It takes a metadata route, its preflight, a challenge header on the right responses, and URLs that match what the client called. Every part has to match. If one part is wrong, nothing errors, and the client fails to connect.

With Supabase Middleware, that whole flow is one entry.withOAuthProtectedResourcehandles OAuth discovery for MCP clients, andwithSupabase({ auth: 'user' })verifies the user's token and hands your handler a client scoped to them.

withOAuthProtectedResourceanswers the metadata request before the auth check, and on the way back out it adds the OAuth challenge header to a 401. Because the client is scoped to the signed-in user, every tool call runs as that user, so your tools can be plain queries. We checked this in a working MCP server on Edge Functions, and theBring your own MCP guidebuilds a full one on the same two entries.

Your RLS policies apply to an agent the same way they apply to a browser session. You don't need to copy them into each tool, and when a policy changes, the agent's access changes with it.

### Write your own middleware#

Supabase doesn't ship everything your handlers need to do on each request. Your own auth flow, the way you call another service, and telemetry are per-request logic too, and without middleware you copy them from handler to handler.defineMiddlewareturns each one into an entry you write once and use anywhere in a pipeline. It works like the ones we ship, because it's the same API we use.

You give it akeyand arunfunction.runtakes your config and returns the function that handles each request, and that function returns an object with your key. Here's one that adds a request ID:

[翻译失败，原文如下]

The type arguments are the key, the config, what the middleware needs from earlier middleware, and what it adds toctx. The types catch mistakes before you ship, and a mistake in per-request logic is easy to ship and slow to find. A duplicate key fails to compile, and so does a middleware placed before the one it needs. These checks are type-level, so they need TypeScript 5.4 or newer. Plain JavaScript gets the same runtime behavior without them.

An example custom middleware would be to extract the org ID from the caller's JWT.

### Share your middleware across projects as a package#

Your logic isn't tied to one project either. Instead of copying a file into the next project, you publish your middleware as a package and install it. Logic in a package has a version, so when you change your auth flow or add telemetry, you publish a release instead of editing every repo.

For example,@supabase-labs/middleware-openfeatureis a vendor-neutral package that depends only on the engine and@openfeature/core. We wrote it outside the engine repo from theauthoring guide, with the samedefineMiddlewareas the rest.

## Get started#

Install the package, then try the MCP server example.

- Build an MCP server for your app with theBring your own MCP guide
- Write your own middleware
- Use it in a framework, or move off the framework adapters, with theframeworks guide
- Browse theAPI referenceand theGitHub repo

---

> 本文由AI自动翻译，原文链接：[Supabase Middleware: composable, reusable middleware for Web Fetch handlers](https://supabase.com/blog/supabase-middleware)
> 
> 翻译时间：2026-10-20 07:22
