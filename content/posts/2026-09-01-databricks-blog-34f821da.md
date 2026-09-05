---
title: How we eliminated $1 million a year of wasted AI agent spend in one hour
title_original: How we eliminated $1 million a year of wasted AI agent spend in one
  hour
date: '2026-09-01'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-we-eliminated-1-million-year-wasted-ai-agent-spend-one-hour
author: ''
summary: '[翻译失败，原文如下]


  • Broken MCP tool calls silently cost real money. Across our agent fleet, seven
  small MCP-server bugs burned ~$499K/year in tokens and 12...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-05T06:35:34.644971'
---

[翻译失败，原文如下]

• Broken MCP tool calls silently cost real money. Across our agent fleet, seven small MCP-server bugs burned ~$499K/year in tokens and 12,000 eng-hours/year ($1.2M lost) because agents quietly retry instead of surfacing failures.• Observe, then fix. Unity Gateway traces every MCP tool call, while Genie One lets teams surface the biggest sources of wasted AI spent using natural language. Our coding agents shipped the fixes in one hour from start to finish.• Design tools for how LLMs actually use them. Models make guesses on ambiguous inputs, so tools should handle variations gracefully rather than crash on unexpected inputs.

Databricks engineers rely heavily on AI agents to streamline and accelerate their work. In turn, these agents require access not only to different Foundation Models but also to MCP servers with tools that enable access to relevant artifacts (e.g., system logs, usage tables, support tickets, wikis). In aprevious blog, we shared that managing AI costs at scale requires optimizing not only model selection but also how agents use tools. In this post, we describe how we looked for cost savings in our agents' use of tools, the challenges we hit along the way, and how OTel tracing in Unity Gateway cut the path from analysis to $1.2M/year in savings to a single hour.

Enabling our developers to build their agents was a huge unlock on productivity, but as usage ramped up, we also faced increasing costs. We started investigating several optimizations, and one suspicion that we had was the hidden cost of failing tool calls. Specifically, when tools misbehave, the calling agent rarely fails loudly. Instead, it retries, guesses, and eventually works around the problem, quietly burning tokens and developer time the whole way. This type of waste is dangerous: from the outside, the task still completes, and an aggregate cost dashboard may show a 10% bump in token spend that can be easily misinterpreted as usage growth.

We investigated this suspicion in our agent fleet using Unity Gateway'stracingandGenie One. We found seven small bugs in our tool servers that were costing an estimated$499K/year in wasted tokensand about 12,000 engineering hours per year in agent wait time. Overall, this is an estimated$1.2M/yearin lost productivity.

Finding all seven bugs, quantifying them, and fixing them took about an hour. This post describes the process we followed and what it taught us about building tools for agents.

## How to monitor AI agent and MCP activity

When we first deployed AI agents widely at Databricks for coding and internal workflows, it was impossible to manage or even fully understand costs because we lacked visibility into the agents’ tool calls and overall activity. To solve this, we leveraged Unity Gateway, which automatically emits an OpenTelemetry trace for all MCP tool invocations, including the tool name, arguments, error (if any), token counts, latency, and a session ID that ties calls together. Those traces land in a single table that records exactly what our agents did over any time window. No new instrumentation was required, and the gateway already sits on the path of every call, so the data was readily available.

![](/images/posts/24a8008b5afa.png)

This makes AI agent cost management more actionable, where instead of seeing only aggregate token spend, we can attribute wasted spend to specific tools, errors, and agent sessions.

Now that the data is available, the next step is exploration:

- Which tool errors recur the most?
- When an agent hits one, how many turns does it take to recover?
- What does each error cost in tokens and wall-clock wait time?

Normally, the expensive part of this kind of analysis is the SQL and the schema spelunking. But with Genie One, we just pointed it at the trace table,asked these exact questions in plain English, and got answers back in minutes. Most of our hour went to reading those answers rather than writing queries.

## What the traces revealed: How MCP tool failures drive up AI agent costs

Genie One turned a vague suspicion ("agents seem to thrash on Jira calls") into a ranked, quantified bug list in minutes. Here is an example from a single 24-hour window, showing bugs in our Jira and Google Drive/Docs tool servers:

Errors/day

Annual token cost

Annual wait time

Repeat rate

Jira: KeyError: 'fields' (get)

$250K

