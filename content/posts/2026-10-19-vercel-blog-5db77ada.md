---
title: Making every harness durable
title_original: Making every harness durable
date: '2026-10-19'
source: Vercel Blog
source_url: https://vercel.com/blog/making-every-harness-durable
author: ''
summary: '[翻译失败，原文如下]


  Developers are familiar with running coding agents locally through harnesses like
  Pi, Claude Code, and others. They are reliable daily dr...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:23.394601'
---

[翻译失败，原文如下]

Developers are familiar with running coding agents locally through harnesses like Pi, Claude Code, and others. They are reliable daily drivers for generating code, but keeping agents running around the clock requires your computer to be on and awake, which led to the laptop lid memes and Mac mini demand spike.

software engineers before vs after agents

![Image](/images/posts/fd645b5b4bf7.jpg)

![Image](/images/posts/c26e5b86f602.jpg)

#### Copy link to headingRunning harnesses in the cloud

Harness workloads are moving to the cloud. Individual developers are deploying always-on coding agent workflows, projects like OpenWork and HanaAgent use open-source harnesses as the engines behind the apps, and engineers are building their own harness products.

These harnesses are designed for long-lived processes that keep the session in memory, and agent tasks commonly run for minutes or hours. Locally, a harness has direct, continuous access to the workspace and session history on the same disk, so resuming interrupted work only requires a simple prompt.

In the cloud, you can replicate that setup with a VM and persistent storage, but the VM doesn't automatically record which model and tool calls completed or resume interrupted turns after a crash. A failed turn or network error means lost work.

Also, not every agent task executed through a harness needs a sandbox. Database queries and API calls can run securely in functions, and that also means required credentials never have to enter the sandbox.

### Copy link to headingMaking every harness durable

We builteveandfxto run durably in the cloud out of the box, and today we are introducingdurable-harness, which extends that durability to any harness, includingPi,OpenCode,Codex, andClaude Code. It uses the same machinery that powersWorkflow SDKto survive crashes and function timeouts.

Withdurable-harness, you can:

- Run any of these harnesses durably on Vercel
- Self-host a harness with your own Postgres instance
- Make your local harness workflow durable
- Build your own durable harness

Run any of these harnesses durably on Vercel

Self-host a harness with your own Postgres instance

Make your local harness workflow durable

Build your own durable harness

## Copy link to headingSessions that survive a crash mid-turn

Take the example ofa coding agent adding a pricing page to an existing app. The agent reads the existing page, writes a new one, opens a pull request, and waits for CI to finish before reporting back.

What happens if its function times out while CI is still running?

Kill the function or drop the connection in the demo below to compare how the two agents recover and which work is repeated.

Without durability, the agent stops work until it is manually restarted, and completed work is repeated unnecessarily.

Withdurable-harness, a new function reads completed results from the log and resumes the turn.If the browser disconnects, the agent keeps running, and reconnecting catches up from the log.

## Copy link to headingLogs and queues

durable-harnessis the newest package in our open source portfolio. It’s a set of adapters and utilities that let the harnesses you already use keep their sessions in aWorld, the Workflow SDK’s durable backend.

It writes each step of a turn to a durable log. Before a model call or tool call runs, it records an intent, and when the call finishes, it records the outcome. The turn itself is backstopped with a queue message, so if its function dies, the queue hands the turn to a new function that reads the log and continues where it left off.

After a crash, the log says what finished, what was running, and what never started:

- Completed calls never run again because their results are read from the log, so you’re never billed twice for a finished model call’s tokens.
- Models remember their previous calls rather than repeating them.
- Interrupted tools markedreplay: 'safe'run again. Any other tool comes back to the model as possibly run, and the model decides whether to check.

Completed calls never run again because their results are read from the log, so you’re never billed twice for a finished model call’s tokens.

Models remember their previous calls rather than repeating them.

Interrupted tools markedreplay: 'safe'run again. Any other tool comes back to the model as possibly run, and the model decides whether to check.

