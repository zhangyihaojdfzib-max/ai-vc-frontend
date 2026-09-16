---
title: How Delphi ships 100 times a day with its Python backend on Vercel | Customers
  | Vercel
title_original: How Delphi ships 100 times a day with its Python backend on Vercel
  | Customers | Vercel
date: '2026-09-15'
source: Vercel Blog
source_url: https://vercel.com/blog/how-delphi-ships-100-times-a-day-with-its-python-backend-on-vercel
author: ''
summary: '[翻译失败，原文如下]


  ### Copy link to headingDelphi on Vercel


  - 10 engineers with no dedicated infrastructure role

  - Everyone ships code, including product a...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:53.577652'
---

[翻译失败，原文如下]

### Copy link to headingDelphi on Vercel

- 10 engineers with no dedicated infrastructure role
- Everyone ships code, including product and design
- 100+ production deploys a day behind feature flags

10 engineers with no dedicated infrastructure role

Everyone ships code, including product and design

100+ production deploys a day behind feature flags

Delphibuilds digital minds. They capture what someone has written, recorded, and taught, so anyone can tap that expertise on demand. Delphi is “a destination where you can find and interact with interesting minds,” says founding engineer Spencer Schoeben.

Nobody has built a digital mind network before, so Delphi figures out what to build by shipping features and watching how people use them. That only works if the product is fast to change. "If we are going to win, we need to have an excellent developer and agentic experience," Spencer says. "Otherwise, we could not adapt to how fast our user’s demands change."

![A screen capture of a Delphi digital mind conversation. ](/images/posts/ecbda45c8fea.jpg)

![A screen capture of a Delphi digital mind conversation. ](/images/posts/d7bedc288ebe.jpg)

Delphi's frontend had run on Vercel since day one. "The frontend has always been easy," Spencer says, "but the backend was a nightmare." Six months ago, the team rebuilt its Python backend on Vercel as well. Today the whole team ships to production 100+ times a day.

## Copy link to headingBuilding a Python backend that's easy to work on

### Copy link to headingThe backend slowed every change

Delphi's backend previously ran on AWS, with ECS, Docker Desktop, and local databases. In the earliest days, the setup worked because the team was small and much of the context lived in people’s heads. As Delphi grew, that made onboarding slower than the team wanted: getting a new engineer to their first deploy took a full day of environment setup.

Delphi could have fixed that without leaving AWS. But fixing it properly would have meant designing and owning the infrastructure themselves, and the team didn't want to own infrastructure at all. "That is not our current goal as a company," Spencer says. After moving the backend to Vercel, new engineers could get to production much faster, with the same deploy workflow the rest of the team used every day.

## Copy link to headingWorkflows and Queues made the move possible

When Delphi was founded,Vercel WorkflowsandVercel Queuesdidn't exist. Without them, Spencer says, the move would have been much harder, if possible at all.

Delphi's backend depends on long-running work and queued background jobs. Digital minds need durable agents that generate content ahead of time, plus ingestion that turns a person's books and talks into a knowledge graph.

Workflows handles the long-running work and Queues handle the background jobs. Neither requires setup. A developer writes the workflow or the queue handler as a function in the codebase, and Vercel provisions what's needed to run it on deploy.

## Copy link to heading100+ deploys a day, straight to production

Moving the backend to Vercel let Delphi stop treating backend changes as heavyweight releases and ship them as everyday product work. The team used to deploy to staging, then production. Now it skips the middle step, shipping 100+ times a day behind feature flags and running A/B tests instead of batching changes into a release.

Vercel Agent'sanomaly detection watches production at that pace, flagging when something is misbehaving and why. Before, Spencer says, they often would not have known.

Moving fast has helped clear a backlog of small experiments that never used to make the priority list. Many of those experiments test how to turn a visitor into an owner, someone who arrives to talk to a mind and leaves having started their own.

Shipping isn't limited to engineers, either. Delphi's CPO and its growth teams build and deploy dashboards, prototypes, and experiments themselves, which Spencer says wouldn't have happened on the old setup.

## Copy link to headingInfrastructure built for agents and engineers

### Copy link to headingPreview deployments are how agents check their work

Delphi's engineers hand problems to cloud agents, with very little development happening locally. The preview deployment is where they first see what the agent built. Vercel preview deployments give every push its own live URL, so anyone can check the result from a phone or a Slack thread without pulling the branch.

When an agent fails, it's usually because it couldn't get at the information it needed. Vercel exposes the data and controls agents need through the SDK, MCP, and CLI, so an agent can read logs, inspect a deployment, or change an environment variable through whichever it's using. For Delphi, agents are now the main users of those tools, so the platform has to be as easy for them as it is for people.

## Copy link to headingAn internal agent on Sandbox for customer success

Delphi's own agents run on Vercel as well. One of them, an internal agent onVercel Sandbox, simplifies working with the company's codebase. The customer success team uses Slack to ask it about reported issues, find the problem, and hand an engineer a root cause and a proposed fix.

Edge cases used to fall through the cracks. "Before, we either couldn't get to everything, or we had to spend way more time than we had available," Spencer says. "Now we have an agent they can just ask in Slack."

Vercel Sandbox gives the agent an isolated environment with a file system, where it can check out the codebase, run it, and pull in whatever data a question needs. The agent itself is built with eve, Vercel's agent framework. Delphi's first version ran on a hosted agent platform and could only use the integrations that platform offered. In eve, tools are code Delphi writes, so when a question needs one that doesn't exist, the team adds it.

## Copy link to headingAI Gateway picks the model for each mind

Delphi's chat traffic runs throughAI Gateway.Every digital mind is different, and some come out better on one model than another, so Delphi picks the model for each customer and adjusts as its own evals change. When a new model ships, open-source or otherwise, Delphi can route to it the same day.

Gateway also handles failover. Before, Delphi worked directly with a model provider to line up fallback capacity on other clouds, and it was hard. "With AI Gateway, we always know that we're going to get the fallbacks if they exist," Spencer says.

## Copy link to headingWhat's next

Delphi's first chapter was training digital minds and letting people chat with them. Now it is building the interface beyond chat. Spencer describes a search page where you bring a question, get perspectives from several minds at once, and have the page adapt to who you are.

That work runs as long-running agents on Workflows, with AI Gateway supplying whichever model each experiment calls for.

AboutDelphi:Delphi is a platform that turns a person's knowledge, thinking, and voice into a digital mind others can talk to. Anyone can create their own Delphi to make their expertise discoverable and accessible, part of a network of minds people can seek out, learn from, and converse with.

---

> 本文由AI自动翻译，原文链接：[How Delphi ships 100 times a day with its Python backend on Vercel | Customers | Vercel](https://vercel.com/blog/how-delphi-ships-100-times-a-day-with-its-python-backend-on-vercel)
> 
> 翻译时间：2026-09-16 07:28
