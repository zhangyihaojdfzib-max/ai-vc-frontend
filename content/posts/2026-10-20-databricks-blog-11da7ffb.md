---
title: Introducing Agent Memory on Databricks
title_original: Introducing Agent Memory on Databricks
date: '2026-10-20'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-agent-memory-databricks
author: ''
summary: '[翻译失败，原文如下]


  Today we''re introducing agent memory on Agent Bricks, Databricks'' agent developer
  platform. Agent memory improves agent quality while dec...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:27.802821'
---

[翻译失败，原文如下]

Today we're introducing agent memory on Agent Bricks, Databricks' agent developer platform. Agent memory improves agent quality while decreasing costs and latency by storing critical facts, preferences, and workflows that an agent should remember. It's available in Beta today, runs on Lakebase for high reliability and low latency, and is built on Databricks' latest memory research.

Without memory, agents risk rediscovering key facts, forgetting user preferences, and repeat mistakes it was already corrected on. In response, many developers are rolling their own memory solutions, but run into numerous design questions - for example, where should memories be stored? How should memories get synthesized? And once generated, how should they be retrieved?

To address this, Databricks Agent Memory is built on the MemCurrent architecture, pioneered byDatabricks Research. MemCurrent combines three access patterns: plugins to log and load context automatically, tools the agent calls on demand, and an offline dreaming pipeline that consolidates memory in the background. All of this is served with extremely low latency using Lakebase. In our internal benchmarks, implementing this memory architecture tripled agent pass rate on real enterprise tasks while using 31% fewer tokens.

Agent Memory joins the rest of Agent Bricks, including agent hosting, Databricks Sandbox, Unity Gateway, pre-built MCP servers, and tracing and evaluation, providing developers all the infrastructure capabilities needed to build production agents.

## Problem: stateless agents pay for the same context twice

Two problems show up as soon as an agent moves from a demo to daily use.

- Costs climb with every rediscovery.A stateless agent re-derives what it figured out yesterday: which table holds usage data, what an internal acronym means, which join actually works. In one real session from our research, an agent took 11 tool calls, 8 subagents, and nearly six minutes to answer a question about one product's top customers. The next day, it would have done all of that again.
- Agents never get personal.A user states a preference, corrects a mistake, or explains how their team defines a metric, and the agent forgets it when the session ends. Either the user repeats themselves, or the agent repeats the mistake.

Agent developers, and the platform teams that run their agents, have two common workarounds. Each one trades one problem for another:

- Replaying the full history into contextworks until histories get long. On open-source memory benchmarks, full context used about 12x more input tokens per question than a well-designed memory at the same accuracy, and on the longest histories it scoredworse, because irrelevant turns confused the agent.
- Building memory yourselfon object storage or a vector database means owning extraction, deduplication, retrieval, and access control. Memories go stale, contradictory facts pile up, and no one can tell which memory caused a bad answer.

What teams need is memory that makes agents cheaper and more personal at the same time, without standing up another system to get it.

## How Agent Memory on Databricks works

![](/images/posts/3fcc8e98c663.png)

Figure 1. Agent Memory on Agent Bricks. The agent appends each turn to managed sessions, recalls and saves memories directly, and a memory pipeline distills sessions into long-term memory in the background.

Agent Memory has three parts:

- Managed sessionsrecord each conversation as an ordered history of messages, tool calls, and results, in your framework's native format.
- Managed memorykeeps what's worth remembering: profile, preferences, domain knowledge, and workflows. At the start of a session, the agent loads an index of what is known in memory. During the session, it finds details with hybrid keyword and semantic search.
- Memory pipelinesdistill sessions into memory in the background, on demand or on a regular basis in the background. They extract durable facts and preferences, remove duplicates, and replace facts that newer conversations contradict.

Everything runs on Lakebase, Databricks' serverless Postgres, provisioned in your workspace and operated by Databricks. This ensures that storing and retrieving memories is lightning fast, and that your stores can scale along with your agent traffic.

## Built on our memory research

Agent Memory is a production implementation of MemCurrent, the memory system described inMemCurrent: Designing Memory for Enterprise Agents. Our researchers’ central finding is that memory works best in two layers: a raw record of what happened, and a distilled record of what's worth remembering, kept current by a background process rather than written ad hoc by the agent mid-task.

Built that way, memory improved quality and efficiency at the same time. Agents passed about three times as many tasks as agents without memory, finished faster, and used fewer tokens. The same infrastructure already powers memory in Genie, Databricks' natural-language experience for business users.

![](/images/posts/6bdf658360d5.png)

Figure 2. Agents with and without memory on Databricks' internal memory benchmark of enterprise data tasks. Source: MemCurrent research.

## What changes for your agents

- Lower cost per task.Agents skip work they've already done. In the example above, once the workflow was saved to memory, the agent answered a related follow-up question in 2 tool calls and 41 seconds, down from 11 tool calls and nearly six minutes.
- Personalization that persists.Preferences, corrections, and team-specific definitions carry across sessions, scoped to each user, so people stop repeating themselves.
- Mistakes that stay fixed.Agents remember their mistakes, and can avoid making the same mistake twice - saving valuable time and tokens.
- Memory you own and control.Sessions and memories live in your Lakebase project, independent of any single agent framework. Developers can read, export, and delete the entries an agent keeps about each user, and give a memory pipeline instructions that steer what it retains, such as "keep durable customer preferences; ignore one-off debugging notes."
- One platform for the whole loop.The same agent uses models through Unity Gateway, deploys with the Agent Bricks CLI, and is traced and evaluated with Agent Bricks' tracing, with memory included.

## Get started

None of this requires new infrastructure on your side. The Agent Bricks CLI can help you deploy an agent with memory and sessions in minutes.

From then on, your agent's next conversation with each user starts with what it learned from the previous ones. For more info, see thequickstartto create a new agent with memory, or ourtutorialfor adding memory to an existing agent.

Agent Memory is one part of Agent Bricks, Databricks' agent developer platform for building, running, and improving custom agents at scale, with any model, framework, or harness.Explore Agent Bricksto see the rest of the platform.

## More resources

- Build a stateful agent in under 10 minuteswith theAgent Bricks CLI documentation.
- Add memory and sessions to an existing agentwith theagent memory and sessions documentation.
- Read the researchbehind it inMemCurrent: Designing Memory for Enterprise Agents.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Introducing Agent Memory on Databricks](https://www.databricks.com/blog/introducing-agent-memory-databricks)
> 
> 翻译时间：2026-10-21 06:58