Harnesses that keep their own session files, like Claude Code's transcript, Codex's rollout, and OpenCode's event store, have every record mirrored into the log, so a new function or Sandbox rebuilds them from it.

## Copy link to headingPick your harness

fxandeveare durable on their own. For the rest,durable-harnessadds durability from the outside, without changing the harness.

For the full setup guide for each harness, check thedocs.

## Copy link to headingRuns everywhere

Durable agents need a log of each step, a way to resume a turn when its process dies, and a stream for whoever is watching.

Workflow SDK ships all three behind one interface, aWorld.

```
import type { Queue, Storage, Streamer } from '@workflow/world'interface World extends Storage, Queue, Streamer {}
```

A World is the log, the backstop and the stream behind one interface.

durable-harnesswrites to that interface, so you can move the same agent from one World to another without changing its code:

- On Vercel, it uses theVercel World.
- In development, it usesfiles on your machine.
- On your own servers, it usesPostgres, MongoDB, Redis, or Turso.

On Vercel, it uses theVercel World.

In development, it usesfiles on your machine.

On your own servers, it usesPostgres, MongoDB, Redis, or Turso.

Two variables move every agent usingdurable-harnessto Postgres.

```
WORKFLOW_TARGET_WORLD="@workflow/world-postgres"WORKFLOW_POSTGRES_URL="postgres://user:password@host:5432/database"
```

Redirects durable-harness to use the Postgres World for durability.

For more control, such as setting a namespace or recovering sessions when your server starts, create the World in code and pass it to your agent:

Check theself-hosting docsfor more details.

## Copy link to headingSee every session in Agent Runs

Agent Runson Vercel shows the trace for every session, including each model call and tool call. Turns that resumed after a crash appear in the same trace, so you can see exactly where a turn stopped and picked back up.

A Pi session in the Agent Runs tab with an interrupted and retried model call.

## Copy link to headingTools

An agent has only the tools you give it, and they run in your function. Each tool says what should happen if a crash interrupts it. A'safe'tool, such as a lookup, can run again. A'never'tool, such as a refund, never runs twice: the model is told the call may have happened, so it can check before it tries again.

Here’s how the coding agent from the demo above might define its tools:

- A tool that reads a file or checks CI status is marked as'safe'so it can run again automatically.
- A tool that posts a PR comment is marked as'never'so that comments aren't posted twice.

A tool that reads a file or checks CI status is marked as'safe'so it can run again automatically.

A tool that posts a PR comment is marked as'never'so that comments aren't posted twice.

The following example defines a tool for each policy using the example of an agent processing a refund:

[翻译失败，原文如下]

```
1import { pi } from 'durable-harness/pi';2import type { HostTool } from 'durable-harness';3import { getOrder, refundOrder } from './orders'; 4
5const tools: HostTool[] = [6  {7    name: 'get_order',8    description: 'Looks up an order',9    replay: 'safe', 10    inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] },11    execute: async ({ id }) => JSON.stringify(await getOrder(id)),12  },13  {14    name: 'refund_order',15    description: 'Refunds an order',16    replay: 'never', 17    inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] },18    execute: async ({ id }) => JSON.stringify(await refundOrder(id)),19  },20];21
22export const agent = pi({ model: 'anthropic/claude-sonnet-5.5', tools });
```

A lookup can run again after a crash, and a refund never runs twice.

For each harness’s built-in tools, like its shell and file editing, read on.

## Copy link to headingFiles

When a harness needs a shell and files, it’s not safe to run them directly on a shared serverless function host. Many sessions can share the same function, and its filesystemisn’t guaranteed to persist between invocations.

To address this,durable-harnessgives you a few options:

- virtual()keeps the files in the session’s log, with a bash-compatible shell that can’t reach your function’s files or the network. It suits short tasks and small workspaces without starting an entire sandbox.
- virtual({ durable: false })keeps the files in memory for scratch work and clears them at the end of every turn.
- sandbox()gives the session its ownVercel Sandbox, with/workspaceon aDrivethat outlives every sandbox and every function. It suits real projects and long-running work.

