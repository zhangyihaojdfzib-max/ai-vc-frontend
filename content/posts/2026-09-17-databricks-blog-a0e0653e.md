---
title: The Web Search Your Agent Inherited Isn't Good Enough
title_original: The Web Search Your Agent Inherited Isn't Good Enough
date: '2026-09-17'
source: Databricks Blog
source_url: https://www.databricks.com/blog/web-search-your-agent-inherited-isnt-good-enough
author: ''
summary: '[翻译失败，原文如下]


  - Omnigent is a layer that lets engineers define an agent once — model, tools, policies,
  limits — and run it across any harness (Claude C...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-18T06:56:53.141568'
---

[翻译失败，原文如下]

- Omnigent is a layer that lets engineers define an agent once — model, tools, policies, limits — and run it across any harness (Claude Code, Codex, raw API), with Nimble filling the web search slot.
- Building the same agent multiple times across different harnesses wastes engineering time on plumbing, and each harness's bundled web search returns inconsistent, incomplete results with no shared cost tracking, governance, or audit trail.
- One agent definition replaces three rebuilds, model calls route through Databricks Foundation Model APIs for unified cost and governance, and Nimble's web search raised benchmark accuracy from 46% to 71% while cutting search costs in half.

## An agent that needs the outside world

An engineer at a software company is building an agent to keep the company's view of the market up to date. It monitors a few hundred thousand prospects and customer accounts for signals that an account is open to engagement: a new funding round, a leadership change, a product launch, or a hiring surge that indicates budget.

The account records already live in Databricks, in Delta tables governed by Unity Catalog and joined to the company's own usage and pipeline data. But the signals that move an account live outside the company, on the web. The agent's job is to combine the two, continuously, into one coherent and up-to-the-moment picture of every account, so it can tell a salesperson which handful to call this week.

## Version 1.0: a workable mess

The first version isn't one system. It's the same enrichment logic, rebuilt from scratch three separate times, once in each tool the engineer reached for. The first pass runs in Claude Code, where the agentic parts (deciding which accounts need a fresh look, chaining searches, writing the summary) are most of the work. When a colleague mentions that Codex handles a certain kind of batch scripting faster, the engineer ports the enrichment loop over to check. A third copy skips the harness entirely and calls a model directly over the API, for a lightweight nightly job that just needs a single prompt and a response, no tool orchestration required. Same job, three builds, each shaped by whichever tool fit that moment.

Each harness bundles its own tools and its own web search and wires them up its own way, so the engineer builds the same enrichment logic three times, once in each harness's config format. That is where the day goes. Instead of improving how accounts get enriched, the engineer is learning how Claude Code wants its tools declared, why the same MCP server connects differently in Codex, and what the raw API path is missing that the other two had for free.

The tools are not equivalent, and so neither are the results. The web search bundled into one harness returns different data than the next. A source reachable in one is missed in another. Built-in web search tools for LLMs can find high-level information like funding rounds and leadership changes, but miss granular details like tech stack changes. Access to online information is the thing this agent exists to produce, but its quality now depends on web search that can’t reliably surface key details on the web.

And nothing sits above the three of them. No shared meter, so no one can see or cap what a cycle costs across a few hundred thousand accounts. No shared rulebook, so which sources an agent may read and when a human signs off are set three ways or not at all. No shared record, so when a result is wrong, there is nowhere to reconstruct what the agent read, spent, or decided.

It sort of works in that it produces a result. And that is exactly why it never gets fixed. It works well enough to keep, but not enough to fully trust.

## Omnigent: one definition, any harness

Omnigent is the layer that reins in the sprawl. It sits above the individual harnesses, so the engineer defines the agent once, the model it runs on, the tools it can reach, the policies and limits it operates within. The three rebuilds collapse into one definition, and the engineer's attention goes back to account enrichment. Tools stop being whatever each harness came bundled with and become declarations on the agent, set once and swapped freely. Running on a Databricks-hosted model, the model calls route through the Foundation Model APIs, where every call is captured for cost, audit, and governance in one place instead of scattered across three runtimes. And when the model or the economics change, the engineer changes one line, picking a new model or downshifting to a cheaper one without disruption.

That closes most of the sprawl, but it leaves one critical thing decided by default rather than by design. Web search is one of the core capabilities every harness bundles, and no two bundle the same one. The same query gives one result through Claude Code and another through Codex. Omnigent provides you the ability to define a consistent choice across each task, but it does not make the decision for you. You have to assign a partner search capability. With a partner like Nimble, you can put something in the slot that adapts to the task instead, and give every harness underneath the same expert read.

## Nimble: filling the search slot

Nimble’sSearch APIcan ground answers in fresh, real-time web data through live search. For deep research tasks, Nimble’sWeb Search Agentsautomate web search and extraction orchestration to fulfill your task, working many sources, cross-checking them, and returning an answer with the citations to back each claim, an audit trail that the general path could never produce.

While general web search tools treat every use case the same, Nimble specializes in the agent’s specific use case, self-learns the best retrieval methods, and adapts web search and crawling to go deep into the domain to capture data that generic search tools miss. It gets to the data behind JavaScript, filters, and pagination that an ordinary crawler gives up on. And because it remembers the best way to retrieve the relevant data, it reuses data retrieval paths rather than rediscovering everything from scratch to reduce token costs. Named as the provider in the config, this is the fast path to a more complete web context for your agents.

InNimble's testing, adding Nimble’s web search raised LLM benchmark accuracy from 46 percent to 71 percent, while cutting web search costs in half (ClaudevsNimbleweb search costs). Web Search Agents can be pointed at a domain and kept there, so it remembers which sources and which retrieval paths produced the right data and reuse them the next time. It gets sharper the longer it works a domain, and the cost of rediscovering where a signal lives drops on the accounts it runs against most.

## Version 2.0: built once, on Databricks and Nimble

Returning to the engineer, the agent is now on a path to becoming a coherent, manageable, trustworthy whole. The agent is defined once in Omnigent, on a Databricks-hosted model, with its tools, policies, and limits in a single spec. The three rebuilds are gone. So is the plumbing tax; the engineer is back on enrichment, not on how each harness wants its tools declared.

Web search is now one decision instead of three. Naming Nimble on the web_search builtin points every harness underneath at the same Nimble Search API for fast and efficient web search:

For the accounts that need a defensible answer rather than raw web data, Omnigent can reach for Nimble's Web Search Agents, which automate web search and extraction for research, enrichment, or dataset building.

The key comes from a Nimble account, which you canstart free.

Control now has one home. Model calls route through the Foundation Model APIs under governance, cost is visible and capped in one place, and what the agent reads, spends, and decides is captured consistently across one governance surface.

[翻译失败，原文如下]

And the two halves of the picture finally sit together. The internal record in Databricks and the external signal from Nimble, in one place, governed and read by one agent. Version 1.0 was three harnesses and no vantage point. This is one agent, grounded in what the company knows and what the web can tell it, running where the data already is. Consistent where it used to drift, deep where it used to be shallow, and full governance over external web context retrieval.

## Try it today

Standing this up takes two steps.

Connect Omnigent to Databricks.Databricks runs the Omnigent server for you. On your own machine, install the CLI with the Databricks integration and register the machine as a host:

![](/images/posts/628ae436db8f.png)

Then sign in with your workspace identity and run your first agent on a Databricks-hosted model.Omnigent on Databricksis the place to start; it covers the managed setup end-to-end and links the CLI steps. Two prerequisites to check first: the Omnigent Beta has to be enabled for your workspace, and the workspace has to be in a region that supports Unity AI Gateway. For other install methods and requirements, the fullinstall referencehas them.

Your agents run on the managed server, so the same sessions follow you across every surface:

- the terminal, where you installed
- the desktop app, a native window with notifications and a dock badge for agents waiting on you
- mobile, native iOS and Android apps, or the web UI in any phone browser, by entering your workspace URL

Point search at Nimble.Name Nimble on the web_search builtin, the one-line change from earlier, and every Databricks-hosted agent grounds its answers through it. For defensible, auditable work, reach for the research pass. TheNimble connector docscover both. You will need a Nimble key,start a free trialto get one.

The internal record is already yours. This is what it takes to let your agents reason over the rest of the web, with the same platform holding both halves.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[The Web Search Your Agent Inherited Isn't Good Enough](https://www.databricks.com/blog/web-search-your-agent-inherited-isnt-good-enough)
> 
> 翻译时间：2026-09-18 06:56