2,500 h

Jira: 'list' object has no attribute 'split'

4,850 h

30.5%

Jira: KeyError: 'fields' (search)

580 h

GDrive: Invalid field selection

2,740 h

54.5%

Jira: unexpected analysis_prompt kwarg

840 h

50.0%

GDocs: find_text required

440 h

14.3%

Jira: quote_from_bytes() expected bytes

$1.2K

66.7%

Total

1,409

$499K

12,023 h

Take the highest-volume bug, 535 failures a day, as an example. The Jira issues.search tool takes a fields parameter, and the server did this:

It expected a comma-separated string like "key,summary,status". But an array is the semantically natural JSON type for "a list of fields," and that is what the model inferred from its background knowledge of JSON conventions and from adjacent tool calls in the same session. So it passed the structured value that a reasonable caller would:

A list has no .split(), so the server raised 'list' object has no attribute 'split', a raw Python traceback that tells the agent nothing about what it did wrong. So the agent guessed again. Sometimes it retried the same list and failed the same way; sometimes it re-read the schema or fell back to trial and error. On average, it took12 turnsto recover, and 30% of sessions hit the error more than once. One .split() call was costing an estimated $87K/year in tokens and 4,850 hours of agent wait time.

The Google Drive Invalid field selection error was even more striking in volume:49.6% of alldrive_file_getcalls failed, because the model kept passing valid-looking Drive API field names (id, name, mimeType) that the tool's endpoint did not accept.

## The real lesson: How to design MCP tools for AI agents and LLMs

The obvious takeaway is "write better error messages," and the data backs it up. Recovery cost tracks error-message quality almost perfectly:

Error message quality

Example

Avg turns to recover

Self-documenting

"find_text and replace_text required"

Somewhat informative

"Missing required parameters: org, repo"

Cryptic traceback

"'list' object has no attribute 'split'"

Misleading

"unexpected keyword argument 'analysis_prompt'"

But "good error messages help" is old news. The more interesting question iswhythe model called these tools "wrong" in the first place. In most of these cases, it didn't.

MCP tool signatures are often deliberately under-specified. We keep them loose on purpose: partly for generality, and partly to save context tokens, since every parameter description costs tokens the model pays for on every call. The consequence is that when a signature is vague about fields, the model fills the gap with a reasonable guess, and a JSON array is a reasonable guess for a list of fields. The bug was not that the model called the tool incorrectly. It was that the server accepted only one of several reasonable interpretations and crashed on the rest.

So the design principle is the reverse of the reflexive one:tools for agents should adapt to the way LLMs naturally call them,e.g., coerce the list into a string, default the omitted parameter, absorb the unexpected argument, and so on. An under-specified signature is a promise of flexibility, and the tool should honor that promise on the receiving end rather than crash on the first input that doesn't match the one shape its author had in mind.

## The easy part: How we reduced wasted AI agent spend in one hour

[翻译失败，原文如下]

The fixes themselves were simple and are not the interesting part of this story. Once Genie One had handed us a ranked list of which errors to fix and what the model was actually sending, applying the fixes across the tool servers was a quick pass with a coding agent. The whole loop (find, quantify, fix) took about an hour.

The scarce, expensive step was never writing the fix. It was knowing what to fix. Tracing plus Genie One turned that step from a research project into a question you can ask out loud.

## Closing the loop: How to continuously monitor and reduce AI agent costs

As more real work shifts onto agents, silent tool failures become a first-class cost center, the kind that hides inside "usage growth" and never pages anyone. The loop for catching them is cheap and repeatable: Unity Gateway makes agent behavior observable, and Genie One makes that behavior queryable without SQL.

Together, this gives teams a repeatable way to monitor AI agents, diagnose MCP tool failures, and reduce wasted AI spend. If you run agents against your own tools, do the same. Trace the calls and ask Genie One what keeps going wrong.

## Get started with Unity Gateway trace analysis with Genie One

Unity Gateway is Generally Available, and you can now monitor all AI activity using the unified trace table, which is now in Beta. Seeour docson how to get started.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How we eliminated $1 million a year of wasted AI agent spend in one hour](https://www.databricks.com/blog/how-we-eliminated-1-million-year-wasted-ai-agent-spend-one-hour)
> 
> 翻译时间：2026-09-05 06:35
