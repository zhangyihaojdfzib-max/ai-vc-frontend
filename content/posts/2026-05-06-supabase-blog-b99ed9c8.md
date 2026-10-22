---
title: Introducing @supabase/server
title_original: Introducing @supabase/server
date: '2026-05-06'
source: Supabase Blog
source_url: https://supabase.com/blog/introducing-supabase-server
author: ''
summary: '[翻译失败，原文如下]


  Today we''re releasing@supabase/serverin public beta.


  This is a new package that handles auth verification, client setup, request context...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:56:06.636876'
---

[翻译失败，原文如下]

Today we're releasing@supabase/serverin public beta.

This is a new package that handles auth verification, client setup, request context, and common server-side boilerplate for you. It works acrossEdge Functions, Vercel Functions, Cloudflare Workers, Hono and Bun.

We anonymously analyzed 25,000 deployed Edge Functions and saw the same pattern everywhere: developers were rebuilding the same setup code over and over just to get to their actual business logic.

Most functions needed to:

- Create a Supabase client withSUPABASE_ANON_KEY
- Create another admin client withSUPABASE_SERVICE_ROLE_KEYthat can bypassRow Level Security
- Verify the JWT
- Parse claims
- Handle CORS
- Wire up auth context
- Copy/paste the same_shared/*.tsfiles between functions

With@supabase/serveryou just declare who can call your endpoint and get a fully initialized context back:

- User-scoped Supabase client
- Admin client with service role access
- Verified user identity
- JWT claims
- Built-in request/auth helpers

Note thatexport default { fetch }is equivalent toDeno.serve(...). Both define a request handler. We useexport defaultthroughout this post because it works across Edge Functions, Workers, and Bun. If you preferDeno.serve, you can keep using it — it'sstill supportedon Edge Functions.

## How it works#

At the core of@supabase/serveris theSupabaseContext: a request context that includes everything most Edge Functions need, already configured for you.

That includes:

- A user-scoped Supabase client
- An admin client with service role access
- Verified user identity
- JWT claims
- Auth metadata

@supabase/servergives you multiple ways to get aSupabaseContext. The most common iswithSupabase, a wrapper that handles auth, client creation, and CORS before your handler runs:

If you need more control over error handling and responses, you can also callcreateSupabaseContextdirectly:

Both approaches give you the sameSupabaseContext. No shared utility files. No environment variable management. No manual JWT verification.

## What's in the context#

EverywithSupabasehandler receives actxobject with two pre-configured clients:

ctx.supabase— a user-scoped client that automatically respects RLS policiesctx.supabaseAdmin— an admin client using the service role for privileged operations

No manual client setup, JWT verification, or environment variable wiring required.

The full context looks like this:

## Declarative access control#

With@supabase/server, authentication happens before your handler runs.

You declare who is allowed to call the endpoint, and the package handles verification automatically.

For example, this endpoint allows unauthenticated requests:

This endpoint requires a valid user JWT:

If the request does not include a valid user token, the request is rejected before your handler executes.

Here's all of the auth modes included in the package:

Your function's security model is visible in one line.

## Adopting new auth keys without the boilerplate#

Last year we improved project security withasymmetric JWT Signing Keysandnew API keys. Better security for every project, but migrating existing functions was hard.

You had to installjose, configure a JWKS endpoint, build your own auth middleware, expose new secrets, and update every function individually.

We fixed it.@supabase/serverhandles new key validation and JWT verification internally. You adopt the package and the new security model comes with it. Nojose. No JWKS configuration. No manual secret setup.

Now you get support for the new auth keys without manual JWT verification. Delete your shared utility files and focus on business logic.

## Same code, every runtime#

withSupabasereturns a standard(Request) => Promise<Response>handler. It works with any runtime that supports the Web API pattern.

Edge Functions, Vercel Functions, and Cloudflare Workers:

On Edge Functions, declare the dependency indeno.jsonto import@supabase/serverfromnpm:@supabase/server.

Hono (with the included adapter):

## Composable primitives#

Most developers don't need anything beyondwithSupabaseorcreateSupabaseContext. But you can use the underlying primitives directly.

These are useful when you need more control: multiple routes with different auth, custom response headers, or domain-specific wrappers like MCP servers.

Here's an Edge Function with per-route auth:

These are the same primitives that powerwithSupabase. Teams building MCP servers, custom middleware, or framework adapters can compose them into their own patterns.

## One pattern for humans and AI agents#

We designed@supabase/serverwith agentic development in mind. Every function follows the same structure: declare access, receive context, write logic.

During internal testing, Claude Code migrated an entire project's Edge Functions to@supabase/serverin a single prompt. That included adopting new API keys, removing shared utility files, and switching every function towithSupabase. All functions worked on the first run.

When every function looks the same, agents produce correct code from a single example.

Does this replace@supabase/ssr?

No.@supabase/ssrhandles cookie-based session management for frameworks like Next.js and SvelteKit.@supabase/serverhandles stateless, header-based auth for Edge Functions, Workers, and other backend runtimes. The two packages coexist and are not replacements for each other. Deeper integration with@supabase/ssris on the roadmap.

If you would like to adopt the DX that this package provides, check ourSSR frameworksdocumentation for implementation references.

Which runtimes does this support?

Any runtime or platform that supports the standardRequest/ResponseWeb API.withSupabasereturns a standard(Request) => Promise<Response>handler, so it works on Supabase Edge Functions, Vercel Functions, Cloudflare Workers, Bun, Deno and more.

Is Hono the only supported framework?

No. Hono was the first framework adapter we shipped, and we have already merged a community PR for the H3 adapter. We expect to accept more community-contributed adapters.

See more in our adaptersdocumentation.

Where is the documentation?

The package ships with full documentation in theGitHub repo. We're also working on adding guides to theSupabase docs.

What about environment variables?

On the Supabase platform and Local Development (CLI), your Edge Functions will receive the required environment variables to work out of the box (SUPABASE_PUBLISHABLE_KEYS,SUPABASE_SECRET_KEYS,SUPABASE_JWKS).

In local development or self-hosted environments, use the same plural form:SUPABASE_PUBLISHABLE_KEYSinstead ofSUPABASE_ANON_KEY,SUPABASE_SECRET_KEYSinstead ofSUPABASE_SERVICE_ROLE_KEY.

Check out theenvironment variables documentationfor more details.

How can I leave feedback?

Open an issue on theGitHub repoor join the conversation inDiscord.

## Get started#

Install the package and the AI skill:

The skill gives Claude Code, Codex, Cursor and any agentic coding tool full context about the API surface, patterns, and migration paths. From there, you can prompt your way through most tasks.

Scaffold a new REST API with Hono:

Add a protected Edge Function with admin operations:

Or write it by hand:

@supabase/serveris in public beta. We're looking for feedback on the API surface, the adapter patterns, and edge cases we haven't hit yet.

Check out theGitHub repoand thedocsand let us know what you build.

---

> 本文由AI自动翻译，原文链接：[Introducing @supabase/server](https://supabase.com/blog/introducing-supabase-server)
> 
> 翻译时间：2026-10-22 06:56
