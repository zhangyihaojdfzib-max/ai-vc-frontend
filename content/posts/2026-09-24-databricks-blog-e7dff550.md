---
title: How I built agent-based security reviews on Databricks
title_original: How I built agent-based security reviews on Databricks
date: '2026-09-24'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks
author: ''
summary: '[翻译失败，原文如下]


  - An agent-based review layer on Databricks automates predictable security work
  while routing novel, high-risk, or ambiguous cases to hum...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-24T07:29:17.452438'
---

[翻译失败，原文如下]

- An agent-based review layer on Databricks automates predictable security work while routing novel, high-risk, or ambiguous cases to human reviewers.
- Unity Catalog, Databricks-hosted foundation models, Lakeflow Jobs, and Databricks Apps provide a governed stack for intake, reasoning, workflows, evidence, and metrics.
- Evidence-based decisions, conservative escalation, and operational dashboards improve cycle time and consistency without removing human authority.

We already had automation in parts of our security review process. It was useful, but it did not reduce the manual work enough.

I kept seeing the same pattern in the queue: a routine integration using a familiar design could sit next to a genuinely novel, high-risk architecture, both waiting for the same scarce resource, an experienced reviewer.

The issue was not that our existing automation had failed. It had simply reached its limits. We were still spending expert time on predictable work, leaving less room for the decisions that truly required expert judgment.

So I built an agent-based layer to extend what we already had. The goal was not to replace the process or the people behind it. It was to help the system understand a request, apply our standards, ask for missing information, and recognize when a person needed to step in.

The first agent-based version focused on one review path. My team saw the broader pattern and expanded it into a set of agents that now support additional parts of our security intake and review process. I built that first version entirely on Databricks, the same platform our customers use.

## Why the platform mattered

I could move quickly because the core pieces were already available in one environment.

Unity Catalog provided a governed space for our security standards, request data, supporting evidence, decisions, and system outputs. Databricks-hosted foundation models provided the model layer for classification and reasoning. Lakeflow Jobs orchestrated the notebook-based workflows on serverless compute. Databricks Apps delivered the intake experience and the executive dashboard.

## How the pieces fit together

At a high level, a request flows through the platform in one continuous path, with every step reading from and writing to the same governed tables:

1. Intake- A conversational app built on Databricks Apps turns a plain-language description into a structured request and attaches any supporting design documents.
2. Reasoning- Databricks-hosted foundation models (Claude Haiku, Sonnet, and Opus) classify the request, assess risk, and draft requirements, always grounded in our security standards. Haiku handles lightweight classification, Sonnet handles most review work, and Opus is reserved for the heaviest reasoning.
3. Orchestration- Lakeflow Jobs run the review agents on serverless compute, moving each request through its stages on a schedule.
4. System of record- Unity Catalog holds the standards, request data, evidence, model outputs, and decisions as governed tables, with one permission and lineage model across all of it.
5. Observability- A second Databricks App reads those same tables to report on volume, risk mix, automation rate, and time saved.

![image2.png](/images/posts/7f85963cac3a.png)

This gave us a consistent governance and operational model across the data, models, workflows, and applications. Instead of assembling separate services with different permissions, logs, and data paths, I could focus on the review logic and user experience.

The practical difference was speed. I had a working system in under two hours. Doing the same thing by wiring up separate services would have taken weeks.

## Not every review needs the same path

Most security queues contain both predictable requests and genuine exceptions.

An integration that uses an approved authentication pattern and does not handle sensitive data is not the same decision as an internet-facing service that processes sensitive information with broad administrative access. Yet a traditional queue can send both through the same manual path.

I wasn't aiming to automate every review. I automated the repeatable parts and preserved human judgment where the risk or uncertainty was higher.

That led to a simple rule: automation for well-understood cases within explicit criteria; people for novel, high-risk, or ambiguous decisions.

## A better front door

Review quality depends on the information available at the start.

