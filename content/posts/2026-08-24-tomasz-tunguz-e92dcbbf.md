---
title: How Long Should an AI Agent Live?
title_original: How Long Should an AI Agent Live?
date: '2026-08-24'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/how-long-should-an-agent-live/
author: ''
summary: '[翻译失败，原文如下]


  In short :When designing an agent, should its session run for your entire five-year
  company tenure or reset every day? Perpetual sessions...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T02:58:58.370104'
---

[翻译失败，原文如下]

In short :When designing an agent, should its session run for your entire five-year company tenure or reset every day? Perpetual sessions suffer from context rot and security exposure. The winning architecture is a daily coordinator that resets every 24 hours, delegating to ephemeral specialists and persisting state to local files.

Mary, Mary, quite contrary, how long do your agents live?

New products likeGrok Bot& othermeta-harnessesask us to create agents. How long should they live?

When you design a calendar agent, how long should its session run? Should it stay alive for your entire five-year tenure at a company, or reset every day?

![Grok Bot specialized agent interface showing dedicated calendar, email, and news agents](/images/posts/12db3db0d573.jpg)

Ever more powerful models tempt us to build perpetual sessions that never close. But long-running sessions rot from the inside out.

As conversational turns pile up, attention degrades. Modern models easily spot a single fact in a long document. But research shows even across frontier models, agent memory is like human memory : it degrades as it grows.1

Temporary commands turn into permanent ghosts. Tell your bot in March, “I have a cold this week, cancel morning meetings,” & by November it is still avoiding morning slots.

Long sessions also break security. An agent holding multi-year read & write access to your inbox & calendar is an open door. One malicious email or calendar invite can poison the conversation, quietly hijacking your schedule months down the road.2

The winning pattern is simple : give your daily assistant a 24-hour life, & delegate individual tasks to narrow specialists.

A daily reset matches how humans actually work. During the day, your assistant remembers immediate context : “I’m running fifteen minutes late,” or “keep two to three free for prep.” At midnight, the active conversation wipes clean so tomorrow starts fresh.

When work needs doing, the daily coordinator hands the job to a single-purpose helper : a calendar agent to schedule, an email agent to draft a reply, or a news agent to search the web. Each helper lives for thirty seconds with only the specific tools it needs, does the job, & disappears.3

For the daily coordinator, the system prompt acts as a dispatcher :

```text
You are Tomasz's daily coordinator.
Your session lives for 24 hours.

Workflow:
- Morning: Load preferences from `preferences.md`
  & today's calendar.
- Intraday: Do not execute directly. Delegate
  to sub-agents (`calendar_bot`, `email_bot`).
- Night: At midnight, save durable learnings
  to `preferences.md` and terminate.

```

For the calendar helper, the system prompt is a stateless executor :

```text
You are an ephemeral calendar specialist.
Process this single request, call the tool,
report the result, & terminate.

Rules:
- Time zone: America/Los_Angeles.
- Duration: 30 minutes.
- Hours: 9:00 AM – 6:00 PM.
- Always check availability first.
  Never double-book.
- If full, propose 2 nearest openings & stop.

Output: Return event title, time, & attendees,
then exit.

```

Before the day’s session wipes at midnight, a quick consolidation pass runs. An offline summarizer reviews the day, saves lasting preferences (“Tomasz prefers thirty-minute meetings”) into a permanent note on disk, & throws away the rest of the daily chatter.4

Does Grok Bot or your chat assistant perform this sleep cycle automatically?

Not today. Most bots leave threads open forever until you click “+ New Chat” or context compaction silently erases your rules.

![An editorial line illustration of a robot kneeling in a garden, carefully cultivating rows of cockle shells and silver bells](/images/posts/5ed4e1d7f5d3.jpg)

The nursery rhyme asks about a garden : silver bells & cockle shells, all in a row. Things that persist, in an order someone chose. The answer for an agent is the same : throw away the conversation ; keep the rules in a file to keep your agent & its garden healthy.

1. Amirali Ebrahimzadeh and Seyyed Muhammad Salili,“Not All Needles Are Found: How Fact Distribution and Prompting Shape Inference in Long-Context LLMs,”arXiv:2601.02023, January 2026; Kelly Hong et al.,“Context rot: How increasing input tokens impacts LLM performance,”Chroma Research, 2025.↩︎
2. “Sleeper Memory Poisoning in LLM Agents,”arXiv:2605.15338, May 2026. Demonstrates persistent cross-session memory poisoning attacks in stateful AI assistants.↩︎
3. Shiyang Chen,“Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents,”arXiv:2606.22528, June 2026. Demonstrates that compaction drops standing rules in 30–59% of episodes.↩︎
4. Anthropic,“Dreams: Memory Consolidation,”research previewdreaming-2026-04-21, April 2026; and the Letta v2 stateful agent framework (2026).↩︎

Amirali Ebrahimzadeh and Seyyed Muhammad Salili,“Not All Needles Are Found: How Fact Distribution and Prompting Shape Inference in Long-Context LLMs,”arXiv:2601.02023, January 2026; Kelly Hong et al.,“Context rot: How increasing input tokens impacts LLM performance,”Chroma Research, 2025.↩︎

“Sleeper Memory Poisoning in LLM Agents,”arXiv:2605.15338, May 2026. Demonstrates persistent cross-session memory poisoning attacks in stateful AI assistants.↩︎

Shiyang Chen,“Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents,”arXiv:2606.22528, June 2026. Demonstrates that compaction drops standing rules in 30–59% of episodes.↩︎

Anthropic,“Dreams: Memory Consolidation,”research previewdreaming-2026-04-21, April 2026; and the Letta v2 stateful agent framework (2026).↩︎

---

> 本文由AI自动翻译，原文链接：[How Long Should an AI Agent Live?](https://www.tomtunguz.com/how-long-should-an-agent-live/)
> 
> 翻译时间：2026-08-26 02:58
