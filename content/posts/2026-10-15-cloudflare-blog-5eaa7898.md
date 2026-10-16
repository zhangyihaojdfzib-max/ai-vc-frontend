---
title: Deploy with Void
title_original: Deploy with Void
date: '2026-10-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/deploy-with-void/
author: ''
summary: "[翻译失败，原文如下]\n\nVoidZero's tools such as Vite, Vitest, Oxc, and Rolldown\
  \ â\x80\x94 bundled in one toolchain asVite+Â â\x80\x94 have made frontend development\
  \ faster,..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:40:52.756327'
---

[翻译失败，原文如下]

VoidZero's tools such as Vite, Vitest, Oxc, and Rolldown â bundled in one toolchain asVite+Â â have made frontend development faster, but building full-stack applications requires more than just a tooling stack. These applications need server routes, databases, local development environments, and a fast and easy way to deploy ideas to production.

Weâre excited to open-source three new products that bring server routing, typed data access, and Cloudflare deployment into a unified Vite workflow.

- Void Platform:Â A shared deployment platform for teams to host Void apps on Cloudflare.
- Void SDK:Â A composable JavaScript SDK for building full-stack apps with Vite.
- Void CLI:Â A CLI for provisioning resources and deploying Vite apps to Cloudflare.

The CLI deploys apps built with the SDK to the Platform. All three products are open-sourced as a single JavaScript package and Vite plugin that you can install vianpm install void. WithVoid, you can build your server and client together, carry types from your database to the UI, and let Void automatically provision the Cloudflare resources that your app uses.

We originally set out to build a single, private platform for all users to deploy apps to. AfterVoidZero joined Cloudflare, we adjusted our direction to open-source the platform and allow anyone to install because we saw a growing need:companies want to encourage vibe-coded internal apps, but are concerned about security and do not want to give cloud access to every employee. Void addresses this problem.

## Void Platform: a cloud platform for your company

The Void Platform is fully open source and you can fork it and adapt it to your needs by integrating your company's systems, customize deployment workflows, build features for your customers, or make it work on other deployment platforms. Use the platform as it is, contribute improvements upstream, or fork it and build only the features you need. The open source code can be used out of the box or as a starting point.

As an admin of a Void Platform, you control access, set resource limits, inspect deployments and usage through the Void CLI or admin dashboard, and provide guardrails so everyone else can ship serious and vibe coded apps to the same shared platform.

By installing a Void Platform, your team or customers have a shared deployment environment in your Cloudflare account on top ofWorkers for Platforms. Void Platform enables:

1. Faster prototyping. Your team can quickly build prototypes, deploy them, and share working apps for feedback, without setting up a separate Cloudflare account or provisioning resources for every project. This reduces the time to ship internal apps from days/weeks to minutes.
2. Non-technical teams building. This workflow also lets teammates who do not normally write code work with coding agents to build and share their own apps. A designer can create an interactive prototype, or an operations teammate can build an internal dashboard, then deploy it to the same platform. All with the right security measures in place.

To self-host a Void platform, you need:

- A Cloudflare account with Workers for Platforms and R2 enabled
- A PostgreSQL database
- An account with your chosen login provider
- A domain for your apps

Then install Void as a cloud platform by running a single command:

Once your platform is set up, approved users can connect to it via the Void CLI for deployment.

```
void connect https://api.orange-company.dev
```

A user builds their app using the Void SDK, which is what powers Void Platform benefits like authentication, framework detection, resource provisioning, and more. In other words, Void Platform only works because of the accompanying SDK and CLI.

## Void SDK: zero-config infrastructure

VoidÂ turns a Vite app into a full-stack Cloudflare Workers app. You or your agents can write code and Void will automatically infer resource bindings and provision resources such as databases, queues, or AI bindings during deployment.

To get started, add Void as a Vite plugin:

```
import { defineConfig } from "vite";
import { voidPlugin } from "void";
import { voidReact } from "@void/react/plugin";

export default defineConfig({
  plugins: [voidPlugin(), voidReact()],
});
```

