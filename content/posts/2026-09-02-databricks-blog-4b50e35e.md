---
title: Announcing the Databricks Big Book of AgentOps
title_original: Announcing the Databricks Big Book of AgentOps
date: '2026-09-02'
source: Databricks Blog
source_url: https://www.databricks.com/blog/announcing-databricks-big-book-agentops
author: ''
summary: '[翻译失败，原文如下]


  - AgentOps is the operating discipline for building, evaluating, governing and improving
  AI agents in production.

  - The Big Book of Agent...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-03T07:04:16.814280'
---

[翻译失败，原文如下]

- AgentOps is the operating discipline for building, evaluating, governing and improving AI agents in production.
- The Big Book of AgentOps provides practical guidance on architecture, evaluation, observability, cost management and stakeholder alignment.
- The book provides a blueprint that combines field-tested architectures, technical best practices, stakeholder alignment playbooks, and highlights common pitfalls to avoid.

## What is AgentOps?

AgentOps is the operating discipline for building, deploying and improving AI agents in production. It brings architecture, evaluation, observability, governance, security and cost management together into a process teams can repeat.

An AI agent is more than a model producing a response. Agents can choose tools at runtime, retrieve enterprise data, call APIs and work through a multi-step task on their own. Every one of those capabilities is a place where something can go wrong, such as a bad tool call, an overbroad permission or a cost spike nobody planned for.

AgentOps exists to keep that complexity from becoming a liability. Done well, it makes a system reliable enough that people trust it and simple enough that a team can actually run it.

## Why do AI agents need AgentOps?

Generative AI has moved from experimentation into the enterprise faster than most technology waves. The next challenge is turning promising pilots into systems people can depend on.

Most teams stall on the same operational questions:

- Is the agent producing the right result for this task?
- Can we trace what it did, including the tools and data it used?
- How do we control access to sensitive data and actions?
- What will a request cost once it triggers several model calls, retries or guardrail checks?
- Who decides the agent is ready to ship, and who’s watching once it’s live?

Answering those questions takes more than a stronger model. It takes an operating model for the agent itself.

This is familiar territory.MLOpsmatured as teams moved machine learning models out of notebooks and into production.LLMOpsfollowed, adding practices for prompt and model versioning, distributed serving, and cost control. AgentOps is the next layer and extends that discipline to systems that reason, use tools, and take action on their own.

A production agent needs clear boundaries on what its tools can touch, a traceable record of multi-step execution, a way to measure quality, a plan for what happens when something fails, and enough alignment across engineering, product, security, compliance, and finance that nobody is surprised when it ships.

Customer experience bears this out. FactSet’s text-to-code knowledge agent evolved from a single foundation model into a full agent system and delivered a 44% improvement in accuracy.Read the FactSet story.

The Big Book of AgentOps codifies the practices that help enterprise teams make that transition: architecture patterns, a phased delivery pipeline, evaluation and feedback loops, governance, cost management and the stakeholder decisions that determine whether an agent actually reaches production.

## What’s inside The Big Book of AgentOps

The book moves from concepts to implementation across six chapters.

### 1. Understanding AI agent architectures

Agents are not the same as a prompt-and-response LLM call.

Logging, evaluation gates, governance, rollback and monitoring all matter, but requirements shift across four agent architectures. We outline each architecture and their corresponding operational requirements for easy reference.

Also, just as important are the anti-patterns that keep pilots from shipping: starting with a use case that’s too broad, reaching for multi-agent orchestration before the complexity is justified, having an unnecessary reasoning loop an leaving evaluation for later than it should be. We share a list of common ones we’ve seen so similar mistakes can be avoided.

### 2. AI agent deployment architecture patterns

Deployment architectures range from simple to complex depending on a use case and an organizations need. We cover four deployment patterns spanning deploying from a single Databricks workspace to the most complex setup: a multi-account, multi-agent enterprise topology. Each pattern comes with guidance on how to select and evolve between patterns as your needs change. At each stage,Unity Catalog,Unity GatewayandMLflowremain at the core of support the architecture.

### 3. The AgentOps project lifecycle

A seven-phase roadmap starting from how to form a team, select a use-case, through to setting up data infrastructure, evaluation loops, and governance best practices.

We highlight important things to note for each phase. For example, cost is an important part of the lifecycle. A single user request can trigger several model calls once sub-agents, retries and guardrail checks are taken into account. That makes it critical to attribute usage, set limits and establish clear accountability for spend.

### 4. Applying DevOps principles to AI agents

Teams need to iterate quickly to develop a high-quality agent. They also need to evolve and agent based on developments at the frontier of research and in response to the changing needs of their organization. To address this, we highlight how the principles of flow, feedback and continuous-learning, taken fromThe DevOps Handbookprovide a useful foundation for operating AI agent systems.