Static forms expect requesters to know which review they need, to understand security terminology, and to anticipate the evidence a reviewer will request. When they do not, the request arrives incomplete, and the review begins with another round of questions.

I built a conversational intake application with Databricks Apps. A requester describes what they are trying to do in plain language. The application identifies the likely review path, asks context-dependent follow-up questions, and can use a built-in design document as supporting context. It highlights missing information and provides a preliminary risk indication before a formal request is created.

Once it has enough context, it creates a structured request for the security team.

The application also has a consultation mode grounded in our security standards. Not every question needs to become a ticket. Teams can get guidance while they are still shaping a design and open a formal review only when one is warranted.

This became one of the most useful parts of the system. It lets people make progress sooner, rather than treating the queue as the only way to engage security.

## How the agents work

Behind the intake application is a collection of focused agents implemented in Databricks Notebooks and orchestrated with Lakeflow Jobs.

I deliberately avoided building a single agent with broad authority to act as a security reviewer. Each agent has a bounded responsibility: collect context, assess risk, map the request to relevant standards, draft requirements, manage follow-ups, or prepare a handoff to a person.

## Seven focused agents, each with one job

It is a set of focused agents - not one general agent, and not a single script - each with a narrow job, orchestrated as scheduled jobs behind the intake application:

- Intake agent- Runs the conversational front door: identifies the review path, asks context-dependent questions, and assembles a structured request.
- Risk assessment agent- Assigns a risk tier with supporting evidence, and defaults to a higher tier when the picture is incomplete.
- Requirements agent- Maps a request to the relevant standards and drafts implementation-specific requirements for well-understood cases.
- Specialized review agents- Handle request types that need dedicated logic, such as browser-extension threat modeling and third-party vendor assessment.
- Validation agent- Builds a per-item validation checklist for higher-risk requests before anything closes.
- Workflow agent- Handles follow-up work: clarifications, reminders, acknowledgment tracking, and person escalations.
- Learning agent- Periodically compares reviewer edits against the original output to surface improvements to prompts and standards.

Each agent has bounded responsibility, so its behavior remains inspectable and testable, and a change to one does not silently affect another.

The system first evaluates the request’s risk and records the evidence supporting that assessment. A risk label by itself is not enough.

When information is missing or contradictory, the system asks for clarification or routes the request to a reviewer. It does not infer its way to approval.

[翻译失败，原文如下]

For routine requests, the agents generate requirements based on the actual architecture and the applicable standards, rather than returning generic boilerplate. The requester acknowledges those requirements and provides the necessary evidence. Eligible low- and medium-risk requests may be completed through the automated path once the defined criteria and validations are satisfied.

### An example

Take a common case: an internal integration that uses an approved single-sign-on pattern and handles no sensitive data. Instead of generic boilerplate, the requirements agent produces specific, checkable items tied to that architecture - for example:

- Authenticate through the approved identity provider and disable any local or shared credentials.
- Restrict the integration to the minimum necessary access scopes, and document them.
- Send application and access logs to the central logging pipeline.
- Confirm the data classification level and re-review before any sensitive data is introduced.

The requester acknowledges these items and attaches evidence. If everything checks out and the case meets the eligibility criteria, it can be completed via the automated path.

High-risk, critical, unusual, or ambiguous requests go to a person. By that point, the reviewer receives a structured summary, supporting evidence, applicable standards, and any remaining open questions.

The agents also handle much of the administrative work around a review: collecting missing details, sending reminders, tracking acknowledgments, and escalating when someone asks for help. A reviewer is brought in when a request becomes ambiguous or needs judgment.

Automation operates within rules we define. People retain control over exceptions and consequential decisions.

## Making the system trustworthy

The hardest part was not getting a model to produce an answer. It was making that answer constrained, reviewable, and appropriate for action.

The agents are grounded in our security standards. Risk assessments must include supporting evidence. Missing context triggers a follow-up or escalation, not an optimistic assumption. Automated completion is limited to predefined request classes and criteria. The workflow records the inputs, outputs, evidence, and decisions associated with each request.