The Void SDK ships with adapters for popular JavaScript UI frameworks such as React and Vue, provides file-based API routing, pre-rendering, caching, islands, and end-to-end type safety from the database to your UI.

All of Voidâs features are optional and composable. Void integrates with existing application frameworks such as Vinext, React Router, SvelteKit, Nuxt, TanStack Start, and Astro. You can use those frameworks for routing and rendering, while Void handles resource APIs using Hono, migrations, deployment, and authentication with Better Auth.

Let's take a look at building a server-rendered page, with types inferred from the database query through to the client:

```
// pages/blog.server.ts
import { defineHandler, type InferProps } from 'void';
import { db } from 'void/db';
import { posts } from '@schema';

export const loader = defineHandler(async () => ({
  posts: await db.select().from(posts),
}));

export type Props = InferProps<typeof loader>;
```

```
// pages/blog.tsx
export default function Blog({ posts }: Props) {
  return (
    <ul>
      {posts.map((post) => <li key={post.id}>{post.title}</li>)}
    </ul>
  );
}
```

By importingvoid/db, Void provides a local database to your app during development and makesvoid deployÂ provision D1 automatically for you in production. This also works for using AI through Cloudflareâs AI Gateway: just by importingvoid/ai, everything is set up automatically for you.

```
// routes/api/decide.ts
import { defineHandler } from 'void';
import { ai } from 'void/ai';

export const POST = defineHandler(async (c) => {
  const { question } = await c.req.json();
  const result = await ai.run('@cf/cloudflare/clef', {
    model: 'clef',
    state: {},
    questions: {
      decision: { type: 'noul', instructions: question },
    },
  });
  const probability = result.answers.decision.noul;
  return c.json({
    answer: probability >= 0.5 ? 'yes' : 'no',
    probability,
  });
});
```

Void's React router is built forAsync React, using transitions and Suspense to enable responsive navigation across screens. When you pair this router with a modern data framework such asfateÂ and UI libraries such asAstryx, you can coordinate navigation, data fetching and mutations through React's transitions, as well as actions and optimistic updates across your entire application. Together, these pieces let you build apps that feel synchronous on fast networks, gracefully fall back on slower ones, and keep interactions responsive during expensive rendering updates.

If a user does not need Void Platformâs team management features, they can use their own Cloudflare account. Void SDK alsodeploys to Cloudflare directly.

## Void CLI: one deployment command

The Void CLI is the main interface for Void. The CLI manages the platform and deploys the app. It's built on top of the newcf CLIÂ and works well with agents.

With the Void CLI, you can ask your agent to debug failing requests, read deployment logs, analyze how your app is performing, or have them take care of the full lifecycle by deploying a finished app for you. Â

Once your app is ready to deploy to Cloudflare, you can run:

The first time you runvoid deploy, the CLI will prompt you to log into your Cloudflare account. Void builds your app using Vite, applies migrations, automatically provisions resources, and deploys to Cloudflare or a Void Platform. It can be used to handle the full lifecycle of your project such as building, deploying, and managing your resources and projects, for example:

Similar to how the CLI, and an agent by extension, can manage the entire lifecycle of a Void app, you can also use the CLI to manage a Void Platform:

[翻译失败，原文如下]

- Manage users, project access, and resources
- Inspect deployments, logs, and rollbacks
- Monitor platform health and usage

## Connect with us

VoidZeroâs mission is to make JavaScript developers more productive than ever before. We brought Vite, Rolldown, Oxlint, Oxfmt, and Vitest together inVite+Â for development, bundling, code quality, and testing. Void extends that stack to full-stack application development, letting you and your agents build, test, and deploy entire applications.

Weâve been using the Void SDK, CLI, and Platform in production at VoidZero for the past several months and we are excited to see what you'll build with Void. Please share your feedback with us:

- Discord:Step into the Void community Discord serverÂ for real-time discussions
- GitHub:Star the repo, start discussions, and report issues
- Deploy an app with Void:Quick Start Guide
- X / Bluesky:Follow VoidZero for updates on XÂ or onBluesky

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Deploy with Void](https://blog.cloudflare.com/deploy-with-void/)
> 
> 翻译时间：2026-10-16 06:40
