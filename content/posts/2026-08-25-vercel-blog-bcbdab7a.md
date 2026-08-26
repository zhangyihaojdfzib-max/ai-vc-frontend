---
title: Vercel Connect is now generally available - Vercel
title_original: Vercel Connect is now generally available - Vercel
date: '2026-08-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-connect-ga
author: ''
summary: '[翻译失败，原文如下]


  Vercel Connectis now generally available on all plans and inv0. Instead of storing
  long-lived provider secrets, your code requests short-...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:11:35.153749'
---

[翻译失败，原文如下]

Vercel Connectis now generally available on all plans and inv0. Instead of storing long-lived provider secrets, your code requests short-lived, scoped tokens at runtime. Deployments authenticate with their existing Vercel OIDC identity. Each token is scoped to the task, refreshed automatically, and expires on its own.

![Connect to 100+ services through secure, scoped tokens](/images/posts/daf57794399a.jpg)

![Connect to 100+ services through secure, scoped tokens](/images/posts/14ec08e1c4c8.jpg)

## Copy link to headingAny service with one command

Register a connectoronce from the CLI. Pass the service name and the CLI pre-populates the brand name, icon, auth type, and MCP or discovery URL, then prompts for any credentials the service requires:

```
vercel connect create slack --name acme-slack
```

Create a Slack connector named acme-slack

Connect ships with100+ preset connectorsfor tools likeNotionandWorkday, managed connectors forSlack,GitHub,Linear,Salesforce,Snowflake, andMicrosoft, plus generic OAuth, API key authentication, and MCP servers.

## Copy link to headingTokens at runtime, not secrets at rest

Request a token only when your code needs one, withgetToken:

```
import { getToken } from '@vercel/connect';
const token = await getToken('slack/acme-slack', {  subject: { type: 'app' },});
```

Request an app-level Slack token

Switch thesubjectfrom the app to a named user and the token acts on that user's behalf, triggering the authorization flow when consent is needed.

## Copy link to headingAccess your team can inspect and prove

New at GA:

- Fine-grained RBACcontrols who can create and manage connectors
- Audit logsrecord authorization and connector activity
- Token and trigger observabilityshows how tokens are used across projects

Fine-grained RBACcontrols who can create and manage connectors

Audit logsrecord authorization and connector activity

Token and trigger observabilityshows how tokens are used across projects

Together with per-environment attachment, includingCustom Environments, and one-command revocation, external access becomes something your team can inspect, prove, and cut off in seconds.

## Copy link to headingTriggers without stored webhook secrets

Triggers deliver provider events to your app without a stored secret. Vercel Connect verifies signatures server-side, re-attests each event using an OIDC identity, and forwards the event to your project, even when Deployment Protection is enabled.

Connect also manages private keys and the full credential lifecycle, so you get standards-compliant OAuth without building the infrastructure yourself.

## Copy link to headingWorks with your stack

Connect works wherever your functions run and is supported inv0, eve, and Chat SDK. Adapters are available for the auth libraries and agent tooling you already use:

- Better Auth:@vercel/connect/betterauth
- Auth.js:@vercel/connect/authjs
- AI SDK:@vercel/connect/ai-sdk
- MCP clients:@vercel/connect/mcp
- eve:@vercel/connect/eve
- Chat SDK:@vercel/connect/chat

Better Auth:@vercel/connect/betterauth

Auth.js:@vercel/connect/authjs

AI SDK:@vercel/connect/ai-sdk

MCP clients:@vercel/connect/mcp

eve:@vercel/connect/eve

Chat SDK:@vercel/connect/chat

### Copy link to headingSecurely connect your AI SDK agents to MCP servers

The AI SDK adapter authenticates MCP clients with tokens minted at runtime. In this example, the agent gets read-only Linear access issued for a single user, so downstream actions carry that user's identity:

```
import { createMCPClient } from '@ai-sdk/mcp';import { connectAuthProvider } from '@vercel/connect/ai-sdk';import { streamText } from 'ai';
const mcpClient = await createMCPClient({  transport: {    type: 'http',    url: 'https://mcp.linear.app',    authProvider: connectAuthProvider('oauth/linear', {      subject: { type: 'user', id: userId },      scopes: ['read'],    }),  },});
const result = await streamText({  model: 'openai/gpt-5.6-sol',  tools: await mcpClient.tools(),  prompt,});
```

### Copy link to headingGive your GitHub agents only the access they need

GitHub Tools, our open source tool layer for GitHub agents, plugs into eve through Connect via aneve extension. Presets likecode-reviewmap to Connect scopes automatically, so tokens carry only the permissions the toolset needs:

```
import githubExtension from '@github-tools/eve-extension';
export default githubExtension({  connector: 'github/my-connector',  preset: 'code-review',});
```

## Copy link to headingPricing and availability

Vercel Connect is available on all plans, with pricing based on token requests and trigger events. Hobby includes 500 token requests and 1,000 triggers per month at no additional cost. Pro is billed at $3 per 1,000 token requests and $0.95 per 1,000 triggers, with custom pricing on Enterprise.

## Copy link to headingGet started

- Deploy asoftware factory template with Vercel Connectorbrowse the source
- Follow thequickstart guidein the documentation or read thelaunch blog post
- Hand the prompt below to your coding agent to set up Vercel Connect:

Deploy asoftware factory template with Vercel Connectorbrowse the source

Follow thequickstart guidein the documentation or read thelaunch blog post

Hand the prompt below to your coding agent to set up Vercel Connect:

Help me set up Vercel Connect in this application.

Install the Vercel Connect skill first with `npx skills add vercel/vercel-plugin --skill vercel-connect` and follow it.

Read vercel.com/docs/connect.md for anything the skill does not cover. Link the project (`vercel link`) and pull a local OIDC token (`vercel env pull`). Ask me which provider to connect, create a connector for it, and attach it to this project. Then install @vercel/connect and request a token at runtime with getToken.

Make a test call against the provider to confirm it works.

If you have any questions or get stuck, don't assume the answer, just ask me.

## Contributors

Joe Sadowski,Bhrigu Srivastava,Allen Zhou,Raghav Agarwal,Yasoob Rasheed,Tony Pan,Caleb Boyd,Pranav Kanchi

---

> 本文由AI自动翻译，原文链接：[Vercel Connect is now generally available - Vercel](https://vercel.com/changelog/vercel-connect-ga)
> 
> 翻译时间：2026-08-26 03:11