virtual()keeps the files in the session’s log, with a bash-compatible shell that can’t reach your function’s files or the network. It suits short tasks and small workspaces without starting an entire sandbox.

virtual({ durable: false })keeps the files in memory for scratch work and clears them at the end of every turn.

sandbox()gives the session its ownVercel Sandbox, with/workspaceon aDrivethat outlives every sandbox and every function. It suits real projects and long-running work.

Compare the three side by side in thedocs.

Each harness’s built-in tools run on the workspace you choose. With Pi,CodingToolsinstalls Pi’s ownread,write,edit, andbash, andvirtualEnv()orsandboxEnv()gives them a workspace:

```
1import { BACKGROUND_CONTEXT as ctx } from '@earendil-works/chord/context';2import { createRegistry, Harness, type Storage } from '@earendil-works/pi-durable';3import { CodingTools, gatewayModels, resumeWith, virtualEnv } from 'durable-harness/pi-durable';4
5const models = gatewayModels();6const registry = createRegistry();7registry.install(CodingTools); 8
910const env = virtualEnv();11
12export const open = resumeWith((storage: Storage) => Harness.open(storage, { models, registry, env }, ctx));
```

Gives Pi its coding tools on a virtual workspace or in a Vercel Sandbox.

For OpenCode, pass the workspace asworkspace, and for fx, pass it tofxTools(). Claude Code and Codex always run in a Vercel Sandbox, since they expect a real shell and filesystem, and aren’t safe for multi-tenant use. Their built-in tools work on the session’s Drive once you turn them on withbuiltins: true. Eachharness guidelists its built-in tools.

## Copy link to headingDocuments

Some state belongs with the session but isn’t part of the conversation, such as a to-do list, a plan, or a form the agent fills in. A document is typed JSON that lives in the session’s log, so it survives a crash and moves with the session.

Tools can edit documents throughio.docs, and each edit commits to the log alongside the tool’s result, so the document’s durable state stays consistent with the tool calls themselves:

```
1import { defineDoc, type HostTool } from 'durable-harness';2
3export const Todos = defineDoc<{ items: string[] }>({4  kind: 'app.todos',5  version: 1,6  initial: () => ({ items: [] }),7});8
9export const addTodo: HostTool<{ item: string }> = {10  name: 'add_todo',11  description: 'Adds a todo',12  replay: 'safe',13  inputSchema: { type: 'object', properties: { item: { type: 'string' } }, required: ['item'] },14  async execute({ item }, io) {15    const todos = io.docs!.update(Todos, (draft) => {16      draft.items.push(item);17    });18    return `${todos.items.length} todos`;19  },20};
```

Defines a to-do list document and a tool that adds to it.

Your app can read and edit the same document without a database of its own, and the chat route can even stream every change to your UI:

```
1import { agent } from '@/lib/agent';2import { Todos } from '@/lib/todos';3
45const { value } = await agent.sessions.doc(sessionId, Todos);6
78export const { GET, POST } = agent.chatRoute({ authorize, docs: [Todos] }); 
```

Reads the to-do list from your app and streams its changes to your UI.

In fact, thevirtual()workspace from earlier is built on documents: its file tree is a document in the session’s log, and each tool call’s changes commit with its result.

Learn more abouttools, files, and documentsand how tokeep your agent secure.

## Copy link to headingWrapping up

Developers choose a harness for the choices it makes about prompts, tools, and context. How it survives a crash shouldn’t be one of them. Withdurable-harness, a turn that loses its function partway through continues from the log on a new one, without a manual retry and without repeating what already finished. Self-hosting and portability work out of the box by building on top of the Workflow SDK’s World interface.

durable-harnessisopen source on GitHub.

Make your harness durable

Adapters that make Pi, OpenCode, Claude Code, and Codex durable on Vercel, Postgres, or your laptop.

Read the docs

## Contributors

Ben Sabic,Esteban Suárez,Pranit Sharma

---

> 本文由AI自动翻译，原文链接：[Making every harness durable](https://vercel.com/blog/making-every-harness-durable)
> 
> 翻译时间：2026-10-21 06:58
