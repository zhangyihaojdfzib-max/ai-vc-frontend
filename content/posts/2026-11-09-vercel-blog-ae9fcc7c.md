---
title: Workflow SDK now writes over WebSockets on Vercel - Vercel
title_original: Workflow SDK now writes over WebSockets on Vercel - Vercel
date: '2026-11-09'
source: Vercel Blog
source_url: https://vercel.com/changelog/workflow-writes-now-use-websockets-on-vercel
author: ''
summary: '[翻译失败，原文如下]


  TheWorkflow SDKnow sends event writes and stream writes toVercel Workflowsover a
  WebSocket by default, replacing one HTTP request per wri...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-16T08:50:35.182333'
---

[翻译失败，原文如下]

TheWorkflow SDKnow sends event writes and stream writes toVercel Workflowsover a WebSocket by default, replacing one HTTP request per write, or per write group for streams. No code change is needed beyond upgrading toworkflow@5.2.0or later.

Once you deploy the upgrade, new runs use it. In-flight runs finish on the deployment they started on.

```
1npm install workflow@latest
```

Existing streaming code works as is. A step that writes a burst of chunks, like AI tokens, sends them over the WebSocket once it opens:

```
1import { getWritable } from "workflow";2
3async function streamChunks(chunks: string[]) {4  "use step";5  const writer = getWritable<string>().getWriter();6  for (const chunk of chunks) {7    await writer.write(chunk);8  }9  writer.releaseLock();10}11
12export async function streamingWorkflow(chunks: string[]) {13  "use workflow";14  await streamChunks(chunks);15}
```

### Copy link to headingStreams keep pace with AI output

In abenchmarkreplaying an AI agent's token stream, v5.2.0, which writes streams over a WebSocket by default, delivered the full response 4.2× faster than v4.8.12, with no chunk delayed over a second.

### Copy link to headingFewer HTTP requests for event writes

Every step start and completion is an event write, now sent over the WebSocket, so workflows with many steps make fewer HTTP requests. The added efficiency also improves performance and reduces costs. The queue handler opens the connection for every delivery.

## Copy link to headingGet started

Read theVercel World documentationto get started. If you're on 4.x, start with theupgrade guide, since v5 is a major release.

## Reference Architecture

Choose a stack and work through the decisions behind it, with curated documentation, guides, templates, and courses to help you build.

- Agent stack:Build and operate agents with models, tools, and durable workflows.
- Web applications:Choose rendering, data, authentication, and caching approaches.
- Backends:Choose a runtime, connect services, and run background work.

Browse all stacks

## Build with prompts

Build an app, extend an agent, or improve your project with ready-to-use prompts for your coding agent.

Browse the prompt library·Read the Markdown index

---

> 本文由AI自动翻译，原文链接：[Workflow SDK now writes over WebSockets on Vercel - Vercel](https://vercel.com/changelog/workflow-writes-now-use-websockets-on-vercel)
> 
> 翻译时间：2026-11-16 08:50