## What that looks like in practice

Three things make an automated decision safe to act on:

- Predefined request classes.Only well-understood, lower-risk categories are eligible for automated completion - for example, a routine internal integration on an approved pattern that handles no sensitive data. Anything outside those classes is routed to a person by default.
- Acceptable evidence.A decision is only as good as what backs it. Evidence means concrete, verifiable artifacts: a linked design document, a stated data classification level, or configuration and references demonstrating that an approved control is in place. An assertion with no evidence is treated as missing information.
- A rejected or uncertain assessment.When evidence is missing or contradictory, the system does not guess. It defaults to the more conservative risk tier, posts a specific clarification request, or hands the request to a reviewer with the open questions attached. It does not find its way to approval.

Reviewer feedback helps us identify gaps and improve the system over time. We use those corrections to refine our standards, prompts, and workflow logic rather than allowing the agents to change production behavior on their own.

Those controls matter more than the model itself. A strong model can improve reasoning, but trust comes from the system around it: clear scope, explicit evidence, conservative escalation, and human authority that gives risk real weight.

## Where my team took it

I built the first agent-based version to improve one review path. My team recognized that the same pattern could support much more.

They expanded the architecture to additional request types, hardened the workflows, improved how the agents apply our standards, and added the controls needed for daily use. What began as a single agent-based workflow has become a shared system that the team continues to develop.

I started it, but the system became valuable because the team made it operational and made it theirs.

As a builder, I am proud that the first version worked. As a leader, I am more proud that the team saw a foundation worth extending.

## Measuring the outcome

Efficiency claims are easy to make and hard to trust without evidence.

I built an executive dashboard as another Databricks App. It reads from the same Unity Catalog data produced by the review workflows and tracks request volume, risk distribution, automated completion, human escalation, cycle time, and estimated time saved by reviewers.

Because the metrics come from operational records, we can trace them back to the requests and decisions that generated them, rather than manually reconciling exports from separate systems.

It changed the conversation with leadership. We could show where automation reduced manual effort, where reviewers remained engaged, and how the mix changed over time.

## The numbers

The dashboard tracks a consistent set of measures, all derived from the same operational records.

![Dashboard (with some of the internal-only data redacted).](/images/posts/4c1a116ad837.png)

## What changed

Eligible routine requests that once waited in the queue for days can now be completed in minutes. Teams can receive guidance before opening a ticket, and requests that do reach a reviewer arrive with better context.

Our security engineers can spend more time on novel designs, meaningful risks, and decisions that require experience. The first pass is also more consistent because requests are evaluated against the same standards and evidence requirements. When the system is uncertain, it escalates.

This is not security without people. It is a system designed to use expert attention where it has the greatest value.

## What I took from the experience

Adding reviewers can increase capacity, but it does not remove repetitive work.

The first step is to separate process from judgment. Automate repeatable steps only when the criteria are explicit, the system is grounded in real standards, evidence is required, uncertainty is escalated, and outcomes can be measured.

Do not automate a decision simply because a model can produce an answer. Automate it only when the process defines what an acceptable answer looks like, what evidence supports it, and what happens when the system is unsure.

Keep people in control of consequential decisions and exceptions.

My intent was not to remove humans from security review. I set out to reduce the time they spend on work that a controlled system can handle consistently. Building on Databricks gave us the platform foundation to do that. Watching my team take the first version, strengthen it, and make it theirs has been the best part.

Start with the Databricks multi-agent guide, then adapt the pattern from this post - governed data in Unity Catalog, focused agents on Lakeflow Jobs, and a Databricks App as the front door - into your own repeatable, evidence-based review workflow.

Build a multi-agent system on Databricks Apps

---

> 本文由AI自动翻译，原文链接：[How I built agent-based security reviews on Databricks](https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks)
> 
> 翻译时间：2026-09-24 07:29