Applying these principles to agent systems means building a golden evaluation dataset from real traces, calibrating automated judges against subject-matter-expert feedback and using evaluation results to drive what gets built next. A worked example of a customer email agent shows human review, model-based judges and rules-based checks working together without turning every release into a manual audit.

### 5. How to operationalize AI agents

A six-step planning sequence helps teams put effort where it actually changes the outcome: map the human workflow, translate it into a technical architecture, define observability needs by persona, design tracing into the system, map access controls to data and tools and identify what can be reused.

A telecommunications customer-support agent puts the sequence into practice, down to the data schemas, the tools available to a billing sub-agent and the fine-grained controls that keep one customer from ever seeing another customer’s data.

### 6. Managing stakeholders for production AI agents

Good engineering doesn’t guarantee an agent reaches production. Plenty of technically sound projects stall on people problems instead.

Production readiness depends on stakeholders being aligned across the organization, from executive sponsors and product owners to SMEs, security, compliance and finance. This section provides a practical RACI matrix clarifies ownership for decisions that most often get stuck and suggested communication cadences for pre and post-launch project phases. These team processes mean tight SME feedback loops ensure, post-launch operational monitoring and reviews go smoothly, and that projects deliver value for the long term.

## AgentOps best practices for production AI agents

### Start with simple AI agent architectures

Pick one well-defined use case with clear success metrics before reaching for orchestration. Get a working prototype in front of stakeholders early. Let what you learn,not a pre-built roadmap,decide what gets built next.

DXC Technology took this path while expanding its AI portfolio. The company now runs three AI agents in production, has eight more in pilot or development, and cut the platform's total cost of ownership by 30% after migrating to Databricks.Read the DXC Technology story.

### Build AI agent evaluation in from day one

[翻译失败，原文如下]

Evaluation is what lets a team ship an agent with confidence,and keep updating it safely afterward. Start with SMEs reviewing real traces, not a handful of hand-picked chat prompts. That human judgment surfaces failure modes, builds a representative evaluation set and calibrates the automated judges that eventually take over the routine checks.

Databricks builds this directly into the platform: agent evaluation, AI-assisted judges and trace-based analysis that let teams find production issues, dig into root causes and test a fix before redeploying.

Intercontinental Exchange(ICE) put this to work in a governed text-to-SQL application that answers business questions using financial data, achieving 77% syntactic accuracy and 96% execution matches across roughly 50 queries.

### Unify AI agent observability and governance

Controls that reside within individual applications become harder to audit as the number of agents grows. A platform approach gives teams one place to manage data access, model and tool usage, tracing, evaluation, and policy enforcement, rather than reinventing governance for each new agent.

On Databricks, that foundation isMLflowfor evaluation and tracing,Unity Gatewayfor model and tool traffic, andUnity Catalogfor governed discovery, permissions, lineage, and access control across data and AI assets.

Blockis a good example of what a governed foundation buys you. Its Databricks environment supports both AI and operational use cases, with Unity Catalog managing data access across business units. Databricks reports $10 million in productivity gains from Block’s AI agent system for seller operations.

## Who should read it

The Big Book of AgentOps is written for anyone responsible for getting an AI agent into production or keeping it there once it’s live:

- AI, data, software, and platform engineers building and operating agent systems
- Product managers and business owners are accountable for outcomes
- SMEs who define what “good” looks like and review real-world behavior
- Security, compliance, and risk teams are responsible for safe deployment
- Finance and FinOps teams tracking usage, cost, and scale

Anyone whose users depend on the agent's behavior should have this on their desk.

## Get started with AgentOps on Databricks

Read the full eBookto go deeper, and explore the platform capabilities behind production AI agents:

- Build and deploy AI agents on Databricks
- Control and trace your agentic estate with Unity Gateway
- Explore the Databricks AI agent approach
- Review the customer stories

## AgentOps Frequently asked questions

It’s the set of practices for building, evaluating, deploying, governing, observing and improving AI agents once they’re live, and the operational discipline that keeps a system reasoning, using tools, and taking action reliably.

Because so much can happen between a request coming in and an answer going out: tool calls, retrieval, permission checks, retries, and orchestration. Each of those affects quality, risk, latency, or cost, and none of them show up if you’re only watching the model’s final output.

### What does The Big Book of AgentOps cover?

Agent landscapes and anti-patterns, deployment architectures, a seven-phase project pipeline, evaluation and feedback loops, DevOps practices adapted for nondeterministic systems, high-leverage planning activities, and stakeholder management.

### How do I get started with AgentOps on Databricks?

Pick a narrow use case with measurable success criteria. Build an evaluation set from real examples, trace what the agent actually does, apply least-privilege governance and settle on an operating cadence before you expand into more complex orchestration.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Announcing the Databricks Big Book of AgentOps](https://www.databricks.com/blog/announcing-databricks-big-book-agentops)
> 
> 翻译时间：2026-09-03 07:04
