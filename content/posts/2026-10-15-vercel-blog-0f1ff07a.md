---
title: MCP Events support in Vercel Connect is now in public beta - Vercel
title_original: MCP Events support in Vercel Connect is now in public beta - Vercel
date: '2026-10-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/mcp-events-support-in-vercel-connect-is-now-in-public-beta
author: ''
summary: '[翻译失败，原文如下]


  Vercel Connectnow supports MCP Events in public beta, allowing your apps and agents
  to subscribe to webhook events from compatible MCP se...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-26T07:41:41.261867'
---

[翻译失败，原文如下]

Vercel Connectnow supports MCP Events in public beta, allowing your apps and agents to subscribe to webhook events from compatible MCP servers. Build agents for tasks like summarizing new messages, reviewing newly created issues, or responding to document feedback.

Connect creates subscriptions on the MCP server and renews them automatically as needed, verifying the server’s webhooks and forwarding events to your application using authenticated delivery.

You can use the Connect SDK to subscribe to MCP events:

```
1import { experimental_subscribe } from '@vercel/connect/mcp';234export async function subscribeToIssues(idempotencyKey: string) {5  return experimental_subscribe('oauth/issues', {6    tokenParams: { subject: { type: 'app' } },7    name: 'issue.created',8    arguments: { project_id: 'ABC' },9    destination: { path: '/hooks' },10    ttlMs: 24 * 60 * 60 * 1000,11    idempotencyKey,12  });13}
```

Requesting a 24-hour subscription to issue events

At your delivery endpoint, use the SDK to verify that each delivery came from Connect before acknowledging receipt:

```
1import { experimental_verifyMcpEvent } from '@vercel/connect/mcp';2
3export async function POST(request: Request) {4  await experimental_verifyMcpEvent(request, { path: '/hooks' });5  return new Response(null, { status: 204 });6}
```

Verifying incoming deliveries in a Next.js route

You can also exposeAI SDKevent discovery and subscription APIs as agent tools, using Connect’s MCP Events adapter to manage subscriptions.

Ineve, enabling events on an MCP connection gives agents tools to discover the server’s events and use Connect to create, inspect, or stop subscriptions.

Read theMCP Events docsandVercel Connect quickstartfor SDK setup and authentication.

---

> 本文由AI自动翻译，原文链接：[MCP Events support in Vercel Connect is now in public beta - Vercel](https://vercel.com/changelog/mcp-events-support-in-vercel-connect-is-now-in-public-beta)
> 
> 翻译时间：2026-10-26 07:41
